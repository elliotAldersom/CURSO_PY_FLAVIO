# `DataFrame.reset_index`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.reset_index(
    level=None,
    *,
    drop=False,
    inplace=False,
    col_level=0,
    col_fill='',
    allow_duplicates=_NoDefault.no_default,
    names=None
)
```

## 2. ¿Qué es?

Es un **método de reestructuración de índices** que restablece el índice de filas a la secuencia numérica entera predeterminada `RangeIndex(0, n)`.

## 3. ¿Para qué sirve?

Permite transformar índices significativos (o jerárquicos tras `groupby`) en columnas normales de datos, o descartar índices fragmentados tras filtrados mediante `drop=True`.

## 4. ¿Cómo funciona?

1. **Inserción de columna o descarte:** Si `drop=False`, inserta las etiquetas del índice actual como una nueva columna al inicio del DataFrame. Si `drop=True`, descarta el índice anterior liberando memoria.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `drop` | `bool` | Opcional | `False` | Si es `True`, no inserta el índice viejo como columna y lo elimina. |
| `inplace` | `bool` | Opcional | `False` | En desuso en Pandas 2.x+. |
| `names` | `str`, `list[str]` | Opcional | `None` | Nuevo nombre para la columna que contendrá el índice previo. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Reconstrucción de índice continuo tras filtrado:

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Messi", "Ronaldo", "Mbappé"], "goles": [25, 22, 28]})
df_filtrado = df[df["goles"] > 23].reset_index(drop=True)
print(df_filtrado)
```

**Salida real:**

```text
  jugador  goles
0   Messi     25
1  Mbappé     28
```

---

### Nivel 2: Intermedio

Conversión de índice a columna con renombrado explícito:

```python
import pandas as pd

df = pd.DataFrame({"goles": [31, 28]}, index=["Haaland", "Mbappé"])
df_plano = df.reset_index(names="nombre_jugador")
print(df_plano)
```

**Salida real:**

```text
  nombre_jugador  goles
0        Haaland     31
1         Mbappé     28
```

---

### Nivel 3: Avanzado

Aplanamiento de MultiIndex tras agregación con `groupby`:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona"],
    "goles": [21, 15, 26]
})

resumen = df_liga.groupby("equipo")["goles"].sum()
# Convierte la Serie agrupada con índice 'equipo' en un DataFrame plano
df_reporte = resumen.reset_index()
print(df_reporte)
```

**Salida real:**

```text
        equipo  goles
0    Barcelona     26
1  Real Madrid     36
```

## 8. Errores frecuentes y casos borde

1. Olvidar `drop=True` al querer solo reindexar: Crea columnas basura llamadas `'index'` o `'level_0'`.

## 9. Buenas prácticas y rendimiento

* Tras `sort_values` o filtros severos, encadenar `.reset_index(drop=True)` para mantener la consistencia posicional.

## 10. Métodos relacionados

* [set_index](set_index.md) — Asigna una columna existente como nuevo índice.
* [sort_values](sort_values.md) — Reorganiza filas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.reset_index](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html) (Pandas 2.2).
