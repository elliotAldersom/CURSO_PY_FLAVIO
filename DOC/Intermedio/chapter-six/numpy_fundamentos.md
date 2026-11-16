# Fundamentos de Arreglos N-Dimensionales con NumPy (`ndarray`)

## 2. Introducción

En el ecosistema científico, financiero y de aprendizaje automático en Python, **NumPy** (*Numerical Python*) constituye la biblioteca fundacional sobre la cual se construyen prácticamente todas las herramientas modernas de computación numérica, incluyendo [Pandas](../chapter-three/pandas_fundamentos.md), SciPy, Matplotlib, Scikit-Learn, PyTorch y TensorFlow.

Aunque las [listas](../../Basico/chapter-two/listas.md) nativas de Python son contenedores sumamente versátiles, resultan inadecuadas para computación numérica de alto rendimiento: almacenan punteros a objetos genéricos heterogéneos dispersos por la memoria RAM (*pointer arrays*), imponen un costo de indirección continuo y requieren comprobaciones dinámicas de tipo en cada operación elemental.

NumPy resuelve estas limitaciones introduciendo la estructura de datos **`ndarray`** (*N-dimensional array*): un bloque contiguo de memoria que aloja elementos numéricos homogéneos del mismo tipo de datos fijo (`dtype`), procesable directamente en memoria C mediante instrucciones vectorizadas de CPU (*SIMD*) con un rendimiento órdenes de magnitud superior.

## 3. Fundamentos y conceptos

**Estructura interna de un `ndarray` en memoria.** Un arreglo de NumPy se compone de dos elementos arquitectónicos principales:

1. **Búfer de datos (*Data Buffer*):** un segmento continuo de memoria física que contiene los bytes crudos de los elementos sin envoltorios de objetos Python.
2. **Encabezado de metadatos (*Array Header*):** un descriptor ligero de Python que almacena:
   - **`shape`:** una tupla de enteros que define el tamaño del arreglo a lo largo de cada dimensión o eje (*axis*).
   - **`dtype`:** el descriptor de tipo de dato que especifica el tamaño en bytes y la representación binaria de cada celda (p. ej. `int32`, `float64`, `bool`).
   - **`strides`:** una tupla de enteros que indica cuántos bytes debe desplazarse el cursor de memoria en el búfer para avanzar una posición en cada dimensión.
   - **`ndim`:** el número de dimensiones o rango del arreglo (`len(shape)`).
   - **`size`:** el número total de elementos almacenados ($\prod \text{shape}_i$).

**Comparación de arquitectura de memoria: Lista de Python frente a `ndarray`.**
- **Lista de Python (`list[int]`):** array de punteros de 64 bits hacia objetos independientes `PyObject` en el montón (*heap*), cada uno con su propio contador de referencias y metadatos (un entero en Python ocupa típicamente 28 bytes de memoria).
- **Arreglo de NumPy (`np.ndarray` con `dtype=int32`):** memoria plana contigua donde cada entero ocupa exactamente 4 bytes sin sobrecarga de objetos. Esto optimiza drásticamente la tasa de aciertos en la memoria caché de la CPU (*cache locality*).

**El sistema de tipos de datos de NumPy (`dtype`).** NumPy implementa tipos numéricos estrictos con longitud en bits explícita:

| Familia de tipos | Dtypes comunes | Tamaño en memoria | Rango / Precisión |
| :--- | :--- | :--- | :--- |
| **Enteros con signo** | `int8`, `int16`, `int32`, `int64` | 1, 2, 4, 8 bytes | `int32`: $[-2^{31}, 2^{31}-1]$; `int64`: $[-2^{63}, 2^{63}-1]$ |
| **Enteros sin signo** | `uint8`, `uint16`, `uint32`, `uint64` | 1, 2, 4, 8 bytes | `uint8`: $[0, 255]$ (estándar para píxeles de imágenes) |
| **Punto flotante** | `float16`, `float32`, `float64` | 2, 4, 8 bytes | `float32`: precisión simple (32 bits); `float64`: doble precisión (64 bits, defecto de Python) |
| **Booleanos** | `bool_` | 1 byte por elemento | `True` o `False` |
| **Complejos** | `complex64`, `complex128` | 8, 16 bytes | Parte real e imaginaria combinadas |

