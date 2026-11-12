# Comprensiones y Expresiones Generadoras en Python

## 2. Introducción

Una de las operaciones más frecuentes en programación consiste en partir de una colección existente, seleccionar algunos de sus elementos según un criterio y transformar cada uno para construir una colección nueva: convertir una lista de cadenas numéricas `"10, 20, 30"` en enteros `[10, 20, 30]`, elevar al cuadrado solo los números pares o formatear los pares de un diccionario como líneas de texto. Con las herramientas del nivel básico, cada una de estas tareas exige crear una colección vacía, abrir un [bucle](../../Basico/chapter-two/bucles.md) `for`, anidar un [condicional](../../Basico/chapter-one/condicionales.md) `if` e invocar `.append()` en cada vuelta.

Las **comprensiones** (*comprehensions*) son construcciones declarativas del lenguaje Python —inspiradas en la notación matemática de conjuntos por comprensión— que permiten **crear listas, conjuntos y diccionarios nuevos a partir de cualquier iterable en una sola expresión concisa y legible**. Junto a ellas, la misma gramática entre paréntesis da origen a las **expresiones generadoras** (*generator expressions*), que producen los resultados uno a uno bajo demanda sin almacenarlos todos en memoria.

¿Por qué existen y cuál es su importancia dentro de Python?

1. **Expresan el "qué" antes que el "cómo":** al colocar al inicio la expresión resultante (`[num ** 2 for num in numeros if num % 2 == 0]`), quien lee el código comprende de inmediato qué contiene la nueva colección sin rastrear mutaciones paso a paso.
2. **Previenen errores de inicialización:** eliminan variables acumuladoras vacías y evitan trampas de referencias compartidas al construir matrices o diccionarios de listas.
3. **Eficiencia de ejecución y memoria:** las listas por comprensión aprovechan instrucciones internas especializadas en **CPython**, mientras que las expresiones generadoras procesan flujos extensos con consumo mínimo de memoria RAM, razón por la cual aparecen constantemente junto a `.join()`, `sum()`, `any()` y `all()`.

## 3. Fundamentos y conceptos

**Del bucle imperativo a la comprensión de lista (PEP 202).** Tal como contrasta detalladamente `CREAR_FUNCIONES.py` (L165-207), todo patrón imperativo de acumulación:

```text
resultado = []
for elemento in iterable:
    if condicion:
        resultado.append(transformacion)
```

se expresa de forma equivalente mediante una **lista por comprensión** (*list comprehension*):

```text
resultado = [transformacion for elemento in iterable if condicion]
```

La cláusula `if condicion` final es opcional: si se omite (`[x * 2 for x in numeros]`, como en `BUCLE_FOR.py` L273), se transforman todos los elementos del iterable; si se incluye, actúa como **filtro** dejando pasar únicamente los elementos donde `condicion` evalúa como verdadera.

**Filtro al final frente a expresión condicional al inicio.** Una duda muy común surge al querer usar `else` dentro de una comprensión. Es fundamental distinguir dos construcciones diferentes del lenguaje:

- **Filtrado (`if` al final, sin `else`):** `[x for x in datos if x > 0]` decide **si el elemento entra o se descarta**. Puede producir una lista más corta que la original; escribir `else` al final constituye un `SyntaxError`.
- **Transformación condicional (`a if cond else b` al inicio):** `["par" if x % 2 == 0 else "impar" for x in datos]` coloca una **expresión condicional ternaria** (estudiada en [condicionales](../../Basico/chapter-one/condicionales.md)) como valor calculado. Aquí **ningún elemento se descarta**: la lista resultante conserva exactamente la misma longitud que la entrada, eligiendo entre dos valores posibles en cada paso. Ambas piezas pueden incluso combinarse: `[x if x > 0 else 0 for x in datos if x is not None]`.

**Comprensiones de conjuntos y de diccionarios (PEP 274).** Python extiende exactamente la misma estructura sintáctica a las demás colecciones mutables del capítulo:

- **Comprensión de conjunto (*set comprehension*):** se escribe entre llaves `{expresion for item in iterable if condicion}` y construye un [conjunto](conjuntos.md) `set`, eliminando automáticamente cualquier resultado duplicado.
- **Comprensión de diccionario (*dict comprehension*):** se escribe entre llaves separando clave y valor con dos puntos `{clave_expr: valor_expr for item in iterable if condicion}` y construye un [diccionario](diccionarios.md) `dict`. Resulta además la solución correcta para crear listas independientes por clave (`{k: [] for k in claves}`), evitando la referencia compartida de `dict.fromkeys(claves, [])`.

