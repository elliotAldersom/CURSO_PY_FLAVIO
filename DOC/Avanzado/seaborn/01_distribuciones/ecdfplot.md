# Seaborn: ecdfplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.ecdfplot(data=None, *, x=None, y=None, hue=None, weights=None, stat='proportion', complementary=False, palette=None, hue_order=None, hue_norm=None, log_scale=None, legend=True, ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.ecdfplot` calcula y dibuja la función de distribución acumulada empírica (Empirical Cumulative Distribution Function).

## 3. ¿Para qué sirve?

Es la herramienta estadística superior para evaluar distribuciones completas sin pérdida de información, ya que grafica cada observación individual sin depender del tamaño de bins (como `histplot`) ni de parámetros de suavizado (como `kdeplot`).

## 4. ¿Cómo funciona?

Ordena los datos de menor a mayor y genera una función escalonada monótona creciente donde la altura en el punto $x$ corresponde exactamente al porcentaje o conteo de muestras menores o iguales a $x$.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Dataset tabular de entrada. |
| `x`, `y` | `str` o `ArrayLike` | Opcional | `None` | Variable a evaluar de forma acumulativa. |
| `hue` | `str` o `ArrayLike` | Opcional | `None` | Agrupación semántica categórica por color. |
| `stat` | `'proportion'`, `'count'`, `'percent'` | Opcional | `'proportion'` | Métrica del eje vertical (de 0 a 1 en proportion, de 0 a 100 en percent). |
| `complementary` | `bool` | Opcional | `False` | Si es `True`, grafica $1 - F(x)$ (Survival Function / CCDF). |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje de Matplotlib destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con la curva escalonada ECDF trazada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"tiempos_seg": [2.1, 2.5, 3.0, 3.2, 4.0, 4.5, 5.1, 6.0]})
fig, ax = plt.subplots()
ret = sns.ecdfplot(data=df, x="tiempos_seg", ax=ax)

print(f"Tipo retornado: {type(ret).__name__}")
print(f"Límites Y (de 0 a 1): {ax.get_ylim()}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Límites Y (de 0 a 1): (0.0, 1.0)
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "latencia": [10, 12, 15, 20, 25, 40, 50, 80],
    "version": ["v1", "v1", "v1", "v1", "v2", "v2", "v2", "v2"]
})

fig, ax = plt.subplots()
sns.ecdfplot(data=df, x="latencia", hue="version", ax=ax)
print(f"Líneas de distribución escalonada: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Líneas de distribución escalonada: 2
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "tiempo_vida_horas": [120, 250, 400, 600, 850, 1200]
})

fig, ax = plt.subplots()
# Curva de supervivencia complementaria (CCDF: P(X > x))
sns.ecdfplot(data=df, x="tiempo_vida_horas", complementary=True, color="purple", ax=ax)
ax.set_title("Curva de Supervivencia Complementaria (CCDF)")

print(f"CCDF trazada correctamente")
plt.close(fig)
```

**Salida real:**

```text
CCDF trazada correctamente
```

## 8. Errores frecuentes y casos borde

- **Interpretar como densidad:** ECDF no representa una campana de densidad sino una probabilidad acumulada de 0 a 1. La mediana se lee directamente en $Y = 0.5$.
- **Intentar usar en variables categóricas nominales:** Solo tiene sentido matemático riguroso sobre datos cuantitativos continuos u ordinales.

## 9. Buenas prácticas y rendimiento

- Preferir siempre `ecdfplot` sobre histogramas cuando se requiere comparar percentiles exactos (ej. SLAs p90, p95, p99 en ingeniería de software).
- Usar `complementary=True` para análisis de confiabilidad de sistemas y tiempo de fallo.

## 10. Métodos relacionados

- [histplot](histplot.md)
- [kdeplot](kdeplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.ecdfplot.html
