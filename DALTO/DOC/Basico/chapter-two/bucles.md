# Bucles en Python: `while`, `for` y control de flujo

## 2. Introducción

Los programas no solo calculan una vez: muchas tareas exigen **repetir** una acción. Imprimir cien líneas, sumar los valores de una lista, pedir una contraseña hasta que el usuario escriba una válida... Sin repetición, cada programa estaría limitado a ejecutar cada instrucción exactamente una vez y en el orden en que se escribió.

Un **bucle** (del inglés *loop*) es un bloque de instrucciones que se ejecuta varias veces seguidas. Cada paso por el bloque se llama **iteración** (del inglés *iteration*). En lugar de copiar y pegar la misma línea cien veces, se escribe una sola vez dentro de un bucle y Python la repite.

Python ofrece dos bucles:

- **`while`** (en español, "mientras") repite el bloque **mientras una condición sea verdadera**. Una [condición](../chapter-one/condicionales.md) es una expresión que resulta en `True` o `False`, por ejemplo `contador < 10`.
- **`for`** recorre una **secuencia** (una colección ordenada de elementos, como una [cadena de texto](cadenas.md) o una [lista](listas.md)) y ejecuta el bloque una vez **por cada elemento**.

Por qué existen: casi todo dato real llega en cantidad variable (un archivo tiene N filas, un formulario tiene N campos), y un bucle es la única forma de procesar N elementos sin saber N de antemano. Su importancia es estructural: junto con las estructuras condicionales, los bucles son el mecanismo que permite a un programa tomar decisiones **repetidamente** y recorrer datos completos. Son también el primer escalón hacia conceptos superiores: funciones, comprensiones, generadores e iteradores se apoyan en esta base.

## 3. Fundamentos y conceptos

**El ciclo de una iteración.** Todo bucle repite siempre el mismo esquema: (1) evaluar si corresponde continuar, (2) ejecutar el bloque, (3) volver al paso 1. La diferencia entre `while` y `for` está en quién decide el paso 1: en `while` lo decide una condición escrita por quien programa; en `for` lo decide la propia secuencia (cuando se agotan los elementos, el bucle termina).

**`while`: la condición manda.** El bucle `while` evalúa su condición antes de cada vuelta; si es falsa desde el principio, el bloque **no se ejecuta ni una sola vez**. Por eso la condición debe depender de algo que cambie dentro del bloque: si el bloque no modifica lo que se evalúa, el bucle nunca terminará (eso es un **bucle infinito**, tratado en la sección 8).

**Los cuatro patrones de `while`.** El material original los practica todos:

1. **Condición simple:** `while contador < 10:` con un contador que avanza (BUCLE_WHILE.py).
2. **Contador:** se inicializa una variable (`contador = 0`), se prueba (`contador < 10`) y se incrementa dentro del bloque (`contador += 1`).
3. **Centinela** (*sentinel*): un valor especial leído desde los datos (por ejemplo la respuesta `"no"` de un usuario) marca el fin; el bucle se repite **mientras el valor no sea el centinela**. El número de vueltas no se conoce de antemano.
4. **`while True` + `break`:** el bucle se declara "para siempre" y la única salida es una sentencia `break` dentro de una condición. Este patrón hace explícita la salida y es el habitual cuando hay que pedir datos hasta que sean válidos.

**`for`: recorrer una secuencia.** Un objeto es **iterable** cuando puede recorrerse elemento por elemento. Son iterables las cadenas de texto, las listas, las tuplas, los conjuntos, los diccionarios y `range`; los números (`int`, `float`) **no** lo son. Comprobarlo es directo: `iter("hola")` devuelve un iterador y `iter(23)` lanza un error.

**`range`: secuencia de números.** `range(inicio, fin, paso)` genera una sucesión de enteros. La regla que más confunde es que **`fin` es exclusivo**: `range(5, 10)` produce 5, 6, 7, 8 y 9, nunca el 10. Por eso `range(5)` (con un solo argumento) empieza en 0 y produce cinco valores.

**`enumerate` frente a `range(len(...))`.** Para recorrer una lista necesitando a la vez posición y valor hay dos caminos: `range(len(lista))`, que genera los índices y obliga a indexar aparte (`lista[numero]`), y `enumerate(lista)`, que en cada vuelta entrega una tupla `(índice, valor)` lista para desempaquetar. El material los contrasta explícitamente y etiqueta al primero como "forma no óptima". Además, `range(len(...))` es imposible sobre conjuntos (no tienen índice), mientras que `enumerate` funciona sobre cualquier iterable.

**Recorrer diccionarios y conjuntos.** Un `for` sobre un diccionario entrega sus **claves**; con `.items()` entrega pares `(clave, valor)`. Sobre un conjunto entrega sus elementos, pero **sin orden garantizado**: el material recorre conjuntos con `for` y `enumerate`, y en este documento solo se usa el recorrido básico; la teoría de conjuntos pertenece al nivel intermedio.

**`break` y `continue`.** Son sentencias de control que solo existen dentro de un bucle: `break` **termina el bucle de inmediato** (salta a la instrucción siguiente al bucle) y `continue` **abandona la vuelta actual** y pasa a la siguiente sin ejecutar el resto del bloque.

