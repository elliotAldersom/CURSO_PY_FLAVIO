# Matplotlib: pyplot.subplots

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)
```

## 2. ¿Qué es?

`pyplot.subplots` es la función factoría primordial de la interfaz orientada a objetos de Matplotlib que crea simultáneamente una instancia de `Figure` y una grilla de uno o múltiples lienzos `Axes`.

## 3. ¿Para qué sirve?

Provee un punto de entrada centralizado para diseñar interfaces gráficas multipanel, configurando de manera limpia el espacio de dibujo sin manipular manualmente geometrías de bajo nivel.

## 4. ¿Cómo funciona?

Instancia un objeto `Figure` y utiliza internamente `GridSpec` para particionar el espacio en `nrows * ncols`. Retorna los ejes empaquetados en un array de NumPy (si hay múltiples) o un único objeto `Axes` según el parámetro `squeeze`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `nrows` | `int` | Opcional | `1` | Cantidad de filas de subplots en la cuadrícula. |
| `ncols` | `int` | Opcional | `1` | Cantidad de columnas de subplots en la cuadrícula. |
| `sharex` | `bool` o `'all'`, `'row'`, `'col'` | Opcional | `False` | Comparte el eje X entre subplots. |
| `sharey` | `bool` o `'all'`, `'row'`, `'col'` | Opcional | `False` | Comparte el eje Y entre subplots. |
| `squeeze` | `bool` | Opcional | `True` | Si es `True`, simplifica dimensiones extras del array de retorno. |
| `figsize` | `tuple[float, float]` | Opcional | `None` | Dimensiones en pulgadas `(ancho, alto)`. |
| `dpi` | `float` | Opcional | `None` | Resolución en puntos por pulgada (dots per inch). |

## 6. Retorno

`tuple[Figure, Axes | numpy.ndarray]`. La figura global creada y el o los ejes asociados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([1, 2, 3], [10, 20, 30])
print(f"Tipo fig: {type(fig).__name__}")
print(f"Tipo ax: {type(ax).__name__}")
plt.close(fig)
```

**Salida real:**

```text
Tipo fig: Figure
Tipo ax: Axes
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True, sharey=True)
print(f"Forma de axes: {axes.shape}")

for i, ax in enumerate(axes.flat):
    ax.text(0.5, 0.5, f"Panel {i+1}", ha='center')
plt.close(fig)
```

**Salida real:**

```text
Forma de axes: (2, 2)
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

# Grilla con ratios de ancho desiguales para dashboard
fig, (ax_main, ax_sidebar) = plt.subplots(
    nrows=1, ncols=2,
    figsize=(9, 4),
    gridspec_kw={"width_ratios": [3, 1]}
)
ax_main.set_title("Serie Temporal Principal")
ax_sidebar.set_title("Distribución")

print(f"Ratios configurados: 3 a 1")
print(f"Cantidad de ejes: {len(fig.axes)}")
plt.close(fig)
```

**Salida real:**

```text
Ratios configurados: 3 a 1
Cantidad de ejes: 2
```

## 8. Errores frecuentes y casos borde

- **Indexación incorrecta de `axes` cuando `nrows=1` o `ncols=1`:** Con `squeeze=True`, un subplot 1x2 devuelve un array 1D (`axes[0]`, `axes[1]`), pero un subplot 2x2 devuelve array 2D (`axes[0, 1]`). Usar `axes.flat` para iterar con seguridad.
- **Fugas de memoria:** Crear figuras en bucle sin llamar a `plt.close(fig)` satura la memoria.

## 9. Buenas prácticas y rendimiento

- Usar siempre `plt.subplots()` en lugar de múltiples llamadas a `plt.figure()` y `plt.subplot()`.
- Utilizar `sharex=True` y `sharey=True` al comparar métricas con escalas equivalentes.

## 10. Métodos relacionados

- [figure](figure.md)
- [tight_layout](../04_exportacion_composicion/tight_layout.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
