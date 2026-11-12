# Listas en Python

## 2. Introducción

Una [variable](../chapter-one/variables.md) guarda un valor: un número, una cadena. Pero casi todo dato real llega **en conjunto**: las notas de un curso, los nombres de una clase, los precios de un catálogo. Una **lista** es la estructura de Python para guardar una colección ordenada de elementos bajo un solo nombre, separados por comas y encerrados entre corchetes: `["Ana", "Luis", "Marta"]`.

¿Por qué existe? Porque el número de elementos no se conoce de antemano: una lista **crece y encoge** mientras el programa corre. Es posible agregar un elemento al final, quitar el que está en la posición 3 o reordenar todo, y la lista sigue siendo la misma lista. Esa capacidad de cambiar se llama **mutabilidad** y es la gran diferencia frente a las [cadenas de texto](cadenas.md), que no admiten cambios en el lugar.

Las listas son la estructura de datos más usada del nivel básico: sirven para acumular resultados, para recorrer registros con un [bucle](bucles.md), para convertir texto en datos con `split` (ver [cadenas](cadenas.md)) y como base de casi todas las colecciones del nivel intermedio. Su importancia es práctica: dominar indexado, mutación y métodos de lista es el requisito para entender listas por comprensión, diccionarios y, más adelante, el tratamiento de datos con Pandas.

## 3. Fundamentos y conceptos

**Creación.** La forma directa es el literal con corchetes `["a", "b"]` (la lista vacía es `[]`). La función `list(...)` convierte otro dato en lista: `list("hola")` produce `['h', 'o', 'l', 'a']`, `list((1, 2))` produce `[1, 2]`, `list({"a": 1, "b": 2})` produce `["a", "b"]` —sobre un diccionario entrega sus **claves**— y `list(diccionario.values())` entrega sus valores, tal como practica el material. A diferencia de otros lenguajes, una lista de Python admite **tipos mezclados** en la misma lista (`[1, "hola", True]`), aunque conviene evitarlo para ordenar (sección 8).

**Indexado.** Igual que en las cadenas: los índices empiezan en 0 y llegan hasta `len(lista) - 1`; los negativos cuentan desde el final (`lista[-1]` es el último). Acceder fuera de rango produce `IndexError`. Esta simetría no es casual: lista y cadena son ambas **secuencias**, y comparten la notación de posiciones y rebanadas documentada en [cadenas](cadenas.md).

**Rebanadas.** `lista[inicio:fin:paso]` entrega una **lista nueva** con los elementos pedidos, con `fin` exclusivo. Una rebanada es siempre una copia: modificarla no altera la original, y `lista[:]` o `lista.copy()` son la forma de clonar la lista completa.

**Mutación.** La posición se puede reasignar: `lista[3] = "nuevo"` cambia **ese elemento** dejando intactos los demás. La reasignación completa (`lista = [...]`) no modifica la lista original: crea otra y apunta la variable a ella. Ese detalle explica por qué el material puede "cambiar todos los datos" de una tupla redefiniendo la variable, mientras que en la lista basta con tocar una posición (ver `Ejm_Datos_Compuestos.py`).

**Métodos que modifican y métodos que entregan.** `append`, `insert`, `extend`, `pop`, `remove`, `clear`, `reverse` y `sort` actúan **sobre la misma lista** y devuelven `None` (ningún valor); por eso `lista.append("x")` no puede guardarse esperando la lista. En cambio `pop` y `index` sí devuelven un dato (el elemento eliminado, la posición) y `count` devuelve un número. `sorted(...)` es la excepción de la familia: es una **función** que no toca la original y devuelve una lista ordenada nueva.

**`sort()` frente a `sorted()`.** `lista.sort()` ordena **en el sitio** (la lista queda modificada y el método devuelve `None`); `sorted(lista)` devuelve una **lista nueva** ordenada y deja la original como estaba. Además `sorted` funciona sobre cualquier iterable (tuplas, conjuntos, diccionarios), no solo sobre listas. Para ordenar por un criterio propio se usa el parámetro `key`, frecuentemente con una función `lambda`; ese tema se estudia en [funciones lambda](../../Intermedio/chapter-two/funciones_lambda.md).