**El `else` del bucle.** `for` y `while` admiten un bloque `else` opcional. Su regla, contraria a la intuición de quien viene de los condicionales, es: **el `else` se ejecuta cuando el bucle terminó sin que ninguna `break` se ejecutara** — ya sea porque la condición se volvió falsa o porque se agotó la secuencia, e incluso si el bucle no llegó a iterar. Si el bucle sale con `break`, el `else` se salta. Por eso sirve como "plan B por defecto": buscar algo y actuar solo si no se encontró.

**Bucles anidados.** Un bucle puede contener a otro. El bucle interno completa **todas** sus vueltas en cada vuelta del externo; es el patrón clásico de las validaciones encadenadas (primero pedir la contraseña, luego pedir su confirmación), tal como hace el material en `BUCLE_WHILE.py`.

**`zip`, en brevedad.** `zip(a, b)` empareja los elementos de dos secuencias posición a posición para recorrerlas juntas en un `for`. Si las longitudes difieren, se detiene en la más corta; el material pide longitudes iguales para no perder datos. El tratamiento completo queda en [desempaquetamiento](../../Intermedio/chapter-one/desempaquetamiento.md).

**El protocolo de iteradores, en una sola idea.** Por debajo, cada `for` obtiene un iterador con el método `__iter__()` y pide el elemento siguiente con `next()` hasta que se agota. Esa mecánica no hace falta para usar los bucles, y su desarrollo completo corresponde a [iteradores](../../Avanzado/chapter-one/iteradores.md); aquí queda solo como presentación, igual que en el material original.

## 4. Sintaxis y funcionamiento

Sintaxis general del bucle `while`:

```text
while <condición>:
    <bloque>
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `while` | Palabra clave que abre el bucle | `while contador < 10:` |
| 2 | Condición | Expresión evaluada **antes de cada vuelta** | `contador < 10` |
| 3 | `:` | Cierra el encabezado; el bloque va indentado debajo | cuatro espacios de sangría |
| 4 | Bloque | Instrucciones que se repiten mientras la condición sea verdadera | `contador += 1` |
| 5 | Actualización | Cambio que acerca la condición a ser falsa; sin ella, bucle infinito | `contador += 1` |

Sintaxis general del bucle `for`:

```text
for <variable> in <secuencia>:
    <bloque>
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `for` | Palabra clave que abre el bucle | `for animal in animales:` |
| 2 | Variable de bucle | Recibe el elemento actual; se reasigna en cada vuelta | `animal` |
| 3 | `in` | Separa la variable de la secuencia a recorrer | `in animales` |
| 4 | Secuencia | Objeto iterable del que se toman los elementos | lista, cadena, `range` |
| 5 | `:` + bloque | Cuerpo indentado, ejecutado una vez por elemento | `print(animal)` |

Argumentos de `range(inicio, fin, paso)`:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `inicio` | Primer valor de la sucesión; es 0 cuando se omite | `range(5)` empieza en 0 |
| 2 | `fin` | Límite superior **exclusivo**: no se incluye | `range(5, 10)` termina en 9 |
| 3 | `paso` | Diferencia entre valores consecutivos; es 1 cuando se omite | `range(5, 106, 20)` |

Elementos de recorrido y control:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `enumerate(secuencia)` | Entrega pares `(índice, valor)` en cada vuelta | `for i, v in enumerate(lista):` |
| 2 | `enumerate(secuencia, inicio)` | Índice inicial opcional (por defecto 0) | `enumerate(lista, 1)` |
| 3 | `range(len(secuencia))` | Genera solo los índices; exige indexar aparte | `lista[numero]` |
| 4 | `break` | Termina el bucle actual de inmediato | dentro de un `if` |
| 5 | `continue` | Abandona la vuelta actual y pasa a la siguiente | dentro de un `if` |
| 6 | `else` de bucle | Se ejecuta solo si el bucle terminó sin `break` | `for ... else:` |

Funcionamiento del `while`: (1) se evalúa la condición; (2) si es verdadera, se ejecuta el bloque completo; (3) se vuelve al paso 1; (4) en cuanto la condición sea falsa, el bucle termina y sigue la instrucción siguiente. Funcionamiento del `for`: (1) Python pide el elemento siguiente a la secuencia; (2) si lo hay, lo asigna a la variable y ejecuta el bloque; (3) repite hasta que la secuencia se agota; (4) si existe un `else`, se ejecuta siempre que no haya habido un `break`.

Detalle de salida útil dentro de bucles: `print` agrega un salto de línea al final, pero admite el parámetro `end` para cambiarlo. El material lo usa para mostrar todas las vueltas en una sola línea:

```python
for letra in "abc":
    print(letra, end="-")
```

Resultado esperado:

```text
a-b-c-
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Contador con `while`.**

```python
contador = 0
while contador < 10:
    contador += 1
    print(contador)
print("El while llegó a su fin.")
```

Explicación línea por línea:

- Línea 1: `contador` se inicializa en 0; sin este valor inicial, la condición de la línea 2 no podría evaluarse (habría una [variable](../chapter-one/variables.md) indefinida).
- Línea 2: `while` evalúa `contador < 10`. Con `contador = 0` es verdadero, así que entra al bloque.
- Línea 3: `contador += 1` suma 1 al contador. Esta es la **actualización**: sin ella, la condición seguiría siendo verdadera para siempre.
- Línea 4: imprime el valor actualizado. Primero se incrementa y luego se imprime, por eso la salida comienza en 1 y no en 0.
- Línea 5: al terminar cada vuelta se vuelve a la línea 2. Cuando `contador` llega a 10, `10 < 10` es falso y el bucle termina.
- Línea 6: está al nivel cero (misma sangría que el `while`), por lo que no forma parte de ningún bucle y se ejecuta una sola vez, después del bucle.

Resultado esperado:

```text
1
2
3
4
5
6
7
8
9
10
El while llegó a su fin.
```

**Ejemplo 2 — `for` recorriendo una lista.**

```python
animales = ["gato", "perro", "loro", "pez"]
for animal in animales:
    print("Ahora la variable animal es igual a: " + animal)
