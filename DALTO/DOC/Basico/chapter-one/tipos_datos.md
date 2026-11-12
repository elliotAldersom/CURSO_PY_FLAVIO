# Tipos de datos en Python

## 2. Introducción

En la vida real un texto y un número no se manejan igual: no se suman palabras con la misma regla que las cifras. En programación esa distinción existe como **tipo de dato**: la clasificación que indica qué clase de valor es y qué operaciones admite.

Python asigna un tipo a cada valor: `42` es un entero (`int`), `3.5` es un decimal (`float`), `"hola"` es una cadena de texto (`str`), `True` y `False` son booleanos (`bool`) y `None` representa la ausencia de valor. Estos son los tipos **simples**, los que se usan solos; más adelante están los tipos **compuestos** (listas, tuplas, conjuntos y diccionarios), que agrupan otros valores dentro.

Python es un lenguaje de **tipado dinámico**: no hay que declarar el tipo de una variable; el tipo viaja con el valor y se puede consultar en cualquier momento con la función `type(...)`. Por eso el mismo nombre puede contener un número hoy y un texto mañana (ver [variables](variables.md)).

Este tema resuelve tres preguntas: ¿qué valores puedo usar?, ¿cómo transformo uno en otro? y ¿cómo averiguo el tipo de algo que tengo delante? Es el puente entre las entradas y salidas (que devuelven texto) y los [operadores](operadores.md), que necesitan tipos compatibles para calcular.

## 3. Fundamentos y conceptos

**Enteros `int`.** Números sin parte decimal: `-3`, `0`, `42`. En Python los enteros tienen precisión ilimitada: `10 ** 30` sigue siendo un entero exacto, no un valor aproximado. Esto distingue a Python de lenguajes donde el entero desborda a un valor máximo.

**Decimales `float`.** Números con parte fraccionaria en notación decimal escrita: `3.5`, `-0.01`, `2e3` (que vale `2000.0`). Internamente se almacenan como **punto flotante binario** de doble precisión: una aproximación binaria del número decimal. La consecuencia práctica es que algunas sumas no son exactas: `0.1 + 0.2` resulta `0.30000000000000004`. No es un error de Python, sino la representación binaria de esas fracciones; el tema completo del dinero con precisión exacta se estudia con el módulo `decimal` en el nivel intermedio.

**Cadenas `str`.** Secuencias de caracteres entre comillas: `"hola"`, `'42'`, `"""texto largo"""`. Una cadena **no es un número** aunque esté formada por dígitos: `str` y `int` son tipos distintos y `input` siempre devuelve `str`. Las cadenas son **inmutables**: sus métodos devuelven una cadena nueva sin modificar la original; el tratamiento completo está en [cadenas](../chapter-two/cadenas.md).

**Booleanos `bool`.** Solo dos valores: `True` y `False` (con mayúscula inicial). El material original los resume como `True: 1` y `False: 0`; la precisión correcta es que `bool` es una **subclase** de `int` (`True` se comporta como `1` y `False` como `0` en aritmética), pero son un tipo propio con identidad propia: `type(True)` devuelve `bool`, no `int`. Los booleanos son el resultado de las comparaciones y la materia prima de las [condicionales](condicionales.md).

**`NoneType`.** `None` es el único valor del tipo `NoneType` y significa "no hay valor": el resultado de una función que no devuelve nada, o un dato ausente. No es cero ni texto vacío: es la ausencia explícita.

**Funciones introspectivas y de verificación.** `type(valor)` devuelve el tipo exacto del valor (`type(True)` es `bool`); `isinstance(valor, tipo)` comprueba si el valor es instancia de ese tipo o de una subclase suya (`isinstance(42, int)` y `isinstance(True, int)` devuelven `True`, y admite una tupla de tipos como `isinstance(x, (int, float))`); `dir(valor)` devuelve la lista de nombres (atributos y métodos) disponibles sobre ese valor. Las tres son **funciones integradas** (`type(dato)`, `isinstance(dato, int)`), no métodos (`dato.type()` no existe).

