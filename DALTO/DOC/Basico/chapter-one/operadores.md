# Operadores en Python

## 2. Introducción

Un **operador** es un símbolo que realiza una operación sobre uno o más valores: `+` suma, `>` compara, `and` combina condiciones. Los valores sobre los que actúa se llaman **operandos**, y la combinación operador + operandos que produce un nuevo valor se llama **expresión**: `12 + 5` es una expresión que vale `17`.

Python agrupa sus operadores en familias: **aritméticos** (calcular), **comparación** (comparar y producir `True`/`False`), **lógicos** (`and`, `or`, `not`: combinar condiciones), **de pertenencia** (`in`, `not in`: preguntar si un valor está contenido), **de identidad** (`is`: preguntar si dos nombres apuntan al mismo objeto) y **de asignación** (`=`, `+=`...: guardar resultados, tratados en [variables](variables.md)).

Por qué existen: sin operadores, cada cálculo requeriría funciones verbosas y cada comparación sería un procedimiento aparte; los símbolos hacen que el código se lea como matemática familiar. Su importancia en Python es central: los operadores de comparación devuelven booleanos, que a su vez alimentan las [condicionales](condicionales.md), y los operadores lógicos deciden qué combinación de condiciones se considera verdadera.

## 3. Fundamentos y conceptos

**Operadores aritméticos.** La materia original del curso lista ocho operaciones: suma `+`, resta `-`, multiplicación `*`, división `/`, división entera `//`, módulo `%`, potencia `**` y raíz como potencia fraccionaria (`x ** (1 / n)`). Reglas que suelen sorprender:

- `/` **siempre** devuelve `float`: `12 / 5` es `2.4` y `10 / 2` es `5.0`, aunque la división sea exacta.
- `//` devuelve la parte entera redondeada **hacia abajo** (hacia menos infinito): `17 // 5` es `3`, y con negativos `-7 // 2` es `-4`, no `-3`.
- `%` devuelve el resto de la división, y su signo sigue al **divisor**: `-7 % 2` es `1`.
- `**` es potencia: `12 ** 5` es `248832`; la raíz cuadrada de `x` es `x ** (1 / 2)`.
- Los operandos de distinto tipo numérico se combinan sin problema (`5 + 2.0` → `7.0`), pero texto y número no se mezclan con `+` (ver sección 8).

**Operadores de comparación.** Seis símbolos: `==` (igual), `!=` (distinto), `>`, `<`, `>=`, `<=`. Todos devuelven **booleano** (`True` o `False`), nunca modifican los operandos. Funcionan también con cadenas: la comparación es **lexicográfica**, es decir, orden alfabético carácter por carácter (`"abc" < "abd"` → `True`), no valor numérico. Python permite encadenar comparaciones de forma legible: `1 < 2 < 3` equivale a `1 < 2 and 2 < 3`.

**Operadores lógicos.** `and` solo es `True` cuando **ambos** lados lo son; `or` es `True` cuando **al menos uno** lo es; `not` invierte el valor. Pueden recibir cualquier valor, no solo booleanos: Python evalúa su **verdad** (falsy/Truthy) — `0`, `""`, `None`, `[]` son falsos; el resto es verdadero (ver [tipos de datos](tipos_datos.md)). Comportamiento clave: **evaluación corta** (*short-circuit*): en `a and b`, si `a` es falso, `b` no se evalúa; en `a or b`, si `a` es verdadero, `b` no se evalúa. Eso permite proteger operaciones costosas o peligrosas sin `if`.

**Operadores de pertenencia.** `valor in colección` devuelve `True` si el valor está contenido; `not in` invierte la pregunta. Sobre cadenas significa "contiene la subcadena"; sobre listas, conjuntos y diccionarios, "contiene el elemento o la clave". Es la forma idiomática de validar entradas (como hace el material original con listas de opciones).

**Operadores de identidad.** `a is b` pregunta si `a` y `b` apuntan al **mismo objeto**, no si tienen el mismo valor. Para comparar valores se usa `==`; `is` se reserva para comprobaciones de identidad, la más habitual siendo `x is None`. Con cadenas la confusión es peligrosa: Python **puede** reutilizar (internar) objetos de texto inmutables, de modo que en CPython dos literales iguales a veces son el mismo objeto y a veces no; el lenguaje **no garantiza** ese comportamiento, así que jamás se usa `is` para comparar el contenido de dos cadenas. El material original comenta mal un caso de `is` (ver sección 8).

