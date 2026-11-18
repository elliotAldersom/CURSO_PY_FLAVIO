# Matplotlib: Axes.set_xlim y Axes.set_ylim

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.set_xlim(left=None, right=None, *, emit=True, auto=False, **kw)
Axes.set_ylim(bottom=None, top=None, *, emit=True, auto=False, **kw)
```

## 2. ¿Qué es?

Métodos que establecen explícitamente los límites numéricos mínimo y máximo para las escalas de coordenadas de los ejes X e Y.

## 3. ¿Para qué sirve?

Permiten hacer zoom sobre un rango crítico de interés, homogeneizar escalas entre múltiples subplots comparativos o invertir el sentido de un eje.

## 4. ¿Cómo funciona?

Sobrescriben el comportamiento de cálculo automático (`autoscale`) del objeto `Axis`, fijando rígidamente la transformación matemática de coordenadas del lienzo.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `left` / `bottom` | `float` | Opcional | `None` | Límite inferior de la escala numérica. |
| `right` / `top` | `float` | Opcional | `None` | Límite superior de la escala numérica. |
| `auto` | `bool` | Opcional | `False` | Si es `True`, reactiva el autoescalado de ese límite. |

## 6. Retorno

`tuple[float, float]`. Tupla con los límites asignados `(min, max)`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 15, 12, 18])

lims = ax.set_ylim(0, 30)
print(f"Límites Y asignados: {lims}")
plt.close(fig)
```

**Salida real:**

```text
Límites Y asignados: (0.0, 30.0)
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 20, 30, 40])

# Inversión de eje (por ejemplo profundidad o ranking)
ax.set_ylim(50, 0)
print(f"Límites invertidos: {ax.get_ylim()}")
plt.close(fig)
```

**Salida real:**

```text
Límites invertidos: (50.0, 0.0)
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
ax1.plot([1, 2, 3], [10, 20, 15])
ax2.plot([1, 2, 3], [5, 12, 8])

# Homogeneización programática de escala vertical
max_y = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
ax1.set_ylim(0, max_y)
ax2.set_ylim(0, max_y)

print(f"Escala compartida superior: {max_y}")
plt.close(fig)
```

**Salida real:**

```text
Escala compartida superior: 20.5
```

## 8. Errores frecuentes y casos borde

- **Omitir datos por zoom excesivo:** Fijar límites más estrechos que los datos recorta visualmente los puntos fuera del rango sin advertencia.
- **Pasar argumentos invertidos involuntariamente:** `set_xlim(10, 0)` invierte el eje deliberadamente; verificar siempre `(min, max)`.

## 9. Buenas prácticas y rendimiento

- Al graficar porcentajes o ratios, fijar límites estables `ax.set_ylim(0, 100)` para proveer contexto visual inequívoco.
- Al comparar múltiples paneles independientes, sincronizar sus límites manualmente o mediante `sharey=True`.

## 10. Métodos relacionados

- [grid](grid.md)
- [subplots](../01_figura_ejes/subplots.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xlim.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_ylim.html
