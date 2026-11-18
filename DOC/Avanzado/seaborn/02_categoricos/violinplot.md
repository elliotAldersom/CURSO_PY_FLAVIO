# Seaborn: violinplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.violinplot(data=None, *, x=None, y=None, hue=None, order=None, hue_order=None, bw_method='scott', bw_adjust=1, cut=2, density_norm='area', scale=None, scale_hue=None, gridsize=100, width=0.8, side='both', inner='box', split=False, dodge='auto', orient=None, linewidth=None, color=None, palette=None, saturation=0.75, fill=True, inner_kws=None, ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.violinplot` combina un diagrama de caja y bigotes tradicional con una estimación de densidad de Kernel (KDE) simétrica a ambos lados.

## 3. ¿Para qué sirve?

Permite comparar distribuciones entre grupos revelando aspectos críticos que el `boxplot` oculta, tales como bimodalidad, agrupaciones múltiples o asimetría interna extrema.

## 4. ¿Cómo funciona?

Calcula la curva KDE para cada subconjunto de datos y la dibuja de manera espejada. En el centro del violín, dibuja por defecto una representación en miniatura de la caja intercuartílica y la mediana (`inner='box'`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Conjunto de datos en formato tabular. |
| `x`, `y` | `str` | Opcional | `None` | Variables categórica y continua. |
| `hue` | `str` | Opcional | `None` | Variable categórica de partición semántica. |
| `split` | `bool` | Opcional | `False` | Si es `True` y `hue` tiene 2 niveles, dibuja cada mitad del violín para un nivel distinto. |
| `inner` | `'box'`, `'quartile'`, `'point'`, `'stick'`, `None` | Opcional | `'box'` | Representación visual interna del núcleo del violín. |
| `bw_adjust` | `float` | Opcional | `1` | Parámetro de suavizado del ancho de banda KDE. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con los violines estadísticos generados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "grupo": ["A", "A", "A", "B", "B", "B"],
    "score": [20, 25, 22, 50, 55, 52]
})

fig, ax = plt.subplots()
ret = sns.violinplot(data=df, x="grupo", y="score", ax=ax)
print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total colecciones de violines: {len(ax.collections)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total colecciones de violines: 2
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "departamento": ["Ventas", "Ventas", "Ventas", "Ventas", "IT", "IT", "IT", "IT"],
    "genero": ["F", "M", "F", "M", "F", "M", "F", "M"],
    "salario": [45, 48, 50, 52, 70, 75, 78, 80]
})

fig, ax = plt.subplots()
# Violines divididos simétricamente para comparar 2 niveles (split=True)
sns.violinplot(data=df, x="departamento", y="salario", hue="genero", split=True, palette="pastel", ax=ax)
print(f"Violines partidos con split=True exitosamente")
plt.close(fig)
```

**Salida real:**

```text
Violines partidos con split=True exitosamente
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "proceso": ["Alpha", "Alpha", "Alpha", "Alpha"],
    "calibracion": [10.1, 10.2, 10.1, 10.3]
})

fig, ax = plt.subplots()
# inner='quartile' dibuja líneas horizontales directas para Q1, Q2 y Q3
sns.violinplot(data=df, x="proceso", y="calibracion", inner="quartile", color="lightgreen", ax=ax)
ax.set_title("Control de Tolerancias con Cuartiles Explícitos")

print(f"Violinplot con cuartiles configurado")
plt.close(fig)
```

**Salida real:**

```text
Violinplot con cuartiles configurado
```

## 8. Errores frecuentes y casos borde

- **Uso con tamaños de muestra minúsculos ($N < 10$):** Con muy pocos puntos, el KDE extrapola probabilidades ficticias y da la ilusión de una distribución rica cuando en realidad solo hay 3 observaciones.
- **Extensión a rangos negativos:** Al igual que en `kdeplot`, si no se tiene precaución, los violines pueden extenderse más allá de cotas físicas.

## 9. Buenas prácticas y rendimiento

- Usar `split=True` al comparar distribuciones de dos clases binarias (ej. Tratamiento vs Control) para ahorrar espacio y maximizar la comparación directa.
- En muestras pequeñas ($N < 30$), preferir `boxplot` combinado con `stripplot`.

## 10. Métodos relacionados

- [boxplot](boxplot.md)
- [kdeplot](../01_distribuciones/kdeplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.violinplot.html
