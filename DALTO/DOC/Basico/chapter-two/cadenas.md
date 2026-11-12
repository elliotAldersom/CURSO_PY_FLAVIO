# Cadenas de texto en Python

## 2. Introducción

Todo programa maneja texto: nombres, correos, mensajes, rutas, palabras dentro de un archivo. Una **cadena de texto** (del inglés *string*) es una secuencia de caracteres escrita entre comillas, por ejemplo `"Hola"` o `'17'`. Este documento la trata como lo que es en Python: una colección ordenada de caracteres a la que se accede por posición y sobre la cual existen decenas de operaciones preparadas.

¿Qué problema resuelve? Sin cadenas, recibir un dato del usuario, comprobar si tiene un formato válido, pasarlo a mayúsculas, separarlo en palabras o insertarlo en un mensaje obligaría a escribir todo a mano. Con cadenas, esas tareas son llamadas de una línea. Su importancia es doble: primero, porque `input()` **siempre** devuelve una cadena, así que casi todo programa interactivo empieza procesando texto (ver [entradas y salidas](../chapter-one/entradas_y_salidas.md)); segundo, porque la cadena es el puente entre el dato capturado y el dato numérico o de lista que el programa necesita (`int("17")`, `"a,b,c".split(",")`).

Un detalle que aparece desde el primer método y se explica en la sección 3: las cadenas son **inmutables**, es decir, no se pueden alterar "en el lugar"; cuando se aplica una operación, Python devuelve una **cadena nueva** y la original queda intacta.

## 3. Fundamentos y conceptos

**Cadena como secuencia indexada.** Cada carácter tiene una posición (**índice**) que empieza en **0**: en `"Python"` la `P` es el índice 0 y la `n` el 5. La función `len(cadena)` devuelve la cantidad de caracteres; como los índices llegan hasta `len - 1`, pedir la posición `len` produce un error (sección 8). La cadena vacía `""` tiene longitud 0.

**Índices negativos.** Python admite contar desde el final: `-1` es el último carácter, `-2` el penúltimo y así sucesivamente. `cadena[-1]` es la forma corta de "último elemento", un recurso que también usan las [listas](listas.md).

**Rebanadas (*slicing*).** La expresión `cadena[inicio:fin:paso]` extrae un trozo: `inicio` se incluye, **`fin` no** (otra vez el límite exclusivo, igual que en `range`), y `paso` indica el incremento. Los valores pueden omitirse (`cadena[:3]`, `cadena[3:]`, `cadena[::2]`) y ser negativos; `cadena[::-1]` devuelve la cadena invertida. Una rebanada siempre entrega una **cadena nueva**, aunque sus caracteres sean los mismos.

**Inmutabilidad: por qué y para qué.** No existe `cadena[0] = "h"`: Python lo rechaza. El diseño oficial razona así — una cadena fija puede guardarse como **clave de un diccionario** (porque su valor no cambia, su identificador hash tampoco) y puede compartirse entre varias partes del programa sin que nadie la altere por sorpresa. Consecuencia práctica: los métodos de cadena **devuelven un valor**, nunca modifican el original. Por eso `texto.upper()` solo produce un resultado desechable y el cambio real exige `texto = texto.upper()`.

**Función frente a método.** El material dedica un archivo a esta distinción y conviene fijarla aquí: una **función** se escribe `funcion(dato)` y pertenece al lenguaje (`len(cadena)`, `type(dato)`, `dir(dato)`); un **método** se escribe `dato.metodo()` y pertenece a la clase del dato (`cadena.upper()`). Llamar a un método sin paréntesis entrega el objeto del método en lugar de ejecutarlo, y llamar a una función sin paréntesis no hace nada.

**Buscar: `find` e `index`.** Los dos encuentran la primera posición de un texto dentro de la cadena, pero difieren en el fallo: `find` devuelve **-1** cuando no hay coincidencia y el programa sigue; `index` lanza una **excepción** (un error que detiene el programa si nadie lo captura). Elegir uno u otro depende de si "no encontrado" es un caso normal o una anomalía.

**Convertir: `split` y `join`.** `split(separador)` **divide** la cadena y devuelve una **lista** de trozos; `join(iterable)` hace el camino inverso: une una lista de cadenas con un separador. Son el puente natural entre el mundo del texto y el mundo de las listas (ver [listas](listas.md)).

