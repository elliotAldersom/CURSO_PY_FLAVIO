# Estructuras condicionales en Python

## 2. Introducción

Los programas no solo calculan: también **deciden**. "Si el usuario tiene 18 años o más, mostrar mensaje A; si no, mensaje B". Esa bifurcación es una **estructura condicional**: un bloque de código que solo se ejecuta cuando se cumple una condición.

Una **condición** es una expresión que resulta en `True` (verdadero) o `False` (falso); los [operadores de comparación](operadores.md) (`>=`, `==`, `!=`...) son los que las producen. El statement (instrucción) `if` (en español, "si") evalúa la condición y ejecuta su bloque solo si es verdadera. `elif` ("else if", de ahí la abreviatura) agrega ramas alternativas, y `else` ("si no") captura el caso restante.

Por qué existen: sin condicionales, cada programa tendría un solo camino fijo de ejecución, útil solo para cálculos conociendo de antemano todos los datos. Con condicionales el código responde al dato real: valida entradas, aplica reglas de negocio, clasifica resultados. Su importancia es estructural: junto con [variables](variables.md), [tipos de datos](tipos_datos.md) y [operadores](operadores.md), forman el conjunto mínimo con el cual se puede escribir un programa que resuelva un problema con decisiones.

## 3. Fundamentos y conceptos

**La condición debe ser booleana.** `if` evalúa la expresión que le sigue y consulta su verdad: un booleano (`True`/`False`), o cualquier otro valor, que Python clasifica como verdadero o falso (`0`, `""`, `None`, `[]` son falsos; el resto es verdadero — ver [tipos de datos](tipos_datos.md)). Por eso `if edad:` significa "si `edad` tiene contenido verdadero" y `if edad >= 18:` significa "si la comparación dio `True`".

**Anatomía del `if`.** La instrucción se escribe: la palabra `if`, la condición, dos puntos `:` y, en el **renglón siguiente**, las instrucciones del bloque **indentadas** (con sangría). La indentación no es decorado: es la sintaxis que define qué líneas pertenecen al `if`. En Python, la sangría se mide con espacios (cuatro por convención PEP 8) y nunca se mezclan con tabuladores. Este uso de la indentación como sintaxis es **fundamento complementario**: el material original lo practica sin explicarlo.

**`elif` y `else` opcionales.** `elif` repite la estructura con otra condición y puede aparecer varias veces; `else` aparece como máximo una vez y siempre al final. Un `if` puede existir solo, con `else`, con `elif` o con ambos. La gramática de Python no permite `elif` después de `else` (el material lo señala correctamente: un `elif` va después de un `if`).

**El orden importa.** Python evalúa las condiciones **de arriba hacia abajo** y ejecuta **solo la primera** cuya condición sea verdadera; el resto no se evalúa. Por eso las ramas se ordenan de más específica a más general: si se pone primero `if nivel >= 500` antes de `if nivel >= 1000`, cualquier valor de 1000 o más caerá en el tramo de 500. El material original subraya esta idea al explicar su cadena de ingresos.

**Anidamiento.** Un `if` puede vivir dentro del bloque de otro `if`. El bloque interno solo se evalúa si el externo ya fue verdadero; su `else` pertenece al `if` interno y solo cubre esa rama. La sangría es la única indicación de a qué `if` pertenece cada `else`.

**Condiciones compuestas.** Los operadores lógicos `and`, `or` y `not` (ver [operadores](operadores.md)) combinan varias preguntas en una: `if edad >= 18 and tiene_permiso:`. El operador de pertenencia `in` también es habitual en condiciones: `if asignatura in opciones_validas:` comprueba si un valor está en una lista — patrón usado por el material original.

**Cuidado con los tipos en la condición.** Como `input` devuelve texto, `if input("Edad: ") == 18:` compara texto con número y será `False` **siempre**, sin ningún aviso: el programa corre y toma la rama equivocada. Convertir (`int(input(...))`) antes de comparar es obligatorio (ver [tipos de datos](tipos_datos.md)).