**`reverse()` frente a `sort(reverse=True)`.** `reverse()` solo invierte el orden actual sin ordenar; `sort(reverse=True)` ordena de mayor a menor. Invertir no es ordenar: `[3, 1, 2].reverse()` da `[2, 1, 3]`.

**Borrado con `del`.** La sentencia `del` elimina una variable, un elemento (`del lista[0]`) o una rebanada completa (`del lista[1:3]`) de la lista. No existe para tuplas ni cadenas, porque sus elementos no se pueden quitar. El origen de esta palabra clave en el material es `Keyword_del.py` (sección 10).

**Referencias y copias.** `b = a` **no** copia la lista: ambas variables apuntan a **la misma** lista en memoria, y cualquier cambio se ve en las dos. La copia real es `b = a.copy()` o `b = list(a)`. Esta distinción es la fuente de muchos resultados sorprendentes y se demuestra en la sección 8.

**`sum`, `max` y `min`.** Además de los métodos, la biblioteca estándar ofrece funciones integradas que trabajan sobre listas numéricas: `sum(notas)` totaliza, `max(notas)` y `min(notas)` devuelven el mayor y el menor. Se usan brevemente en el Ejemplo 8; su cobertura completa corresponde a [funciones integradas](../../Intermedio/chapter-two/funciones_integradas.md) en el nivel intermedio.

**Listas por comprensión (mención).** El material escribe `numeros_duplicados = [x*2 for x in numeros]`: una forma abreviada de construir listas que combina bucle y transformación en una línea. Aquí solo se anuncia; el desarrollo completo está en [comprensiones](../../Intermedio/chapter-one/comprensiones.md).

**Intercambio de valores (adelanto).** El material resuelve intercambios con una variable temporal (`v0 = v1; v1 = v2; v2 = v0`) y también con la forma corta `a, b = b, a + b`, que aprovecha el empaquetamiento de valores. Esta segunda notación se explica con detalle en [tuplas](../../Intermedio/chapter-one/tuplas.md).

## 4. Sintaxis y funcionamiento

Sintaxis general de listas:

```text
[<elemento1>, <elemento2>, ...]
<lista>[<índice>]
<lista>[<inicio>:<fin>:<paso>]
<lista>.<método>(<argumento>)
del <lista>[<índice o rebanada>]
```

Componentes de acceso:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | Índice positivo | Posición desde el inicio (0 es el primero) | `lista[0]` primer elemento |
| 2 | Índice negativo | Posición desde el final (-1 es el último) | `lista[-1]` último elemento |
| 3 | `inicio` (rebanada) | Primera posición incluida; 0 al omitirlo | `lista[:3]` primeros tres |
| 4 | `fin` (rebanada) | Primera posición **excluida**; hasta el final al omitirlo | `lista[3:]` desde la cuarta |
| 5 | `paso` (rebanada) | Incremento entre posiciones; 1 al omitirlo | `lista[::2]` de dos en dos |
| 6 | `del` | Elimina un elemento o una rebanada de la lista | `del lista[0]` |

Métodos de consulta y conversión:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `list(x)` | Convierte cadena, tupla, conjunto o diccionario en lista | `list("hola")` → `['h', 'o', 'l', 'a']` |
| 2 | `len(lista)` | Cantidad de elementos | `len([1, 2])` → `2` |
| 3 | `count(x)` | Veces que aparece `x` | `[1, 2, 1].count(1)` → `2` |
| 4 | `index(x)` | Primera posición de `x`; lanza `ValueError` si falta | `[1, 2].index(2)` → `1` |
| 5 | `copy()` | Copia superficial de la lista | `lista.copy()` |
| 6 | `sorted(lista)` | Función: devuelve una **nueva** lista ordenada | `sorted([2, 1])` → `[1, 2]` |