**Validar: la familia `is*`.** `isnumeric()`, `isdigit()`, `isalpha()`, `isspace()`, `isalnum()`, `islower()` e `isupper()` examinan la cadena y devuelven `True` o `False`. Detalle importante: solo son verdaderas si **todos** los caracteres cumplen la condición; `"1234".isnumeric()` es `True`, pero `"12 34".isnumeric()` es `False` porque el espacio no es un dígito.

**Comparar cadenas.** `==` exige los mismos caracteres en el mismo orden, distinguiendo mayúsculas (`"beta" > "Beta"`). Las comparaciones `>` y `<` son lexicográficas: se ordenan como en un diccionario, y si un texto es prefijo de otro, el más largo es mayor (`"alpha" < "alphabet"`).

**f-strings y `str.format()`.** La interpolación literal `f"Edad: {edad}"` (introducida en Python 3.6) incrusta expresiones entre llaves evaluadas en el punto donde se escribe la cadena; se presentó en [entradas y salidas](../chapter-one/entradas_y_salidas.md) y es la forma predominante del material. Antes de las f-strings, el mecanismo estándar era el método `"Edad: {}".format(edad)` (presente en el bloque de POO del curso para armar plantillas con códigos de color ANSI), donde cada `{}` actúa como marcador posicional o con nombre reemplazado por los argumentos de `format(...)`. En código moderno se prefieren las f-strings por legibilidad y menor sobrecarga cuando las variables ya están disponibles, reservando `str.format()` para plantillas definidas de antemano que se reutilizan más adelante. El formato avanzado (especificadores de presentación y expresiones dentro de las llaves) se estudia junto a [funciones](../../Intermedio/chapter-two/funciones.md).

**Secuencias de escape.** Dentro de una cadena, la barra invertida `\` da significado especial al carácter siguiente: `\n` salto de línea, `\t` tabulador, `\\` barra literal y `\"` comilla literal. Para escribir rutas de Windows sin escapar cada barra existen las cadenas crudas (`r"C:\temp"`), que desactivan la interpretación de `\`. Este tema se retoma en la sección 4.

**Iterar una cadena.** Un `for` recorre una cadena carácter a carácter (`for letra in "hola":`), tal como se ve en [bucles](bucles.md).

## 4. Sintaxis y funcionamiento

Sintaxis de acceso y de llamada a métodos:

```text
<cadena>[<índice>]
<cadena>[<inicio>:<fin>:<paso>]
<cadena>.<método>(<argumento>)
```

Componentes de una rebanada:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `inicio` | Primera posición incluida; 0 cuando se omite | `texto[:3]` empieza al inicio |
| 2 | `fin` | Primera posición **excluida**; hasta el final cuando se omite | `texto[3:]` del 3 en adelante |
| 3 | `paso` | Incremento entre posiciones; 1 cuando se omite | `texto[::2]` toma de 2 en 2 |
| 4 | Índices negativos | Cuentan desde el final (-1 es el último) | `texto[-3:]` últimos tres |

Métodos de transformación (todos devuelven una cadena nueva):

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `upper()` | Todo en mayúsculas | `"hola".upper()` → `"HOLA"` |
| 2 | `lower()` | Todo en minúsculas | `"HOLA".lower()` → `"hola"` |
| 3 | `capitalize()` | Primera en mayúscula, resto en minúsculas | `"hOLA".capitalize()` → `"Hola"` |
| 4 | `title()` | Primera letra de cada palabra en mayúscula | `"hola mundo".title()` → `"Hola Mundo"` |
| 5 | `swapcase()` | Intercambia mayúsculas y minúsculas | `"Hola".swapcase()` → `"hOLA"` |
| 6 | `strip()` | Quita espacios (y saltos de línea) de los dos extremos | `"  hola  ".strip()` → `"hola"` |
| 7 | `lstrip()` | Quita solo del extremo izquierdo | `"  hola  ".lstrip()` → `"hola  "` |
| 8 | `rstrip()` | Quita solo del extremo derecho | `"  hola  ".rstrip()` → `"  hola"` |
| 9 | `replace(a, b)` | Reemplaza **todas** las apariciones de `a` | `"hola hola".replace("hola", "hi")` |
| 10 | `split(sep)` | Divide en una lista; sin argumento, divide por espacios | `"a,b".split(",")` → `["a", "b"]` |
| 11 | `rsplit(sep)` | Como `split`, pero divide desde la derecha | `"a,b,c".rsplit(",", 1)` |
| 12 | `partition(sep)` | Parte en tres: antes, separador, después | `"a=b".partition("=")` → `("a", "=", "b")` |
| 13 | `join(iterable)` | Une cadenas de un iterable con un separador | `", ".join(["a", "b"])` → `"a, b"` |
| 14 | `format(...)` | Sustituye marcadores `{}` por los argumentos dados | `"Hola {}".format("Ana")` → `"Hola Ana"` |

