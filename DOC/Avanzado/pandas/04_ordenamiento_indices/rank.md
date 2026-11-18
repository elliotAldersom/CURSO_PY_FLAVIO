# `DataFrame.rank` y `Series.rank`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.rank(
    axis=0,
    method='average',
    numeric_only=False,
    na_option='keep',
    ascending=True,
    pct=False
)
```

## 2. ¿Qué es?

Es un **método de cálculo ordinal estadístico** que asigna rangos numéricos (posiciones en ranking) a los valores de una Serie o columnas de un DataFrame.

## 3. ¿Para qué sirve?

Calcula clasificaciones ordinales manejando empates formalmente, y computa percentiles o posiciones relativas para modelado y tablas de posiciones deportivas.

* **Equivalencia en SQL:** Funciones de ventana `RANK() OVER (ORDER BY ...)`, `DENSE_RANK()`, `ROW_NUMBER()`.

## 4. ¿Cómo funciona?

1. **Políticas de desempate:** Permite configurar `method`:
   * `'average'`: Promedio de rangos empatados (p. ej. empate en 1º y 2º puesto da 1.5).
   * `'min'`: Rango mínimo del empate (análogo a `RANK()` en SQL).
   * `'dense'`: Rangos consecutivos sin saltos (análogo a `DENSE_RANK()` en SQL).
   * `'first'`: Orden de aparición en datos.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `method` | `{'average', 'min', 'max', 'first', 'dense'}` | Opcional | `'average'` | Criterio para desempatar valores idénticos. |
| `ascending` | `bool` | Opcional | `True` | `True` asigna el rango 1 al menor valor; `False` al mayor. |
| `pct` | `bool` | Opcional | `False` | Si es `True`, calcula rangos normalizados entre 0 y 1. |

## 6. Retorno

* `pandas.DataFrame` o `Series` con valores de rango flotantes o enteros.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles = pd.Series([25, 25, 31], index=["Messi", "Mbappé", "Haaland"])
# Ranking descendente (más goles = mejor puesto)
print(goles.rank(ascending=False, method="min"))
```

**Salida real:**

```text
Messi      2.0
Mbappé     2.0
Haaland    1.0
dtype: float64
```

---

### Nivel 2: Intermedio

Comparación de métodos `dense` vs `min` en tabla de goleadores:

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["A", "B", "C", "D"], "goles": [30, 25, 25, 20]})
df["rank_min"] = df["goles"].rank(ascending=False, method="min")
df["rank_dense"] = df["goles"].rank(ascending=False, method="dense")
print(df)
```

**Salida real:**

```text
  jugador  goles  rank_min  rank_dense
0       A     30       1.0         1.0
1       B     25       2.0         2.0
2       C     25       2.0         2.0
3       D     20       4.0         3.0
```

---

### Nivel 3: Avanzado

Cálculo de percentil acumulado de rendimiento (`pct=True`):

```python
import pandas as pd

df_rendimiento = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Bellingham", "Rodrygo", "Guler"],
    "puntos": [92, 95, 80, 75]
})

df_rendimiento["percentil"] = (
    df_rendimiento["puntos"].rank(pct=True, ascending=True) * 100
).round(1)
print(df_rendimiento.sort_values(by="percentil", ascending=False))
```

**Salida real:**

```text
       jugador  puntos  percentil
1   Bellingham      95      100.0
0  Vinicius Jr      92       75.0
2      Rodrygo      80       50.0
3        Guler      75       25.0
```

## 8. Errores frecuentes y casos borde

1. No notar que `ascending=True` da el puesto 1 al menor valor por defecto. Para rankings donde más es mejor, usar `ascending=False`.

## 9. Buenas prácticas y rendimiento

* Usar `method='dense'` para clasificaciones deportivas oficiales.

## 10. Métodos relacionados

* [sort_values](sort_values.md) — Reorganiza físicamente las filas.
* [nlargest](nlargest.md) — Obtiene los $N$ mayores.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.rank](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html) (Pandas 2.2).
