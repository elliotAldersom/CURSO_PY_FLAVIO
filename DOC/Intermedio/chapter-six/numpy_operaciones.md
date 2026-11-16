# Operaciones Vectorizadas, Indexación Avanzada y Broadcasting en NumPy

## 2. Introducción

El verdadero poder de [NumPy](numpy_fundamentos.md) como motor de cálculo científico no radica únicamente en su almacenamiento compacto en memoria, sino en su modelo de ejecución: la **computación vectorizada**.

En el modelo tradicional de Python, aplicar una operación matemática sobre una colección de un millón de elementos exige escribir un [bucle `for`](../../Basico/chapter-two/bucles.md) o una comprensión de listas. En cada iteración, el intérprete debe determinar dinámicamente el tipo de dato, resolver la función aritmética correspondiente en CPython, comprobar límites y empaquetar un nuevo objeto numérico en el montón (*heap*).

NumPy sustituye este ciclo interpretado por **funciones universales (`ufunc`)** implementadas en C optimizado y ensamblador vectorial. La misma operación se expresa de forma declarativa sin bucles visibles a nivel de usuario, procesando bloques contiguos de memoria con paralelismo a nivel de instrucción (*SIMD*). 

Asimismo, NumPy introduce dos conceptos fundamentales de la arquitectura matricial moderna:
1. **Reglas formales de Difusión (*Broadcasting*):** aritmética transparente entre arreglos de diferentes formas sin replicar físicamente datos en memoria RAM.
2. **Diferenciación estricta entre Vistas (*Views*) y Copias (*Copies*):** manipulación de subarreglos sin duplicación de memoria para máxima eficiencia.

## 3. Fundamentos y conceptos

**Indexación básica y el concepto de Vista (*View*) frente a Copia (*Copy*).**
Cuando se extrae un subarreglo en Python ordinario mediante rebanado (`sub = lista[1:5]`), Python crea siempre una **copia física independiente** de los elementos.

En NumPy, el rebanado básico con sintaxis de dos puntos (`sub = arreglo[1:5]`) genera por defecto una **Vista (*View*)**:
- Una vista es un nuevo encabezado `ndarray` que apunta al **mismo búfer de memoria física** original, alterando únicamente el desplazamiento (*offset*), la forma (`shape`) y los pasos (`strides`).
- Cualquier modificación efectuada sobre la vista **altera directamente el arreglo original**.
- Para determinar si un arreglo es una vista o posee su propia memoria, se inspecciona el atributo `arreglo.base`: si devuelve `None`, el arreglo es dueño de sus datos; si devuelve una referencia a otro arreglo, es una vista.
- Para forzar la duplicación física e independizar los datos se utiliza explícitamente el método `.copy()`.

**Indexación Avanzada (*Fancy Indexing* y Máscaras Booleanas).**
A diferencia del rebanado básico con dos puntos, la **indexación avanzada siempre retorna una copia física nueva en memoria**:
1. **Indexación con máscaras booleanas:** se evalúa una condición lógica sobre el arreglo produciendo un arreglo booleano de la misma forma; al pasarlo como índice (`datos[datos > 0]`), filtra y extrae únicamente las celdas que cumplen la condición.
2. **Indexación con arreglos de enteros (*Fancy Indexing*):** se pasa una lista o arreglo de posiciones enteras (`datos[[0, 4, 2]]`) para extraer o reorganizar elementos en un orden arbitrario.

**Funciones Universales (`ufunc`) y Vectorización.**
Una `ufunc` es una función matemática que opera sobre `ndarray` elemento por elemento de forma vectorizada a nivel de C:
- Operaciones aritméticas elementales: `+`, `-`, `*`, `/`, `//`, `%`, `**` se sobrecargan llamando internamente a `np.add`, `np.subtract`, `np.multiply`, etc.
- Funciones matemáticas trascendentes: `np.sqrt()`, `np.exp()`, `np.log()`, `np.sin()`, `np.cos()`, `np.abs()`.
- Funciones lógicas y comparaciones: `>`, `<`, `==`, `!=`, combinables con operadores bit a bit vectorizados: `&` (AND lógico), `|` (OR lógico), `~` (NOT lógico).