Métodos de búsqueda y validación:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `find(s)` | Índice de la primera aparición; -1 si no está | `"abc".find("z")` → `-1` |
| 2 | `index(s)` | Como `find`, pero lanza `ValueError` si no está | `"abc".index("b")` → `1` |
| 3 | `count(s)` | Número de apariciones de `s` | `"aXaX".count("X")` → `2` |
| 4 | `startswith(s)` | `True` si la cadena empieza por `s` | `"hola".startswith("ho")` |
| 5 | `endswith(s)` | `True` si la cadena termina por `s` | `"hola".endswith("la")` |
| 6 | `isnumeric()` | `True` si todos los caracteres son numéricos | `"123".isnumeric()` |
| 7 | `isdigit()` | `True` si todos son dígitos | `"123".isdigit()` |
| 8 | `isalpha()` | `True` si todos son letras | `"abc".isalpha()` |
| 9 | `isspace()` | `True` si todos son espacios (o tabulaciones/saltos) | `" ".isspace()` |
| 10 | `isalnum()` | `True` si todos son letras o dígitos | `"abc123".isalnum()` |
| 11 | `islower()` | `True` si hay letras y todas son minúsculas | `"hola".islower()` |
| 12 | `isupper()` | `True` si hay letras y todas son mayúsculas | `"HOLA".isupper()` |

Funcionamiento: una expresión de acceso (`texto[1:4]`) se evalúa creando una cadena nueva con los caracteres pedidos; el índice fuera de rango detiene el programa con `IndexError` (sección 8). En una llamada `texto.metodo(arg)`, Python ejecuta el método de la clase `str` y **devuelve** un valor: una cadena (los métodos de la tabla 1), un entero (`find`, `index`, `count`), un booleano (los métodos `is*`, `startswith`, `endswith`) o una tupla (`partition`). Como ninguna de esas operaciones modifica el original, el resultado hay que **guardarlo** o **mostrarlo** para que no se pierda.

Secuencias de escape, ejecutadas:

```python
print("Primera línea\nSegunda línea")
print("Ruta: C:\\temp\\archivo.txt")
print(r"Ruta literal: C:\temp\archivo.txt")
```

Resultado esperado:

```text
Primera línea
Segunda línea
Ruta: C:\temp\archivo.txt
Ruta literal: C:\temp\archivo.txt
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Posiciones, longitud y primera rebanada.**

```python
dato = "Pepito es un pepe feliz"
print(dato[0])
print(dato[0:2])
print(len(dato))
print(dato[-1])
```

Explicación línea por línea:

- Línea 1: se crea la cadena; el índice 0 corresponde a la letra `P`.
- Línea 2: `dato[0:2]` toma desde la posición 0 **hasta la 2 sin incluirla**, es decir, dos caracteres: `Pe`. La rebanada no "cuenta hasta el 2", sino "hasta antes del 2" (regla de la sección 4).
- Línea 3: `len()` es una función, no un método: cuenta los caracteres, espacios incluidos.
- Línea 4: el índice negativo `-1` entrega el último carácter sin calcular la longitud.

Resultado esperado:

```text
P
Pe
23
z
```

Este mismo patrón (rebanada con longitud elegida por el usuario, `dato[0:escoger]`) aparece en `Ejm_String.py` y en `REPASO(01)_CLASSS_ONE.py`, donde se comenta que `dato[0:2]` imprime `"Pepit"`; el valor real es `Pe` (sección 8).

**Ejemplo 2 — Rebanadas omitidas, negativas y con paso.**

```python
texto = "Python"
print(texto[1:4])
print(texto[:3])
print(texto[3:])
print(texto[-3:])
print(texto[::2])
print(texto[::-1])
```

Explicación línea por línea:

- Línea 2: posiciones 1, 2 y 3 → `yth`.
- Línea 3: `inicio` omitido, arranca en 0 hasta la 3 sin incluirla → `Pyt`.
- Línea 4: `fin` omitido, va de la 3 hasta el final → `hon`.
- Línea 5: desde la -3 (que es la `h`) hasta el final → `hon`.
- Línea 6: paso 2 desde el inicio → posiciones 0, 2 y 4 → `Pto`.
- Línea 7: paso -1 desde el final: invierte la cadena completa → `nohtyP`.

Resultado esperado:

```text
yth
Pyt
hon
hon
Pto
nohtyP
```

**Ejemplo 3 — Mayúsculas, minúsculas y espacios.**

```python
texto = "  hola MUNDO  "
print(texto.strip())
print(texto.strip().lower())
print(texto.strip().capitalize())
print(texto.strip().title())
```

Explicación línea por línea:

- Línea 1: la cadena tiene dos espacios a cada lado, datos típicos de una entrada de usuario.
- Línea 2: `strip()` elimina los espacios exteriores → `hola MUNDO`.
- Línea 3: se **encadenan** métodos: `strip()` entrega una cadena y sobre esa cadena se aplica `lower()`. Cada eslabón recibe el resultado del anterior.
- Línea 4: `capitalize()` pone la primera letra en mayúscula y **todo lo demás** en minúscula → `Hola mundo` (no respeta la palabra posterior).
- Línea 5: `title()` trata cada palabra por separado → `Hola Mundo`.

Resultado esperado:

```text
hola MUNDO
hola mundo
Hola mundo
Hola Mundo
```

### Intermedio

**Ejemplo 4 — De cadena a lista: `split`, validar y volver a unir con `join`.**

```python
registro = "Ana,17,Lima"
campos = registro.split(",")
print(campos)
print(campos[0])
print(campos[1].isnumeric())
saludo = "Hola " + campos[0]
print(saludo)
```

Explicación de las decisiones tomadas:

- `split(",")` convierte un registro delimitado en una **lista** de tres campos; el tipo de dato resultante es `list`, y sus operaciones se documentan en [listas](listas.md). El material hace exactamente esta conversión en `REPASO(01)_CLASSS_ONE.py` L315.
- `campos[0]` accede al primer campo por índice: la lista y la cadena comparten la misma notación de posiciones.
- `campos[1].isnumeric()` valida que la edad sea un texto solo de dígitos **sin convertirla todavía**: se comprueba el formato antes de confiar en el dato (la conversión a número se hace cuando hace falta, ver [tipos de datos](../chapter-one/tipos_datos.md)).
- El saludo se arma con `+`; el camino inverso completo (`join`) se muestra en el Ejemplo 8.

Resultado esperado:

```text
['Ana', '17', 'Lima']
Ana
True
Hola Ana
```

**Ejemplo 5 — Buscar y contar dentro de un correo.**

```python
correo = "ana.perez@correo.com"
print(correo.find("@"))
print(correo.find("xyz"))
print(correo.index("@"))
print(correo.count("."))
print(correo.startswith("ana"))
print(correo.endswith(".com"))
```

Explicación de las decisiones tomadas:

- `find("@")` devuelve la posición del arroba; sirve para partir la dirección en usuario y dominio (aquí solo se muestra la posición).
- El segundo `find` demuestra el caso de fallo: **-1** es la señal de "no está", y el programa continúa sin detenerse.
- `index("@")` entrega la misma posición que `find` cuando hay coincidencia; la diferencia solo se ve cuando falta el texto (sección 8).
- `count(".")` cuenta los puntos: en una dirección de correo, dos puntos suelen indicar un formato sospechoso.
- `startswith` y `endswith` responden `True`/`False` y son la forma directa de validar prefijos y sufijos (extensiones de archivo, protocolos, esquemas).

Resultado esperado:

```text
9
-1
9
2
True
True
```

**Ejemplo 6 — Cadena a lista: comprobar si es capicúa.**

```python
numero = "12321"
caracteres = list(numero)
invertida = caracteres.copy()
invertida.reverse()
print(caracteres)
print(invertida)
print(caracteres == invertida)
```

Explicación de las decisiones tomadas:

- `list(numero)` convierte la cadena en una lista de caracteres: una cadena no se puede invertir "en el lugar", así que primero se pasa a un tipo mutable.
- `.copy()` crea una copia para no destruir el original al invertir; `.reverse()` sí modifica la lista **sobre la que se llama** (por eso se invierte la copia y no `caracteres`).
- La comparación `==` entre listas compara elemento a elemento y en el mismo orden; dos listas idénticas dan `True`.
- Este es el núcleo de `EJERCICIO_Capicua.py` L29-40, escrito allí dentro de funciones; aquí se presenta como script lineal, porque las funciones son tema del nivel intermedio.

Resultado esperado:

```text
['1', '2', '3', '2', '1']
['1', '2', '3', '2', '1']
True
```

### Avanzado

**Ejemplo 7 — Normalización de una entrada de usuario.**

```python
entrada = "  CAFÉ con LECHE  "
normalizado = entrada.strip().lower()
palabras = normalizado.split()
limpio = " ".join(palabras)
print(repr(limpio))
print(limpio == "café con leche")
```

Explicación de las decisiones tomadas:

- La entrada real llega con espacios accidentales y mayúsculas arbitrarias; **normalizar** antes de comparar es la regla de oro: primero `strip()` (extremos) y luego `lower()` (criterio de mayúsculas).
- `split()` **sin argumento** es deliberado: parte por cualquier racha de espacios y descarta los trozos vacíos, de modo que `"  a  b "` produce `["a", "b"]`. Con `split(" ")` los espacios múltiples generarían cadenas vacías (sección 8).
- `" ".join(palabras)` reconstruye el texto con **un solo espacio** entre palabras: el pipeline "romper y volver a armar" elimina espacios internos repetidos sin contarlos a mano.
- `repr(limpio)` muestra la cadena entre comillas con sus caracteres exactos, la forma honesta de depurar texto (un final de línea invisible se vería como `\n`).
- La comparación final confirma que la normalización produjo exactamente lo esperado; `islower()` sobre `entrada` habría dado `False` precisamente por los espacios y las mayúsculas.

Resultado esperado:

```text
'café con leche'
True
```

**Ejemplo 8 — Construir un reporte con f-strings, `enumerate` y `join`.**

```python
notas = [8.5, 9.0, 7.5]
lineas = []
for numero, nota in enumerate(notas, 1):
    lineas.append(f"Nota {numero}: {nota}")
