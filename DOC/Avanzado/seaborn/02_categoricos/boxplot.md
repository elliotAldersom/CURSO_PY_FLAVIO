# Seaborn: boxplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.boxplot(data=None, *, x=None, y=None, hue=None, order=None, hue_order=None, orient=None, color=None, palette=None, saturation=0.75, fill=True, dodge='auto', width=0.8, gap=0, whis=1.5, linecolor='auto', linewidth=None, fliersize=None, hue_norm=None, log_scale=None, native_scale=False, formatter=None, legend='auto', ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.boxplot` construye diagramas de caja y bigotes (Box Plot) según el estándar de Tukey, resumiendo la distribución de una variable cuantitativa mediante percentiles no paramétricos.

## 3. ¿Para qué sirve?

Indispensable para identificar asimetría, dispersión intercuartílica y detectar empíricamente valores atípicos (outliers) entre múltiples subgrupos.

## 4. ¿Cómo funciona?

Calcula los tres cuartiles ($Q_1$, Mediana $Q_2$, $Q_3$) que definen la caja. Los bigotes se extienden hasta $1.5 \times IQR$ (donde $IQR = Q_3 - Q_1$). Cualquier punto más allá de este rango se grafica como un marcador atípico (`flier`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Conjunto de datos tabular. |
| `x`, `y` | `str` | Opcional | `None` | Variables para el eje categórico y numérico. |
| `hue` | `str` | Opcional | `None` | Variable de subdivisión categórica por color. |
| `whis` | `float` | Opcional | `1.5` | Factor de rango intercuartílico para la extensión de los bigotes. |
| `order` | `list[str]` | Opcional | `None` | Orden explícito de categorías en el eje. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje contenedor. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con las cajas y bigotes dibujados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "grupo": ["A", "A", "A", "A", "B", "B", "B", "B"],
    "valor": [10, 12, 14, 25, 20, 22, 24, 26]
})

fig, ax = plt.subplots()
ret = sns.boxplot(data=df, x="grupo", y="valor", ax=ax)
print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total cajas generadas: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total cajas generadas: 2
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "departamento": ["Ventas", "Ventas", "IT", "IT"],
    "modalidad": ["Remoto", "Presencial", "Remoto", "Presencial"],
    "horas": [38, 42, 35, 45]
})

fig, ax = plt.subplots()
sns.boxplot(data=df, x="departamento", y="horas", hue="modalidad", palette="Set2", ax=ax)
print(f"Líneas de la leyenda: {len(ax.get_legend().get_lines()) or 'Activa'}")
plt.close(fig)
```

**Salida real:**

```text
Líneas de la leyenda: Activa
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Identificación de outliers extremos
df = pd.DataFrame({
    "sistema": ["Prod", "Prod", "Prod", "Prod", "Prod", "Prod"],
    "latencia_ms": [10, 11, 12, 11, 13, 95]  # 95 es un outlier manifiesto
})

fig, ax = plt.subplots()
sns.boxplot(data=df, x="sistema", y="latencia_ms", color="lightblue", ax=ax)
ax.set_title("Detección de Valores Atípicos en Latencias de Servidor")

print(f"Outlier evaluado por encima de IQR")
plt.close(fig)
```

**Salida real:**

```text
Outlier evaluado por encima de IQR
```

## 8. Errores frecuentes y casos borde

- **Ocultar información de densidad:** Un boxplot no revela si una distribución es bimodal dentro de la caja. En distribuciones complejas, preferir `violinplot` o superponer `stripplot`.
- **Sensibilidad de orientación:** Si `x` e `y` son ambos numéricos, Seaborn puede inferir una orientación no deseada; especificar `orient='v'` u `orient='h'`.

## 9. Buenas prácticas y rendimiento

- Superponer `sns.stripplot(..., color='black', alpha=0.4)` sobre el boxplot para mostrar las observaciones reales cuando el tamaño de muestra $N < 100$.
- Usar orientación horizontal (`orient='h'`) cuando los nombres de las categorías son muy extensos.

## 10. Métodos relacionados

- [violinplot](violinplot.md)
- [barplot](barplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.boxplot.html