```

Explicación línea por línea:

- Línea 1: se crea la [lista](listas.md) con cuatro elementos; es la secuencia que se va a recorrer.
- Línea 2: en la primera vuelta `animal` vale `"gato"`, en la segunda `"perro"`, y así hasta agotar la lista. Python asigna cada elemento **solo con iterar**: no hay que pedirlo por índice.
- Línea 3: se imprime un mensaje donde se concatena el valor actual de `animal` con `+` (la unión de cadenas se detalla en [cadenas](cadenas.md)).

Resultado esperado:

```text
Ahora la variable animal es igual a: gato
Ahora la variable animal es igual a: perro
Ahora la variable animal es igual a: loro
Ahora la variable animal es igual a: pez
```

**Ejemplo 3 — `range` con paso.**

```python
for numero in range(5, 106, 20):
    print(numero)
```

Explicación línea por línea:

- Línea 1: `range(5, 106, 20)` arranca en 5, avanza de 20 en 20 y se detiene antes de 106.
- Línea 2: imprime cada valor de la sucesión.

La sucesión completa es 5, 25, 45, 65, 85, 105: el siguiente valor sería 125, que ya supera el límite. Nótese que el último valor es **105** y no 106, porque el límite superior es exclusivo. El comentario del material original sobre este mismo `range` afirma "pasos de a 2" y "hasta el 101"; ambos datos son incorrectos (sección 8).

Resultado esperado:

```text
5
25
45
65
85
105
```

**Ejemplo 4 — `continue` y `break`.**

```python
frutas = ["banana", "manzana", "granada", "pera", "durazno"]
print("CON CONTINUE:")
for fruta in frutas:
    if fruta == "granada":
        continue
    print("Voy a comer una: " + fruta)
print("CON BREAK:")
for fruta in frutas:
    print("Voy a comer una: " + fruta)
    if fruta == "granada":
        break
print("Bucle terminado.")
```

Explicación de las decisiones tomadas:

- El primer bucle usa `continue`: al llegar a `"granada"` abandona **esa vuelta** y sigue con `"pera"`; por eso granada no aparece en la salida pero el resto sí.
- El segundo bucle usa `break`: al encontrar `"granada"` termina **todo el bucle**, por eso `"pera"` y `"durazno"` no se procesan.
- La comparación `fruta == "granada"` usa `==` (comparación, no asignación) dentro de un `if`, tal como se vio en [condicionales](../chapter-one/condicionales.md).
- `print("Bucle terminado.")` está fuera de ambos bucles y se imprime siempre.

Resultado esperado:

```text
CON CONTINUE:
Voy a comer una: banana
Voy a comer una: manzana
Voy a comer una: pera
Voy a comer una: durazno
CON BREAK:
Voy a comer una: banana
Voy a comer una: manzana
Voy a comer una: granada
Bucle terminado.
```

### Intermedio

**Ejemplo 5 — Intentos limitados con contador y `break`.**

```python
clave_registrada = "python"
intentos = 0
max_intentos = 3
while intentos < max_intentos:
    intento = input("Ingresa la contraseña: ")
    if intento == clave_registrada:
        print("Acceso concedido.")
        break
    intentos += 1
    print("Contraseña incorrecta. Intentos restantes: " + str(max_intentos - intentos))
if intentos == max_intentos:
    print("Acceso denegado.")
```

Explicación de las decisiones tomadas:

- El bucle se apoya en **dos** mecanismos a la vez: la condición `intentos < max_intentos` (contador) y el `break` (salida anticipada al acertar). Las dos rutas de salida hacen el programa más robusto que cualquiera de ellas sola.
- El contador solo avanza cuando la contraseña es **incorrecta**: no consume intento en el acierto.
- El límite se guarda en `max_intentos` en lugar de escribir el número 3 dentro de la condición; cambiar el límite exige tocar un solo lugar. El material original comete ese error de hardcodeo en `ejercicio1_s3.py` (sección 8).
- Después del bucle, `if intentos == max_intentos` distingue "salí porque se agotaron los intentos" de "salí con `break`". Es el mismo patrón que `EJEM_WHILE.py`.
- Nota didáctica: la clave está a la vista en el código; en un proyecto real las contraseñas jamás se guardan en claro (sección 7).

Con las entradas `no` y `python`, resultado esperado:

```text
Ingresa la contraseña: Contraseña incorrecta. Intentos restantes: 2
Ingresa la contraseña: Acceso concedido.
```

Con tres entradas `no`, resultado esperado:

```text
Ingresa la contraseña: Contraseña incorrecta. Intentos restantes: 2
Ingresa la contraseña: Contraseña incorrecta. Intentos restantes: 1
Ingresa la contraseña: Contraseña incorrecta. Intentos restantes: 0
Acceso denegado.
```

Los mensajes de las entradas aparecen en la misma línea que lo que sigue porque `input()` no imprime salto de línea.

**Ejemplo 6 — Bucle con centinela.**

```python
proceso = "en curso"
while proceso != "fin":
    print("Ciclo de trabajo en marcha.")
    respuesta = input("Repetir el ciclo? (si/no): ")
    if respuesta.strip().lower() == "no":
        proceso = "fin"
