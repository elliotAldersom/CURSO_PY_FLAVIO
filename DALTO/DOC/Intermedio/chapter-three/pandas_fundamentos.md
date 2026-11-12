# Fundamentos de Análisis Tabular con Pandas: Series y DataFrame

## 2. Introducción

Mientras el módulo estándar [csv](archivos_csv.md) resulta idóneo para recorrer archivos registro por registro con memoria mínima, realizar cálculos estadísticos, reordenamientos multicriterio, selecciones por etiquetas o filtrados compuestos sobre listas de diccionarios en Python puro exige escribir numerosos bucles imperativos lentos y propensos a errores.

**Pandas** es una **biblioteca externa de terceros** (`pip install pandas`) —no incluida en la biblioteca estándar de Python— diseñada para la manipulación y el análisis eficiente de datos tabulares y series etiquetadas en memoria, apoyada internamente sobre bloques contiguos tipados de NumPy (y opcionalmente Apache Arrow en Pandas 2.x).

Dominar los fundamentos de Pandas permite abordar con rigor cuatro operaciones esenciales en ciencia e ingeniería de datos:

1. **Modelado tabular tipado por columna:** representar conjuntos de datos heterogéneos mediante estructuras `DataFrame` y `Series` donde cada columna posee su propio tipo físico (`int64`, `float64`, `bool`, `object`/`string`).
2. **Inspección estructural y estadística inmediata:** auditar dimensiones (`shape`), tipos (`dtypes`, `info()`) y estadísticos descriptivos (`describe()`, `Importando_con_pandas.py` L178) en una sola instrucción.
3. **Selección sin ambigüedades (`loc` frente a `iloc`):** distinguir con exactitud entre la indexación basada en etiquetas (`df.loc`) y la indexación basada en posición entera (`df.iloc`, `Importando_con_pandas.py` L220-311).
4. **Filtrado booleano vectorizado:** sustituir iteraciones manuales fila por fila por máscaras booleanas evaluadas en código compilado empleando los operadores `&`, `|` y `~` (`Importando_con_pandas.py` L324-340).

Las técnicas avanzadas de limpieza de datos faltantes (`dropna`, `fillna`), deduplicación (`drop_duplicates`), transformación elemento a elemento con `DataFrame.map`, concatenación (`pd.concat`) y agregaciones grupales se desarrollan en profundidad en [Pandas avanzado](../../Avanzado/chapter-four/pandas_avanzado.md).

## 3. Fundamentos y conceptos

**Pandas como dependencia externa y arquitectura columnar.** A diferencia de `sys`, `pathlib` o `csv`, utilizar Pandas requiere instalar el paquete en un entorno virtual (`pip install pandas`) e importarlo convencionalmente bajo el alias `import pandas as pd` (`Importando_con_pandas.py` L12). Internamente, mientras una lista de filas en Python dispersa millones de objetos individuales por el montículo (*heap*), un `DataFrame` organiza cada columna en un arreglo homogéneo contiguo en memoria, habilitando operaciones **vectorizadas** que procesan columnas enteras sin el sobrecosto del bucle interpretado de Python.

**Las tres estructuras nucleares: `Index`, `Series` y `DataFrame`.**

1. **`Index`:** secuencia inmutable de etiquetas asociada a las filas (y a los nombres de las columnas). Por defecto, al cargar un archivo sin especificar columna índice, Pandas crea un `RangeIndex(start=0, stop=n, step=1)`. Su función clave es la **alineación automática de datos** al operar entre columnas o tablas.
2. **`Series`:** estructura unidimensional compuesta por un arreglo de valores con tipo uniforme (`dtype`) más su `Index` de etiquetas.
3. **`DataFrame`:** tabla bidimensional ordenada cuyas columnas son objetos `Series` que comparten el mismo `Index` de filas (`Importando_con_pandas.py` L18-25).

**Corrección conceptual sobre `problemas_CSV.py` (L8-11): `type(df["Edad"])` frente a `dtype`.** En `problemas_CSV.py` (L8-11) aparece el siguiente fragmento tras ejecutar `df["Edad"] = df["Edad"].astype(str)`:

- `print(type(df["Edad"][0]))` imprime efectivamente `<class 'str'>` porque consulta un valor escalar individual.
- Sin embargo, el comentario en la línea 11 afirma que `print(type(df["Edad"]))` imprime `<class 'str'>`. **Esto es incorrecto:** extraer una sola columna con corchetes simples (`df["Edad"]`) retorna siempre el contenedor unidimensional de Pandas, por lo que `type(df["Edad"])` evalúa a `<class 'pandas.core.series.Series'>`. Para conocer el tipo de dato almacenado en esa columna debe consultarse el atributo `df["Edad"].dtype` (que tras `.astype(str)` es `object`, o `string` si se emplea el tipo dedicado `.astype("string")` de Pandas 2.x). Asimismo, al seleccionar **varias columnas** pasando una lista de nombres (`df[["nombre", "apellido"]]` en `Importando_con_pandas.py` L257), el resultado deja de ser una `Series` y pasa a ser un sub-`DataFrame` bidimensional.

**Carga con `pd.read_csv` y precaución con el parámetro `names`.** La función `pd.read_csv(ruta_o_flujo)` analiza el archivo CSV e infiere automáticamente los tipos numéricos (`int64`, `float64`) de cada columna. Conviene precisar un matiz importante sobre el ejemplo comentado en `Importando_con_pandas.py` (L15 y L106):

- Si el archivo CSV **carece** de fila de encabezados, pasar `names=["Name", "Last Name", "Age"]` asigna esos nombres directamente.
- Si el archivo CSV **sí contiene** encabezados en su primera línea (`"nombre","apellido","edad"` en `Datos.csv`) y se pasa `names=[...]` sin indicar `header=0`, Pandas tratará la primera línea textual como la fila de datos `0`, impidiendo además que `"edad"` se infiera como entero porque contendrá la cadena `"edad"`. Para renombrar encabezados existentes al leer debe escribirse `pd.read_csv(ruta, header=0, names=["Name", "Last Name", "Age"])`.

**Inspección estructural, estadística y ordenamiento.** Una vez cargado el `DataFrame`, el diagnóstico inicial combina cinco herramientas (`Importando_con_pandas.py` L28-30, L96-101, L124-195):

- `df.head(n)` y `df.tail(n)`: devuelven las primeras o últimas `n` filas (`5` por defecto; si `n=0`, devuelven un `DataFrame` vacío solo con los nombres de columnas).
- `df.shape`: propiedad (no método, sin paréntesis) que retorna una [tupla](../chapter-one/tuplas.md) `(filas, columnas)`, apta para [desempaquetamiento](../chapter-one/desempaquetamiento.md) directo `filas, columnas = df.shape` (`Importando_con_pandas.py` L173).
- `df.dtypes` y `df.info()`: detallan el tipo de cada columna, el conteo de valores no nulos y el consumo en memoria.
- `df.describe()`: calcula sobre las columnas numéricas el conteo no nulo (`count`), la media aritmética (`mean`), la desviación estándar muestral (`std`, calculada con denominador $N - 1$), el mínimo (`min`), los cuartiles (`25%`, mediana `50%`, `75%`) y el máximo (`max`).
- `df.sort_values(by="edad", ascending=True)`: devuelve un **nuevo** `DataFrame` ordenado de forma ascendente (`ascending=True`, por defecto) o descendente (`ascending=False`), dejando intacto a `df` salvo que el resultado se reasigne a una variable (`Importando_con_pandas.py` L96-100).

**Indexación explícita: diferencia crítica entre `df.loc` y `df.iloc`.** Acceder a celdas encadenando corchetes como `df["Edad"][0]` (`problemas_CSV.py` L9) se conoce como *indexación encadenada* (*chained indexing*) y constituye un antipatrón en Pandas porque puede devolver vistas o copias impredecibles (y lanza errores al intentar asignar bajo el modelo *Copy-on-Write* de Pandas 2.x/3.0). En su lugar deben utilizarse siempre los indexadores explícitos `loc` e `iloc` (`Importando_con_pandas.py` L220-311):

