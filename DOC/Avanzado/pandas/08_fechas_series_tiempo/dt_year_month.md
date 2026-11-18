# `Series.dt.year` y `Series.dt.month`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.dt.year -> pandas.Series[int32]
Series.dt.month -> pandas.Series[int32]
Series.dt.month_name(locale=None) -> pandas.Series[str]
```

## 2. ¿Qué es?

Son **propiedades y métodos del accesor temporal `.dt`** que extraen el año, mes numérico y nombre de mes.

## 3. ¿Para qué sirve?

Permite segmentar y agregar registros por componentes de calendario anual y mensual.

## 4. ¿Cómo funciona?

1. Accede directamente a los campos de la estructura `datetime64[ns]` de NumPy en tiempo constante.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| *No aplica* | N/A | N/A | N/A | Son propiedades sin argumentos (salvo `month_name(locale)`). |

## 6. Retorno

* `pandas.Series[int32]` o `pandas.Series[str]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-06-15']))
print(f.dt.year.values[0], f.dt.month.values[0])
```

**Salida real:**

```text
2024 6
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

f = pd.to_datetime(pd.Series(['2024-01-10', '2024-08-20']))
print(f.dt.month_name().tolist())
```

**Salida real:**

```text
['January', 'August']
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({'fecha': pd.to_datetime(['2024-01-15', '2024-02-10']), 'goles': [3, 4]})
df['mes'] = df['fecha'].dt.month
print(df)
```

**Salida real:**

```text
       fecha  goles  mes
0 2024-01-15      3    1
1 2024-02-10      4    2
```

## 8. Errores frecuentes y casos borde

1. Invocar sobre una columna que no es datetime: Lanza `AttributeError: Can only use .dt accessor with datetimelike values`.

## 9. Buenas prácticas y rendimiento

* Asegurarse de ejecutar `pd.to_datetime` antes de usar `.dt`.

## 10. Métodos relacionados

* `dt_day_names` — Nombres de día.
* `to_datetime` — Conversión previa.

## 11. Referencias oficiales

* **API Reference:** [`Series.dt.year` y `Series.dt.month`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.year.html) (Pandas 2.2).
