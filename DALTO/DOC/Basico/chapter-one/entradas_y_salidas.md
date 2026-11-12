# Entradas y salidas de datos en Python

## 2. Introducción

Un programa de computadora recibe datos, los procesa y devuelve un resultado. En Python, el punto de contacto más directo con quien lo usa es la **terminal**: la ventana de texto donde se ejecuta el script. Desde la terminal se **leen** respuestas del usuario y se **muestran** los resultados.

Dos **funciones integradas** del lenguaje (*built-in functions*, disponibles directamente en el espacio de nombres `builtins` sin necesidad de `import`, a diferencia de los módulos de la biblioteca estándar como `math` o `decimal`) cubren esa necesidad:

- `print(...)`: función integrada de **salida**; escribe valores en la terminal.
- `input(...)`: función integrada de **entrada**; detiene el programa, espera a que el usuario escriba una línea y devuelve ese texto al código.

Una **función** es un bloque de código con nombre que realiza una tarea concreta y al que se "llama" escribiendo su nombre seguido de paréntesis. Una **cadena de texto** (en inglés *string*) es una secuencia de caracteres, por ejemplo `"Ana"`. El texto que `input()` muestra para pedir el dato se llama **prompt**.

Este tema es el primer paso del curso porque casi todo programa útil necesita dos cosas: mostrar información (`print`) y recibir datos (`input`). Sin salidas no hay forma de comprobar qué hizo el programa; sin entradas solo se podrían ejecutar programas con valores fijos escritos por el programador.

## 3. Fundamentos y conceptos

**Salida con `print`.** La función `print` recibe uno o más valores y los muestra en la terminal. Entre cada valor inserta automáticamente un espacio (el **separador**, `sep`) y al final agrega un salto de línea (`end`). Ese comportamiento por defecto explica por qué dos llamadas consecutivas a `print` aparecen en dos renglones distintos.

**Entrada con `input`.** La función `input` muestra el prompt, espera a que el usuario escriba algo y pulse Enter, y devuelve **siempre una cadena de texto**, aunque el usuario haya escrito dígitos. Python no adivina la intención: `"30"` (texto) y `30` (número) son valores de tipos distintos. Esta decisión de diseño simplifica la función `input` (no necesita adivinar el tipo) y obliga a la conversión **explícita** cuando se necesita aritmética: `int(...)` convierte a entero y `float(...)` a decimal. La conversión de tipos se trata con detalle en [tipos de datos](tipos_datos.md).

**Mostrar números junto con texto.** Para unir texto y números hay tres caminos:

1. Convertir el número a texto con `str(...)` y concatenar con `+`.
2. Pasar varios valores separados por comas a `print`, que los une con un espacio.
3. Usar una **f-string**: una cadena que comienza con `f` y permite incrustar expresiones entre llaves, por ejemplo `f"Tienes {edad} años"`.

Las f-strings son la opción más legible y se usan en la documentación de todo el curso. Los métodos (operaciones que se aplican a un dato, con estructura `dato.metodo()`) y el manejo completo de cadenas se estudian en [cadenas](../chapter-two/cadenas.md); aquí solo se usa lo mínimo para mostrar resultados.

**Secuencias de escape.** Dentro de una cadena, la combinación `\n` representa un salto de línea y `\t` un tabulador. Permiten dar formato al texto mostrado sin escribir varias llamadas a `print`. Python también admite secuencias hexadecimales como `\x1b` (carácter *Escape*), que combinadas con códigos como `\x1b[1;33m` forman **secuencias ANSI**: Python solo emite esos caracteres en la salida estándar y es el emulador de terminal (no el lenguaje) quien los interpreta para colorear el texto.

**Diferencia entre función y método.** `print(...)` y `input(...)` son **funciones**: se escriben como `función(argumento)`. En cambio, un **método** pertenece a un dato y se escribe como `dato.metodo()`, por ejemplo `texto.upper()`. Esta distinción, presente en el material original del curso, se reutiliza en todos los temas siguientes.

**Errores que ocurren en la frontera entrada/salida.** Convertir texto no numérico con `int("abc")` lanza (lanza = interrumpe el programa con un mensaje) un `ValueError`. Unir texto y número con `+` lanza un `TypeError`. Ambos casos se analizan en la sección 8; el manejo ordenado de estos errores con `try/except` se estudia en [excepciones](../../Intermedio/chapter-four/excepciones.md).

