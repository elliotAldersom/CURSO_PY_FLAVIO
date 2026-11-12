# Variables y constantes en Python

## 2. Introducción

Un programa necesita recordar datos entre una línea y la siguiente: el nombre que acaba de leer, el precio que va a calcular, el contador de intentos. Para eso existen las **variables**: nombres con los que el programador identifica un valor guardado en memoria.

Una **variable** no es el valor en sí, sino un nombre que apunta a ese valor. Al escribir `edad = 30`, el programa asocia el nombre `edad` con el número `30`; después, escribir `edad` equivale a usar ese número. El nombre se elige para que el código se lea como una frase comprensible: `pago_mensual` comunica más que `x`.

Por qué existen: sin nombres, cada resultado intermedio tendría que perderse o reutilizarse de forma caótica. Con variables, un cálculo se expresa una vez y se reutiliza cuantas veces haga falta. Su importancia en Python es doble: son la base de toda la programación y, además, reflejan el estilo del proyecto, porque Python no exige declararlas con un tipo: la variable adopta el tipo del valor que recibe.

## 3. Fundamentos y conceptos

**Asignación.** El signo `=` es el operador de **asignación**: toma el valor de la derecha y lo asocia al nombre de la izquierda. Se lee "nombre toma valor", no "nombre es igual a valor" (esa confusión con el operador de comparación `==` se trata en [operadores](operadores.md) y en [condicionales](condicionales.md)).

**Declaración y definición.** En Python no hay una línea separada para declarar una variable: el primer `nombre = valor` la crea (la material original lo llama "declarar y definir"). Asignar de nuevo a un mismo nombre **reasigna** el valor; la variable anterior queda descartada sin comandos extra.

**Tipado dinámico.** La misma variable puede apuntar a valores de tipos distintos en momentos distintos: `contador = 5` y más adelante `contador = "cinco"` son instrucciones válidas. Python asocia el tipo con el **valor**, no con el nombre. Esta flexibilidad es el **tipado dinámico** que define al lenguaje; el catálogo de tipos se revisa en [tipos de datos](tipos_datos.md). Conviene no confundir esta reasignación dinámica (como `x = 5; x = 5.4; x = "Hola"`) con el **polimorfismo de inclusión (subtipos)** de la programación orientada a objetos: reasignar cambia a qué objeto apunta un identificador, mientras que el polimorfismo permite tratar instancias de distintas clases bajo una interfaz común (tema desarrollado en [polimorfismo](../../Intermedio/chapter-five/polimorfismo.md)).

**Reglas de los nombres (identificadores).** Un nombre válido: (1) puede contener letras, dígitos y guion bajo `_`; (2) no puede empezar por un dígito; (3) distingue mayúsculas de minúsculas (`Edad` y `edad` son variables distintas); (4) no puede ser una palabra reservada del lenguaje (`if`, `class`, `for`, `import`...). Los nombres se escriben en **snake_case** (minúsculas y guiones bajos), por ejemplo `monto_total`.

**Convención de constantes.** Un valor que no debe cambiar durante la ejecución (porcentajes de impuesto, límites, claves de configuración) se escribe en **MAYÚSCULAS_CON_GUION_BAJO**, por ejemplo `TASA_IMPUESTO = 0.19`. Python no impide reasignar una constante; la convención es un acuerdo de legibilidad que el lenguaje respeta pero no verifica. Esta convención es **fundamento complementario** (PEP 8) y no aparece explícitamente en el material original.

**Asignación aumentada.** Los operadores `+=`, `-=`, `*=`, `/=` y `**=` combinan operación y asignación: `total += 10` significa `total = total + 10`. Ahorran texto y expresan la intención "acumular". Atención: el material original comenta que `numero += 1` con `numero = 21` imprime 21; en realidad imprime **22**, porque la operación se aplica antes de la reasignación (ver sección 8).

**Asignación encadenada.** `v1 = v2 = 0` asigna el mismo valor a varios nombres en una sola instrucción; es el modo idiomático de inicializar varias variables (aparece en los ejercicios del curso).

