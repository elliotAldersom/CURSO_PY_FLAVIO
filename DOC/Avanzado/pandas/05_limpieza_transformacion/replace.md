# `DataFrame.replace` y `Series.replace`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.replace(
    to_replace=None,
    value=_NoDefault.no_default,
    *,
    inplace=False,
    limit=None,
    regex=False,
    method=_NoDefault.no_default
)
```

## 2. ¿Qué es?

Es un **método de sustitución de valores** que mapea y reemplaza datos escalares, listas, diccionarios o patrones Regex por nuevos valores.

## 3. ¿Para qué sirve?

Corrige errores tipográficos, estandariza valores nulos codificados como cadenas mágicas (`'-'`, `'N/A'`, `'?'`) y remapea categorías.

* **Equivalencia en SQL:** Expresión `CASE WHEN col = 'A' THEN 'B' ELSE col END`.

## 4. ¿Cómo funciona?

1. **Sustitución exacta o por Regex:** Si `regex=False`, busca coincidencias exactas. Con diccionarios anidados, permite aplicar reglas específicas para diferentes columnas simultáneamente.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `to_replace` | escalar, lista, `dict`, Regex | Obligatorio | Posicional | Valor(es) a buscar y reemplazar. |
| `value` | escalar, lista, `dict` | Opcional | `None` | Valor de reemplazo. |
| `regex` | `bool` | Opcional | `False` | Si es `True`, interpreta `to_replace` como expresión regular. |

## 6. Retorno

* `pandas.DataFrame` o `Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

posiciones = pd.Series(["DEL", "MED", "DEF", "DEL"])
print(posiciones.replace({"DEL": "Delantero", "MED": "Mediocampista"}))
```

**Salida real:**

```text
0        Delantero
1    Mediocampista
2              DEF
3        Delantero
dtype: object
```

---

### Nivel 2: Intermedio

Reemplazo masivo de valores centinela por `np.nan`:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Pedri", "Gavi"],
    "goles": ["?", "4"],
    "minutos": ["-", "1200"]
})

df_limpio = df.replace(["?", "-"], np.nan)
print(df_limpio)
```

**Salida real:**

```text
  jugador goles minutos
0   Pedri   NaN     NaN
1    Gavi     4    1200
```

---

### Nivel 3: Avanzado

Sustitución basada en expresiones regulares avanzadas:

```python
import pandas as pd

df_salarios = pd.DataFrame({
    "jugador": ["Haaland", "Mbappé"],
    "salario_txt": ["$ 25,000,000 USD", "$ 30,000,000 USD"]
})

# Limpieza Regex de caracteres no numéricos
df_salarios["salario_num"] = df_salarios["salario_txt"].replace(r"[^\d]", "", regex=True).astype("int64")
print(df_salarios[["jugador", "salario_num"]])
```

**Salida real:**

```text
   jugador  salario_num
0  Haaland     25000000
1   Mbappé     30000000
```

## 8. Errores frecuentes y casos borde

1. Confundir `replace()` con `Series.str.replace()`: `replace()` busca por defecto la celda entera; `str.replace()` busca subcadenas dentro del texto.

## 9. Buenas prácticas y rendimiento

* Usar diccionarios `{antiguo: nuevo}` para máxima expresividad.

## 10. Métodos relacionados

* [map](map.md) — Mapeo exhaustivo de una Serie.
* [fillna](fillna.md) — Imputación específica de nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.replace](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html) (Pandas 2.2).
