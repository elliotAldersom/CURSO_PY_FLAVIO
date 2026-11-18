# Seaborn: heatmap

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.heatmap(data, *, vmin=None, vmax=None, cmap=None, center=None, robust=False, annot=None, fmt='.2g', annot_kws=None, linewidths=0, linecolor='white', cbar=True, cbar_kws=None, cbar_ax=None, square=False, xticklabels='auto', yticklabels='auto', mask=None, ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.heatmap` visualiza datos bidimensionales en formato matricial codificando los valores numéricos mediante una gradiente continua de colores.

## 3. ¿Para qué sirve?

Fundamental para el análisis de matrices de correlación de Pearson, matrices de confusión en Machine Learning y tablas de contingencia multidimensionales.

## 4. ¿Cómo funciona?

Mapea cada celda $(i, j)$ a un rectángulo coloreado según la escala del mapa de color (`cmap`), interpolando entre los límites `vmin` y `vmax`. Puede superponer anotaciones numéricas formateadas (`annot=True`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` o `ArrayLike` 2D | Obligatorio | N/A | Matriz rectangular de valores numéricos continuos. |
| `vmin`, `vmax` | `float` | Opcional | `None` | Anclajes numéricos mínimo y máximo para la escala de color. |
| `cmap` | `str` o `Colormap` | Opcional | `None` | Esquema cromático (ej. `'coolwarm'`, `'viridis'`, `'Blues'`). |
| `center` | `float` | Opcional | `None` | Valor numérico central al usar paletas divergentes (ej. `0` en correlaciones). |
| `annot` | `bool` o `ArrayLike` | Opcional | `None` | Si es `True`, escribe el valor numérico dentro de cada celda. |
| `fmt` | `str` | Opcional | `'.2g'` | Cadena de formato de cadena de texto (ej. `'.2f'`, `'d'`). |
| `mask` | `DataFrame` o `ArrayLike` booleano | Opcional | `None` | Máscara booleana: las celdas donde sea `True` no se dibujarán. |
| `square` | `bool` | Opcional | `False` | Si es `True`, fuerza que cada celda sea un cuadrado geométrico perfecto. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con el mapa de calor y su colorbar asociada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame([[1.0, 0.5], [0.5, 1.0]], columns=["A", "B"], index=["A", "B"])
fig, ax = plt.subplots()
ret = sns.heatmap(df, annot=True, ax=ax)

print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total textos anotados: {len(ax.texts)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total textos anotados: 4
```

### Nivel 2: Intermedio

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.DataFrame({
    "X1": [1, 2, 3, 4],
    "X2": [2, 4, 5, 8],
    "X3": [9, 7, 5, 2]
})

corr = data.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots()
# Mapa triangular con paleta divergente centrada en cero
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1, square=True, ax=ax)
print(f"Máscara aplicada sobre matriz: {mask.shape}")
plt.close(fig)
```

**Salida real:**

```text
Máscara aplicada sobre matriz: (3, 3)
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Matriz de confusión en clasificación
cm = pd.DataFrame(
    [[45, 5], [2, 48]],
    index=["Real_Positivo", "Real_Negativo"],
    columns=["Pred_Positivo", "Pred_Negativo"]
)

fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, linewidths=1.5, ax=ax)
ax.set_title("Matriz de Confusión del Modelo")

print(f"Verdaderos Positivos: {cm.iloc[0, 0]}")
plt.close(fig)
```

**Salida real:**

```text
Verdaderos Positivos: 45
```

## 8. Errores frecuentes y casos borde

- **Olvidar fijar `vmin=-1` y `vmax=1` en correlaciones:** Si la correlación más baja es 0.3, el mapa asignará el color mínimo a 0.3 distorsionando la percepción de neutralidad. Fijar siempre `vmin=-1, vmax=1, center=0`.
- **Error de formato con enteros (`ValueError`):** Pasar `fmt='.2f'` sobre números enteros no lanza error pero muestra decimales irrelevantes; usar `fmt='d'` para recuentos o enteros.

## 9. Buenas prácticas y rendimiento

- Usar `linewidths=0.5` con `linecolor='white'` para separar limpiamente las celdas contiguas.
- En matrices grandes (> 20 variables), deshabilitar `annot=False` para evitar saturación visual incomprensible.

## 10. Métodos relacionados

- [pairplot](pairplot.md)
- [scatterplot](../03_relacionales/scatterplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.heatmap.html
