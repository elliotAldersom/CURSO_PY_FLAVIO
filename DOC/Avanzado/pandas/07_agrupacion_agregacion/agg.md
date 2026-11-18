# `DataFrame.agg` y `DataFrameGroupBy.agg`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.agg(func=None, axis=0, *args, **kwargs)
```

## 2. ¿Qué es?

Es un **método de agregación multifunción** que permite aplicar múltiples funciones estadísticas (como `'mean'`, `'sum'`, `'count'`, desvío o funciones de usuario) a diferentes columnas en una sola instrucción.

## 3. ¿Para qué sirve?

Genera resúmenes ejecutivos avanzados aplicando métricas heterogéneas por columna (p. ej. suma de goles y promedio de minutos simultáneamente).

* **Equivalencia en SQL:** `SELECT SUM(goles), AVG(minutos), MAX(asistencias) GROUP BY ...`.

## 4. ¿Cómo funciona?

1. **Despacho columnar:** Mapea el diccionario `{columna: [funciones]}` evaluando cada operación en código C vectorizado de Pandas/NumPy.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `func` | `str`, `callable`, `list`, `dict` | Obligatorio | Posicional | Funciones a computar. |
| `axis` | `{0, 1}` | Opcional | `0` | Eje de agregación (`0` columnas). |

## 6. Retorno

* `pandas.Series` o `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Múltiples métricas sobre una sola Serie:

```python
import pandas as pd

goles = pd.Series([21, 28, 15, 31])
print(goles.agg(["sum", "mean", "max"]))
```

**Salida real:**

```text
sum     95.00
mean    23.75
max     31.00
dtype: float64
```

---

### Nivel 2: Intermedio

Agregaciones diferenciadas por columna mediante diccionario:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Bellingham"],
    "goles": [21, 28, 19],
    "asistencias": [11, 8, 12]
})

print(df.agg({"goles": ["sum", "max"], "asistencias": "mean"}))
```

**Salida real:**

```text
      goles  asistencias
sum    68.0          NaN
max    28.0          NaN
mean    NaN    10.333333
```

---

### Nivel 3: Avanzado

Agregación con tuplas nombradas (*Named Aggregation*) para columnas limpias sin MultiIndex:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona", "Barcelona"],
    "goles": [21, 28, 26, 18],
    "minutos": [2100, 2450, 2600, 1800]
})

df_resumen = df_liga.groupby("equipo").agg(
    total_goles=pd.NamedAgg(column="goles", aggfunc="sum"),
    minutos_promedio=pd.NamedAgg(column="minutos", aggfunc="mean"),
    jugadores_evaluados=pd.NamedAgg(column="goles", aggfunc="count")
).reset_index()

print(df_resumen)
```

**Salida real:**

```text
        equipo  total_goles  minutos_promedio  jugadores_evaluados
0    Barcelona           44            2200.0                    2
1  Real Madrid           49            2275.0                    2
```

## 8. Errores frecuentes y casos borde

1. Pasar listas de funciones a múltiples columnas genera encabezados MultiIndex complejos. Usar `pd.NamedAgg` para evitarlo.

## 9. Buenas prácticas y rendimiento

* Pasar nombres como strings (`'sum'`, `'mean'`) en lugar de funciones de Python puro (`sum`, `np.mean`) para aprovechar las implementaciones optimizadas en C (*Cython fast-paths*).

## 10. Métodos relacionados

* [groupby](groupby.md) — Agrupación previa.
* [pivot_table](pivot_table.md) — Agregación multidimensional.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.agg](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html) (Pandas 2.2).