**¿Por qué `(x for x in iterable)` NO es una comprensión de tupla? Expresiones generadoras (PEP 289).** Al ver `[...]` para listas y `{...}` para conjuntos, suele suponerse que `(...)` crea una [tupla](tuplas.md). En Python no es así: escribir `(x * 2 for x in numeros)` construye una **expresión generadora** (*generator expression*), un objeto iterador de **evaluación perezosa** (*lazy evaluation*). En lugar de calcular todos los valores de golpe y guardarlos en memoria, la expresión generadora entrega cada elemento **solo en el instante en que alguien lo solicita** y **una única vez** (tras recorrerla, queda agotada).

Esta característica explica el patrón presente tanto en `CLASES_PYTHON` (`CLASE_ONE.py` L619-660) como en `CLASS_PY_POO` (`Decoradores_Multiples.py` L177, `Juego.py` L167, `Crear_Clase.py` L91, `Decorador_Property.py` L32 y `Herencia_Multiple.py` L83):

```text
", ".join(str(x) for x in lista_1)
"\n".join(f"{key}: {value}" for key, value in dicci.items())
```

Según la gramática de PEP 289, cuando una expresión generadora es el **único argumento** dentro de la llamada a una función o método, los paréntesis propios de la llamada bastan y no hace falta escribir doble paréntesis `join((str(x) ...))`. Si realmente se desea materializar una tupla en memoria, se pasa la expresión generadora al constructor integrado: `tuple(x * 2 for x in numeros)`. El estudio profundo de los generadores corresponde a [iteradores](../../Avanzado/chapter-one/iteradores.md).

**Ámbito local aislado en Python 3.** En un bucle `for x in range(5):` ordinario, la variable `x` permanece viva después del bucle en el ámbito circundante con el valor `4`. En cambio, en Python 3 todas las comprensiones y expresiones generadoras evalúan sus variables de iteración dentro de un **ámbito léxico aislado**: la variable `x` de `[x * 2 for x in range(5)]` no se filtra hacia afuera ni sobrescribe otra variable llamada `x` definida antes en la misma función o módulo (el funcionamiento general de los ámbitos se desarrolla en [ámbito de variables](../chapter-two/ambito_variables.md)).

**Bucles múltiples en comprensiones.** Una comprensión admite varios bloques `for` seguidos: `[elemento for fila in matriz for elemento in fila]`. La regla para leerlos sin confusión es que **se escriben en el mismo orden de arriba hacia abajo que tendrían los bucles `for` anidados tradicionales**: el primer `for` es el bucle externo y el segundo `for` es el interno. Muy distinto es anidar corchetes dentro de la expresión inicial (`[[0 for _ in range(3)] for _ in range(2)]`), lo cual construye una lista de listas (matriz) evaluando una comprensión interna completa por cada paso de la externa.

**Rendimiento interno: lenguaje frente a CPython.** El lenguaje Python define que una comprensión equivale semánticamente a construir la colección iterando sobre el origen. A nivel de implementación en **CPython**, las listas por comprensión se compilan empleando la instrucción de *bytecode* especializada `LIST_APPEND` (y desde **CPython 3.12**, PEP 709 ejecuta la comprensión *inline* dentro del marco actual conservando el aislamiento de variables, sin el costo de invocar un objeto función auxiliar), lo que evita buscar repetidamente el atributo `.append` en cada iteración y ofrece un menor tiempo de ejecución que el bucle manual equivalente.

## 4. Sintaxis y funcionamiento

Formas sintácticas de las cuatro variantes:

```text
lista = [<expresion> for <variables> in <iterable> if <filtro>]
conjunto = {<expresion> for <variables> in <iterable> if <filtro>}
diccionario = {<clave>: <valor> for <variables> in <iterable> if <filtro>}
generador = (<expresion> for <variables> in <iterable> if <filtro>)
```