print("Proceso finalizado.")
```

Explicación de las decisiones tomadas:

- `proceso` es la **variable centinela**: el bucle continúa mientras su valor no sea `"fin"`. Nadie sabe de antemano cuántas vueltas hará; eso depende del usuario.
- La línea inicial `proceso = "en curso"` es obligatoria: la condición necesita un valor inicial distinto de `"fin"`, de lo contrario el bucle no entraría nunca.
- `respuesta.strip().lower()` normaliza la entrada antes de comparar: `" no "` o `"NO"` deben significar lo mismo que `"no"` (los métodos de cadena se detallan en [cadenas](cadenas.md)).
- A diferencia del Ejemplo 5, aquí no hay `break`: el bucle termina porque la **condición** se volvió falsa. Esa distinción es la que gobierna el `else` de bucle (Ejemplo 10).

Con las entradas `si` y `no`, resultado esperado:

```text
Ciclo de trabajo en marcha.
Repetir el ciclo? (si/no): Ciclo de trabajo en marcha.
Repetir el ciclo? (si/no): Proceso finalizado.
```

**Ejemplo 7 — `enumerate` frente a `range(len(...))`.**

```python
materias = ["Software", "Informática", "Matemáticas"]
for numero, materia in enumerate(materias):
    print(str(numero) + ". " + materia)
print("---")
for numero in range(len(materias)):
    print(str(numero) + ". " + materias[numero])
```

Explicación de las decisiones tomadas:

- `enumerate(materias)` devuelve en cada vuelta una tupla `(índice, valor)` que se **desempaquetan** directamente en `numero` y `materia`. Nótese que la variable `materia` se usa sin volver a indexar: el valor viene gratis.
- El segundo bloque muestra la forma clásica: `range(len(materias))` genera los índices `0, 1, 2` y luego `materias[numero]` recupera el valor. Funciona, pero repite el trabajo y obliga a mantener dos formas de acceder a los mismos datos.
- Ambos caminos imprimen exactamente lo mismo; la diferencia es legibilidad y seguridad (un índice mal escrito en la forma indexing produce un error o el dato equivocado).
- `enumerate` admite un segundo argumento para el inicio del índice (`enumerate(materias, 1)` produce números de 1 en adelante), como usa el material en `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py`.
- Sobre un **conjunto** la primera forma sigue funcionando y la segunda es imposible, porque los conjuntos no admiten acceso por índice.

Resultado esperado (los dos bucles imprimen la misma lista):

```text
0. Software
1. Informática
2. Matemáticas
---
0. Software
1. Informática
2. Matemáticas
```

**Ejemplo 8 — Recorrer un diccionario y `for…else`.**

```python
estudiante = {"nombre": "Ana", "apellido": "Pérez", "edad": 17}
for clave in estudiante:
    print(clave)
print("---")
for clave, valor in estudiante.items():
    print(clave + ": " + str(valor))
else:
    print("No hay más valores en el diccionario.")
```

Explicación de las decisiones tomadas:

- El primer `for` recorre el diccionario **directamente** y entrega sus claves; es la forma más corta de listar las claves.
- `.items()` devuelve pares `(clave, valor)`, que se desempaquetan en dos variables para imprimir ambos. `str(valor)` es necesario porque `edad` es un número y `+` no une texto con números.
- El `else` se ejecuta al final **porque ningún `break` interrumpió el bucle**. Si dentro del bucle hubiera un `break` condicionado, el `else` se saltaría.
- El orden de las claves respeta el orden de inserción, garantizado desde Python 3.7.
- El material presenta este mismo patrón en `BUCLE_FOR.py` L199-209.

Resultado esperado:

```text
nombre
apellido
edad
---
nombre: Ana
apellido: Pérez
edad: 17
No hay más valores en el diccionario.
```

### Avanzado

**Ejemplo 9 — Validación anidada con `while True` y `break`.**

```python
longitud_minima = 6
while True:
    contraseña = input("Crea tu contraseña: ")
    if len(contraseña) >= longitud_minima:
        while True:
            confirmacion = input("Confirma tu contraseña: ")
            if contraseña == confirmacion:
                print("Contraseña registrada.")
                break
            print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        break
    print("La longitud mínima es de " + str(longitud_minima) + " caracteres.")
