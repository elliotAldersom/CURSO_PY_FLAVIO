# Matplotlib: Axes.legend

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.legend(*args, **kwargs)
```

## 2. ¿Qué es?

`Axes.legend` coloca una caja de leyenda explicativa dentro del lienzo `Axes` para identificar los artistas gráficos que poseen etiquetas asignadas (`label`).

## 3. ¿Para qué sirve?

Resuelve el problema de legibilidad en gráficos con múltiples series o subgrupos, asociando colores y estilos de línea a sus entidades semánticas.

## 4. ¿Cómo funciona?

Escanea la lista de artistas pertenecientes al eje (`ax.lines`, `ax.patches`, etc.), extrae aquellos cuyo atributo `_label` no comience con guión bajo (`_`), y calcula la posición espacial óptima según el algoritmo de colisión especificado en `loc='best'`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `loc` | `str` o `int` o `tuple` | Opcional | `'best'` | Ubicación (`'upper right'`, `'lower left'`, `'center'`, etc.). |
| `fontsize` | `int` o `str` | Opcional | `None` | Tamaño de la fuente tipográfica en la leyenda. |
| `frameon` | `bool` | Opcional | `True` | Dibuja o remueve el marco de la caja de leyenda. |
| `ncols` / `ncol` | `int` | Opcional | `1` | Cantidad de columnas en las que se distribuyen las etiquetas. |
| `bbox_to_anchor` | `tuple[float, float]` | Opcional | `None` | Coordenadas externas para ubicar la leyenda fuera del eje. |

## 6. Retorno

`matplotlib.legend.Legend`. La instancia del objeto leyenda adjunto al eje.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2], [10, 20], label="Serie Alfa")
ax.plot([1, 2], [20, 15], label="Serie Beta")

leg = ax.legend(loc="upper left")
print(f"Tipo retornado: {type(leg).__name__}")
print(f"Etiquetas en leyenda: {[t.get_text() for t in leg.get_texts()]}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Legend
Etiquetas en leyenda: ['Serie Alfa', 'Serie Beta']
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 2, 3], label="A")
ax.plot([1, 2, 3], [3, 2, 1], label="B")
ax.plot([1, 2, 3], [2, 2, 2], label="C")

# Leyenda horizontal distribuida en 3 columnas sin borde
ax.legend(loc="upper center", ncol=3, frameon=False)
print(f"Borde activado: {ax.get_legend().get_frame_on()}")
plt.close(fig)
```

**Salida real:**

```text
Borde activado: False
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2], [3, 4], label="Métrica Primaria")

# Anclaje de la leyenda fuera del área de trazado (bbox_to_anchor)
leg = ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
print(f"Posición exterior configurada correctamente")
plt.close(fig)
```

**Salida real:**

```text
Posición exterior configurada correctamente
```

## 8. Errores frecuentes y casos borde

- **`No artists with labels found to put in legend`:** Ocurre al llamar `ax.legend()` sin haber pasado el argumento `label="..."` a los métodos de trazado (`plot`, `bar`, etc.).
- **Leyenda tapa datos críticos con `loc='best'`:** En series densas, el cálculo heurístico de 'best' puede fallar o enlentecer el renderizado. Especificar la posición explícita o usar `bbox_to_anchor`.

## 9. Buenas prácticas y rendimiento

- Evitar leyendas con decenas de entradas; dificultan la lectura. Considerar el etiquetado directo sobre las líneas (`direct labeling`).
- Usar `bbox_to_anchor` en dashboards corporativos para no invadir el área analítica de datos.

## 10. Métodos relacionados

- [plot](../02_graficos_basicos/plot.md)
- [grid](grid.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html
