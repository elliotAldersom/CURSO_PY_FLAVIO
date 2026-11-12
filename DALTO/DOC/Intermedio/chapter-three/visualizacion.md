# Visualización de Datos Estadísticos con Matplotlib y Seaborn

## 2. Introducción

Las métricas agregadas como la media o la suma total resumen una columna en un único escalar, pero pueden ocultar fenómenos decisivos: picos abruptos en una fecha concreta (`grafico_lineal.csv` L4), concentración desproporcionada en una sola categoría (`grafico_barras.csv` L2), anomalías alejadas de una tendencia lineal (`grafico_de_dispersion.csv` L10) o asimetrías severas entre grupos (`grafico_de_bigotes.csv`).

En el ecosistema científico de Python, la representación visual estándar se apoya en dos **bibliotecas externas de terceros** —ajenas a la biblioteca estándar y que deben instalarse explícitamente (`pip install matplotlib seaborn`)— estrechamente integradas con [Pandas](pandas_fundamentos.md):

- **Matplotlib (`matplotlib.pyplot`):** motor gráfico fundacional de dos dimensiones que controla con precisión cada lienzo, eje, marca, tipografía y formato de exportación.
- **Seaborn (`seaborn`):** interfaz declarativa de visualización estadística construida sobre Matplotlib que traduce columnas de un `DataFrame` directamente en codificaciones visuales y resúmenes estadísticos.

Dominar ambas herramientas permite cubrir cuatro competencias esenciales:

1. **Elección rigurosa del tipo de gráfico:** seleccionar entre líneas, barras, dispersión y diagramas de caja según la naturaleza matemática de las variables (temporal, categórica o cuantitativa continua).
2. **Combinación de capas declarativas y anotaciones finas:** trazar tendencias con Seaborn (`sns.lineplot`) y resaltar hitos puntuales o umbrales con primitivas de Matplotlib (`ax.plot`, `grafico_lineal.py` L23-26).
3. **Arquitectura orientada a objetos (`Figure` y `Axes`):** superar las limitaciones de la máquina de estados global `plt.*` al componer paneles múltiples o funciones reutilizables.
4. **Renderizado automatizado en servidores (*headless*):** exportar figuras en alta resolución (`savefig`, `dpi=300`) con el *backend* `Agg` y liberar memoria explícitamente (`plt.close(fig)`) en entornos de producción sin pantalla.

## 3. Fundamentos y conceptos

**Relación arquitectónica entre Pandas, Matplotlib y Seaborn.** Ninguna de estas tres herramientas pertenece a la biblioteca estándar de Python. Operan en tres niveles complementarios:

1. **Capa de datos ([Pandas](pandas_fundamentos.md)):** entrega un `DataFrame` en formato *tidy* (datos ordenados), donde cada columna representa una variable (`"fecha"`, `"ingresos"`, `"tiempo"`, `"categoría"`) y cada fila una observación.
2. **Capa de abstracción estadística (Seaborn):** funciones como `sns.lineplot`, `sns.barplot`, `sns.scatterplot` y `sns.boxplot` reciben `data=df` y los nombres de columnas `x=...`, `y=...`, `hue=...`, calculan agregaciones o cuartiles automáticamente y dibujan sobre un objeto `Axes` de Matplotlib.
3. **Capa de lienzo y renderizado (Matplotlib):** organiza cada gráfico en una jerarquía de objetos (*Artists*):
   - **`Figure`:** el contenedor raíz (la ventana o imagen completa) que define las dimensiones físicas y la resolución (`dpi`).
   - **`Axes`:** cada subgráfico individual dentro de la figura, provisto de eje X, eje Y, título, etiquetas y área de trazado. Una sola `Figure` puede alojar uno o varios `Axes`.

**Criterio de selección entre los cuatro gráficos fundamentales.** Elegir un gráfico equivocado distorsiona la interpretación de los datos. Cada uno de los cuatro diagramas estudiados en el curso responde a una pregunta analítica específica:

| Gráfico | Función Seaborn | Variables (`x`, `y`) | Propósito analítico principal | Referencia del curso |
|---|---|---|---|---|
| **Líneas** | `sns.lineplot` | Secuencia ordenada/temporal (`x`) vs. cuantitativa (`y`) | Observar evolución, tendencias, ciclos y picos a lo largo del tiempo | `grafico_lineal.py` |
| **Barras** | `sns.barplot` | Categórica discreta (`x`) vs. cuantitativa (`y`) | Comparar magnitudes o medias entre categorías independientes | `grafico_barras.py` |
| **Dispersión** | `sns.scatterplot` | Cuantitativa continua (`x`) vs. cuantitativa continua (`y`) | Evaluar correlación, forma funcional, agrupamientos y puntos atípicos bivariados | `grafico_de_dispersion.py` |
| **Caja y bigotes** | `sns.boxplot` | Categórica (`x`) vs. cuantitativa (`y`) | Comparar mediana, dispersión intercuartílica, asimetría y valores atípicos (*outliers*) | `grafico_de_bigotes.py` |

**Reglas de integridad visual y anatomía estadística de cada gráfico.**

- **Gráfico de líneas (`sns.lineplot`):** conecta puntos adyacentes con segmentos, lo que implica continuidad u orden secuencial entre observaciones (`"01-01"` a `"01-15"` en `grafico_lineal.csv`). Nunca debe usarse un gráfico de líneas para categorías nominales sin orden intrínseco (como países o áreas), pues la pendiente entre ellas carecería de significado. En `grafico_lineal.py` (L26) se resalta el pico con `plt.plot("01-03", 17, "o")`; en código mantenible conviene calcular dicho máximo dinámicamente sobre el `DataFrame` (`idxmax()`) para que la marca se actualice sola si cambian los datos.
- **Gráfico de barras (`sns.barplot`):** codifica la magnitud mediante la **longitud** del rectángulo. Por ello, **el eje numérico de un gráfico de barras debe iniciar siempre en `0`**: recortar la base exagera visualmente diferencias pequeñas. Además, si existen varias filas para una misma categoría en `df`, `sns.barplot` calcula por defecto el promedio y dibuja una barra de incertidumbre (controlable en Seaborn >= 0.12 mediante el parámetro `errorbar`, p. ej. `errorbar=None` o `errorbar="sd"`).
- **Gráfico de dispersión (`sns.scatterplot`):** coloca un marcador por cada par $(x_i, y_i)$ sin unirlos (`grafico_de_dispersion.py` L23; obsérvese que el comentario de la línea 15 decía por arrastre "gráfico de barras", tratándose en realidad de un diagrama de dispersión). Permite distinguir de inmediato en `grafico_de_dispersion.csv` la relación creciente entre `tiempo` y `dinero`, así como la anomalía aislada en `(94, 192)`.
- **Diagrama de caja y bigotes (`sns.boxplot`):** sintetiza cinco estadísticos robustos de orden (`grafico_de_bigotes.py` L23, donde también conviene corregir el bloque documental de las líneas 15-21 que mencionaba `barplot`):
  - El borde inferior y el borde superior de la caja corresponden al primer cuartil $Q_1$ (percentil 25) y al tercer cuartil $Q_3$ (percentil 75); la altura de la caja es el **rango intercuartílico** $\text{IQR} = Q_3 - Q_1$, que concentra el $50\%$ central de los datos.
  - La línea interior marca la **mediana** $Q_2$ (percentil 50), inmune a valores extremos.
  - Según la convención estándar de Tukey (`whis=1.5`), los **bigotes** se extienden hasta la observación real más lejana contenida dentro del intervalo $[Q_1 - 1.5 \cdot \text{IQR},\; Q_3 + 1.5 \cdot \text{IQR}]$.
  - Todo dato situado fuera de esas vallas se representa individualmente como valor atípico (*outlier*).

**Interfaz implícita `pyplot` frente a la API explícita orientada a objetos (`fig, ax = plt.subplots()`).** Matplotlib ofrece dos estilos de programación:

1. **Estilo implícito basado en estado (`plt.plot(...)`, `plt.title(...)`, `plt.show()`):** utilizado en los cuatro guiones iniciales del curso. Mantiene internamente variables globales ocultas que apuntan a la "figura activa" y al "eje activo". Resulta breve para pruebas rápidas de un solo gráfico, pero se vuelve frágil al generar múltiples figuras concurrentes o paneles compuestos.
2. **Estilo explícito orientado a objetos (`fig, ax = plt.subplots()`):** crea referencias explícitas al lienzo `fig` y al eje `ax` (o matriz de ejes `axes`). Todas las funciones a nivel de ejes de Seaborn aceptan el argumento `ax=ax` (`sns.boxplot(..., ax=ax)`), y los títulos, límites y etiquetas se configuran sobre ese eje concreto (`ax.set_title(...)`, `ax.set_xlabel(...)`, `ax.set_ylabel(...)`). Es el estándar recomendado para aplicaciones modulares y producción.

