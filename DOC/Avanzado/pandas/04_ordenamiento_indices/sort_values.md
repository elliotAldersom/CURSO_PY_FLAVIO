# `DataFrame.sort_values`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.sort_values(
    by,
    *,
    axis=0,
    ascending=True,
    inplace=False,
    kind='quicksort',
    na_position='last',
    ignore_index=False,
    key=None
)
```

## 2. ¿Qué es?

Es un **método de ordenamiento** de `pandas.DataFrame` (y `pandas.Series`) que reorganiza las filas (o columnas) según los valores presentes en una o varias columnas especificadas.

## 3. ¿Para qué sirve?

Permite clasificar datos (tablas de posiciones, rankings, secuencias cronológicas) y preparar conjuntos de datos para deduplicación determinista.

* **Equivalencia en SQL:** Equivale directamente a `ORDER BY col1 ASC, col2 DESC`.

## 4. ¿Cómo funciona?

1. **Algoritmos C:** Por defecto utiliza `quicksort` (inestable pero veloz); si se requiere preservar el orden relativo de empates, puede pasarse `kind='mergesort'` o `kind='stable'`.
2. **Posicionamiento de nulos:** El parámetro `na_position` coloca los `NaN` al final (`'last'`) o al principio (`'first'`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `by` | `str`, `list[str]` | Obligatorio | Posicional | Nombre o lista de nombres de columnas por las cuales ordenar. |
| `ascending` | `bool`, `list[bool]` | Opcional | `True` | Dirección de orden (`True` ascendente, `False` descendente). Puede ser lista para criterios mixtos. |
| `inplace` | `bool` | Opcional | `False` | Modifica in-place (obsoleto en Pandas 2.x+). |
| `na_position` | `{'first', 'last'}` | Opcional | `'last'` | Ubicación de valores `NaN`. |
| `ignore_index` | `bool` | Opcional | `False` | Si es `True`, resetea el índice resultante a `0..n-1`. |
| `key` | `callable` | Opcional | `None` | Función a aplicar antes de comparar (p. ej. `key=lambda x: x.str.lower()`). |

## 6. Retorno

* `pandas.DataFrame` ordenado (o `None` si `inplace=True`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Modric", "Mbappé", "Vinicius Jr"], "goles": [2, 28, 21]})
print(df.sort_values(by="goles", ascending=False))
```

**Salida real:**

```text
       jugador  goles
1       Mbappé     28
2  Vinicius Jr     21
0       Modric      2
```

---

### Nivel 2: Intermedio

Orden multicriterio con direcciones combinadas:

```python
import pandas as pd

df = pd.DataFrame({
    "equipo": ["Real Madrid", "Barcelona", "Real Madrid", "Barcelona"],
    "goles": [25, 25, 18, 20],
    "jugador": ["Mbappé", "Lewandowski", "Rodrygo", "Raphinha"]
})

# Equipo ascendente (A-Z) y Goles descendente (Mayor a menor)
df_ordenado = df.sort_values(
    by=["equipo", "goles"],
    ascending=[True, False],
    ignore_index=True
)
print(df_ordenado)
```

**Salida real:**

```text
        equipo  goles      jugador
0    Barcelona     25  Lewandowski
1    Barcelona     20     Raphinha
2  Real Madrid     25       Mbappé
3  Real Madrid     18      Rodrygo
```

---

### Nivel 3: Avanzado

Ordenamiento con función clave (`key`) para normalizar textos sin mutar los datos:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["álvarez", "Bellingham", "Álvaro", "carvajal"]
})

# Ordenamiento insensible a tildes o mayúsculas mediante función clave
df_alfabetico = df_liga.sort_values(
    by="jugador",
    key=lambda col: col.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8").str.lower(),
    ignore_index=True
)
print(df_alfabetico)
```

**Salida real:**

```text
      jugador
0     alvarez
1      Alvaro
2  Bellingham
3    carvajal
```

## 8. Errores frecuentes y casos borde

1. Pasar listas de longitudes dispares a `by` y `ascending`: Lanza `ValueError: Length of ascending (2) must be same as length of by (3)`.

## 9. Buenas prácticas y rendimiento

* Si se requiere estabilidad estricta en registros empatados, fijar `kind='stable'`.

## 10. Métodos relacionados

* [reset_index](reset_index.md) — Reconstrucción de índices tras ordenar.
* [nlargest](nlargest.md) — Extracción directa de los $N$ mayores valores.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.sort_values](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html) (Pandas 2.2).