print("Registro finalizado.")
```

Explicación de las decisiones tomadas:

- Son dos bucles `while True` anidados, cada uno con **una sola responsabilidad**: el externo garantiza la longitud mínima y el interno garantiza la confirmación. Cada `break` cierra solo su propio nivel; por eso hacen falta los dos, uno detrás del otro.
- La salida interna (`break` tras confirmar) no saca del programa: cae en la línea `break` del bucle externo, que a su vez libera el `while True` principal. Es el patrón de validación encadenada de `BUCLE_WHILE.py` L18-45, simplificado.
- Con `longitud_minima` en una variable, el requisito se ajusta en un solo lugar; el material escribe a veces el límite dentro de la condición (sección 8).
- El bucle externo pide de nuevo en cada iteración en lugar de usar una estructura condicional compleja: la lectura vive siempre en la misma línea del flujo.
- Este es el lado educativo del patrón; en producción, comprobar contraseñas contra valores guardados en claro es un anti-patrón de seguridad (sección 7).

Con las entradas `abc`, `secreto` y `secreto`, resultado esperado:

```text
Crea tu contraseña: La longitud mínima es de 6 caracteres.
Crea tu contraseña: Confirma tu contraseña: Contraseña registrada.
Registro finalizado.
```

**Ejemplo 10 — El `else` del bucle como plan B: `for…else` y `while…else`.**

Primer caso, `for…else` sobre un inventario:

```python
productos = ["teclado", "monitor", "mouse", "webcam"]
buscado = "monitor"
for posicion, producto in enumerate(productos):
    if producto == buscado:
        print(buscado + " está en la posición " + str(posicion))
        break
else:
    print("El producto no está en el inventario.")
```

Resultado esperado:

```text
monitor está en la posición 1
```

Si `buscado` fuera `"impresora"`, el `for` terminaría sin `break` y se imprimiría `El producto no está en el inventario.`

Segundo caso, `while…else` con intentos agotados:

```python
secreto = 7
intento = 1
max_intentos = 3
while intento <= max_intentos:
    valor = int(input("Adivina el número (1-10): "))
    if valor == secreto:
        print("Acertaste en el intento " + str(intento) + ".")
        break
    intento += 1
else:
    print("Se agotaron los intentos. El número era " + str(secreto) + ".")
```

Explicación de las decisiones tomadas:

- Ambos casos ilustran la misma regla: el `else` **no** funciona como el `else` de un `if` (que se ejecuta cuando la condición es falsa), sino como un "el bucle terminó y nadie cortó el recorrido".
- En el primer caso, el `break` se dispara **solo** cuando se encuentra el producto; si se encuentra, el `else` se salta. Si no, el `for` se agota y el `else` anuncia la ausencia.
- En el segundo caso, el `break` premia el acierto; si el usuario falla las tres veces, la condición se vuelve falsa **sin** `break` y el `else` comunica el fracaso. Es el mismo esquema que aplica `numero_secreto.py` L42-43 del material, donde la variable aleatoria se genera con el módulo `random` (tema del nivel intermedio).
- `intento += 1` va **después** del `if`, no dentro de su rama de acierto: así el intento acertado tampoco se cuenta de más.
- Con `valor = int(input(...))` se convierte la entrada a número antes de comparar; sin esa conversión, `7 == "7"` sería siempre falso.

Con la entrada `7`, resultado esperado:

```text
Adivina el número (1-10): Acertaste en el intento 1.
```

Con las entradas `1`, `2` y `3`, resultado esperado:

```text
Adivina el número (1-10): Adivina el número (1-10): Adivina el número (1-10): Se agotaron los intentos. El número era 7.
```

**Ejemplo 11 — `while True` con `try`/`except` para leer un índice válido.**

```python
frutas = ["manzana", "pera", "mango"]
while True:
    posicion = input("Ingresa el índice para mostrar el valor: ")
    try:
        posicion = int(posicion)
    except ValueError:
        print("Debes ingresar un número entero.")
        continue
    if 0 <= posicion < len(frutas):
        print("El valor en el índice " + str(posicion) + " es " + frutas[posicion])
        break
    print("Índice fuera de rango. Usa un valor entre 0 y " + str(len(frutas) - 1) + ".")
