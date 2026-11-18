# `Series.value_counts` y `DataFrame.value_counts`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.value_counts(
    normalize=False,
    sort=True,
    ascending=False,
    bins=None,
    dropna=True
)
```

## 2. ¿Qué es?

Es un **método de agregación** que calcula la tabla de distribución de frecuencias para los valores únicos de una Serie o combinaciones de columnas en un DataFrame.

## 3. ¿Para qué sirve?

Permite analizar la frecuencia y porcentaje de categorías, detectar desbalances de clases y explorar la dispersión de variables discretas.

* **Equivalencia en SQL:** Equivale a `SELECT columna, COUNT(*) FROM tabla GROUP BY columna ORDER BY COUNT(*) DESC`.

## 4. ¿Cómo funciona?

1. **Agrupación y ordenamiento:** Agrupa internamente mediante tabla hash y ordena los resultados descendentemente por frecuencia por defecto (`sort=True, ascending=False`). Con `normalize=True`, divide cada conteo por el total de filas obteniendo proporciones relativas.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `normalize` | `bool` | Opcional | `False` | Si es `True`, devuelve proporciones relativas (entre 0 y 1) en lugar de conteos absolutos. |
| `sort` | `bool` | Opcional | `True` | Ordena el resultado por frecuencia. |
| `ascending` | `bool` | Opcional | `False` | Si es `True`, ordena de menor a mayor frecuencia. |
| `bins` | `int` | Opcional | `None` | Agrupa variables numéricas continuas en intervalos semiabiertos. |
| `dropna` | `bool` | Opcional | `True` | Si es `False`, incluye el conteo de valores `NaN`. |

## 6. Retorno

* **Tipo devuelto:** `pandas.Series` indexada por los valores analizados con sus frecuencias correspondientes.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

posiciones = pd.Series(["Delantero", "Mediocampista", "Delantero", "Defensa", "Delantero"])
print(posiciones.value_counts())
```

**Salida real:**

```text
Delantero        3
Mediocampista    1
Defensa          1
Name: count, dtype: int64
```

---

### Nivel 2: Intermedio

Cálculo de porcentajes relativos con inclusión de nulos:

```python
import pandas as pd

equipos = pd.Series(["Real Madrid", "Barcelona", "Real Madrid", None])
print(equipos.value_counts(normalize=True, dropna=False))
```

**Salida real:**

```text
Real Madrid    0.50
Barcelona      0.25
NaN            0.25
Name: proportion, dtype: float64
```

---

### Nivel 3: Avanzado

Agrupación continua por bins para análisis de distribución de goles:

```python
import pandas as pd

goles_jugadores = pd.Series([2, 5, 8, 12, 15, 22, 28, 31, 35])
distribucion = goles_jugadores.value_counts(bins=3, sort=False)
print("Distribución por tramos de goles:")
print(distribucion)
```

**Salida real:**

```text
Distribución por tramos de goles:
(1.966, 13.0]    4
(13.0, 24.0]     2
(24.0, 35.0]     3
Name: count, dtype: int64
```

## 8. Errores frecuentes y casos borde

1. Asumir que la suma de `normalize=True` con `dropna=True` da 1.0 si existen nulos: La suma dará 1.0 respecto a los elementos válidos evaluados.

## 9. Buenas prácticas y rendimiento

* En variables de alta cardinalidad, combinar con `.head(10)` para visualizar únicamente las 10 categorías más dominantes.

## 10. Métodos relacionados

* [nunique](nunique.md) — Conteo escalar de valores únicos.
* [groupby](../07_agrupacion_agregacion/groupby.md) — Agrupaciones más complejas.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.value_counts](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html) (Pandas 2.2).