**Operador de intersección `&`.** Sobre conjuntos (`set`), `a & b` devuelve los elementos comunes. El material lo usa para detectar símbolos en una contraseña. Sobre enteros, `&` es el operador bit a bit ("y" binario), tema que se toca solo de paso aquí. La cobertura completa de conjuntos está en [conjuntos](../../Intermedio/chapter-one/conjuntos.md).

**Precedencia (orden de evaluación).** Cuando se mezclan operadores en una expresión, Python respeta un orden fijo, de mayor a menor: `**` → signos unarios `-`/`+` → `*`, `/`, `//`, `%` → `+`, `-` → comparaciones → `not` → `and` → `or`. Por eso `2 + 3 * 4` vale `14` y no `20`, y por eso los paréntesis son la herramienta para que el orden sea evidente. Esta tabla es **fundamento complementario**: el material original la aplica sin explicarla.

## 4. Sintaxis y funcionamiento

Sintaxis general de una expresión con operador:

```text
operando1 operador operando2
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `+ - * /` | Suma, resta, multiplicación y división (devuelve `float`) | `12 / 5` → `2.4` |
| 2 | `//` | División entera: parte entera hacia abajo | `17 // 5` → `3` |
| 3 | `%` | Resto de la división; el signo sigue al divisor | `17 % 5` → `2` |
| 4 | `**` | Potencia; la raíz es la potencia fraccionaria | `12 ** 5` → `248832` |
| 5 | `== != > < >= <=` | Comparaciones; devuelven siempre booleano | `5 < 10` → `True` |
| 6 | `and or not` | Lógica booleana con evaluación corta | `True and False` → `False` |
| 7 | `in`, `not in` | Pertenencia; devuelven booleano | `"hola" in "hola mundo"` → `True` |
| 8 | `is`, `is not` | Identidad de objeto (no de contenido) | `x is None` |

Orden de precedencia, de mayor a menor:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `**` | Potencia (mayor precedencia; asociatividad de derecha a izquierda) | `2 ** 3 * 2` → `16` |
| 2 | `+x`, `-x` | Signos unarios positivo y negativo (se evalúan después de `**`) | `-2 ** 2` → `-4` |
| 3 | `* / // %` | Multiplicativos (mismo nivel; evaluación de izquierda a derecha) | `2 + 3 * 4` → `14` |
| 4 | `+ -` | Aditivos (suma y resta binarias) | `2 * 3 + 1` → `7` |
| 5 | `== != > < >= <=`, `is`, `in` | Comparaciones, identidad y pertenencia | `1 + 1 == 2` → `True` |
| 6 | `not` | Negación lógica booleana | `not 1 == 2` → `True` |
| 7 | `and` | Conjunción lógica con evaluación corta | `True or False and False` → `True` |
| 8 | `or` | Disyunción lógica (menor precedencia de las expresiones booleanas) | `False or True` → `True` |

Funcionamiento: Python evalúa la expresión de adentro hacia afuera, respeta la precedencia, aplica la evaluación corta en `and`/`or` y produce un valor que puede guardarse en una variable o pasarse a `print`. Los operadores nunca alteran los operandos originales: crean un valor nuevo.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Las ocho operaciones aritméticas.**

```python
suma = 12 + 5
resta = 12 - 5
producto = 12 * 5
division = 12 / 5
division_baja = 12 // 5
modulo = 12 % 5
potencia = 12 ** 5
raiz = round(12 ** (1 / 2), 4)
print(suma, resta, producto)
print(division, division_baja, modulo)
print(potencia, raiz)
```

Explicación línea por línea:

- Líneas 1-3: operaciones básicas; todos los resultados son enteros porque los operandos lo son.
- Línea 4: la división `/` devuelve decimal: `12 / 5` → `2.4`.
- Línea 5: `//` descarta la parte decimal: `12 // 5` → `2`.
- Línea 6: `%` devuelve el resto: `5 * 2 = 10`, a `12` le sobran `2`.
- Línea 7: potencia: `12` multiplicado por sí mismo cinco veces → `248832`.
- Línea 8: raíz cuadrada escrita como potencia `12 ** 0.5`; `round(..., 4)` limita el decimal mostrado a cuatro cifras.
- Líneas 9-11: `print` con varios valores los separa con un espacio (sección 4 de [entradas y salidas](entradas_y_salidas.md)).

