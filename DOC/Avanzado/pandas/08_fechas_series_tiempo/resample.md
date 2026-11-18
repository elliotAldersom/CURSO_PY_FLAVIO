# `DataFrame.resample` y `Series.resample`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.resample(rule, axis=0, closed=None, label=None, on=None)
```

## 2. ¿Qué es?

Es un **método de remuestreo temporal** (análogo a un `groupby` de series temporales) que convierte datos a frecuencias regulares.

## 3. ¿Para qué sirve?

Permite consolidar series temporales irregulares en intervalos fijos (`'D'` diario, `'W'` semanal, `'ME'` mensual).

## 4. ¿Cómo funciona?

1. Agrupa los registros que caen dentro de cada celda de tiempo de la regla de frecuencia `rule` y aplica una función agregadora.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `rule` | `str`, offset | Obligatorio | Posicional | Frecuencia de remuestreo (`'D'`, `'W'`, `'ME'`, `'h'`). |
| `on` | `str` | Opcional | `None` | Columna con fecha si el índice no es temporal. |

## 6. Retorno

* `Resampler` (objeto perezoso).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

fechas = pd.date_range('2024-01-01', periods=4, freq='D')
s = pd.Series([1, 2, 3, 4], index=fechas)
print(s.resample('2D').sum())
```

**Salida real:**

```text
2024-01-01    3
2024-01-03    7
Freq: 2D, dtype: int64
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

df = pd.DataFrame({
    'fecha': pd.to_datetime(['2024-01-10', '2024-01-20', '2024-02-05']),
    'goles': [2, 3, 4]
})
print(df.resample('ME', on='fecha')['goles'].sum())
```

**Salida real:**

```text
fecha
2024-01-31    5
2024-02-29    4
Freq: ME, Name: goles, dtype: int64
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

idx = pd.date_range('2024-06-01 20:00', periods=30, freq='min')
df = pd.DataFrame({'bpm': [140 + i for i in range(30)]}, index=idx)
print(df.resample('15min').mean())
```

**Salida real:**

```text
                     bpm
2024-06-01 20:00:00  147.0
2024-06-01 20:15:00  162.0
```

## 8. Errores frecuentes y casos borde

1. Olvidar que el índice debe ser DatetimeIndex o usar `on='columna_fecha'`.

## 9. Buenas prácticas y rendimiento

* En Pandas 2.2+, usar `'ME'` para fin de mes en lugar de la regla deprecada `'M'`.

## 10. Métodos relacionados

* `to_datetime` — Conversión previa.
* `groupby` — Agrupaciones generales.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.resample` y `Series.resample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html) (Pandas 2.2).