**La palabra `del`.** `del nombre` elimina la asociación entre el nombre y su valor; después de usarla, el nombre deja de existir en ese ámbito. También funciona sobre elementos de listas, claves de diccionarios y atributos de objetos (incluidas las propiedades gestionadas con `@property`, donde `del objeto.propiedad` invoca el método `@propiedad.deleter`, tema que se estudia en [encapsulamiento](../../Intermedio/chapter-five/encapsulamiento.md)). Eliminar una variable desvincula el nombre, no "borra la memoria" de forma manual: el **lenguaje Python** establece gestión automática de memoria y recolección de basura para los objetos inaccesibles, mientras que la estrategia concreta de **conteo de referencias inmediato combinado con un recolector cíclico de basura** es propia de la implementación **CPython** (otras implementaciones, como PyPy, utilizan recolectores distintos sin garantizar liberación inmediata tras `del`).

**Ámbito (preview).** Dónde vive una variable (dentro de un bloque, un módulo, una función) se llama **ámbito** y se estudia en el nivel intermedio; en este capítulo todas las variables se crean en el archivo principal.

## 4. Sintaxis y funcionamiento

Sintaxis de la asignación:

```text
nombre = valor
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `nombre` | Identificador válido (letras, dígitos, `_`, sin empezar por dígito) | `pago_mensual` |
| 2 | `=` | Operador de asignación: asocia el valor de la derecha al nombre | `edad = 30` |
| 3 | `valor` | Cualquier expresión evaluada primero: literal, resultado, lectura | `total = a + b` |
| 4 | Reasignación | Un nombre ya usado recibe un nuevo valor; el anterior se descarta | `nombre = "Ana"` luego `nombre = "Luis"` |

Operadores de asignación aumentada:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `+=` | Suma y reasigna | `contador += 1` |
| 2 | `-=` | Resta y reasigna | `saldo -= 50` |
| 3 | `*=` | Multiplica y reasigna | `factor *= 2` |
| 4 | `/=` | Divide y reasigna (el resultado siempre es decimal) | `total /= 4` |
| 5 | `**=` | Potencia y reasigna | `base **= 2` |

Funcionamiento interno: cuando Python ejecuta `total = a + b`, primero evalúa la expresión de la derecha (obtiene un valor), luego asocia ese valor al nombre de la izquierda **reemplazando** cualquier valor anterior en el mismo ámbito. No hay que avisar el tipo ni reservar espacio: la asociación nombre → valor es lo que persiste.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Crear, reasignar y leer una variable.**

```python
nombre = "FLAVIO"
print(nombre)
nombre = "GERARDO"
print(nombre)
```

Explicación línea por línea:

- Línea 1: se asocia el nombre `nombre` al texto `"FLAVIO"`.
- Línea 2: se muestra el valor asociado: `FLAVIO`.
- Línea 3: se reasigna; el valor anterior se sustituye por `"GERARDO"`.
- Línea 4: se muestra el valor actual: `GERARDO`. Solo el último valor queda asociado al nombre.

Resultado esperado:

```text
FLAVIO
GERARDO
```

**Ejemplo 2 — Variables como operandos de un cálculo.**

```python
a = 2
b = 3
c = a + b
print(c)
```

Explicación línea por línea:

- Líneas 1-2: dos nombres guardan dos números; `a` y `b` son solo apodos de `2` y `3`.
- Línea 3: Python evalúa `2 + 3` y asocia el resultado `5` a `c`.
- Línea 4: se muestra `5`. En este archivo, `c` sigue valiendo `5` hasta que se reasigne.

Resultado esperado:

```text
5
```

**Ejemplo 3 — Tipado dinámico: un nombre, dos tipos.**

```python
dato = 17
print(dato)
dato = "diecisiete"
print(dato)
```

Explicación línea por línea:

- Línea 1: `dato` apunta al entero `17`.
- Línea 2: se imprime `17`.
- Línea 3: el mismo nombre ahora apunta a una cadena; no hubo que cambiar nada de declaración.
- Línea 4: se imprime `diecisiete`. El tipo viaja con el valor, no con el nombre.

Resultado esperado:

```text
17
diecisiete
```

### Intermedio

**Ejemplo 4 — Constantes con nombre: reparto de una donación.**

```python
donacion = 1000.0
MEDICINA_GENERAL = 0.45
CARDIOLOGIA = 0.30
PEDIATRIA = 0.15
TRAUMATOLOGIA = 0.10