Comparativa estructural de las variantes disponibles:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `[expr for x in it]` | **Comprensión de lista**: evalúa de inmediato y devuelve `list` | `[n * 2 for n in [1, 2, 3]]` |
| 2 | `[expr for x in it if c]` | Filtra solo los elementos donde `c` es verdadera y devuelve `list` | `[n for n in range(6) if n % 2 == 0]` |
| 3 | `[a if c else b for x in it]` | Transforma **todos** los elementos eligiendo entre `a` y `b` | `["sí" if n > 0 else "no" for n in [-1, 2]]` |
| 4 | `{expr for x in it}` | **Comprensión de conjunto**: evalúa de inmediato y devuelve `set` sin duplicados | `{palabra.lower() for palabra in lista}` |
| 5 | `{k: v for x in it}` | **Comprensión de diccionario**: evalúa de inmediato y devuelve `dict` | `{x: x ** 2 for x in range(3)}` |
| 6 | `(expr for x in it)` | **Expresión generadora**: perezosa, de un solo recorrido; devuelve `generator` | `gen = (x * x for x in range(1000))` |
| 7 | `func(expr for x in it)` | Expresión generadora directa como argumento único de una función | `", ".join(str(x) for x in datos)` |
| 8 | `[e for f in m for e in f]` | Aplanamiento con múltiples `for` (externo a la izquierda, interno a la derecha) | `[n for fila in [[1, 2], [3]] for n in fila]` |

Componentes internos de una comprensión y orden de evaluación:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `<iterable>` | Se evalúa primero para obtener el iterador fuente | `numeros.split(",")` |
| 2 | `for <variables> in` | Extrae cada elemento (admite [desempaquetamiento](desempaquetamiento.md) como `k, v`) | `for clave, valor in d.items()` |
| 3 | `if <filtro>` (opcional) | Si es falso, descarta el elemento actual y pasa a la siguiente iteración | `if valor >= 18` |
| 4 | `<expresion>` | Solo se calcula para los elementos que superaron el filtro | `int(num.strip())` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Transformación, limpieza de texto y filtrado en listas por comprensión.**

```python
numeros = [1, 2, 3, 4, 5, 6]
duplicados = [x * 2 for x in numeros]
cuadrados_pares = [num ** 2 for num in numeros if num % 2 == 0]

entrada_csv = " 10, 25 , 40 , 5 "
enteros_limpios = [int(fragmento.strip()) for fragmento in entrada_csv.split(",")]

print("Duplicados:", duplicados)
print("Cuadrados de pares:", cuadrados_pares)
print("Enteros desde texto:", enteros_limpios, "| Suma:", sum(enteros_limpios))
```

Explicación línea por línea:

- Líneas 1-2: reproducen el caso inicial de `BUCLE_FOR.py` (L270-273), multiplicando cada elemento de `numeros` por `2`.
- Línea 3: aplica el filtro `if num % 2 == 0` (`CREAR_FUNCIONES.py` L169); solo `2`, `4` y `6` pasan el filtro y se elevan al cuadrado (`4`, `16`, `36`).
- Líneas 5-6: adaptan de forma determinista el flujo de `CREAR_FUNCIONES.py` (L149): `entrada_csv.split(",")` separa la cadena por comas, `.strip()` quita espacios laterales y `int(...)` convierte cada texto en número entero.
- Líneas 8-10: muestran las tres listas generadas y la suma total (`80`).

Resultado esperado:

```text
Duplicados: [2, 4, 6, 8, 10, 12]
Cuadrados de pares: [4, 16, 36]
Enteros desde texto: [10, 25, 40, 5] | Suma: 80
```

**Ejemplo 2 — Diferencia entre filtrar al final y clasificar con `if ... else` al inicio, más aislamiento de ámbito.**

```python
x = "valor_externo_intacto"
notas = [18, 9, 14, 7, 20]

aprobadas = [x for x in notas if x >= 11]
etiquetas = ["Aprobado" if x >= 11 else "Desaprobado" for x in notas]

print("Solo aprobadas (filtrada):", aprobadas)
print("Todas etiquetadas:", etiquetas)
print("Variable externa x:", x)
```

Explicación línea por línea:

- Línea 1: define una variable `x` en el ámbito principal antes de las comprensiones.
- Línea 4: el `if x >= 11` al final descarta `9` y `7`, reduciendo la lista de cinco a tres elementos.
- Línea 5: la expresión ternaria `"Aprobado" if x >= 11 else "Desaprobado"` al inicio clasifica las cinco notas sin descartar ninguna.
- Línea 9: comprueba que `x` fuera de las comprensiones conserva `"valor_externo_intacto"`, demostrando el aislamiento de ámbito de Python 3.

