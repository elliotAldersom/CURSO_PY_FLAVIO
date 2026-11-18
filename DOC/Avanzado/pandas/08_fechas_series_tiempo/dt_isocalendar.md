# `Series.dt.isocalendar`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.dt.isocalendar() -> pandas.DataFrame
```

## 2. ¿Qué es?

Es un **método del accesor temporal** que retorna un DataFrame con año, semana y día según ISO 8601.

## 3. ¿Para qué sirve?

Garantiza agrupaciones semanales continuas e interoperables internacionalmente.

## 4. ¿Cómo funciona?

1. Aplica el algoritmo formal ISO donde la primera semana del año es la que contiene el primer jueves.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| *No aplica* | N/A | N/A | N/A | Método sin parámetros. |

## 6. Retorno

* `pandas.DataFrame` con columnas `year`, `week`, `day` en tipo `UInt32`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-01-01', '2024-06-15']))
print(f.dt.isocalendar())
```

**Salida real:**

```text
   year  week  day
0  2024     1    1
1  2024    24    6
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-05-20']))
print('Semana:', f.dt.isocalendar()['week'].values[0])
```

**Salida real:**

```text
Semana: 21
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'fecha': pd.to_datetime(['2024-05-20', '2024-05-28']), 'km': [11.5, 12.0]})
df['semana_iso'] = df['fecha'].dt.isocalendar()['week']
print(df.groupby('semana_iso')['km'].sum())
```

**Salida real:**

```text
semana_iso
21    11.5
22    12.0
Name: km, dtype: float64
```

## 8. Errores frecuentes y casos borde

1. Desajuste de año a fin de año: El 31 de diciembre puede pertenecer a la semana 1 del año siguiente según ISO.

## 9. Buenas prácticas y rendimiento

* Emplear `dt.isocalendar()` en lugar de divisiones de días manuales.

## 10. Métodos relacionados

* `to_period` — Periodos regulares.

## 11. Referencias oficiales

* **API Reference:** [`Series.dt.isocalendar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.isocalendar.html) (Pandas 2.2).
