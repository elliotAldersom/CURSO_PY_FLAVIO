# `DataFrame.pivot_table`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.pivot_table(
    values=None,
    index=None,
    columns=None,
    aggfunc='mean',
    fill_value=None,
    margins=False,
    dropna=True,
    margins_name='All',
    observed=_NoDefault.no_default,
    sort=True
)
```

## 2. ¿Qué es?

Es un **método de agregación multidimensional** que resume y remodela datos en una tabla de doble entrada cruzando variables en filas e índices de columnas.

## 3. ¿Para qué sirve?

Crea matrices de análisis de negocio (tablas dinámicas de Excel) donde se cruzan dos variables discretas calculando métricas agregadas en cada celda de intersección.

* **Equivalencia en SQL:** Consultas agregadas con operadores `PIVOT` o `FILTER(WHERE ...)`.

## 4. ¿Cómo funciona?

1. **Doble agrupación:** Realiza un `groupby([index, columns])` y desapila (*unstack*) la segunda dimensión a las columnas, agregando subtotales marginales con `margins=True`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `values` | columna numérica | Opcional | `None` | Variable sobre la cual computar la métrica. |
| `index` | columna | Obligatorio | Posicional | Variable para las filas de la tabla dinámica. |
| `columns` | columna | Obligatorio | Posicional | Variable para las columnas cruzadas. |
| `aggfunc` | función, string | Opcional | `'mean'` | Función de agregación (`'sum'`, `'mean'`, etc.). |
| `margins` | `bool` | Opcional | `False` | Añade fila y columna de totales generales (`'All'`). |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "equipo": ["Real Madrid", "Real Madrid", "Barcelona", "Barcelona"],
    "posicion": ["DEL", "MED", "DEL", "MED"],
    "goles": [21, 6, 26, 4]
})

print(df.pivot_table(index="equipo", columns="posicion", values="goles", aggfunc="sum"))
```

**Salida real:**

```text
posicion     DEL  MED
equipo               
Barcelona     26    4
Real Madrid   21    6
```

---

### Nivel 2: Intermedio

Inclusión de totales generales y relleno de celdas vacías:

```python
import pandas as pd

df = pd.DataFrame({
    "club": ["Real Madrid", "Real Madrid", "Arsenal"],
    "posicion": ["DEL", "DEF", "DEL"],
    "minutos": [2100, 2400, 1950]
})

tabla = df.pivot_table(
    index="club",
    columns="posicion",
    values="minutos",
    aggfunc="mean",
    fill_value=0,
    margins=True
)
print(tabla)
```

**Salida real:**

```text
posicion        DEF     DEL          All
club                                    
Arsenal           0  1950.0  1950.000000
Real Madrid    2400  2100.0  2250.000000
All            2400  2025.0  2150.000000
```

---

### Nivel 3: Avanzado

Múltiples métricas y variables cruzadas para reportes analíticos:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "temporada": ["2023", "2023", "2024", "2024"],
    "club": ["Madrid", "Barca", "Madrid", "Barca"],
    "goles": [85, 70, 95, 80],
    "asistencias": [50, 45, 60, 52]
})

resumen = df_liga.pivot_table(
    index="temporada",
    columns="club",
    values=["goles", "asistencias"],
    aggfunc={"goles": "sum", "asistencias": "mean"}
)
print(resumen)
```

**Salida real:**

```text
            asistencias       goles      
club              Barca Madrid Barca Madrid
temporada                                  
2023               45.0   50.0    70     85
2024               52.0   60.0    80     95
```

## 8. Errores frecuentes y casos borde

1. Confundir `pivot()` con `pivot_table()`: `pivot()` lanza error si existen combinaciones duplicadas; `pivot_table()` las agrega.

## 9. Buenas prácticas y rendimiento

* Pasar `fill_value=0` para evitar celdas con `NaN` en combinaciones sin observaciones.

## 10. Métodos relacionados

* [crosstab](crosstab.md) — Tabla de frecuencias cruzadas.
* [groupby](groupby.md) — Agrupación clásica.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.pivot_table](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html) (Pandas 2.2).