Resultado esperado:

```text
Solo aprobadas (filtrada): [18, 14, 20]
Todas etiquetadas: ['Aprobado', 'Desaprobado', 'Aprobado', 'Desaprobado', 'Aprobado']
Variable externa x: valor_externo_intacto
```

### Intermedio

**Ejemplo 3 — Comprensiones de conjunto y de diccionario para normalizar e invertir datos.**

```python
correos_crudos = [" Ana@Mail.com ", "LUIS@mail.com", "ana@mail.com", "marta@mail.com "]
correos_unicos = {correo.strip().lower() for correo in correos_crudos}
print("Correos normalizados únicos:", sorted(correos_unicos))

precios_soles = {"teclado": 120, "monitor": 900, "cable": 25, "laptop": 3500}
catalogo_premium = {prod: round(precio / 3.75, 2) for prod, precio in precios_soles.items() if precio >= 100}
indice_inverso = {valor: clave for clave, valor in precios_soles.items()}

print("Premium en USD:", catalogo_premium)
print("Producto de S/ 900:", indice_inverso[900])
```

Explicación de las decisiones tomadas:

- La comprensión de conjunto `{correo.strip().lower() ...}` limpia espacios, unifica minúsculas y descarta el duplicado de `"ana@mail.com"` en un solo paso declarativo.
- `catalogo_premium` recorre `precios_soles.items()` desempaquetando `prod, precio`, filtra artículos desde `100` soles y calcula el equivalente redondeado en dólares como nuevo diccionario.
- `indice_inverso` intercambia `{valor: clave ...}`, patrón habitual cuando los valores son únicos y se requiere consultar rápidamente a qué clave pertenece un código o importe determinado.

Resultado esperado:

```text
Correos normalizados únicos: ['ana@mail.com', 'luis@mail.com', 'marta@mail.com']
Premium en USD: {'teclado': 32.0, 'monitor': 240.0, 'laptop': 933.33}
Producto de S/ 900: monitor
```

**Ejemplo 4 — Expresiones generadoras dentro de `.join()` en clases y reportes.**

```python
class FichaJugador:
    def __init__(self, nombre, fuerza, velocidad):
        self.nombre = nombre
        self.fuerza = fuerza
        self.velocidad = velocidad

    def resumen_linea(self):
        estadisticas = {"Nombre": self.nombre, "Fuerza": self.fuerza, "Velocidad": self.velocidad}
        return " || ".join(f"{clave}: {valor}" for clave, valor in estadisticas.items())


jugador = FichaJugador("Goku", 95, 88)
print(jugador.resumen_linea())

codigos = (101, 204, 309)
print("Códigos CSV:", ", ".join(str(c) for c in codigos))
```

Explicación de las decisiones tomadas:

- Este ejemplo sintetiza el idioma transversal que une `CLASE_ONE.py` (L619-660) con `Juego.py` (L167), `Decoradores_Multiples.py` (L177), `Crear_Clase.py` (L91) y `Decorador_Property.py` (L32).
- El método `str.join()` exige que todos los elementos entregados sean cadenas (`str`). Al escribir `" || ".join(f"{clave}: {valor}" for clave, valor in estadisticas.items())`, la expresión generadora formatea cada par al vuelo sin crear primero una lista auxiliar innecesaria (si bien internamente **CPython** puede materializar una secuencia temporal cuando `str.join` necesita calcular en dos pasadas la longitud exacta de la cadena final, en funciones consumidoras de una sola pasada como `sum()`, `any()` o `all()` el ahorro de memoria es estrictamente `O(1)`).

Resultado esperado:

```text
Nombre: Goku || Fuerza: 95 || Velocidad: 88
Códigos CSV: 101, 204, 309
```

### Avanzado

**Ejemplo 5 — Procesamiento perezoso en memoria constante frente a listas y creación segura de matrices.**

```python
import sys

lista_cuadrados = [n * n for n in range(10_000)]
gen_cuadrados = (n * n for n in range(10_000))

print("Generador usa menos RAM que lista:", sys.getsizeof(gen_cuadrados) < sys.getsizeof(lista_cuadrados))
print("Suma desde generador:", sum(gen_cuadrados))
print("Segunda suma sobre generador agotado:", sum(gen_cuadrados))

tablero = [[0 for _ in range(3)] for _ in range(2)]
tablero[0][1] = 9
print("Matriz con filas independientes:", tablero)
```

