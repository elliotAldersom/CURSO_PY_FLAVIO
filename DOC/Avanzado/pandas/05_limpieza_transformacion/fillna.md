# `DataFrame.fillna` y `Series.fillna`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.fillna(
    value=None,
    *,
    method=None,
    axis=None,
    inplace=False,
    limit=None,
    downcast=_NoDefault.no_default
)
```

## 2. ¿Qué es?

Es un **método de imputación de datos** que sustituye valores nulos (`NaN`, `None`, `pd.NA`) por constantes predefinidas o valores derivados mediante diccionarios.

## 3. ¿Para qué sirve?

Previene fallos en algoritmos de Machine Learning y evita la propagación de nulos en cálculos de agregación.

* **Equivalencia en SQL:** `COALESCE(columna, valor_defecto)`.

## 4. ¿Cómo funciona?

1. **Reemplazo vectorizado:** Identifica las posiciones nulas y las sobrescribe en un nuevo arreglo preservando la tipología.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `value` | escalar, `dict`, `Series` | Opcional | `None` | Valor a inyectar en lugar de los nulos. |
| `method` | `{'ffill', 'bfill'}` | Opcional | `None` | Propagación hacia adelante/atrás (**obsoleto**: usar `df.ffill()` o `df.bfill()`). |
| `inplace` | `bool` | Opcional | `False` | Obsoleto en Pandas 2.x+. |

## 6. Retorno

* `pandas.DataFrame` o `Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles = pd.Series([25, None, 18])
print(goles.fillna(0))
```

**Salida real:**

```text
0    25.0
1     0.0
2    18.0
dtype: float64
```

---

### Nivel 2: Intermedio

Imputación específica por columna mediante diccionario:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Guler"],
    "goles": [21, None],
    "categoria": [None, "Suplente"]
})

df_imputado = df.fillna({
    "goles": 0,
    "categoria": "Sin Categoría"
})
print(df_imputado)
```

**Salida real:**

```text
       jugador  goles      categoria
0  Vinicius Jr   21.0  Sin Categoría
1        Guler    0.0       Suplente
```

---

### Nivel 3: Avanzado

Imputación estadística con la media grupal sin data leakage:

```python
import pandas as pd

df_rendimiento = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona", "Barcelona"],
    "minutos": [2100, None, 1800, None]
})

# Imputa el promedio del equipo correspondiente
df_rendimiento["minutos"] = df_rendimiento["minutos"].fillna(
    df_rendimiento.groupby("equipo")["minutos"].transform("mean")
)
print(df_rendimiento)
```

**Salida real:**

```text
        equipo  minutos
0  Real Madrid   2100.0
1  Real Madrid   2100.0
2    Barcelona   1800.0
3    Barcelona   1800.0
```

## 8. Errores frecuentes y casos borde

1. Usar `method='ffill'` dentro de `fillna`: Lanza advertencia de obsolescencia. Utilizar `.ffill()` directamente.

## 9. Buenas prácticas y rendimiento

* Pasar un diccionario con los valores de imputación por columna en lugar de imputar un valor genérico sobre toda la tabla.

## 10. Métodos relacionados

* [dropna](dropna.md) — Eliminación de filas con nulos.
* [isna](../02_inspeccion_exploracion/isna.md) — Detección de nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.fillna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html) (Pandas 2.2).