| Característica | `df.loc[filas, columnas]` | `df.iloc[filas, columnas]` |
|---|---|---|
| Criterio de búsqueda | **Etiquetas** del índice y nombres de columnas (o máscaras booleanas) | **Posición entera** estricta en base `0` (`0` a `n - 1`) |
| Comportamiento en rebanado (`a:b`) | **Extremo final inclusivo**: `df.loc[0:2]` incluye las etiquetas `0`, `1` **y `2`** | **Semiabierto `[a, b)`**: `df.iloc[0:2]` incluye solo las posiciones `0` y `1` (excluye `2`, igual que las [listas](../../Basico/chapter-two/listas.md)) |
| Ejemplo de celda única | `df.loc[0, "edad"]` | `df.iloc[0, 2]` |

Observación clave: si un `DataFrame` acaba de ordenarse con `sort_values` y su primera fila visual tiene la etiqueta original `3`, entonces `df_ordenado.iloc[0]` devuelve esa primera fila visual, mientras que `df_ordenado.loc[0]` busca la fila cuya etiqueta sigue llamándose `0` sin importar en qué posición haya quedado.

**Filtrado booleano vectorizado y precedencia de `&`, `|` y `~`.** Al evaluar una comparación como `df["edad"] >= 18`, Pandas devuelve una `Series` de valores `True`/`False` alineada con el índice. Pasarla dentro de `df.loc[mascara, :]` filtra de golpe todas las filas verdaderas (`Importando_con_pandas.py` L324). Para combinar múltiples condiciones (`Importando_con_pandas.py` L339-343) rigen dos reglas estrictas del lenguaje Python:

1. **No pueden usarse `and`, `or` ni `not`:** las palabras reservadas lógicas de Python exigen reducir cada operando a un único valor booleano escalar (`bool(serie)`), lo cual es ambiguo para una columna con múltiples elementos y lanza `ValueError: The truth value of a Series is ambiguous`. Pandas sobrecarga en su lugar los operadores bit a bit **`&` (conjunción lógica)**, **`|` (disyunción lógica)** y **`~` (negación lógica)** para operar elemento a elemento.
2. **Cada condición individual debe encerrarse entre paréntesis:** en la gramática de Python, `&` y `|` tienen **mayor precedencia** que `<`, `<=`, `>`, `>=`, `==` y `!=`. Escribir sin paréntesis `df["edad"] < 18 & df["edad"] > 0` se agrupa internamente como `df["edad"] < (18 & df["edad"]) > 0`, provocando un fallo de evaluación. La sintaxis obligatoria es `(df["edad"] < 18) & (df["edad"] > 0)`.

## 4. Sintaxis y funcionamiento

Operaciones fundamentales sobre `DataFrame` y `Series` en Pandas 2.x:

```text
import pandas as pd

df = pd.read_csv(ruta, encoding="utf-8")
subtabla = df.loc[(df["col_a"] >= limite) & (df["col_b"] == "activo"), ["col_a", "col_c"]]
```

Tabla sintética de atributos, métodos e indexadores esenciales:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `pd.read_csv(f, ...)` | Carga un CSV en un `DataFrame` infiriendo tipos columnares | `pd.read_csv("datos.csv", encoding="utf-8")` |
| 2 | `df.to_csv(f, index=False)` | Exporta el `DataFrame` a CSV omitiendo la columna del índice | `df.to_csv("out.csv", index=False)` |
| 3 | `df["col"]` | Extrae una columna individual como objeto `pandas.Series` | `edades = df["edad"]` |
| 4 | `df[["c1", "c2"]]` | Extrae un subconjunto de columnas como nuevo `DataFrame` | `df[["nombre", "apellido"]]` |
| 5 | `df.shape` | Tupla `(n_filas, n_columnas)` con las dimensiones de la tabla | `filas, cols = df.shape` |
| 6 | `df.dtypes` / `s.dtype` | Tipos de almacenamiento de cada columna o de una `Series` | `df["edad"].dtype` |
| 7 | `df.head(n)` / `df.tail(n)` | Retorna las primeras o últimas `n` filas (`5` por defecto) | `df.head(3)` |
| 8 | `df.describe()` | Resumen estadístico (`count`, `mean`, `std`, cuartiles, extremos) | `resumen = df.describe()` |
| 9 | `df.sort_values(by, ascending)` | Retorna copia ordenada por una o varias columnas | `df.sort_values("edad", ascending=False)` |
| 10 | `df.loc[etiq_f, etiq_c]` | Selección por etiquetas o máscara booleana (rebanado **inclusivo**) | `df.loc[0:2, "nombre":"edad"]` |
| 11 | `df.iloc[pos_f, pos_c]` | Selección por posición entera base `0` (rebanado **semiabierto**) | `df.iloc[0:2, [0, 2]]` |
| 12 | `(c1) & (c2)` / `|` / `~` | Operadores booleanos vectorizados elemento a elemento | `df.loc[(df["x"] > 0) & (~df["nulo"])]` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Ingesta tabular, distinción exacta entre `DataFrame`, `Series`, `dtype` y escalar, y métricas descriptivas.**

