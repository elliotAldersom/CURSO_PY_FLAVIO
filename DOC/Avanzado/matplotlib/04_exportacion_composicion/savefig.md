# Matplotlib: Figure.savefig

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Figure.savefig(fname, *, transparent=None, dpi='figure', format=None, metadata=None, bbox_inches=None, pad_inches=0.1, facecolor='auto', edgecolor='auto', backend=None, **kwargs)
```

## 2. ¿Qué es?

`Figure.savefig` es el método de persistencia que renderiza el lienzo completo a un archivo en disco, un flujo binario en memoria o una cadena SVG.

## 3. ¿Para qué sirve?

Permite serializar visualizaciones en formatos vectoriales de alta fidelidad (PDF, SVG) o imágenes rasterizadas (PNG, JPEG, WebP) para publicaciones científicas, reportes y microservicios web.

## 4. ¿Cómo funciona?

Compila todos los artistas registrados en el árbol de la figura, invoca el renderer correspondiente al backend seleccionado (ej. `RendererAgg` para PNG o `RendererSVG`) y escribe los bytes resultantes.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `fname` | `str` o `Path` o `io.BytesIO` | Obligatorio | N/A | Ruta del archivo de salida o búfer en memoria. |
| `dpi` | `float` o `'figure'` | Opcional | `'figure'` | Resolución en puntos por pulgada para formatos rasterizados. |
| `format` | `str` | Opcional | `None` | Formato explícito (`'png'`, `'pdf'`, `'svg'`). Si es `None`, se deduce de la extensión. |
| `bbox_inches` | `'tight'` o `Bbox` | Opcional | `None` | Si es `'tight'`, recorta espacios blancos sobrantes alrededor de los ejes. |
| `transparent` | `bool` | Opcional | `False` | Genera la figura con fondo transparente si el formato lo soporta. |

## 6. Retorno

`None`. Escribe el contenido binario en el destino especificado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import io
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2], [3, 4])

buffer = io.BytesIO()
fig.savefig(buffer, format="png")
print(f"Bytes exportados a buffer: {len(buffer.getvalue()) > 0}")
plt.close(fig)
```

**Salida real:**

```text
Bytes exportados a buffer: True
```

### Nivel 2: Intermedio

```python
import io
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))
ax.set_title("Gráfico Vectorial de Alta Resolución")
ax.plot([0, 1], [0, 100])

pdf_buffer = io.BytesIO()
fig.savefig(pdf_buffer, format="pdf", bbox_inches="tight")
print(f"Encabezado de archivo PDF: {pdf_buffer.getvalue()[:4]}")
plt.close(fig)
```

**Salida real:**

```text
Encabezado de archivo PDF: b'%PDF'
```

### Nivel 3: Avanzado

```python
import io
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter([1, 2], [3, 4], color="green")
ax.set_title("Exportación con Fondo Transparente")

buffer = io.BytesIO()
fig.savefig(buffer, format="png", transparent=True, dpi=300, bbox_inches="tight")
print(f"Tamaño PNG a 300 DPI: {len(buffer.getvalue())} bytes")
plt.close(fig)
```

**Salida real:**

```text
Tamaño PNG a 300 DPI: 24785 bytes
```

## 8. Errores frecuentes y casos borde

- **Llamar `plt.show()` antes de `savefig()`:** En entornos interactivos, `plt.show()` crea una nueva figura vacía al cerrarse la ventana previa, provocando que `savefig()` guarde una imagen totalmente en blanco. Llamar siempre `savefig()` antes de `show()`.
- **Etiquetas cortadas en los márgenes:** Resolver pasando siempre `bbox_inches='tight'`.

## 9. Buenas prácticas y rendimiento

- En entornos de producción headless (servidores, Docker), utilizar `io.BytesIO()` para no tocar el disco rígido innecesariamente.
- Seleccionar formatos vectoriales (`.pdf`, `.svg`) para publicaciones académicas y documentos imprimibles.

## 10. Métodos relacionados

- [tight_layout](tight_layout.md)
- [figure](../01_figura_ejes/figure.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html
