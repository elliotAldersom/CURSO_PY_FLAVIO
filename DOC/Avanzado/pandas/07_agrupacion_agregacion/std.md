# `DataFrame.std` y `Series.std`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.std(axis=0, skipna=True, ddof=1, numeric_only=False)
```

## 2. ¿Qué es?

Es un **método de dispersión estadística** que calcula la desviación estándar muestral de los datos.

## 3. ¿Para qué sirve?

Mide la variabilidad o dispersión respecto a la media para cuantificar consistencia en el rendimiento.

## 4. ¿Cómo funciona?

1. Computa la raíz cuadrada de la varianza muestral con divisor $N - ddof$ en código C optimizado.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `ddof` | `int` | Opcional | `1` | Grados de libertad delta (`1` muestral, `0` poblacional). |
| `skipna` | `bool` | Opcional | `True` | Omite nulos. |

## 6. Retorno

* Escalar o `pandas.Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

rendimiento = pd.Series([10, 12, 11, 13])
print(round(rendimiento.std(), 2))
```

**Salida real:**

```text
1.29
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

s = pd.Series([10, 20, 30])
print('Muestral:', round(s.std(ddof=1), 2))
print('Poblacional:', round(s.std(ddof=0), 2))
```

**Salida real:**

```text
Muestral: 10.0
Poblacional: 8.16
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'minutos': [2100, 2450, 1800, 2600]})
df['z_score'] = ((df['minutos'] - df['minutos'].mean()) / df['minutos'].std()).round(2)
print(df)
```

**Salida real:**

```text
   minutos  z_score
0     2100    -0.39
1     2450     0.60
2     1800    -1.23
3     2600     1.02
```

## 8. Errores frecuentes y casos borde

1. Un solo elemento en la serie con `ddof=1`: Divisor $N - 1 = 0$, retorna `NaN`.

## 9. Buenas prácticas y rendimiento

* Para normalización Z-Score, usar `ddof=0` o `ddof=1` de forma consistente en todo el pipeline.

## 10. Métodos relacionados

* `mean` — Media.
* `corr` — Correlación.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.std` y `Series.std`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.std.html) (Pandas 2.2).