**Reglas formales de Difusión (*Broadcasting*).**
El *Broadcasting* describe cómo NumPy gestiona operaciones aritméticas entre arreglos que tienen diferentes dimensiones o formas. En lugar de copiar los datos en memoria para igualar las matrices, NumPy simula la expansión dimensional ajustando los pasos (*strides*) a cero.

Para que dos arreglos sean compatibles bajo *Broadcasting*, sus dimensiones se alinean **de derecha a izquierda (desde el último eje hacia el primero)**. Para cada dimensión alineada, debe cumplirse una de las siguientes dos condiciones:
1. Las dimensiones tienen **exactamente el mismo tamaño** ($d_1 = d_2$).
2. Una de las dimensiones es **igual a 1** ($d_1 = 1$ o $d_2 = 1$).

Si un arreglo tiene menos dimensiones que el otro, se le añaden dimensiones ficticias de tamaño `1` a la izquierda hasta igualar el rango. Si en algún eje las dimensiones difieren y ninguna es `1`, NumPy lanza inmediatamente un `ValueError: operands could not be broadcast together`.

## 4. Sintaxis y funcionamiento

Indexación multidimensional y rebanado:

```python
import numpy as np

matriz = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

# Selección de celda fila 1, columna 2 -> 60
celda = matriz[1, 2]

# Submatriz: filas 0 a 1, columnas 1 a 2
sub_vista = matriz[0:2, 1:3]

# Modificar sub_vista afecta a matriz original
sub_vista[0, 0] = 999  # Altera matriz[0, 1]
```

Filtrado booleano y reasignación condicional:

```python
import numpy as np

datos = np.array([-5, 12, -3, 8, 0, 15])

# Máscara booleana
positivos = datos[datos > 0]  # [12, 8, 15] (crea una copia)

# Reasignación condicional vectorizada: recortar negativos a cero
datos[datos < 0] = 0          # [0, 12, 0, 8, 0, 15] in-place
```

Alineación por *Broadcasting*:

```python
import numpy as np

# Matriz (3, 3) y vector (3,)
matriz = np.ones((3, 3))
vector = np.array([10, 20, 30])  # Forma (3,) -> se alinea como (1, 3) y se propaga a (3, 3)

# Suma vectorizada por columnas sin bucle
resultado = matriz + vector
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Aritmética vectorizada, funciones universales y verificación de vistas frente a copias.**

```python
import numpy as np

# 1. Aritmética elemento a elemento y ufuncs
angulos_grados = np.array([0.0, 30.0, 45.0, 60.0, 90.0])
angulos_radianes = np.deg2rad(angulos_grados)
senos = np.sin(angulos_radianes)

print("Grados  :", angulos_grados)
print("Radianes:", np.round(angulos_radianes, 3))
print("Senos   :", np.round(senos, 3))

# 2. Demostración crítica: Vistas mutables vs Copias independientes
original = np.array([10, 20, 30, 40, 50])

vista_rebanada = original[1:4]      # Elementos [20, 30, 40]
copia_segura = original[1:4].copy() # Elementos [20, 30, 40] pero en nuevo búfer

# Mutar la vista altera el original
vista_rebanada[0] = 999
# Mutar la copia NO altera el original
copia_segura[1] = 888

print("\n--- Demostración de Memoria Compartida ---")
print("Original tras mutar la vista :", original)
print("Vista referenciando al padre :", vista_rebanada.base is original)
print("Copia independiente del padre:", copia_segura.base is None)
```

Explicación paso a paso:

- `np.deg2rad` y `np.sin` procesan el arreglo de 5 elementos en un solo paso vectorial en C, retornando un nuevo `ndarray` con los valores trigonométricos calculados sin requerir bucles explícitos.
- `original[1:4]` no reserva nueva memoria: crea una vista cuya propiedad `.base` apunta a `original`. Modificar `vista_rebanada[0] = 999` altera automáticamente la posición índice 1 del arreglo `original`.
- `.copy()` duplica los bytes en una nueva región de memoria física (`copia_segura.base is None`), garantizando aislamiento total.

Resultado esperado:

```text
Grados  : [ 0. 30. 45. 60. 90.]
Radianes: [0.    0.524 0.785 1.047 1.571]
Senos   : [0.    0.5   0.707 0.866 1.   ]