monto_mg = donacion * MEDICINA_GENERAL
monto_c = donacion * CARDIOLOGIA
monto_p = donacion * PEDIATRIA
monto_t = donacion * TRAUMATOLOGIA

print("Medicina general:", monto_mg)
print("Cardiologia:", monto_c)
print("Pediatria:", monto_p)
print("Traumatologia:", monto_t)
```

Explicación de las decisiones tomadas:

- Los cuatro porcentajes se escriben en MAYÚSCULAS porque son constantes del negocio: si mañana cambian, se editan en un solo lugar y ningún lector las confunde con valores calculados.
- Los nombres intermedios (`monto_mg`...) van en snake_case porque son resultados, no constantes; la diferencia de estilo distingue de un vistazo qué se puede tocar y qué no.
- `donacion` se define con decimal porque es un importe; su valor es un ejemplo fijo para que el resultado sea reproducible.
- La suma de los cuatro porcentajes es 1.0 (100 %); una comprobación de esa invariant es una práctica habitual en producción.

Resultado esperado:

```text
Medicina general: 450.0
Cardiologia: 300.0
Pediatria: 150.0
Traumatologia: 100.0
```

**Ejemplo 5 — Intercambio de valores y asignación aumentada.**

```python
v1 = 10
v2 = 20

v0 = v1
v1 = v2
v2 = v0

print("v1 =", v1)
print("v2 =", v2)

contador = 21
contador += 1
print("contador =", contador)
```

Explicación de las decisiones tomadas:

- El intercambio necesita una tercera variable (`v0`): si se hiciera `v1 = v2` primero, el valor original de `v1` se perdería. El orden guarda → sobrescribir → recuperar es la clave.
- `contador += 1` equivale a `contador = contador + 1`; el resultado mostrado es **22**, no 21. El comentario del material original (`CLASE_ONE.py` L74) que afirma "va a salir 21" es incorrecto: la operación se evalúa antes de reasignar (ver sección 8).
- Los `print` usan la coma de `print` para etiquetar la salida, técnica de la sección 4 de [entradas y salidas](entradas_y_salidas.md).

Resultado esperado:

```text
v1 = 20
v2 = 10
contador = 22
```

### Avanzado

**Ejemplo 6 — Presupuesto reescrito con buenas prácticas y limpieza con `del`.**

Versión con nombres poco expresivos (así suele llegar el código de un primer borrador):

```python
x = 5000
y = 0.10
z = x * y
print(z)
```

Versión mejorada:

```python
PRESUPUESTO_ANUAL = 5000
TASA_AHORRO = 0.10

ahorro_anual = PRESUPUESTO_ANUAL * TASA_AHORRO
ahorro_mensual = ahorro_anual / 12

print("Ahorro anual:", ahorro_anual)
print("Ahorro mensual:", round(ahorro_mensual, 2))

datos_temporales = [PRESUPUESTO_ANUAL, TASA_AHORRO]
del datos_temporales

try:
    print(datos_temporales)
except NameError:
    print("La variable datos_temporales ya no existe")
