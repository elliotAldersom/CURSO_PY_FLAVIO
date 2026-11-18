# `DataFrame.quantile` y `Series.quantile`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.quantile(q=0.5, axis=0, numeric_only=False, interpolation='linear')
```

## 2. ¿Qué es?

Es un **método de cálculo de cuantiles** que computa el valor en el umbral especificado `q` (entre 0.0 y 1.0).

## 3. ¿Para qué sirve?

Calcula percentiles arbitrarios (P90, P95, P99) para aislar colas de distribución y detectar anomalías.

## 4. ¿Cómo funciona?

1. Ordena los datos válidos e interpola matemáticamente según `interpolation` (`linear`, `nearest`, `lower`, `higher`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `q` | `float`, `list[float]` | Opcional | `0.5` | Cuantil(es) a computar (entre 0 y 1). |
| `interpolation` | `str` | Opcional | `'linear'` | Método de interpolación matemática. |

## 6. Retorno

* Escalar, `Series` o `DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles = pd.Series([5, 10, 15, 20, 25, 30])
print(goles.quantile(0.9))
```

**Salida real:**

```text
27.5
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

minutos = pd.Series([500, 1200, 1800, 2400, 2700])
print(minutos.quantile([0.25, 0.5, 0.75]))
```

**Salida real:**

```text
0.25    1200.0
0.50    1800.0
0.75    2400.0
dtype: float64
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'jugador': ['A', 'B', 'C', 'D'], 'dist': [10.2, 11.5, 12.8, 11.0]})
u_p90 = df['dist'].quantile(0.9)
print(df[df['dist'] >= u_p90])
```

**Salida real:**

```text
  jugador  dist
2       C  12.8
```

## 8. Errores frecuentes y casos borde

1. Pasar `q` fuera del rango `[0, 1]`: Lanza `ValueError`.

## 9. Buenas prácticas y rendimiento

* Utilizar percentiles para establecer umbrales dinámicos de clasificación deportiva.

## 10. Métodos relacionados

* `qcut` — Discretización por cuantiles.
* `describe` — Cuartiles estándar.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.quantile` y `Series.quantile`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.quantile.html) (Pandas 2.2).