--- Demostración de Memoria Compartida ---
Original tras mutar la vista : [ 10 999  30  40  50]
Vista referenciando al padre : True
Copia independiente del padre: True
```

### Intermedio

**Ejemplo 2 — Filtrado booleano compuesto, indexación posicional y normalización condicional con `np.where`.**

```python
import numpy as np

# Datos simulados de lecturas de sensores industriales (temperatura en °C)
lecturas = np.array(
    [
        [22.4, 28.1, 45.2, 19.8],
        [85.6, 21.0, 92.3, 31.5],
        [18.5, 78.9, 25.4, 110.2],
    ]
)

# 1. Máscara booleana compuesta: anomalías térmicas (menores a 20°C o mayores a 80°C)
mascara_alerta = (lecturas < 20.0) | (lecturas > 80.0)
valores_anomalos = lecturas[mascara_alerta]

# 2. np.where: sustitución condicional vectorizada (equivalente a if/else sobre matrices)
# Si es anómalo marcar como -1.0; si es normal, conservar el valor original
lecturas_saneadas = np.where(mascara_alerta, -1.0, lecturas)

# 3. Fancy Indexing: extraer columnas específicas en orden inverso (columna 3 y columna 0)
columnas_clave = lecturas[:, [3, 0]]

print("Matriz original de sensores:\n", lecturas)
print("\nMáscara booleana de alertas (True = peligro):\n", mascara_alerta)
print("\nValores anómalos extraídos :", valores_anomalos)
print("\nMatriz con anomalías reemplazadas por -1.0:\n", lecturas_saneadas)
print("\nColumnas 3 y 0 extraídas por Fancy Indexing:\n", columnas_clave)
```

Explicación técnica:

- Para combinar condiciones lógicas sobre arreglos de NumPy se utilizan operadores bit a bit (`|` para OR, `&` para AND, `~` para NOT) envueltos en paréntesis obligatorios, pues los operadores lógicos estándar de Python (`or`, `and`) intentarían evaluar el arreglo completo como un único booleano arrojando `ValueError`.
- `np.where(condicion, valor_si_true, valor_si_false)` es la forma canónica de expresar un condicional vectorizado que se ejecuta a máxima velocidad en C sin ramificaciones interpretadas.
- La indexación `lecturas[:, [3, 0]]` toma todas las filas (`:`) y selecciona únicamente las columnas de índices 3 y 0, produciendo una copia física con la estructura reorganizada.

Resultado esperado:

```text
Matriz original de sensores:
 [[ 22.4  28.1  45.2  19.8]
 [ 85.6  21.   92.3  31.5]
 [ 18.5  78.9  25.4 110.2]]

Máscara booleana de alertas (True = peligro):
 [[False False False  True]
 [ True False  True False]
 [ True False False  True]]

Valores anómalos extraídos : [ 19.8  85.6  92.3  18.5 110.2]

Matriz con anomalías reemplazadas por -1.0:
 [[22.4 28.1 45.2 -1. ]
 [-1.  21.  -1.  31.5]
 [-1.  78.9 25.4 -1. ]]

Columnas 3 y 0 extraídas por Fancy Indexing:
 [[ 19.8  22.4]
 [ 31.5  85.6]
 [110.2  18.5]]
```

### Avanzado

**Ejemplo 3 — Normalización estadística de características (Z-score) mediante Broadcasting multidimensional.**

```python
import numpy as np

# Matriz de datos: 4 observaciones (filas) y 3 variables o características (columnas)
# Col 0: Edad [años], Col 1: Ingreso mensual [USD], Col 2: Puntuación crediticia [puntos]
observaciones = np.array(
    [
        [25.0, 1500.0, 650.0],
        [42.0, 4800.0, 720.0],
        [31.0, 2900.0, 590.0],
        [58.0, 7200.0, 810.0],
    ]
)

# 1. Calcular la media (mean) y desviación estándar (std) a lo largo del eje 0 (columnas)
# Observaciones tiene forma (4, 3)
medias = np.mean(observaciones, axis=0)      # Forma resultante: (3,)
desviaciones = np.std(observaciones, axis=0) # Forma resultante: (3,)