## 4. Sintaxis y funcionamiento

Sintaxis general de `print`:

```text
print(valor1, valor2, ..., sep=" ", end="\n")
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `valor1, valor2, ...` | Uno o más valores a mostrar (texto, números, resultados) | `print("Total:", 150)` |
| 2 | `sep` | Texto que se coloca entre valores; por defecto es un espacio | `print("a", "b", sep="-")` muestra `a-b` |
| 3 | `end` | Texto que se coloca al final; por defecto es un salto de línea (`\n`) | `print("fin", end="")` no salta de renglón |
| 4 | Conversión implícita | `print` convierte cualquier valor a texto antes de mostrarlo | `print(150)` muestra `150`, no falla |

Sintaxis general de `input`:

```text
variable = input("Prompt: ")
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `"Prompt: "` | Mensaje que se muestra antes de esperar la respuesta | `input("Edad: ")` |
| 2 | `input(...)` | Espera una línea y devuelve **siempre** `str` | `input("Edad: ")` → `"30"`, no `30` |
| 3 | `variable = ...` | Guarda la respuesta en una variable para reutilizarla | `edad = int(input("Edad: "))` |

Sintaxis de las conversiones básicas:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `int(texto)` | Convierte texto numérico a entero | `int("30")` → `30` |
| 2 | `float(texto)` | Convierte texto a decimal | `float("30.5")` → `30.5` |
| 3 | `str(valor)` | Convierte cualquier valor a texto | `str(30)` → `"30"` |

Funcionamiento paso a paso de un programa con entrada: (1) se muestra el prompt; (2) el programa se pausa; (3) el usuario escribe una línea y pulsa Enter; (4) `input` devuelve esa línea como cadena; (5) el código la convierte si necesita aritmética; (6) procesa; (7) `print` muestra el resultado y el programa continúa o termina.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Primeras salidas.**

```python
print("Hola, mundo")
print("Mi primer programa en Python.")
```

Explicación línea por línea:

- Línea 1: se llama a `print` con una cadena; la función escribe el texto y agrega un salto de línea.
- Línea 2: se llama a `print` otra vez; como la llamada anterior terminó con salto de línea, este texto aparece en el renglón siguiente.

Resultado esperado:

```text
Hola, mundo
Mi primer programa en Python.
```

**Ejemplo 2 — Leer un nombre y saludar.**

```python
nombre = input("Ingresa tu nombre: ")
print("Hola, " + nombre + "!")
```

Explicación línea por línea:

- Línea 1: `input` muestra el prompt y devuelve lo escrito como cadena; `nombre` guarda ese texto. Si el usuario escribe `Ana`, la variable contiene `"Ana"`.
- Línea 2: se concatenan (une con `+`) tres cadenas: el saludo, el nombre y el signo; `print` muestra el resultado.

Con `Ana` como entrada, resultado esperado (el prompt no agrega salto de línea):

```text
Ingresa tu nombre: Hola, Ana!
```

**Ejemplo 3 — Edad convertida a número.**

```python
edad = int(input("Ingresa tu edad: "))
print(f"Tienes {edad} años y el próximo cumplirás {edad + 1}.")
```

Explicación línea por línea:

- Línea 1: `input` devuelve `"30"` (texto); `int` lo convierte a `30` (entero); la variable `edad` guarda el número.
- Línea 2: la f-string comienza con `f`; entre llaves se inserta el valor de `edad` y la expresión `edad + 1`, que solo es posible porque `edad` es un número.

Con `30` como entrada, resultado esperado:

```text
Ingresa tu edad: Tienes 30 años y el próximo cumplirás 31.
```

### Intermedio

**Ejemplo 4 — Formato de salida con f-string, separador y secuencias de escape.**

```python
nombre = "Ana"
promedio = 8.75
print("Reporte académico")
print(f"Alumno: {nombre}\nPromedio: {promedio:.1f}")
print("Estado", "aprobado", sep=" | ", end=".\n")
```

Explicación de las decisiones tomadas:

- Se usan dos variables fijas para que el ejemplo sea reproducible sin escribir entradas.
- La f-string `:.1f` formatea el número con un decimal: el valor se redondea para **mostrarlo**; el dato interno sigue siendo `8.75`. Formatear la salida no modifica el valor almacenado.
- `\n` dentro de la f-string genera un salto de línea, por lo que el promedio aparece en un renglón propio sin una tercera llamada a `print`.
- El tercer `print` muestra por qué existen `sep` y `end`: los dos valores se unen con `" | "` en lugar de un espacio, y el punto con `end=".\n"` cierra la línea y luego salta de renglón.

Resultado esperado:

```text
Reporte académico
Alumno: Ana
Promedio: 8.8
Estado | aprobado.
```

**Ejemplo 5 — Calcular cuotas a partir de datos leídos.**

```python
monto = float(input("Ingresa el monto del equipo: "))
letras = int(input("Ingresa el número de cuotas: "))
incremento = 0.19
interes = 0.05
monto_pagar = monto * (1 + incremento)
monto_mensual = monto_pagar / letras
pago = round(monto_mensual * (1 + interes))
print("El pago mensual es:", pago)
```

Explicación de las decisiones tomadas:

- El monto se lee con `float` porque puede tener decimales; el número de cuotas con `int` porque solo tiene sentido como cantidad completa.
- `incremento` y `interes` se guardan en variables con nombre descriptivo para que la fórmula se lea como una frase: `monto * (1 + incremento)`. La convención de nombres de constantes se formaliza en [variables](variables.md).
- Los paréntesis dejan explícito el orden de operaciones, que Python también deduce por precedencia (ver [operadores](operadores.md)).
- `round(...)` redondea el resultado a un entero porque el ejemplo pide un pago en unidades completas.

Con `1000` como monto y `4` como número de cuotas, resultado esperado:

```text
Ingresa el monto del equipo: Ingresa el número de cuotas: El pago mensual es: 312
```

### Avanzado

**Ejemplo 6 — Lectura robusta de datos con manejo de errores.**

```python
try:
    nombre = input("Ingresa tu nombre: ").strip().capitalize()
    total = float(input("Ingresa el total: "))
    impuesto = float(input("Ingresa el impuesto: "))
except ValueError:
    print("Debes ingresar valores numéricos válidos.")
except KeyboardInterrupt:
    print("\nOperación cancelada por el usuario.")
except EOFError:
    print("\nNo hay más datos disponibles.")
else:
    print(f"{nombre} debe pagar {total + impuesto:.2f}")
```

Explicación de las decisiones tomadas:

- `try:` agrupa las líneas que pueden fallar. Si algo falla, Python salta al bloque `except` correspondiente en lugar de detener el programa con un mensaje crudo.
- `.strip()` es un método de cadena que elimina espacios al inicio y al final; evita que `" Ana "` deje de coincidir con `"Ana"`. Se muestra con detalle en [cadenas](../chapter-two/cadenas.md).
- Las dos conversiones a `float` están **dentro** del `try`: si el usuario escribe letras, `float(...)` lanza `ValueError` justo ahí y se ejecuta el primer `except`.
- `except KeyboardInterrupt` atiende a quien pulsa Ctrl+C, y `except EOFError` a quien cierra la entrada estándar (fin de archivo). Son los dos casos que el material original contempla.
- El bloque `else` solo se ejecuta cuando **ninguna** excepción ocurrió: los cálculos solo tienen sentido con todos los datos válidos.
- Este ejemplo es la versión mínima de una idea que se estudia a fondo en [excepciones](../../Intermedio/chapter-four/excepciones.md).

Con entradas ` Ana `, `100` y `21`, resultado esperado:

```text
Ingresa tu nombre: Ingresa el total: Ingresa el impuesto: Ana debe pagar 121.00
```

Si en el segundo dato se escribe `cien`, resultado esperado (con código de salida `0`, porque el error fue capturado):

```text
Ingresa tu nombre: Ingresa el total: Debes ingresar valores numéricos válidos.
```

El primer mensaje de la entrada sigue presente porque `nombre` sí se leyó bien; la ejecución se detiene en `float("cien")` y salta al `except ValueError`.

## 6. Aplicaciones en el mundo real

