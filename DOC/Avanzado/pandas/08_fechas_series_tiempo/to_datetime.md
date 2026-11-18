# `pandas.to_datetime`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=False, format=None)
```

## 2. ¿Qué es?

Es una **función constructora y analizadora de fechas** que convierte strings, marcas de tiempo Unix o secuencias a objetos `Timestamp` o `DatetimeIndex`.

## 3. ¿Para qué sirve?

Habilita el análisis temporal (extracción de días, meses, desfases, resampling) garantizando formatos canónicos ISO 8601.

* **Equivalencia en SQL:** `TO_TIMESTAMP(columna, 'YYYY-MM-DD')`.

## 4. ¿Cómo funciona?

1. Analiza con expresiones léxicas o el formato explícito `format` convirtiendo cada entrada a un entero de nanosegundos `datetime64[ns]` en C.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `arg` | `Series`, lista, `str` | Obligatorio | Posicional | Fechas a transformar. |
| `format` | `str` | Opcional | `None` | Formato explícito de fecha (p. ej. `'%Y-%m-%d'`). Acelera enormemente el parsing. |
| `errors` | `{'raise', 'coerce', 'ignore'}` | Opcional | `'raise'` | `'coerce'` convierte fechas corruptas en `NaT` (*Not a Time*). |
| `dayfirst` | `bool` | Opcional | `False` | Si es `True`, interpreta `01/02/2024` como 1 de febrero. |

## 6. Retorno

* `Timestamp`, `DatetimeIndex` o `Series[datetime64[ns]]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

fechas = pd.Series(['2024-05-15', '2024-06-01'])
fechas_dt = pd.to_datetime(fechas)
print(fechas_dt.dtype)
```

**Salida real:**

```text
datetime64[ns]
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

fechas_mixtas = pd.Series(['15/05/2024', 'FECHA_INVALIDA'])
fechas_limpias = pd.to_datetime(fechas_mixtas, format='%d/%m/%Y', errors='coerce')
print(fechas_limpias.tolist())
```

**Salida real:**

```text
[Timestamp('2024-05-15 00:00:00'), NaT]
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

timestamps_ms = pd.Series([1715760000000, 1718438400000])
fechas_utc = pd.to_datetime(timestamps_ms, unit='ms', utc=True)
print(fechas_utc)
```

**Salida real:**

```text
0   2024-05-15 08:00:00+00:00
1   2024-06-15 08:00:00+00:00
dtype: datetime64[ns, UTC]
```

## 8. Errores frecuentes y casos borde

1. Formatos ambiguos de mes y día (`02/03/2024`): Usar siempre `format='%d/%m/%Y'` o `dayfirst=True` para evitar inferencias erróneas.

## 9. Buenas prácticas y rendimiento

* Especificar siempre `format` si el patrón es constante: acelera la lectura hasta un 500%.

## 10. Métodos relacionados

* `dt` — Accesor temporal.
* `resample` — Remuestreo.

## 11. Referencias oficiales

* **API Reference:** [`pandas.to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) (Pandas 2.2).