# 2. Mecanismo de Broadcasting en la normalización Z-score:
# Fórmula matemática: Z = (X - mu) / sigma
# Alineación:
# X      -> (4, 3)
# medias ->    (3,) -> se expande virtualmente a (1, 3) y se propaga a (4, 3)
matriz_centrada = observaciones - medias

# División vectorizada por broadcasting:
# matriz_centrada -> (4, 3)
# desviaciones    ->    (3,) -> se propaga a (4, 3)
matriz_estandarizada = matriz_centrada / desviaciones

# 3. Verificación matemática: las columnas normalizadas deben tener media 0 y desviación 1
medias_verif = np.mean(matriz_estandarizada, axis=0)
desv_verif = np.std(matriz_estandarizada, axis=0)

print("Forma de la matriz de datos     :", observaciones.shape)
print("Medias por columna (mu)         :", np.round(medias, 2))
print("Desviación por columna (sigma)  :", np.round(desviaciones, 2))
print("\nMatriz estandarizada (Z-score):\n", np.round(matriz_estandarizada, 4))
print("\nVerificación de media resultante (esperado 0):", np.round(medias_verif, 6))
print("Verificación de std resultante (esperado 1)  :", np.round(desv_verif, 6))
```

Explicación de ingeniería:

- En procesamiento de datos para aprendizaje automático, las variables con escalas astronómicas (como ingresos de \$7200) dominan y sesgan a los modelos sobre variables de menor escala (como edades de 25). La estandarización Z-score las lleva a una escala adimensional común con media $\mu = 0$ y varianza $\sigma^2 = 1$.
- `np.mean(observaciones, axis=0)` colapsa las filas produciendo un vector `(3,)` con el promedio de cada columna.
- Mediante las reglas de difusión (*broadcasting*), NumPy alinea el vector `(3,)` con la matriz `(4, 3)` desde la derecha, interpretándolo como si tuviera forma `(1, 3)` y restándolo de cada una de las 4 filas simultáneamente sin crear ninguna matriz intermedia de réplica en RAM.
- La normalización completa de las cuatro filas y tres columnas se ejecuta en una sola línea elegante, legible y computada a velocidad de lenguaje ensamblador.

Resultado esperado:

```text
Forma de la matriz de datos     : (4, 3)
Medias por columna (mu)         : [  39.25 4100.    692.5 ]
Desviación por columna (sigma)  : [  12.38 2137.76   80.74]

Matriz estandarizada (Z-score):
 [[-1.1514 -1.2162 -0.5264]
 [ 0.2222  0.3274  0.3406]
 [-0.6666 -0.5613 -1.2696]
 [ 1.515   1.4501  1.4554]]

Verificación de media resultante (esperado 0): [ 0. -0.  0.]
Verificación de std resultante (esperado 1)  : [1. 1. 1.]
```

## 6. Aplicaciones en el mundo real

- **Filtrado y Procesamiento Digital de Señales:** convolución discreta de audio y eliminación de ruido de fondo aplicando umbrales con máscaras booleanas.
- **Normalización de Tensores en Deep Learning:** estandarización de lotes (*Batch Normalization*) y escalamiento de píxeles dividiendo arreglos de imágenes `(N, 28, 28)` por `255.0` mediante difusión escalar.
- **Cálculo de Distancias en Clústeres (K-Means / KNN):** cálculo vectorizado de la distancia euclidiana entre matrices de centroides y matrices de observaciones sin bucles anidados utilizando difusión dimensional.
- **Gráficos de Superficie 3D:** generación de mallas de coordenadas bidimensionales con `np.meshgrid()` para evaluar funciones bivariadas $z = f(x, y)$ en física y gráficos computacionales.

## 7. Uso en producción

- **Estar siempre alerta ante la creación accidental de vistas mutables:** al extraer una rodaja para trabajar de forma aislada, si el subarreglo va a sufrir modificaciones que no deban repercutir en el dataset original, llamar siempre a `.copy()` de manera explícita.
- **Verificar la compatibilidad de Broadcasting antes de cálculos pesados:** cuando se operan arreglos de formas complejas en pipelines automatizados, validar programáticamente las tuplas de dimensiones (`shape`) para evitar que dimensiones incompatibles fallen en medio de una transacción masiva.
- **Aprovechar argumentos `out=` en `ufunc` para no saturar la memoria RAM:** funciones como `np.add(a, b, out=a)` permiten almacenar el resultado directamente sobre uno de los arreglos existentes, evitando reservar memoria para matrices intermedias en servidores con restricciones estrictas de hardware.
- **Usar paréntesis siempre en comparaciones booleanas compuestas:** la precedencia de operadores en Python sitúa a los operadores bit a bit (`&`, `|`) por encima de los relacionales (`<`, `>`). Escribir `arr > 0 & arr < 10` se evalúa como `arr > (0 & arr) < 10`, arrojando errores semánticos o de tipos. La sintaxis obligatoria es siempre `(arr > 0) & (arr < 10)`.

## 8. Errores comunes y recomendaciones

1. **Usar `and` u `or` lógicos de Python en lugar de `&` y `|` vectorizados (`ValueError`).**

```python
import numpy as np

