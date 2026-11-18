# Fundamentos de Matplotlib: Arquitectura y Visualización Científica en Python

Matplotlib es la biblioteca fundacional del ecosistema científico de Python para la generación de figuras estáticas, animadas e interactivas con calidad de publicación.

## 2. Introducción

Desarrollada originalmente por John D. Hunter en 2003 para emular los comandos gráficos de MATLAB en Python, Matplotlib se convirtió en el motor gráfico subyacente sobre el cual operan bibliotecas de alto nivel como Seaborn, Pandas Plotting y GeoPandas.

La biblioteca está estructurada en capas arquitectónicas rigurosas: la capa Backend (que interactúa con el sistema operativo y formatos de renderizado como AGG, PDF, SVG), la capa Artist (donde residen las primitivas gráficas: líneas, textos, figuras, ejes) y la capa Scripting (`matplotlib.pyplot`), que provee una interfaz procedural para construir visualizaciones rápidamente.

## 3. Fundamentos y conceptos

Comprender Matplotlib requiere dominar su jerarquía de objetos fundamental:
1. **`Figure` (Figura):** El lienzo o ventana completa donde se dibuja. Contiene uno o múltiples sistemas de coordenadas (`Axes`), títulos globales, leyendas de figura y elementos de colorbar.
2. **`Axes` (Ejes o Subplot):** El área de trazado donde se representan los datos numéricos. Posee dos (o tres en 3D) objetos `Axis` que controlan límites, escalas y marcas (`ticks`). Un `Figure` puede albergar múltiples `Axes`.
3. **`Axis` (Eje coordenado):** Administrador de la escala matemática, límites (`xlim`, `ylim`), líneas de cuadrícula y etiquetas de las marcas (`ticks`).
4. **`Artist`:** Cualquier objeto visualizable en el lienzo (texto, línea, rectángulo, polígono, colección). Tanto `Figure`, `Axes` y `Axis` son en sí mismos tipos especializados de `Artist`.

Existen dos paradigmas de programación en Matplotlib:
- **Paradigma Orientado a Objetos (OO):** Se crean explícitamente instancias de `Figure` y `Axes` (`fig, ax = plt.subplots()`) y se invocan métodos sobre `ax`. Es el estándar innegociable en desarrollo profesional y entornos de producción.
- **Paradigma Procedural (`pyplot` tipo MATLAB):** Mantiene un estado global implícito (`plt.plot()`, `plt.title()`). Es aceptable para exploración rápida en notebooks, pero peligroso en producción debido a colisiones de estado global.

## 4. Sintaxis y funcionamiento

El patrón moderno y robusto se fundamenta en `plt.subplots()`:

```python
import matplotlib.pyplot as plt

# Creación explícita de figura y lienzo coordenado
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

# Llamadas a métodos del objeto Axes
ax.plot([1, 2, 3], [10, 20, 15], label="Serie A")
ax.set_title("Evolución Temporal")
ax.set_xlabel("Periodo")
ax.set_ylabel("Métrica")
ax.legend()

# Liberación explícita de memoria
plt.close(fig)
```

## 5. Ejemplos prácticos progresivos

### Básico

Construcción orientada a objetos de un gráfico lineal simple con inspección de metadatos de los ejes.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

linea = ax.plot(x, y, color="tab:blue", linestyle="--", label="Lineal")[0]
ax.set_title("Gráfico Lineal Básico")
ax.set_xlabel("X")
ax.set_ylabel("Y")

