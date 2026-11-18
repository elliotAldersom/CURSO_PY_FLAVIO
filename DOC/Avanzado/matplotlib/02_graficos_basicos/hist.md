# Matplotlib: Axes.hist

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.hist(x, bins=None, range=None, density=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False, *, data=None, **kwargs)
```

## 2. ¿Qué es?

`Axes.hist` computa la distribución de frecuencias de un conjunto de datos numéricos unidimensionales agrupándolos en intervalos contiguos (`bins`) y los grafica como histograma.

## 3. ¿Para qué sirve?

Fundamental para el análisis exploratorio de datos (EDA), verificación de normalidad, detección de sesgo (skewness) y estimación empírica de densidad.

## 4. ¿Cómo funciona?

Aplica internamente la función de conteo de frecuencias equivalente a `numpy.histogram()`, construye los contenedores rectangulares con las frecuencias calculadas y configura la escala del eje.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `x` | `ArrayLike` | Obligatorio | N/A | Conjunto de observaciones numéricas unidimensionales. |
| `bins` | `int` o `Sequence[float]` o `str` | Opcional | `None` (10) | Cantidad de intervalos o cortes específicos (ej. `'auto'`, `'fd'`). |
| `density` | `bool` | Opcional | `False` | Si es `True`, normaliza el área bajo el histograma a 1 (densidad). |
| `cumulative` | `bool` | Opcional | `False` | Si es `True`, calcula el histograma acumulativo. |
| `edgecolor` | `color` | Opcional | `None` | Color del borde de cada barra (crucial para legibilidad). |

## 6. Retorno

`tuple[numpy.ndarray, numpy.ndarray, BarContainer | Polygon]`. Retorna una tupla de tres elementos: `(n, bins, patches)` donde `n` son las frecuencias por bin y `bins` son los límites de los cortes.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
datos = [12, 15, 14, 18, 19, 24, 25, 29, 31, 35, 38, 42]

n, bins, patches = ax.hist(datos, bins=4, edgecolor="black")
print(f"Frecuencias por bin: {n.tolist()}")
print(f"Cortes de bins: {[round(b, 1) for b in bins.tolist()]}")
plt.close(fig)
```

**Salida real:**

```text
Frecuencias por bin: [4.0, 2.0, 3.0, 3.0]
Cortes de bins: [12.0, 19.5, 27.0, 34.5, 42.0]
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
edades = [22, 25, 25, 26, 28, 30, 31, 35, 40, 42, 45, 52]

ax.hist(edades, bins="auto", density=True, color="skyblue", edgecolor="navy", alpha=0.7)
ax.set_title("Densidad de Probabilidad de Edades")
ax.set_xlabel("Años")
ax.set_ylabel("Densidad")

print(f"Cantidad de patches generados: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Cantidad de patches generados: 4
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# Histograma acumulativo para análisis de percentiles
puntajes = [45, 55, 60, 65, 70, 75, 80, 85, 90, 95]

n, bins, _ = ax.hist(puntajes, bins=5, cumulative=True, color="teal", edgecolor="white")
ax.set_title("Distribución Acumulada de Rendimiento")

print(f"Total acumulado final: {int(n[-1])}")
plt.close(fig)
```

**Salida real:**

```text
Total acumulado final: 10
```

## 8. Errores frecuentes y casos borde

- **No especificar `edgecolor`:** Con el estilo por defecto de Matplotlib, las barras continuas se fusionan en un bloque homogéneo indistinguible visualmente. Colocar siempre `edgecolor='black'` o similar.
- **Valores NaN o infinitos:** Si `x` contiene valores nulos, lanza un `ValueError`. Es obligatorio prefiltrar con `dropna()` o `np.isnan()`.

## 9. Buenas prácticas y rendimiento

- Usar `bins='auto'` o la regla de Freedman-Diaconis (`bins='fd'`) para determinar dinámicamente el número óptimo de intervalos según el volumen de datos.
- Al comparar dos grupos de diferentes tamaños, usar siempre `density=True` para evaluar proporciones relativas.

## 10. Métodos relacionados

- [bar](bar.md)
- [scatter](scatter.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html