a = np.array([1, 2, 3])
# ERROR: ValueError: The truth value of an array with more than one element is ambiguous.
# if a > 1 and a < 3: pass

# Corrección: operadores bit a bit con paréntesis
mascara = (a > 1) & (a < 3)  # [False, True, False]
```

Diagnóstico: `and` requiere que el operando evalúe a un único valor booleano mediante `bool()`; un arreglo con múltiples elementos no puede decidir unívocamente si representa `True` o `False`. Recomendación: utilizar siempre los operadores vectorizados `&`, `|`, `~` con paréntesis.

2. **Error de compatibilidad en difusión (*operands could not be broadcast together*).**

```python
import numpy as np

matriz = np.ones((3, 4))
vector = np.array([1, 2, 3])  # Forma (3,)

# ERROR: ValueError: operands could not be broadcast together with shapes (3,4) (3,)
# resultado = matriz + vector
```

Diagnóstico: el vector `(3,)` se alinea desde la derecha contra la columna de tamaño 4 de la matriz `(3, 4)`. Como $3 \ne 4$ y ninguno es 1, la difusión falla. Recomendación: redimensionar el vector a columna mediante `vector[:, np.newaxis]` para que tenga forma `(3, 1)`, el cual sí se difunde de forma válida contra `(3, 4)`.

3. **Confundir la multiplicación de matrices algebraicas (`@` / `dot`) con la multiplicación elemento a elemento (`*`).**

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[2, 0], [1, 2]])

producto_elemento = a * b  # [[1*2, 2*0], [3*1, 4*2]] = [[2, 0], [3, 8]]
producto_matricial = a @ b  # Producto algebraico de matrices (filas x columnas)
```

Diagnóstico: en NumPy, el operador `*` es estrictamente la multiplicación de Hadamard (elemento a elemento). Para el producto matricial del álgebra lineal debe utilizarse el operador `@` o `np.dot(a, b)`.

## 9. Resumen

- La **computación vectorizada** reemplaza los bucles interpretados de Python por bucles altamente optimizados en C que operan directamente sobre bloques contiguos de memoria de CPU.
- El rebanado básico genera **vistas** livianas que comparten la memoria física con el arreglo original, mientras que la indexación avanzada (**máscaras booleanas** y *fancy indexing*) produce siempre **copias** independientes.
- Las **funciones universales (`ufunc`)** proveen transformaciones matemáticas rápidas que aceptan arreglos y escalares de forma homogénea.
- Las reglas de **difusión (*Broadcasting*)** permiten operar arreglos con diferentes dimensiones alineándolos desde la derecha, expandiendo virtualmente ejes de tamaño 1 sin duplicar memoria RAM.
- La función `np.where` provee bifurcaciones condicionales vectorizadas sin penalización de rendimiento.

## 10. Referencias oficiales

- <https://numpy.org/doc/stable/user/basics.broadcasting.html> — Guía oficial de NumPy sobre teoría y reglas formales de Difusión (*Broadcasting*).
- <https://numpy.org/doc/stable/user/basics.indexing.html> — Guía oficial de NumPy sobre indexación básica, avanzada y reglas de generación de vistas frente a copias.
- <https://numpy.org/doc/stable/reference/ufuncs.html> — Documentación oficial de NumPy sobre funciones universales (`ufunc`), métodos y parámetros de salida.
- <https://numpy.org/doc/stable/reference/generated/numpy.where.html> — Referencia de API para la función condicional `numpy.where`.

