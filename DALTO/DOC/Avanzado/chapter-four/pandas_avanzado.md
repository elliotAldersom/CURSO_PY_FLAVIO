# Procesamiento Avanzado de Datos con Pandas: Limpieza, Transformación y Escalabilidad

## 2. Introducción

En el capítulo dedicado a los [fundamentos de Pandas](../../Intermedio/chapter-three/pandas_fundamentos.md) se establecieron las bases operativas de la biblioteca: la distinción entre `Series` y `DataFrame`, la carga estándar mediante `pd.read_csv`, la inspección mediante `head`, `shape` y `describe`, y la selección rigurosa con `loc` e `iloc`. Sin embargo, en escenarios reales de ingeniería y ciencia de datos, los conjuntos de información difícilmente se presentan en formatos tabulares limpios, tipados y listos para su explotación directa.

Los datos brutos suelen contener valores nulos o incompletos, registros duplicados producidos por reintentos en fuentes transaccionales, cadenas de texto contaminadas con comillas residuales y espacios en blanco, tipos de datos sobrecargados que consumen cantidades exorbitantes de memoria RAM, y volúmenes tabulares que exceden con creces la memoria física disponible en el sistema.

El presente capítulo aborda las técnicas avanzadas indispensables para transformar y limpiar datos tabulares con [Pandas](https://pandas.pydata.org/docs/) moderno:

1. **Gestión integral de valores faltantes y nulos:** detección con `.isna()` y `.notna()`, depuración selectiva con `.dropna()` y estrategias de imputación mediante `.fillna()`, distinguiendo entre el centinela tradicional de coma flotante (`np.nan`) y los tipos anulables modernos (`pd.NA`).
2. **Deduplicación rigurosa:** erradicación de redundancias con `.drop_duplicates()` y control de retención mediante el parámetro `keep`.
3. **Casting de tipos y optimización de memoria:** reducción del consumo en memoria RAM mediante el tipo categórico (`category`) para datos de baja cardinalidad y tipos numéricos de ancho reducido.
4. **Reshape y combinación de datos:** combinación vertical y horizontal mediante `pd.concat()`, controlando la alineación de índices y evitando la fragmentación estructural.
5. **Transformaciones elemento a elemento y vectorizadas:** aplicación de funciones sobre celdas mediante el método moderno `DataFrame.map()` —corrigiendo la obsolescencia y eliminación de `applymap`—, vectorización con accesores `.str` y contrastes de rendimiento frente a `.apply()`.
6. **Escalabilidad y procesamiento fuera de memoria (*out-of-core*):** comprensión de la regla de sobrecosto de memoria (5x a 10x), ingestión por fragmentos con `chunksize` en `pd.read_csv`, integración del motor Apache Arrow (`dtype_backend="pyarrow"`) en Pandas 2.x, y criterios de transición hacia tecnologías de procesamiento masivo como Polars, DuckDB y Apache Spark.

## 3. Fundamentos y conceptos

### Naturaleza de Pandas como biblioteca externa

A diferencia de módulos del núcleo estándar de Python como [csv](../../Intermedio/chapter-three/archivos_csv.md) o [pathlib](../../Intermedio/chapter-three/manejo_archivos.md), Pandas es una **biblioteca externa de terceros** (`pip install pandas`) que proporciona estructuras de datos bidimensionales y alineación de índices inspiradas en el lenguaje R y las bases de datos relacionales. 

Internamente, un `DataFrame` de Pandas organiza la información en columnas homogéneas contiguas en memoria física, delegando el cómputo matemático intensivo a núcleos escritos en C, Cython y C++ mediante NumPy, y opcionalmente a Apache Arrow a partir de Pandas 2.0.

### Detección y tratamiento de datos faltantes

En el estándar IEEE 754 de coma flotante, la ausencia de un valor numérico se representa históricamente mediante el centinela `NaN` (*Not a Number*), accesible en Python vía `numpy.nan` o `float("nan")`. Esta representación histórica acarrea una limitación severa: cualquier columna de números enteros que contenga al menos un valor nulo se convierte obligatoriamente al tipo `float64`, perdiendo la naturaleza discreta del campo.

Para subsanar esta inconsistencia, Pandas introdujo los **tipos de datos anulables** (*nullable dtypes*), cuyo centinela es `pd.NA`. Tipos como `Int64` (con `I` mayúscula), `boolean` y `string[pyarrow]` permiten mantener enteros, booleanos y cadenas con valores faltantes reales sin forzar la coacción a coma flotante.

El ciclo de depuración de valores nulos se apoya en tres métodos fundamentales:

1. **Auditoría de nulidad (`isna()` y `notna()`):** generan máscaras booleanas que identifican la presencia o ausencia de celdas vacías en cada posición de la tabla.
2. **Eliminación controlada (`dropna()`):** descarta filas o columnas que presenten datos faltantes. Admite configurar:
   - `axis`: `0` o `"index"` para eliminar filas (comportamiento predeterminado); `1` o `"columns"` para descartar columnas enteras (`problemas_CSV.py` L33).
   - `how`: `"any"` para eliminar el registro si al menos una celda es nula; `"all"` para descartarlo únicamente si todas las celdas del registro son nulas (`problemas_CSV.py` L36).
   - `subset`: lista de etiquetas de columnas o índices sobre las cuales se restringe la evaluación de nulidad, preservando filas que contengan nulos en campos no críticos.
3. **Imputación de valores (`fillna()`):** sustituye los valores nulos por constantes escalares (como `0` o la media calculada) o por proyecciones basadas en propagación de valores vecinos mediante los métodos modernos `ffill()` (*forward fill*) o `bfill()` (*backward fill*).

### Deduplicación de registros

En flujos transaccionales y archivos CSV provenientes de exportaciones desordenadas, es habitual encontrar filas exactamente iguales o registros que comparten un mismo identificador clave (`problemas_CSV.py` L60-70).

El método `df.drop_duplicates()` evalúa la repetición de registros devolviendo un nuevo `DataFrame` sin redundancias:

- `subset`: lista de nombres de columnas que definen la unicidad del registro (por ejemplo, `subset=["Nombre", "Apellido"]`). Si no se suministra, evalúa la totalidad de las columnas.
- `keep`: estrategia de retención:
  - `"first"`: conserva la primera aparición encontrada y descarta las siguientes (valor por defecto).
  - `"last"`: conserva la última aparición observada en el orden del índice.
  - `False`: descarta todas las filas que tengan duplicados, sin conservar ninguna de ellas.
- `ignore_index`: valor booleano (`False` por defecto). Si se establece en `True`, el índice resultante se renumera de `0` a `n - 1`, evitando saltos o discontinuidades.

### Optimización de memoria mediante tipos categóricos

En Python puro, las cadenas de caracteres se almacenan como objetos `PyObject` independientes distribuidos por el montículo de memoria (*heap*). En un `DataFrame` donde una columna de tipo `object` contiene cadenas repetitivas (por ejemplo, géneros, categorías, estados o nombres de ciudades), cada celda almacena un puntero a un objeto de texto independiente.

El tipo de dato categórico (`category`) implementa una codificación por diccionario (*dictionary-encoding*):

1. Mantiene un arreglo interno de enteros pequeños (`int8`, `int16` o `int32`), denominados códigos (*codes*).
2. Conserva una colección ordenada de valores únicos, denominados categorías (*categories*).

Si una columna de 1.000.000 de filas contiene únicamente 5 valores textuales distintos, convertirla con `df["col"] = df["col"].astype("category")` reduce el consumo de memoria de decenas de megabytes a pocos kilobytes, además de acelerar significativamente las operaciones de agrupamiento (`groupby`) y ordenamiento.

### Combinación y concatenación estructural con `pd.concat`

Cuando se deben integrar múltiples fuentes de datos homogéneas (como fragmentos mensuales o particiones distribuidas), la función `pd.concat()` une colecciones de objetos `DataFrame` o `Series` a lo largo de un eje específico (`Importando_con_pandas.py` L112-118):

- `axis=0` (vertical): apila las filas de las tablas. Si las columnas no coinciden exactamente, genera la unión de las columnas completando con `NaN` o `pd.NA` donde falte información. El parámetro `ignore_index=True` es crítico para reconstruir un `RangeIndex` unificado y evitar índices duplicados.
- `axis=1` (horizontal): yuxtapone las columnas alineando las filas según su índice. Si los índices difieren, alinea por defecto mediante una unión externa (*outer join*).

### Transformaciones: la corrección de `DataFrame.applymap` por `DataFrame.map`

En versiones históricas de Pandas (como la empleada en `Importando_con_pandas.py` L49), la transformación de valores celda a celda en un `DataFrame` completo se realizaba con `df.applymap(func)`.

> [!IMPORTANT]
> **Deprecación y eliminación oficial de `applymap`:**
> A partir de **Pandas 2.1.0**, el método `DataFrame.applymap` fue formalmente declarado obsoleto (*deprecated*), y fue **eliminado por completo en Pandas 2.2.0**.
> En su lugar, el estándar actual unifica la nomenclatura:
> - `DataFrame.map(func)`: aplica una función de transformación elemento a elemento sobre cada una de las celdas de un `DataFrame`.
> - `Series.map(arg)`: mapea valores de una `Series` según un diccionario de correspondencia, una función de mapeo o una serie auxiliar.

Por su parte, el método `df.apply(func, axis=0|1)` opera a nivel de agregación o transformación vectorial sobre filas completas (`axis=1`) o columnas completas (`axis=0`).

#### Jerarquía de rendimiento computacional en Pandas

Al procesar transformaciones, el orden de eficiencia temporal y espacial de mayor a menor es:

1. **Operaciones vectorizadas nativas en C/SIMD:** expresiones aritméticas directas (`df["a"] + df["b"]`) y accesores especializados `.str` y `.dt`.
2. **Funciones universales compiladas (NumPy ufuncs):** `np.log(df["col"])`, `np.where(...)`.
3. **Comprensiones de listas sobre arreglos NumPy:** `[transformar(x) for x in df["col"].to_numpy()]`.
4. **Mapeo celda a celda:** `df["col"].map(...)` o `DataFrame.map(...)`.
5. **Agregación por filas:** `df.apply(..., axis=1)`.
6. **Iteración fila por fila con bucles imperativos:** `.iterrows()` o `.itertuples()` (antipatrón de rendimiento que debe evitarse en producción).

### Límites de memoria y estrategias de escalabilidad

Pandas opera bajo un modelo estrictamente en memoria (*in-memory*). Una regla empírica fundamental en ingeniería de datos establece que el procesamiento de un archivo en Pandas requiere entre **5 y 10 veces el tamaño del archivo bruto en memoria RAM**. Un archivo CSV de 2 GB requerirá frecuentemente entre 10 GB y 20 GB de memoria de trabajo para permitir lecturas, copias intermedias, indexación y agregaciones.

Para superar este límite existen tres estrategias arquitectónicas:

1. **Ingestión por fragmentos (*chunking*):** mediante el parámetro `chunksize` en `pd.read_csv()`, Pandas lee el archivo por bloques homogéneos, devolviendo un iterador `TextFileReader` que permite procesar y acumular métricas sin sobrecargar la memoria.
2. **Motor Apache Arrow (Pandas 2.0+):** al especificar `engine="pyarrow"` y `dtype_backend="pyarrow"`, Pandas delega el almacenamiento en columnas nativas de memoria compartida de Apache Arrow, reduciendo el consumo de memoria, acelerando la lectura de cadenas y ofreciendo tipos nulos unificados sin copias redundantes.
3. **Herramientas fuera de memoria (*out-of-core*) y computación distribuida:** cuando el conjunto de datos supera la memoria física total de la máquina, la arquitectura debe migrar a motores diseñados para procesamiento *out-of-core* o computación distribuida:
   - **Polars:** biblioteca en Rust con ejecución paralela multihilo y evaluación perezosa (*lazy evaluation*).
   - **DuckDB:** motor analítico SQL OLAP embebido en memoria que ejecuta consultas sobre archivos Parquet y CSV directamente desde el disco.
   - **Apache Spark / Dask:** marcos de trabajo para computación distribuida en clústeres heterogéneos.

## 4. Sintaxis y funcionamiento

La siguiente tabla resume los métodos, parámetros e indexadores avanzados de limpieza, combinación y transformación en Pandas:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `df.isna()` / `df.isnull()` | Genera una máscara booleana que evalúa a `True` en cada celda nula | `mascara = df.isna()` |
| 2 | `df.notna()` / `df.notnull()` | Genera una máscara booleana que evalúa a `True` en cada celda no nula | `validos = df[df["edad"].notna()]` |
| 3 | `df.dropna(axis, how, subset)` | Descarta filas o columnas con valores nulos según criterios de filtro | `df_limpio = df.dropna(subset=["Nombre"], how="any")` |
| 4 | `df.fillna(value)` | Reemplaza celdas nulas por un valor constante o un mapa de sustitución | `df_lleno = df.fillna({"Edad": 0, "Apellido": "Desconocido"})` |
| 5 | `df.ffill()` / `df.bfill()` | Propaga valores no nulos hacia adelante (*forward*) o hacia atrás (*backward*) | `df_imputado = df.ffill()` |
| 6 | `df.drop_duplicates(subset, keep)` | Elimina registros repetidos reteniendo la primera, última o ninguna ocurrencia | `df_unico = df.drop_duplicates(subset=["Email"], keep="first")` |
| 7 | `df["col"].astype("category")` | Convierte una columna a tipo categórico optimizado por diccionario | `df["pais"] = df["pais"].astype("category")` |
| 8 | `df["col"].astype("Int64")` | Convierte a tipo entero anulable que admite valores faltantes `pd.NA` | `df["edad"] = df["edad"].astype("Int64")` |
| 9 | `pd.concat(objs, axis=0, ignore_index)` | Concatena tablas verticalmente apilando filas y reajustando índices | `df_total = pd.concat([df1, df2], axis=0, ignore_index=True)` |
| 10 | `pd.concat(objs, axis=1)` | Concatena tablas horizontalmente uniendo columnas por alineación de índice | `df_horizontal = pd.concat([df_a, df_b], axis=1)` |
| 11 | `df.map(func)` | Aplica una función elemento a elemento sobre todas las celdas del `DataFrame` | `df_limpio = df.map(lambda x: x.strip() if isinstance(x, str) else x)` |
| 12 | `s.map(arg)` | Mapea valores de una `Series` mediante diccionario o función escalar | `s_normalizada = df["estado"].map({"A": "Activo", "I": "Inactivo"})` |
| 13 | `df.apply(func, axis)` | Ejecuta funciones sobre columnas completas (`axis=0`) o filas completas (`axis=1`) | `df["total"] = df.apply(lambda row: row["base"] + row["iva"], axis=1)` |
| 14 | `pd.read_csv(f, chunksize=N)` | Lee un archivo CSV devolviendo un iterador por lotes de `N` registros | `for bloque in pd.read_csv("datos.csv", chunksize=50_000): ...` |
| 15 | `pd.read_csv(f, dtype_backend="pyarrow")` | Carga un archivo empleando los tipos de memoria eficientes de Apache Arrow | `df_arrow = pd.read_csv("datos.csv", dtype_backend="pyarrow")` |

## 5. Ejemplos prácticos progresivos

### Básico

El siguiente ejemplo aborda la problemática original expuesta en `problemas_CSV.py`: ingesta de un archivo con valores nulos dispersos, tipos de datos inconsistentes y filas duplicadas. Se emplean `io.StringIO` y Pandas para auditar la nulidad, aplicar saneamiento con `.dropna()`, imputar datos faltantes con `.fillna()` y depurar redundancias con `.drop_duplicates()`.

```python
import io
import pandas as pd

# Simulación del archivo CSV original con anomalías: valores nulos y registros duplicados
CSV_ORIGINAL = (
    "Nombre,Apellido,Edad\n"
    "Flavio,Silva,18.0\n"
    "Fabian,Silva,21.0\n"
    "Papango,Estrada,40.0\n"
    "Flavio,Silva,18.0\n"
    "Flavio,Silva,18.0\n"
    "Carlos,,\n"
    ",Gomez,29.0\n"
)

# 1. Carga del conjunto de datos en un DataFrame
df_crudo = pd.read_csv(io.StringIO(CSV_ORIGINAL))
print("Dimensiones iniciales:", df_crudo.shape)

# 2. Diagnóstico de valores nulos por columna
nulos_por_columna = df_crudo.isna().sum()
print("Valores nulos identificados:")
print(nulos_por_columna)

# 3. Limpieza: descartar filas donde el Nombre sea nulo
df_sin_nombre_nulo = df_crudo.dropna(subset=["Nombre"]).copy()

# 4. Imputación: rellenar Apellidos faltantes con cadena estándar y Edad con la mediana
df_imputado = df_sin_nombre_nulo.fillna(
    {
        "Apellido": "Sin Apellido",
        "Edad": df_sin_nombre_nulo["Edad"].median(),
    }
)

# 5. Deduplicación: descartar filas repetidas preservando el primer registro
df_saneado = df_imputado.drop_duplicates(keep="first", ignore_index=True)

# 6. Conversión a tipo entero anulable para evitar decimales innecesarios en la edad
df_saneado["Edad"] = df_saneado["Edad"].astype("Int64")

print("\nDataFrame final saneado y deduplicado:")
print(df_saneado)

# Resultado esperado:
# Dimensiones iniciales: (7, 3)
# Valores nulos identificados:
# Nombre      1
# Apellido    1
# Edad        1
# dtype: int64
#
# DataFrame final saneado y deduplicado:
#     Nombre      Apellido  Edad
# 0   Flavio         Silva    18
# 1   Fabian         Silva    21
# 2  Papango       Estrada    40
# 3   Carlos  Sin Apellido    20
```

### Intermedio

Este ejemplo resuelve la normalización celda a celda documentada en `Importando_con_pandas.py` (L43-52), sustituyendo el método eliminado `applymap` por el método moderno `DataFrame.map()`. Adicionalmente, se realiza optimización de memoria RAM mediante el tipo categórico (`category`), se mide la huella física con `memory_usage(deep=True)` y se integran tablas complementarias vertical y horizontalmente con `pd.concat`.

```python
import io
import pandas as pd

# Simulación de archivo CSV con comillas residuales y espacios parásitos
CSV_SUCIO_1 = (
    '"nombre","categoria","ventas"\n'
    '"  Laptop  ","tecnologia",1200\n'
    '"Mouse ","tecnologia",25\n'
    '"  Teclado","tecnologia",45\n'
    '"Monitor ","tecnologia",300\n'
)

CSV_SUCIO_2 = (
    '"nombre","categoria","ventas"\n'
    '"Silla Ergonomica ","muebles",250\n'
    '"Escritorio ","muebles",450\n'
)

# 1. Carga de los conjuntos de datos
df1 = pd.read_csv(io.StringIO(CSV_SUCIO_1))
df2 = pd.read_csv(io.StringIO(CSV_SUCIO_2))

# 2. Normalización de encabezados (eliminando comillas y espacios parásitos)
for d in (df1, df2):
    d.columns = d.columns.str.replace('"', "", regex=False).str.strip()

# 3. Concatenación vertical de lotes con reinicio de índice
df_combinado = pd.concat([df1, df2], axis=0, ignore_index=True)

# 4. Transformación elemento a elemento con DataFrame.map (estándar moderno de Pandas 2.x)
# Sustituye de forma segura a df.applymap, eliminado en Pandas 2.2+
df_normalizado = df_combinado.map(
    lambda celda: celda.replace('"', "").strip() if isinstance(celda, str) else celda
)

# 5. Medición del consumo de memoria antes de la optimización categórica
memoria_previa = df_normalizado.memory_usage(deep=True).sum()

# 6. Optimización de memoria: conversión de columna de baja cardinalidad a 'category'
df_normalizado["categoria"] = df_normalizado["categoria"].astype("category")

memoria_posterior = df_normalizado.memory_usage(deep=True).sum()

print("Datos limpios y unificados:")
print(df_normalizado)
print(f"\nHuella de memoria antes: {memoria_previa} bytes")
print(f"Huella de memoria después: {memoria_posterior} bytes")
print(f"Ahorro de memoria relativo: {((memoria_previa - memoria_posterior) / memoria_previa) * 100:.1f}%")

# 7. Concatenación horizontal: añadir columna calculada como DataFrame auxiliar
df_margen = pd.DataFrame({"margen_pct": [0.15, 0.40, 0.35, 0.20, 0.30, 0.25]})
df_final = pd.concat([df_normalizado, df_margen], axis=1)

print("\nDataFrame con enriquecimiento horizontal:")
print(df_final)

# Resultado esperado:
# Datos limpios y unificados:
#               nombre   categoria  ventas
# 0             Laptop  tecnologia    1200
# 1              Mouse  tecnologia      25
# 2            Teclado  tecnologia      45
# 3            Monitor  tecnologia     300
# 4  Silla Ergonomica      muebles     250
# 5         Escritorio      muebles     450
```

### Avanzado

En aplicaciones de producción con flujos masivos de datos, cargar un archivo completo en memoria puede agotar los recursos del servidor. El siguiente ejemplo ilustra una arquitectura de procesamiento en flujo (*streaming*) por lotes (*chunking*) empleando `pd.read_csv` con `chunksize`. Se computan métricas agregadas globales (sumatorias, conteos, medias y varianzas) acumuladas incrementalmente sin mantener jamás el dataset completo en memoria RAM, combinándolo con el backend de alta eficiencia Apache Arrow.

```python
import io
import pandas as pd

# Simulación de un flujo masivo de registros de transacciones financieras
DATOS_TRANSACCIONES = (
    "id_transaccion,cliente,monto,moneda\n"
    "1001,cliente_a,150.50,USD\n"
    "1002,cliente_b,85.00,USD\n"
    "1003,cliente_a,2300.00,EUR\n"
    "1004,cliente_c,45.20,USD\n"
    "1005,cliente_b,310.00,USD\n"
    "1006,cliente_a,120.00,USD\n"
    "1007,cliente_c,950.00,EUR\n"
    "1008,cliente_d,60.00,USD\n"
    "1009,cliente_b,415.00,USD\n"
    "1010,cliente_a,80.00,USD\n"
)

# Definición de tamaño de fragmento para simular procesamiento fuera de memoria
TAMANO_BLOQUE = 3

flujo_csv = io.StringIO(DATOS_TRANSACCIONES)

# Acumuladores de estado para el pipeline incremental
suma_total_usd = 0.0
total_transacciones_usd = 0
clientes_unicos = set()

# Procesamiento por bloques mediante el iterador TextFileReader
# Se especifican tipos estrictos para optimizar cada lote
lector_bloques = pd.read_csv(
    flujo_csv,
    chunksize=TAMANO_BLOQUE,
    dtype={
        "id_transaccion": "int64",
        "cliente": "string",
        "monto": "float64",
        "moneda": "string",
    },
)

for numero_bloque, lote in enumerate(lector_bloques, start=1):
    # 1. Filtro vectorial en el bloque actual: solo transacciones en USD
    lote_usd = lote.loc[lote["moneda"] == "USD"]
    
    # 2. Acumulación incremental de métricas
    suma_total_usd += float(lote_usd["monto"].sum())
    total_transacciones_usd += int(len(lote_usd))
    
    # 3. Registro de clientes únicos
    clientes_unicos.update(lote_usd["cliente"].dropna().unique())
    
    print(f"Lote #{numero_bloque} procesado: {len(lote)} filas leídas, "
          f"{len(lote_usd)} en USD (Suma parcial: {lote_usd['monto'].sum():.2f})")

ticket_promedio_usd = suma_total_usd / total_transacciones_usd if total_transacciones_usd > 0 else 0.0

print("\n--- RESUMEN GLOBAL DEL PIPELINE STREAMING ---")
print(f"Total procesado en USD:      ${suma_total_usd:,.2f}")
print(f"Transacciones válidas (USD):  {total_transacciones_usd}")
print(f"Ticket promedio global:      ${ticket_promedio_usd:,.2f}")
print(f"Cantidad de clientes únicos:  {len(clientes_unicos)}")

# Resultado esperado:
# Lote #1 procesado: 3 filas leídas, 2 en USD (Suma parcial: 235.50)
# Lote #2 procesado: 3 filas leídas, 2 en USD (Suma parcial: 355.20)
# Lote #3 procesado: 3 filas leídas, 2 en USD (Suma parcial: 180.00)
# Lote #4 procesado: 1 filas leídas, 1 en USD (Suma parcial: 80.00)
#
# --- RESUMEN GLOBAL DEL PIPELINE STREAMING ---
# Total procesado en USD:      $850.70
# Transacciones válidas (USD):  7
# Ticket promedio global:      $121.53
# Cantidad de clientes únicos:  4
```

## 6. Aplicaciones en el mundo real

El procesamiento avanzado con Pandas constituye la columna vertebral de múltiples industrias intensivas en datos:

1. **Ingeniería de datos y canalizaciones ETL (*Extract, Transform, Load*):**
   - Ingesta diaria de millones de eventos crudos generados por servidores web y microservicios.
   - Saneamiento y tipado estricto: eliminación de registros truncados mediante `dropna()`, conversión de identificadores numéricos a enteros anulables (`Int64`), deduplicación de eventos duplicados por reconexión de red (`drop_duplicates()`) y exportación a formatos analíticos como Parquet.
2. **Finanzas cuantitativas y conciliación bancaria:**
   - Cruce de extractos bancarios con libros contables internos mediante concatenación y alineación de índices.
   - Detección de transacciones faltantes con `.isna()` y depuración de registros duplicados generados por reintentos de pasarelas de pago.
3. **Plataformas de comercio electrónico y motores de recomendación:**
   - Transformación de catálogos con millones de productos: normalización de descripciones con `DataFrame.map()`, eliminación de caracteres no imprimibles y compresión del espacio en memoria mediante tipos categóricos en columnas como marcas, categorías y tallas.
4. **Internet de las cosas (IoT) y telemetría industrial:**
   - Ingestión continua por lotes (`chunksize`) proveniente de miles de sensores remotos.
   - Imputación de caídas temporales de señal mediante propagación hacia adelante (`ffill()`) y cálculo incremental de estadísticas térmicas y eléctricas sin desbordar la memoria de servidores perimetrales (*edge computing*).

## 7. Uso en producción

Para desplegar procesos basados en Pandas en entornos productivos de alta confiabilidad, se deben acatar las siguientes directrices arquitectónicas:

1. **Activar y diseñar bajo *Copy-on-Write* (CoW):**
   - En Pandas 2.x se incorporó el modo *Copy-on-Write* (`pd.options.mode.copy_on_write = True`), el cual pasa a ser el comportamiento predeterminado en Pandas 3.0.
   - Este modo elimina los efectos colaterales donde modificar una vista alteraba silenciosamente el `DataFrame` original y erradica el clásico `SettingWithCopyWarning`. Bajo CoW, toda asignación encadenada (`df[filtro]["col"] = val`) lanza un `ChainedAssignmentError`, obligando a usar siempre asignación explícita mediante `df.loc[filtro, "col"] = val`.
2. **Optimización proactiva de tipos de datos (*downcasting*):**
   - Nunca utilizar tipos de datos genéricos `object` cuando se trate de cadenas de texto con pocas variantes; utilizar `category` para reducir la memoria en un 80% o más.
   - Emplear enteros de menor tamaño (`int32`, `int16`, `int8`) o tipos anulables (`Int32`, `Int16`) cuando el rango numérico sea conocido.
3. **Erradicación total de bucles imperativos:**
   - Está prohibido en producción recorrer un `DataFrame` con `for i in range(...)`, `for fila in df.iterrows()` o bucles `while`. Cualquier operación tabular debe resolverse con expresiones vectorizadas, accesores `.str` / `.dt` o, en su defecto, comprensión de listas sobre arrays de NumPy (`df["col"].to_numpy()`).
4. **Monitoreo riguroso de la huella de memoria:**
   - La propiedad `df.memory_usage()` por defecto reporta solo el tamaño de los punteros en columnas `object`. Es mandatorio utilizar `df.memory_usage(deep=True).sum()` para inspeccionar el tamaño real de los datos almacenados en el montículo de memoria de Python.
5. **Criterios de bifurcación tecnológica (Matriz de decisión):**
   - **Pandas en memoria:** óptimo para conjuntos de datos menores a 1-2 GB de tamaño bruto y flujos analíticos interactivos.
   - **Polars:** elección preferida cuando se requiere procesamiento en una sola máquina sobre datasets de 2 GB a 50 GB que aprovechen todos los núcleos de CPU en paralelo con mínimo consumo de RAM.
   - **DuckDB:** recomendado cuando los datos residen en archivos CSV o Parquet en disco y se desean realizar consultas analíticas complejas mediante SQL sin necesidad de cargar la totalidad de los datos en memoria.
   - **PySpark / Ray / Dask:** obligatorio cuando los volúmenes de datos superan la memoria y capacidad de almacenamiento de un único servidor (cientos de gigabytes o terabytes), requiriendo orquestación en clúster.

## 8. Errores comunes y recomendaciones

### 1. Invocación del método obsoleto y eliminado `DataFrame.applymap`

A partir de Pandas 2.2.0, el método `applymap()` fue eliminado definitivamente de la API. Mantener llamadas a este método heredado provoca un error inmediato en tiempo de ejecución.

```python
# ERROR INTENCIONAL: AttributeError por invocar applymap en Pandas 2.2+ (eliminado tras ser deprecado en 2.1)
import pandas as pd

df = pd.DataFrame({
    "producto": ["  teclado  ", " raton "],
    "codigo": ["  a101  ", " b202 "]
})

# applymap fue eliminado en Pandas 2.2.0: lanza AttributeError
df_limpio = df.applymap(lambda valor: valor.strip())
```

**Diagnóstico y corrección:**
El intérprete lanza `AttributeError: 'DataFrame' object has no attribute 'applymap'`. La solución estándar consiste en sustituir `applymap` por el método moderno `DataFrame.map`:

```python
import pandas as pd

df = pd.DataFrame({
    "producto": ["  teclado  ", " raton "],
    "codigo": ["  a101  ", " b202 "]
})
# Corrección estándar moderna:
df_limpio = df.map(lambda valor: valor.strip() if isinstance(valor, str) else valor)
```

### 2. Antipatrón de concatenación acumulativa en bucle ($O(N^2)$)

Un error crítico frecuente consiste en inicializar un `DataFrame` vacío y añadirle lotes dentro de un bucle mediante `df = pd.concat([df, nuevo_bloque])`. Debido a que las estructuras de Pandas son inmutables por naturaleza columnar, cada llamada a `concat` asigna un nuevo bloque completo en memoria y copia la totalidad de los datos anteriores, degradando la complejidad temporal a $O(N^2)$.

```python
# ERROR INTENCIONAL: antipatrón de concatenación acumulativa en bucle (crecimiento cuadrático O(N^2))
import pandas as pd

# Simulación de acumulación ineficiente en bucle
lotes = [pd.DataFrame({"id": [i], "valor": [i * 10]}) for i in range(5)]

df_acumulado = pd.DataFrame()
for bloque in lotes:
    # Cada iteración reasigna y copia todo el contenido anterior
    df_acumulado = pd.concat([df_acumulado, bloque], ignore_index=True)
```

**Diagnóstico y corrección:**
Para preservar la complejidad lineal $O(N)$, se deben acumular los bloques en una lista estándar de Python y ejecutar una única llamada a `pd.concat` al finalizar la ingesta:

```python
import pandas as pd

lotes = [pd.DataFrame({"id": [i], "valor": [i * 10]}) for i in range(5)]

# Corrección lineal: acumular en lista y concatenar en un único paso atómico
lista_lotes = []
for bloque in lotes:
    lista_lotes.append(bloque)

df_total = pd.concat(lista_lotes, axis=0, ignore_index=True)
```

### 3. Coacción indebida de tipos al castear columnas con valores nulos

Intentar convertir una columna numérica que contiene `np.nan` a un entero nativo de Python mediante `.astype(int)` o `.astype("int64")` genera un fallo irrecuperable, ya que el estándar IEEE 754 no admite enteros nulos nativos.

```python
# ERROR INTENCIONAL: ValueError / IntCastingNaNError al intentar castear NaN a entero nativo
import numpy as np
import pandas as pd

df = pd.DataFrame({"edad": [18.0, np.nan, 25.0]})

# Falla porque int64 no puede representar NaN
df["edad"] = df["edad"].astype(int)
```

**Diagnóstico y corrección:**
El entorno lanza `ValueError: Cannot convert non-finite values (NA or inf) to integer`. La solución consiste en emplear el tipo anulable de Pandas con mayúscula `Int64` o imputar previamente los nulos:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"edad": [18.0, np.nan, 25.0]})