**Conversión explícita (*casting*) y coerción implícita.** Las funciones `int(...)`, `float(...)`, `str(...)` y `bool(...)` transforman explícitamente un valor a otro tipo. Entre tipos numéricos compatibles Python aplica **coerción implícita** en operaciones aritméticas (`3 + 4.4` convierte el entero a decimal y produce `7.4`, de tipo `float`), pero **nunca** convierte implícitamente entre cadenas y números (`"3" + 4` lanza `TypeError`). Reglas esenciales de conversión explícita:

- `int("42")` → `42`; `int("42.9")` **falla** (`ValueError`), porque el texto tiene forma decimal: conviene `float("42.9")` primero.
- `int(3.9)` → `3`: la conversión desde decimal **trunca** hacia cero, no redondea. Para redondear existe `round(...)`.
- `float("3.5")` → `3.5`; `float("3,5")` falla: el separador decimal canónico es el punto.
- `str(42)` → `"42"`; `bool("")` → `False` y `bool("texto")` → `True` (una cadena vacía es falsa).

**Tipos compuestos (visión general).** El material original los presenta juntos porque comparten la idea de "agrupar valores": **lista** (`[...]`, ordenada y modificable), **tupla** (`(...)`, ordenada e inmutable), **conjunto** (`{...}`, sin orden ni repetidos) y **diccionario** (`{clave: valor}`, asociación con claves). Aquí solo se anticipan; cada uno tiene su documento: [listas](../chapter-two/listas.md), [tuplas](../../Intermedio/chapter-one/tuplas.md), [conjuntos](../../Intermedio/chapter-one/conjuntos.md) y [diccionarios](../../Intermedio/chapter-one/diccionarios.md).

**Lenguaje, funciones integradas, biblioteca estándar y librerías externas.** Los tipos `int`, `float`, `str`, `bool` y `NoneType` forman parte del **modelo de datos del lenguaje Python**; funciones y constructores como `type()`, `isinstance()`, `dir()`, `int()`, `float()`, `str()` y `bool()` pertenecen al espacio de nombres integrado (**`builtins`**, disponible directamente sin `import`); módulos como [`decimal`](../../Intermedio/chapter-four/decimal.md) pertenecen a la **biblioteca estándar** de Python (se distribuyen con el intérprete y se cargan con `import decimal`); y paquetes como `pandas` o `textblob` son **librerías externas** de terceros que requieren instalación separada. Esta distinción se mantiene en todo el curso.

## 4. Sintaxis y funcionamiento

Sintaxis para consultar y comprobar tipos:

```text
type(valor)  isinstance(valor, tipo)
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `int` | Entero sin decimales, precisión ilimitada | `type(42)` → `<class 'int'>` |
| 2 | `float` | Decimal en representación de doble precisión | `type(3.5)` → `<class 'float'>` |
| 3 | `str` | Cadena de caracteres, inmutable | `type("hola")` → `<class 'str'>` |
| 4 | `bool` | Booleano: `True` o `False` (subclase de `int`) | `type(True)` → `<class 'bool'>` |
| 5 | `NoneType` | Ausencia de valor, único valor `None` | `type(None)` → `<class 'NoneType'>` |
| 6 | `isinstance(v, T)` | Devuelve `True` si `v` es de tipo `T` o subclase suya | `isinstance(42, (int, float))` → `True` |

Sintaxis de las conversiones:

```text
int(valor)  float(valor)  str(valor)  bool(valor)
```

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `int(x)` | Entero desde texto numérico entero o decimal truncado | `int("42")` → `42`; `int(3.9)` → `3` |
| 2 | `float(x)` | Decimal desde texto o entero | `float("3.5")` → `3.5`; `float(2)` → `2.0` |
| 3 | `str(x)` | Texto desde cualquier valor | `str(42)` → `"42"` |
| 4 | `bool(x)` | Falsedad: `0`, `""`, `None`, `[]`, `False`; el resto, `True` | `bool("")` → `False` |

Funcionamiento: `type` y `str`/`int`/`float`/`bool` son **funciones**; se escriben con el valor entre paréntesis y devuelven un resultado que puede guardarse en una variable (`mi_tipo = type(valor)`). La conversión **nunca** modifica el valor original: crea uno nuevo del tipo pedido. Si la forma del valor no admite la conversión (`int("abc")`), Python lanza una excepción y detiene la instrucción; el manejo de eso se estudia en [excepciones](../../Intermedio/chapter-four/excepciones.md).

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Descubrir el tipo de cada literal.**

```python
print(type(42))
print(type(3.5))
print(type("hola"))
print(type(True))
print(type(None))
```

Explicación línea por línea:

- Cada línea pasa un literal a `type`, que devuelve el objeto tipo del valor; `print` lo muestra con la notación `<class '...'>`.
- `42` sin punto es entero; `3.5` con punto es decimal; `"hola"` entre comillas es cadena; `True` es booleano; `None` es el valor de ausencia.

Resultado esperado:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

**Ejemplo 2 — Conversiones básicas entre tipos.**

```python
entero = int("42")
decimal = float("3.5")
texto = str(42)
print(entero + 1)
print(decimal * 2)
print(texto + "!")
```

Explicación línea por línea:

- Línea 1: el texto `"42"` se convierte al entero `42`; sin la conversión, `entero + 1` sería un error de tipos.
- Línea 2: `"3.5"` se convierte al decimal `3.5`.
- Línea 3: el número `42` se convierte al texto `"42"` para poder concatenarlo.
- Línea 4: `42 + 1` → `43`, aritmética de enteros.
- Línea 5: `3.5 * 2` → `7.0`; multiplicar un decimal devuelve decimal.
- Línea 6: `"42" + "!"` → `42!`, concatenación de cadenas.

Resultado esperado:

```text
43
7.0
42!
```

**Ejemplo 3 — Booleanos y valores falsos.**

```python
print(True, False)
print(bool(""), bool("hola"))
print(bool(0), bool(7))
print(True + True, True * 10)
```

Explicación línea por línea:

- Línea 1: los dos únicos valores de `bool` con su notación oficial (mayúscula inicial).
- Línea 2: la cadena vacía es falsa; cualquier texto no vacío es verdadero.
- Línea 3: el entero `0` es falso; cualquier otro número es verdadero.
- Línea 4: confirma que `bool` hereda de `int`: `True` participa en aritmética como `1`, de modo que `True + True` = `2` y `True * 10` = `10`.

Resultado esperado:

```text
True False
False True
False True
2 10
```

### Intermedio

**Ejemplo 4 — Leer números, convertir y redondear un pago.**

```python
monto = float(input("Ingresa el monto: "))
letras = int(input("Ingresa el número de cuotas: "))
total = monto * 1.19
pago = round(total / letras)
print("Pago por cuota:", pago)
```

Explicación de las decisiones tomadas:

- El monto se convierte a `float` porque admite decimales; las cuotas a `int` porque no puede haber media cuota.
- `1.19` representa el incremento del 19 % (`1 + 0.19`); escribir la fórmula completa deja el porcentaje visible sin variables auxiliares.
- `round(...)` se aplica **al final**, sobre el resultado ya dividido: redondear antes produciría un error acumulado.
- El tipo coherente de principio a fin (`float` → `float` → `int` para mostrar) evita sorpresas de formato.

Con `1000` y `4`, resultado esperado:

```text
Ingresa el monto: Ingresa el número de cuotas: Pago por cuota: 298
```

**Ejemplo 5 — Truncar, redondear y comparar conversiones.**

```python
print(int(3.9), int(-3.9))
print(round(2.5), round(3.5))
print(int("42") == 42, float("42") == 42.0)
print(type(42) == type(42.0))
```

Explicación de las decisiones tomadas:

- `int(...)` **trunca** hacia cero (`3.9` → `3`, `-3.9` → `-3`): elimina la parte decimal, no aproxima.
- `round(...)` **redondea** al entero más cercano; con empate exacto (`2.5`, `3.5`) Python usa el entero par más cercano, por eso el resultado es `2` y `4`. Es el comportamiento documentado de `round` con un solo argumento.
- Las comparaciones confirman que el valor convertido es igual al literal del tipo destino: `"42"` convertido es `42`, aunque su tipo original fuera `str`.
- La última línea muestra que entero y decimal son tipos distintos aunque el valor "se parezca": `42 != 42.0` en identidad de tipo, y esa distinción importa al comparar.

Resultado esperado:

```text
3 -3
2 4
True True
False
```

### Avanzado

**Ejemplo 6 — Precisión de los decimales y cómo mostrarlos.**

```python
precio_a = 0.1
precio_b = 0.2
suma = precio_a + precio_b
print(suma)
print(suma == 0.3)
print(round(suma, 2))
print(f"Total: {suma:.2f}")
```

Explicación de las decisiones tomadas:

- `0.1` y `0.2` no tienen representación exacta en binario de doble precisión; su suma acumula el desfase y el resultado real es `0.30000000000000004`.
- Por eso `suma == 0.3` devuelve `False`: comparar decimales con igualdad exacta es un error de diseño, no un fallo del programa. Este conocimiento es requisito para el uso de comparaciones en [operadores](operadores.md).
- `round(suma, 2)` y el especificador `:.2f` corrigen **solo la presentación**; el valor interno sigue siendo impreciso. Decisión de mantenibilidad: documentar que la salida está formateada evita que otro desarrollador confunda el texto mostrado con el dato almacenado.
- Para dinero se exige aritmética exacta: en el nivel intermedio se usa el módulo `decimal` (tipado fijo) o enteros de centavos. Mientras tanto, la regla práctica es: no comparar `float` con `==` y no acumular importes en `float` si la exactitud es crítica.
- Coste/beneficio: el punto flotante es el tipo más rápido para cálculo científico masivo; su limitación es de exactitud, no de rendimiento. Elegir `float`, `decimal` o `int` según el dominio es una decisión de arquitectura de datos.

Resultado esperado:

```text
0.30000000000000004
False
0.3
Total: 0.30
```

## 6. Aplicaciones en el mundo real

- **Validación de datos de entrada:** los formularios y scripts reciben todo como texto; convertir y comprobar tipos es la primera línea de defensa de cualquier programa.
- **Análisis de datos:** las bibliotecas de ciencia de datos trabajan sobre arrays de `float` y `int`; entender la precisión del decimal explica por qué pandas muestra redondeos.
- **Informes financieros:** mostrar importes con dos decimales (`:.2f`) mientras el cálculo interno se hace en enteros de centavos o con `decimal` es el patrón dominante en pagos y facturación.
- **Procesamiento de archivos y CSV:** todo llega como cadena; el primer paso de cualquier importación es reconocer y convertir tipos.
- **Lógica de negocio:** estados (`True`/`False`), flags de configuración y presencia de valores (`None`) modelan decisiones diarias de los sistemas.
- **Interfaces de escritorio:** las cajas de texto entregan cadenas; la capa de presentación convierte antes de pasar datos a la lógica.

## 7. Uso en producción

- **Convertir en la frontera, no en medio del cálculo:** los datos se validan y convierten una sola vez al entrar al sistema; después, el núcleo del programa trabaja con tipos coherentes.
- **Validar antes de convertir:** verificar que el texto tenga forma numérica (o capturar la excepción) produce mejores mensajes que un `ValueError` crudo. El patrón `try/except` se presentó en [entradas y salidas](entradas_y_salidas.md) y se domina en [excepciones](../../Intermedio/chapter-four/excepciones.md).
- **`type()` para inspeccionar, `isinstance()` para validar tipos:** comparar con `type(v) == int` es frágil ante herencia; la forma idiomática en producción es `isinstance(v, int)` (o `isinstance(v, (int, float))`), que el propio material del curso emplea en sus módulos de programación orientada a objetos y procesamiento de datos para comprobar tipos respetando la jerarquía de clases.
- **Dinero sin `float`:** importes exactos con [`decimal`](../../Intermedio/chapter-four/decimal.md) (de la biblioteca estándar) o enteros de centavos; el `float` solo para magnitudes científicas donde la tolerancia es aceptable.
- **Formato en la capa de presentación:** el cálculo no debe depender de cómo se muestra; redondear para imprimir no altera el valor con el que se compara.
- **Documentar los tipos esperados:** nombres como `total_euros` y pruebas que fijan el tipo esperado evitan la deriva silenciosa `int → float → str` en código heredado.
- **Rendimiento:** para volúmenes grandes, el tipo define el consumo de memoria (cadenas y listas de objetos pesan más que arreglos de la librería numérica); ese tema se aborda en el nivel intermedio con Pandas.

## 8. Errores comunes y recomendaciones

1. **Unir texto y número con `+`.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, str e int no se pueden sumar
edad_texto = "18"
print("Edad: " + edad_texto + 1)
```