```python
import io
import pandas as pd

DATOS_CSV = (
    '"nombre","apellido","edad"\n'
    '"flavio","silva",18\n'
    '"fabian","silva",21\n'
    '"joaquin","salazar",7\n'
    '"camila","dalto",24\n'
    '"juan","ramirez",10\n'
    '"roberto","gutierrez",12\n'
)

df = pd.read_csv(io.StringIO(DATOS_CSV))
filas, columnas = df.shape
serie_edades = df["edad"]

print(f"Dimensiones: {filas} filas x {columnas} columnas")
print("Tipo de df:", type(df))
print("Tipo de df['edad']:", type(serie_edades))
print("dtype de df['edad']:", serie_edades.dtype)
print("Tipo de un escalar:", type(df.loc[0, "nombre"]))
print(f"Media: {serie_edades.mean():.2f} | Mediana: {serie_edades.median():.1f}")
```

Explicación paso a paso:

- Reproduciendo de forma autocontenida los datos de `Datos.csv`, `df.shape` entrega `(6, 3)` desempaquetado en `filas` y `columnas`.
- Se verifica rigurosamente la diferencia frente al comentario de `problemas_CSV.py` (L11): `df["edad"]` es `<class 'pandas.core.series.Series'>` con `dtype` `int64`, mientras que `df.loc[0, "nombre"]` accede al escalar individual `<class 'str'>`.
- Los métodos vectorizados `.mean()` y `.median()` coinciden con los valores `15.33` y `15.0` reportados por `df.describe()` en `Importando_con_pandas.py` (L188-192).

Resultado esperado:

```text
Dimensiones: 6 filas x 3 columnas
Tipo de df: <class 'pandas.core.frame.DataFrame'>
Tipo de df['edad']: <class 'pandas.core.series.Series'>
dtype de df['edad']: int64
Tipo de un escalar: <class 'str'>
Media: 15.33 | Mediana: 15.0
```

### Intermedio

**Ejemplo 2 — Contraste práctico entre rebanado inclusivo en `df.loc` y semiabierto en `df.iloc`, junto con `sort_values`.**

```python
import io
import pandas as pd

CSV_EQUIPO = (
    "codigo,nombre,area,edad\n"
    "E10,Flavio,Backend,18\n"
    "E20,Fabian,Datos,21\n"
    "E30,Joaquin,Soporte,19\n"
    "E40,Camila,Arquitectura,24\n"
)

df = pd.read_csv(io.StringIO(CSV_EQUIPO))

# En loc el límite superior 2 es inclusivo (etiquetas 0, 1 y 2)
tramo_loc = df.loc[0:2, ["nombre", "edad"]]
# En iloc el límite superior 2 queda excluido [0:2) (posiciones 0 y 1)
tramo_iloc = df.iloc[0:2, [1, 3]]

ordenado = df.sort_values(by="edad", ascending=False)

print("Filas devueltas por df.loc[0:2]:", list(tramo_loc["nombre"]))
print("Filas devueltas por df.iloc[0:2]:", list(tramo_iloc["nombre"]))
print("Celda exacta con loc[3, 'area']:", df.loc[3, "area"])
print("Celda exacta con iloc[3, 2]:", df.iloc[3, 2])
print("Orden descendente por edad:", list(ordenado["nombre"]))
```