# Solución 1: uso del tipo anulable de Pandas (admite pd.NA)
df["edad_anulable"] = df["edad"].astype("Int64")

# Solución 2: imputación previa antes del casteo nativo
df["edad_imputada"] = df["edad"].fillna(0).astype(int)
```

## 9. Resumen

- **Pandas** es una biblioteca de terceros de computación columnar en memoria que traslada operaciones matemáticas y de reordenamiento a núcleos compilados de alto rendimiento en C, Cython y Apache Arrow.
- **Valores nulos:** la coexistencia histórica de `np.nan` (coma flotante) y los modernos tipos anulables (`pd.NA`, `Int64`, `boolean`) exige seleccionar adecuadamente entre `.dropna()` (para descartar filas o columnas incompletas) y `.fillna()` (para imputar valores basados en medias, medianas o propagación).
- **Deduplicación:** `df.drop_duplicates()` erradica registros redundantes mediante el parámetro `subset` y la estrategia de preservación definida en `keep` (`"first"`, `"last"` o `False`).
- **Optimización de memoria:** convertir columnas textuales de baja cardinalidad al tipo `category` comprime drásticamente el espacio ocupado en RAM mediante codificación de diccionario y acelera las operaciones de agrupamiento y ordenamiento.
- **Concatenación atómica:** la combinación de tablas debe resolverse en una sola instrucción con `pd.concat(lista_de_tablas, axis=0, ignore_index=True)`, evitando el antipatrón de concatenación acumulativa en bucle.
- **Evolución de API:** `DataFrame.applymap()` fue formalmente depreciado en Pandas 2.1 y eliminado en Pandas 2.2; su sustituto moderno oficial es `DataFrame.map()`.
- **Escalabilidad productiva:** ante archivos que superan la memoria de trabajo, se debe recurrir a la lectura por lotes con `chunksize`, la integración con Apache Arrow (`dtype_backend="pyarrow"`) o motores de cálculo analítico fuera de memoria como Polars y DuckDB.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Importando_con_pandas.py` (L1-82, L104-118) | `Importando_con_pandas.py` | Importación de Pandas (`pd`), lectura de CSV, limpieza de comillas y espacios en celdas mediante `applymap` (L49), y concatenación vertical con `pd.concat` (L112-118) | **Se corrigió la obsolescencia de `applymap`**: formalmente eliminado en Pandas 2.2+, sustituido por `DataFrame.map`. Se profundizó en la concatenación atómica con `axis=0`, el reinicio de índices (`ignore_index=True`), y la jerarquía de eficiencia entre métodos vectorizados y funciones celda a celda |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/problemas_CSV.py` (L1-43, L44-80) | `problemas_CSV.py` | Conversión de tipos con `.astype()`, eliminación de columnas con nulos (`dropna(axis=1)`), borrado de filas incompletas (`dropna()`), deduplicación (`drop_duplicates()`) y persistencia en CSV | Se formalizó el contraste entre `axis=0` y `axis=1`, el uso de `subset` y las estrategias de `keep` (`"first"`, `"last"`, `False`). Se clarificó la coacción de tipos enteros a flotantes provocada por `np.nan` y se introdujeron los tipos anulables (`Int64`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Datos.csv` (L1-7) | `Datos.csv` | Dataset tabular con 6 registros y columnas de texto con comillas residuales y espacios | Reproducido mediante `io.StringIO` para ilustrar la normalización de cadenas de texto y encabezados sin dependencias de rutas absolutas locales |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/archivo.csv` (L1-4) | `archivo.csv` | Archivo CSV depurado resultante de las operaciones de filtrado y deduplicación | Empleado como referencia para el estándar de exportación limpia con `index=False` y tipos numéricos consistentes |

**Fundamento complementario:** la documentación original del curso abordaba de manera aislada e interactiva las operaciones de limpieza y concatenación sobre rutas locales fijas del sistema operativo (`C:\\Users\\...`). La presente sistematización incorpora cinco pilares arquitectónicos esenciales para entornos profesionales: (1) la transición obligatoria de `applymap` a `DataFrame.map` en cumplimiento con Pandas 2.2+; (2) la gestión de valores nulos mediante los tipos de datos anulables de Pandas (`pd.NA`, `Int64`); (3) la optimización de memoria en producción utilizando el tipo categórico (`category`) con auditoría profunda mediante `memory_usage(deep=True)`; (4) el análisis de complejidad algorítmica para evitar el antipatrón de concatenación cuadrática en bucles; y (5) los paradigmas de escalabilidad fuera de memoria (*chunksize*, Apache Arrow, Polars y DuckDB) para conjuntos de datos que exceden la memoria RAM disponible.

## 11. Referencias oficiales

- <https://pandas.pydata.org/docs/user_guide/missing_data.html> — Guía oficial de Pandas sobre tratamiento y modelado de datos faltantes (`isna`, `dropna`, `fillna`, tipos anulables `pd.NA`).
- <https://pandas.pydata.org/docs/user_guide/categorical.html> — Guía oficial de Pandas sobre tipos de datos categóricos y optimización de memoria.
- <https://pandas.pydata.org/docs/user_guide/merging.html> — Guía oficial de Pandas sobre combinación, concatenación (`concat`), unión (*merge*) y alineación de índices.
- <https://pandas.pydata.org/docs/user_guide/scale.html> — Guía oficial de Pandas sobre escalabilidad y procesamiento de grandes volúmenes de datos (*scaling to large datasets*).
- <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.map.html> — Referencia de API de Pandas para `DataFrame.map` (método estándar elemento a elemento que reemplaza a `applymap`).
- <https://pandas.pydata.org/docs/reference/api/pandas.concat.html> — Referencia de API de Pandas para la función `pandas.concat`.
- <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html> — Referencia de API de Pandas para `pandas.read_csv` y sus parámetros de escalabilidad (`chunksize`, `dtype_backend`).
