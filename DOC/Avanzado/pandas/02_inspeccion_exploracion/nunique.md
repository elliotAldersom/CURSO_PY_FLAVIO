# `DataFrame.nunique`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.nunique(axis=0, dropna=True)
```

## 2. ¿Qué es?

Es un **método de agregación** que cuenta la cantidad de valores únicos distintos presentes en cada columna (o fila).

## 3. ¿Para qué sirve?

Detecta la cardinalidad de las columnas para evaluar si una variable es identificadora única (clave primaria), categórica de baja cardinalidad o constante redundante.

* **Equivalencia en SQL:** Equivale a `COUNT(DISTINCT columna)`.

## 4. ¿Cómo funciona?

1. **Tabla hash de valores:** Itera calculando el tamaño del conjunto hash de elementos observados en cada columna, descartando o incluyendo `NaN` según `dropna`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | `0` para contar por columnas; `1` para contar por filas. |
| `dropna` | `bool` | Opcional | `True` | Si es `False`, cuenta el valor `NaN` como un valor único adicional. |

## 6. Retorno

* **Tipo devuelto:** `pandas.Series` con los conteos únicos indexados por columna.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Vinicius Jr"],
    "equipo": ["Real Madrid", "Real Madrid", "Real Madrid"]
})

print(df.nunique())
```

**Salida real:**

```text
jugador    2
equipo     1
dtype: int64
```

---

### Nivel 2: Intermedio

Conteo con inclusión explícita de valores nulos:

```python
import pandas as pd

df = pd.DataFrame({"goles": [10, 10, None, None, 20]})
print("Sin dropna:", df["goles"].nunique(dropna=True))
print("Con dropna=False:", df["goles"].nunique(dropna=False))
```

**Salida real:**

```text
Sin dropna: 2
Con dropna=False: 3
```

---

### Nivel 3: Avanzado

Detección automática de columnas unarias constantes para eliminación previa a modelado:

```python
import pandas as pd

df_sensores = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Yamal"],
    "liga": ["Espana", "Espana", "Espana"],
    "minutos": [90, 85, 70]
})

cardinalidad = df_sensores.nunique()
cols_constantes = cardinalidad[cardinalidad == 1].index.tolist()
print("Columnas sin varianza a descartar:", cols_constantes)
df_reducido = df_sensores.drop(columns=cols_constantes)
print(df_reducido)
```

**Salida real:**

```text
Columnas sin varianza a descartar: ['liga']
  jugador  minutos
0   Pedri       90
1    Gavi       85
2   Yamal       70
```

## 8. Errores frecuentes y casos borde

1. Confundir `nunique()` (conteo total) con `unique()` (arreglo con los valores concretos).

## 9. Buenas prácticas y rendimiento

* Si `nunique()` sobre una columna string es menor al 5% de las filas totales, convertirla a `category` optimiza memoria y velocidad.

## 10. Métodos relacionados

* [value_counts](value_counts.md) — Frecuencia detallada de cada valor.
* [isna](isna.md) — Detección de valores nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.nunique](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nunique.html) (Pandas 2.2).