Salida real: `TypeError: can only concatenate str (not "int") to str`. Solución: convertir (`int(edad_texto)`) o usar una f-string (`f"Edad: {edad_texto}"`).

2. **Convertir texto con coma decimal.** Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: ValueError, el separador decimal esperado es el punto
importe = float("3,5")
print(importe)
```

Salida real: `ValueError: could not convert string to float: '3,5'`. El material original lo evita normalizando con `replace(",", ".")` antes de convertir (ver `Ejm_Operadores_Aritméticos.py` L6); en producción conviene rechazar el formato inválido o normalizar de forma explícita y documentada.

3. **Comparar texto convertido con el número original.** Este fallo **no avisa**: el programa corre y da una respuesta equivocada.

```python
edad_leida = "18"
print(edad_leida == 18)
```

Resultado esperado:

```text
False
```

Diagnóstico: `input` devuelve `str`; `"18"` nunca es igual al entero `18`. Solución: convertir al leer (`edad = int(input(...))`) o comparar contra `str(...)`, eligiendo una sola estrategia en todo el programa.

4. **Esperar que `int(...)` redondee.** `int(3.9)` da `3` (trunca hacia cero); para aproximar se usa `round(3.9)`. Y `int("3.9")` **falla** con `ValueError: invalid literal for int() with base 10: '3.9'`: el texto debe tener forma de entero. No confundir truncado, redondeo y fallo de conversión.

5. **Modificar un tipo inmutable.** El material original contiene una línea activa que revienta: `tupla[3] = "hola"` en `CLASE_ONE.py` L134. Bloque deliberadamente erróneo:

```python
    # ERROR INTENCIONAL: TypeError, las tuplas no admiten asignación por índice