Métodos de modificación (devuelven `None` salvo donde se indique):

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `append(x)` | Agrega `x` al final | `lista.append("z")` |
| 2 | `insert(i, x)` | Inserta `x` en la posición `i` | `lista.insert(0, "a")` |
| 3 | `extend(iterable)` | Agrega **varios** elementos al final | `lista.extend([1, 2])` |
| 4 | `pop(i)` | Elimina y **devuelve** el elemento; sin argumento, el último | `lista.pop()` |
| 5 | `remove(x)` | Elimina la primera aparición de `x` (devuelve `None`) | `lista.remove("a")` |
| 6 | `clear()` | Vacía la lista (devuelve `None`) | `lista.clear()` |
| 7 | `reverse()` | Invierte el orden en el sitio (devuelve `None`) | `lista.reverse()` |
| 8 | `sort(...)` | Ordena en el sitio (devuelve `None`); admite `reverse=True` | `lista.sort(reverse=True)` |

Funcionamiento: los métodos de la segunda tabla **mutan** el objeto lista: no hay que reasignar nada, la variable sigue apuntando a la misma lista, ya modificada. Los que devuelven `None` obligan a separar "hacer" de "obtener": para usar el resultado hay que llamar a otro método (`print(lista.sort())` imprime `None`, pero `lista` ya está ordenada). `del` funciona directamente sobre el contenedor: quita el elemento y **desplaza** los posteriores para que no queden huecos. `sorted` es la vía no destructiva: evalúa la lista, crea otra con los elementos ordenados y no toca la original.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Crear, leer y modificar una lista.**

```python
lista = ["Flavio", "Gerardo", "Silva", "Estrada", 61088098]
print(lista)
print(lista[3])
lista[3] = "Estrada"
print(lista)
print(lista[-1])
print(len(lista))
```

Explicación línea por línea:

- Línea 1: se crea la lista con corchetes; contiene cadenas y un número, tipos mezclados (permitido, aunque no recomendable para ordenar).
- Línea 2: imprime la lista completa tal cual.
- Línea 3: `lista[3]` accede a la cuarta posición (índices 0, 1, 2, 3) → `Estrada`.
- Línea 4: **mutación** por índice: se reasigna la posición 3. La lista cambia en el lugar, sin crear otra; es la diferencia frente a las cadenas inmutables.
- Línea 5: el índice negativo `-1` entrega el último elemento → `61088098`.
- Línea 6: `len()` cuenta los elementos, aquí 5 (el número también cuenta como elemento).

Resultado esperado:

```text
['Flavio', 'Gerardo', 'Silva', 'Estrada', 61088098]
Estrada
['Flavio', 'Gerardo', 'Silva', 'Estrada', 61088098]
61088098
5
```

**Ejemplo 2 — Agregar elementos: `append`, `insert` y `extend`.**

```python
meses = ["Enero", "Febrero", "Marzo"]
meses.append("Abril")
meses.insert(0, "Diciembre")
meses.extend(["Mayo", "Junio"])
print(meses)
print(len(meses))
```

Explicación línea por línea:

- Línea 1: lista inicial con tres meses.
- Línea 2: `append` agrega **un** elemento al final: `Marzo` pasa a tener "Abril" detrás.
- Línea 3: `insert(0, ...)` lo coloca en la primera posición; los demás se desplazan a la derecha.
- Línea 4: `extend` agrega **los dos** elementos de la lista dada, no una lista anidada. Si se hubiera usado `append(["Mayo", "Junio"])` habría entrado una lista dentro de la lista.
- Línea 5: la lista resultante tiene siete elementos.
- Línea 6: `len` confirma el conteo.

Resultado esperado:

```text
['Diciembre', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
7
```

**Ejemplo 3 — Quitar elementos: `pop`, `remove` y `clear`.**

```python
numeros = [10, 20, 30, 40]
ultimo = numeros.pop()
borrado = numeros.remove(20)
print(ultimo)
print(numeros)
print(borrado)
numeros.clear()
print(numeros)
```

Explicación línea por línea:

- Línea 2: `pop()` sin argumento elimina y **devuelve** el último elemento (`40`), por eso se puede guardar en una variable.
- Línea 3: `remove(20)` elimina por **valor** (no por posición) y no devuelve nada: `borrado` quedará en `None`.
- Líneas 4-5: se muestra el valor extraído y la lista ya reducida a `[10, 30]`.
- Línea 6: se confirma que `remove` no entregó ningún valor.
- Líneas 7-8: `clear()` vacía la lista por completo; el objeto sigue existiendo, solo que sin elementos.

Resultado esperado:

```text
40
[10, 30]
None
[]
```

### Intermedio

**Ejemplo 4 — De texto a lista ordenada.**

```python
texto = "banana manzana pera"
frutas = texto.split()
frutas.append("durazno")
frutas.sort()
print(frutas)
print(len(frutas))
```

Explicación de las decisiones tomadas:

- `texto.split()` sin argumento parte por espacios y entrega una lista de tres cadenas: la conversión texto → lista de [cadenas](cadenas.md) es el paso de entrada de casi todo procesamiento de datos.
- `append` agrega la cuarta fruta; aquí se usa en lugar de `extend` porque es **un** solo elemento.
- `sort()` ordena alfabéticamente en el sitio: la lista original queda modificada y el método devuelve `None`, por eso no se guarda su resultado (sección 8).
- Los elementos son todos cadenas: ese requisito es justamente lo que permite ordenarlos (ver el Ejemplo 5 y la sección 8).

Resultado esperado:

```text
['banana', 'durazno', 'manzana', 'pera']
4
```

**Ejemplo 5 — `sort()` frente a `sorted()`, con `count` e `index`.**

```python
notas = [70, 95, 80, 95]
print(notas.sort())
print(notas)
print(sorted(notas, reverse=True))
print(notas)
print(notas.count(95))
print(notas.index(80))
```

Explicación de las decisiones tomadas:

- El primer `print` revela el comportamiento crítico: `sort()` devuelve `None` porque ordena **en el sitio**; el valor devuelto no es la lista.
- El segundo `print` muestra que la lista **sí** quedó ordenada: el efecto ocurre aunque el resultado no se asigne.
- `sorted(notas, reverse=True)` crea una copia ordenada de mayor a menor sin tocar `notas`; el cuarto `print` lo confirma: la original sigue en `[70, 80, 95, 95]`.
- `count(95)` devuelve 2 (aparece dos veces) y `index(80)` devuelve 1 (primera posición). Ambos son consultas que no modifican nada.
- `reverse=True` es el parámetro oficial de orden descendente; el mismo efecto in-place se logra con `notas.sort(reverse=True)`.

Resultado esperado:

```text
None
[70, 80, 95, 95]
[95, 95, 80, 70]
[70, 80, 95, 95]
2
1
```

**Ejemplo 6 — Borrar con `del`: elemento y rebanada.**

```python
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
del lista[-1]
print(lista)
borrados = lista[:4]
del lista[:4]
print(lista)
print(borrados)
```

Explicación de las decisiones tomadas:

- `del lista[-1]` quita el último elemento sin devolver nada: la lista pasa de 10 a 9 elementos.
- `borrados = lista[:4]` **copia** los cuatro primeros valores antes de borrarlos: las rebanadas son copias, así que el registro de lo borrado sobrevive al `del`.
- `del lista[:4]` elimina la rebanada completa de un solo gesto; los elementos restantes se desplazan al inicio.
- El patrón "guardar rebanada, luego borrarla" es idéntico al de `Keyword_del.py` L56-69.
- Con `del` sobre una posición se borra por **índice**; para borrar por valor sigue siendo `remove` (Ejemplo 3).

