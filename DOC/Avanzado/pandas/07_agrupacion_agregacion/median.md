# `DataFrame.median` y `Series.median`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.median(axis=0, skipna=True, numeric_only=False)
```

## 2. ¿Qué es?

Es un **método estadístico robusto** que calcula el valor mediano (percentil 50) de una distribución.

## 3. ¿Para qué sirve?

Provee una medida de tendencia central insensible a valores atípicos (*outliers*) extremos en distribuciones sesgadas.

* **Equivalencia en SQL:** `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)`.

## 4. ¿Cómo funciona?

1. Ordena los valores válidos y extrae el elemento central (o el promedio de los dos centrales si $N$ es par).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | Eje de cómputo. |
| `skipna` | `bool` | Opcional | `True` | Omite valores nulos. |

## 6. Retorno

* Escalar o `pandas.Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print(s.median())
```

**Salida real:**

```text
30.0
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40])
print(s.median())
```

**Salida real:**

```text
25.0
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

minutos = pd.Series([90, 85, None, 90, 15])
minutos_limpio = minutos.fillna(minutos.median())
print(minutos_limpio)
```

**Salida real:**

```text
0    90.0
1    85.0
2    87.5
3    90.0
4    15.0
dtype: float64
```

## 8. Errores frecuentes y casos borde

1. Conjunto vacío con `skipna=True`: Retorna `NaN`.

## 9. Buenas prácticas y rendimiento

* Preferir frente a la media para variables con distribución asimétrica (como salarios o precios).

## 10. Métodos relacionados

* `mean` — Media aritmética.
* `quantile` — Cuantiles generales.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.median` y `Series.median`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.median.html) (Pandas 2.2).