**Constructores especializados de arreglos.**
NumPy proporciona rutinas nativas optimizadas para crear arreglos sin pasar por listas intermedias de Python:
- `np.zeros(shape)`: inicializa el bloque de memoria relleno de ceros.
- `np.ones(shape)`: inicializa el bloque relleno de unos.
- `np.full(shape, valor)`: inicializa con un valor constante especificado.
- `np.arange(start, stop, step)`: versión numérica optimizada de `range()` que admite pasos decimales (*floats*).
- `np.linspace(start, stop, num)`: genera $N$ puntos equiespaciados en el intervalo cerrado $[start, stop]$, indispensable para muestreo matemático y gráficos.
- `np.eye(N)`: genera una matriz identidad cuadrada de orden $N \times N$.

## 4. Sintaxis y funcionamiento

Instalación de la biblioteca en el entorno de trabajo:

```bash
pip install numpy
```

Importación canónica e inicializaciones típicas:

```python
import numpy as np

# Creación desde listas de Python
arreglo_1d = np.array([10, 20, 30], dtype=np.int32)
matriz_2d = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)

# Creación mediante generadores nativos de NumPy
ceros = np.zeros((3, 4), dtype=np.float32)        # Matriz 3x4 de ceros
rango = np.arange(0.0, 1.0, 0.2, dtype=np.float64) # [0.0, 0.2, 0.4, 0.6, 0.8]
muestreo = np.linspace(0.0, 100.0, 5)             # 5 puntos exactos: 0, 25, 50, 75, 100
```

Conversión explícita de tipos de datos mediante `.astype()`:

```python
import numpy as np

flotantes = np.array([1.2, 3.8, 5.5], dtype=np.float64)
enteros = flotantes.astype(np.int32)  # Trunca a enteros: [1, 3, 5] creando un nuevo arreglo
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación de arreglos unidimensionales y bidimensionales, e inspección de metadatos.**

```python
import numpy as np

# 1. Crear un vector (1D) y una matriz (2D)
vector = np.array([10, 20, 30, 40, 50], dtype=np.int32)
matriz = np.array(
    [
        [1.5, 2.5, 3.5],
        [4.5, 5.5, 6.5],
    ],
    dtype=np.float64,
)

# 2. Inspección formal de propiedades de memoria
print("--- Inspección del Vector ---")
print("Dimensiones (ndim)    :", vector.ndim)
print("Forma (shape)         :", vector.shape)
print("Total elementos (size):", vector.size)
print("Tipo de dato (dtype)  :", vector.dtype)
print("Bytes por celda       :", vector.itemsize)
print("Memoria total (bytes) :", vector.nbytes)

print("\n--- Inspección de la Matriz ---")
print("Dimensiones (ndim)    :", matriz.ndim)
print("Forma (shape)         :", matriz.shape)
print("Total elementos (size):", matriz.size)
print("Tipo de dato (dtype)  :", matriz.dtype)
print("Bytes por celda       :", matriz.itemsize)
print("Memoria total (bytes) :", matriz.nbytes)
```

Explicación paso a paso:

- `vector.ndim` devuelve `1` indicando que es un eje unidimensional con forma `(5,)`. Al ser `int32`, cada elemento ocupa 4 bytes (`itemsize = 4`), requiriendo exactamente 20 bytes en total (`5 * 4`).
- `matriz.ndim` devuelve `2` con forma `(2, 3)` (2 filas y 3 columnas). Al ser `float64`, cada número ocupa 8 bytes (`itemsize = 8`), ocupando 48 bytes en memoria física (`6 * 8`).

Resultado esperado:

```text
--- Inspección del Vector ---
Dimensiones (ndim)    : 1
Forma (shape)         : (5,)
Total elementos (size): 5
Tipo de dato (dtype)  : int32
Bytes por celda       : 4
Memoria total (bytes) : 20

