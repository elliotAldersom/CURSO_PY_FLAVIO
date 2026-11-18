# `Series.dt.day_name` y `Series.dt.dayofweek`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.dt.day_name(locale=None) -> pandas.Series[str]
Series.dt.dayofweek -> pandas.Series[int32]
```

## 2. ¿Qué es?

Son **métodos y atributos de día semanal** que devuelven el nombre textual del día o su índice entero (0 = Lunes, 6 = Domingo).

## 3. ¿Para qué sirve?

Permite evaluar patrones de actividad según el día de la semana y aislar fines de semana.

## 4. ¿Cómo funciona?

1. Computa el día de la semana mediante aritmética de calendario gregoriano vectorizada.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `locale` | `str` | Opcional | `None` | Idioma regional para el nombre del día. |

## 6. Retorno

* `pandas.Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-06-01']))
print('Día:', f.dt.day_name().values[0], '| Índice:', f.dt.dayofweek.values[0])
```

**Salida real:**

```text
Día: Saturday | Índice: 5
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

df = pd.DataFrame({'fecha': pd.to_datetime(['2024-05-18', '2024-05-21'])})
df['es_fin_de_semana'] = df['fecha'].dt.dayofweek >= 5
print(df)
```

**Salida real:**

```text
       fecha  es_fin_de_semana
0 2024-05-18              True
1 2024-05-21             False
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'fecha': pd.to_datetime(['2024-05-18', '2024-05-25']), 'km': [12.0, 11.5]})
df['dia'] = df['fecha'].dt.day_name()
print(df.groupby('dia')['km'].sum())
```

**Salida real:**

```text
dia
Saturday    23.5
Name: km, dtype: float64
```

## 8. Errores frecuentes y casos borde

1. Asumir que el índice 0 es Domingo: En Pandas, 0 siempre es Lunes conforme a ISO.

## 9. Buenas prácticas y rendimiento

* Usar `dayofweek >= 5` como condición booleana directa para fines de semana.

## 10. Métodos relacionados

* `dt_isocalendar` — Semanas ISO.

## 11. Referencias oficiales

* **API Reference:** [`Series.dt.day_name` y `Series.dt.dayofweek`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.day_name.html) (Pandas 2.2).