reporte = "\n".join(lineas)
print(reporte)
```

Explicación de las decisiones tomadas:

- Cada línea se arma con una f-string (forma básica de la sección 3) y se **acumula en una lista** con `append` en lugar de concatenar sobre una variable.
- La razón es de rendimiento: `reporte = reporte + linea` dentro de un bucle crea una cadena nueva en cada vuelta (costo creciente), mientras que `"\n".join(lineas)` une todo en una sola pasada. Es la recomendación estándar de producción para generar texto.
- `enumerate(notas, 1)` numera desde 1 para que el reporte sea legible para humanos; el primer argumento de `enumerate` es la secuencia y el segundo el índice inicial (ver [bucles](bucles.md)).
- `"\n".join(...)` coloca un salto de línea entre las líneas: la secuencia de escape `\n` se explica en la sección 4. Además de listas, `join` acepta cualquier iterable de cadenas —incluidas expresiones generadoras como `"\n".join(f"{k}: {v}" for k, v in datos.items())`, empleadas en el bloque de POO del material y desarrolladas formalmente en niveles posteriores—.
- El resultado es un único texto listo para imprimir, guardar en archivo o enviar por correo; la construcción de archivos se estudia en el nivel intermedio.

Resultado esperado:

```text
Nota 1: 8.5
Nota 2: 9.0
Nota 3: 7.5
```

## 6. Aplicaciones en el mundo real

- **Validación de datos de usuario:** correos, teléfonos, documentos y contraseñas se comprueban con `startswith`, `endswith`, `isnumeric` y `len` antes de aceptarlos.
- **Limpieza de información:** las entradas llegan con espacios, mayúsculas inconsistentes y saltos de línea; el pipeline `strip` → `lower` → `split` → `join` del Ejemplo 7 es el primer paso de todo análisis de datos.
- **Parsing de archivos y protocolos:** separar campos de un CSV con `split`, leer encabezados con `partition`, extraer extensiones con `endswith` y partir rutas con `rsplit`.
- **Procesamiento de logs y textos:** contar ocurrencias de un error con `count`, localizar marcas de tiempo con `find` y filtrar líneas con `startswith`.
- **Generación de reportes:** construir mensajes, tablas y documentos de texto con f-strings y `join` (Ejemplo 8), tal como se hace en facturas y notificaciones.
- **Desarrollo web:** construir y leer direcciones URL y parámetros de consulta, normalizar encabezados HTTP y preparar contenido antes de mostrarlo en una interfaz.
- **Automatización de escritorio:** renombrar archivos por patrón, inventariar carpetas y rellenar plantillas con datos leídos.

## 7. Uso en producción

- **Normalizar antes de comparar:** toda comparación contra entrada de usuario pasa por `strip()` y, si el criterio lo permite, `lower()`. Comparar sin normalizar es el fallo silencioso más frecuente: el programa no lanza error, simplemente rechaza valores válidos (sección 8).
- **Confiar en el formato, no en la conversión aparente:** `isnumeric()` comprueba el texto; la conversión con `int()` o `float()` se hace **después** de validar, nunca antes. Para formatos complejos (máscaras, correos estrictos, fechas) la herramienta profesional son las expresiones regulares, que se estudian en el nivel avanzado.
- **Guardar siempre el resultado:** por inmutabilidad, ningún método de cadena modifica el original; descartar el valor devuelve el programa a su estado previo sin ningún aviso (sección 8).
- **Preferir f-strings a la concatenación:** son más legibles y menos propensas a olvidar un `str(...)`; la concatenación con `+` solo queda para unir dos fragmentos simples.
- **Unir con `join`, no con `+` en bucles:** acumular texto repitiendo `resultado += linea` degrada el rendimiento a medida que crece; construir una lista de líneas y unirla al final es la práctica estándar (Ejemplo 8).
- **Cuidar el texto que sale del sistema:** el contenido que llega de usuarios se muestra escapado en interfaces web (evitar que un texto contenga HTML o scripts que el navegador interprete) y nunca debe mezclarse sin escapar en consultas a bases de datos; esos temas se retoman en módulos y seguridad.
- **Unicode de verdad:** las cadenas de Python almacenan caracteres de todo el mundo (`"Ñ"`, `"é"`, `"日本"`); los métodos de mayúsculas funcionan sobre ellos, pero comparaciones sin distinguir acentos requieren normalización específica, no un simple `lower()`.
- **Preservar el original:** cuando el dato se limpia para comparar, conviene conservar la versión original para mostrarla al usuario; se normaliza para decidir, no para presentar.

## 8. Errores comunes y recomendaciones

1. **Descartar el resultado de un método.** Este programa no falla, pero no hace nada:

```python
texto = "hola"
texto.upper()
print(texto)
```

Resultado esperado:

```text
hola
```

Diagnóstico: `upper()` devolvió `"HOLA"` y nadie lo guardó. Como las cadenas son inmutables, la asignación original quedó intacta. Solución: `texto = texto.upper()` o `print(texto.upper())`.

2. **Indexar una posición que no existe.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: IndexError, la posición está fuera de la cadena
texto = "hola"
print(texto[10])
```