## 4. Sintaxis y funcionamiento

Esquema profesional combinando Seaborn con la API orientada a objetos de Matplotlib:

```text
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 5))
sns.<funcion_grafico>(data=df, x="<col_x>", y="<col_y>", ax=ax)
ax.set_title("<Título descriptivo>")
ax.set_xlabel("<Etiqueta X>")
ax.set_ylabel("<Etiqueta Y>")
fig.savefig("<ruta_salida>.png", dpi=300, bbox_inches="tight")
plt.close(fig)
```

Elementos principales de visualización con Matplotlib y Seaborn:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `matplotlib.use("Agg")` | Selecciona *backend* sin ventana gráfica para servidores (antes de `pyplot`) | `matplotlib.use("Agg")` |
| 2 | `fig, ax = plt.subplots(...)` | Crea explícitamente una figura (`Figure`) y uno o más ejes (`Axes`) | `fig, ax = plt.subplots(figsize=(8, 4))` |
| 3 | `sns.lineplot(...)` | Traza evolución continua o serie temporal sobre `ax` | `sns.lineplot(data=df, x="fecha", y="ventas", ax=ax)` |
| 4 | `sns.barplot(...)` | Traza barras comparativas por categoría (`errorbar=None` omite intervalos) | `sns.barplot(data=df, x="area", y="monto", ax=ax)` |
| 5 | `sns.scatterplot(...)` | Representa pares cuantitativos $(x, y)$ admitiendo `hue` y `style` | `sns.scatterplot(data=df, x="t", y="usd", ax=ax)` |
| 6 | `sns.boxplot(...)` | Dibuja mediana, caja IQR, bigotes de Tukey y puntos atípicos | `sns.boxplot(data=df, x="grupo", y="valor", ax=ax)` |
| 7 | `ax.plot(x, y, "o")` | Superpone marcadores o líneas puntuales sobre el sistema de ejes `ax` | `ax.plot("01-03", 17, marker="o")` |
| 8 | `ax.set_title` / `set_xlabel` | Asigna título y nombres con unidades explícitas al eje `ax` | `ax.set_ylabel("Ingresos (USD)")` |
| 9 | `fig.savefig(dest, ...)` | Renderiza la figura a disco o búfer (`png`, `svg`, `pdf`) | `fig.savefig("graf.png", dpi=300, bbox_inches="tight")` |
| 10 | `plt.show()` | Abre ventana interactiva bloqueante en entornos locales de escritorio | `plt.show()` |
| 11 | `plt.close(fig)` | Cierra y libera de la memoria global de `pyplot` la figura indicada | `plt.close(fig)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Serie temporal con `sns.lineplot`, detección dinámica del máximo y exportación en memoria (`Agg`).**

```python
import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CSV_LINEAL = (
    '"fecha","comidas"\n'
    '"01-01",3\n"01-02",4\n"01-03",17\n"01-04",3\n"01-05",5\n'
)

df_tiempo = pd.read_csv(io.StringIO(CSV_LINEAL))
fila_pico = df_tiempo.loc[df_tiempo["comidas"].idxmax()]

fig, ax = plt.subplots(figsize=(7, 4))
try:
    sns.lineplot(data=df_tiempo, x="fecha", y="comidas", ax=ax)
    ax.plot(fila_pico["fecha"], fila_pico["comidas"], marker="o", color="crimson")
    ax.set_title("Evolución diaria de comidas registradas")
    ax.set_xlabel("Fecha (MM-DD)")
    ax.set_ylabel("Cantidad de comidas")

    bufer_png = io.BytesIO()
    fig.savefig(bufer_png, format="png", dpi=150, bbox_inches="tight")
    cabecera_valida = bufer_png.getvalue()[:8] == b"\x89PNG\r\n\x1a\n"
    titulo_registrado = ax.get_title()
