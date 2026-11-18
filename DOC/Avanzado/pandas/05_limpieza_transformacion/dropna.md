# `DataFrame.dropna` y `Series.dropna`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.dropna(
    *,
    axis=0,
    how=_NoDefault.no_default,
    thresh=_NoDefault.no_default,
    subset=None,
    inplace=False,
    ignore_index=False
)
```

## 2. ¿Qué es?

Es un **método de depuración estructural** que descarta filas o columnas completas que contengan valores nulos o faltantes.

## 3. ¿Para qué sirve?

Limpia el conjunto de datos de registros incompletos antes de entrenar modelos o exportar reportes.

* **Equivalencia en SQL:** `WHERE columna IS NOT NULL`.

## 4. ¿Cómo funciona?

1. **Filtrado por umbral:** Con `how='any'`, descarta si al menos un elemento es nulo; con `how='all'`, sólo descarta si todos los elementos evaluados son nulos. Con `thresh=k`, exige que existan al menos `k` valores válidos para conservar la fila.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | `0` descarta filas; `1` descarta columnas. |
| `how` | `{'any', 'all'}` | Opcional | `'any'` | Criterio de descarte. |
| `thresh` | `int` | Opcional | `None` | Cantidad mínima de valores no nulos requeridos para no descartar. |
| `subset` | `list[str]` | Opcional | `None` | Columnas específicas a auditar. |
| `ignore_index` | `bool` | Opcional | `False` | Si es `True`, resetea el índice resultante a `0..n-1`. |

## 6. Retorno

* `pandas.DataFrame` o `Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Messi", None, "Mbappé"], "goles": [25, 20, None]})
print(df.dropna())
```

**Salida real:**

```text
  jugador  goles
0   Messi   25.0
```

---

### Nivel 2: Intermedio

Eliminación condicionada a una columna crítica de negocio con reindexación:

```python
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3],
    "jugador": ["Vinicius Jr", None, "Rodrygo"],
    "equipo": ["Real Madrid", "Real Madrid", "Real Madrid"]
})

# Descartar solo si el nombre del jugador falta
print(df.dropna(subset=["jugador"], ignore_index=True))
```

**Salida real:**

```text
   id      jugador       equipo
0   1  Vinicius Jr  Real Madrid
1   3      Rodrygo  Real Madrid
```

---

### Nivel 3: Avanzado

Depuración de columnas mediante umbral de datos válidos (`thresh`):

```python
import pandas as pd

# 4 registros
df_sensores = pd.DataFrame({
    "jugador": ["A", "B", "C", "D"],
    "ritmo_cardiaco": [140, 150, None, 145],  # 3 válidos
    "gps_fallido": [None, None, None, 1]       # 1 válido
})

# Exigir que al menos el 70% de las filas tengan dato (al menos 3 datos no nulos)
df_limpio = df_sensores.dropna(axis=1, thresh=3)
print(df_limpio)
```

**Salida real:**

```text
  jugador  ritmo_cardiaco
0       A           140.0
1       B           150.0
2       C             NaN
3       D           145.0
```

## 8. Errores frecuentes y casos borde

1. Descartar filas completas por descuidar `subset`: Si una columna secundaria tiene muchos nulos, `df.dropna()` sin `subset` puede borrar el 90% del dataset.

## 9. Buenas prácticas y rendimiento

* Usar siempre `subset` con las columnas obligatorias del modelo.

## 10. Métodos relacionados

* [fillna](fillna.md) — Imputación en vez de descarte.
* [isna](../02_inspeccion_exploracion/isna.md) — Identificación de nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.dropna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html) (Pandas 2.2).
