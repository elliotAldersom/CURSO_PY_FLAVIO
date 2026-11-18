# Documentación Técnica de Métodos y Funciones de NumPy

Biblioteca exhaustiva de métodos, funciones y atributos de **NumPy 2.x**, estructurada según los estándares más rigurosos de computación científica y arquitectura de software.

Cada documento es **completamente autónomo**, incluye la firma oficial de la API en NumPy 2.x, análisis de memoria física y vistas, tabla exhaustiva de parámetros, tres niveles de ejemplos prácticos con salidas reales y referencias oficiales.

---

## Índice Temático por Categorías

### 1. Creación de Arreglos
* [Índice de Creación de Arreglos](01_creacion_arreglos/indice.md)
  * [`array`](01_creacion_arreglos/array.md) — Conversión a `ndarray` contiguo.
  * [`arange`](01_creacion_arreglos/arange.md) — Secuencias continuas.
  * [`linspace`](01_creacion_arreglos/linspace.md) — Muestras lineales equiespaciadas.
  * [`zeros`](01_creacion_arreglos/zeros.md) — Inicialización a cero.
  * [`ones`](01_creacion_arreglos/ones.md) — Inicialización a unos.
  * [`full`](01_creacion_arreglos/full.md) — Relleno constante.
  * [`eye`](01_creacion_arreglos/eye.md) — Matriz identidad 2D.

### 2. Propiedades y Dimensiones
* [Índice de Propiedades y Dimensiones](02_propiedades_dimensiones/indice.md)
  * [`shape`](02_propiedades_dimensiones/shape.md) — Tupla dimensional.
  * [`ndim`](02_propiedades_dimensiones/ndim.md) — Rango tensorial o cantidad de ejes.
  * [`dtype`](02_propiedades_dimensiones/dtype.md) — Formato físico de tipos en memoria.
  * [`size`](02_propiedades_dimensiones/size.md) — Cantidad total de elementos.
  * [`itemsize`](02_propiedades_dimensiones/itemsize.md) — Bytes por elemento.

### 3. Indexación y Slicing
* [Índice de Indexación y Slicing](03_indexacion_slicing/indice.md)
  * [`slicing_basico`](03_indexacion_slicing/slicing_basico.md) — Vistas de corte continuo.
  * [`indexacion_booleana`](03_indexacion_slicing/indexacion_booleana.md) — Filtrado condicional vectorizado.
  * [`fancy_indexing`](03_indexacion_slicing/fancy_indexing.md) — Selección por arreglos de enteros.

### 4. Manipulación de Formas
* [Índice de Manipulación de Formas](04_manipulacion_formas/indice.md)
  * [`reshape`](04_manipulacion_formas/reshape.md) — Reorganización dimensional sin mutación.
  * [`flatten`](04_manipulacion_formas/flatten.md) — Aplanado con copia obligatoria.
  * [`ravel`](04_manipulacion_formas/ravel.md) — Aplanado eficiente retornando vista.
  * [`transpose`](04_manipulacion_formas/transpose.md) — Permutación de ejes y transposición $A^T$.
  * [`squeeze`](04_manipulacion_formas/squeeze.md) — Eliminación de ejes unitarios redundantes.
  * [`expand_dims`](04_manipulacion_formas/expand_dims.md) — Inserción de nuevos ejes dimensionales.

### 5. Operaciones Vectorizadas
* [Índice de Operaciones Vectorizadas](05_operaciones_vectorizadas/indice.md)
  * [`broadcasting`](05_operaciones_vectorizadas/broadcasting.md) — Reglas matemáticas de difusión.
  * [`add`](05_operaciones_vectorizadas/add.md) — Suma elemento por elemento.
  * [`multiply`](05_operaciones_vectorizadas/multiply.md) — Producto de Hadamard.
  * [`power`](05_operaciones_vectorizadas/power.md) — Exponenciación elemento a elemento.

### 6. Estadística y Agregación
* [Índice de Estadística y Agregación](06_estadistica_agregacion/indice.md)
  * [`sum`](06_estadistica_agregacion/sum.md) — Sumatoria por ejes con soporte `keepdims`.
  * [`mean`](06_estadistica_agregacion/mean.md) — Media aritmética.
  * [`median`](06_estadistica_agregacion/median.md) — Mediana robusta.
  * [`std`](06_estadistica_agregacion/std.md) — Desviación estándar.
  * [`min_max`](06_estadistica_agregacion/min_max.md) — Cotas mínimas y máximas.
  * [`argmin_argmax`](06_estadistica_agregacion/argmin_argmax.md) — Índices posicionales de extremos.

### 7. Álgebra Lineal
* [Índice de Álgebra Lineal](07_algebra_lineal/indice.md)
  * [`dot`](07_algebra_lineal/dot.md) — Producto punto y multiplicación 2D.
  * [`matmul`](07_algebra_lineal/matmul.md) — Multiplicación matricial canónica `@`.
  * [`inv`](07_algebra_lineal/inv.md) — Matriz inversa multiplicativa.
  * [`det`](07_algebra_lineal/det.md) — Determinante escalar de matrices cuadradas.

### 8. Búsqueda y Ordenamiento
* [Índice de Búsqueda y Ordenamiento](08_busqueda_ordenamiento/indice.md)
  * [`where`](08_busqueda_ordenamiento/where.md) — Selección ternaria y localización condicional.
  * [`select`](08_busqueda_ordenamiento/select.md) — Evaluación condicional múltiple en cascada.
  * [`sort`](08_busqueda_ordenamiento/sort.md) — Ordenamiento rápido en C.
  * [`argsort`](08_busqueda_ordenamiento/argsort.md) — Ordenamiento indirecto de índices.
  * [`unique`](08_busqueda_ordenamiento/unique.md) — Deduplicación y codificación de frecuencias.