finally:
    plt.close(fig)

print(f"Pico detectado: fecha={fila_pico['fecha']} | valor={fila_pico['comidas']}")
print("Título del gráfico:", titulo_registrado)
print("PNG válido generado en memoria:", cabecera_valida)
```

Explicación paso a paso:

- Mejorando `grafico_lineal.py` (L23-29), en lugar de codificar manualmente `"01-03"` y `17`, `df_tiempo["comidas"].idxmax()` localiza dinámicamente la etiqueta de fila con el mayor registro.
- Se emplea `fig, ax = plt.subplots(...)`, se pasa `ax=ax` a `sns.lineplot`, se exporta el PNG a un búfer `io.BytesIO` verificando su firma binaria estándar y se libera la figura en un bloque `finally` con `plt.close(fig)`.

Resultado esperado:

```text
Pico detectado: fecha=01-03 | valor=17
Título del gráfico: Evolución diaria de comidas registradas
PNG válido generado en memoria: True
```

### Intermedio

**Ejemplo 2 — Lienzo multipanel (`1x2`) combinando `sns.barplot` y `sns.scatterplot` con métricas analíticas complementarias.**

```python
import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CSV_INGRESOS = (
    '"fuente","ingresos"\n'
    '"Trabajo fijo",3000\n'
    '"Freelance",800\n'
    '"Youtube regalías",350\n'
    '"Influencer",600\n'
    '"Cripto",150\n'
)

CSV_DISPERSION = (
    "tiempo,dinero\n"
    "12,21\n22,31\n32,43\n42,51\n53,61\n"
    "63,71\n74,87\n87,94\n94,192\n103,112\n"
)

df_ing = pd.read_csv(io.StringIO(CSV_INGRESOS)).sort_values("ingresos", ascending=False)
df_disp = pd.read_csv(io.StringIO(CSV_DISPERSION))

total_usd = int(df_ing["ingresos"].sum())
participacion_principal = (df_ing["ingresos"].iloc[0] / total_usd) * 100
punto_extremo = df_disp.loc[df_disp["dinero"].idxmax()]

fig, (ax_barras, ax_disp) = plt.subplots(nrows=1, ncols=2, figsize=(12, 4.5))
try:
    sns.barplot(data=df_ing, x="fuente", y="ingresos", errorbar=None, ax=ax_barras)
    ax_barras.set_title(f"Ingresos por fuente (Total: {total_usd} USD)")
    ax_barras.tick_params(axis="x", rotation=20)

    sns.scatterplot(data=df_disp, x="tiempo", y="dinero", ax=ax_disp)
    ax_disp.set_title("Relación bivariada tiempo vs. dinero")

    fig.tight_layout()
    cantidad_subgraficos = len(fig.axes)
finally:
    plt.close(fig)

print(f"Subgráficos en la figura: {cantidad_subgraficos}")
print(f"Total ingresos: {total_usd} USD | Fuente líder: {participacion_principal:.2f}%")
print(f"Observación extrema en dispersión: tiempo={punto_extremo['tiempo']}, dinero={punto_extremo['dinero']}")
```

Explicación técnica:

- Integrando los conjuntos de datos de `grafico_barras.csv` y `grafico_de_dispersion.csv`, la API orientada a objetos permite alojar dos gráficos independientes `(ax_barras, ax_disp)` en una misma figura sin interferencia de estado.
- Ordenar previamente las barras de mayor a menor (`sort_values`) y rotar las etiquetas categóricas (`tick_params`) mejora sustancialmente la legibilidad ejecutiva.

Resultado esperado:

```text
Subgráficos en la figura: 2
Total ingresos: 4900 USD | Fuente líder: 61.22%
Observación extrema en dispersión: tiempo=94, dinero=192
```

### Avanzado

**Ejemplo 3 — Análisis de distribución e identificación formal de valores atípicos (criterio de Tukey) con `sns.boxplot` y exportación de producción.**

```python
import io
import tempfile
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CSV_LATENCIAS = (
    "servicio,latencia_ms\n"
    "API_A,40\nAPI_A,42\nAPI_A,45\nAPI_A,48\nAPI_A,50\n"
    "API_A,52\nAPI_A,54\nAPI_A,56\nAPI_A,95\n"
    "API_B,28\nAPI_B,30\nAPI_B,31\nAPI_B,33\nAPI_B,35\n"
)