Resultado esperado:

```text
17 7 60
2.4 2 2
248832 3.4641
```

**Ejemplo 2 — Los seis operadores de comparación.**

```python
a = 5
b = 10
print(a == b, a != b, a > b)
print(a < b, a >= b, a <= b)
```

Explicación línea por línea:

- Líneas 1-2: dos operandos fijos para que los resultados sean reproducibles.
- Línea 3: `5 == 10` es `False`; `5 != 10` es `True`; `5 > 10` es `False`.
- Línea 4: `5 < 10` es `True`; `5 >= 10` es `False`; `5 <= 10` es `True`.
- Todas las comparaciones producen booleanos y **no** modifican `a` ni `b`.

Resultado esperado:

```text
False True False
True False True
```

**Ejemplo 3 — Operadores lógicos sobre booleanos.**

```python
print(True and True, True and False)
print(True or False, False or False)
print(not True, not False)
```

Explicación línea por línea:

- Línea 1: `and` exige ambos verdaderos: `True and True` → `True`; `True and False` → `False`.
- Línea 2: `or` basta con uno verdadero: `True or False` → `True`; `False or False` → `False`.
- Línea 3: `not` invierte: `not True` → `False`; `not False` → `True`.
- Estas son las tablas de verdad completas de `and` y `or`, las mismas que documenta el material original.

Resultado esperado:

```text
True False
True False
False True
```

### Intermedio

**Ejemplo 4 — Reporte aritmético con decisiones derivadas de comparaciones.**

```python
v1 = 17
v2 = 5
print("suma:", v1 + v2, "resta:", v1 - v2)
print("division:", v1 / v2, "entera:", v1 // v2, "resto:", v1 % v2)
mayor = v1 > v2
divisible = v1 % v2 == 0
print("v1 es mayor que v2:", mayor)
print("v1 es divisible entre v2:", divisible)
print("ambas afirmaciones:", mayor and divisible)
```

Explicación de las decisiones tomadas:

- Primero se calculan las operaciones y luego se guardan dos **conclusiones** en variables con nombre semántico (`mayor`, `divisible`): el código se lee como un enunciado y depura más fácil.
- `v1 % v2 == 0` combina dos niveles: el `%` (precedencia alta) produce el resto y `==` lo compara con cero; los paréntesis implícitos los da la precedencia de la tabla de la sección 4.
- `mayor and divisible` muestra la composición: dos comparaciones alimentan un operador lógico, que devuelve un único booleano. Este patrón es exactamente lo que usará `if` en [condicionales](condicionales.md).
- No se usa ningún `if`: los booleanos se muestran directamente, porque la estructura condicional es el tema siguiente.

Resultado esperado:

```text
suma: 22 resta: 12
division: 3.4 entera: 3 resto: 2
v1 es mayor que v2: True
v1 es divisible entre v2: False
ambas afirmaciones: False
```

**Ejemplo 5 — Pertenencia en textos, listas y conjuntos.**

```python
texto = "hola mundo"
print("hola" in texto, "adios" in texto)
print("x" not in texto)
asignaturas = ["Software", "Informatica", "Matematicas"]
print("Software" in asignaturas, "Historia" in asignaturas)
print(bool(set("Flavio@!!") & {"!", "@", "#"}))
```

Explicación de las decisiones tomadas:

- Línea 1: sobre una cadena, `in` busca una **subcadena**; `"adios"` no aparece, por eso `False`.
- Línea 2: `not in` invierte la pregunta: como `x` no está, devuelve `True`.
- Línea 3: una lista de opciones válidas; `in` pregunta si el valor está entre los elementos. Es la validación idiomática que el material original aplica con listas de asignaturas.
- Línea 5: `set(...)` convierte la cadena en un conjunto de caracteres y `&` calcula la intersección con los símbolos permitidos; `bool(...)` traduce "hay intersección no vacía" a `True`. Es la misma detección de símbolos que el material original hace dentro de un `if`, expresada aquí solo con operadores.
- El orden de los elementos de un conjunto no está garantizado, por eso se comprueba la existencia con `bool` en lugar de imprimir el conjunto.

Resultado esperado:

```text
True False
True
True False
True
```

### Avanzado

**Ejemplo 6 — Precedencia, evaluación corta y el peligro de `is`.**