```

Explicación de las decisiones tomadas:

- `x`, `y` y `z` comunica nada; `PRESUPUESTO_ANUAL`, `TASA_AHORRO` y `ahorro_anual` documentan el dominio sin necesidad de comentarios. Mantenibilidad: el cambio de una tasa toca un solo lugar y es verificable al releer el archivo.
- Las constantes van en mayúsculas y los resultados en snake_case: el estilo codifica el rol de cada nombre.
- `round(ahorro_mensual, 2)` limita el resultado mostrado a dos decimales; el valor interno no cambia (fue explicado en [entradas y salidas](entradas_y_salidas.md)).
- `del datos_temporales` elimina el nombre intermedio una vez que ya no aporta; el `try/except NameError` demuestra que el nombre dejó de existir sin tumbar el programa. Este patrón de comprobación se usa aquí solo con fines didácticos: en código real simplemente no se vuelve a usar el nombre eliminado.
- El archivo completo es el mismo programa en ambas versiones: refactorizar nombres no cambia la salida del cálculo, solo su legibilidad.

Resultado esperado (versión mejorada):

```text
Ahorro anual: 500.0
Ahorro mensual: 41.67
La variable datos_temporales ya no existe
```

## 6. Aplicaciones en el mundo real

- **Constantes de negocio:** tasas impositivas, límites de retiro, porcentajes de comisión; en cualquier sistema financiero viven como constantes con nombre mayúsculas.
- **Acumuladores y contadores:** totales de carrito, número de intentos de acceso, registros procesados; se actualizan con `+=` a lo largo del programa.
- **Variables de intercambio y estado:** algoritmos que reordenan datos (como el intercambio del Ejemplo 5) usan una variable temporal de apoyo.
- **Nombres como documentación:** en equipos, los nombres `cliente_activo` y `fecha_corte` reducen la necesidad de comentar el código; el estilo snake_case es un estándar del ecosistema Python.
- **Configuración y parámetros:** valores que cambian entre entornos (URLs, umbrales) se guardan en variables o constantes al inicio del archivo, nunca incrustados en medio de la lógica.

## 7. Uso en producción

- **PEP 8 como ley de estilo:** snake_case para variables y funciones, MAYÚSCULAS para constantes, sin letras ambiguas (`l`, `I`, `O`). Es el estándar oficial de estilo de Python y la referencia completa está en la sección 11.
- **Evitar números mágicos:** un `0.19` suelto en medio de una fórmula obliga a leer el contexto; `TASA_IMPUESTO = 0.19` se entiende solo. La mejora se muestra en el Ejemplo 6.
- **Nombres cortos solo en un contexto corto:** `i` puede ser aceptable dentro de un bucle de cinco líneas; fuera de ahí, el nombre debe describir el dominio.
- **No escribir secretos en el código:** el material original del curso compara y almacena contraseñas en texto plano dentro de los scripts (`CLASE_ONE.py` L239-242, `COSAS_GENERALES/contraseña_registro.py`). Eso es un anti-patrón de seguridad grave: las credenciales van en variables de entorno o en un almacén de secretos, nunca en el repositorio.
- **Reasignación controlada:** reasignar es potente, pero en código compartido el ciclo de vida de cada variable debe ser evidente; si un nombre cambia de significado a mitad de archivo, conviene dividir el bloque o renombrar.
- **No confundir estilo con validación:** que Python permita `contador = "texto"` no significa que sea correcto; en sistemas tipados con revisión estática se prefiere mantener el tipo coherente (análisis de tipos con *type hints* es un tema posterior del ecosistema, no de este capítulo).

## 8. Errores comunes y recomendaciones

1. **Usar una palabra reservada como nombre.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, class es palabra reservada de Python
class = 1
print(class)
```

Salida real: `SyntaxError: invalid syntax`. Python reserva `class` (y `if`, `for`, `import`...) para su sintaxis; usarla como nombre impide que el analizador distinga lenguaje de datos. Solución: renombrar, por ejemplo `clase_nueva = 1`.

2. **Empezar el nombre por un dígito.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: SyntaxError, el nombre no puede empezar por dígito
1nombre = "valor"
print(1nombre)
```

Salida real: `SyntaxError: invalid decimal literal`. Solución: `nombre1 = "valor"` o `primer_nombre = "valor"`.

3. **Usar una variable antes de asignarla.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: NameError, salario nunca fue asignada
print(salario)
```

Salida real: `NameError: name 'salario' is not defined`. Diagnóstico: revisar el orden de las líneas o el nombre (Python distingue `Salario` de `salario`).

4. **Creer que `+=` no cambia nada.** El material original (`CLASE_ONE.py` L74) comenta que `numero = 21; numero += 1` imprime 21; imprime 22. Comprobación ejecutable (ya mostrada en el Ejemplo 5): `contador = 21; contador += 1; print(contador)` → `22`. Confía en la ejecución, no en el comentario: verifica siempre el comportamiento real.

5. **Confundir asignación y comparación.** `total = 10` guarda un valor; `total == 10` produce un booleano (`True`/`False`) y no guarda nada. En condiciones (`if`) se usa `==`; el error clásico de escribir `=` ahí se analiza en [condicionales](condicionales.md).

6. **Sombrear funciones integradas.** Nombres como `list`, `str`, `print` o `input` funcionan, pero ocultan la herramienta original dentro del ámbito donde se redefinen y generan confusiones difíciles de depurar. Regla: nunca reutilizar nombres del catálogo básico de Python.