df_lat = pd.read_csv(io.StringIO(CSV_LATENCIAS))
serie_a = df_lat.loc[df_lat["servicio"] == "API_A", "latencia_ms"]

q1 = serie_a.quantile(0.25)
mediana = serie_a.quantile(0.50)
q3 = serie_a.quantile(0.75)
iqr = q3 - q1
umbral_superior = q3 + 1.5 * iqr
atipicos_a = list(serie_a[serie_a > umbral_superior])

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta_figura = Path(tmp_dir) / "reporte_latencias.png"
    fig, ax = plt.subplots(figsize=(7, 4.5))
    try:
        sns.boxplot(data=df_lat, x="servicio", y="latencia_ms", ax=ax)
        ax.set_title("Distribución de latencia por servicio")
        ax.set_xlabel("Servicio evaluado")
        ax.set_ylabel("Latencia de respuesta (ms)")
        fig.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    finally:
        plt.close(fig)

    archivo_valido = ruta_figura.exists() and ruta_figura.stat().st_size > 0

print(f"API_A -> Q1={q1:.1f} | Mediana={mediana:.1f} | Q3={q3:.1f} | IQR={iqr:.1f}")
print(f"Valla superior de Tukey: {umbral_superior:.1f} ms | Atípicos: {atipicos_a}")
print("Figura de 300 DPI exportada en disco:", archivo_valido)
```

Explicación estadística y operativa:

- Hace explícita la matemática exacta que `sns.boxplot` traza visualmente: para `API_A`, el rango intercuartílico es $\text{IQR} = 54.0 - 45.0 = 9.0\text{ ms}$ y el límite superior del bigote es $54.0 + 1.5 \times 9.0 = 67.5\text{ ms}$, por lo que la observación de `95` ms queda marcada fuera del bigote como valor atípico (*outlier*).
- La exportación con `dpi=300` y `bbox_inches="tight"` evita que se recorten títulos o etiquetas rotadas y genera un activo apto para informes técnicos impresos o digitales.

Resultado esperado:

```text
API_A -> Q1=45.0 | Mediana=50.0 | Q3=54.0 | IQR=9.0
Valla superior de Tukey: 67.5 ms | Atípicos: [95]
Figura de 300 DPI exportada en disco: True
```

## 6. Aplicaciones en el mundo real

- **Observabilidad e ingeniería de confiabilidad (*SRE*):** diagramas de líneas temporales y cajas de cuantiles para vigilar tiempos de respuesta (p50, p95, p99), consumo de memoria y tasas de error tras cada despliegue.
- **Generación automatizada de informes financieros y ejecutivos:** tareas nocturnas que leen indicadores consolidados con Pandas, renderizan gráficos comparativos en PNG o SVG y los incrustan en documentos PDF o correos corporativos.
- **Validación y diagnóstico en ciencia de datos:** gráficos de dispersión de residuos y diagramas de caja por segmento para detectar anomalías de captura o sesgos antes de entrenar modelos predictivos.
- **Publicaciones científicas y académicas:** exportación vectorial en PDF o SVG mediante Matplotlib garantizando nitidez tipográfica a cualquier escala de ampliación.

## 7. Uso en producción

- **Configurar un *backend* no interactivo (`Agg`) y eliminar `plt.show()` en servidores:** en contenedores Linux, funciones *serverless* o demonios en segundo plano no existe monitor ni servidor X11; llamar a `plt.show()` no muestra nada o bloquea la ejecución indefinidamente. En producción debe fijarse `matplotlib.use("Agg")` (o la variable de entorno `MPLBACKEND=Agg`) y persistirse la salida exclusivamente con `fig.savefig(...)`.
- **Cerrar siempre cada figura (`plt.close(fig)`) para evitar fugas de memoria:** cuando se crean figuras mediante `plt.subplots()` dentro de un bucle de reportes o en un servidor web de larga vida, `pyplot` mantiene una referencia interna global a cada `Figure`. Omitir `plt.close(fig)` impide al recolector de basura reclamar esa memoria y termina agotando la RAM del proceso (*Out Of Memory*). En servidores multihilo de alta concurrencia se recomienda incluso instanciar `from matplotlib.figure import Figure` directamente sin pasar por `pyplot`, ya que la máquina de estados global de `pyplot` no es segura entre hilos (*not thread-safe*).
- **Utilizar paletas accesibles para daltonismo e incluir unidades explícitas:** configurar paletas perceptualmente seguras (`sns.set_palette("colorblind")` o `viridis`) y rotular siempre las unidades de medida en los ejes (`"Ingresos (USD)"`, `"Latencia (ms)"`) garantiza que el gráfico sea autoexplicativo fuera de contexto.
- **Evitar `sns.boxplot` en muestras diminutas sin superponer los puntos reales:** cuando una categoría cuenta con muy pocas observaciones (como las `3` y `2` filas de `grafico_de_bigotes.csv`), calcular cuartiles por sí solos puede resultar engañoso; en muestras menores a ~20 registros conviene acompañar o sustituir la caja con `sns.stripplot` o `sns.swarmplot` para mostrar cada observación real.

## 8. Errores comunes y recomendaciones

1. **Olvidar `plt.close(fig)` dentro de procesos por lotes o endpoints web (fuga progresiva de RAM).**

```python
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Forma segura: cerrar cada figura inmediatamente después de exportarla
for lote in range(3):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [lote, lote + 1, lote + 2])
    plt.close(fig)