print("Consulta finalizada.")
```

Explicación de las decisiones tomadas:

- `try`/`except` protege la conversión `int(...)`: si el usuario escribe letras, `int` lanzaría un `ValueError` y detendría el programa. Aquí el `except` lo captura, avisa y el `continue` reinicia la vuelta pidiendo de nuevo.
- El rango se comprueba con la comparación encadenada `0 <= posicion < len(frutas)`, idéntica en espíritu al guard `not(0 <= x <= 5)` del material: Python permite encadenar comparaciones en una sola expresión.
- El `break` solo se alcanza cuando el índice es válido; todas las demás rutas vuelven al inicio del bucle.
- Este patrón está tomado de `REPASO(01).py` L139-152 y de `EJEMPLO_IN.py`. El manejo completo de excepciones (otras clases, `else`, `finally`) corresponde a [excepciones](../../Intermedio/chapter-four/excepciones.md).
- La salida final se escribe fuera del bucle para que se imprima exactamente una vez, sea cual sea el camino seguido.

Con las entradas `a`, `5` y `1`, resultado esperado:

```text
Ingresa el índice para mostrar el valor: Debes ingresar un número entero.
Ingresa el índice para mostrar el valor: Índice fuera de rango. Usa un valor entre 0 y 2.
Ingresa el índice para mostrar el valor: El valor en el índice 1 es pera
Consulta finalizada.
```

## 6. Aplicaciones en el mundo real

- **Procesamiento de registros:** recorrer las filas de un archivo CSV o los resultados de una consulta, una por una, aplicando una regla a cada fila. Es la forma natural de "para cada cliente, generar su factura".
- **Validación de entradas:** formularios, terminales y APIs repiten la petición hasta recibir un dato válido o agotar los intentos (Ejemplos 5, 9 y 11).
- **Reintentos ante fallos transitorios:** consultar un servicio externo con un número máximo de intentos y pausas es el mismo patrón del contador con `break`.
- **Búsqueda:** localizar un elemento en un inventario, un nombre en una lista o una palabra en un texto, con `for…else` como notificación de "no encontrado" (Ejemplo 10).
- **Transformación por lotes:** convertir todas las cadenas de una lista a mayúsculas, filtrar valores fuera de rango o acumular totales: un `for` por colección.
- **Simulaciones y juegos:** turnos que se repiten hasta que alguien gane, contadores de intentos y estados que cambian en cada vuelta.
- **Automatización de escritorio:** renombrar archivos, mover elementos o generar reportes: tareas definidas sobre conjuntos de elementos de tamaño variable.

## 7. Uso en producción

- **Elegir el bucle según el dato:** cuando existe una secuencia conocida (lista, diccionario, líneas de un archivo), el `for` es la opción idiomática y más legible; el `while` corresponde a repeticiones cuyo número depende de una condición en tiempo de ejecución (esperas, reintentos, menús).
- **Garantizar que la condición progresa.** Toda salida debe ser posible: un contador que se incrementa, un centinela que se actualiza o un `break` alcanzable. En programas interactivos se añade además un techo de intentos para que ningún bucle pueda quedar colgado indefinidamente.
- **`while True` + `break` es un patrón aceptado**, siempre que el `break` sea visible y esté condicionado. Ocultar la salida del bucle en efectos secundarios remotos de la condición dificulta su revisión.
- **No mutar la secuencia mientras se recorre.** Agregar o quitar elementos de la lista dentro del `for` que la recorre desplaza los índices y deja elementos sin procesar; la demostración y la solución están en la sección 8.
- **Cuidar el costo de los bucles.** En **CPython** (la implementación de referencia del lenguaje), un bucle `for` ejecuta *bytecode* interpretado en cada iteración —a diferencia de implementaciones alternativas con compilador JIT como PyPy, capaces de compilar bucles frecuentes a código máquina—: resulta apropiado para lógica de control y entrada/salida, pero costoso ante millones de operaciones numéricas. En esos escenarios, las bibliotecas del ecosistema científico (por ejemplo NumPy o Pandas, abordadas en niveles superiores) ofrecen operaciones vectorizadas que delegan el recorrido a rutinas compiladas en C. La regla práctica: el bucle gobierna el flujo; la biblioteca especializada gobierna el cálculo masivo.
- **Nombrar según PEP 8:** variables de bucle en `snake_case` y con nombres de una palabra cuando expresan el elemento (`producto`, `linea`, `intento`); se evita el uso de `l`, `O` e `I`, confundibles con el 1 y el 0. Este criterio de estilo se presenta aquí como fundamento complementario.
- **Probar los casos límite:** secuencia vacía (el cuerpo no se ejecuta, pero el `else` sí), condición falsa desde el primer intento y `break` tomado en la primera vuelta. Las tres rutas cambian el resultado final y suelen ser las que fallan.
- **Depurar por observación:** imprimir la variable de bucle y el estado de la condición en cada vuelta aísla el problema; cuando el bucle no termina, la primera pregunta es "¿qué valor debería cambiar y quién lo cambia".

## 8. Errores comunes y recomendaciones

1. **Olvidar los dos puntos.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, falta los dos puntos del encabezado del bucle
contador = 0
while contador < 5
    contador += 1
```

Salida real: `SyntaxError: expected ':'`. Python exige `:` tanto en `while` como en `for`, `else` de bucle y todo bloque indentado (regla ya vista en [condicionales](../chapter-one/condicionales.md)).

2. **No actualizar la condición dentro del bloque.** Bloque deliberadamente erróneo, **no lo ejecute**: no termina nunca y obliga a interrumpir el programa con Ctrl+C.

```python
    # ERROR INTENCIONAL: bucle infinito, la condición nunca cambia dentro del bloque
contador = 0
while contador < 10:
    print(contador)
```

Diagnóstico: `contador` sigue valiendo 0 en todas las vueltas, así que `contador < 10` es siempre verdadero. La sentencia `contador += 1` debe estar **dentro** del bloque, como en el Ejemplo 1.

3. **Olvidar que el límite de `range` es exclusivo.** Este programa no falla: termina un elemento antes de lo esperado.

```python
for numero in range(1, 5):
    print(numero)
```

Resultado esperado (cuatro valores, no cinco):

```text
1
2
3
4
```

Diagnóstico: quien espera contar del 1 al 5 escribe `range(1, 5)` y obtiene cuatro vueltas. Solución: si el último valor **sí** debe incluirse, usar `range(1, 6)`; conviene escribir en comentario el primer y el último valor esperados.

4. **Replicar el comentario erróneo del material sobre `range`.** En `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` L288-293, `range(5,106,20)` se comenta como "pasos de a 2" y "hasta el 101". El comportamiento real es **paso 20** y **último valor 105** (Ejemplo 3): `5 + 20·n < 106`. Documentar o copiar ese comentario introduce un error de comprensión del tercer argumento de `range`; verificar siempre la sucesión imprimiéndola.

5. **Comparar el contador con la longitud usando `<=`.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: IndexError, la condición permite una vuelta con índice igual a la longitud
numeros = [10, 20, 30]
i = 0
while i <= len(numeros):
    print(numeros[i])
    i += 1