Salida real: `IndexError: string index out of range`. Diagnóstico: los índices válidos de `"hola"` van de 0 a 3 (`len - 1`). Solución: comprobar la longitud antes de acceder o usar una rebanada (`texto[10:11]`), que devuelve `""` en lugar de fallar.

3. **Leer mal los límites de una rebanada.** El comentario de `REPASO(01)_CLASSS_ONE.py` L3 afirma que `print(dato[0:2])` sobre `"Pepito es un pepe feliz"` imprime `"Pepit"`; el valor real es `Pe`:

```python
dato = "Pepito es un pepe feliz"
print(dato[0:2])
```

Resultado esperado:

```text
Pe
```

Diagnóstico: la rebanada incluye `inicio` y excluye `fin`, es decir, entrega `fin - inicio` caracteres. Con `0:2` son dos caracteres, no cinco. Solución: pensar la rebanada como "de la posición A a la posición B", nunca como "del 0 al 2 inclusive".

4. **`index` sin coincidencia detiene el programa.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: ValueError, index lanza excepción si no encuentra
cadena = "soy flavio"
print(cadena.index("python"))
```

Salida real: `ValueError: substring not found`. Diagnóstico: `index` no devuelve un código de error, lanza una excepción y nadie la está capturando. Solución: usar `find()` cuando la ausencia es un caso normal (`resultado = cadena.find("python")` da `-1` y el programa sigue), o manejar la excepción con `try`/`except` (ver [excepciones](../../Intermedio/chapter-four/excepciones.md)).

5. **`split(" ")` con espacios múltiples.** Este programa no falla, pero produce trozos vacíos:

```python
texto = "hola   mundo"
print(texto.split(" "))
print(texto.split())
```

Resultado esperado:

```text
['hola', '', '', 'mundo']
['hola', 'mundo']
```

Diagnóstico: cada espacio se interpreta como separador, y entre tres espacios seguidos quedan dos separadores consecutivos, lo que genera cadenas vacías entre palabras. Solución: para dividir por espacios usar `split()` sin argumento, que colapsa las rachas; `split(" ")` solo cuando los espacios son exactamente un separador.

6. **Comparar sin normalizar.** Este programa responde `False` aunque el usuario escribió lo correcto:

```python
respuesta = " Sí "
print(respuesta == "sí")
```

Resultado esperado:

```text
False
```

Diagnóstico: `" Sí "` tiene espacios y mayúscula inicial; `==` compara carácter por carácter, sin tolerancia alguna. Solución: `respuesta.strip().lower() == "sí"` (con cuidado de que la comparación también esté normalizada, como en el Ejemplo 7). Un caso hermano, unir texto y número con `+`, ya se trata en [entradas y salidas](../chapter-one/entradas_y_salidas.md).

7. **`join` sobre elementos que no son cadenas.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, join solo acepta cadenas
print(", ".join([1, 2, 3]))
```

