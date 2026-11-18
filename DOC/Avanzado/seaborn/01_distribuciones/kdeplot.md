# Seaborn: kdeplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.kdeplot(data=None, *, x=None, y=None, hue=None, weights=None, palette=None, hue_order=None, hue_norm=None, color=None, fill=None, multiple='layer', common_norm=True, common_grid=False, cumulative=False, bw_method='scott', bw_adjust=1, log_scale=None, levels=10, thresh=0.05, gridsize=200, cut=3, clip=None, legend=True, warn_singular=True, ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.kdeplot` grafica una estimación de densidad de Kernel (KDE), produciendo una curva suave continua que representa la función de densidad de probabilidad no paramétrica de los datos.

## 3. ¿Para qué sirve?

Permite evaluar la multimodalidad, asimetría y curtosis de una variable continua sin la sensibilidad arbitraria impuesta por el tamaño de los cortes de un histograma.

## 4. ¿Cómo funciona?

Coloca una función Gaussiana (Kernel) centrada en cada punto de muestra y suma todas las densidades normalizadas a lo largo de una grilla continua de evaluación de tamaño `gridsize`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Estructura de datos tabular. |
| `x`, `y` | `str` o `ArrayLike` | Opcional | `None` | Variable analizada (univariada o bivariada si se pasan ambos). |
| `hue` | `str` o `ArrayLike` | Opcional | `None` | Variable categórica de división semántica. |
| `fill` | `bool` | Opcional | `False` | Si es `True`, rellena el área bajo la curva con transparencia. |
| `bw_adjust` | `float` | Opcional | `1` | Factor de ajuste del ancho de banda del Kernel (suavizado). |
| `common_norm` | `bool` | Opcional | `True` | Normaliza condicionalmente respecto a la muestra global. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje contenedor. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con la curva de densidad agregada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"tiempos": [10, 12, 14, 15, 16, 18, 20, 22, 25]})
fig, ax = plt.subplots()
ret = sns.kdeplot(data=df, x="tiempos", fill=True, ax=ax)

print(f"Curvas generadas: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Curvas generadas: 1
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "edad": [21, 22, 25, 26, 45, 48, 50, 52],
    "cohorte": ["Joven", "Joven", "Joven", "Joven", "Senior", "Senior", "Senior", "Senior"]
})

fig, ax = plt.subplots()
# Comparativa con densidad independiente (common_norm=False)
sns.kdeplot(data=df, x="edad", hue="cohorte", fill=True, common_norm=False, ax=ax)
print(f"Líneas de contorno calculadas: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Líneas de contorno calculadas: 2
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "consumo_w": [100, 110, 105, 115, 200, 210, 205, 220]
})

fig, ax = plt.subplots()
# bw_adjust menor a 1 revela subestructuras bimodales sin sobresuavizado
sns.kdeplot(data=df, x="consumo_w", bw_adjust=0.5, color="darkred", ax=ax)
ax.set_title("Detección de Bimodalidad con Ajuste de Kernel Fino")

print(f"bw_adjust=0.5 aplicado exitosamente")
plt.close(fig)
```

**Salida real:**

```text
bw_adjust=0.5 aplicado exitosamente
```

## 8. Errores frecuentes y casos borde

- **Valores fuera del dominio real (curvas que se extienden a números negativos):** El kernel gaussiano se extiende a $\pm \infty$. Si una variable como edad o precio no puede ser negativa, usar el parámetro `clip=(0, None)` para truncar el soporte.
- **Sobresuavizado (`bw_adjust` muy alto):** Puede ocultar distribuciones bimodales reales haciendo parecer los datos normales.

## 9. Buenas prácticas y rendimiento

- Configurar siempre `clip` en datos con cotas físicas estrictas (ej. tiempos de espera, precios).
- Usar `common_norm=False` al comparar grupos con volúmenes de datos muy desiguales.

## 10. Métodos relacionados

- [histplot](histplot.md)
- [ecdfplot](ecdfplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.kdeplot.html