--- Inspección de la Matriz ---
Dimensiones (ndim)    : 2
Forma (shape)         : (2, 3)
Total elementos (size): 6
Tipo de dato (dtype)  : float64
Bytes por celda       : 8
Memoria total (bytes) : 48
```

### Intermedio

**Ejemplo 2 — Rutinas de inicialización analítica: `linspace`, `arange`, matrices especiales y conversión defensiva con `astype`.**

```python
import numpy as np

# 1. Generación de mallas numéricas
eje_tiempo = np.linspace(0.0, 1.0, num=5)  # 5 muestras en 1 segundo
marcas_paso = np.arange(0, 10, step=2, dtype=np.int16)

# 2. Arreglos estructurales constantes
mascara_identidad = np.eye(3, dtype=np.int8)
cuadricula_constante = np.full((2, 4), fill_value=7.5, dtype=np.float32)

# 3. Conversión de tipos y manejo de sobreflujo (overflow)
sensores_crudos = np.array([254, 255, 256, 300], dtype=np.int32)
sensores_seguros = sensores_crudos.astype(np.int16)

# Demostración del comportamiento ante truncamiento
valores_decimales = np.array([9.99, -4.75, 0.05], dtype=np.float32)
valores_truncados = valores_decimales.astype(np.int32)

print("Eje temporal con linspace       :", eje_tiempo)
print("Secuencia con arange            :", marcas_paso)
print("Matriz Identidad 3x3:\n", mascara_identidad)
print("Matriz constante (2x4):\n", cuadricula_constante)
print("Conversión flotante a entero    :", valores_truncados)
```

Explicación técnica:

- `np.linspace(0.0, 1.0, num=5)` divide el intervalo en exactamente 4 saltos iguales de `0.25`: `[0.0, 0.25, 0.5, 0.75, 1.0]`, garantizando incluir ambos extremos de forma determinista.
- `np.full((2, 4), 7.5)` reserva un bloque de 8 flotantes de 32 bits e inicializa cada posición con `7.5`.
- `.astype(np.int32)` trunca hacia cero la parte fraccionaria de los números de punto flotante, convirtiendo `9.99` en `9` y `-4.75` en `-4`.

Resultado esperado:

```text
Eje temporal con linspace       : [0.   0.25 0.5  0.75 1.  ]
Secuencia con arange            : [0 2 4 6 8]
Matriz Identidad 3x3:
 [[1 0 0]
 [0 1 0]
 [0 0 1]]
Matriz constante (2x4):
 [[7.5 7.5 7.5 7.5]
 [7.5 7.5 7.5 7.5]]
Conversión flotante a entero    : [ 9 -4  0]
```

### Avanzado

**Ejemplo 3 — Comparación de rendimiento y consumo de memoria: Lista nativa de Python frente a `ndarray` de NumPy en un millón de elementos.**

```python
import sys
import time
import numpy as np

CANTIDAD_ELEMENTOS = 1_000_000

# 1. Medición de memoria espacial física
lista_python = list(range(CANTIDAD_ELEMENTOS))
arreglo_numpy = np.arange(CANTIDAD_ELEMENTOS, dtype=np.int64)

