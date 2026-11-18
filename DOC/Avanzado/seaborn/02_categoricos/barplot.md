# Seaborn: barplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.barplot(data=None, *, x=None, y=None, hue=None, order=None, hue_order=None, estimator='mean', errorbar=('ci', 95), n_boot=1000, seed=None, units=None, weights=None, orient=None, color=None, palette=None, saturation=0.75, width=0.8, dodge='auto', ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.barplot` calcula y traza una estimación central (por defecto la media aritmética) para cada categoría discreta, acompañada de una barra de error que cuantifica la incertidumbre estadística mediante remuestreo bootstrap.

## 3. ¿Para qué sirve?

A diferencia del `bar` elemental de Matplotlib que solo dibuja rectángulos de alturas dadas, `sns.barplot` realiza inferencia estadística agregada automática sobre los datos crudos.

## 4. ¿Cómo funciona?

Agrupa las observaciones de `y` según los niveles únicos de `x`, calcula el estimador (`estimator='mean'`), ejecuta un remuestreo bootstrap de $N=1000$ iteraciones para determinar el intervalo de confianza del 95%, y dibuja la barra junto a su segmento de dispersión.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Conjunto de datos en formato tabular. |
| `x`, `y` | `str` | Opcional | `None` | Variables categórica y numérica respectivamente. |
| `hue` | `str` | Opcional | `None` | Subagrupación categórica semántica. |
| `estimator` | `str` o `Callable` | Opcional | `'mean'` | Función estadística de agregación central (`'mean'`, `'median'`, `np.sum`). |
| `errorbar` | `str` o `tuple` o `None` | Opcional | `('ci', 95)` | Intervalo de incertidumbre (`('ci', 95)`, `'sd'`, `'se'`, `None`). |
| `order` | `list[str]` | Opcional | `None` | Orden explícito de las categorías en el eje. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con el gráfico de barras estadísticas generado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "region": ["Norte", "Norte", "Sur", "Sur", "Sur"],
    "ventas": [120, 150, 90, 110, 95]
})

fig, ax = plt.subplots()
ret = sns.barplot(data=df, x="region", y="ventas", ax=ax)
print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total barras calculadas: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total barras calculadas: 2
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "equipo": ["Frontend", "Frontend", "Backend", "Backend"],
    "nivel": ["Junior", "Senior", "Junior", "Senior"],
    "salario": [40, 75, 45, 85]
})

fig, ax = plt.subplots()
sns.barplot(data=df, x="equipo", y="salario", hue="nivel", palette="muted", errorbar=None, ax=ax)
print(f"Total barras agrupadas por hue: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Total barras agrupadas por hue: 4
```

### Nivel 3: Avanzado

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "canal": ["Email", "Email", "Redes", "Redes", "Directo", "Directo"],
    "ingresos": [1000, 1200, 500, 700, 1500, 1800]
})

fig, ax = plt.subplots()
# Estimador robusto mediana y desviación estándar en barra de error
sns.barplot(data=df, x="canal", y="ingresos", estimator=np.median, errorbar="sd", palette="viridis", ax=ax)
ax.set_title("Mediana de Ingresos por Canal (Barras de Error: SD)")

print(f"Categorías representadas: {len(ax.get_xticklabels())}")
plt.close(fig)
```

**Salida real:**

```text
Categorías representadas: 3
```

## 8. Errores frecuentes y casos borde

- **Asumir que la altura es una suma total:** Por defecto, `barplot` calcula la MEDIA, no la suma. Si se requiere la suma, pasar `estimator='sum'`.
- **Lentitud con datasets masivos:** El bootstrap para calcular el intervalo de confianza por defecto (`errorbar=('ci', 95)`) puede demorar segundos si el DataFrame tiene millones de filas. Usar `errorbar=None` o `errorbar='sd'` en esos casos.

## 9. Buenas prácticas y rendimiento

- Usar siempre `errorbar=None` en pipelines de procesamiento batch de alto rendimiento.
- Para conteos simples de registros donde no hay variable continua $Y$, usar `countplot` en lugar de `barplot`.

## 10. Métodos relacionados

- [countplot](countplot.md)
- [boxplot](boxplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.barplot.html
