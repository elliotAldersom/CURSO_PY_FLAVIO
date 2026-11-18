# Matplotlib: Figure y pyplot.figure

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
matplotlib.pyplot.figure(num=None, figsize=None, dpi=None, *, facecolor=None, edgecolor=None, frameon=True, FigureClass=Figure, clear=False, **kwargs)
```

## 2. ¿Qué es?

`pyplot.figure` es la función administradora que instancia o recupera una ventana de figura de nivel superior (`matplotlib.figure.Figure`).

## 3. ¿Para qué sirve?

Controla las propiedades del lienzo contenedor global (resolución DPI, color de fondo, tamaño físico) y administra la ventana en backends de GUI interactivos.

## 4. ¿Cómo funciona?

Registra la figura creada en el gestor global de figuras de `pyplot`. Si se especifica un identificador `num` existente, conmuta el contexto activo hacia dicha figura en lugar de recrearla.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `num` | `int` o `str` | Opcional | `None` | Identificador de la figura. Si existe, la activa. |
| `figsize` | `tuple[float, float]` | Opcional | `(6.4, 4.8)` | Tamaño de figura en pulgadas `(ancho, alto)`. |
| `dpi` | `float` | Opcional | `100.0` | Resolución de renderizado en puntos por pulgada. |
| `facecolor` | `color` | Opcional | `'white'` | Color de fondo del lienzo contenedor. |
| `clear` | `bool` | Opcional | `False` | Si es `True` y la figura ya existía, limpia sus artistas. |

## 6. Retorno

`matplotlib.figure.Figure`. La instancia de figura creada o activada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7, 3), dpi=120)
print(f"Tamaño en pulgadas: {fig.get_size_inches()}")
print(f"DPI: {fig.get_dpi()}")
plt.close(fig)
```

**Salida real:**

```text
Tamaño en pulgadas: [7. 3.]
DPI: 120.0
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([0, 1], [0, 10])
print(f"Cantidad de ejes: {len(fig.axes)}")
plt.close(fig)
```

**Salida real:**

```text
Cantidad de ejes: 1
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

# Reutilización y conmutación de contexto de figuras
fig1 = plt.figure(1)
fig2 = plt.figure(2)

print(f"Número de figura activa: {plt.gcf().number}")
plt.close('all')
print("Figuras cerradas limpiamente.")
```

**Salida real:**

```text
Número de figura activa: 2
Figuras cerradas limpiamente.
```

## 8. Errores frecuentes y casos borde

- **Crear figuras sin subplots:** Una `Figure` por sí sola no dibuja datos numéricos hasta que se le añade un `Axes` vía `fig.add_subplot()` o se usa `plt.subplots()`.
- **Sobrescribir por duplicar identificadores `num`:** Pasar el mismo entero modifica la figura existente sin advertencia previa si `clear=False`.

## 9. Buenas prácticas y rendimiento

- Para la gran mayoría de flujos analíticos, preferir `plt.subplots()` que gestiona la figura y los ejes de forma atómica.
- Definir el `dpi` según el destino: `100` para web/pantalla, `300` para impresión.

## 10. Métodos relacionados

- [subplots](subplots.md)
- [savefig](../04_exportacion_composicion/savefig.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