Resultado esperado:

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[5, 6, 7, 8, 9]
[1, 2, 3, 4]
```

### Avanzado

**Ejemplo 7 — Pila y cola, y por qué el extremo importa.**

```python
pila = []
pila.append(1)
pila.append(2)
pila.append(3)
print(pila.pop())
print(pila.pop())
cola = ["primero", "segundo", "tercero"]
print(cola.pop(0))
print(cola)
```

Explicación de las decisiones tomadas:

- La **pila** (LIFO, último en entrar, primero en salir) se implementa con `append` para agregar y `pop()` para retirar: ambos actúan sobre el **final** de la lista. En **CPython** (y en las implementaciones estándar basadas en arreglos dinámicos), `list` se representa internamente mediante un arreglo contiguo de punteros (`PyListObject`) con sobreasignación de capacidad (*over-allocation*), lo que permite que `append()` y `pop()` operen en tiempo amortizado `O(1)`.
- `pop()` sin argumento devuelve el último (`3`) y después el penúltimo (`2`): la pila se vacía en orden inverso al de entrada.
- La **cola** (FIFO, primero en entrar, primero en salir) requiere retirar del **inicio**: `cola.pop(0)` lo resuelve funcionalmente, pero en esa representación de arreglo contiguo tiene costo `O(n)`, ya que obliga a desplazar una posición hacia atrás las `n - 1` referencias restantes.
- Consideración de rendimiento: cada `insert(0, ...)` o `pop(0)` desplaza toda la secuencia; en bucles con miles de elementos esa diferencia resulta significativa. Con `list` conviene operar sobre el final y, cuando se requiere una cola FIFO intensiva, emplear `collections.deque` (perteneciente a la **biblioteca estándar** de Python), que ofrece inserciones y extracciones `O(1)` en ambos extremos.
- La salida muestra el resultado correcto en ambos casos; lo que se optimiza es el costo algorítmico, no el comportamiento observable.

Resultado esperado:

```text
3
2
primero
['segundo', 'tercero']
```

**Ejemplo 8 — Reporte de notas con funciones integradas y copia de seguridad.**

```python
lecturas = [65, 80, 92, 55, 78, 88]
total = sum(lecturas)
print(total)
print(max(lecturas))
print(min(lecturas))
promedio = total / len(lecturas)
print(round(promedio, 2))
copia = lecturas.copy()
copia.sort(reverse=True)
print(copia)
print(lecturas)
```

Explicación de las decisiones tomadas:

- `sum`, `max` y `min` son **funciones integradas** que recorren la lista numérica y devuelven un dato; aquí se usan de forma breve, sin reemplazar los métodos de lista (su estudio completo corresponde a [funciones integradas](../../Intermedio/chapter-two/funciones_integradas.md)).
- El promedio se calcula con `total / len(lecturas)`; la división `/` siempre devuelve decimal, y `round(x, 2)` limita la presentación a dos decimales (mismo recurso que el material usa en `EJERCICIO_WHILE.py`).
- Antes de ordenar de mayor a menor se crea una **copia** con `copy()`: así el ranking no destruye el orden original de las lecturas, que puede ser relevante para el reporte.
- `copia.sort(reverse=True)` modifica solo la copia; el último `print` confirma que `lecturas` quedó intacta. Sin la copia, ambas variables habrían apuntado al mismo objeto (sección 8).
- El resultado combina acumulación (`sum`), estadística básica (`max`, `min`, promedio) y presentación (`round`, orden descendente) sobre una única fuente de datos.

Resultado esperado:

```text
458
92
55
76.33
[92, 88, 80, 78, 65, 55]
[65, 80, 92, 55, 78, 88]
```

## 6. Aplicaciones en el mundo real

- **Agrupar registros:** los alumnos de un curso, los pedidos de un día o los registros de un CSV se cargan en listas para procesarlos con bucles.
- **Acumular resultados:** construir una lista con `append` dentro de un bucle es el patrón estándar para recopilar totales, filtrados o transformaciones.
- **Pilas y colas:** deshacer acciones, gestionar llamadas pendientes o recorrer tareas en orden (Ejemplo 7) son estructuras presentes en editores, navegadores y servidores.
- **Ordenar para decidir:** rankings de notas, listas de precios de menor a mayor y clasificaciones deportivas se resuelven con `sort` o `sorted` (Ejemplo 5).
- **Parsing de texto:** separar un archivo o un mensaje en campos con `split` y operar sobre la lista resultante (Ejemplo 4) es la puerta de entrada al procesamiento de datos.
- **Intermedio de datos:** antes de llevar información a tablas (Pandas) o a diccionarios, los datos suelen vivir en listas de listas o listas de tuplas.
- **Interfaces de escritorio:** rellenar listados de un formulario y actualizar su contenido al agregar o quitar filas.

## 7. Uso en producción

- **`append` por defecto, `insert(0, ...)` y `pop(0)` con moderación:** en la representación interna de **CPython** (`PyListObject`, arreglo dinámico de punteros con sobreasignación), agregar o retirar al final cuesta `O(1)` amortizado, mientras que insertar o quitar en el inicio cuesta `O(n)` por el desplazamiento de los elementos restantes. Si el diseño exige una cola FIFO de alto volumen, conviene utilizar `collections.deque` de la **biblioteca estándar** de Python (Ejemplo 7).
- **No modificar la lista mientras se recorre:** se desplazan los índices y quedan elementos sin procesar; el patrón completo y la solución están en [bucles](bucles.md) (sección 8).
- **Copiar de forma explícita:** `b = a` comparte el objeto; si la intención es trabajar sin tocar el original, usar `a.copy()` o `list(a)`. Con listas anidadas la copia es **superficial**: solo copia el nivel exterior (los elementos internos siguen compartidos).
- **Listas homogéneas:** cuando la lista va a ordenarse o compararse, todos los elementos deben ser del mismo tipo; las listas mixtas rompen `sort` (sección 8) y confunden la lectura del código.
- **Elegir la estructura adecuada:** datos fijos e inmutables → [tuplas](../../Intermedio/chapter-one/tuplas.md); elementos sin repetición → [conjuntos](../../Intermedio/chapter-one/conjuntos.md); acceso por clave → [diccionarios](../../Intermedio/chapter-one/diccionarios.md). La lista es la opción por defecto para colecciones ordenadas y modificables.
- **Comprobaciones de pertenencia frecuentes:** `x in lista` recorre la lista elemento por elemento; si la verificación se repite mucho, un conjunto ofrece esa búsqueda mucho más rápida (se estudia en el nivel intermedio).
- **Ordenar por criterio:** para un orden propio (por edad, por precio) se usa `sort(key=...)` con `lambda`, tema de [funciones lambda](../../Intermedio/chapter-two/funciones_lambda.md); para no alterar la original, `sorted`.
- **Escribir listas legibles:** PEP 8 recomienda nombres en `snake_case`, espacios después de las comas y una lista por línea cuando es larga. Este criterio de estilo se presenta como fundamento complementario.

## 8. Errores comunes y recomendaciones

1. **Guardar el resultado de `append`.** Este programa no falla, pero la variable contiene `None`:

```python
lista = ["a", "b"]
resultado = lista.append("c")
print(resultado)
print(lista)
```

Resultado esperado:

```text
None
['a', 'b', 'c']
```

Diagnóstico: `append` modifica la lista en el sitio y no devuelve nada; imprimir `resultado` imprime `None`. La lista **sí** creció. Solución: no asignar el resultado de un método de modificación; encadenar el `print` sobre la propia lista (`print(lista)`).

2. **Acceder a una posición inexistente.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: IndexError, la posición 3 no existe
lista = [1, 2, 3]
print(lista[3])
```

