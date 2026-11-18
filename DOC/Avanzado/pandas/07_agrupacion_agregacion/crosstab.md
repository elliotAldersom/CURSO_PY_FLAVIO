# `pandas.crosstab`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.crosstab(
    index,
    columns,
    values=None,
    rownames=None,
    colnames=None,
    aggfunc=None,
    margins=False,
    margins_name='All',
    dropna=True,
    normalize=False
) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es una **función de tabulación cruzada** que calcula tablas de contingencia y frecuencias conjuntas entre dos o más factores discretos.

## 3. ¿Para qué sirve?

Permite contrastar la frecuencia conjunta de dos variables categóricas (p. ej. nacionalidad de jugadores vs club de destino) y calcular probabilidades condicionales mediante `normalize`.

* **Equivalencia en SQL:** Tabla dinámica de conteos cruzados `COUNT(*)`.

## 4. ¿Cómo funciona?

1. Computa la matriz de contingencia bidimensional evaluando pares de factores y normalizando por filas (`'index'`), columnas (`'columns'`) o total general (`True`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `index` | Serie, lista | Obligatorio | Posicional | Valores para agrupar en las filas. |
| `columns` | Serie, lista | Obligatorio | Posicional | Valores para agrupar en las columnas. |
| `normalize` | `{'all', 'index', 'columns', True, False}` | Opcional | `False` | Normaliza a proporciones relativas. |
| `margins` | `bool` | Opcional | `False` | Añade subtotales marginales. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

nacionalidad = pd.Series(["Argentina", "Brasil", "Brasil", "Francia"])
posicion = pd.Series(["DEL", "DEL", "DEF", "DEL"])
print(pd.crosstab(nacionalidad, posicion))
```

**Salida real:**

```text
col_0      DEF  DEL
row_0              
Argentina    0    1
Brasil       1    1
Francia      0    1
```

---

### Nivel 2: Intermedio

Frecuencias normalizadas por fila (distribución porcentual por equipo):

```python
import pandas as pd

df = pd.DataFrame({
    "club": ["Madrid", "Madrid", "Barca", "Barca"],
    "resultado": ["Victoria", "Victoria", "Victoria", "Derrota"]
})

print((pd.crosstab(df["club"], df["resultado"], normalize="index") * 100).round(1))
```

**Salida real:**

```text
resultado  Derrota  Victoria
club                        
Barca         50.0      50.0
Madrid         0.0     100.0
```

---

### Nivel 3: Avanzado

Tabulación cruzada ponderada con función de agregación:

```python
import pandas as pd

df = pd.DataFrame({
    "liga": ["Espana", "Espana", "Inglaterra"],
    "rol": ["Titular", "Suplente", "Titular"],
    "salario": [15.0, 5.0, 20.0]
})

print(pd.crosstab(df["liga"], df["rol"], values=df["salario"], aggfunc="sum", fill_value=0))
```

**Salida real:**

```text
rol         Suplente  Titular
liga                         
Espana           5.0     15.0
Inglaterra       0.0     20.0
```

## 8. Errores frecuentes y casos borde

1. Pasar argumentos de longitud desigual en `index` y `columns`: Lanza `ValueError`.

## 9. Buenas prácticas y rendimiento

* Usar `normalize='index'` para analizar distribuciones de probabilidad condicional.

## 10. Métodos relacionados

* [pivot_table](pivot_table.md) — Tablas dinámicas generales.
* [value_counts](../02_inspeccion_exploracion/value_counts.md) — Conteo unidimensional.

## 11. Referencias oficiales

* **API Reference:** [pandas.crosstab](https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html) (Pandas 2.2).