**Expresión condicional (operador ternario).** Mientras que la sentencia `if`/`else` selecciona qué bloque de instrucciones ejecutar y no produce un valor por sí misma, Python dispone de una **expresión condicional** para elegir entre dos valores en una sola línea: `<valor_si_verdadero> if <condición> else <valor_si_falso>`. Primero se evalúa `<condición>`; si resulta verdadera se evalúa y devuelve únicamente `<valor_si_verdadero>`, y si resulta falsa se evalúa y devuelve únicamente `<valor_si_falso>` (evaluación perezosa de las ramas). La cláusula `else` es obligatoria porque toda expresión debe producir siempre un valor. Es apropiada para asignaciones breves o argumentos en línea (por ejemplo, `"mayor" if intento > secreto else "menor"` o `round(a / b, 2) if b != 0 else "No se puede dividir entre cero"`), pero debe evitarse cuando requiere anidar condiciones o ejecutar múltiples acciones.

**`match`/`case` (Python ≥ 3.10).** Para comparar un mismo valor contra muchos constantes, Python 3.10 introdujo el statement `match`: evalúa la expresión y ejecuta el primer `case` cuyo **patrón** coincida. Los patrones de valor (`case 1:`), los patrones alternativos con `|` (`case 1 | 3:`) y el comodín `case _:` (que coincide con todo) cubren la mayoría de los casos. Requisito de versión explícito: **`match` requiere Python 3.10 o superior**; en versiones anteriores es error de sintaxis. Si ningún `case` coincide y no hay `case _`, no se ejecuta ninguna rama: el bloque termina sin hacer nada, por lo que siempre se incluye un `case _` por defecto (comportamiento observado en CPython 3.12 y 3.14 y descrito en el tutorial oficial).

**Año bisiesto: la regla correcta.** El material original intenta validar fechas pero omite la regla del siglo. La regla completa del calendario gregoriano es: es bisiesto si el año es múltiplo de **400**, o si es múltiplo de 4 y **no** de 100. Por eso 2000 y 2024 son bisiestos, y 1900 y 2100 no. Este documento presenta la regla correcta en la sección de ejemplos avanzados en lugar de replicar el material incompleto.

## 4. Sintaxis y funcionamiento

Sintaxis general de la estructura condicional:

```text
if <condición>:
    <bloque si es verdadero>
elif <otra condición>:
    <bloque alternativo>
else:
    <bloque si ninguna condición fue verdadera>
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `if` | Inicio de la primera rama; exige condición y dos puntos | `if edad >= 18:` |
| 2 | Condición | Expresión evaluada a verdad (booleano u otro valor) | `nivel == "alto"` |
| 3 | `:` | Cierra el encabezado; el bloque va indentado debajo | cuatro espacios de sangría |
| 4 | `elif` | Rama adicional; cero o varias, siempre después de `if` | `elif nivel == "medio":` |
| 5 | `else` | Rama por defecto; cero o una, siempre al final | `else:` |
| 6 | Bloque indentado | Conjunto de instrucciones que pertenece a su rama | `print("mayor de edad")` |

Sintaxis de la expresión condicional (operador ternario):

```text
<valor_si_verdadero> if <condición> else <valor_si_falso>
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `<valor_si_verdadero>` | Expresión evaluada y devuelta solo cuando la condición es verdadera | `"Mayor de edad"` |
| 2 | `if <condición>` | Condición booleana evaluada en primer lugar | `if edad >= 18` |
| 3 | `else <valor_si_falso>` | Rama obligatoria evaluada y devuelta cuando la condición es falsa | `else "Menor de edad"` |

Sintaxis de `match` (Python ≥ 3.10):