tupla = ("uno", "dos")
tupla[1] = "2"
print(tupla)
```

Salida real: `TypeError: 'tuple' object does not support item assignment`. Enseña el comportamiento correcto: las tuplas son inmutables; para cambiar elementos se usa una [lista](../chapter-two/listas.md). Nunca repliques la línea del material original.

6. **Creer que `True` es "solo un 1".** Aunque aritméticamente vale `1`, `type(True)` es `bool`; tratarlo como entero en interfaces públicas confunde a quien lee el código. Usa booleanos para lógica, enteros para cantidades.

7. **Olvidar que `None` no es cero ni cadena vacía.** `None == 0` y `None == ""` son `False`; el chequeo correcto de ausencia es `valor is None` (la identidad se explica en [operadores](operadores.md)).

## 9. Resumen

- El tipo de dato clasifica un valor y define las operaciones que admite; Python lo asigna dinámicamente, se inspecciona con `type(...)` y se valida de forma idiomática con `isinstance(...)`.
- Los tipos simples del curso: `int` (precisión ilimitada), `float` (doble precisión binaria, con sus límites de exactitud), `str` (inmutable), `bool` (`True`/`False`, subclase de `int`) y `NoneType`.
- Las conversiones explícitas `int`/`float`/`str`/`bool` pertenecen a `builtins` y crean valores nuevos (`int` trunca desde decimal y falla con texto no entero; `round` redondea); entre números opera coerción implícita (`int + float` → `float`), pero nunca entre `str` y números.
- `decimal` pertenece a la biblioteca estándar de Python y `pandas` es una librería externa.
- Una cadena numérica no es un número: `input` devuelve `str` y la conversión debe ser explícita.
- `0.1 + 0.2 != 0.3`: el `float` aproxima; el formato de salida (`:.2f`, `round`) arregla la vista, no el valor.
- Los tipos compuestos (lista, tupla, conjunto, diccionario) agrupan valores y se documentan en sus capítulos: [listas](../chapter-two/listas.md), [tuplas](../../Intermedio/chapter-one/tuplas.md), [conjuntos](../../Intermedio/chapter-one/conjuntos.md), [diccionarios](../../Intermedio/chapter-one/diccionarios.md).

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L9-10, L28-44, L199-200) | `CLASE_ONE.py` | `None`, cadenas simples, `int`, `float`, `bool` (`True:1`/`False:0`), función `type` | Se precisó que `bool` es subclase de `int` y no "lo mismo" que `1`/`0`, y se documentó `NoneType` con su significado de ausencia |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L134) | `CLASE_ONE.py` | Intento de asignación a un elemento de tupla (línea que detiene el archivo con `TypeError`) | Se documentó como error deliberado con el mensaje real, para enseñar la inmutabilidad correcta de las tuplas en lugar de replicar la caída |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(01)_CLASSS_ONE.py` (L56-100, L186-195) | `REPASO(01)_CLASSS_ONE.py` | `type()` sobre lista/tupla/set/dict, `dir()`, visión de datos compuestos | Se conservó `type`/`dir` como funciones integradas de `builtins` y se separó la visión de tipos compuestos hacia sus documentos correspondientes |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Datos_Compuestos.py` (L8-37) | `Ejm_Datos_Compuestos.py` | Comparación lista vs tupla vs conjunto vs diccionario, mutabilidad por índice | Se redujo a la visión general con enlaces; la cobertura profunda queda para los capítulos de cada estructura |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/ejemplo1.py` (L1-4, L17) | `ejemplo1.py` | `int`/`float` con `input`, redondeo con `round` | Se desarrolló la distinción truncar vs redondear (Ejemplo 5) y el redondeo al final del cálculo (Ejemplo 4) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Metodos.py` (L21, L55) | `Metodos.py` | Observación comentada sobre `isinstance(name, int)` / `isinstance(name, float)` frente a entradas de `input()` que siempre devuelven `str` | Se integró con la conversión en la frontera: `isinstance()` comprueba el tipo del objeto, no el formato numérico de un texto sin convertir |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/Herencia_Multiple.py` (L64-72) | `Herencia_Multiple.py` | Uso de `isinstance(objeto, Clase)` y explicación sobre verificación de tipos (`str`, `int`, clases propias) respetando la herencia | Se incorporó en las secciones 3, 4 y 7 para contrastar `type()` con `isinstance()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L37-42) | `Decorador_Property.py` | Validación de tipos en un setter mediante `isinstance(new_Data, tuple)`, `isinstance(name, str)` e `isinstance(edad, int)` | Refuerza el uso productivo de `isinstance()` para proteger invariantes de tipos antes de asignar datos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/One.py` (L50-58) | `One.py` | Promedio aritmético con `/` (`float`) seguido de `round(...)` para obtener enteros en atributos calculados | Conecta la conversión y redondeo final con atributos de objetos en ejercicios prácticos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Polimorfismo.py` (L87-100) | `Polimorfismo.py` | Coerción numérica implícita en `3 + 4.4` → `7.4` verificada con `type(...)` | Se documentó en la sección 3 la diferencia entre coerción implícita numérica (`int` a `float`) y ausencia de coerción automática con `str` |

**Fundamento complementario incorporado:** la especificación de formato dentro de las f-strings (`:.2f`, `:.1f`) no aparece en el material original; se usa aquí y en [entradas y salidas](entradas_y_salidas.md) como base del formato de números, con referencia oficial en la sección 11.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/stdtypes.html> — referencia oficial de los tipos integrados: enteros, decimales, cadenas, booleanos y sus operaciones.
- <https://docs.python.org/3/library/functions.html#isinstance> — documentación oficial de las funciones integradas `isinstance` y `type` en el espacio `builtins`.
- <https://docs.python.org/3/tutorial/introduction.html> — tutorial oficial de introducción: literales numéricos, cadenas y operaciones elementales.
- <https://docs.python.org/3/tutorial/floatingpoint.html> — anexo oficial del tutorial sobre aritmética de punto flotante: causas y límites de precisión binaria.