```python
print(2 + 3 * 4, (2 + 3) * 4)
print(-2 ** 2, (-2) ** 2)
print(0.1 + 0.2 == 0.3)
print("izquierda") and print("derecha")
print("izquierda") or print("derecha")
a = "hola"
b = "ho" + "la"
print(a == b)
print("HOLA" is not ("HOLA, mundo"))
```

Explicación de las decisiones tomadas:

- Línea 1: la precedencia de `*` sobre `+` da `14`; los paréntesis fuerzan `20`. En producción se agregan paréntesis redundantes cuando aclaran la intención.
- Línea 2: `**` tiene prioridad sobre el signo unario: `-2 ** 2` es `-(2 ** 2)` = `-4`; con paréntesis, `(-2) ** 2` = `4`. Es la trampa de precedencia más clásica.
- Línea 3: `0.1 + 0.2` no es exactamente `0.3` en punto flotante (ver [tipos de datos](tipos_datos.md)), por lo que comparar decimales con `==` devuelve `False`. Regla de producción: nunca comparar importes `float` con igualdad exacta.
- Líneas 4-5: demostración de la **evaluación corta**. En la línea 4, `print("izquierda")` devuelve `None` (falso), así que `and` no evalúa el lado derecho y `"derecha"` no aparece. En la línea 5, como el lado izquierdo es falso, `or` sí evalúa el derecho y `"derecha"` se imprime.
- Líneas 6-8: las líneas 6 y 7 crean dos cadenas con el mismo contenido por rutas distintas y la línea 8 las compara. `==` compara **contenido** (`True`, garantizado). `is` compara **identidad**: para textos con distinto contenido el resultado de `is not` es `True` de forma inevitable, pero para textos iguales depende de si la implementación reutiliza el objeto — CPython a veces los interna y otras no; el lenguaje no lo especifica. Por eso la única comparación correcta entre cadenas es `==` (y `x is None` para `None`).
- El comentario `#false` que el material original pone junto a `print("HOLA" is not bienvenida)` es incorrecto: `"HOLA"` y `bienvenida` tienen contenidos distintos, entonces `is not` devuelve `True` siempre. La comprobación ejecutable está al final de este ejemplo.

Resultado esperado del bloque principal (las nueve líneas del bloque; las asignaciones de las líneas 6-7 no imprimen nada):

```text
14 20
-4 4
False
izquierda
izquierda
derecha
True
True
```

La última línea genera además un aviso en la salida de error (stderr), no en la salida estándar: `SyntaxWarning: "is not" with 'str' literal. Did you mean "!="?` (verificado con Python 3.14). El propio intérprete avisa que comparar identidad entre cadenas es sospechoso; el resultado en stdout sigue siendo `True`.

Verificación ejecutable del comentario del material original:

```python
bienvenida = "HOLA " + "5" + " ESTA"
print("HOLA" is not bienvenida)
```

Resultado esperado:

```text
True
```

## 6. Aplicaciones en el mundo real

- **Cálculos financieros y de inventario:** sumas, restas, porcentajes (`*` con decimales) y módulos para repartir en partes iguales son la base de facturación y stock.
- **Validación de entradas:** `in` sobre listas de valores permitidos es el mecanismo de control de formularios y APIs; `not in` detecta valores prohibidos.
- **Control de calidad de datos:** `==`, `!=` y comparaciones encadenadas (`0 <= edad <= 120`) filtran registros inválidos en procesamiento por lotes.
- **Lógica de reglas de negocio:** combinaciones `and`/`or`/`not` expresan condiciones como "cliente activo y saldo positivo, o promoción vigente".
- **Algoritmos y entrevistas:** potencia, módulo (`%` para pares/impares, ciclos) y precedencia correcta aparecen en prácticamente todo ejercicio de programación.
- **Detección de símbolos y limpieza de texto:** intersecciones de conjuntos (`&`) comprueban de forma rápida si una cadena contiene caracteres de un grupo determinado, como hace el material original con contraseñas.

## 7. Uso en producción