Explicación técnica:

- Ante el mismo rango `0:2`, `df.loc[0:2, ...]` devuelve `3` registros (`Flavio`, `Fabian`, `Joaquin`), mientras que `df.iloc[0:2, ...]` devuelve `2` registros (`Flavio`, `Fabian`). Comprender esta asimetría evita errores de desplazamiento por una unidad (*off-by-one*).
- `df.sort_values(by="edad", ascending=False)` ordena de mayor a menor edad sin alterar `df`.

Resultado esperado:

```text
Filas devueltas por df.loc[0:2]: ['Flavio', 'Fabian', 'Joaquin']
Filas devueltas por df.iloc[0:2]: ['Flavio', 'Fabian']
Celda exacta con loc[3, 'area']: Arquitectura
Celda exacta con iloc[3, 2]: Arquitectura
Orden descendente por edad: ['Camila', 'Fabian', 'Joaquin', 'Flavio']
```

### Avanzado

**Ejemplo 3 — Columnas calculadas vectorizadas, filtrado booleano compuesto (`~`, `&`, `.isin()`) y exportación limpia.**

```python
import io
import pandas as pd

CSV_PEDIDOS = (
    "id_pedido,categoria,pais,unidades,precio_unitario,cancelado\n"
    "101,Hardware,PE,4,120.0,False\n"
    "102,Software,CL,1,80.0,False\n"
    "103,Hardware,ES,2,350.0,True\n"
    "104,Servicios,PE,3,200.0,False\n"
    "105,Software,MX,10,45.0,False\n"
)

df = pd.read_csv(io.StringIO(CSV_PEDIDOS))
df["importe_bruto"] = df["unidades"] * df["precio_unitario"]

mascara_objetivo = (
    (~df["cancelado"])
    & (df["pais"].isin(["PE", "MX"]))
    & (df["importe_bruto"] >= 400.0)
)

seleccion = df.loc[mascara_objetivo, ["id_pedido", "categoria", "pais", "importe_bruto"]]
salida_csv = io.StringIO()
seleccion.to_csv(salida_csv, index=False, lineterminator="\n")

print("Pedidos seleccionados:", seleccion.shape[0])
print("Facturación filtrada:", seleccion["importe_bruto"].sum())
print(salida_csv.getvalue().strip())
```

Explicación de rendimiento y diseño:

- La expresión `df["unidades"] * df["precio_unitario"]` multiplica ambos arreglos elemento a elemento en C sin ningún bucle `for` en Python.
- La máscara booleana combina negación vectorizada `~df["cancelado"]`, pertenencia a conjunto `.isin(["PE", "MX"])` (mucho más limpia que encadenar múltiples `|`) y umbral numérico, todo protegido con paréntesis explícitos dentro de `df.loc[mascara_objetivo, ...]`.
- Al exportar con `to_csv(..., index=False)` (`problemas_CSV.py` L73), se evita añadir una columna espuria `Unnamed: 0` en lecturas posteriores.

Resultado esperado:

```text
Pedidos seleccionados: 3
Facturación filtrada: 1530.0
id_pedido,categoria,pais,importe_bruto
101,Hardware,PE,480.0
104,Servicios,PE,600.0
105,Software,MX,450.0
```

## 6. Aplicaciones en el mundo real

- **Análisis exploratorio de datos (*EDA*) y reportería de negocio:** inspección rápida de ventas, métricas financieras, retención de clientes y preparación de tablas resumen previas a la [visualización estadística](visualizacion.md).
- **Ingeniería de características (*feature engineering*) en aprendizaje automático:** creación vectorizada de indicadores, normalización de variables y filtrado de cohortes de entrenamiento antes de alimentar modelos de `scikit-learn`.
- **Auditoría y conciliación financiera:** cruce y filtrado de transacciones sospechosas, detección de valores extremos mediante cuantiles de `describe()` y validación de reglas contables sobre decenas de miles de registros.
- **Transformación intermedia de formatos:** ingesta desde CSV o Excel para normalizar tipos y reexportar hacia formatos columnares de alto rendimiento como Parquet o Feather.