Salida real: `IndexError: list index out of range`. Diagnóstico: los índices válidos son 0, 1 y 2 (`len - 1`). Solución: comprobar la longitud antes de indexar o usar una rebanada (`lista[3:4]`), que devuelve `[]` sin fallar.

3. **`remove` con un valor que no está.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: ValueError, remove no encuentra el valor
lista = [1, 2, 3]
lista.remove(4)
```

Salida real: `ValueError: list.remove(x): x not in list`. Diagnóstico: `remove` trabaja por valor y exige que el valor exista. Solución: verificar antes con `if x in lista:` o manejar la excepción (ver [excepciones](../../Intermedio/chapter-four/excepciones.md)). Además, `remove` elimina **solo la primera** aparición: si el valor se repite, hará falta repetir la llamada.

4. **Asignar una lista a otra esperando una copia.** Este programa no falla, pero modifica el original:

```python
original = [1, 2, 3]
copia = original
copia.append(4)
print(original)
```

Resultado esperado (la "copia" tocó al original):

```text
[1, 2, 3, 4]
```

Diagnóstico: `copia = original` crea **dos nombres para la misma lista**, no dos listas; `append` se vio en ambas variables. Solución: `copia = original.copy()` (o `list(original)`). Es el mismo motivo por el que el Ejemplo 8 ordena una copia y no la lista original.

5. **Ordenar guardando el resultado de `sort()`.** Este programa no falla, pero imprime `None`:

```python
numeros = [3, 1, 2]
ordenada = numeros.sort()
print(ordenada)
```

Resultado esperado:

```text
None
```

Diagnóstico: misma causa que el punto 1 — `sort` ordena en el sitio y devuelve `None`; la variable queda vacía de contenido útil mientras `numeros` sí está ordenada. Solución: `numeros.sort()` sin asignar, o `ordenada = sorted(numeros)` cuando se necesita la lista ordenada aparte (Ejemplo 5).

6. **Ordenar una lista de tipos mezclados.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, Python no sabe comparar str con int
datos = [3, "banana", 1]
datos.sort()
```

