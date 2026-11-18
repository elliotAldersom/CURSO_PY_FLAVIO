# Seaborn: scatterplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.scatterplot(data=None, *, x=None, y=None, hue=None, size=None, style=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, markers=True, style_order=None, legend='auto', ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.scatterplot` dibuja diagramas de dispersión bivariados permitiendo mapear variables adicionales a través de color (`hue`), tamaño (`size`) y forma de marcador (`style`).

## 3. ¿Para qué sirve?

Permite explorar interacciones multifactoriales entre hasta 5 dimensiones de datos en una única visualización 2D intuitiva y concisa.

## 4. ¿Cómo funciona?

Gestiona internamente la creación del `PathCollection` de Matplotlib, automatizando la normalización de tamaños con `sizes=(min, max)` y generando una leyenda compuesta unificada que decodifica color, escala y símbolo.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Estructura de datos tabular. |
| `x`, `y` | `str` o `ArrayLike` | Opcional | `None` | Coordenadas cuantitativas de posición. |
| `hue` | `str` | Opcional | `None` | Mapeo semántico de color. |
| `size` | `str` | Opcional | `None` | Mapeo semántico de tamaño de marcador. |
| `style` | `str` | Opcional | `None` | Mapeo semántico de forma del marcador (ej. círculo, cruz, triángulo). |
| `sizes` | `tuple[float, float]` | Opcional | `None` | Rango de tamaños mínimo y máximo para `size`. |
| `palette` | `str` o `list` | Opcional | `None` | Paleta de colores a aplicar. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje de Matplotlib destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con los puntos graficados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 15, 30]})
fig, ax = plt.subplots()
ret = sns.scatterplot(data=df, x="x", y="y", ax=ax)

print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total puntos graficados: {len(ret.collections[0].get_offsets())}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total puntos graficados: 4
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "edad": [25, 35, 45, 55],
    "ingresos": [30, 60, 80, 95],
    "genero": ["M", "F", "F", "M"],
    "inversion": [5, 20, 35, 50]
})

fig, ax = plt.subplots()
sns.scatterplot(data=df, x="edad", y="ingresos", hue="genero", size="inversion", sizes=(40, 200), ax=ax)
print(f"Leyenda compuesta generada: {ax.get_legend() is not None}")
plt.close(fig)
```

**Salida real:**

```text
Leyenda compuesta generada: True
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "sensor_1": [1.2, 2.3, 3.1, 4.5],
    "sensor_2": [5.1, 4.2, 7.3, 8.1],
    "estado": ["OK", "WARN", "OK", "FAIL"]
})

fig, ax = plt.subplots()
# Asignación de estilos de marcador por categoría
sns.scatterplot(data=df, x="sensor_1", y="sensor_2", hue="estado", style="estado", s=100, palette="Set1", ax=ax)
ax.set_title("Telemetría con Marcadores Semánticos")

print(f"Puntos renderizados: {len(df)}")
plt.close(fig)
```

**Salida real:**

```text
Puntos renderizados: 4
```

## 8. Errores frecuentes y casos borde

- **Sobrecarga cognitiva por demasiadas dimensiones:** Usar simultáneamente `hue`, `size` y `style` con variables de alta cardinalidad puede hacer la visualización indescifrable.
- **Solapamiento masivo de puntos:** En datasets grandes, utilizar `alpha=0.5` o considerar `kdeplot` bivariado.

## 9. Buenas prácticas y rendimiento

- Especificar siempre `sizes=(20, 200)` al usar el argumento `size` para asegurar que los puntos más pequeños sigan siendo visibles.
- Preferir paletas secuenciales cuando `hue` mapea una variable numérica continua.

## 10. Métodos relacionados

- [lineplot](lineplot.md)
- [histplot](../01_distribuciones/histplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.scatterplot.html