```text
match <expresión>:
    case <patrón>:
        <acción>
    case <patrón> | <patrón>:
        <acción alternativa>
    case _:
        <acción por defecto>
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `match` | Evalúa la expresión una vez y la compara contra los patrones | `match grado:` |
| 2 | `case` + valor | Patrón literal: coincide si el valor es igual | `case 2:` |
| 3 | Alternativas `|` | Varios valores en un mismo `case` | `case 1 \| 3:` |
| 4 | Comodín `_` | Coincide con cualquier valor; irá al final | `case _:` |

Funcionamiento: (1) Python evalúa la condición del `if`; (2) si es verdadera, ejecuta **solo** ese bloque y salta al final de la estructura; (3) si es falsa, prueba el siguiente `elif` con el mismo criterio; (4) si ninguno coincide, ejecuta el `else` si existe; (5) cualquier instrucción indentada al mismo nivel que el `if` se ejecuta siempre, con independencia del resultado. En `match`, el paso análogo compara patrones en orden hasta el primero que coincide.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Primera decisión: mayor o menor de edad.**

```python
edad = int(input("Ingresa tu edad: "))
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")
print("Esto se ejecuta siempre.")
```

Explicación línea por línea:

- Línea 1: se lee la respuesta como texto y se convierte a entero; sin esa conversión, la comparación siguiente fallaría en silencio (sección 3).
- Línea 2: `if` evalúa `edad >= 18`, que produce `True` o `False`; los dos puntos abren el bloque.
- Línea 3: solo se ejecuta cuando la condición fue verdadera; su sangría (cuatro espacios) la adscribe al `if`.
- Línea 4: `else` abre la rama complementaria; no lleva condición porque cubre todo lo que el `if` no cubrió.
- Línea 5: se ejecuta solo cuando la condición fue falsa.
- Línea 6: al nivel cero (misma sangría que el `if`), forma parte de ninguna rama: **siempre** se ejecuta. Es la misma observación que hace el material original.

Con `20`, resultado esperado:

```text
Ingresa tu edad: Eres mayor de edad
Esto se ejecuta siempre.
```

Con `15`, resultado esperado:

```text
Ingresa tu edad: Eres menor de edad
Esto se ejecuta siempre.
```

**Ejemplo 2 — Tres ramas con `elif`.**

```python
v1 = float(input("Ingresa el primer valor: "))
v2 = float(input("Ingresa el segundo valor: "))
if v1 > v2:
    print("V1 es mayor que V2")
elif v2 > v1:
    print("V2 es mayor que V1")
else:
    print("V1 y V2 son iguales")
```

Explicación línea por línea:

- Líneas 1-2: los dos valores se leen como decimales para que la comparación tenga sentido numérico.
- Línea 3: primera rama; si `v1` es mayor, se ejecuta y **el resto de la estructura se salta**.
- Línea 4: `elif` solo se evalúa si el `if` anterior falló; aquí se pregunta lo contrario.
- Línea 6: `else` cubre el único caso restante (son iguales): con dos ramas mutuamente excluyentes ya agotadas, no hace falta ninguna condición más.
- La estructura cubre los tres casos posibles sin solapamientos: exactamente una rama se ejecuta siempre.

Con `5` y `3`, resultado esperado:

```text
Ingresa el primer valor: Ingresa el segundo valor: V1 es mayor que V2
```

### Intermedio

**Ejemplo 3 — Condicionales anidados: balance mensual.**

```python
ingreso_mensual = 14000
gastos_mensual = 4000

if ingreso_mensual >= 10000:
    if ingreso_mensual - gastos_mensual < 0:
        print("Estas en deficit.")
    elif ingreso_mensual - gastos_mensual > 3000:
        print("Tu balance es solido.")
    else:
        print("Regula tus gastos.")
elif ingreso_mensual >= 1000:
    print("Ingreso moderado.")
elif ingreso_mensual >= 500:
    print("Ingreso bajo.")
else:
    print("Sin ingreso registrado.")
```

Explicación de las decisiones tomadas:

- Primero se comprueba el tramo de ingreso; el bloque interno solo se considera cuando el ingreso es de 10000 o más. Ese anidamiento codifica la regla "para evaluar el balance, primero hay que estar en el tramo alto".
- Dentro, las tres ramas del balance se ordenan de más restrictiva a menos: déficit (`< 0`), holgura (`> 3000`) y el resto. El `else` interno cierra ese subproblema y **no** tiene relación con el `else` final: la sangría lo deja claro.
- Los `elif` externos se encadenan después del `if` principal (nunca después de un `else`, que ya cerraría la cadena) y prueban los tramos en orden descendente.
- Con los valores fijos, `14000 - 4000 = 10000 > 3000`, así que se ejecuta "Tu balance es solido.".
- Las comparaciones y el orden de las ramas replican el ejemplo de ingresos del material original; los mensajes se redactaron en registro neutro y los valores son fijos para que la salida sea reproducible.

Resultado esperado:

```text
Tu balance es solido.
```

Si `gastos_mensual` fuera `13500`, la misma estructura imprimiría `Regula tus gastos.` (balance de 500: ni negativo ni mayor que 3000).

**Ejemplo 4 — Despacho de operaciones con `elif` (mini calculadora).**

```python
operador = input("Ingresa el operador: ")
a = float(input("Ingresa el primer valor: "))
b = float(input("Ingresa el segundo valor: "))