```

Salida real: imprime `10`, `20`, `30` y luego `IndexError: list index out of range`. Diagnóstico: los índices válidos llegan hasta `len(numeros) - 1`; con `<=` se permite la vuelta `i == 3`. Solución: `while i < len(numeros):`. La familia `while ... <= len(...)` es la fuente clásica de errores fuera de rango.

6. **Hardcodear el límite en la comprobación.** `ejercicio1_s3.py` L20 decide con `if(i == 3):` sobre el contador de intentos, de modo que si el usuario pide 5 intentos el mensaje final nunca aparece (o aparece con 3). La corrección es comparar contra la variable que define el límite (`if intentos == max_intentos:`), como en el Ejemplo 5. El problema del hardcodeo en sí ya se señala desde [condicionales](../chapter-one/condicionales.md); aquí afecta además a la lógica de conteo del bucle.

7. **`break` o `continue` fuera de un bucle.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, break solo es válido dentro de un bucle
if True:
    break
```

Salida real: `SyntaxError: 'break' outside loop`. `break` y `continue` pertenecen a la gramática de `for` y `while`; no existen para saltar de un `if`. También producen error si están dentro de una función sin bucle (una función no es un bucle).

8. **Modificar la lista mientras se la recorre.** Este programa no lanza ningún error, pero deja una `banana` sin eliminar:

```python
frutas = ["pera", "banana", "banana", "uva"]
for fruta in frutas:
    if fruta == "banana":
        frutas.remove(fruta)
print(frutas)
```

Resultado esperado (queda una copia sin procesar):

```text
['pera', 'banana', 'uva']
```

Diagnóstico: `remove` acorta la lista mientras `for` avanza sobre ella; el elemento siguiente se desplaza a la posición que el bucle ya pasó, y ese elemento se salta. Solución: recorrer una **copia** (`for fruta in frutas.copy():`), construir una lista nueva o filtrar en una comprensión. El fenómeno se analiza también desde el lado de la mutabilidad en [listas](listas.md).

9. **Interpretar el `else` del bucle como el `else` de un `if`.** Quien espera que `else` signifique "la condición fue falsa" se sorprende: el `else` del bucle se ejecuta **también** cuando el bucle corre completo y termina normalmente (véase el segundo `for` del Ejemplo 8), y **no** se ejecuta cuando hay un `break` (Ejemplo 10). Regla de memoria: `break` cancela el `else`; la finalización normal lo activa.

10. **Esperar un orden determinado sobre conjuntos.** El material recorre conjuntos con `for` y `enumerate` (`BUCLE_FOR.py` L139-172); conviene recordar que el orden de un conjunto no está garantizado, así que "el primer elemento" no significa nada sobre él. Para posiciones estables se usan listas y tuplas.

## 9. Resumen