print("Figuras retenidas abiertas en pyplot:", len(plt.get_fignums()))
```

Resultado esperado:

```text
Figuras retenidas abiertas en pyplot: 0
```

Diagnóstico: sin `plt.close(fig)`, `plt.get_fignums()` crecería indefinidamente (`1, 2, 3, ...`) reteniendo megabytes de búferes de píxeles por cada gráfico. Solución: envolver la creación y el guardado en `try ... finally: plt.close(fig)`.

2. **Llamar a `fig.savefig(...)` después de haber ejecutado `plt.show()` sobre la interfaz global.**

```python
# ERROR INTENCIONAL: guardar un lienzo en blanco por invocar plt.savefig() después de plt.show()
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [10, 20, 30])
plt.show()                  # Al cerrarse la ventana interactiva, pyplot limpia y descarta la figura activa
plt.savefig("blanco.png")   # Crea una figura nueva completamente vacía y guarda una imagen en blanco
```

Diagnóstico: `plt.show()` consume y cierra la figura activa al cerrarse la ventana emergente; la llamada posterior a `plt.savefig()` instancia silenciosamente una figura nueva vacía. Solución: invocar siempre `fig.savefig(...)` **antes** de `plt.show()` (o prescindir de `plt.show()` en flujos automatizados).

3. **Truncar el eje Y en un gráfico de barras exagerando diferencias marginales.** Llamar a `ax.set_ylim(2900, 3050)` sobre un `sns.barplot` hace que un valor de `3000` parezca visualmente diez veces mayor que `2910`. Si se requiere hacer foco en variaciones estrechas lejos del cero, debe emplearse un gráfico de puntos (`sns.pointplot` o `sns.scatterplot`) en lugar de barras rellenas.

4. **Usar gráficos de líneas sobre categorías nominales no ordenadas.** Unir con una línea continua `"Trabajo fijo"`, `"Freelance"` y `"Cripto"` sugiere falsamente una trayectoria intermedia entre categorías discretas; para variables nominales corresponden barras (`sns.barplot`).

## 9. Resumen

- **Matplotlib** y **Seaborn** son bibliotecas externas de terceros: Matplotlib suministra la jerarquía de objetos `Figure` y `Axes`, mientras que Seaborn construye abstracciones estadísticas declarativas directamente sobre `DataFrame` de Pandas.
- Cada gráfico responde a una estructura de datos distinta: `sns.lineplot` para evolución secuencial o temporal, `sns.barplot` (con base obligatoria en `0`) para comparación de categorías, `sns.scatterplot` para relación conjunta entre dos variables numéricas y `sns.boxplot` para comparar mediana, rango intercuartílico ($\text{IQR}$) y valores atípicos.
- Para código modular, multipanel y mantenible debe preferirse la API explícita orientada a objetos (`fig, ax = plt.subplots()`, pasando `ax=ax` a Seaborn) frente a la interfaz implícita de estado global `plt.*`.
- En entornos de producción sin pantalla se configura el *backend* `Agg`, se exporta mediante `fig.savefig(..., dpi=300, bbox_inches="tight")` antes de cualquier visualización interactiva y se cierra obligatoriamente la figura con `plt.close(fig)`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_lineal.py` (L1-29) | `grafico_lineal.py` | Importación de `pandas`, `matplotlib.pyplot` y `seaborn`; `sns.lineplot(x="fecha", y="comidas", data=df)`, marcador `plt.plot("01-03", 17, "o")` y `plt.show()` | Se sustituyó el punto fijo literal por cálculo dinámico con `idxmax()` y se migró de `plt.*` global a `fig, ax = plt.subplots()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_lineal.csv` (L1-16) | `grafico_lineal.csv` | Serie de 15 registros diarios con pico máximo (`17` en `"01-03"`) | Analizado como caso canónico de dominio secuencial ordenado |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_barras.py` (L1-32) | `grafico_barras.py` | Gráfico categórico `sns.barplot(x="fuente", y="ingresos", data=df)` complementado con `df["ingresos"].sum()` | Se añadieron criterios de ordenamiento descendente, base cero obligatoria, parámetro moderno `errorbar=None` y rotación de etiquetas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_barras.csv` (L1-6) | `grafico_barras.csv` | Cinco fuentes de ingreso que totalizan `4900` USD | Integrado en un lienzo multipanel calculando participación relativa (`61.22%`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_de_dispersion.py` (L1-27) | `grafico_de_dispersion.py` | Gráfico bivariado `sns.scatterplot(x="tiempo", y="dinero", data=df)` | Se corrigió la nota interna copiada en L15 ("gráfico de barras") y se explicó la lectura de correlación y detección de anomalías |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_de_dispersion.csv` (L1-11) | `grafico_de_dispersion.csv` | Diez pares `(tiempo, dinero)` con tendencia creciente y punto atípico `(94, 192)` | Empleado para ilustrar el diagnóstico visual y programático de valores extremos bivariados |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_de_bigotes.py` (L1-28) | `grafico_de_bigotes.py` | Diagrama `sns.boxplot(x="categoría", y="valor", data=df)` | Se corrigieron los comentarios copiados de `barplot` (L15-21) y se desarrolló formalmente el significado de cuartiles, $\text{IQR}$ y vallas de Tukey |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_de_bigotes.csv` (L1-6) | `grafico_de_bigotes.csv` | Cinco observaciones divididas en categorías `A` y `B` | Se advirtió además sobre la interpretación cautelosa de `boxplot` en tamaños muestrales muy reducidos |

**Fundamento complementario:** se añadieron cinco pilares técnicos fundamentales para trabajar con visualización en entornos reales: (1) la distinción explícita de Matplotlib y Seaborn como bibliotecas externas y su jerarquía interna `Figure` → `Axes` → `Artist`; (2) el contraste entre la máquina de estados `pyplot` y la API orientada a objetos `plt.subplots()`; (3) la formulación matemática del rango intercuartílico y las vallas de Tukey ($1.5 \times \text{IQR}$) en diagramas de caja; (4) el renderizado sin pantalla mediante el *backend* `Agg` y `fig.savefig(..., dpi=300, bbox_inches="tight")`; y (5) la prevención de fugas de memoria y problemas de concurrencia cerrando explícitamente cada figura con `plt.close(fig)`.

## 11. Referencias oficiales

- <https://matplotlib.org/stable/users/index.html> — Guía oficial de usuario de Matplotlib: arquitectura `Figure`/`Axes`, interfaces explícita (`subplots`) e implícita (`pyplot`), y formatos de salida.
- <https://matplotlib.org/stable/users/explain/figure/backends.html> — Documentación oficial de Matplotlib (*Backends*): uso de motores interactivos frente a motores sin pantalla como `Agg`.
- <https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html> — Referencia de API (`Figure.savefig`): parámetros `dpi`, `bbox_inches="tight"` y escritura en flujos binarios.
- <https://seaborn.pydata.org/tutorial/introduction.html> — Introducción oficial a Seaborn: integración con `pandas.DataFrame`, codificación visual semántica y funciones a nivel de ejes.
- <https://seaborn.pydata.org/tutorial/function_overview.html> — Guía de arquitectura de funciones en Seaborn: funciones a nivel de ejes (`ax=`) frente a nivel de figura.