Explicación de rendimiento y mantenibilidad:

- `lista_cuadrados` reserva espacio inmediato para diez mil enteros en memoria, mientras que `gen_cuadrados` almacena únicamente el estado de iteración (unos pocos cientos de bytes constantes en **CPython**, sea el rango de diez mil o de cien millones).
- Al ejecutar el primer `sum(gen_cuadrados)`, Python consume los valores uno por uno y obtiene `333283335000`. La línea siguiente demuestra una propiedad crítica de los generadores: **son iteradores de un solo uso**; una vez recorridos quedan exhaustos y el segundo `sum(gen_cuadrados)` devuelve `0`. Cuando una colección debe recorrerse múltiples veces o indexarse con `[i]`, se requiere una comprensión de lista; cuando se consume una sola vez en `sum()`, `max()`, `min()`, `any()` o `all()`, la expresión generadora es superior en escalabilidad.
- Finalmente, `[[0 for _ in range(3)] for _ in range(2)]` construye dos listas internas distintas: modificar `tablero[0][1] = 9` no contamina `tablero[1]`, evitando el clásico fallo de escribir `[[0] * 3] * 2` (que repite dos referencias hacia la misma fila).

Resultado esperado:

```text
Generador usa menos RAM que lista: True
Suma desde generador: 333283335000
Segunda suma sobre generador agotado: 0
Matriz con filas independientes: [[0, 9, 0], [0, 0, 0]]
```

## 6. Aplicaciones en el mundo real

- **Ingesta y saneamiento de datos (ETL):** limpiar espacios, descartar líneas vacías o comentarios (`[linea.strip() for linea in archivo if linea.strip() and not linea.startswith("#")]`) y convertir tipos al leer archivos de texto o CSV.
- **Transformación de respuestas en APIs backend:** proyectar listas de entidades de base de datos u objetos de dominio hacia diccionarios resumidos listos para serializar a JSON (`[{"id": u.id, "nombre": u.nombre} for u in usuarios if u.activo]`).
- **Agregaciones sobre grandes volúmenes:** calcular totales financieros (`sum(p.subtotal for p in pedidos if p.pagado)`) o verificar invariantes de negocio (`all(item.stock > 0 for item in carrito)`) con expresiones generadoras sin duplicar colecciones en memoria.
- **Formateo de salidas textuales, consultas y reportes:** ensamblar representaciones `__str__` de objetos o fragmentos de texto unidos mediante `"\n".join(...)`, tal como muestran los ejercicios de POO del material original.
- **Construcción de índices de búsqueda rápida:** transformar una lista de objetos en un diccionario indexado por identificador (`{producto.sku: producto for producto in catalogo}`) para acelerar búsquedas posteriores a `O(1)`.

## 7. Uso en producción

- **Límite de legibilidad (regla de las dos cláusulas):** las guías de estilo profesionales (PEP 8 y *Google Python Style Guide*) recomiendan evitar comprensiones que combinen más de dos cláusulas `for` o múltiples filtros complejos. Si una comprensión obliga a desplazarse horizontalmente o cuesta más de unos segundos entenderla, un bucle `for` explícito con variables intermedias bien nombradas o una función auxiliar resulta mucho más mantenible.
- **Jamás emplear comprensiones por sus efectos secundarios:** escribir `[print(item) for item in lista]` o `[guardar_en_bd(u) for u in usuarios]` es una mala práctica severa en producción: además de ocultar que el objetivo es ejecutar una acción y no construir datos, reserva en memoria una lista inútil `[None, None, ...]` del tamaño total de la entrada. Para efectos secundarios se utiliza siempre un bucle `for` ordinario.
- **Evitar recalcular expresiones costosas dos veces por elemento:** en `[calcular(x) for x in datos if calcular(x) > 0]` la función `calcular(x)` se ejecuta **por duplicado** en cada elemento válido. En Python 3.8+ puede evitarse con el operador de asignación `:=` (`[res for x in datos if (res := calcular(x)) > 0]`) o separando el cálculo en una expresión generadora previa.
- **Preferir comprensiones frente a `map()` y `filter()` con `lambda`:** mientras en `LAMBDA_FUNCIONES.py` se estudia `list(filter(lambda n: n % 2 == 0, listado))` con fines formativos (tema desarrollado en [funciones lambda](../chapter-two/funciones_lambda.md)), en Python idiomático `[n for n in listado if n % 2 == 0]` es más directo, evita el costo de invocar una función `lambda` por elemento y permite combinar filtrado y transformación en un mismo lugar.

