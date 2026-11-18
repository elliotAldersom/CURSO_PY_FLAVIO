# Scikit-learn: KMeans

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.cluster.KMeans(n_clusters=8, *, init='k-means++', n_init='auto', max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='lloyd')
```

## 2. ¿Qué es?

`KMeans` es el algoritmo no supervisado por excelencia para particionar $N$ observaciones en $K$ clusters disjuntos donde cada muestra pertenece al grupo con el centroide más cercano.

## 3. ¿Para qué sirve?

Fundamental para segmentación de clientes, compresión de imágenes, detección de patrones no etiquetados y preprocesamiento de características espaciales.

## 4. ¿Cómo funciona?

Minimiza la inercia (suma de distancias euclidianas al cuadrado al centroide más próximo) alternando dos pasos: (1) Asignar cada punto al centroide más cercano y (2) Recalcular los centroides como el promedio vectorial de los puntos asignados. Inicializa inteligentemente con `init='k-means++'` para garantizar convergencia rápida.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `n_clusters` | `int` | Opcional | `8` | Número de clusters $K$ a generar. |
| `init` | `'k-means++'`, `'random'`, `ndarray` | Opcional | `'k-means++'` | Estrategia de selección inicial de centroides. |
| `n_init` | `'auto'`, `int` | Opcional | `'auto'` | Cantidad de ejecuciones con diferentes centroides iniciales. |
| `max_iter` | `int` | Opcional | `300` | Número máximo de iteraciones por ejecución. |
| `random_state` | `int` | Opcional | `None` | Semilla para convergencia determinista. |

## 6. Retorno

`KMeans`. Instancia del estimador no supervisado con centroides calculados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1.0, 1.0], [1.5, 1.2], [8.0, 8.0], [8.5, 8.2]])
kmeans = KMeans(n_clusters=2, random_state=42, n_init=5)
kmeans.fit(X)

print(f"Etiquetas asignadas: {kmeans.labels_.tolist()}")
print(f"Coordenadas de centroides: {[list(map(lambda v: round(v, 2), c)) for c in kmeans.cluster_centers_.tolist()]}")
```

**Salida real:**

```text
Etiquetas asignadas: [1, 1, 0, 0]
Coordenadas de centroides: [[8.25, 8.1], [1.25, 1.1]]
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.cluster import KMeans

X_train = np.array([[1, 2], [2, 3], [10, 11], [11, 12]])
kmeans = KMeans(n_clusters=2, random_state=42, n_init=5)
kmeans.fit(X_train)

# Inferencia de cluster sobre nuevos puntos no vistos
nuevos = np.array([[1.5, 2.5], [9.5, 10.5]])
clusters_pred = kmeans.predict(nuevos)

print(f"Clusters para nuevos datos: {clusters_pred.tolist()}")
```

**Salida real:**

```text
Clusters para nuevos datos: [1, 0]
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# Inercia (Within-Cluster Sum of Squares) para el método del codo
kmeans = KMeans(n_clusters=2, random_state=42, n_init=5)
kmeans.fit(X)

print(f"Inercia del agrupamiento: {float(kmeans.inertia_):.2f}")
```

**Salida real:**

```text
Inercia del agrupamiento: 16.00
```

## 8. Errores frecuentes y casos borde

- **No escalar los datos previamente:** KMeans se basa en distancias euclidianas. Si una variable está en miles y otra en decimales, la primera dominará el 99% del cálculo de distancia. Escalar SIEMPRE con `StandardScaler`.
- **Clusters no esféricos:** KMeans asume clusters esféricos e isotrópicos de tamaño similar; falla ante geometrías alargadas o densidades dispares (preferir `DBSCAN` o `GaussianMixture`).

## 9. Buenas prácticas y rendimiento

- Determinar el número óptimo de clusters $K$ mediante el método del codo graficando `kmeans.inertia_` o calculando el puntaje de silueta (`silhouette_score`).
- Usar `init='k-means++'` para evitar óptimos locales deficientes.

## 10. Métodos relacionados

- [standard_scaler](../01_preprocesamiento/standard_scaler.md)
- [pipeline](../05_pipelines/pipeline.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