# Memoria de la lista: tamaño de la lista de punteros + tamaño estimado de cada int de Python
memoria_lista_bytes = sys.getsizeof(lista_python) + sum(
    sys.getsizeof(x) for x in lista_python[:100]
) * (CANTIDAD_ELEMENTOS // 100)
memoria_numpy_bytes = arreglo_numpy.nbytes

# 2. Medición de rendimiento temporal en cálculo aritmético (elevar al cuadrado)
inicio_lista = time.perf_counter()
resultado_lista = [x**2 for x in lista_python]
tiempo_lista = time.perf_counter() - inicio_lista

inicio_numpy = time.perf_counter()
resultado_numpy = arreglo_numpy**2
tiempo_numpy = time.perf_counter() - inicio_numpy

factor_aceleracion = tiempo_lista / tiempo_numpy
factor_ahorro_ram = memoria_lista_bytes / memoria_numpy_bytes

print(f"--- Benchmark: {CANTIDAD_ELEMENTOS:,} elementos ---")
print(f"Memoria Lista Python : {memoria_lista_bytes / (1024**2):.2f} MB")
print(f"Memoria Arreglo NumPy: {memoria_numpy_bytes / (1024**2):.2f} MB")
print(f"Ahorro de memoria RAM: {factor_ahorro_ram:.1f}x más eficiente")
print(f"\nTiempo Lista (bucle) : {tiempo_lista * 1000:.2f} ms")
print(f"Tiempo NumPy (vector): {tiempo_numpy * 1000:.2f} ms")
print(f"Aceleración de cómputo: {factor_aceleracion:.1f}x más rápido")
print("Consistencia de datos:", resultado_lista[10] == int(resultado_numpy[10]))
```

Explicación de ingeniería:

- En una lista de Python de un millón de enteros, el intérprete reserva un vector de punteros de 8 megabytes sumado a un millón de estructuras `PyLongObject` de 28 bytes cada una, totalizando cerca de 36 megabytes de memoria RAM.
- En NumPy con `int64`, un millón de enteros se almacenan en exactamente `1_000_000 * 8 bytes = 8 MB` planos, logrando un ahorro sustancial de memoria.
- La operación `arreglo_numpy ** 2` se ejecuta mediante un bucle vectorial compilado en C optimizado para instrucciones AVX/SIMD de la CPU sin overhead de evaluación dinámica de tipos, ejecutándose típicamente entre 20 y 80 veces más rápido que la comprensión de listas.

Resultado esperado:

```text
--- Benchmark: 1,000,000 elementos ---
Memoria Lista Python : 35.85 MB
Memoria Arreglo NumPy: 7.63 MB
Ahorro de memoria RAM: 4.7x más eficiente

Tiempo Lista (bucle) : 45.20 ms
Tiempo NumPy (vector): 1.15 ms
Aceleración de cómputo: 39.3x más rápido
Consistencia de datos: True
```

## 6. Aplicaciones en el mundo real

- **Visión por Computadora y Procesamiento de Imágenes:** una imagen digital se representa de forma natural como un arreglo 3D de dimensiones `(alto, ancho, canales_color)` con `dtype=np.uint8`, manipulable en OpenCV o Pillow.
- **Entrenamiento de Redes Neuronales y Machine Learning:** capas de pesos sinápticos, lotes de datos (*batches*) y tensores multidimensionales se inicializan y transfieren internamente como arreglos contiguos en memoria.
- **Señales de Audio y Series Temporales:** muestreo de ondas sonoras a 44.1 kHz representadas como vectores unidimensionales `float32` para filtrado por transformada de Fourier (*FFT*).
- **Finanzas Cuantitativas y Simulación de Riesgo:** matrices de correlación de carteras de inversión y simulaciones numéricas de Monte Carlo con millones de trayectorias simultáneas.

## 7. Uso en producción

- **Seleccionar el `dtype` más pequeño que preserve la fidelidad numérica:** utilizar `float64` por defecto cuando `float32` es suficiente duplica el consumo de memoria RAM y el ancho de banda hacia la memoria caché. En procesamiento masivo de datos o entrenamiento de modelos, definir `dtype=np.float32` o `int16` permite duplicar o cuadruplicar el volumen procesable en el mismo hardware.
- **Evitar bucles `for` en Python sobre arreglos de NumPy:** iterar un `ndarray` con un bucle `for item in arreglo:` anula todas las ventajas de rendimiento de NumPy, pues cada acceso desacopla el valor y crea un objeto temporal de Python. Las operaciones deben realizarse siempre mediante funciones vectorizadas.
- **Garantizar contigüidad de memoria (*C-contiguous*):** al pasar arreglos a bibliotecas escritas en C, Rust o CUDA, verificar con `arreglo.flags.c_contiguous` que los datos no estén fragmentados o traspuestos en memoria para habilitar transferencias DMA de máxima velocidad.
- **Cuidado con el desbordamiento silencioso en enteros de longitud fija:** en NumPy, a diferencia de los enteros de Python que tienen precisión arbitraria infinita, los enteros de NumPy son de longitud fija en hardware (`int32`, `int64`). Si un cálculo supera el valor máximo permitido, ocurrirá un desbordamiento numérico (*integer overflow*) silencioso arrojando resultados negativos o inesperados sin lanzar excepciones.

## 8. Errores comunes y recomendaciones

1. **Desbordamiento numérico (*Overflow*) silencioso en enteros de longitud fija.**

```python
import numpy as np

# ERROR: int8 solo abarca de -128 a 127
a = np.array([100, 120], dtype=np.int8)
resultado = a + a  # 100 + 100 = 200, excede 127 y desborda a -56
```

Diagnóstico: los tipos enteros de NumPy respetan el tamaño exacto del hardware. Al alcanzar el límite, los bits desbordan sin advertencias. Recomendación: verificar rangos y seleccionar tipos de capacidad suficiente (`int32` o `int64`) antes de operar sumas o productos acumulativos.

2. **Usar `np.arange` con pasos de punto flotante para intervalos cerrados.**

```python
import numpy as np

# PROBLEMA: la aritmética de coma flotante binaria puede incluir o excluir el límite superior
puntos = np.arange(0.0, 1.0, 0.1)
```

Diagnóstico: debido a que `0.1` no tiene representación exacta en binario, el paso puede acumular errores de redondeo dejando fuera el último punto o agregando uno adicional inesperado. Recomendación: para divisiones decimales uniformes, utilizar siempre `np.linspace(inicio, fin, num_puntos)` que garantiza matemáticamente la cantidad de muestras y los extremos exactos.

3. **Confundir la conversión `.astype()` con una mutación in-place.**

```python
import numpy as np

valores = np.array([1.5, 2.8, 3.2])
valores.astype(np.int32)  # NO modifica "valores" in-place; retorna un NUEVO arreglo

print("Tipo sigue siendo flotante:", valores.dtype)  # float64
# Corrección: reasignar la variable
valores = valores.astype(np.int32)
```

Diagnóstico: `.astype()` no muta el arreglo subyacente; reserva un nuevo búfer con la copia convertida y lo retorna. Recomendación: capturar el valor de retorno en una nueva variable o reasignar explícitamente.

## 9. Resumen

- El **`ndarray`** de NumPy es la estructura fundamental para computación numérica de alto rendimiento en Python, alojando datos homogéneos en un bloque contiguo de memoria administrado en C.
- Cada arreglo está caracterizado por sus metadatos fundamentales: **`shape`** (dimensiones), **`dtype`** (tipo y tamaño de celda), **`ndim`** (rango de ejes) y **`size`** (total de elementos).
- Frente a las listas de Python, los arreglos de NumPy consumen sustancialmente menos memoria RAM y ejecutan operaciones matemáticas con aceleraciones de varios órdenes de magnitud gracias al procesamiento vectorial directo en CPU.
- Funciones generadoras como `zeros`, `ones`, `arange` y `linspace` permiten construir mallas numéricas eficientes sin sobrecarga de listas temporales.
- En producción es crítico seleccionar el `dtype` adecuado para optimizar la caché y prevenir desbordamientos numéricos en enteros de tamaño fijo.

## 10. Referencias oficiales

- <https://numpy.org/doc/stable/reference/arrays.ndarray.html> — Documentación oficial de NumPy: especificación completa de la clase `ndarray`, memoria y atributos.
- <https://numpy.org/doc/stable/reference/arrays.dtypes.html> — Documentación oficial de NumPy: catálogo exhaustivo de tipos de datos (`dtypes`), escalares y conversiones.
- <https://numpy.org/doc/stable/reference/routines.array-creation.html> — Documentación oficial de NumPy: catálogo de rutinas de creación de arreglos (`zeros`, `ones`, `arange`, `linspace`).
- <https://numpy.org/doc/stable/user/basics.types.html> — Guía de usuario de NumPy: representación binaria, tamaños y prevención de sobreflujo de tipos numéricos.

