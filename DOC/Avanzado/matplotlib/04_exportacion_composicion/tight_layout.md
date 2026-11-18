# Matplotlib: Figure.tight_layout

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Figure.tight_layout(*, pad=1.08, h_pad=None, w_pad=None, rect=None)
```

## 2. ¿Qué es?

`Figure.tight_layout` ajusta automáticamente los márgenes, espaciados inter-subplots y acolchados de la figura para evitar colisiones entre etiquetas de ejes, títulos y marcas.

## 3. ¿Para qué sirve?

Elimina el trabajo manual de calibrar coordenadas en figuras compuestas multipanel, garantizando que todos los textos sean completamente visibles.

## 4. ¿Cómo funciona?

Calcula la caja envolvente (`bounding box`) de todos los textos y artistas de cada eje, redimensionando la cuadrícula de subplots de manera proporcional según el espacio disponible.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `pad` | `float` | Opcional | `1.08` | Espaciado entre el borde de la figura y los límites de los ejes. |
| `h_pad` | `float` | Opcional | `None` | Espaciado vertical específico entre subplots contiguos. |
| `w_pad` | `float` | Opcional | `None` | Espaciado horizontal específico entre subplots contiguos. |
| `rect` | `tuple[float, float, float, float]` | Opcional | `None` | Rectángulo contenedor normalizado `(left, bottom, right, top)` para reservar espacio a títulos globales. |

## 6. Retorno

`None`. Modifica la geometría interna de los subplots en la figura.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_ylabel("Métrica con Etiqueta Muy Extensa")
ax2.set_ylabel("Otra Métrica Externa")

fig.tight_layout()
print("tight_layout aplicado con éxito")
plt.close(fig)
```

**Salida real:**

```text
tight_layout aplicado con éxito
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(6, 6))
for i, ax in enumerate(axes.flat):
    ax.set_title(f"Panel Detallado #{i+1}")

fig.tight_layout(h_pad=2.0, w_pad=2.0)
print("Espaciados horizontal y vertical personalizados")
plt.close(fig)
```

**Salida real:**

```text
Espaciados horizontal y vertical personalizados
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
fig.suptitle("Título Maestro Corporativo Global", fontsize=14)

# Reserva del 10% superior (rect top=0.90) para que el suptitle no colisione
fig.tight_layout(rect=[0, 0, 1, 0.90])
print("Layout adaptado con reserva para suptitle")
plt.close(fig)
```

**Salida real:**

```text
Layout adaptado con reserva para suptitle
```

## 8. Errores frecuentes y casos borde

- **Conflicto con `constrained_layout`:** Si la figura fue creada con `layout='constrained'`, llamar a `tight_layout()` genera una advertencia o ignora el ajuste.
- **Suptitle superpuesto:** El `tight_layout` básico no toma en cuenta `fig.suptitle()`, por lo que se debe especificar el parámetro `rect`.

## 9. Buenas prácticas y rendimiento

- Considerar la alternativa moderna `plt.subplots(..., layout='constrained')` introducida en versiones recientes de Matplotlib para ajustes automáticos en tiempo real.
- En scripts de exportación, invocar `fig.tight_layout()` inmediatamente antes de `fig.savefig()`.

## 10. Métodos relacionados

- [savefig](savefig.md)
- [subplots](../01_figura_ejes/subplots.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.tight_layout.html