if operador.strip() == "+":
    print("La suma es:", a + b)
elif operador.strip() == "-":
    print("La resta es:", a - b)
elif operador.strip() == "*":
    print("El producto es:", a * b)
else:
    print("Operador no aceptado.")
```

Explicación de las decisiones tomadas:

- El usuario escribe un símbolo como **texto**; cada `elif` compara ese texto con un operador permitido. El patrón "cadena de `elif` sobre el mismo valor" es un despacho (*dispatch*): elegir una acción según un valor de categoría.
- `.strip()` elimina espacios accidentales antes de comparar: `" + "` no es igual a `"+"`, y sin el método el operador correcto se rechazaría en silencio. Es el mismo cuidado que usa el `calculadora_simple.py` original.
- El `else` actúa como red de seguridad: cualquier operador desconocido cae ahí en lugar de ejecutar nada.
- Los valores se convierten a `float` una sola vez, antes de la cadena de condiciones; el original del curso hace lo mismo con `Decimal`, cuyo uso exacto se estudia en el nivel intermedio.
- El resultado de cada rama se calcula **dentro** de esa rama: no se ejecutan operaciones inútiles de los demás caminos.

Con entradas `+`, `12.5` y `7.5`, resultado esperado:

```text
Ingresa el operador: Ingresa el primer valor: Ingresa el segundo valor: La suma es: 20.0
```

Con operador `x` (y cualquier otro valor no listado), resultado esperado:

```text
Ingresa el operador: Ingresa el primer valor: Ingresa el segundo valor: Operador no aceptado.
```

Los tres mensajes de la entrada aparecen en la misma línea porque `input()` no agrega salto de línea; el mensaje de la rama `else` llega después de haber leído los dos valores.

### Avanzado

**Ejemplo 5 — Validación de año bisiesto con la regla completa.**

```python
anio = int(input("Ingresa el año: "))
if anio % 400 == 0:
    print(f"{anio} es bisiesto (multiplo de 400).")
elif anio % 100 == 0:
    print(f"{anio} no es bisiesto (siglo no bisiesto).")
elif anio % 4 == 0:
    print(f"{anio} es bisiesto.")
else:
    print(f"{anio} no es bisiesto.")
```

Explicación de las decisiones tomadas:

- La secuencia de condiciones **es** la regla del calendario gregoriano, escrita en orden: primero los múltiplos de 400 (2000, 2400: bisiestos por esa razón), luego descartar los siglos no bisiestos (1900, 2100: múltiplos de 100 que no son de 400), luego aceptar los múltiplos de 4 corrientes (2024) y por último el resto (2023).
- El orden es obligatorio: si el caso `anio % 100 == 0` se evaluara antes del de 400, el año 2000 se clasificaría como "siglo no bisiesto" por ser múltiplo de 100. La primera rama verdadera gana (sección 3).
- El operador `%` (resto de la división, ver [operadores](operadores.md)) es la herramienta clásica de "¿es múltiplo de n?": un número es múltiplo de `n` cuando `n` lo divide sin resto.
- Este ejercicio sustituye la validación incompleta del material original (`anyo_bi.py` termina sin salir, y `REPASO(01)` y `ejercicio3.py` omiten la regla del siglo); aquí se documenta el comportamiento correcto.
- Cada año da un solo mensaje porque las ramas son mutuamente excluyentes por construcción.

Verificado con cinco entradas (la ejecución muestra antes `Ingresa el año: ` en la misma línea, ya que `input()` no imprime salto de línea; la tabla indica solo el mensaje que sigue):

| Entrada | Resultado esperado |
|---|---|
| `2000` | `2000 es bisiesto (multiplo de 400).` |
| `1900` | `1900 no es bisiesto (siglo no bisiesto).` |
| `2024` | `2024 es bisiesto.` |
| `2100` | `2100 no es bisiesto (siglo no bisiesto).` |
| `2023` | `2023 no es bisiesto.` |

**Ejemplo 6 — `match`/`case` con patrones alternativos (Python ≥ 3.10).**

```python
grado = 1
match grado:
    case 0:
        print("El grado no puede ser 0")
    case 1 | 3:
        print(f"Estas en {grado}ro")
    case 2:
        print(f"Estas en {grado}do")
    case 4 | 5 | 6:
        print(f"Estas en {grado}to")
    case _:
        print("Grado fuera del rango esperado")
