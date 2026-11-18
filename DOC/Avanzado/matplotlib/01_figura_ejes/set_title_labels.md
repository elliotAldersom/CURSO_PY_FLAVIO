# Matplotlib: Axes.set_title, set_xlabel y set_ylabel

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.set_title(label, fontdict=None, loc='center', pad=None, *, y=None, **kwargs)
```

## 2. ¿Qué es?

Métodos del objeto `Axes` dedicados a asignar y dar formato a los títulos textuales del gráfico y a las etiquetas identificadoras de los ejes de coordenadas X e Y.

## 3. ¿Para qué sirve?

Proporcionan contexto semántico esencial para que los gráficos sean legibles, comprensibles y autónomos sin ambigüedades en auditorías y reportes.

## 4. ¿Cómo funciona?

Crean o modifican instancias internas de `matplotlib.text.Text` posicionadas relativamente en las coordenadas del lienzo de trazado y las integran al árbol de artistas.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `label` | `str` | Obligatorio | N/A | Texto a mostrar como título o etiqueta. |
| `fontdict` | `dict` | Opcional | `None` | Diccionario con propiedades de tipografía (size, weight, family). |
| `loc` | `'left'`, `'center'`, `'right'` | Opcional | `'center'` | Alineación horizontal del título. |
| `pad` | `float` | Opcional | `None` | Espaciado en puntos respecto al borde del eje. |

## 6. Retorno

`matplotlib.text.Text`. El objeto de texto generado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
t = ax.set_title("Ventas Trimestrales", loc="left", fontsize=12)
x_lbl = ax.set_xlabel("Trimestre Fiscal")
y_lbl = ax.set_ylabel("Monto en USD")

print(f"Texto del título: {t.get_text()}")
print(f"Texto eje X: {x_lbl.get_text()}")
plt.close(fig)
```

**Salida real:**

```text
Texto del título: Ventas Trimestrales
Texto eje X: Trimestre Fiscal
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_title("Consumo Energético", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Hora del Día (24h)", fontsize=10, color="gray")
ax.set_ylabel("Potencia (kW)", fontsize=10, color="gray")

print(f"Posición título: {ax.title.get_position()}")
plt.close(fig)
```

**Salida real:**

```text
Posición título: (0.5, 1.0)
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# Formateo con LaTeX integrado y múltiples fuentes
ax.set_title("Ajuste Gaussiano: f(x) = exp(-0.5 * ((x-mu)/sigma)**2)", fontsize=11)
ax.set_xlabel("Desviacion estandar (sigma)", fontsize=10)
ax.set_ylabel("Densidad de Probabilidad", fontsize=10)

print(f"Titulo contiene Gaussiano: {'Gaussiano' in ax.get_title()}")
plt.close(fig)
```

**Salida real:**

```text
Titulo contiene Gaussiano: True
```

## 8. Errores frecuentes y casos borde

- **Usar `plt.title()` en lugar de `ax.set_title()`:** En figuras con múltiples ejes, `plt.title()` afecta únicamente al último eje creado o activado, causando títulos en posiciones incorrectas.
- **Solapamiento:** Si el `pad` o tamaño de fuente es excesivo, el título puede superponerse con los ticks superiores.

## 9. Buenas prácticas y rendimiento

- Emplear `ax.set(title=..., xlabel=..., ylabel=...)` para definir todas las propiedades en una sola línea compacta.
- Mantener consistencia de unidades de medida (ej. [kg], [$], [s]) siempre explícitas en las etiquetas.

## 10. Métodos relacionados

- [subplots](subplots.md)
- [legend](../03_personalizacion_estilos/legend.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_title.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xlabel.html