- Un bucle repite un bloque; cada paso es una iteración. `while` repite mientras una condición sea verdadera; `for` repite una vez por elemento de una secuencia.
- Todo `while` necesita una forma de terminar: una actualización que haga falsa la condición, un centinela leído de los datos o un `break` explícito.
- `range(inicio, fin, paso)` genera enteros con **límite superior exclusivo**; el paso por defecto es 1 y el inicio por defecto es 0.
- `enumerate` entrega `(índice, valor)` en cada vuelta y es preferido a `range(len(...))`, que solo genera índices y exige indexar aparte.
- Los iterables habituales son cadenas, listas, tuplas, conjuntos, diccionarios y `range`; sobre diccionarios `for` recorre claves y `.items()` entrega pares.
- `break` termina el bucle y `continue` salta a la siguiente vuelta; ambos solo existen dentro de un bucle.
- El `else` de `for` y `while` se ejecuta cuando el bucle termina **sin** `break`, incluso sin ninguna iteración.
- Los bucles se anidan: el interno completa todas sus vueltas en cada vuelta del externo; es la base de las validaciones encadenadas.
- Detrás de cada `for` opera el protocolo de iteradores (`__iter__`/`next()`), cuyo detalle corresponde a un nivel avanzado.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L1-36) | `BUCLE_FOR.py` | Definición de iterable, `iter()`, `__iter__()` y `next()` | Se conserva como presentación breve de la sección 3; el desarrollo completo queda en [iteradores](../../Avanzado/chapter-one/iteradores.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L62-72) | `BUCLE_FOR.py` | `zip()` para recorrer dos listas en paralelo | Se resume en la sección 3 con la precisión oficial (se detiene en la secuencia más corta); el detalle queda en [desempaquetamiento](../../Intermedio/chapter-one/desempaquetamiento.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L77-95, L288-293) | `BUCLE_FOR.py` | `range` con inicio, fin y paso | Se documentó la regla del límite exclusivo en la tabla de la sección 4 y se corrigió el comentario erróneo de la L288-293 en la sección 8 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L97-120) | `BUCLE_FOR.py` | Contraste `range(len())` frente a `enumerate` | Se convirtió en el Ejemplo 7, añadiendo el desempaquetamiento directo de la tupla y la imposibilidad de indexar conjuntos |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L122-131) | `BUCLE_FOR.py` | `for…else` | Se explicó su semántica exacta (se ejecuta si no hubo `break`) en la sección 3 y en el Ejemplo 10 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L139-209) | `BUCLE_FOR.py` | Recorrido de conjuntos y diccionarios, `items()`, `else` con diccionario | El diccionario es el Ejemplo 8; el recorrido de conjuntos queda mencionado con la advertencia de orden no garantizado y su teoría va a [conjuntos](../../Intermedio/chapter-one/conjuntos.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L212-262) | `BUCLE_FOR.py` | `continue`, `break` y recorrido de cadenas carácter a carácter | `continue`/`break` son el Ejemplo 4; el recorrido de cadenas se documenta en [cadenas](cadenas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L279-280) | `BUCLE_FOR.py` | `print(end=)` dentro de un bucle | Se muestra ejecutado al final de la sección 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_WHILE.py` (L8-15) | `BUCLE_WHILE.py` | `while` con contador y actualización | Es el Ejemplo 1, con explicación línea por línea |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_WHILE.py` (L18-45) | `BUCLE_WHILE.py` | `while True` + `break` anidados, validación de longitud y símbolos con conjuntos | Se adaptó como Ejemplo 9; la validación con conjunto de símbolos se omite para no duplicar [cadenas](cadenas.md) y [conjuntos](../../Intermedio/chapter-one/conjuntos.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_WHILE.py` (L48-70) | `BUCLE_WHILE.py` | Intentos con contador, `break` y comprobación final | Es el Ejemplo 5, con el límite en variable y sin credenciales en claro |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/EJEMPLO_while_if_elif.py` | `EJEMPLO_while_if_elif.py` | Centinela (`sigue`), guarda `not(0 <= x <= 5)`, `elif` + `break` | Se desarrolló como Ejemplo 6 (centinela) y se citó la comparación encadenada en el Ejemplo 11; el `elif` pertenece a [condicionales](../chapter-one/condicionales.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/EJERCICIO_WHILE.py` (L4-15, L22-24, L32-36) | `EJERCICIO_WHILE.py` | Menú con `while True` + `break`, guardas de entrada anidadas, `round(x, 2)` | Las guardas de ingreso informan el diseño del Ejemplo 9; `round` se cita como función integrada usada en el cálculo de porcentajes |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/ejercicio1_s3.py` (L9-21) | `ejercicio1_s3.py` | Contador con `break` y comprobación de intentos agotados | Se conservó el patrón y se corrigió el hardcodeo `if(i == 3)` en la sección 8 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/ejercicio2_s3.py` (L4-25) | `ejercicio2_s3.py` | Bucle de validación con centinela y comparaciones encadenadas `a > b > c` | Se cita en la sección 3; la notación de comparaciones encadenadas reaparece en el Ejemplo 11 con `0 <= posicion < len(frutas)` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/ejercicio3.py` | `ejercicio3.py` | Bucle que repite hasta obtener dos valores distintos, intercambio con variable temporal | Se cita como ejemplo de centinela numérico; el intercambio se retoma en [listas](listas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLO_IN.py` (L1-17) | `EJEMPLO_IN.py` | `while True` con `try`/`except` y `continue` sobre entrada de datos | Es la base del Ejemplo 11; el catálogo de excepciones queda en [excepciones](../../Intermedio/chapter-four/excepciones.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/EJM_FOR.py` | `EJM_FOR.py` | `zip`, `range`, `enumerate` y `for…else` demostrados | Se integraron en los Ejemplos 7 y 8 y en la sección 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/EJEM_WHILE.py` | `EJEM_WHILE.py` | Contador de intentos con `break` y aviso de intentos restantes | Es el antecedente directo del Ejemplo 5 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/REPASO(01).py` (L139-152) | `REPASO(01).py` | `while True` + `try`/`except` para pedir un índice válido | Se reescribió como Ejemplo 11 con validación de rango explícita |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/RANDOM/numero_secreto.py` (L25-43) | `numero_secreto.py` | `while` con intentos y `else` aplicado al agotar oportunidades | Es el segundo caso del Ejemplo 10, sin dependencia de `random`; ese módulo se estudia en el nivel intermedio |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Polimorfismo.py` (L104-116) | `Polimorfismo.py` | Función `Recorrer(coleccion)` con bloque `for…else` sobre distintas secuencias | Demuestra que el `else` de bucle se ejecuta al agotarse normalmente cualquier iterable recorrido; se profundiza como búsqueda con `break` en el Ejemplo 10 |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L2-31, L210, L482, L522, L530-535, L555, L576) | `Juego.py` | `enumerate(lista_guerrero, 1)` con índice inicial, `for…else` en listados de objetos y menús `while True` con `continue`/`break` y `in range(...)` | Sustenta `enumerate(secuencia, inicio)` en la sección 4 y en el Ejemplo 7, refuerza el uso real de `for…else` e ilustra el límite superior exclusivo de `range(1, 1000)` (sección 8) |

**Fundamento complementario:** (1) la convención PEP 8 para bucles (variables en `snake_case`, sin letras ambiguas, líneas de hasta 79 caracteres) y la distinción de rendimiento entre el *bytecode* interpretado de **CPython** y alternativas JIT o vectorizadas no se enseñan explícitamente en el material original y se presentan en la sección 7; (2) el comportamiento del `else` de bucle cuando el bucle no itera ni una vez tampoco aparece explicado en las clases: se verifica aquí con los Ejemplos 8 y 10.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/controlflow.html> — tutorial oficial: sentencias `for`, `break`/`continue` y el `else` de los bucles, además de la sección sobre `while`.
- <https://docs.python.org/3/library/functions.html#func-range> — referencia oficial de la función integrada `range`.
- <https://docs.python.org/3/library/functions.html#print> — referencia oficial de `print`, incluido el parámetro `end`.
