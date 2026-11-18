# `Series.dt.to_period`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.dt.to_period(freq=None) -> pandas.Series[Period]
```

## 2. ¿Qué es?

Es un **método de transformación temporal** que convierte marcas de tiempo en intervalos regulares (`Period`).

## 3. ¿Para qué sirve?

Agrupa fechas en bloques mensuales o trimestrales sin horas ni segundos residuales.

## 4. ¿Cómo funciona?

1. Trunca y mapea cada Timestamp a su intervalo representativo de frecuencia `freq`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `freq` | `str` | Opcional | `None` | Frecuencia objetivo (`'M'` mes, `'Q'` trimestre, `'Y'` año). |

## 6. Retorno

* `pandas.Series[Period]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-05-15', '2024-06-20']))
print(f.dt.to_period('M'))
```

**Salida real:**

```text
0    2024-05
1    2024-06
dtype: period[M]
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-02-10', '2024-08-15']))
print(f.dt.to_period('Q'))
```

**Salida real:**

```text
0    2024Q1
1    2024Q3
dtype: period[Q-DEC]
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'fecha': pd.to_datetime(['2024-01-05', '2024-02-14']), 'goles': [2, 4]})
df['periodo_mes'] = df['fecha'].dt.to_period('M')
print(df.groupby('periodo_mes')['goles'].sum())
```

**Salida real:**

```text
periodo_mes
2024-01    2
2024-02    4
Freq: M, Name: goles, dtype: int64
```

## 8. Errores frecuentes y casos borde

1. Comparar un `Period` con un string sin castear: Puede lanzar advertencias en versiones estrictas.

## 9. Buenas prácticas y rendimiento

* Convertir a `Period` antes de generar reportes financieros o de temporada deportiva.

## 10. Métodos relacionados

* `resample` — Remuestreo temporal.

## 11. Referencias oficiales

* **API Reference:** [`Series.dt.to_period`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.to_period.html) (Pandas 2.2).
