# Accesor `Series.dt` en Pandas

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.dt -> pandas.core.accessor.CombinedDatetimelikeProperties
```

## 2. ¿Qué es?

Es un **accesor de propiedades y métodos vectorizados** especializado en columnas de tipo fecha y hora (`datetime64`, `timedelta`, `Period`).

## 3. ¿Para qué sirve?

Expone atributos temporales (`year`, `month`, `day`, `day_name()`) de forma vectorizada sin necesidad de iterar con bucles Python.

## 4. ¿Cómo funciona?

1. Mapea las estructuras temporales de C en NumPy/Arrow exponiendo getters y métodos optimizados en tiempo constante.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| *No aplica* | N/A | N/A | N/A | Es un objeto accesor, no una función directa. |

## 6. Retorno

* Accesor `CombinedDatetimelikeProperties`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

fechas = pd.to_datetime(pd.Series(['2024-06-01', '2024-12-25']))
print('Años:', fechas.dt.year.tolist())
```

**Salida real:**

```text
Años: [2024, 2024]
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

fechas = pd.to_datetime(pd.Series(['2024-05-15']))
print('Día:', fechas.dt.day_name().values[0])
print('Mes:', fechas.dt.month_name().values[0])
```

**Salida real:**

```text
Día: Wednesday
Mes: May
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

contratos = pd.to_datetime(pd.Series(['2020-07-01', '2023-01-15']))
ref = pd.to_datetime('2024-07-01')
print((ref - contratos).dt.days.tolist())
```

**Salida real:**

```text
[1461, 533]
```

## 8. Errores frecuentes y casos borde

1. Usar `.dt` sobre una columna de texto (`object`): Lanza `AttributeError`.

## 9. Buenas prácticas y rendimiento

* Ejecutar siempre `pd.to_datetime()` antes de acceder a `.dt`.

## 10. Métodos relacionados

* `to_datetime` — Conversión previa.
* `dt_year_month` — Año y mes.

## 11. Referencias oficiales

* **API Reference:** [Accesor `Series.dt` en Pandas](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html) (Pandas 2.2).
