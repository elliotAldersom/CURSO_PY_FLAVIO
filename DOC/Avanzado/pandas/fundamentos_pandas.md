# Fundamentos de Arquitectura y Manipulación de Datos con Pandas

## 2. Introducción

Pandas es la biblioteca líder del ecosistema Python para la manipulación y el análisis de datos estructurados y tabulares en memoria. Construida originalmente sobre bloques contiguos de NumPy y modernizada en sus versiones 2.x mediante el soporte nativo de tipos de Apache Arrow y el modelo *Copy-on-Write* (CoW), provee estructuras de datos de alto rendimiento optimizadas para operaciones vectorizadas sin la sobrecarga del bucle interpretado de Python.

Dominar Pandas desde una perspectiva arquitectónica exige comprender su modelo físico en memoria, la alineación automática por índice y la distinción rigurosa entre vistas referenciales y copias independientes.

## 3. Fundamentos y conceptos

1. **Estructuras nucleares de datos:**
   * **`Index`:** Secuencia ordenada e inmutable de etiquetas que define los ejes del DataFrame (filas y columnas). Permite búsquedas en tiempo constante $O(1)$ basadas en tablas hash internas.
   * **`Series`:** Arreglo unidimensional etiquetado compuesto por una secuencia contigua homogénea de valores más su correspondiente `Index`.
   * **`DataFrame`:** Tabla bidimensional estructurada en columnas contiguas independientes, donde cada columna es una `Series` y todas comparten el mismo `Index` de filas.
2. **Arquitectura Columnar frente a Row-Oriented:** A diferencia de una lista nativa de diccionarios donde los datos están dispersos en el montículo (*heap*), un DataFrame almacena los datos de cada columna de forma contigua en memoria (mediante el gestor de bloques `BlockManager`), lo que maximiza el aprovechamiento de la memoria caché de la CPU (*cache locality*) y permite procesar millones de registros con operaciones vectorizadas SIMD.
3. **El modelo *Copy-on-Write* (CoW) en Pandas 2.x:** Históricamente, las operaciones de corte y filtrado podían devolver una vista o una copia de forma impredecible, detonando advertencias como `SettingWithCopyWarning`. Bajo *Copy-on-Write*, los cortes comparten la memoria de forma segura y sólo se duplica la memoria en el instante exacto en que se realiza una modificación destructiva.

## 4. Sintaxis y funcionamiento

Instalación en el entorno virtual de trabajo:

```bash
pip install pandas openpyxl pyarrow
```

Patrón idiomático canónico de importación:

```python
import pandas as pd
import numpy as np
```

Creación defensiva de un DataFrame a partir de un diccionario de listas homogéneas:

```python
import pandas as pd

df_plantilla = pd.DataFrame({
    "jugador": ["Lionel Messi", "Kylian Mbappé", "Erling Haaland"],
    "equipo": ["Inter Miami", "Real Madrid", "Manchester City"],
    "goles": [25, 28, 31],
    "minutos_jugados": [2100, 2450, 2600]
})
```

## 5. Ejemplos prácticos progresivos

### Básico

Inspección estructural básica y verificación de dimensiones físicas:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Rodrygo"],
    "goles": [21, 15]
})

print("Dimensiones (filas, columnas):", df.shape)
print("\nTipos de datos físicos:")
print(df.dtypes)
```

**Salida real:**

```text
Dimensiones (filas, columnas): (2, 2)

Tipos de datos físicos:
jugador    object
goles       int64
dtype: object
```

---

### Intermedio

Indexación explícita con `loc` y filtrado vectorizado multicriterio:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Bellingham", "Kroos", "Modric", "Guler"],
    "minutos": [2450, 2100, 1600, 750],
    "goles": [19, 1, 2, 6]
}, index=["JUG_01", "JUG_02", "JUG_03", "JUG_04"])

# Filtrado booleano vectorizado con operadores bitwise
mascara = (df_liga["minutos"] > 1000) & (df_liga["goles"] >= 5)
df_destacados = df_liga.loc[mascara, ["jugador", "goles"]]
print(df_destacados)
```