## 8. Errores comunes y recomendaciones

1. **Colocar `else` al final de una comprensión de filtrado.**

```python
# ERROR INTENCIONAL: SyntaxError al escribir else en la posición del filtro final
numeros = [1, 2, 3, 4]
resultado = [n for n in numeros if n % 2 == 0 else 0]
```

Diagnóstico: lanza `SyntaxError: invalid syntax`. El `if` situado después del `for` solo filtra qué elementos pasan; no admite rama `else`. Solución: cuando se requiere un valor alternativo con `else`, trasladar la expresión condicional completa **antes** del `for`: `[n if n % 2 == 0 else 0 for n in numeros]`.

2. **Reutilizar una expresión generadora creyendo que almacena los elementos como una lista.**

```python
pares_gen = (n for n in [1, 2, 3, 4] if n % 2 == 0)
primera_lectura = list(pares_gen)
segunda_lectura = list(pares_gen)

print("Primera lectura:", primera_lectura)
print("Segunda lectura:", segunda_lectura)
```

Resultado esperado:

```text
Primera lectura: [2, 4]
Segunda lectura: []
```

Diagnóstico: `pares_gen` es un iterador de un solo paso; `primera_lectura` consumió todos sus elementos y `segunda_lectura` lo encuentra vacío (`[]`), sin lanzar error alguno. Solución: usar `[...]` (comprensión de lista) siempre que los resultados deban consultarse más de una vez, medir su longitud con `len()` o indexarse por posición.

3. **Invertir el orden de los bucles `for` al aplanar listas anidadas.**

```python
# ERROR INTENCIONAL: NameError porque 'fila' se usa antes del for que la define
matriz = [[1, 2], [3, 4]]
plana = [num for num in fila for fila in matriz]
```

Diagnóstico: lanza `NameError: name 'fila' is not defined`. A diferencia del inglés coloquial, en Python las cláusulas `for` dentro de una comprensión se leen **de izquierda a derecha desde el bucle más externo hacia el más interno**. Solución: escribir `[num for fila in matriz for num in fila]`.

4. **Olvidar los paréntesis al crear tuplas dentro de una comprensión.**

```python
# ERROR INTENCIONAL: SyntaxError al escribir una coma suelta en la expresión inicial
pares = [x, x ** 2 for x in range(3)]
```

Diagnóstico: lanza `SyntaxError: did you forget parentheses around the comprehension target?`. Dentro del encabezado de una comprensión, la coma suelta resultaría ambigua para el analizador sintáctico. Solución: encerrar siempre las tuplas producidas entre paréntesis explícitos: `[(x, x ** 2) for x in range(3)]`.

5. **Construir matrices 2D multiplicando listas mutables en vez de usar una comprensión.** Escribir `matriz = [[0] * 3] * 2` crea dos referencias hacia **la misma fila**; modificar `matriz[0][0] = 1` altera también `matriz[1][0]`. Como se mostró en el Ejemplo 5, usar `[[0 for _ in range(3)] for _ in range(2)]` o `[[0] * 3 for _ in range(2)]` garantiza que cada fila sea una lista nueva e independiente.

## 9. Resumen

