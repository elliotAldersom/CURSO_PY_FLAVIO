# `DataFrame.groupby`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.groupby(
    by=None,
    axis=_NoDefault.no_default,
    level=None,
    as_index=True,
    sort=True,
    group_keys=True,
    observed=_NoDefault.no_default,
    dropna=True
) -> pandas.api.typing.DataFrameGroupBy
```

## 2. ¿Qué es?

Es un **método de particionamiento y agregación** que implementa el paradigma *Split-Apply-Combine* (Dividir, Aplicar y Combinar) para segmentar datos según claves categóricas y computar resúmenes por grupo.

## 3. ¿Para qué sirve?

Permite calcular métricas por segmento (p. ej. goles totales por equipo, promedio de minutos por posición) de forma vectorizada.

* **Equivalencia en SQL:** Equivale directamente a la cláusula `GROUP BY columna`.

## 4. ¿Cómo funciona?

1. **Split (Dividir):** Clasifica los índices de fila en grupos discretos utilizando una tabla hash en C.
2. **Apply (Aplicar):** Aplica la agregación (`sum`, `mean`, `agg`) a cada grupo de forma aislada.
3. **Combine (Combinar):** Ensambla los resultados parciales en un nuevo DataFrame. Si `as_index=True`, las claves de agrupación se convierten en el índice de filas.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `by` | columna, lista de columnas, callable | Obligatorio | Posicional | Clave o columnas por las cuales agrupar. |
| `as_index` | `bool` | Opcional | `True` | Si es `False`, mantiene las columnas agrupadoras como columnas ordinarias. |
| `sort` | `bool` | Opcional | `True` | Ordena las claves de grupo (desactivar con `sort=False` mejora la velocidad). |
| `dropna` | `bool` | Opcional | `True` | Si es `False`, incluye los `NaN` como un grupo válido. |

## 6. Retorno

* `DataFrameGroupBy` (objeto intermedio perezoso que espera una función de agregación).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona", "Barcelona"],
    "goles": [25, 21, 26, 18]
})

print(df.groupby("equipo")["goles"].sum())
```

**Salida real:**

```text
equipo
Barcelona      44
Real Madrid    46
Name: goles, dtype: int64
```

---

### Nivel 2: Intermedio

Agrupación manteniendo columnas planas con `as_index=False`:

```python
import pandas as pd

df = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona"],
    "jugador": ["Vinicius Jr", "Mbappé", "Lewandowski"],
    "goles": [21, 28, 26]
})

df_resumen = df.groupby("equipo", as_index=False)["goles"].mean()
print(df_resumen)
```

**Salida real:**

```text
        equipo  goles
0    Barcelona   26.0
1  Real Madrid   24.5
```

---

### Nivel 3: Avanzado

Agrupación multidimensional con `observed=True` para tipos categóricos:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "pais": pd.Categorical(["Espana", "Espana", "Inglaterra"], categories=["Espana", "Inglaterra", "Italia"]),
    "equipo": ["Real Madrid", "Barcelona", "Man City"],
    "puntos": [95, 85, 91]
})

# observed=True evita calcular grupos vacíos (como Italia)
resumen = df_liga.groupby(["pais", "equipo"], observed=True)["puntos"].sum()
print(resumen)
```

**Salida real:**

```text
pais        equipo     
Espana      Barcelona      85
            Real Madrid    95
Inglaterra  Man City       91
Name: puntos, dtype: int64
```

## 8. Errores frecuentes y casos borde

1. Intentar visualizar directamente `df.groupby('col')`: Muestra `<DataFrameGroupBy object>`, ya que es una evaluación perezosa que requiere un método terminal (`.sum()`, `.mean()`, `.agg()`).

## 9. Buenas prácticas y rendimiento

* Pasar `sort=False` si no se requiere orden alfabético de grupos para acelerar la computación hasta un 30%.

## 10. Métodos relacionados

* [agg](agg.md) — Agregaciones complejas sobre grupos.
* [pivot_table](pivot_table.md) — Tablas dinámicas bidimensionales.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) (Pandas 2.2).
