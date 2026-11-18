# `pandas.merge` y `DataFrame.merge`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.merge(
    left,
    right,
    how='inner',
    on=None,
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=False,
    suffixes=('_x', '_y'),
    copy=None,
    indicator=False,
    validate=None
) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es una **función y método de combinación relacional** que une dos DataFrames basándose en columnas de clave compartida o en sus índices, implementando operaciones de álgebra relacional.

## 3. ¿Para qué sirve?

Permite cruzar entidades relacionadas (p. ej. jugadores con sus contratos, estadísticas de partidos con datos de clubes) mediante uniones equivalentes a SQL.

* **Equivalencia en SQL:** Sentencias `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN` y `CROSS JOIN`.

## 4. ¿Cómo funciona?

1. **Hash Join en C:** Utiliza algoritmos de unión por tabla hash en C/Cython que indexan la clave de la tabla menor y sondean las filas de la tabla mayor en tiempo lineal $O(N + M)$.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `how` | `{'inner', 'left', 'right', 'outer', 'cross'}` | Opcional | `'inner'` | Tipo de unión relacional. |
| `on` | `str`, `list[str]` | Opcional | `None` | Nombre(s) de columna compartidos en ambos DataFrames. |
| `left_on` / `right_on` | `str`, `list[str]` | Opcional | `None` | Columnas clave si se llaman diferente en cada tabla. |
| `suffixes` | `tuple[str, str]` | Opcional | `('_x', '_y')` | Sufijos para desambiguar columnas con nombres idénticos que no son clave. |
| `indicator` | `bool`, `str` | Opcional | `False` | Añade la columna `_merge` indicando el origen (`left_only`, `both`, `right_only`). |
| `validate` | `{'1:1', '1:m', 'm:1', 'm:m'}` | Opcional | `None` | Valida la cardinalidad contractual de la unión. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Inner join por clave compartida:

```python
import pandas as pd

df_jugadores = pd.DataFrame({"id": [1, 2], "jugador": ["Vinicius Jr", "Mbappé"]})
df_goles = pd.DataFrame({"id": [1, 2], "goles": [21, 28]})

df_unido = pd.merge(df_jugadores, df_goles, on="id")
print(df_unido)
```

**Salida real:**

```text
   id      jugador  goles
0   1  Vinicius Jr     21
1   2       Mbappé     28
```

---

### Nivel 2: Intermedio

Left join con trazabilidad de origen mediante `indicator=True`:

```python
import pandas as pd

df_plantel = pd.DataFrame({"id": [1, 2, 3], "jugador": ["Modric", "Kroos", "Guler"]})
df_titulares = pd.DataFrame({"id": [1, 2], "minutos": [1600, 2100]})

df_cruce = pd.merge(df_plantel, df_titulares, on="id", how="left", indicator=True)
print(df_cruce)
```

**Salida real:**

```text
   id jugador  minutos     _merge
0   1  Modric   1600.0       both
1   2   Kroos   2100.0       both
2   3   Guler      NaN  left_only
```

---

### Nivel 3: Avanzado

Validación contractual estricta de cardinalidad uno-a-muchos (`validate='1:m'`):

```python
import pandas as pd

df_club = pd.DataFrame({"club_id": [10], "nombre_club": ["Real Madrid"]})
df_jugadores = pd.DataFrame({"club_id": [10, 10], "jugador": ["Vinicius Jr", "Bellingham"]})

# validate='1:m' verifica que 'club_id' sea único en la tabla izquierda
df_validado = pd.merge(df_club, df_jugadores, on="club_id", validate="1:m")
print(df_validado)
```

**Salida real:**

```text
   club_id  nombre_club      jugador
0       10  Real Madrid  Vinicius Jr
1       10  Real Madrid   Bellingham
```

## 8. Errores frecuentes y casos borde

1. Explosión cartesiana inesperada: Ocurre al hacer merge sobre columnas que tienen duplicados en ambas tablas sin declararlo. **Solución:** Usar `validate='1:m'` o `validate='1:1'`.

## 9. Buenas prácticas y rendimiento

* Si las tablas ya están indexadas por la clave, usar `left_index=True` y `right_index=True` es más rápido.

## 10. Métodos relacionados

* [concat](concat.md) — Concatenación posicional por ejes.
* [set_index](../04_ordenamiento_indices/set_index.md) — Indexación previa.

## 11. Referencias oficiales

* **API Reference:** [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) (Pandas 2.2).