- **Scripts de terminal (CLI):** herramientas que reciben parámetros escritos por quien las ejecuta y reportan resultados; es el caso de uso clásico de `input` y `print`.
- **Automatización administrativa:** programas que piden un monto, una fecha o un código y devuelven un cálculo (impuestos, cuotas, descuentos), como el Ejemplo 5.
- **Carga y revisión de datos:** antes de procesar archivos, muchas herramientas permiten revisar un registro por pantalla con `print` y corregirlo con `input`.
- **Prototipado y aprendizaje:** cualquier idea se puede probar en segundos escribiendo un script corto que lea un dato y muestre un resultado.
- **Pruebas de validación:** los desarrolladores usan la terminal para verificar rápidamente funciones y conversiones antes de integrar el código en una aplicación mayor.

## 7. Uso en producción

- **No se deja `input()` en el nivel superior del módulo ni dentro de clases del dominio.** En un script educativo, las llamadas a `input` seguidas de `print` son normales; en un proyecto real la lectura de datos se separa del procesamiento y jamás se incrusta dentro del constructor (`__init__`) ni de los métodos de negocio de una clase, para que los objetos sean reutilizables y verificables sin intervención manual en consola.
- **Separar lectura, conversión y cálculo.** Programar la validación de los datos antes de convertirlos evita que un error de tipeo llegue hasta el cálculo.
- **Preferir f-strings para el formato.** Son más legibles que la concatenación con `+` y `str(...)` y producen menos errores al editar mensajes.
- **Los mensajes no deben ocultar errores.** En producción, un dato inválido se registra y se reintenta o se reporta; no se imprime un resultado calculado con valores por defecto.
- **Muestra de estructura de un script organizado** (conocimiento previo adelantado; el bloque `if __name__ == "__main__":` se explica más adelante en el curso):

```text
def procesar(datos):
    ...

if __name__ == "__main__":
    entrada = input("Dato: ")
    print(procesar(entrada))
```

- **Diferencia entre ejemplo educativo y producción:** este documento usa `print` como vitrina del resultado; un sistema en producción registra eventos con un mecanismo de registro (*logging*), que permite filtrar por severidad y guardar histórico. Además, los datos fijos de los ejemplos (porcentajes, mensajes) en un sistema real provienen de configuración o base de datos, nunca escritos a mano en el código.
- **Seguridad:** el material original del curso compara contraseñas escritas en claro dentro del código; eso jamás debe hacerse en producción. Las credenciales se guardan de forma protegida y se verifican con funciones de hash diseñadas para ello.

## 8. Errores comunes y recomendaciones

1. **Unir texto y número con `+`.** Python se niega a sumar tipos distintos. Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, no se puede unir str e int con +
edad = 25
print("Edad: " + edad)
```

Salida real: `TypeError: can only concatenate str (not "int") to str`. Diagnóstico: el mensaje del error indica los dos tipos en conflicto. Solución: `str(edad)`, una f-string o el separador por comas de `print`.

2. **Convertir texto que no es numérico.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: ValueError, "12a" no representa un entero
texto = "12a"
numero = int(texto)
print(numero)
```

Salida real: `ValueError: invalid literal for int() with base 10: '12a'`. Solución: validar el contenido antes de convertir o capturar la excepción, como en el Ejemplo 6.

3. **Suponer que `input` devuelve un número.** `edad = input(...)` deja texto en la variable; comparaciones como `edad == 18` darán `False` siempre, sin ningún aviso. Regla: convertir en el momento de asignar (`int(input(...))`) o validar antes de usar.

4. **Espacios accidentales en la respuesta.** Si el usuario escribe ` Ana ` con espacios, `" Ana " != "Ana"`. Se corrige con `.strip()` (Ejemplo 6).

5. **Copiar la expresión `int and str(input(...))` del material original.** En `REPASO(01)_CLASSS_ONE.py` (línea 43) aparece `int and str(input(...))`; no convierte nada: `int` es un objeto verdadero y el operador `and` devuelve el operador derecho, de modo que el resultado equivale a `str(input(...))`. Demostración ejecutable:

```python
entrada = "1990-01-01"
valor = int and str(entrada)
print(type(valor).__name__, valor)
```

Resultado esperado:

```text
str 1990-01-01
```

La intención del autor era convertir; la forma correcta es `int(input(...))`. Nunca repliques esa expresión.

6. **Mezclar muchos `print` para una sola tabla.** Cuando el formato crece, agrupa la salida en una f-string; el formato complejo se cubre en [cadenas](../chapter-two/cadenas.md).

## 9. Resumen

