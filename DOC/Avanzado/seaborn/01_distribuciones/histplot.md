# Seaborn: histplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.histplot(data=None, *, x=None, y=None, hue=None, weights=None, stat='count', bins='auto', binwidth=None, binrange=None, discrete=None, cumulative=False, common_bins=True, common_norm=True, multiple='layer', element='bars', fill=True, shrink=1, kde=False, kde_kws=None, line_kws=None, thresh=0, pthresh=None, pmax=None, cbar=False, cbar_ax=None, cbar_kws=None, palette=None, hue_order=None, hue_norm=None, color=None, log_scale=None, legend=True, ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.histplot` es la función a nivel de ejes estándar de Seaborn para calcular y trazar histogramas univariados o bivariados con soporte nativo de agrupación categórica y superposición de KDE.

## 3. ¿Para qué sirve?

Resuelve la exploración de la forma empírica de una distribución continua o discreta, permitiendo comparar subpoblaciones mediante barras apiladas, escalonadas o rellenas.

## 4. ¿Cómo funciona?

Integra internamente la segmentación de datos tabulares, calcula los bins óptimos y proyecta las alturas calculando frecuencias absolutas, densidades o probabilidades relativas según `stat`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Estructura de datos tabular. |
| `x`, `y` | `str` o `ArrayLike` | Opcional | `None` | Nombre de la variable continua a evaluar. |
| `hue` | `str` o `ArrayLike` | Opcional | `None` | Variable categórica de agrupación semántica por color. |
| `stat` | `'count'`, `'frequency'`, `'density'`, `'percent'`, `'probability'` | Opcional | `'count'` | Métrica de agregación estadística calculada para cada bin. |
| `kde` | `bool` | Opcional | `False` | Si es `True`, traza simultáneamente la curva continua de densidad Kernel. |
| `multiple` | `'layer'`, `'dodge'`, `'stack'`, `'fill'` | Opcional | `'layer'` | Comportamiento geométrico al comparar múltiples subgrupos. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje de Matplotlib sobre el cual dibujar. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con el histograma renderizado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"puntaje": [55, 62, 65, 70, 72, 75, 78, 82, 85, 90, 95]})
fig, ax = plt.subplots()
ret = sns.histplot(data=df, x="puntaje", bins=4, ax=ax)

print(f"Tipo de retorno: {type(ret).__name__}")
print(f"Cantidad de barras en el histograma: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo de retorno: Axes
Cantidad de barras en el histograma: 4
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "salario": [30, 35, 40, 50, 70, 80, 85, 90],
    "departamento": ["Ventas", "Ventas", "Ventas", "Ventas", "IT", "IT", "IT", "IT"]
})

fig, ax = plt.subplots()
sns.histplot(data=df, x="salario", hue="departamento", multiple="dodge", kde=True, ax=ax)
print(f"Total barras dibujadas (dodge): {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Total barras dibujadas (dodge): 8
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "latencia_ms": [15, 18, 22, 25, 30, 45, 80, 120, 250, 400]
})

fig, ax = plt.subplots()
# Histograma logarítmico para colas pesadas en métricas de software
sns.histplot(data=df, x="latencia_ms", log_scale=True, stat="percent", color="teal", ax=ax)
ax.set_title("Distribución Porcentual de Latencia (Escala Log)")

print(f"Escala X logarítmica: {ax.get_xscale()}")
plt.close(fig)
```

**Salida real:**

```text
Escala X logarítmica: log
```

## 8. Errores frecuentes y casos borde

- **Confundir con `sns.displot`:** `displot` es a nivel de figura y no acepta el parámetro `ax`.
- **`multiple='layer'` poco legible:** Con datos densos, capas transparentes superpuestas pueden ser difíciles de distinguir; preferir `multiple='dodge'` o `kdeplot`.

## 9. Buenas prácticas y rendimiento

- Usar `stat='percent'` o `stat='density'` siempre que los subgrupos a comparar tengan tamaños de muestra dispares.
- Incorporar `kde=True` para visualizar la tendencia subyacente sin perder la evidencia discreta de las muestras.

## 10. Métodos relacionados

- [kdeplot](kdeplot.md)
- [ecdfplot](ecdfplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.histplot.html