```

Explicación de las decisiones tomadas:

- `match grado:` evalúa una vez el valor sujeto y lo compara con los patrones **en orden**, ejecutando solo el primero que coincide: equivalente a una cadena de `if`/`elif` sobre igualdades, pero más declarativo cuando hay muchos valores fijos.
- `case 1 | 3:` es un patrón alternativo (o-pattern): coincide con `1` **o** con `3`. Nota: dentro de `case` el símbolo `|` no es el operador de unión de conjuntos; es parte de la sintaxis de patrones.
- Los sufijos (`ro`, `do`, `to`) se generan con f-strings (ver [entradas y salidas](entradas_y_salidas.md)).
- `case _:` es el comodín: siempre coincide y actúa como rama por defecto. Sin él, un valor que no esté en ningún `case` (por ejemplo `9`) **no ejecuta ninguna rama** y el programa continúa en silencio: una fuente clásica de errores difíciles de ver.
- Requisito de versión: este código necesita **Python 3.10 o superior**; en versiones anteriores `match` ni siquiera se reconoce. El material original del curso usa esta misma construcción en `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py`.
- Mantenibilidad: si los tramos crecen, `match` escala mejor que `elif` encadenados; para solo dos o tres ramas, `if`/`elif` sigue siendo más directo.

Resultado esperado (con `grado = 1`):

```text
Estas en 1ro
```

**Ejemplo 7 — Expresión condicional (operador ternario) y evaluación perezosa.**

```python
intento = 14
secreto = 10
pista = "mayor" if intento > secreto else "menor"
print("El número ingresado es", pista, "que el secreto.")