Salida real: `TypeError: sequence item 0: expected str instance, int found`. Diagnóstico: `join` concatena **cadenas**; la lista contiene enteros. Solución: convertir antes, `", ".join(str(x) for x in [1, 2, 3])`, que es exactamente el recurso que usa el material (`CLASE_ONE.py` L619).

8. **Creer que `isnumeric` acepta cualquier cosa parecida a un número.** Este programa no falla y responde con precisión:

```python
print("1234".isnumeric())
print("12 34".isnumeric())
print("12a4".isnumeric())
```

Resultado esperado:

```text
True
False
False
```

Diagnóstico: los métodos `is*` exigen que **todos** los caracteres cumplan la condición; un espacio o una letra la rompen, sin importar que el resto sea numérico. Es el comportamiento correcto y es el que el material explica al validar documentos de identidad: si el formato admite separadores, se eliminan con `replace` o `strip` antes de validar.

9. **Escribir mal el nombre de un método al encadenar llamadas.** Bloque deliberadamente erróneo (tomado de `BUENAS_PRACTICAS.py` L43):

```python
    # ERROR INTENCIONAL: AttributeError, el método es title(), no tile()
color = "  azul marino  ".strip().tile()
```

Salida real: `AttributeError: 'str' object has no attribute 'tile'`. Diagnóstico: Python resuelve los nombres de método en tiempo de ejecución; una errata como `.tile()` en lugar de `.title()` pasa desapercibida hasta que el flujo ejecuta esa línea exacta. Solución: verificar el identificador (`"  azul marino  ".strip().title()`) y ejercitar todas las ramas de entrada durante las pruebas.

## 9. Resumen

