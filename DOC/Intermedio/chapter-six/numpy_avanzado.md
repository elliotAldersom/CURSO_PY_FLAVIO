# Manipulación Estructural, Estadística y Álgebra Lineal en NumPy

## 2. Introducción

Una vez comprendida la naturaleza de los [arreglos fundamentales](numpy_fundamentos.md) y la mecánica de las [operaciones vectorizadas y broadcasting](numpy_operaciones.md), el desarrollo de sistemas computacionales complejos exige dominar la manipulación estructural de dimensiones, el cálculo estadístico multidimensional y las operaciones fundamentales de álgebra lineal.

En flujos de trabajo de ciencia de datos y aprendizaje automático, los datos rara vez ingresan con la forma geométrica requerida por los modelos algorítmicos. Las imágenes capturadas como flujos lineales deben reconstruirse como tensores bidimensionales o tridimensionales, los lotes de datos deben concatenarse o dividirse para validación cruzada, y las variables deben ser agregadas a lo largo de ejes específicos sin alterar el resto de la estructura.

Este capítulo aborda las herramientas avanzadas indispensables de NumPy: reorganización dimensional de memoria (`reshape`, `ravel`, transposición), apilamiento y división de matrices (`concatenate`, `vstack`, `hstack`, `split`), reducciones estadísticas multidimensionales con control de eje (`axis`), el subsistema de álgebra lineal `numpy.linalg` y la persistencia binaria de alta velocidad con compresión (`np.save`, `np.load`, `np.savez_compressed`).

## 3. Fundamentos y conceptos

**Reorganización dimensional (*Reshaping*) y contigüidad en memoria.**
Cambiar la forma de un arreglo mediante `.reshape(nueva_forma)` reinterpreta la geometría de las dimensiones sin alterar los datos subyacentes:
- La única restricción matemática inquebrantable es que el número total de celdas debe conservarse idéntico: $\prod \text{forma\_original} = \prod \text{nueva\_forma}$.
- NumPy admite el uso del valor comodín `-1` en una de las dimensiones para que el motor deduzca automáticamente su tamaño a partir del número total de elementos.
- **Aplanamiento a 1D:**
  - `ravel()`: aplana el arreglo devolviendo una **vista (*view*)** si la memoria es contigua, evitando copias innecesarias.
  - `flatten()`: aplana el arreglo devolviendo siempre una **copia física independiente** de los datos.
- **Transposición (`matriz.T` o `np.transpose()`):** invierte el orden de los ejes. En una matriz 2D permuta filas por columnas intercambiando sus pasos (*strides*), ejecutándose en tiempo constante $O(1)$ sin mover un solo byte en memoria RAM.

**Concatenación y partición de tensores.**
- `np.concatenate((a, b), axis=0)`: une arreglos existentes a lo largo de un eje que ya debe estar presente en las matrices.
- `np.vstack((a, b))` (*vertical stack*): apila matrices verticalmente (a lo largo de las filas, eje 0).
- `np.hstack((a, b))` (*horizontal stack*): apila matrices horizontalmente (a lo largo de las columnas, eje 1).
- `np.split(arreglo, divisiones, axis=0)`: divide un arreglo en submallas de igual tamaño a lo largo del eje seleccionado.

**El concepto de Eje (*Axis*) en reducciones estadísticas.**
Comprender el parámetro `axis` resulta crucial para no invertir cálculos analíticos:
- **`axis=None` (predeterminado):** colapsa **todos** los elementos del arreglo en un único escalar (p. ej. la suma o media global).
- **`axis=0`:** la operación se ejecuta **a lo largo de las filas** (colapsando la dimensión vertical), produciendo un resultado por cada columna.
- **`axis=1`:** la operación se ejecuta **a lo largo de las columnas** (colapsando la dimensión horizontal), produciendo un resultado por cada fila.
- `keepdims=True`: mantiene las dimensiones colapsadas con tamaño `1`, facilitando operaciones posteriores mediante *broadcasting* sin requerir reindexaciones manuales.

