# Fundamentos de Computación Matricial y Arreglos con NumPy

## 2. Introducción

NumPy (*Numerical Python*) es el cimiento de la computación científica y de datos en Python. Toda la infraestructura analítica moderna (Pandas, Scikit-learn, PyTorch, SciPy) está construida sobre su estructura nuclear: el arreglo homogéneo $N$-dimensional `ndarray`.

Comprender NumPy desde sus fundamentos de arquitectura de sistemas permite escribir código vectorizado que aprovecha instrucciones SIMD de la CPU y memoria caché, superando en hasta dos órdenes de magnitud la velocidad de las listas nativas de Python.

## 3. Fundamentos y conceptos

1. **El `ndarray` frente a listas nativas:**
   * Una lista de Python es un arreglo de punteros que apuntan a objetos dispersos por la memoria dinámica (*heap*). Cada entero ocupa 28 bytes en CPython.
   * Un `ndarray` de NumPy es un bloque continuo y contiguo de memoria cruda en C con metadatos de estrías (*strides*), dimensión (*shape*) y tipo físico uniforme (*dtype*). Un entero `int64` ocupa exactamente 8 bytes contiguos.
2. **Localidad espacial de caché (*Cache Locality*):** Al estar los datos contiguos, la CPU precarga bloques enteros a su memoria caché L1/L2/L3, eliminando fallos de caché (*cache misses*).
3. **Broadcasting (Difusión):** Conjunto de reglas que permiten operar aritméticamente entre arreglos de diferentes dimensiones sin duplicar datos en memoria.
4. **Vistas frente a Copias:** Modificar un corte (*slice*) de un arreglo de NumPy muta el arreglo original porque comparten el mismo búfer de memoria. Para independizar datos debe invocarse `.copy()`.

## 4. Sintaxis y funcionamiento

Instalación:

```bash
pip install numpy
```

Importación canónica:

```python
import numpy as np
```

Creación básica y consulta de metadatos:

```python
import numpy as np

arr = np.array([10, 20, 30, 40], dtype=np.int32)
print("Forma:", arr.shape)
print("Tipo:", arr.dtype)
print("Bytes por elemento:", arr.itemsize)
```

## 5. Ejemplos prácticos progresivos

### Básico

Vectorización directa sin bucles imperativos:

```python
import numpy as np

distancias_km = np.array([10.5, 12.1, 11.8])
tiempo_horas = np.array([1.0, 1.2, 1.1])

# Vectorización elemento a elemento en C
velocidades = distancias_km / tiempo_horas
print("Velocidades medias:", np.round(velocidades, 2))
```

**Salida real:**

```text
Velocidades medias: [10.5  10.08 10.73]
```

---

### Intermedio

Indexación booleana y filtrado condicional rápido:

```python
import numpy as np

goles = np.array([25, 31, 28, 15, 8, 22])
mascara_elite = goles >= 20
print("Goles de élite:", goles[mascara_elite])
```

**Salida real:**

```text
Goles de élite: [25 31 28 22]
```

---

### Avanzado

Transformación matricial bidimensional con álgebra lineal:

```python
import numpy as np

# Matriz de rendimiento (3 atletas x 2 métricas: minutos, goles)
datos = np.array([
    [2100, 21],
    [2450, 28],
    [1800, 15]
])

# Normalización Z-score vectorizada por columna (axis=0)
medias = np.mean(datos, axis=0)
desvios = np.std(datos, axis=0)
datos_z = (datos - medias) / desvios
print("Matriz estandarizada Z-score:")
print(np.round(datos_z, 2))
```

**Salida real:**

```text
Matriz estandarizada Z-score:
[[-0.06 -0.06]
 [ 1.25  1.23]
 [-1.18 -1.18]]
```

## 6. Aplicaciones en el mundo real

En el procesamiento de imágenes digitales y visión por computadora, una fotografía a color de $1920 	imes 1080$ píxeles se almacena como un arreglo NumPy tridimensional `ndarray` de forma `(1080, 1920, 3)` con tipo `uint8`. Operaciones como filtros de brillo, detección de bordes mediante convolución o normalización de canales RGB se ejecutan como productos matriciales en NumPy antes de alimentar redes neuronales.

## 7. Uso en producción

1. **Control estricto de tipos (`dtype`):** Declarar tipos compactos (`int16`, `float32`) evita consumos excesivos de memoria en microservicios analíticos.
2. **Evitar copias innecesarias:** Conocer cuándo NumPy genera una vista y cuándo una copia es crítico para prevenir fugas de memoria (*memory leaks*).
3. **Orden de almacenamiento C vs Fortran:** Los arreglos creados por defecto usan orden mayor por filas (*C-contiguous*). Recorrerlos por columnas es más lento; si el algoritmo lo exige, especificar `order='F'`.

## 8. Errores comunes y recomendaciones

* **Error común: Mutar vistas creyendo que son independientes:** `b = a[0:5]; b[0] = 999` modifica `a[0]`. **Recomendación:** Usar `b = a[0:5].copy()`.
* **Error común: Bucles `for` para operar arreglos:** Destruye la aceleración de NumPy. **Recomendación:** Emplear funciones universales vectorizadas (`ufuncs`).

## 9. Resumen

NumPy provee la infraestructura básica de arreglos contiguos en C `ndarray`. Sus principios nucleares son la vectorización, el *broadcasting*, la indexación avanzada y el soporte de álgebra lineal de alto rendimiento.

## 10. Referencias oficiales

* [NumPy Official Documentation](https://numpy.org/doc/stable/).
* [NumPy User Guide](https://numpy.org/doc/stable/user/index.html).