- Las **comprensiones** construyen colecciones nuevas de forma declarativa combinando iteración, transformación y filtrado opcional en una sola expresión.
- Existen tres tipos de comprensiones evaluadas de inmediato en memoria: **de lista** `[expr for ...]`, **de conjunto** `{expr for ...}` y **de diccionario** `{k: v for ...}`.
- Un `if` **al final** filtra elementos (sin `else`); una expresión `a if cond else b` **al inicio** transforma todos los elementos sin cambiar la longitud.
- Escribir paréntesis `(expr for ...)` crea una **expresión generadora** perezosa y de un solo recorrido (no una tupla), ideal como argumento directo de `.join()`, `sum()`, `any()`, `all()` o `tuple(...)`.
- En Python 3, las variables de iteración de comprensiones y expresiones generadoras tienen **ámbito local propio** y no contaminan el entorno exterior.
- Por mantenibilidad, deben reservarse para crear datos (nunca para efectos secundarios como `print()`) y sustituirse por bucles `for` convencionales cuando la lógica supere dos niveles de complejidad.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L266-275) | `BUCLE_FOR.py` | Introducción a la lista por comprensión `[x*2 for x in numeros]` como transformación en una línea | Se explicó su semántica declarativa, aislamiento de ámbito en Python 3 y optimización `LIST_APPEND` en **CPython** |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CREAR_FUNCIONES.py` (L149, L159-208) | `CREAR_FUNCIONES.py` | Sintaxis `[nuevo_elemento for elemento in iterable if condición]`, conversión `[int(num.strip()) for num in numeros.split(",")]`, filtrado de pares y comparación frente al bucle con `.append()` | Se contrastó el filtro `if` final frente a la expresión condicional `a if cond else b` al inicio (Ejemplo 2 y sección 8) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/LAMBDA_FUNCIONES.py` (L34-100) | `LAMBDA_FUNCIONES.py` | Filtrado funcional con `filter(...)` convertido a `list` y `tuple` | Se relacionó en la sección 7 como alternativa funcional frente a la claridad idiomática de las comprensiones |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L618-661) | `CLASE_ONE.py` | Expresiones generadoras pasadas directamente a `", ".join(str(x) for x in ...)` sobre listas, tuplas, conjuntos, `.values()` e `.items()` | Se identificó explícitamente que `str(x) for x in ...` dentro de `.join(...)` es una expresión generadora (PEP 289) y no una comprensión de lista |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L177) | `Decoradores_Multiples.py` | Formateo de atributos en `__str__()` con `"\n".join(f"{key}: {value}" for key,value in dicci.items())` | Integrado en el Ejemplo 4 como patrón estándar de presentación en clases |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L167) | `Juego.py` | Construcción de reporte de batalla `" \|\| ".join(f"{key}: {value}" for key,value in dicci.items())` | Reproducido de forma autocontenida en el método `resumen_linea()` del Ejemplo 4 |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Crear_Clase.py` (L91) | `Crear_Clase.py` | Expresión generadora sobre `(roca_One.__dict__).items()` dentro de `"\n".join(...)` | Vincula expresiones generadoras, desempaquetamiento e introspección de instancias |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L32) | `Decorador_Property.py` | Expresión generadora dentro de una propiedad `@property` para serializar datos del objeto | Demuestra su uso idiomático en métodos de consulta de POO |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Herencia_Multiple.py` (L83) | `Herencia_Multiple.py` | Formateo con `"\n".join(f"{key}: {values}" for key, values in valores_dict)` en jerarquías de herencia | Confirma la consistencia del patrón en todo el bloque de POO |

**Fundamento complementario:** mientras `CLASES_PYTHON/` enseña listas por comprensión y ambos directorios emplean expresiones generadoras dentro de `.join(...)` sin nombrarlas teóricamente como tales, se añadieron como fundamento complementario: (1) las **comprensiones de conjuntos** (`{...}`) y **de diccionarios** (`{k: v ...}`, PEP 274) como extensiones directas de la misma gramática; (2) la distinción conceptual y de memoria entre comprensiones ansiosas y **expresiones generadoras perezosas** de un solo recorrido (PEP 289); (3) la regla de aislamiento léxico de la variable de iteración en Python 3; y (4) el orden de evaluación en comprensiones anidadas y la creación segura de matrices 2D.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions> — Tutorial oficial de Python: listas por comprensión, filtrado, bucles anidados y comprensiones de conjuntos y diccionarios.
- <https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries> — Referencia formal del lenguaje: gramática, alcance léxico y orden de evaluación de comprensiones y expresiones generadoras.
- <https://peps.python.org/pep-0202/> — PEP 202 (*List Comprehensions*): diseño original de las listas por comprensión en Python.
- <https://peps.python.org/pep-0274/> — PEP 274 (*Dict Comprehensions*): extensión de la sintaxis de comprensión hacia diccionarios.
- <https://peps.python.org/pep-0289/> — PEP 289 (*Generator Expressions*): especificación de las expresiones generadoras perezosas y su uso directo como argumentos de funciones.