Salida real: `TypeError: '<' not supported between instances of 'str' and 'int'`. Diagnóstico: desde Python 3, ordenar exige comparables entre sí; texto y número no lo son. Solución: mantener listas homogéneas (una lista de números **y** una de textos) o, si el dato es mixto por diseño, ordenar con `key=str` como hace el material (`CLASE_ONE.py` L805), convirtiendo todos los elementos a texto para la comparación.

7. **Modificar la lista mientras se la recorre.** Quitar o agregar elementos dentro del `for` que los recorre desplaza los índices y deja elementos sin procesar, sin ningún error en pantalla. La demostración completa, el diagnóstico y las tres soluciones (recorrer copia, construir lista nueva, comprensión) están en [bucles](bucles.md), sección 8; aquí basta la regla: **iterar sobre lo que no cambia**.

8. **Usar el nombre de una función integrada como variable.** Bloque deliberadamente erróneo (el material comete este error al escribir `list = ["Enero", ...]` en `Métodos_Listas.py` L54):

```python
    # ERROR INTENCIONAL: TypeError, la variable 'list' tapa a la función integrada
list = [1, 2, 3]
nueva = list("hola")
```

Salida real: `TypeError: 'list' object is not callable`. Diagnóstico: la asignación redefinió `list` de función a lista; a partir de ahí, `list(...)` intenta "llamar" a una lista. El mismo riesgo existe con `dict`, `set`, `str`, `input` y `type`. Solución: nombrar las variables con nombres descriptivos (`lista`, `meses`, `notas`) y nunca reutilizar identificadores del lenguaje (PEP 8).

Recomendaciones de uso: conviene elegir `pop` cuando se conoce **la posición** y `remove` cuando se conoce **el valor**; preferir `append`/`extend` para crecer por el extremo final y `copy` antes de transformar una lista que se necesita conservar; y, cuando una operación sobre listas se convierta en un patrón repetido, encapsularla en una [función](../../Intermedio/chapter-two/funciones.md) (tema del nivel intermedio).

## 9. Resumen

