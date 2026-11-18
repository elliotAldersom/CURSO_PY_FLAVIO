# `pandas.read_csv`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.read_csv(
    filepath_or_buffer,
    *,
    sep=_NoDefault.no_default,
    delimiter=None,
    header='infer',
    names=_NoDefault.no_default,
    index_col=None,
    usecols=None,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skipinitialspace=False,
    skiprows=None,
    skipfooter=0,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=_NoDefault.no_default,
    skip_blank_lines=True,
    parse_dates=None,
    date_format=None,
    dayfirst=False,
    cache_dates=True,
    iterator=False,
    chunksize=None,
    compression='infer',
    thousands=None,
    decimal='.',
    lineterminator=None,
    quotechar='"',
    quoting=0,
    doublequote=True,
    escapechar=None,
    comment=None,
    encoding=None,
    encoding_errors='strict',
    dialect=None,
    on_bad_lines='error',
    delim_whitespace=_NoDefault.no_default,
    low_memory=True,
    memory_map=False,
    float_precision=None,
    storage_options=None,
    dtype_backend=_NoDefault.no_default
)
```

## 2. ¿Qué es?

Es una **función constructora** perteneciente al módulo principal `pandas` (invocada convencionalmente como `pd.read_csv`). Analiza y carga datos tabulares formateados como texto delimitado (CSV, TSV, TXT) en una estructura en memoria `pandas.DataFrame`.

## 3. ¿Para qué sirve?

Permite importar datos desde archivos locales, URLs remotas o flujos en memoria (`io.StringIO`), infiriendo tipos de datos, gestionando valores nulos, decodificando caracteres y optimizando el consumo de RAM mediante lectura por lotes o selección columnar.

* **Equivalencia en SQL:** Equivale a una sentencia de importación masiva `COPY tabla FROM 'archivo.csv' WITH (FORMAT csv, HEADER)`.

## 4. ¿Cómo funciona?

1. **Selección del motor:** Emplea por defecto el motor en C (`engine='c'`), altamente optimizado para velocidad; si se requieren delimitadores multicarácter o expresiones regulares, conmuta al motor en Python (`engine='python'`) o `engine='pyarrow'` para mayor paralelismo.
2. **Inferencia léxica y de tipos:** Lee las primeras líneas para inferir encabezados (si `header='infer'`) y analiza las columnas para asignar tipos homogéneos (`int64`, `float64`, `bool`, `object`/`string`).
3. **Mapeo de memoria y streaming:** Con `low_memory=True`, analiza el archivo internamente en bloques, lo que puede provocar advertencias de tipos mixtos en columnas con formatos heterogéneos; con `chunksize`, devuelve un iterador perezoso `TextFileReader` que mantiene la memoria constante en $O(1)$.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `filepath_or_buffer` | `str`, `Path`, archivo abierto | Obligatorio | Posicional | Ruta al archivo, URL remota o flujo en memoria a analizar. |
| `sep` / `delimiter` | `str` | Opcional | `','` | Carácter delimitador de campos (por ejemplo `','` o `';'`). |
| `header` | `int`, `list[int]`, `None` | Opcional | `'infer'` | Número de fila que contiene los nombres de columna. `None` si el archivo no tiene cabeceras. |
| `names` | `list[str]` | Opcional | `None` | Lista de nombres de columnas a aplicar. Si el archivo ya tiene encabezados, debe combinarse con `header=0` para renombrarlos. |
| `usecols` | `list`, `callable` | Opcional | `None` | Subconjunto de columnas a cargar en memoria, ignorando las demás. |
| `dtype` | `dict`, tipo | Opcional | `None` | Diccionario que mapea nombres de columna a tipos físicos de Pandas/NumPy (p. ej. `{'id': 'int32'}`). |
| `chunksize` | `int` | Opcional | `None` | Si se especifica, retorna un iterador para procesar el archivo en bloques de `n` filas. |
| `encoding` | `str` | Opcional | `None` | Codificación del archivo de texto (p. ej. `'utf-8'`, `'latin1'`). |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la variable declarada en la definición de la función (`usecols`, `dtype`). El **argumento** es el dato concreto pasado al invocarla (`usecols=['jugador', 'goles']`).

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `pandas.io.parsers.TextFileReader` si se usa `chunksize` o `iterator=True`).
* **Mutabilidad:** Crea y retorna una **nueva instancia en memoria**; no muta ninguna estructura previa.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Lectura directa de un CSV en memoria con encabezados automáticos:

```python
import io
import pandas as pd