## 7. Uso en producción

- **Declarar explícitamente `dtype` y `usecols` en `pd.read_csv`:** en cargas productivas no debe dejarse la inferencia de tipos al azar, especialmente en códigos postales o documentos de identidad con ceros a la izquierda (`dtype={"dni": "string"}` evita que `"00421"` se convierta en el entero `421`). Asimismo, `usecols=[...]` carga únicamente las columnas necesarias reduciendo drásticamente el uso de memoria.
- **Evitar por completo iterar filas con `for` o `.iterrows()`:** recorrer un `DataFrame` fila por fila en Python anula la ventaja columnar y suele ser entre `50` y `500` veces más lento que una operación vectorizada (`df["a"] + df["b"]`, `.str.strip()`, `np.where`).
- **Activar o diseñar pensando en *Copy-on-Write* (Pandas 2.x / 3.0):** realizar asignaciones siempre en un único paso mediante `df.loc[condicion, "columna"] = nuevo_valor` (y nunca mediante `df[condicion]["columna"] = ...`), garantizando compatibilidad plena con Pandas 2.x (`pd.options.mode.copy_on_write = True`) y Pandas 3.0.
- **Procesar archivos mayores que la RAM por bloques (`chunksize`) o motores alternativos:** si un archivo CSV pesa 20 GB en un contenedor con 2 GB de RAM, `pd.read_csv(ruta, chunksize=100_000)` devuelve un iterador de sub-`DataFrame` manejables por lotes, o bien puede emplearse el módulo estándar [csv](archivos_csv.md).

## 8. Errores comunes y recomendaciones

1. **Usar `and`, `or` o `not` en lugar de `&`, `|`, `~` o omitir los paréntesis en filtros compuestos (`ValueError`).**

```python
# ERROR INTENCIONAL: ValueError por usar 'and' lógico sobre objetos Series en lugar de '&' con paréntesis
import pandas as pd

df = pd.DataFrame({"edad": [15, 20, 30], "activo": [True, True, False]})
filtrado = df.loc[df["edad"] >= 18 and df["activo"]]
```

Diagnóstico: Python intenta convertir `df["edad"] >= 18` a un único booleano escalar antes de evaluar `and`, lanzando `ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().` Solución: escribir siempre `df.loc[(df["edad"] >= 18) & (df["activo"])]`.

2. **Asignar valores mediante indexación encadenada (*chained indexing*).**

```python
# ERROR INTENCIONAL: asignación encadenada ambigua (SettingWithCopyWarning / ChainedAssignmentError)
import pandas as pd

df = pd.DataFrame({"nombre": ["Flavio", "Joaquin"], "edad": [18, 7]})
df[df["edad"] < 18]["edad"] = 0
```

Diagnóstico: `df[df["edad"] < 18]` puede construir un `DataFrame` temporal independiente; mutar `["edad"] = 0` sobre ese temporal descarta el cambio o falla con `ChainedAssignmentError` en Pandas moderno. Solución: usar un único acceso `df.loc[df["edad"] < 18, "edad"] = 0`.

3. **Pasar `names=[...]` sin `header=0` a un archivo CSV que ya trae fila de encabezados.** Convierte los nombres originales de la línea 1 en la fila `0` de datos y degrada las columnas numéricas al tipo `object`. Solución: añadir `header=0` al renombrar al vuelo o renombrar después con `df.rename(columns={...})`.

4. **Olvidar `index=False` en `df.to_csv(...)`.** Si el índice es un `RangeIndex` autogenerado `0, 1, 2...` y no se pasa `index=False`, cada ciclo de guardado y lectura acumula columnas innecesarias `Unnamed: 0`.

## 9. Resumen