7. **Mayúsculas en todo o en nada.** Usar MAYÚSCULAS para valores calculados sugiere que son inmutables y confunde al lector; reservarlas para constantes reales es la mitad del valor de la convención.

## 9. Resumen

- Una variable asocia un nombre a un valor mediante el operador de asignación `=`; reasignar cambia el valor asociado sin declarar tipos.
- Python es de **tipado dinámico**: el tipo lo lleva el valor, no el nombre.
- Los nombres válidos usan letras, dígitos y `_`, no empiezan por dígito, distinguen mayúsculas y no pueden ser palabras reservadas.
- snake_case para variables; MAYÚSCULAS_CON_GUION_BAJO para constantes (convención PEP 8, fundamento complementario).
- `+=` y los demás operadores de asignación aumentada acumulan de forma explícita; `v1 = v2 = 0` asigna en cadena.
- `del` desvincula un nombre o invoca el eliminador de un atributo; la liberación de memoria corresponde al recolector automático de Python (en CPython, conteo de referencias más recolector cíclico).
- Los comentarios erróneos del material original se contrastan ejecutando el código: `numero += 1` con `numero = 21` produce 22.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L47-74) | `CLASE_ONE.py` | Definición de variable, reasignación, "declarar y definir", asignación aumentada `+=` | Se explicó el modelo de enlace nombre-valor, se documentaron las reglas de nombres y se corrigió el comentario erróneo de la L74 (el resultado es 22, no 21) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/ejemplo2.py` (L2-5, L7-10) | `ejemplo2.py` | Cuatro porcentajes fijos usados como constantes y sus cálculos | Se formalizó como convención de constantes MAYÚSCULAS (PEP 8) y se añadió el reparto completo como Ejemplo 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L41-74) | `Keyword_del.py` | `del` sobre variable, elemento de lista, rebanado y clave de diccionario | Se documentó `del` sobre variables y la diferencia entre recolección automática en Python y conteo de referencias en CPython; la parte `class Stack` pertenece a [clases y objetos](../../Intermedio/chapter-five/clases_y_objetos.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS/EJERCICIO_1.py` (L1-15) | `EJERCICIO_1.py` | Asignación encadenada `v1=v2=0` e intercambio de valores con variable temporal | Se convirtió en el Ejemplo 5, con explicación del orden del intercambio y del resultado correcto de `contador += 1` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Polimorfismo.py` (L23-27) | `Polimorfismo.py` | Reasignación dinámica `x = 5`, `x = 5.4`, `x = "Hola"` rotulada en el archivo como "polimorfismo de inclusión" | Se aclaró en la sección 3 que reasignar un mismo nombre a valores de distintos tipos es **tipado dinámico**, no polimorfismo de inclusión o subtipos ([polimorfismo](../../Intermedio/chapter-five/polimorfismo.md)) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_@Property.py` (L53-62, L82) | `Decoradores_@Property.py` | Eliminación de atributos privados con `del self.__name` e invocación de `@Borrar_Datos.deleter` mediante `del flavio.Borrar_Datos` | Se anticipó en la sección 3 el comportamiento de `del` sobre atributos gestionados con `@property`, desarrollado en [encapsulamiento](../../Intermedio/chapter-five/encapsulamiento.md) |

**Fundamento complementario:** las convenciones de nomenclatura PEP 8 (snake_case para variables, MAYÚSCULAS para constantes) no se enseñan explícitamente en el material original; se incorporan aquí como base de estilo para todos los documentos del curso. La guía oficial se cita en la sección 11.

## 11. Referencias oficiales

- <https://docs.python.org/3/reference/simple_stmts.html#assignment-statements> — referencia oficial del lenguaje sobre sentencias de asignación, reasignación y enlace de nombres.
- <https://docs.python.org/3/reference/simple_stmts.html#the-del-statement> — referencia oficial de la sentencia `del` y su efecto sobre nombres y atributos.
- <https://docs.python.org/3/tutorial/introduction.html> — tutorial oficial de introducción a Python: primeras variables, números y cadenas.
- <https://peps.python.org/pep-0008/> — PEP 8, guía de estilo oficial de Python: convenciones de nombres para variables y constantes.