print(f"Tipo de objeto retornado: {type(linea)}")
print(f"Límites X calculados: {ax.get_xlim()}")
print(f"Límites Y calculados: {ax.get_ylim()}")
plt.close(fig)
```

**Salida real:**

```text
Tipo de objeto retornado: <class 'matplotlib.lines.Line2D'>
Límites X calculados: (0.8, 5.2)
Límites Y calculados: (1.6, 10.4)
```

### Intermedio

Composición de múltiples subplots en una grilla con escalas compartidas y personalización de marcas.

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

meses = ["Ene", "Feb", "Mar", "Abr"]
ventas_a = [120, 150, 180, 220]
ventas_b = [90, 130, 210, 240]

ax1.bar(meses, ventas_a, color="teal", alpha=0.8)
ax1.set_title("Región Norte")
ax1.set_ylabel("Ventas (k$)")
ax1.grid(axis="y", linestyle=":", alpha=0.6)

ax2.bar(meses, ventas_b, color="coral", alpha=0.8)
ax2.set_title("Región Sur")
ax2.grid(axis="y", linestyle=":", alpha=0.6)

fig.suptitle("Comparativa Trimestral de Rendimiento", fontsize=14)
print(f"Número de ejes en la figura: {len(fig.axes)}")
plt.close(fig)
```

**Salida real:**

```text
Número de ejes en la figura: 2
```

### Avanzado

Generación de visualización multipanel en memoria y exportación directa a buffer de bytes para integración en servicios web.

```python
import io
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot([0, 1, 2, 3], [0, 1, 4, 9], 'r-o', label="Cuadrática")
ax.set_title("Exportación en Memoria")
ax.legend()

buffer = io.BytesIO()
fig.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
buffer.seek(0)
png_bytes = buffer.getvalue()

print(f"Longitud de bytes generados: {len(png_bytes)} bytes")
print(f"Firma inicial PNG: {png_bytes[:8]}")
plt.close(fig)
```

**Salida real:**

```text
Longitud de bytes generados: 15420 bytes
Firma inicial PNG: b'\x89PNG\r\n\x1a\n'
```

## 6. Aplicaciones en el mundo real

- **Monitoreo de telemetría y dashboards:** Trazado de señales temporales (CPU, memoria, latencias de red) en pipelines de observabilidad.
- **Reportes financieros y regulatorios:** Exportación de gráficos en formatos vectoriales (PDF, SVG) para auditorías bancarias y presentaciones corporativas.
- **Investigación científica y bioinformática:** Representación de mapas de dispersión génica, espectrometría de masas y modelos de ajuste no lineal con barras de error rigurosas.

## 7. Uso en producción

- **Backend sin cabeza (Headless):** En servidores o contenedores Docker sin display gráfico, configurar explícitamente el backend no interactivo antes de importar pyplot:
```python
# NO EJECUTAR (Configuracion headless en servidor)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```
- **Fuga de memoria (Memory Leaks):** Matplotlib mantiene referencias globales a todas las figuras creadas hasta que se invoca `plt.close(fig)`. En servidores web o bucles de generación masiva de reportes, omitir `plt.close(fig)` satura la memoria RAM rápidamente.

## 8. Errores comunes y recomendaciones

- **Mezclar `plt.algo()` con métodos de `ax`:** Provoca que títulos o etiquetas se apliquen al eje activo incorrecto cuando existen múltiples subplots. Emplear exclusivamente métodos de `Axes` (`ax.set_title()`, `ax.set_xlabel()`).
- **Omitir `tight_layout()` o `bbox_inches='tight'`:** Resulta en etiquetas de ejes cortadas o superpuestas con el borde de la imagen.
- **No cerrar figuras:** Llamar a `plt.close('all')` o `plt.close(fig)` al finalizar cada renderizado.

## 9. Resumen

Matplotlib es un motor gráfico de bajo nivel altamente configurable basado en la jerarquía `Figure` -> `Axes` -> `Axis`. El uso estricto de la interfaz orientada a objetos (`fig, ax = plt.subplots()`) y el control del ciclo de vida del backend (`Agg`) garantizan visualizaciones reproducibles, eficientes y seguras para despliegue industrial.

## 10. Referencias oficiales

- Documentación oficial de Matplotlib: https://matplotlib.org/stable/users/index.html
- Guía de arquitectura de Matplotlib (The Lifecycle of a Plot): https://matplotlib.org/stable/tutorials/introductory/lifecycle.html
- Referencia de la API de Matplotlib: https://matplotlib.org/stable/api/index.html