**Salida real:**

```text
           jugador  goles
JUG_01  Bellingham     19
```

---

### Avanzado

Pipeline funcional de transformación y optimización de memoria con tipos categóricos:

```python
import pandas as pd

df_raw = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Lamine Yamal", "Lewandowski"],
    "club": ["FC Barcelona", "FC Barcelona", "FC Barcelona", "FC Barcelona"],
    "minutos": [1800, 1200, 2100, 2600],
    "goles": [4, 2, 8, 26]
})

def optimizar_memoria_y_metricas(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.astype({"club": "category", "goles": "int16"})
        .assign(goles_por_90=lambda d: ((d["goles"] / d["minutos"]) * 90).round(2))
        .sort_values(by="goles_por_90", ascending=False)
        .reset_index(drop=True)
    )

df_procesado = optimizar_memoria_y_metricas(df_raw)
print(df_procesado)
```

**Salida real:**

```text
        jugador          club  minutos  goles  goles_por_90
0   Lewandowski  FC Barcelona     2600     26          0.90
1  Lamine Yamal  FC Barcelona     2100      8          0.34
2         Pedri  FC Barcelona     1800      4          0.20
3          Gavi  FC Barcelona     1200      2          0.15
```

## 6. Aplicaciones en el mundo real

En el análisis cuantitativo de rendimiento y la ingeniería deportiva, Pandas se emplea para ingestar archivos de telemetría GPS transmitidos por chalecos de seguimiento de atletas a 10 Hz (diez muestras por segundo). Mediante remuestreo temporal (`resample`), cálculo de aceleraciones instantáneas (`diff`) y segmentación por zonas de fatiga (`cut`), los preparadores físicos identifican picos de sobrecarga muscular antes de que deriven en lesiones traumáticas.

## 7. Uso en producción

1. **Gestión de memoria y tipos:** En entornos de producción con restricciones de memoria, sustituir columnas de tipo `object` por `category` o `string[pyarrow]` reduce el consumo hasta un 80% y previene fallos por *Out-Of-Memory* (OOM).
2. **Procesamiento por lotes (*chunking*):** Para ingerir fuentes de datos de decenas de gigabytes donde el dataset supera la memoria RAM disponible, se debe procesar el flujo en bloques mediante `pd.read_csv(..., chunksize=100000)`.
3. **Inmutabilidad funcional:** Evitar mutaciones directas de estado (`inplace=True`); estructurar el código mediante tuberías funcionales encadenadas con `.pipe()` y `.assign()`.

## 8. Errores comunes y recomendaciones

* **Error común: Indexación encadenada (`df['col'][0] = x`):** Viola el modelo de consistencia de memoria y lanza `SettingWithCopyWarning`. **Recomendación:** Utilizar siempre `.loc[fila, columna]`.
* **Error común: Iterar filas con bucles `for` nativos:** Iterar sobre un DataFrame fila por fila degrada el tiempo de cómputo en varios órdenes de magnitud. **Recomendación:** Emplear operaciones vectorizadas o `.map()`.
* **Error común: Confundir `axis=0` con `axis=1`:** En operaciones de agregación como `sum()` o `dropna()`, `axis=0` opera sobre filas colapsando columnas, mientras que `axis=1` opera horizontalmente sobre columnas colapsando filas.

## 9. Resumen

Pandas estructura los datos tabulares en memoria columnar mediante `Index`, `Series` y `DataFrame`. Sus capacidades nucleares abarcan la ingesta y persistencia multiplataforma, la inspección estadística inmediata, la indexación explícita mediante `loc` e `iloc`, el filtrado booleano vectorizado con operadores bitwise y el soporte analítico multidimensional con `groupby` y `pivot_table`.

## 10. Referencias oficiales

* [Documentación oficial de la API de Pandas](https://pandas.pydata.org/docs/reference/index.html).
* [Guía de usuario de Pandas](https://pandas.pydata.org/docs/user_guide/index.html).
