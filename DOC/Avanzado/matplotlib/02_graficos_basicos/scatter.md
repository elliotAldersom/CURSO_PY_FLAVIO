# Matplotlib: Axes.scatter

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, *, edgecolors=None, plotnonfinite=False, data=None, **kwargs)
```

## 2. ¿Qué es?

`Axes.scatter` genera gráficos de dispersión 2D donde cada punto individual puede tener dimensiones (`s`), colores (`c`) y formas de marcador independientes.

## 3. ¿Para qué sirve?

Ideal para explorar correlaciones bivariadas, clusters no lineales y visualizar una tercera y cuarta dimensión numérica codificada en el tamaño y color del marcador.

## 4. ¿Cómo funciona?

A diferencia de `plot(marker='o')`, `scatter` crea un objeto `PathCollection` que gestiona de manera vectorial propiedades variables punto a punto mapeadas con un colormap (`cmap`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `x, y` | `ArrayLike` | Obligatorio | N/A | Posiciones de los puntos. |
| `s` | `float` o `ArrayLike` | Opcional | `None` | Tamaño de marcador en puntos al cuadrado ($pt^2$). |
| `c` | `color` o `ArrayLike` | Opcional | `None` | Valor numérico mapeado o color para cada punto. |
| `cmap` | `str` o `Colormap` | Opcional | `None` | Mapa de color a emplear si `c` es una secuencia numérica. |
| `alpha` | `float` | Opcional | `None` | Nivel de transparencia entre 0 (invisible) y 1 (opaco). |

## 6. Retorno

`matplotlib.collections.PathCollection`. Colección vectorial de los puntos graficados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
col = ax.scatter([1, 2, 3, 4], [10, 15, 12, 18], color="purple")
print(f"Tipo retornado: {type(col).__name__}")
print(f"Total puntos: {len(col.get_offsets())}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: PathCollection
Total puntos: 4
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = [10, 20, 30, 40]
y = [100, 250, 200, 400]
pesos = [40, 120, 80, 200]  # Dimensión tamaño

sc = ax.scatter(x, y, s=pesos, c=y, cmap="viridis", alpha=0.8)
ax.set_title("Dispersión con Codificación de Color y Tamaño")
print(f"Colormap activo: {sc.get_cmap().name}")
plt.close(fig)
```

**Salida real:**

```text
Colormap activo: viridis
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# Simulación de clusters con límites estrictos
x = [1.2, 1.5, 1.8, 5.1, 5.4, 5.8]
y = [2.0, 2.2, 1.9, 7.0, 7.5, 7.2]
clases = [0, 0, 0, 1, 1, 1]

scatter = ax.scatter(x, y, c=clases, cmap="coolwarm", edgecolors="black", linewidths=1.2)
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
print(f"Offsets shape: {scatter.get_offsets().shape}")
plt.close(fig)
```

**Salida real:**

```text
Offsets shape: (6, 2)
```

## 8. Errores frecuentes y casos borde

- **Rendimiento con millones de puntos:** `scatter` tiene mayor sobrecarga de memoria que `plot` porque calcula propiedades individuales para cada punto. Para $N > 100\,000$ puntos uniformes, preferir `ax.plot(x, y, 'o')` o `hexbin`.
- **Confusión en unidades de tamaño `s`:** El tamaño es área en puntos cuadrados ($pt^2$), no radio.

## 9. Buenas prácticas y rendimiento

- Usar `alpha` bajo (ej. 0.3 - 0.5) cuando existe superposición de datos (overplotting).
- Agregar siempre `fig.colorbar(sc, ax=ax)` cuando `c` mapea una variable cuantitativa continua.

## 10. Métodos relacionados

- [plot](plot.md)
- [bar](bar.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html