csv_datos = """jugador,equipo,goles,minutos_jugados
Lionel Messi,Inter Miami,25,2100
Kylian Mbappé,Real Madrid,28,2450
Erling Haaland,Manchester City,31,2600"""

df_futbol = pd.read_csv(io.StringIO(csv_datos))
print(df_futbol)
```

**Salida real:**

```text
          jugador           equipo  goles  minutos_jugados
0    Lionel Messi      Inter Miami     25             2100
1   Kylian Mbappé      Real Madrid     28             2450
2  Erling Haaland  Manchester City     31             2600
```

---

### Nivel 2: Intermedio

Carga defensiva con tipos estrictos, selección de columnas y delimitador regional:

```python
import io
import pandas as pd

csv_regional = """jugador;equipo;goles;salario_millones
Vinicius Jr;Real Madrid;21;20.5
Rodri;Manchester City;8;14.2
Lamine Yamal;Barcelona;12;8.0"""

df_tipado = pd.read_csv(
    io.StringIO(csv_regional),
    sep=';',
    usecols=['jugador', 'goles'],
    dtype={'jugador': 'string', 'goles': 'int16'}
)

print(df_tipado)
print("\nTipos físicos:")
print(df_tipado.dtypes)
```

**Salida real:**

```text
        jugador  goles
0   Vinicius Jr     21
1         Rodri      8
2  Lamine Yamal     12

Tipos físicos:
jugador    string
goles       int16
dtype: object
```

---

### Nivel 3: Avanzado

Procesamiento en streaming por lotes (*chunking*) para archivos masivos con agregación en memoria constante:

```python
import io
import pandas as pd

csv_masivo = """jugador,equipo,goles
Jude Bellingham,Real Madrid,19
Phil Foden,Manchester City,19
Cole Palmer,Chelsea,22
Bukayo Saka,Arsenal,16
Antoine Griezmann,Atletico Madrid,16"""

lector = pd.read_csv(io.StringIO(csv_masivo), chunksize=2)

total_goles = 0
total_registros = 0

for bloque in lector:
    total_goles += bloque['goles'].sum()
    total_registros += len(bloque)

print(f"Lotes procesados exitosamente.")
print(f"Registros totales: {total_registros} | Suma de goles: {total_goles}")
```

**Salida real:**

```text
Lotes procesados exitosamente.
Registros totales: 5 | Suma de goles: 92
```

## 8. Errores frecuentes y casos borde

1. **Advertencia `DtypeWarning`:** En archivos gigantes sin `dtype`, el motor C lee bloques y puede inferir `int` al principio y `string` más adelante. **Solución:** declarar `dtype={'columna': str}` o `low_memory=False`.
2. **Separador decimal incorrecto:** Si el CSV usa coma decimal (`12,50`), Pandas lo interpreta como texto. **Solución:** pasar `decimal=','`.
3. **Encabezados ausentes:** Cargar un CSV sin cabeceras sin especificar `header=None` provoca que la primera fila de datos se convierta en los nombres de las columnas.

## 9. Buenas prácticas y rendimiento

* **Carga columnar selectiva:** Pasa siempre `usecols` para no cargar en RAM columnas innecesarias.
* **Tipos eficientes:** Emplea tipos de menor tamaño (`int16`, `float32`, `category`) mediante `dtype` para reducir el consumo hasta un 80%.
* **PyArrow Engine:** En Pandas 2.x, usar `engine='pyarrow'` acelera la ingesta multihilo en datasets grandes.

## 10. Métodos relacionados

* [to_csv](to_csv.md) — Exporta un `DataFrame` a texto delimitado CSV.
* [read_excel](read_excel.md) — Carga datos tabulares desde libros Microsoft Excel `.xlsx`.

## 11. Referencias oficiales

* **API Reference:** [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) (Pandas 2.2).
* **Guía de usuario:** [IO tools (text, CSV, HDF5, ...)](https://pandas.pydata.org/docs/user_guide/io.html#csv-text-files).