numerador = 10
divisor = 0
resultado = round(numerador / divisor, 2) if divisor != 0 else "No se puede dividir entre cero"
print("Resultado:", resultado)
```

Explicación de las decisiones tomadas:

- La expresión `"mayor" if intento > secreto else "menor"` produce directamente una cadena que puede asignarse a `pista` o pasarse como argumento a `print`, evitando cuatro líneas de bloque `if`/`else` cuando solo cambia un valor puntual.
- En la segunda parte, `divisor` vale `0`: gracias a la **evaluación perezosa**, Python comprueba primero `divisor != 0` (`False`) y salta directamente al texto después de `else` sin evaluar `numerador / divisor`, evitando un `ZeroDivisionError`.
- Criterio de mantenibilidad: la expresión condicional solo se emplea para seleccionar entre dos expresiones simples; si las ramas requieren múltiples instrucciones o un tercer caso, se utiliza un bloque `if`/`elif`/`else` convencional en lugar de anidar operadores ternarios.

Resultado esperado:

```text
El número ingresado es mayor que el secreto.
Resultado: No se puede dividir entre cero
```

## 6. Aplicaciones en el mundo real

- **Control de acceso:** comprobar rol y permisos ("si es admin o dueño del recurso...") es la primera línea de cualquier sistema multiusuario.
- **Validación de datos:** formatos de correo, rangos de edad, años válidos y campos obligatorios se resuelven con cadenas de condiciones, como el Ejemplo 5.
- **Reglas de negocio:** tramos impositivos, descuentos por volumen, envío gratis a partir de un monto: todas son estructuras condicionales sobre importes.
- **Despacho de operaciones:** el enrutamiento de una calculadora, de un comando de terminal o de una API según el tipo de solicitud usa el patrón `elif`/`match` del Ejemplo 4.
- **Procesamiento de archivos y datos:** clasificar registros (válidos/inválidos, con/sin datos) antes de analizarlos condiciona todo el flujo posterior.
- **Interfaces de escritorio:** habilitar o deshabilitar botones según el estado del formulario depende de condiciones evaluadas continuamente.

## 7. Uso en producción

- **Validar antes de condicionar:** la condición debe trabajar sobre datos ya convertidos y saneados; una comparación entre texto y número no falla, sino que decide mal (sección 3).
- **Preferir guardas tempranas a anidamiento profundo:** en cuanto los `if` se anidan tres o cuatro niveles, la lectura se degrada; el patrón de producción es resolver los casos inválidos primero y dejar el camino principal al nivel cero. Con funciones (nivel intermedio, ver [funciones](../../Intermedio/chapter-two/funciones.md)) ese patrón se vuelve natural con salidas tempranas.
- **Nunca credenciales en claro:** el material original compara contraseñas escritas literalmente en el código (`CLASE_ONE.py` L239-242 y `contraseña_registro.py`). En producción eso es una brecha de seguridad: la verificación se hace contra valores protegidos (hash con sal) y las contraseñas jamás aparecen en el repositorio.
- **Orden por corrección primero, rendimiento después:** la primera rama debe ser la correcta; si además es la más frecuente, se gana un poco de rendimiento al no evaluar el resto. Nunca se reordenan ramas sacrificando la semántica.
- **Sentencia `if`, expresión ternaria o `match`:** usar la expresión condicional (`a if cond else b`) solo para seleccionar un valor breve en una línea sin anidamiento; `match` (≥ 3.10) para despachar numerosos patrones fijos de forma declarativa; e `if`/`elif`/`else` para condiciones generales o bloques con varias instrucciones.
- **Probar todas las ramas:** una estructura condicional solo está completa cuando cada rama tiene una prueba que la ejercita; los casos límite (el `18` exacto, el `0`, el año 2000) son los que suelen fallar.
- **Bloque principal del script:** el patrón `if __name__ == "__main__":` presentado en [entradas y salidas](entradas_y_salidas.md) es el primer uso productivo de un condicional a nivel de archivo; se retoma en el curso al estudiar módulos.

## 8. Errores comunes y recomendaciones

1. **Olvidar los dos puntos.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, falta los dos puntos al final del encabezado
verdadero = True
if verdadero
    print("El bloque se ejecuta")
```

Salida real: `SyntaxError: expected ':'`. Python exige `:` para abrir el bloque de cualquier estructura compuesta (`if`, `elif`, `else`, `match`, `case`, bucles).

2. **Usar `=` donde corresponde `==`.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, = asigna y == compara
edad = 18
if edad = 18:
    print("igual")
```

Salida real: `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`. El analizador detecta la asignación dentro de la condición; en lenguajes más laxos ese error pasaría silencioso, aquí Python lo corta al compilar.

3. **Indentar mal el bloque.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: IndentationError, el bloque de if debe ir sangrado
if True:
print("Sin indentar")
```

Salida real: `IndentationError: expected an indented block after 'if' statement on line 2`. Diagnóstico: la sangría define el bloque; usar siempre cuatro espacios y no mezclarlos con tabuladores. Un `else` mal sangrado también cambia a qué `if` pertenece: es el error de anidamiento más difícil de detectar a simple vista.

4. **Escribir la condición como si fuera una función.** El material original presenta `if condición():` como "estructura" en `CLASE_ONE.py` L263, pero `condición` es una cadena y llamarla con paréntesis lanza un error. Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, una cadena no es una función
condicion = "si"
accion = "ejecutar"
if condicion():
    print(accion)
```

Salida real: `TypeError: 'str' object is not callable`. Regla: la condición es una **expresión** (comparación, valor de verdad), no una llamada. Las llamadas `funcion()` serán válidas cuando se estudien las [funciones](../../Intermedio/chapter-two/funciones.md); aquí la pseudoestructura del material no se replica.

5. **Comparar texto de `input` con número (fallo silencioso).** Este programa no lanza ningún error, pero decide mal siempre:

```python
edad_leida = "18"
if edad_leida == 18:
    print("mayor de edad")
else:
    print("el dato no coincide")
