# Fundamentos de Seaborn: Visualización Estadística Declarativa en Python

Seaborn es una biblioteca de visualización de datos construida sobre Matplotlib y estrechamente integrada con las estructuras de datos tabulares de Pandas.

## 2. Introducción

Mientras Matplotlib se diseñó como un motor imperativo y de bajo nivel inspirado en MATLAB donde cada línea, marca y rectángulo debe configurarse explícitamente, Seaborn introduce una capa de abstracción orientada a la estadística exploratoria y descriptiva.

Desarrollada por Michael Waskom, Seaborn permite responder preguntas analíticas complejas mediante una sintaxis declarativa de alto nivel: en lugar de programar bucles para agrupar datos, calcular intervalos de confianza o asignar paletas de colores por categoría, se declaran los roles semánticos de las variables (`x`, `y`, `hue`, `col`, `row`) y Seaborn realiza las transformaciones estadísticas y el mapeo estético automáticamente.

## 3. Fundamentos y conceptos

Para comprender y dominar Seaborn es indispensable entender sus dos niveles de funciones:
1. **Funciones a nivel de ejes (Axes-level functions):**
   - Operan sobre un objeto `matplotlib.axes.Axes` individual.
   - Retornan dicho objeto `Axes`.
   - Aceptan el parámetro `ax` explícito, lo que permite incrustarlas limpiamente en cualquier cuadrícula prediseñada con `plt.subplots()`.
   - Ejemplos: `sns.histplot()`, `sns.scatterplot()`, `sns.barplot()`, `sns.boxplot()`, `sns.kdeplot()`.
2. **Funciones a nivel de figura (Figure-level functions):**
   - Controlan y orquestan la figura completa de Matplotlib mediante un objeto contenedor especializado (como `FacetGrid` o `JointGrid`).
   - Retornan el contenedor de facetas (`FacetGrid`, `JointGrid`, `PairGrid`), no un `Axes`.
   - Manejan automáticamente la creación de múltiples subplots divididos por columnas y filas según categorías (`col='categoria'`, `row='region'`).
   - Ejemplos: `sns.displot()`, `sns.relplot()`, `sns.catplot()`, `sns.pairplot()`.

Adicionalmente, Seaborn asume por defecto el paradigma de datos limpios o "Tidy Data" (formato largo o long-form), donde cada fila es una observación y cada columna es una variable.

## 4. Sintaxis y funcionamiento

El patrón moderno en Seaborn v0.12+ consiste en pasar el DataFrame completo en `data=` y especificar los nombres de las columnas en los argumentos estéticos:

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "edad": [23, 45, 31, 35, 40],
    "salario": [3000, 5200, 4100, 4300, 4800],
    "departamento": ["IT", "Ventas", "IT", "RRHH", "Ventas"]
})

fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=df, x="edad", y="salario", hue="departamento", ax=ax)
ax.set_title("Relación Salario vs Edad")
plt.close(fig)
```

## 5. Ejemplos prácticos progresivos

### Básico

Generación de un gráfico de dispersión a nivel de ejes integrando Pandas y personalización con Matplotlib.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "experiencia": [1, 2, 3, 5, 8, 10],
    "salario_k": [35, 42, 48, 65, 90, 115]
})

fig, ax = plt.subplots()
ax_retornado = sns.scatterplot(data=df, x="experiencia", y="salario_k", ax=ax)

print(f"Tipo del objeto retornado: {type(ax_retornado).__name__}")
print(f"Puntos trazados: {len(ax.collections[0].get_offsets())}")
plt.close(fig)
```

**Salida real:**

```text
Tipo del objeto retornado: Axes
Puntos trazados: 6
```

### Intermedio

Estimación de densidad no paramétrica multivariada con agrupación semántica de color (`hue`).

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "tiempo_respuesta": [120, 130, 125, 210, 230, 220, 115, 240],
    "cluster": ["A", "A", "A", "B", "B", "B", "A", "B"]
})

fig, ax = plt.subplots(figsize=(7, 3))
sns.kdeplot(data=df, x="tiempo_respuesta", hue="cluster", fill=True, common_norm=False, ax=ax)
ax.set_title("Distribución de Latencias por Cluster")

print(f"Cantidad de curvas KDE generadas: {len(ax.lines)}")
plt.close(fig)
```

**Salida real:**

```text
Cantidad de curvas KDE generadas: 2
```

### Avanzado

Construcción de matriz de correlación anotada con mapa de calor (`heatmap`) y máscara triangular superior para evitar redundancia analítica.

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "ventas": [100, 120, 140, 160],
    "marketing": [20, 25, 35, 40],
    "retencion": [0.85, 0.88, 0.90, 0.94]
})

corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, ax=ax)
ax.set_title("Matriz de Correlación Triangular")

print(f"Dimensiones de la matriz evaluada: {corr.shape}")
plt.close(fig)
```

**Salida real:**

```text
Dimensiones de la matriz evaluada: (3, 3)
```

## 6. Aplicaciones en el mundo real

- **Análisis exploratorio de datos (EDA):** Detección expedita de correlaciones, valores atípicos y bimodalidad previa al entrenamiento de modelos de Machine Learning.
- **Validación de hipótesis A/B Testing:** Comparación de métricas de conversión entre variantes utilizando diagramas de caja y estimaciones con intervalos de confianza bootstrappeados.
- **Bioinformática y Genómica:** Visualización de microarrays de expresión génica mediante mapas de calor jerárquicos agrupados por similitud euclidiana.

## 7. Uso en producción

- **Control del backend en contenedores:** Seaborn depende de Matplotlib, por lo que en servidores desprovistos de interfaz gráfica (servidores Linux, tareas Celery, contenedores Docker) debe garantizarse el uso del backend `'Agg'`.
- **Paletas aptas para personas daltónicas:** Usar siempre paletas accesibles como `palette='colorblind'` o esquemas viridis/magma para reportes públicos o auditables.
- **Rendimiento con Big Data:** Métodos con cálculo de intervalos de confianza (`ci=95` o `errorbar`) ejecutan remuestreo bootstrap intensivo en CPU. En DataFrames con millones de registros, deshabilitar el remuestreo (`errorbar=None`) o preagregar los datos con Pandas.

## 8. Errores comunes y recomendaciones

- **Intentar pasar `ax` a funciones a nivel de figura:** `sns.pairplot(..., ax=ax)` falla porque `pairplot` administra su propia figura (`PairGrid`). Pasar `ax` únicamente a funciones a nivel de ejes (`sns.heatmap`, `sns.histplot`, etc.).
- **Datos en formato ancho (wide-form) no compatibles:** Intentar usar `hue` con datos anchos genera errores. Transformar siempre los datos con `pd.melt()` a formato largo antes de graficar.
- **Olvidar cerrar la figura:** Al igual que en Matplotlib, no invocar `plt.close(fig)` provoca acumulación de figuras en memoria en microservicios.

## 9. Resumen

Seaborn optimiza el flujo de análisis visual reduciendo decenas de líneas imperativas de Matplotlib a declaraciones compactas centradas en los datos. Dominar la distinción entre funciones a nivel de ejes y a nivel de figura, el formato Tidy Data y el control de estimaciones estadísticas permite construir análisis visuales rigurosos, estéticos y reproducibles.

## 10. Referencias oficiales

- Documentación oficial de Seaborn: https://seaborn.pydata.org/
- Guía de funciones Axes-level vs Figure-level: https://seaborn.pydata.org/tutorial/function_overview.html
- Referencia de la API de Seaborn: https://seaborn.pydata.org/api.html