- **Paréntesis sobre ambigüedad:** la precedencia de Python es fija y documentada, pero `a and b or c` sin paréntesis obliga a recordarla; en código compartido se prefiere la expresión explícita.
- **Nunca `==` entre `float` de dinero:** usar enteros de centavos o `decimal` (nivel intermedio) y reservar `==` para valores exactos. Los detalles están en [tipos de datos](tipos_datos.md).
- **`is` solo para `None` y comprobaciones de identidad deliberadas:** comparar cadenas o números con `is` puede funcionar en CPython por internado y fallar después de una refactorización; es un fallo silencioso difícil de rastrear.
- **Validar con `in` contra colecciones nombradas:** `if estado in ESTADOS_VALIDOS` (donde `ESTADOS_VALIDOS` es una constante) escala mejor que cadenas de `or` encadenados.
- **Evaluación corta como protección:** `dato is not None and dato.strip()` evita acceder a `None`; es una técnica de producción, no un truco obsoleto.
- **División y redondeo conscientes:** saber si se necesita `/`, `//` o `round` evita errores de redondeo acumulados en reportes; para dinero, la división exacta exige `decimal`.
- **No abusar de operadores personalizados:** sobrecargar operadores (por ejemplo, definir el comportamiento de `+` o `-` en clases propias mediante métodos especiales como `__add__` y `__sub__`, técnica utilizada en el bloque de POO del curso) solo conviene cuando la operación posee una semántica clara en el dominio; su implementación se desarrolla en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md).

## 8. Errores comunes y recomendaciones

1. **Dividir o calcular módulo entre cero.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: ZeroDivisionError, no se puede dividir entre 0
resultado = 10 / 0
print(resultado)
```

Salida real: `ZeroDivisionError: division by zero`. Diagnóstico: revisar el divisor, que en programas reales llega como dato del usuario; proteger el cálculo con una comprobación o con `try/except` (ver [excepciones](../../Intermedio/chapter-four/excepciones.md)).

2. **Operar con tipos incompatibles.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, no se puede restar int a str
resultado = "abc" - 1
print(resultado)
```

Salida real: `TypeError: unsupported operand type(s) for -: 'str' and 'int'`. Solución: convertir el operando (`int(...)`) o repensar la operación; el mensaje del error nombra los dos tipos en conflicto.

3. **Confundir asignación y comparación.** Asignar donde se espera comparar no siempre produce un error de sintaxis evidente; el clásico es `x = 5 == 5`, que **no** guarda `5` sino `True` (primero se evalúa `5 == 5`):

```python
x = 5 == 5
print(x)
```

Resultado esperado:

```text
True
```

Recomendación: en condiciones siempre `==` (el error dentro de `if` se detalla en [condicionales](condicionales.md)) y revisar los mensajes del linter, que señalan la asignación sospechosa.

4. **Subestimar la precedencia.** `-2 ** 2` es `-4`, no `4`; `True or False and False` es `True` porque `and` se evalúa antes que `or`. Ante la duda, usar paréntesis: es más barato leerlos que depurar un cálculo equivocado.

5. **Usar `is` para comparar valores.** El material original afirma en `CLASE_ONE.py` L110 que `"HOLA" is not bienvenida` da `False`; la comprobación de la sección 5 muestra que da `True`. Además, para cadenas con el mismo contenido el resultado de `is` varía según la implementación y la versión: CPython puede internar literales, pero el lenguaje no lo garantiza. Regla infalible: `==` para contenido, `is` para identidad (y `is None` para nulos).

6. **Creer que `//` siempre descarta decimales hacia abajo en positivos y negativos por igual.** En negativos redondea hacia **menos infinito**: `-7 // 2` es `-4`. Si se necesita truncar hacia cero, se aplica `int(x / y)`; documentar la elección evita descuadres en repartos.

7. **Mezclar textos numéricos con aritmética.** `input` devuelve `str`; `"10" * 2` repite el texto dos veces (`"1010"`) en lugar de multiplicar. Convertir antes de operar (ver [tipos de datos](tipos_datos.md)).

8. **Olvidar que `or`/`and` devuelven operandos, no siempre booleanos.** `"" or "defecto"` devuelve `"defecto"`; eso es útil como valor por defecto, pero sorprende a quien espera `True`/`False`. Para forzar booleano se usa `bool(...)`.

## 9. Resumen