- **Pandas** es una biblioteca externa de terceros especializada en el análisis tabular en memoria mediante `Series` (1D etiquetada) y `DataFrame` (2D de columnas tipadas alineadas por `Index`).
- Extraer una columna con `df["col"]` devuelve un objeto `pandas.Series` cuyo tipo interno se consulta en `.dtype`; seleccionar una lista `df[["c1", "c2"]]` devuelve un `DataFrame`.
- La inspección inicial combina `head()`, `tail()`, `shape`, `dtypes`, `info()` y `describe()`, mientras que `sort_values()` genera vistas o copias ordenadas sin mutar la tabla original por defecto.
- `df.loc` indexa por etiquetas con extremos **inclusivos** en rebanados (`a:b`), mientras que `df.iloc` indexa por posición entera base `0` con intervalos **semiabiertos** (`[a, b)`).
- El filtrado booleano vectorizado exige utilizar `&`, `|` y `~` encerrando cada comparación relacional entre paréntesis: `(condicion_1) & (condicion_2)`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Importando_con_pandas.py` (L12-350) | `Importando_con_pandas.py` | `pd.read_csv`, `head`, `tail`, `columns`, `shape` con desempaquetamiento, `describe`, `sort_values`, `df.loc`, `df.iloc` y filtro con `&` | Se precisó el carácter externo de Pandas, la diferencia de rebanado inclusivo/semiabierto entre `loc` e `iloc`, la precedencia de `&`/`|`/`~` y la obsolescencia de `applymap` (L49, tratado en [Pandas avanzado](../../Avanzado/chapter-four/pandas_avanzado.md)) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Datos.csv` (L1-7) | `Datos.csv` | Tabla de 6 personas empleada para explorar inspección, ordenamiento y filtrado por mayoría de edad | Reproducida de forma portable con `io.StringIO` verificando sus métricas exactas (`mean=15.33`, `median=15.0`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/problemas_CSV.py` (L4-19, L73) | `problemas_CSV.py` | Conversión `.astype(str)`, consulta `type(df["Edad"][0])`, `type(df["Edad"])` y guardado con `df.to_csv(..., index=False, encoding="UTF-8")` | **Se corrigió explícitamente el comentario de L11**: `type(df["Edad"])` es `pandas.Series` (no `str`), diferenciándolo de `.dtype` y advirtiendo contra la indexación encadenada `df["Edad"][0]`. La limpieza `dropna`/`drop_duplicates` (L39-70) se enlaza con [Pandas avanzado](../../Avanzado/chapter-four/pandas_avanzado.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/archivo.csv` (L1-4) | `archivo.csv` | Archivo CSV resultante tras estandarización y exportación sin índice | Integrado en las pautas de exportación limpia (`index=False`) y preservación de tipos numéricos |

**Fundamento complementario:** se incorporaron cinco conceptos indispensables de Pandas 2.x para uso profesional: (1) el rol de `Index` y la arquitectura columnar vectorizada sobre NumPy/Arrow; (2) el efecto exacto de `header=0` al combinar `names=` en `pd.read_csv`; (3) el contraste de extremos en rebanados `loc` frente a `iloc`; (4) la explicación gramatical de `ValueError` al usar `and`/`or` o al omitir paréntesis con `&`/`|`; y (5) la prevención de *chained indexing* bajo el modelo *Copy-on-Write*.

## 11. Referencias oficiales

- <https://pandas.pydata.org/docs/user_guide/10min.html> — Guía oficial de Pandas (*10 minutes to pandas*): recorrido por `Series`, `DataFrame`, inspección, selección y operaciones vectorizadas.
- <https://pandas.pydata.org/docs/user_guide/dsintro.html> — Guía oficial de Pandas (*Intro to data structures*): arquitectura y comportamiento de `Series` y `DataFrame`.
- <https://pandas.pydata.org/docs/user_guide/indexing.html> — Guía oficial de Pandas (*Indexing and selecting data*): reglas formales de `loc`, `iloc`, rebanados y máscaras booleanas.
- <https://pandas.pydata.org/docs/user_guide/copy_on_write.html> — Guía oficial de Pandas (*Copy-on-Write*): semántica moderna de vistas, copias y eliminación de asignaciones encadenadas.
- <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html> — Referencia de API (`pandas.read_csv`): parámetros `names`, `header`, `dtype`, `usecols` y `chunksize`.
