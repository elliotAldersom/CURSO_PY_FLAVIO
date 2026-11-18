# Matplotlib: Axes.bar

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)
```

## 2. ¿Qué es?

`Axes.bar` dibuja gráficos de barras verticales donde la altura de cada barra representa una magnitud cuantitativa respecto a una categoría o valor discreto.

## 3. ¿Para qué sirve?

Utilizado en comparativas discretas entre grupos, conteos de frecuencias, balances contables y rankings.

## 4. ¿Cómo funciona?

Genera una colección de rectángulos `matplotlib.patches.Rectangle` colocados sobre el eje X en las posiciones dadas y con alturas especificadas por `height`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `x` | `float` o `ArrayLike` | Obligatorio | N/A | Posiciones horizontales de las barras o nombres de categorías. |
| `height` | `float` o `ArrayLike` | Obligatorio | N/A | Altura de las barras. |
| `width` | `float` o `ArrayLike` | Opcional | `0.8` | Ancho de las barras. |
| `bottom` | `float` o `ArrayLike` | Opcional | `0` | Base Y desde la que parte la barra (útil para barras apiladas). |
| `align` | `'center'`, `'edge'` | Opcional | `'center'` | Alineación de las barras respecto a las marcas X. |
| `color` | `color` o `ArrayLike` | Opcional | `None` | Color de relleno de las barras. |

## 6. Retorno

`matplotlib.container.BarContainer`. Contenedor que agrupa todos los rectángulos de las barras generadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
categorias = ["Prod A", "Prod B", "Prod C"]
valores = [45, 80, 60]

barras = ax.bar(categorias, valores, color="steelblue")
print(f"Tipo retornado: {type(barras).__name__}")
print(f"Total barras: {len(barras)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: BarContainer
Total barras: 3
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
grupos = ["Q1", "Q2", "Q3", "Q4"]
ventas_directas = [50, 70, 90, 110]
ventas_online = [30, 45, 60, 85]

# Gráfico de barras apiladas (stacked)
ax.bar(grupos, ventas_directas, label="Directas", color="navy")
ax.bar(grupos, ventas_online, bottom=ventas_directas, label="Online", color="gold")
ax.legend()
ax.set_ylabel("Ingresos (k$)")

print(f"Altura barra Q4 apilada: {ventas_directas[3] + ventas_online[3]}")
plt.close(fig)
```

**Salida real:**

```text
Altura barra Q4 apilada: 195
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
meses = ["Ene", "Feb", "Mar"]
ingresos = [120, 150, 180]

barras = ax.bar(meses, ingresos, width=0.5, color="teal")
# Inyección directa de etiquetas sobre las barras
ax.bar_label(barras, padding=3, fmt="$%d")
ax.set_ylim(0, 220)

print(f"Texto primer bar label: {barras[0].get_height()}")
plt.close(fig)
```

**Salida real:**

```text
Texto primer bar label: 120
```

## 8. Errores frecuentes y casos borde

- **Solapamiento en barras agrupadas:** No desplazar manualmente la coordenada `x` al comparar múltiples series causa que las barras se superpongan entre sí. Se debe computar un offset proporcional al `width`.
- **Etiquetas categóricas muy largas:** Si las etiquetas se tocan, aplicar rotación con `ax.tick_params(axis='x', rotation=45)`.

## 9. Buenas prácticas y rendimiento

- Utilizar la función nativa `ax.bar_label(container)` introducida en Matplotlib 3.4+ para etiquetar valores sin calcular coordenadas manuales con bucles `ax.text`.
- Iniciar siempre el eje numérico en cero para no distorsionar las proporciones visuales.

## 10. Métodos relacionados

- [hist](hist.md)
- [scatter](scatter.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html
