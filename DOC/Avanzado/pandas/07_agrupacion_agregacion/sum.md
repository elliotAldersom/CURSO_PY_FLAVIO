# `DataFrame.sum` y `Series.sum`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.sum(axis=0, skipna=True, numeric_only=False, min_count=0)
```

## 2. ¿Qué es?

Es un **método de reducción estadística** que computa la sumatoria de los valores a lo largo de un eje.

## 3. ¿Para qué sirve?

Calcula totales de volumen (goles totales, minutos acumulados, inversión salarial).

* **Equivalencia en SQL:** `SUM(columna)`.

## 4. ¿Cómo funciona?

1. Suma los valores contiguos en C ignorando los nulos si `skipna=True`. Si se define `min_count`, exige un mínimo de valores válidos.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | `0` suma por columnas; `1` suma por filas. |
| `skipna` | `bool` | Opcional | `True` | Omite valores faltantes. |
| `min_count` | `int` | Opcional | `0` | Mínimo de valores válidos exigidos; si hay menos, retorna `NaN`. |

## 6. Retorno

* Escalar (en Series) o `pandas.Series` (en DataFrame).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles = pd.Series([25, 28, 31])
print(goles.sum())
```

**Salida real:**

```text
84
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

vacios = pd.Series([None, None])
print('min_count=0:', vacios.sum(min_count=0))
print('min_count=1:', vacios.sum(min_count=1))
```

**Salida real:**

```text
min_count=0: 0.0
min_count=1: nan
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'goles': [21, 28], 'asistencias': [11, 8]})
df['total'] = df.sum(axis=1)
print(df)
```

**Salida real:**

```text
   goles  asistencias  total
0     21           11     32
1     28            8     36
```

## 8. Errores frecuentes y casos borde

1. Sumar columnas tipo object con strings: Concatena los strings en lugar de sumar números.

## 9. Buenas prácticas y rendimiento

* Usar `numeric_only=True` en tablas mixtas para garantizar operaciones puramente numéricas.

## 10. Métodos relacionados

* `cumsum` — Suma acumulada.
* `mean` — Promedio.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.sum` y `Series.sum`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html) (Pandas 2.2).