- Un operador combina operandos en una expresión; Python distingue aritméticos, comparación, lógicos, pertenencia, identidad y asignación.
- `/` siempre devuelve decimal; `//` redondea hacia abajo; `%` devuelve el resto con el signo del divisor; `**` es potencia y la raíz es la potencia fraccionaria.
- Las seis comparaciones devuelven booleanos y funcionan también con texto (comparación lexicográfica); se pueden encadenar (`1 < 2 < 3`).
- `and`/`or`/`not` combinan condiciones y evalúan en corto: el lado derecho puede no ejecutarse.
- `in`/`not in` preguntan pertenencia sobre textos y colecciones; `&` intersecta conjuntos.
- `is` compara identidad, no contenido: nunca para cadenas ni números; `==` para valores.
- La precedencia (`**` → signos unarios → multiplicativos → aditivos → comparaciones → `not` → `and` → `or`) explica por qué `2 + 3 * 4` vale `14` y `-2 ** 2` vale `-4`; los paréntesis aclaran la intención.
- Los booleanos que producen estos operadores son la materia prima de [condicionales](condicionales.md).

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L110, L166-238, L305-356) | `CLASE_ONE.py` | Ocho operaciones aritméticas con ejemplos, seis comparaciones, `and`/`or`/`not` con tablas de verdad, intersección `&` de conjuntos | Se documentó la precedencia, la evaluación corta, el signo de `//` y `%` con negativos y se corrigió el comentario erróneo sobre `is` de la L110 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(01)_CLASSS_ONE.py` (L107-163) | `REPASO(01)_CLASSS_ONE.py` | Las siete primeras operaciones aritméticas y los seis operadores de comparación sobre dos valores leídos | Se reorganizaron por familias con tablas y se añadieron la división entera con negativos y la comparación lexicográfica de textos |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Operadores_Aritméticos.py` (L1-74) | `Ejm_Operadores_Aritméticos.py` | Las ocho operaciones completas (incluida raíz como potencia fraccionaria), normalización de comas con `replace(",", ".")` | Se mantuvo el catálogo de ocho operaciones; el uso de `Decimal` y `quantize` se trata en el nivel intermedio y aquí se sustituyó por ejemplos con tipos integrados |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Operadores_Comparación.py` (L6-40) | `Ejm_Operadores_Comparación.py` | Los seis operadores de comparación evaluados con pares `if`/`else` | Se conservaron los seis operadores; el uso dentro de `if` se traslada a [condicionales](condicionales.md), que es el tema siguiente |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L120-146) | `REPASO(02)_CLASS_ONE.py` | Consultas `in` / `not in` sobre un texto con prompts interactivos | Se sistematizó como operadores de pertenencia con ejemplos reproducibles y sin entradas interactivas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/EJERCICIO_2.py` (L1-10) | `EJERCICIO_2.py` | Suma, resta, producto y división sobre dos valores numéricos | Se integró como práctica elemental de operadores aritméticos binarios |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/EJERCICIO_5.py` (L1-4) | `EJERCICIO_5.py` | Fórmula de Gauss `v1 * (v1 + 1) / 2` para sumar los primeros `n` enteros | Ilustra el uso de paréntesis y la precedencia entre multiplicación y división `/` (que produce `float`) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Metodos_Especiales.py` (L78-113) | `Metodos_Especiales.py` | Sobrecarga del operador `+` mediante el método especial `__add__` para combinar objetos `Persona` | Se anticipó en la sección 7 la conexión entre operadores y modelo de datos, enlazando su estudio completo en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/One.py` (L48-67) | `One.py` | Fusión de instancias con `+` (`__add__`) y cálculo de atributos con `/` y `**` | Refuerza la precedencia con paréntesis explícitos y el adelanto de sobrecarga de operadores |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L75-170, L495, L589) | `Juego.py` | Sobrecarga de `+` (`__add__`) y `-` (`__sub__`) junto con operadores aritméticos y de pertenencia `in` | Se registró como caso práctico integrador de operadores estándar y sobrecargados ([métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md)) |

**Fundamento complementario:** la tabla completa de precedencia de operadores y la semántica de evaluación corta de `and`/`or` no se explican explícitamente en el material original (aunque el código las aplica); se incorporan aquí como base para leer expresiones con seguridad, con referencia oficial en la sección 11.

## 11. Referencias oficiales

- <https://docs.python.org/3/reference/expressions.html#operator-precedence> — referencia oficial del lenguaje sobre expresiones, semántica de operadores y tabla completa de precedencia.
- <https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not> — documentación oficial de operaciones booleanas, comparaciones y pertenencia en tipos integrados.
- <https://docs.python.org/3/tutorial/introduction.html> — tutorial oficial de introducción: primeras expresiones aritméticas y de comparación.
- <https://docs.python.org/3/tutorial/> — tutorial oficial de Python, contexto general.