- Una lista es una secuencia **mutable**: crece, se modifica y se reordena mientras el programa corre.
- Se crea con corchetes o con `list(...)`, que convierte cadenas, tuplas, conjuntos y diccionarios (estos últimos, por sus claves).
- El indexado usa posiciones desde 0 o negativas desde el final, y las rebanadas producen **copias** con el límite superior exclusivo.
- Los métodos de modificación (`append`, `insert`, `extend`, `pop`, `remove`, `clear`, `reverse`, `sort`) actúan en el sitio y devuelven `None`, salvo `pop`, que devuelve el elemento retirado.
- `sort()` ordena en el sitio; `sorted()` devuelve una lista nueva y funciona sobre cualquier iterable.
- `del` borra elementos o rebanadas; `count`, `index` y `len` son consultas que no alteran la lista.
- `b = a` no copia: hay que usar `copy()` o `list(...)` para trabajar sobre una lista independiente.
- `sum`, `max` y `min` complementan a los métodos para listas numéricas, y las listas por comprensión (mencionadas) son la forma abreviada de construirlas.
- Elegir entre lista, tupla, conjunto y diccionario según los datos es la base de la organización de información en Python.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L710-862) | `CLASE_ONE.py` | Métodos de lista del bloque inicial (`list`, `append`, `insert`, `extend`, `pop`, `remove`, `clear`, `sorted`, `sort`, `copy`, `reverse`, `index`) y ordenación con `key=str` | Se ordenaron en las tablas de la sección 4, se documentó qué devuelve cada método (el `None` que el material imprime por error en la L735) y se contrastó `sort` con `sorted` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/MÉTODOS Y FUNCIONES/Métodos_Listas.py` (L7-44, L46-171) | `Métodos_Listas.py` | Conversión con `list()` desde cadena, tupla, conjunto y diccionario; `append`, `insert`, `extend`, `pop`, `remove`, `clear`, `sort`, `reverse` | Son la base de los Ejemplos 1, 2, 3 y 4; el uso de `list` como nombre de variable (L54) se documenta como error en la sección 8 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L292-461) | `REPASO(02)_CLASS_ONE.py` | Recorrido guiado de métodos de lista sobre datos ingresados | Se integró en las tablas de la sección 4 y en los Ejemplos 2 a 5 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Datos_Compuestos.py` (L8-17) | `Ejm_Datos_Compuestos.py` | Mutación de lista por índice frente a la inmutabilidad de la tupla | Es el Ejemplo 1; el contraste completo con tuplas se traslada a [tuplas](../../Intermedio/chapter-one/tuplas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(1).py` (L24-29) | `EJERCICIO(1).py` | Índice negativo (`compañeros[-1][0]`), `sort(key=lambda ...)` | El índice negativo se documenta en la sección 3 y el Ejemplo 1; el orden con `lambda` queda como adelanto hacia [funciones lambda](../../Intermedio/chapter-two/funciones_lambda.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(3.2).py` (L10-18) | `EJERCICIO(3.2).py` | Construcción de lista con `append` dentro de un bucle e intercambio `a, b = b, a + b` | El patrón de acumulación informa el Ejemplo 8; el intercambio se cita en la sección 3 como adelanto de [tuplas](../../Intermedio/chapter-one/tuplas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L41-74) | `Keyword_del.py` | `del` sobre variable, elemento de lista y rebanada de lista | Es el Ejemplo 6 y la fila `del` de la tabla de acceso; el `del` sobre diccionario pertenece a [diccionarios](../../Intermedio/chapter-one/diccionarios.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/INTEGRADAS_FUNCIONES.PY` (L114-138) | `INTEGRADAS_FUNCIONES.PY` | `sum()` sobre listas, tuplas, conjuntos y valores de diccionario (junto a `max`/`min` en el mismo bloque) | Se usa brevemente en el Ejemplo 8; la cobertura completa queda en [funciones integradas](../../Intermedio/chapter-two/funciones_integradas.md) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/One.py` (L50-56) | `One.py` | Agrupación de atributos numéricos en listas (`lista_fuerza`, `lista_vel`) combinada con `sum(...)` y `len(...)` | Conecta las consultas agregadas del Ejemplo 8 con el cálculo de promedios sobre atributos de objetos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L78-80, L99-162, L171-172, L461-608) | `Juego.py` | Gestión dinámica de objetos en `lista_guerrero` (`.append()`, `len()`, indexación, `to_list()`) y conteo de aciertos booleanos con `g1.count(True)` y `g2.count(True)` (L159-161) | Demuestra el uso real de `.count()` sobre listas (Ejemplo 5) y la administración en memoria de colecciones dinámicas a lo largo de un menú interactivo |

**Fundamento complementario:** (1) el modelo de costos asintóticos —`append()` y `pop()` al final operan en `O(1)` amortizado gracias al arreglo dinámico de punteros `PyListObject` con sobreasignación en **CPython**, mientras que `insert(0, ...)` y `pop(0)` cuestan `O(n)` por el desplazamiento de referencias, y la alternativa `collections.deque` pertenece a la **biblioteca estándar**— no se explica en el material y se incorpora en el Ejemplo 7 y en la sección 7; (2) la convención PEP 8 para listas (nombres en `snake_case`, espacios tras las comas y no sobrescribir identificadores integrados como `list`, `dict` o `set`) tampoco se formula explícitamente en las clases.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/introduction.html#lists> — tutorial oficial: listas, indexado, rebanado y operaciones básicas de mutación.
- <https://docs.python.org/3/tutorial/datastructures.html#more-on-lists> — tutorial oficial de estructuras de datos: catálogo completo de métodos de `list`, uso como pilas y colas (`collections.deque`) y sentencia `del`.
- <https://docs.python.org/3/library/stdtypes.html#lists> — referencia oficial del tipo `list` y de las operaciones sobre secuencias mutables en la biblioteca estándar.