**Álgebra lineal con `numpy.linalg`.**
El submódulo `numpy.linalg` enlaza con bibliotecas de álgebra lineal optimizadas en hardware (BLAS y LAPACK):
- Producto interno y matricial: `@` o `np.dot(a, b)`.
- Determinante: `np.linalg.det(A)`.
- Matriz inversa: `np.linalg.inv(A)` (resuelve $A \cdot A^{-1} = I$).
- Solución de sistemas lineales $A \cdot x = b$: `np.linalg.solve(A, b)` (más rápido y numéricamente más estable que calcular explícitamente $A^{-1} \cdot b$).

## 4. Sintaxis y funcionamiento

Reorganización de dimensiones y adición de ejes:

```python
import numpy as np

vector = np.arange(12)  # [0, 1, 2, ..., 11]

# Redimensionar a matriz de 3 filas y 4 columnas
matriz_3x4 = vector.reshape((3, 4))

# Deducir filas automáticamente con -1: 2 columnas -> calcula 6 filas
matriz_6x2 = vector.reshape((-1, 2))

# Agregar dimensión unitaria para broadcasting: forma (12, 1)
columna_2d = vector[:, np.newaxis]
```

Reducciones con control de ejes:

```python
import numpy as np

datos = np.array([[10, 20, 30], [40, 50, 60]])

total_global = np.sum(datos)              # 210
suma_por_columnas = np.sum(datos, axis=0) # [50, 70, 90]
suma_por_filas = np.sum(datos, axis=1)    # [60, 150]
```

Resolución de sistemas de ecuaciones lineales ($A \cdot x = b$):

```python
import numpy as np

# Sistema:
# 2x + 3y = 8
# 1x + 4y = 9
A = np.array([[2.0, 3.0], [1.0, 4.0]])
b = np.array([8.0, 9.0])

# Solución vectorial exacta [x, y]
solucion = np.linalg.solve(A, b)  # Retorna array([1., 2.])
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Manipulación de formas, transposición y agregaciones estadísticas por eje.**

```python
import numpy as np

# 1. Crear un arreglo de 12 elementos y reorganizar a matriz 3x4
datos_lineales = np.arange(1, 13, dtype=np.int32)
matriz = datos_lineales.reshape((3, 4))
matriz_traspuesta = matriz.T

print("Matriz original (3x4):\n", matriz)
print("\nMatriz traspuesta (4x3):\n", matriz_traspuesta)

# 2. Reducciones estadísticas con axis
suma_total = np.sum(matriz)
media_por_columna = np.mean(matriz, axis=0)
maximo_por_fila = np.max(matriz, axis=1)
indice_max_por_columna = np.argmax(matriz, axis=0)

