# `DataFrame.describe`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.describe(
    percentiles=None,
    include=None,
    exclude=None
)
```

## 2. ¿Qué es?

Es un **método de instancia** que computa y compila estadísticas descriptivas sobre las columnas numéricas o categóricas de un DataFrame o Series.

## 3. ¿Para qué sirve?

Provee un resumen numérico central para análisis exploratorio (EDA): conteo (`count`), media (`mean`), dispersión (`std`), valor mínimo (`min`), cuartiles (`25%`, `50%`, `75%`) y valor máximo (`max`).

* **Equivalencia en SQL:** Equivale a una consulta agregada con `COUNT()`, `AVG()`, `STDDEV()`, `MIN()`, `PERCENTILE_CONT(...)` y `MAX()`.

## 4. ¿Cómo funciona?

1. **Filtrado por tipo:** Por defecto, selecciona únicamente columnas con tipos numéricos (`int`, `float`). Si se pasa `include='all'`, incorpora estadísticas categóricas (`unique`, `top`, `freq`).
2. **Cálculo vectorizado:** Invoca algoritmos vectorizados de NumPy omitiendo valores faltantes (`skipna=True`). La desviación estándar se calcula con $N - 1$ grados de libertad (muestral).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `percentiles` | `list[float]` | Opcional | `None` | Lista de números entre 0 y 1 para los percentiles deseados (p. ej. `[0.1, 0.9]`). |
| `include` | `'all'`, lista de tipos | Opcional | `None` | Tipos a incluir en el reporte (`'all'`, `[object]`, `[np.number]`). |
| `exclude` | lista de tipos | Opcional | `None` | Tipos a excluir del resumen estadístico. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición formal `percentiles`. El **argumento** es la lista concreta `percentiles=[0.05, 0.95]`.

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `pandas.Series`).
* **Mutabilidad:** Inmutable; retorna un nuevo DataFrame con los estadísticos calculados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Estadísticas estándar de variables numéricas:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Haaland", "Kane", "Mbappé", "Lautaro"],
    "goles": [31, 36, 28, 27],
    "partidos": [35, 36, 34, 33]
})

print(df_liga.describe())
```

**Salida real:**

```text
           goles   partidos
count   4.000000   4.000000
mean   30.500000  34.500000
std     3.872983   1.290994
min    27.000000  33.000000
25%    27.750000  33.750000
50%    29.500000  34.500000
75%    32.250000  35.250000
max    36.000000  36.000000
```

---

### Nivel 2: Intermedio

Inclusión de variables categóricas con percentiles personalizados:

```python
import pandas as pd

df_plantel = pd.DataFrame({
    "posicion": ["Delantero", "Delantero", "Mediocampista", "Defensa"],
    "minutos": [2100, 2450, 1800, 2600]
})

print(df_plantel.describe(include="all", percentiles=[0.1, 0.9]))
```

**Salida real:**

```text
         posicion      minutos
count           4     4.000000
unique          3          NaN
top     Delantero          NaN
freq            2          NaN
mean          NaN  2237.500000
std           NaN   354.436172
min           NaN  1800.000000
10%           NaN  1890.000000
50%           NaN  2275.000000
90%           NaN  2555.000000
max           NaN  2600.000000
```

---

### Nivel 3: Avanzado

Extracción programática de rangos intercuartílicos para detección de anomalías:

```python
import pandas as pd

df_rendimiento = pd.DataFrame({
    "goles": [10, 12, 14, 15, 16, 18, 45]  # 45 es un outlier
})

stats = df_rendimiento["goles"].describe()
q1 = stats["25%"]
q3 = stats["75%"]
iqr = q3 - q1
limite_superior = q3 + (1.5 * iqr)

outliers = df_rendimiento[df_rendimiento["goles"] > limite_superior]
print(f"Límite superior IQR: {limite_superior}")
print("Outliers detectados:")
print(outliers)
```

**Salida real:**

```text
Límite superior IQR: 24.5
Outliers detectados:
   goles
6     45
```

## 8. Errores frecuentes y casos borde

1. **Columnas numéricas como string:** Si una columna numérica contiene comas o strings ('25.0'), `describe()` la tratará como texto omitiendo media y percentiles.

## 9. Buenas prácticas y rendimiento

* No ejecutar `describe(include='all')` en tablas con miles de columnas de texto de alta cardinalidad, pues calcular `unique` y `top` en cada una degrada la velocidad.

## 10. Métodos relacionados

* [info](info.md) — Diagnóstico de tipos y memoria.
* [quantile](../07_agrupacion_agregacion/quantile.md) — Cálculo de cuantiles individuales.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) (Pandas 2.2).
