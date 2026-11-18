# Seaborn: pairplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.pairplot(data, *, hue=None, hue_order=None, palette=None, vars=None, x_vars=None, y_vars=None, kind='scatter', diag_kind='auto', markers=None, height=2.5, aspect=1, corner=False, dropna=False, plot_kws=None, diag_kws=None, grid_kws=None)
```

## 2. ¿Qué es?

`seaborn.pairplot` es una función a nivel de figura que construye una grilla de dispersión por pares para todas las variables numéricas de un dataset.

## 3. ¿Para qué sirve?

Provee una vista panorámica integral instantánea en la fase de análisis exploratorio (EDA), mostrando relaciones bivariadas en los triángulos fuera de la diagonal y distribuciones univariadas en la diagonal principal.

## 4. ¿Cómo funciona?

Instancia un objeto `PairGrid` particionado en $N \times N$ ejes (donde $N$ es el número de variables numéricas). En la diagonal mapea por defecto histogramas o KDEs (`diag_kind='auto'`), y en las celdas fuera de la diagonal mapea gráficos de dispersión (`kind='scatter'`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Obligatorio | N/A | Conjunto de datos en formato tabular. |
| `hue` | `str` | Opcional | `None` | Variable categórica para estratificar colores y leyendas. |
| `vars` | `list[str]` | Opcional | `None` | Lista de nombres de columnas numéricas a incluir. |
| `kind` | `'scatter'`, `'kde'`, `'hist'`, `'reg'` | Opcional | `'scatter'` | Tipo de gráfico en las celdas fuera de la diagonal. |
| `diag_kind` | `'auto'`, `'hist'`, `'kde'`, `None` | Opcional | `'auto'` | Tipo de gráfico univariado sobre la diagonal principal. |
| `corner` | `bool` | Opcional | `False` | Si es `True`, dibuja únicamente el triángulo inferior de la grilla evitando duplicidad. |
| `height` | `float` | Opcional | `2.5` | Altura en pulgadas de cada faceta individual. |

## 6. Retorno

`seaborn.axisgrid.PairGrid`. Contenedor a nivel de figura que orquesta la cuadrícula completa.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "edad": [25, 30, 40],
    "salario": [3000, 4500, 6000]
})

g = sns.pairplot(df)
print(f"Tipo retornado: {type(g).__name__}")
print(f"Dimensiones de la grilla: {g.axes.shape}")
plt.close(g.figure)
```

**Salida real:**

```text
Tipo retornado: PairGrid
Dimensiones de la grilla: (2, 2)
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "x1": [1, 2, 5, 6],
    "x2": [10, 12, 20, 22],
    "clase": ["A", "A", "B", "B"]
})

g = sns.pairplot(df, hue="clase", corner=True, diag_kind="kde")
print(f"Esquina inferior configurada (corner=True)")
plt.close(g.figure)
```

**Salida real:**

```text
Esquina inferior configurada (corner=True)
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "feature_a": [1.0, 2.0, 3.5, 4.0],
    "feature_b": [10.5, 9.2, 5.1, 4.0],
    "target": [0, 0, 1, 1]
})

# Subselección explícita de columnas críticas con variables x e y independientes
g = sns.pairplot(
    df,
    x_vars=["feature_a"],
    y_vars=["feature_b"],
    hue="target",
    height=3.5,
    palette="Dark2"
)

print(f"Ejes generados en grilla custom: {g.axes.shape}")
plt.close(g.figure)
```

**Salida real:**

```text
Ejes generados en grilla custom: (1, 1)
```

## 8. Errores frecuentes y casos borde

- **Pasar `ax` a `pairplot`:** `pairplot` es Figure-level y administra múltiples ejes; pasar `ax=ax` lanza un `TypeError: unexpected keyword argument 'ax'`.
- **Explosión computacional en datasets anchos:** Ejecutar `pairplot` sobre un DataFrame con 50 columnas numéricas intentará construir una cuadrícula de $50 \times 50 = 2500$ subplots, saturando la memoria y congelando el proceso. Usar siempre `vars=['col1', 'col2', 'col3']`.

## 9. Buenas prácticas y rendimiento

- Usar siempre `corner=True` para no renderizar información redundante en el triángulo superior y reducir a la mitad el tiempo de dibujo.
- Subseleccionar un máximo de 4 a 6 variables numéricas clave mediante el parámetro `vars`.

## 10. Métodos relacionados

- [heatmap](heatmap.md)
- [scatterplot](../03_relacionales/scatterplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.pairplot.html