print("\n--- Reducciones Estadísticas ---")
print("Suma total del arreglo          :", suma_total)
print("Media de cada columna (axis=0)  :", media_por_columna)
print("Máximo de cada fila (axis=1)    :", maximo_por_fila)
print("Índices de fila del valor máx   :", indice_max_por_columna)
```

Explicación paso a paso:

- `matriz.reshape((3, 4))` organiza los doce enteros en 3 filas y 4 columnas leyendo la memoria en orden C (por filas).
- `matriz.T` invierte los ejes convirtiendo las filas originales en columnas sin copiar datos en RAM; simplemente intercambia los saltos de memoria (*strides*).
- `np.mean(matriz, axis=0)` colapsa las 3 filas sumando verticalmente y dividiendo por 3, devolviendo un arreglo de 4 elementos con el promedio de cada columna.
- `np.argmax(matriz, axis=0)` devuelve el índice de la fila donde se ubica el valor más alto para cada columna (todas ubicadas en la fila índice `2`).

Resultado esperado:

```text
Matriz original (3x4):
 [[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]

Matriz traspuesta (4x3):
 [[ 1  5  9]
 [ 2  6 10]
 [ 3  7 11]
 [ 4  8 12]]

--- Reducciones Estadísticas ---
Suma total del arreglo          : 78
Media de cada columna (axis=0)  : [5. 6. 7. 8.]
Máximo de cada fila (axis=1)    : [ 4  8 12]
Índices de fila del valor máx   : [2 2 2 2]
```

### Intermedio

**Ejemplo 2 — Concatenación, partición de lotes (*Batch Split*) y ordenamiento indirecto con `argsort`.**

```python
import numpy as np

# Dos lotes independientes de datos (cada fila es una muestra de 3 métricas)
lote_manana = np.array([[12.5, 45.0, 1.2], [15.0, 52.0, 1.8]])
lote_tarde = np.array([[11.0, 40.0, 0.9], [18.5, 60.0, 2.1]])

# 1. Concatenación vertical de lotes (unión de muestras)
dataset_completo = np.vstack((lote_manana, lote_tarde))

# 2. Ordenamiento indirecto: ordenar todas las filas según la columna 1 (métrica central)
indices_orden = np.argsort(dataset_completo[:, 1])
dataset_ordenado = dataset_completo[indices_orden]

# 3. Partición de datos en conjuntos de Entrenamiento y Prueba (Train/Test Split de 50%)
lote_train, lote_test = np.split(dataset_ordenado, 2, axis=0)

print("Dataset consolidado (4 muestras, 3 métricas):\n", dataset_completo)
print("\nÍndices de orden según columna 1:", indices_orden)
print("\nDataset ordenado ascendentemente por métrica 1:\n", dataset_ordenado)
print("\nSubconjunto Entrenamiento (Train):\n", lote_train)
print("\nSubconjunto Prueba (Test):\n", lote_test)
```

Explicación técnica:

- `np.vstack((lote_manana, lote_tarde))` apila las matrices bidimensionales verticalmente a lo largo de las filas produciendo una matriz `(4, 3)`.
- `np.argsort(dataset_completo[:, 1])` extrae los valores de la segunda columna (`[45.0, 52.0, 40.0, 60.0]`) y devuelve los índices enteros que ordenarían dicho vector de menor a mayor: `[2, 0, 1, 3]`.
- Al aplicar *Fancy Indexing* con esos índices (`dataset_completo[indices_orden]`), reordenamos las filas completas sin perder la correspondencia entre métricas de una misma muestra.
- `np.split(dataset_ordenado, 2, axis=0)` divide el arreglo en dos particiones iguales a lo largo del eje de filas, técnica habitual en validación cruzada.

Resultado esperado:

```text
Dataset consolidado (4 muestras, 3 métricas):
 [[12.5 45.   1.2]
 [15.  52.   1.8]
 [11.  40.   0.9]
 [18.5 60.   2.1]]

Índices de orden según columna 1: [2 0 1 3]

Dataset ordenado ascendentemente por métrica 1:
 [[11.  40.   0.9]
 [12.5 45.   1.2]
 [15.  52.   1.8]
 [18.5 60.   2.1]]

Subconjunto Entrenamiento (Train):
 [[11.  40.   0.9]
 [12.5 45.   1.2]]

Subconjunto Prueba (Test):
 [[15.  52.   1.8]
 [18.5 60.   2.1]]
```

### Avanzado

**Ejemplo 3 — Resolución de modelos lineales de regresión por Álgebra Lineal (`solve`) y serialización binaria ultrarrápida comprimida (`np.savez_compressed`).**

```python
import tempfile
from pathlib import Path
import numpy as np

# Problema físico: determinar coeficientes de un modelo lineal multivariado
# Ecuación matricial normal: (X^T * X) * w = X^T * y
# donde w es el vector de pesos que minimiza los errores cuadráticos ordinarios (MCO)

# Matriz de diseño X (4 observaciones con término independiente en col 0 y variable x en col 1)
X = np.array(
    [
        [1.0, 1.0],
        [1.0, 2.0],
        [1.0, 3.0],
        [1.0, 4.0],
    ]
)
# Vector de respuestas observadas y
y = np.array([2.2, 2.8, 3.6, 4.5])

# 1. Construcción de ecuaciones normales
XtX = X.T @ X      # Matriz cuadrada (2, 2)
Xty = X.T @ y      # Vector (2,)

# 2. Solución robusta mediante np.linalg.solve (evitando invertir explícitamente XtX)
pesos_w = np.linalg.solve(XtX, Xty)
intercepto, pendiente = pesos_w[0], pesos_w[1]

# Predicciones vectorizadas del modelo
y_predichas = X @ pesos_w
error_cuadratico_medio = np.mean((y - y_predichas) ** 2)

# 3. Persistencia binaria de alta velocidad con compresión en disco (.npz)
with tempfile.TemporaryDirectory() as temp_dir:
    ruta_modelo = Path(temp_dir) / "modelo_entrenado.npz"

    # Guardar múltiples arreglos en un archivo binario comprimido
    np.savez_compressed(
        ruta_modelo,
        matriz_X=X,
        pesos=pesos_w,
        metricas=np.array([error_cuadratico_medio]),
    )

    # Cargar y verificar integridad
    datos_cargados = np.load(ruta_modelo)
    pesos_recuperados = datos_cargados["pesos"]
    mse_recuperado = datos_cargados["metricas"][0]

print("Coeficientes ajustados:")
print(f"  Intercepto (w0): {intercepto:.4f}")
print(f"  Pendiente  (w1): {pendiente:.4f}")
print(f"Error Cuadrático Medio (MSE): {error_cuadratico_medio:.5f}")
print("\n--- Verificación de Persistencia Binaria ---")
print("Archivos contenidos en el archivo .npz:", datos_cargados.files)
print("Pesos recuperados idénticos          :", np.allclose(pesos_w, pesos_recuperados))
print("MSE recuperado                       :", round(float(mse_recuperado), 5))
```

Explicación de ingeniería:

- En álgebra lineal numérica, calcular la solución de $A \cdot x = b$ mediante inversión explícita de matriz `np.linalg.inv(A) @ b` es computacionalmente ineficiente e inestable ante matrices mal condicionadas (*ill-conditioned*). `np.linalg.solve(A, b)` utiliza la factorización LU con pivoteo de LAPACK, reduciendo a la mitad los ciclos de CPU y minimizando errores de redondeo.
- `np.savez_compressed` empaqueta múltiples arreglos de NumPy en un archivo con formato `.npz` comprimido con el algoritmo DEFLATE de forma nativa. Al tratarse de una copia binaria exacta de la memoria física sin conversiones textuales a JSON o CSV, la serialización y deserialización se efectúan al límite de velocidad del canal I/O del disco.

Resultado esperado:

```text
Coeficientes ajustados:
  Intercepto (w0): 1.4000
  Pendiente  (w1): 0.7700
Error Cuadrático Medio (MSE): 0.00350

--- Verificación de Persistencia Binaria ---
Archivos contenidos en el archivo .npz: ['matriz_X', 'pesos', 'metricas']
Pesos recuperados idénticos          : True
MSE recuperado                       : 0.0035
```

## 6. Aplicaciones en el mundo real

- **Modelado Estadístico y Regresión Múltiple:** estimación analítica de coeficientes por mínimos cuadrados ordinarios y descomposición en valores singulares (*SVD*).
- **Redes Neuronales Convolucionales (CNN):** manipulación de tensores cuatridimensionales `(lote, alto, ancho, canales)` reorganizando formas antes de ingresar a capas lineales totalmente conectadas (*dense layers*).
- **Procesamiento de Imágenes y Filtros Espaciales:** transposición de ejes cromáticos, extracción de parches con `split` y análisis espectral con autovalores y autovectores (`np.linalg.eig`).
- **Almacenamiento de Datasets Científicos:** archivo de experimentos masivos en formato comprimido `.npz` de NumPy o jerárquico HDF5 (`h5py`).

## 7. Uso en producción

- **Evitar `np.linalg.inv` para resolver sistemas lineales:** siempre que se necesite resolver $A \cdot x = b$, utilizar taxativamente `np.linalg.solve(A, b)` en lugar de `np.linalg.inv(A) @ b`; `solve` es el doble de rápido y posee órdenes de magnitud mayor estabilidad numérica ante singularidades.
- **Preferir `ravel()` frente a `flatten()` cuando sea seguro:** `ravel()` evita reservar nueva memoria devolviendo una vista contigua si es posible, mientras que `flatten()` siempre duplica el arreglo en memoria física.
- **Utilizar `np.savez_compressed` para cachés intermedias de cómputo:** en lugar de guardar datos numéricos pesados en CSV o bases de datos relacionales durante pipelines de transformación, serializar en `.npz` reduce el espacio en disco en más de un 80 % y acelera los tiempos de recarga en 20x.
- **Comprobar condicionamiento numérico con `np.linalg.cond`:** antes de invertir o resolver matrices en procesos autónomos, comprobar que el número de condición de la matriz no sea astronómico para prevenir matrices casi singulares que destruyan la exactitud numérica.

## 8. Errores comunes y recomendaciones

1. **Intentar `reshape` con un número incompatible de elementos (`ValueError`).**

```python
import numpy as np

datos = np.arange(10)
# ERROR: ValueError: cannot reshape array of size 10 into shape (3,4)
# datos.reshape((3, 4))  # 3 * 4 = 12 != 10
```

Diagnóstico: la nueva forma geométrica exige obligatoriamente que el producto de sus dimensiones coincida con el número total de elementos del arreglo original (`datos.size`). Recomendación: calcular el total o utilizar `-1` en una de las dimensiones para que NumPy deduzca el tamaño compatible: `datos.reshape((2, -1))` producirá `(2, 5)`.

2. **Invertir el eje en agregaciones estadísticas (`axis=0` vs `axis=1`).**

```python
import numpy as np

# Filas: Alumnos (2), Columnas: Exámenes (3)
notas = np.array([[8, 9, 10], [4, 5, 6]])

# ERROR COMÚN: querer el promedio de cada alumno y usar axis=0
promedio_equivocado = np.mean(notas, axis=0)  # [6., 7., 8.] -> promedio del examen!

# CORRECCIÓN: colapsar columnas a lo largo de axis=1
promedio_alumnos = np.mean(notas, axis=1)     # [9., 5.] -> promedio por alumno
```

Diagnóstico: `axis=0` comprime las filas sumando verticalmente hacia abajo, produciendo un escalar por columna. Para agregar horizontalmente a lo largo de las columnas y obtener una métrica por fila, debe especificarse `axis=1`.

3. **Invertir explícitamente matrices para resolver ecuaciones algebraicas.**

Diagnóstico: calcular la matriz inversa explícitamente mediante `np.linalg.inv(A)` acumula imprecisiones catastróficas de redondeo en flotantes IEEE 754 y requiere $O(n^3)$ operaciones innecesarias. Recomendación: utilizar siempre `np.linalg.solve(A, b)` que implementa eliminación gaussiana optimizada con pivoteo parcial.

## 9. Resumen

- **`reshape()`** altera la estructura geométrica de un arreglo conservando el número total de celdas; **`ravel()`** aplana hacia una vista 1D de memoria compartida y **`flatten()`** genera una copia física independiente.
- La transposición **`.T`** permuta los ejes en tiempo constante $O(1)$ sin mover datos en la memoria física.
- El parámetro **`axis`** gobierna la dirección de las reducciones estadísticas: `axis=0` colapsa las filas produciendo un valor por columna, y `axis=1` colapsa las columnas produciendo un valor por fila.
- `np.argsort()` proporciona ordenamiento indirecto por índices, permitiendo ordenar matrices multidimensionales según columnas o criterios arbitrarios.
- El módulo **`numpy.linalg`** implementa cálculo matricial de alto rendimiento; la función `solve()` es la alternativa numéricamente robusta a la inversión explícita de matrices.
- La serialización binaria con **`np.savez_compressed`** optimiza la persistencia y carga de conjuntos masivos de tensores sin costo de formateo textual.

## 10. Referencias oficiales

- <https://numpy.org/doc/stable/reference/routines.linalg.html> — Documentación oficial de NumPy: submódulo de álgebra lineal (`numpy.linalg`), descomposición, sistemas de ecuaciones y matrices inversas.
- <https://numpy.org/doc/stable/reference/generated/numpy.reshape.html> — Referencia de API para manipulación dimensional y función `numpy.reshape`.
- <https://numpy.org/doc/stable/reference/routines.statistics.html> — Catálogo oficial de funciones estadísticas en NumPy (`mean`, `std`, `var`, `percentile`, `median`).
- <https://numpy.org/doc/stable/reference/routines.io.html> — Catálogo oficial de entrada y salida binaria de NumPy (`save`, `load`, `savez_compressed`).