- Una cadena es una secuencia indexada cuyos índices van de 0 a `len - 1`; los índices negativos cuentan desde el final.
- La rebanada `cadena[inicio:fin:paso]` incluye `inicio` y excluye `fin`; admite valores omitidos, negativos y paso, y siempre devuelve una cadena nueva.
- Las cadenas son **inmutables**: los métodos no modifican el original, devuelven una cadena nueva que debe guardarse o mostrarse.
- Función (`len(dato)`) y método (`dato.upper()`) difieren en la forma de llamarlos y en a quién pertenecen.
- Los métodos de transformación (`upper`, `lower`, `capitalize`, `title`, `strip`, `replace`) devuelven texto; los de búsqueda (`find`, `index`, `count`) devuelven posiciones o cantidades; los `is*` devuelven booleanos.
- `find` devuelve -1 ante la ausencia; `index` lanza `ValueError`. Elegir según si la ausencia es normal.
- `split` convierte una cadena en una lista y `join` hace el camino inverso; `split()` sin argumento divide por rachas de espacios.
- Las f-strings permiten incrustar valores directamente con `{}` (mientras `str.format()` rellena plantillas reutilizables); las secuencias de escape (`\n`, `\t`, `\\`) dan formato al texto.
- Antes de comparar entrada de usuario se normaliza con `strip()` y `lower()`; para unir mucho texto se usa `join`, no `+` en bucle.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L360-707) | `CLASE_ONE.py` | Los 23 métodos de cadena del curso (`upper`, `lower`, `capitalize`, `find`, `index`, `isnumeric`, `isalpha`, `count`, `startswith`, `endswith`, `replace`, `split`, `title`, `strip`, `isalnum`, `islower`, `isspace`, `isupper`, `join`, `swapcase`, `isdigit`...), comparación lexicográfica de cadenas | Se ordenaron en las dos tablas de la sección 4, se explicó qué devuelve cada uno, se contrastaron `find`/`index` y se añadió la inmutabilidad como explicación del porqué. Nota: el archivo se detiene con error en la L134 (asignación a una tupla); esas líneas no se replican |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L969-991) | `CLASE_ONE.py` | `input` junto a f-strings y concatenación con `str(...)` | El uso básico se presenta en la sección 3 con enlace a [entradas y salidas](../chapter-one/entradas_y_salidas.md); el formato avanzado queda para [funciones](../../Intermedio/chapter-two/funciones.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(01)_CLASSS_ONE.py` (L1-9, L199-333, L315) | `REPASO(01)_CLASSS_ONE.py` | Rebanada `[0:2]`, `len`, rebanada con longitud dinámica `[0:escoger]`, recorrido de 13 métodos, `split` que genera una lista | La rebanada es el Ejemplo 1 (con corrección del comentario de la L3 en la sección 8); el `split`→lista es el Ejemplo 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L159-261) | `REPASO(02)_CLASS_ONE.py` | Recorrido guiado de métodos de cadena sobre texto ingresado | Se integró en las tablas de la sección 4 y en los Ejemplos 3 y 5 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/MÉTODOS Y FUNCIONES/Funciones_Metodos_ejm.py` (L1-14, L48-55) | `Funciones_Metodos_ejm.py` | Distinción función/método, `dir`, `len`, `split`, `replace`, validación con `isnumeric`/`isalpha` | La distinción es el quinto concepto de la sección 3; los métodos aparecen en las tablas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_String.py` (L1-14) | `Ejm_String.py` | `dato[0:2]`, `len` y rebanada con límite elegido por el usuario | Es el Ejemplo 1, con la explicación de los límites corregida |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L56-69) | `Keyword_del.py` | Uso de `del` sobre rebanadas de una lista | Se cita como contraste conceptual: `del` no puede borrar caracteres de una cadena (son inmutables) y su uso sobre listas se documenta en [listas](listas.md) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO_Capicua.py` (L29-40) | `EJERCICIO_Capicua.py` | `str`→`list`, `.copy()`, `.reverse()` e igualdad de listas aplicadas a una cadena | Es el Ejemplo 6, reescrito sin funciones para el nivel básico-intermedio |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L7, L31, L43, L149) | `BUENAS_PRACTICAS.py` | Normalización encadenada `.strip().title()` y `.strip().capitalize()`; errata `.strip().tile()` en la L43 (corregida en la L149) | Refuerza el encadenamiento de métodos del Ejemplo 3 y sustenta el caso 9 de la sección 8 sobre `AttributeError` en tiempo de ejecución |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L177) | `Decoradores_Multiples.py` | `"\n".join(f"{key}: {value}" for key, value in dicci.items())` dentro de `__str__` | Conecta la construcción de reportes del Ejemplo 8 con el uso de `join` sobre expresiones generadoras y f-strings |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L12, L167, L189, L270) | `Juego.py` | `" \|\| ".join(f"{key}: {value}" for key, value in dicci.items())` y normalización `.strip().lower()` / `.strip().title()` en menús | Ejemplifica la unión de pares clave-valor con separador personalizado y la normalización sistemática de entradas antes de comparar |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` (L9, L38) | `Con_TextBlob.py` | `"\x1b[1;{}m{}\x1b[0;37m".format(self.color, self.nombre)` y secuencias de escape ANSI | Sustenta la presentación de `str.format()` y su contraste frente a las f-strings en las secciones 3 y 4 |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Ejercicio-Final_Optimizado.py` (L21, L48) | `Ejercicio-Final_Optimizado.py` | Plantilla con marcadores posicionales `{}` mediante `str.format()` en `__str__` | Complementa la trazabilidad de `str.format()` en objetos personalizados (sin reproducir credenciales externas presentes en el script original) |

**Fundamento complementario:** (1) los métodos `lstrip`, `rstrip`, `rsplit` y `partition` **no aparecen** en el material original (verificado por búsqueda en ambos directorios del curso); se añaden a la tabla de la sección 4 como contrapartes oficiales de `strip` y `split`, documentadas con sus valores de retorno. (2) Las cadenas crudas (`r"..."`) tampoco se enseñan en las clases; se presentan en la sección 3 como apoyo para escribir rutas sin escapar la barra invertida.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/introduction.html#text> — tutorial oficial: cadenas de texto, secuencias de escape, indexado y rebanado.
- <https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str> — referencia oficial del tipo de texto `str`: métodos completos y semántica de inmutabilidad.
- <https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting> — tutorial oficial sobre formateo de cadenas con f-strings y `str.format()`.
