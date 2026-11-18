# Seaborn: lineplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.lineplot(data=None, *, x=None, y=None, hue=None, size=None, style=None, units=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, dashes=True, markers=None, style_order=None, estimator='mean', errorbar=('ci', 95), n_boot=1000, seed=None, sort=True, err_style='band', err_kws=None, legend='auto', ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.lineplot` traza líneas continuas representando relaciones funcionales o series de tiempo, agregando automáticamente múltiples observaciones repetidas para un mismo valor de $X$ mediante estimación de media y bandas de error.

## 3. ¿Para qué sirve?

Resuelve el trazado de tendencias experimentales repetidas donde existen múltiples réplicas o mediciones por unidad de tiempo, evitando el cálculo manual de medias y desviaciones estándar.

## 4. ¿Cómo funciona?

Ordena los datos por la coordenada X (`sort=True`), agrupa observaciones repetidas por `x` y calcula el estimador (`estimator='mean'`). Luego genera una banda semitransparente que representa el intervalo de confianza de bootstrap (`err_style='band'`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Estructura de datos tabular. |
| `x`, `y` | `str` o `ArrayLike` | Opcional | `None` | Coordenadas horizontal y vertical. |
| `hue` | `str` | Opcional | `None` | Agrupación semántica por series de color. |
| `style` | `str` | Opcional | `None` | Mapeo de estilos de línea (guiones, puntos). |
| `estimator` | `str` o `Callable` | Opcional | `'mean'` | Función de agregación para réplicas en cada punto X. |
| `errorbar` | `str` o `tuple` | Opcional | `('ci', 95)` | Intervalo de dispersión (`('ci', 95)`, `'sd'`, `None`). |
| `err_style` | `'band'`, `'bars'` | Opcional | `'band'` | Banda sombreada o barras verticales de error. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con las líneas y bandas estadísticas generadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"paso": [1, 2, 3, 4], "perdida": [0.9, 0.7, 0.4, 0.2]})
fig, ax = plt.subplots()
ret = sns.lineplot(data=df, x="paso", y="perdida", ax=ax)

print(f"Tipo retornado: {type(ret).__name__}")
print(f"Líneas trazadas: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Líneas trazadas: 1
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Múltiples mediciones experimentales en los mismos instantes de tiempo
df = pd.DataFrame({
    "tiempo": [1, 1, 1, 2, 2, 2, 3, 3, 3],
    "temperatura": [20, 22, 21, 25, 27, 26, 30, 34, 32]
})

fig, ax = plt.subplots()
# Agregación automática con banda sombreada de confianza
sns.lineplot(data=df, x="tiempo", y="temperatura", ax=ax)
print(f"Bandas sombreadas calculadas: {len(ax.collections)}")
plt.close(fig)
```

**Salida real:**

```text
Bandas sombreadas calculadas: 1
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "dia": [1, 2, 3, 1, 2, 3],
    "usuarios": [100, 150, 180, 80, 110, 140],
    "region": ["Latam", "Latam", "Latam", "Europa", "Europa", "Europa"]
})

fig, ax = plt.subplots()
sns.lineplot(data=df, x="dia", y="usuarios", hue="region", style="region", markers=True, dashes=False, ax=ax)
ax.set_title("Evolución Diaria por Región")

print(f"Series independientes: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Series independientes: 2
```

## 8. Errores frecuentes y casos borde

- **Líneas desordenadas en zig-zag:** Si `sort=False` y los datos temporales no están estrictamente cronológicos, las líneas se cruzarán de forma caótica. Mantener siempre `sort=True`.
- **Lentitud en series de alta frecuencia:** Si se tienen 500,000 puntos en series financieras sin réplicas, deshabilitar `errorbar=None` para evitar cálculos innecesarios de bootstrap.

## 9. Buenas prácticas y rendimiento

- Usar `errorbar='sd'` en lugar de bootstrap cuando interese representar la variabilidad de la población en vez de la incertidumbre de la media muestral.
- Activar `markers=True` para identificar inequívocamente los instantes reales de medición.

## 10. Métodos relacionados

- [scatterplot](scatterplot.md)
- [barplot](../02_categoricos/barplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.lineplot.html