- `print` es la función de salida: muestra valores, separa con `sep` (por defecto un espacio) y termina con `end` (por defecto salto de línea).
- `input` es la función de entrada: muestra un prompt y devuelve **siempre** una cadena de texto.
- Los números se obtienen convirtiendo de forma explícita: `int(input(...))`, `float(input(...))`.
- Para mostrar texto y números juntos se usa `str(...)`, la coma de `print` o, preferiblemente, una f-string.
- Las f-strings permiten incrustar expresiones con llaves y formatear números (`:.2f`).
- `try/except` protege la lectura de datos contra respuestas inválidas, Ctrl+C y fin de entrada; su estudio completo está en [excepciones](../../Intermedio/chapter-four/excepciones.md).
- En producción, la entrada no se hace con `input` a nivel de módulo y los resultados se registran con herramientas de registro, no solo con `print`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L21-44, L969-991) | `CLASE_ONE.py` | `input`, `int`/`float(input(...))`, `print` con concatenación, f-strings, tipos básicos | Se ordenó la progresión entrada → conversión → salida, se documentaron `sep` y `end`, y se explicó por qué `input` devuelve texto y pertenece a `builtins` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(01)_CLASSS_ONE.py` (L4-9, L43) | `REPASO(01)_CLASSS_ONE.py` | Lectura de nombre, `len`, rebanado inicial, expresión `int and str(input(...))` | Se conservó el uso de `input` y se documentó en la sección 8 por qué la expresión de la L43 no convierte el dato |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L150-155) | `REPASO(02)_CLASS_ONE.py` | Distinción entre función (`función(dato)`) y método (`dato.metodo()`) | Se incorporó desde el primer tema para que la notación sea familiar en los siguientes |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/ejemplo1.py` (L1-4, L17) | `ejemplo1.py` | `int`/`float`/`str` con `input`, redondeo con `round` | Se reutilizó la idea de la calculadora de cuotas como Ejemplo 5, con constantes nombradas y formato de salida explicado |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLO_IN.py` (L1-17) | `EJEMPLO_IN.py` | `try` con `except KeyboardInterrupt, EOFError`, `.strip().capitalize()`, operador `in` | Se adaptó al Ejemplo 6 como lectura robusta; se añadió `except ValueError` y el bloque `else`, que el original no incluye |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clase_One.py` (L146, L178-185) | `Clase_One.py` | `print(..., sep="")`, comparación entre concatenar con `str(...)` y separar argumentos con comas, saltos de línea `\n` | Se integraron las variantes para combinar texto con valores y el parámetro `sep` en las secciones 3 y 4 |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L3-200) | `BUENAS_PRACTICAS.py` | Contraste explícito entre invocar `input()`/`print()` dentro de `__init__` (mala práctica) y extraer la lectura a una función externa | Se incorporó en la sección 7 como regla de arquitectura en producción: desacoplar las clases y la lógica de negocio de la entrada/salida por terminal |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` (L8-9, L38-40) | `Con_TextBlob.py` | Secuencias de escape ANSI (`\x1b[1;33m`, `\x1b[0;37m`) en `input(...)` y `__str__` para colorear la salida en consola | Se precisó en la sección 3 que `\x1b` es un escape hexadecimal de cadena en Python mientras que el color depende del soporte ANSI de la terminal |

**Fundamento complementario:** (1) el bloque `if __name__ == "__main__":` de la sección 7 no aparece en los primeros ejercicios básicos (aunque sí se emplea más adelante en `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py`); aquí se presenta solo como adelanto de organización de scripts. (2) Los especificadores de formato dentro de f-strings (`{valor:.2f}`) tampoco aparecen en el material original; se usan aquí como base del formato de números y se retoman en [tipos de datos](tipos_datos.md).

## 11. Referencias oficiales

- <https://docs.python.org/3/library/functions.html#input> — documentación oficial de la función integrada `input`: contrato de entrada, prompt y valor devuelto.
- <https://docs.python.org/3/library/functions.html#print> — documentación oficial de la función integrada `print`: parámetros `sep` y `end`.
- <https://docs.python.org/3/tutorial/inputoutput.html#tut-f-strings> — tutorial oficial sobre literales de cadena formateados (f-strings) y especificadores de formato.
- <https://docs.python.org/3/tutorial/> — tutorial oficial de Python, punto de partida para entrada y salida de datos.