```

Resultado esperado:

```text
el dato no coincide
```

Diagnóstico: `"18" == 18` es `False` porque son tipos distintos. Solución: convertir al leer (`edad = int(input(...))`) y comparar números con números.

6. **Ordenar mal las ramas (`elif` imposible).** Este programa nunca llega a su segunda rama:

```python
nivel = 1500
if nivel >= 500:
    print("tramo alto")
elif nivel >= 1000:
    print("tramo muy alto")
```

Resultado esperado:

```text
tramo alto
```

Diagnóstico: `1500 >= 500` es verdadero, así que la primera rama gana y el `elif` queda inalcanzable para cualquier valor de 1000 o más. Solución: ordenar de mayor a menor (`>= 1000` antes que `>= 500`) o usar rangos explícitos (`if 500 <= nivel < 1000:`).

7. **Replicar el control de fechas incompleto del material.** `REPASO(01)_CLASSS_ONE.py` L177 valida febrero con una lógica que ignora el año y omite la regla del siglo; `anyo_bi.py` queda sin terminar y `ejercicio3.py` lleva el aviso del propio autor ("PROGRAMA ... CON ERRORES"). La única versión correcta es la del Ejemplo 5: múltiplo de 400, o múltiplo de 4 y no de 100.

8. **Hardcodear la comprobación.** `ejercicio1_s3.py` L20 decide con `if(i==3):` sobre un contador: la regla ("3 intentos") queda incrustada en la condición y no se puede reutilizar. En producción, los límites son constantes nombradas (`if intentos == MAX_INTENTOS:`), como se ve en [variables](variables.md).

9. **Confiar en que `else` siempre estará donde parece.** El `else` se asocia por sangría al `if` inmediatamente anterior **al mismo nivel**; un bloque mal indentado puede hacer que un `else` cierre un `if` distinto del que el lector cree. Revisar la sangría en los puntos de unión es la primera rutina de depuración de estas estructuras.

## 9. Resumen

- Una estructura condicional ejecuta un bloque solo cuando su condición es verdadera; `if` abre la primera rama, `elif` agrega alternativas y `else` cubre lo restante.
- La condición puede ser cualquier valor de verdad; en la práctica son comparaciones (`>=`, `==`, `!=`) combinadas con `and`, `or`, `not` y `in`.
- La **sintaxis por indentación** define los bloques: dos puntos en el encabezado, cuatro espacios en el cuerpo.
- Las ramas se evalúan de arriba hacia abajo y solo se ejecuta la primera verdadera: el orden de las condiciones es parte de la corrección del algoritmo.
- Los `if` pueden anidarse; la sangría determina a qué `if` pertenece cada `else`.
- La **expresión condicional** (`valor_1 if condicion else valor_2`) evalúa perezosamente y devuelve un valor en línea; exige siempre `else` y se reserva para expresiones simples sin anidar.
- Convertir antes de comparar evita el fallo silencioso de comparar texto con número.
- El año bisiesto se valida con la regla completa: múltiplo de 400, o múltiplo de 4 y no de 100.
- `match`/`case` (Python ≥ 3.10) ofrece patrones alternativos (`case 1 | 3`) y comodín (`case _`); sin comodín, los valores no contemplados no ejecutan ninguna rama.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L246-301) | `CLASE_ONE.py` | `if`/`elif`/`else`, bloque indentado, condicionales anidados, orden de evaluación | Se explicó la anatomía y el flujo paso a paso, se documentó que la pseudoestructura `if condición():` de la L263 lanza `TypeError` (sección 8) y se conservó el ejemplo de ingresos como Ejemplo 3 con mensajes en registro neutro |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L305-356) | `CLASE_ONE.py` | `and`, `or`, `not` usados con condiciones; intersección `&` de conjuntos para validar | Se trasladó la teoría de los operadores a [operadores](operadores.md) y aquí solo se usa; la validación con `&` aparece como fundamento del Ejemplo 5 de ese documento |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Operadores_Comparación.py` (L6-40) | `Ejm_Operadores_Comparación.py` | Los seis operadores de comparación evaluados con pares `if`/`else` | Se citan como el primer uso práctico de `if`; la teoría de los operadores quedó en [operadores](operadores.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/calculadora_simple.py` (L11-30) | `calculadora_simple.py` | Cadena de `elif` despachando operadores, `strip()` en la comparación, `else` por defecto | Se adaptó como Ejemplo 4 con tipos integrados (`float`); el uso de `Decimal` y `quantize` corresponde al nivel intermedio |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/EJEMPLO_while_if_elif.py` | `EJEMPLO_while_if_elif.py` | Uso de `elif` dentro de un proceso interactivo | Se aprovecha solo la parte `elif`; el bucle `while` que lo envuelve pertenece a [bucles](../chapter-two/bucles.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/ejercicio2.py` (L26-30) | `ejercicio2.py` | `if`/`else` sobre un umbral (`> 120`) con mensaje distinto | Se cita como ejemplo de umbral único; la lógica de conteo con `split` y `len` se relaciona con [cadenas](../chapter-two/cadenas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLO_IN.py` (L7-12) | `EJEMPLO_IN.py` | `if` con operador de pertenencia `in` sobre lista de opciones, con `else` | Se incorporó a la sección 3 como patrón de validación idiomático |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/contraseña_registro.py` | `contraseña_registro.py` | `if` anidados validando longitud, símbolos y confirmación | Se usa como referencia de anidamiento; el almacenamiento en claro se señala como anti-patrón en la sección 7 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/anyo_bi.py` | `anyo_bi.py` | Intento de validación de año bisiesto con `if` y división entera (archivo incompleto, sin salida) | Se documentó la regla completa y correcta en el Ejemplo 5, en lugar de completar el archivo original |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(01)_CLASSS_ONE.py` (L171-182) | `REPASO(01)_CLASSS_ONE.py` | Validación parcial de febrero con `if`/`else` omitiendo el año y la regla secular | Se contrastó en la sección 8 con la regla gregoriana completa del Ejemplo 5 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/ejercicio3.py` (L11-17) | `ejercicio3.py` | Validación de fecha con `if`/`else` y nota explícita del autor sobre errores en la lógica | Se corrigió la condición eliminando la doble negación defectuosa e incorporando los múltiplos de 100 y 400 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/ejercicio1_s3.py` (L20) | `ejercicio1_s3.py` | Condición sobre valor fijo (`if(i==3)`) dentro de un contador | Se documentó en la sección 8 como hardcodeo frágil, con la corrección por constante nombrada |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/Funciones_Repaso.py` (L52) | `Funciones_Repaso.py` | Expresión condicional `round(a/b, 2) if b != 0 else "No se puede dividir entre cero"` | Se integró en el Ejemplo 7 para demostrar la evaluación perezosa frente a `ZeroDivisionError` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/RANDOM/numero_secreto.py` (L37) | `numero_secreto.py` | Expresión condicional `"mayor" if numero_ingresado > numero_random else "menor"` dentro de `print(...)` | Se documentó en las secciones 3, 4 y 5 (Ejemplo 7) como selección concisa de valores en línea |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L62, L69) | `Decoradores_Multiples.py` | Expresiones condicionales `"Mayor de edad" if edad >= 18 else "Menor de edad"` y `"Puede entrar" if ... else ...` en decoradores | Muestra que la expresión condicional produce valores asignables y retornables en funciones de orden superior |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py` (L58-99) | `One.py` | `match`/`case` con patrones alternativos `case 1 \| 3` y comodín `case _`, dentro de un bucle con manejo de errores | Se adaptó como Ejemplo 6 con la advertencia explícita de versión (Python ≥ 3.10) y la explicación del comportamiento sin comodín; el bucle y los `except` pertenecen a sus respectivos temas |

**Fundamento complementario:** el uso de la indentación (cuatro espacios) como sintaxis que define los bloques y la convención PEP 8 de no mezclar tabuladores no se enseñan explícitamente en el material original; se incorporan aquí como base para escribir y leer las estructuras condicionales.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/controlflow.html#if-statements> — tutorial oficial de sentencias condicionales: `if`, `elif` y `else`.
- <https://docs.python.org/3/reference/expressions.html#conditional-expressions> — referencia oficial del lenguaje sobre expresiones condicionales (`x if C else y`).
- <https://docs.python.org/3/tutorial/controlflow.html#match-statements> — tutorial oficial de `match`/`case` (requiere Python 3.10 o superior).
- <https://docs.python.org/3/tutorial/> — tutorial oficial de Python, contexto general de control de flujo.
