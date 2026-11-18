# Matplotlib: Axes.plot

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
```

## 2. ¿Qué es?

`Axes.plot` es el método de dibujo fundamental para trazar líneas continuas, curvas discretas y marcadores puntuales sobre un sistema de coordenadas 2D.

## 3. ¿Para qué sirve?

Permite visualizar relaciones funcionales $y = f(x)$, series temporales y tendencias continuas a lo largo de un eje ordinal o continuo.

## 4. ¿Cómo funciona?

Recibe secuencias de coordenadas X e Y, construye objetos `matplotlib.lines.Line2D` y los agrega a la colección de artistas del eje, ajustando automáticamente los límites matemáticos del lienzo (`autoscale`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `x, y` | `ArrayLike` | Obligatorio | N/A | Coordenadas horizontales y verticales de los puntos. |
| `fmt` | `str` | Opcional | `''` | Cadena compacta de formato (ej. `'r--o'` para rojo, guiones y círculos). |
| `color` | `color` | Opcional | `None` | Color de la línea (hexadecimal, nombre CSS o tupla RGBA). |
| `linestyle` | `str` | Opcional | `'-'` | Estilo de trazo (`'-'`, `'--'`, `':'`, `'-.'`). |
| `linewidth` | `float` | Opcional | `1.5` | Grosor de la línea en puntos tipográficos. |
| `marker` | `str` | Opcional | `None` | Tipo de marcador para cada punto (`'o'`, `'s'`, `'^'`). |
| `label` | `str` | Opcional | `None` | Etiqueta de la serie para la leyenda. |

## 6. Retorno

`list[Line2D]`. Lista de las líneas añadidas al lienzo.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
lineas = ax.plot([1, 2, 3, 4], [10, 25, 20, 35], color="blue", linewidth=2)
print(f"Cantidad de líneas creadas: {len(lineas)}")
print(f"Color asignado: {lineas[0].get_color()}")
plt.close(fig)
```

**Salida real:**

```text
Cantidad de líneas creadas: 1
Color asignado: blue
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = [0, 1, 2, 3, 4]
y1 = [0, 1, 4, 9, 16]
y2 = [0, 1, 8, 27, 64]

ax.plot(x, y1, 'b-o', label="Cuadrática")
ax.plot(x, y2, 'r--s', label="Cúbica")
ax.legend()
print(f"Límites del eje Y: {ax.get_ylim()}")
plt.close(fig)
```

**Salida real:**

```text
Límites del eje Y: (-3.2, 67.2)
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 3))
dias = [1, 2, 3, 4, 5, 6, 7]
precios = [102.5, 104.0, 101.8, 106.2, 105.7, 108.9, 110.1]

ax.plot(dias, precios, color="#2ca02c", marker="D", markersize=6, alpha=0.9, label="Activo Financiero")
ax.set_title("Cotización Diaria")
ax.set_ylabel("USD")
ax.grid(True, linestyle="--", alpha=0.5)

print(f"Puntos trazados: {len(ax.lines[0].get_xdata())}")
plt.close(fig)
```

**Salida real:**

```text
Puntos trazados: 7
```

## 8. Errores frecuentes y casos borde

- **Diferencia de longitudes entre X e Y:** Si `len(x) != len(y)`, lanza un `ValueError: x and y must have same first dimension`.
- **Datos no numéricos:** Pasar listas de strings sin orden explícito genera ejes categóricos no deseados.

## 9. Buenas prácticas y rendimiento

- Para series con miles de puntos, usar formatos vectorizados como NumPy arrays en lugar de listas de Python puras.
- Especificar siempre `label` en `ax.plot()` si se va a invocar `ax.legend()`.

## 10. Métodos relacionados

- [scatter](scatter.md)
- [legend](../03_personalizacion_estilos/legend.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
