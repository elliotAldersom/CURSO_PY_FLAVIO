# Definición, Parámetros y Retorno de Funciones en Python

## 2. Introducción

A medida que un programa supera unas pocas decenas de líneas, repetir las mismas instrucciones de cálculo, formateo o validación en distintos lugares introduce tres problemas estructurales: duplicación de lógica difícil de mantener, mayor probabilidad de inconsistencias al corregir un criterio y dificultad para verificar cada operación de manera aislada.

Una **función** es una unidad de código con nombre e interfaz explícita que encapsula una tarea bien definida, recibe datos de entrada opcionales a través de **parámetros**, ejecuta una secuencia de instrucciones en su propio [ámbito de variables](ambito_variables.md) y entrega un resultado mediante la sentencia `return`.

En el diseño de software con Python, dominar el modelo de funciones resuelve cuatro necesidades esenciales:

1. **Abstracción y descomposición modular:** divide un problema complejo en subproblemas pequeños y comprensibles, como separar la verificación de primalidad `es_primo(n)` de la generación de una serie completa en `EJERCICIO(2).py` (L11-39).
2. **Desacoplamiento entre cálculo e interfaz:** permite escribir lógica pura que transforma datos sin depender de `input()` ni `print()`, principio central demostrado al refactorizar clases y funciones en `BUENAS_PRACTICAS.py` (L86-199).
3. **Firmas expresivas y flexibles:** combina argumentos posicionales, argumentos por palabra clave, valores por defecto, captura variádica (`*args`, `**kwargs`) y restricciones de posición o nombre (`/` y `*`).
4. **Composición de orden superior:** dado que en Python las funciones son objetos de primera clase, pueden almacenarse en colecciones, pasarse como argumentos a otras funciones y devolverse dinámicamente, sustentando tanto las [funciones lambda](funciones_lambda.md) como los [decoradores](../../Avanzado/chapter-one/decoradores.md).

## 3. Fundamentos y conceptos

**Sentencia `def` y creación del objeto función.** En Python, `def` no es una mera declaración para un compilador previo, sino una **sentencia ejecutable**: al alcanzarse durante la ejecución del módulo, construye en memoria un objeto de tipo `function` y lo enlaza al identificador indicado en el espacio de nombres actual. Distinguir entre la referencia a la función (`saludar`, que evalúa al objeto función) y su invocación (`saludar()`, que ejecuta su cuerpo mediante el operador de llamada `()`) resulta fundamental para trabajar con funciones de primera clase.

**Función libre frente a método.** Tal como contrasta inicialmente `Funciones_Metodos_ejm.py` (L1-15), una **función independiente** se invoca pasando el objeto como argumento explícito (`len(texto)`, `dir(texto)`), mientras que un **método** es una función definida dentro de una [clase](../chapter-five/clases_y_objetos.md) y enlazada a una instancia u objeto receptor mediante notación de punto (`texto.upper()`, estudiado en detalle en [atributos y métodos](../chapter-five/atributos_y_metodos.md)).

**Parámetros frente a argumentos y modelo de paso de objetos.** Aunque en conversaciones informales suelen usarse como sinónimos, ambos términos describen momentos distintos:

- **Parámetro:** variable local declarada en la firma de `def` que actúa como nombre receptor (`def saludar(nombre, sexo):` en `CREAR_FUNCIONES.py` L37).
- **Argumento:** valor u objeto concreto entregado en el punto de llamada (`saludar("Elena", "mujer")`).

Python utiliza el modelo de **paso de referencias a objetos por valor** (*call by sharing* o *pass-by-object-reference*): el parámetro local recibe una referencia al mismo objeto que el argumento, sin copiarlo en memoria. Si dentro de la función se **reasigna** el parámetro (`nombre = nombre.strip()`), solo cambia a qué objeto apunta la variable local; en cambio, si el objeto recibido es mutable (como una `list` o un `dict`) y se **muta en sitio** (`lista.append(...)`), el cambio es visible fuera de la función.

**Modalidades de paso de argumentos y orden en la firma.** Al invocar una función, los argumentos pueden entregarse por **posición** (de izquierda a derecha) o por **palabra clave** (*keyword arguments*, `apellido="Silva", nombre="Flavio"`, `CREAR_FUNCIONES.py` L225), siempre que ningún argumento posicional aparezca después de uno por nombre (`DEF_CLASS_TWO.py` L126). En la definición de la función, Python soporta cinco categorías de parámetros con un orden sintáctico estricto:

1. **Solo posicionales (`/` — PEP 570, Python 3.8+):** los parámetros situados a la izquierda de `/` únicamente aceptan argumentos por posición; el llamador no puede nombrarlos como *keyword*. Es útil cuando el nombre interno del parámetro carece de valor semántico externo o puede cambiar en futuras versiones sin romper compatibilidad.
2. **Posicionales o por palabra clave (estándar):** pueden pasarse tanto por posición como por nombre, y admiten valores por defecto (`adjetivo="programador"`).
3. **Variádico posicional (`*args`):** precedido por un asterisco (`*numeros` en `CREAR_FUNCIONES.py` L133 o `*names` en `Funciones_Repaso.py` L63), agrupa en una **[tupla](../chapter-one/tuplas.md) inmutable** todos los argumentos posicionales sobrantes. Conviene precisar un matiz respecto al comentario de `CREAR_FUNCIONES.py` (L130-131): en Python 3 **sí** pueden declararse parámetros después de `*args`, pero todos ellos pasan automáticamente a ser *solo por palabra clave*.
4. **Solo por palabra clave (`*` — PEP 3102):** cualquier parámetro situado después de `*args` o de un asterisco desnudo `*` exige que el llamador especifique explícitamente su nombre (` clave=valor`), evitando llamadas ambiguas con múltiples banderas booleanas o numéricas.
5. **Variádico por palabra clave (`**kwargs`):** precedido por doble asterisco (`**names` en `Funciones_Repaso.py` L79), captura en un **[diccionario](../chapter-one/diccionarios.md)** todos los argumentos con nombre no asociados a parámetros explícitos.

**La trampa de los valores por defecto mutables.** En Python, las expresiones de valores por defecto (`def f(x, lista=[]):`) se evalúan **una sola vez cuando se ejecuta la sentencia `def`**, nunca de nuevo en cada llamada. El objeto resultante queda guardado en el atributo `f.__defaults__`. Si ese objeto por defecto es mutable (una lista, un diccionario o un conjunto) y la función lo modifica, todas las llamadas posteriores que omitan ese argumento compartirán y acumularán el mismo contenedor. El patrón estándar consiste en usar `None` como centinela inmutable (`def f(x, lista=None):`) y crear la lista nueva dentro del cuerpo (`if lista is None: lista = []`).

**Sentencia `return` frente a `print()`, retorno `None` y tuplas de retorno.** `print()` escribe texto en la salida estándar como efecto secundario para lectura humana (`entradas y salidas` en [entradas y salidas](../../Basico/chapter-one/entradas_y_salidas.md)), pero no entrega ningún dato aprovechable al código llamador. Por el contrario, `return` finaliza de inmediato la ejecución de la función —haciendo inalcanzable cualquier instrucción escrita debajo dentro del mismo bloque, como advierte `DEF_CLASS_TWO.py` (L96-100)— y devuelve el objeto resultante al punto de llamada. Si una función termina sin ejecutar `return` (o ejecuta `return` sin expresión), Python devuelve implícitamente el objeto único `None` (`DEF_CLASS_TWO.py` L16-26). Cuando se escriben varias expresiones separadas por comas (`return suma, resta, multiplicacion, division` en `Funciones_Repaso.py` L53), Python construye y retorna una **única `tuple`**, lista para extraerse mediante [desempaquetamiento](../chapter-one/desempaquetamiento.md).

**Corrección de validación en `CREAR_FUNCIONES.py` (L84).** En la función `crear_contraseña_random(num)` del material original (`CREAR_FUNCIONES.py` L78-90) se escribió `while(chars <= len(chars)):`, donde `chars` es `str` y `len(chars)` es `int`. En Python 3 los operadores de orden `<=` no están definidos entre `str` e `int`, por lo que esa línea lanza `TypeError: '<=' not supported between instances of 'str' and 'int'` en tiempo de ejecución; además, aun si se comparase `len(chars) <= num`, omitir la actualización de `chars` dentro del bucle produciría un ciclo infinito. En una función bien diseñada, la cadena semilla y el número deben recibirse como parámetros y validarse mediante `if len(chars) <= num: raise ValueError(...)`, delegando la captura por consola a una función externa de interfaz.

**Documentación (`docstring`, PEP 257) y anotaciones de tipo (PEP 484).** Un literal de cadena colocado como primera sentencia del cuerpo de una función se almacena automáticamente en su atributo `__doc__` y constituye su documentación formal (*docstring*), consultable con `help(funcion)`. Por su parte, las **anotaciones de tipo** en parámetros y retorno —presentes en `Funciones_Repaso.py` L111 (`-> int`), `One.py` L121 (`user: Estudiante`) y `Polimorfismo.py` L199 (`animal: Animal`)— registran metadatos sobre los tipos esperados. Es indispensable comprender que **el intérprete de Python no impone ni valida las anotaciones de tipo en tiempo de ejecución**: pasar un argumento de otro tipo no genera error por la mera presencia de la anotación; su propósito es documentar contratos y alimentar analizadores estáticos (`mypy`, `pyright`), editores e herramientas de introspección.

**Funciones como objetos de primera clase.** En Python, una función tiene identidad, tipo (`function`), atributos propios y el mismo estatus que un entero o una cadena: puede asignarse a otra variable (`decorador = my_custome_decorator` en `Decoradores.py` L178), almacenarse en diccionarios de despacho, recibirse como parámetro (`Ejecutar_operacion(Suma, 5, 3)` en `Decoradores.py` L54-66) y crearse o retornarse desde otra función (`Decoradores.py` L87-95).

## 4. Sintaxis y funcionamiento

Estructura completa de definición de una función con anotaciones, *docstring* y todas las categorías de parámetros:

```text
def <nombre_funcion>(
    <pos_only>, /,
    <estandar>, <con_defecto>=<valor>,
    *<args>,
    <kw_only>, <kw_defecto>=<valor>,
    **<kwargs>
) -> <tipo_retorno>:
    """Descripción concisa del propósito, parámetros y valor retornado."""
    <cuerpo_de_la_funcion>
    return <expresion>
```

Elementos sintácticos de la definición e invocación de funciones:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `def f():` | Crea un objeto `function` y lo enlaza al nombre `f` | `def saludar(): return "Hola"` |
| 2 | `return expr` | Termina la ejecución de `f` y entrega el objeto evaluado | `return total * 1.18` |
| 3 | Sin `return` | Al llegar al final del bloque retorna implícitamente `None` | `def log(x): print(x)` → `None` |
| 4 | `return a, b` | Empaqueta múltiples resultados en una sola `tuple` | `return cociente, resto` |
| 5 | `param=valor` | Valor por defecto evaluado **una única vez** al definir `f` | `def conectar(port=5432):` |
| 6 | `/` | Marca los parámetros previos como **solo posicionales** (PEP 570) | `def pot(base, exp, /):` |
| 7 | `*args` | Captura argumentos posicionales adicionales en una `tuple` | `def suma(*nums): return sum(nums)` |
| 8 | `*` | Fuerza que los parámetros siguientes sean **solo por nombre** (PEP 3102) | `def exportar(datos, *, utf8=True):` |
| 9 | `**kwargs` | Captura argumentos con nombre adicionales en un `dict` | `def crear(**atributos):` |
| 10 | `p: T -> R` | Anotaciones de tipo informativas (PEP 484); no validan en ejecución | `def area(r: float) -> float:` |
| 11 | `"""..."""` | *Docstring* inicial (PEP 257) accesible mediante `f.__doc__` | `"""Calcula el área."""` |

Reglas de resolución de argumentos al llamar: Python asigna primero los argumentos posicionales a las posiciones declaradas (y el excedente a `*args`), luego enlaza los argumentos por nombre (y el excedente a `**kwargs`), y finalmente rellena con sus valores por defecto los parámetros omitidos. Si falta un parámetro obligatorio o un mismo parámetro recibe valor tanto por posición como por nombre, se lanza `TypeError`.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Diferencia entre `print()` y `return`, valores por defecto y retorno múltiple.**

```python
def registrar_en_consola(usuario: str) -> None:
    print(f"[LOG] Sesión iniciada para {usuario}")


def resumir_notas(notas: list[float], redondeo: int = 2) -> tuple[float, float, float]:
    """Retorna el promedio, la nota mínima y la nota máxima de una lista no vacía."""
    promedio = round(sum(notas) / len(notas), redondeo)
    return promedio, min(notas), max(notas)


salida_log = registrar_en_consola("Flavio")
print("Retorno de función sin return:", salida_log, type(salida_log))

media, minima, maxima = resumir_notas([15.5, 18.0, 13.2, 19.4], redondeo=1)
print(f"Media: {media} | Mínima: {minima} | Máxima: {maxima}")
```

Explicación línea por línea:

- Líneas 1-2: `registrar_en_consola` solo ejecuta `print()` como efecto lateral y carece de sentencia `return`, reflejando el comportamiento analizado en `DEF_CLASS_TWO.py` (L16-26).
- Líneas 5-8: `resumir_notas` incorpora *docstring*, anotaciones de tipo, un parámetro con valor por defecto (`redondeo=2`) y un retorno múltiple de tres métricas empaquetadas como tupla.
- Líneas 11-12: muestran que `salida_log` vale `None` (`NoneType`) pese a haberse impreso una línea en consola.
- Líneas 14-15: sobreescriben `redondeo=1` mediante argumento por palabra clave y desempaquetan la tupla devuelta en tres variables semánticas.

Resultado esperado:

```text
[LOG] Sesión iniciada para Flavio
Retorno de función sin return: None <class 'NoneType'>
Media: 16.5 | Mínima: 13.2 | Máxima: 19.4
```

**Ejemplo 2 — Función pura y validación segura refactorizando `CREAR_FUNCIONES.py` (L78-91).**

```python
def generar_clave_determinista(semilla_numerica: int, alfabeto: str) -> tuple[str, int]:
    """Construye una clave breve a partir del primer dígito de la semilla y un alfabeto."""
    digito = int(str(abs(semilla_numerica))[0])
    if len(alfabeto) <= digito:
        raise ValueError(
            f"El alfabeto tiene longitud {len(alfabeto)}, pero debe superar {digito}."
        )
    clave = f"{alfabeto[digito - 2]}{alfabeto[digito]}{alfabeto[digito - 5]}{digito * 2}"
    return clave, digito


clave_generada, digito_base = generar_clave_determinista(742, "abcdefghij")
print(f"Clave: {clave_generada} (dígito base: {digito_base})")
```

Explicación de las correcciones aplicadas:

- Se desacopla por completo la función respecto de `input()` (`BUENAS_PRACTICAS.py` L86-93), recibiendo `semilla_numerica` y `alfabeto` como parámetros verificables en pruebas automatizadas.
- Se corrige el fallo de tipos de `CREAR_FUNCIONES.py` (L84): en lugar de `chars <= len(chars)` (`str <= int`), se compara `len(alfabeto) <= digito` (`int <= int`) y se señaliza una condición inválida con `ValueError` en vez de bloquear en un bucle infinito.

Resultado esperado:

```text
Clave: fhc14 (dígito base: 7)
```

### Intermedio

**Ejemplo 3 — Firma expresiva combinando `/`, `*args`, parámetros *keyword-only* (`*`) y `**kwargs`.**

```python
def construir_consulta(
    tabla: str,
    /,
    *columnas: str,
    limite: int = 10,
    ordenar_por: str | None = None,
    **filtros_exactos: object,
) -> str:
    """Genera una representación legible de consulta parametrizada."""
    seleccion = ", ".join(columnas) if columnas else "*"
    partes = [f"SELECT {seleccion} FROM {tabla}"]
    if filtros_exactos:
        condiciones = " AND ".join(f"{campo}={valor!r}" for campo, valor in filtros_exactos.items())
        partes.append(f"WHERE {condiciones}")
    if ordenar_por is not None:
        partes.append(f"ORDER BY {ordenar_por}")
    partes.append(f"LIMIT {limite}")
    return " ".join(partes)


sql_1 = construir_consulta("usuarios", "id", "nombre", "correo", activo=True, rol="editor", limite=5)
sql_2 = construir_consulta("productos", ordenar_por="precio")
print(sql_1)
print(sql_2)
```

Explicación de las decisiones tomadas:

- `tabla` va antes de `/`: es obligatorio pasarla como primer argumento posicional (`"usuarios"`), lo que deja libre incluso la clave `tabla=...` dentro de `**filtros_exactos` si una tabla tuviese una columna con ese nombre.
- `*columnas` recibe cualquier cantidad de nombres de columna posicionales en una tupla; si no se entrega ninguno (`sql_2`), queda como `()` y se emplea `"*"`.
- `limite` y `ordenar_por` aparecen después de `*columnas`, por lo que son estrictamente *keyword-only*: nunca se confundirán con un nombre de columna adicional.
- `**filtros_exactos` agrupa en un diccionario todos los pares clave-valor restantes (`activo=True`, `rol='editor'`).

Resultado esperado:

```text
SELECT id, nombre, correo FROM usuarios WHERE activo=True AND rol='editor' LIMIT 5
SELECT * FROM productos ORDER BY precio LIMIT 10
```

### Avanzado

**Ejemplo 4 — Funciones como objetos de primera clase: tabla de despacho e inspección de metadatos.**

```python
from typing import Callable

Operacion = Callable[[float, float], float]


def sumar(a: float, b: float) -> float:
    """Suma dos operandos reales."""
    return a + b


def restar(a: float, b: float) -> float:
    """Resta el segundo operando al primero."""
    return a - b


def potencia(a: float, b: float) -> float:
    """Eleva la base al exponente indicado."""
    return a ** b


REGISTRO_OPERACIONES: dict[str, Operacion] = {
    "suma": sumar,
    "resta": restar,
    "potencia": potencia,
}


def ejecutar_lote(tareas: list[tuple[str, float, float]]) -> list[str]:
    reportes: list[str] = []
    for nombre_op, x, y in tareas:
        funcion = REGISTRO_OPERACIONES[nombre_op]
        resultado = funcion(x, y)
        reportes.append(f"{funcion.__name__}({x}, {y}) = {resultado}")
    return reportes


salida = ejecutar_lote([("suma", 12, 8), ("resta", 12, 8), ("potencia", 2, 5)])
for linea in salida:
    print(linea)
print("Docstring de sumar:", sumar.__doc__)
```

Explicación de arquitectura y mantenibilidad:

- Evolucionando la idea de `Ejecutar_operacion(Suma, 5, 3)` en `Decoradores.py` (L54-66), guardar referencias a funciones en `REGISTRO_OPERACIONES` sustituye largas cadenas `if`/`elif` por una búsqueda constante $O(1)$ en diccionario (patrón *Command* / *Strategy* funcional).
- Cada función conserva sus propios atributos de introspección (`__name__`, `__doc__`, `__annotations__`), lo que permite registrar trazas precisas sin codificar nombres manualmente.

Resultado esperado:

```text
sumar(12, 8) = 20
restar(12, 8) = 4
potencia(2, 5) = 32
Docstring de sumar: Suma dos operandos reales.
```

## 6. Aplicaciones en el mundo real

- **Capas de servicio y reglas de negocio:** aislar cálculos tributarios, descuentos, elegibilidad crediticia o validaciones de dominio en funciones puras fáciles de verificar con pruebas unitarias sin levantar bases de datos ni interfaces gráficas.
- **Controladores y manejadores de rutas (*handlers*) en APIs web:** frameworks como FastAPI o Flask asocian rutas HTTP a funciones Python e inspeccionan sus firmas, valores por defecto y anotaciones de tipo para deserializar y documentar peticiones automáticamente.
- **Tuberías de limpieza y transformación de datos (ETL):** encadenar funciones pequeñas y reutilizables que normalizan cadenas (`CREAR_FUNCIONES.py` L26-30), convierten tipos y filtran registros defectuosos antes de persistirlos en [archivos CSV](../chapter-three/archivos_csv.md) o marcos de datos.
- **Registro de *plugins*, *callbacks* y eventos:** almacenar funciones en diccionarios o listas de suscriptores que se invocan dinámicamente cuando ocurre un evento del sistema o se selecciona un formato de exportación.
- **Envolturas transversales con decoradores:** utilizar funciones que aceptan `*args` y `**kwargs` para añadir medición de tiempos, control de permisos, caché o reintentos sin alterar el código de la función original (`Decoradores.py` L116-145).

## 7. Uso en producción

- **Separar estrictamente las funciones puras de la entrada/salida:** tal como enfatiza `BUENAS_PRACTICAS.py` (L86-199), una función de cálculo o validación nunca debe llamar internamente a `input()` ni depender de `print()` para comunicar resultados. Recibir datos por parámetro y devolver valores con `return` permite reutilizar la misma función en una CLI, una API web, un proceso por lotes y una suite de `pytest`.
- **Preferir parámetros *keyword-only* (`*`) para banderas booleanas y opciones:** una llamada como `procesar_pedido(pedido, True, False, 30)` es opaca y propensa a inversiones accidentales; definir `def procesar_pedido(pedido, *, notificar=True, urgente=False, timeout=30):` obliga a escribir `procesar_pedido(pedido, notificar=True, urgente=False, timeout=30)`, haciendo el código autodocumentado.
- **Respetar las convenciones de nombres de PEP 8:** aunque en los primeros apuntes aparecen nombres como `Saludo()`, `Operaciones_matematicas()` o `Pedir_Datos()`, el estándar profesional de Python reserva `PascalCase` exclusivamente para clases (`Estudiante`, `Guerrero`) y exige `snake_case` en minúsculas con verbos descriptivos para funciones y métodos (`calcular_promedio`, `pedir_datos`, `es_primo`).
- **Combinar anotaciones de tipo con verificación estática en integración continua:** dado que Python ignora las anotaciones en tiempo de ejecución, en proyectos profesionales se ejecutan verificadores estáticos (`mypy --strict` o `pyright`) en el flujo de CI para detectar desajustes de tipos antes del despliegue, reservando la validación en tiempo de ejecución para fronteras con datos externos (JSON, formularios, variables de entorno).
- **Mantener una única responsabilidad y un tipo de retorno consistente:** evitar funciones que en una rama devuelven un número y en otra devuelven un mensaje de texto de error (`Funciones_Repaso.py` L52 devuelve `float` o `"No se puede dividir entre cero"`), ya que obliga al llamador a comprobar tipos constantemente; ante entradas inválidas, es preferible lanzar una [excepción](../chapter-four/excepciones.md) explícita o retornar `None` documentado como `float | None`.

## 8. Errores comunes y recomendaciones

1. **Usar una lista o diccionario mutable como valor por defecto.**

```python
def agregar_etiqueta_erronea(etiqueta: str, acumulado: list[str] = []) -> list[str]:
    acumulado.append(etiqueta)
    return acumulado


def agregar_etiqueta_segura(etiqueta: str, acumulado: list[str] | None = None) -> list[str]:
    if acumulado is None:
        acumulado = []
    acumulado.append(etiqueta)
    return acumulado


print("Mutable compartido 1:", agregar_etiqueta_erronea("python"))
print("Mutable compartido 2:", agregar_etiqueta_erronea("backend"))
print("Con centinela None 1:", agregar_etiqueta_segura("python"))
print("Con centinela None 2:", agregar_etiqueta_segura("backend"))
```

Resultado esperado:

```text
Mutable compartido 1: ['python']
Mutable compartido 2: ['python', 'backend']
Con centinela None 1: ['python']
Con centinela None 2: ['backend']
```

Diagnóstico: en `agregar_etiqueta_erronea`, la lista `[]` se creó una única vez al ejecutarse `def`; la segunda llamada reutiliza la misma lista que ya contenía `'python'`. Solución: emplear siempre `None` como valor por defecto e instanciar la colección nueva dentro de la función cuando `acumulado is None`.

2. **Confundir `print()` con `return` e intentar operar con el resultado (`TypeError`).**

```python
# ERROR INTENCIONAL: TypeError al sumar un entero con el None devuelto por una función sin return
def calcular_doble(n):
    print(n * 2)


total = calcular_doble(10) + 5
```

Diagnóstico: `calcular_doble(10)` muestra `20` por pantalla, pero retorna `None`; al evaluar `None + 5`, Python lanza `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`. Solución: sustituir `print(n * 2)` por `return n * 2` y dejar que el código llamador decida si imprime o sigue operando con el valor.

3. **Colocar un argumento posicional después de un argumento por palabra clave (`SyntaxError`).**

```python
# ERROR INTENCIONAL: SyntaxError al pasar un argumento posicional tras uno con nombre
def restar(a, b):
    return a - b


resultado = restar(a=10, 3)
```

Diagnóstico: tal como advierte `DEF_CLASS_TWO.py` (L126), el analizador sintáctico rechaza la llamada con `SyntaxError: positional argument follows keyword argument`. Solución: colocar primero todos los argumentos posicionales y al final los argumentos con nombre (`restar(10, b=3)` o `restar(a=10, b=3)`).

4. **Asumir que las anotaciones de tipo bloquean datos inválidos en tiempo de ejecución.**

```python
def duplicar_entero(numero: int) -> int:
    return numero * 2


print(duplicar_entero(7))
print(duplicar_entero("ja"))
```

Resultado esperado:

```text
14
jaja
```

Diagnóstico: a pesar de la anotación `numero: int -> int`, pasar `"ja"` no lanza ningún error en ejecución porque `"ja" * 2` es válido en Python. Recomendación: usar herramientas de análisis estático para atrapar el error durante el desarrollo y añadir validación explícita (`isinstance(numero, int)`) únicamente cuando el dato provenga de una fuente externa no confiable.

5. **Olvidar los paréntesis al invocar una función sin argumentos.** Escribir `resultado = obtener_datos` asigna el propio objeto función a `resultado` en lugar de ejecutarla; para invocarla y obtener su valor de retorno es imprescindible escribir `resultado = obtener_datos()`.

## 9. Resumen

- La sentencia `def` crea en tiempo de ejecución un objeto `function` con su propio ámbito local, metadatos (`__name__`, `__doc__`, `__annotations__`, `__defaults__`) y estatus de objeto de primera clase.
- Los **parámetros** son los nombres locales declarados en la firma; los **argumentos** son las referencias a objetos entregadas al invocar la función (*pass-by-object-reference*).
- La firma de una función admite, en orden: parámetros solo posicionales (`/`), estándar, variádico posicional (`*args`, recibido como `tuple`), solo por palabra clave (`*`) y variádico por nombre (`**kwargs`, recibido como `dict`).
- Los valores por defecto se evalúan **una única vez** en el momento de definir la función; nunca deben usarse colecciones mutables como valor por defecto, sino el centinela `None`.
- `return` finaliza inmediatamente la función y entrega un objeto al llamador (o una `tuple` si se separan varios valores con comas); su ausencia produce implícitamente `None`.
- Las *docstrings* (PEP 257) y las anotaciones de tipo (PEP 484) documentan contratos y habilitan verificación estática sin imponer comprobaciones automáticas en tiempo de ejecución.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CREAR_FUNCIONES.py` (L1-62, L78-138, L214-241) | `CREAR_FUNCIONES.py` | Definición con `def`, parámetros frente a `input` interno, retorno múltiple `(contraseña, num)`, `*numeros`, argumentos por palabra clave y valores por defecto | Se corrigió el fallo de tipos en L84 (`while(chars <= len(chars)):`, `str <= int`) y se precisó que tras `*args` sí caben parámetros *keyword-only* |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/DEF_CLASS_TWO.py` (L16-51, L77-129) | `DEF_CLASS_TWO.py` | Retorno implícito `None` (`NoneType`), diferencia entre `print()` y `return`, código inalcanzable tras `return` y reglas de orden en llamadas con *keyword arguments* | Se formalizó el modelo de evaluación de argumentos y el diagnóstico exacto de `SyntaxError` y `TypeError` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/Funciones_Repaso.py` (L28-96, L111-125) | `Funciones_Repaso.py` | Variantes de firma (sin/con parámetros y retorno), retorno de 4 valores, `*names`, `**names`, funciones anidadas y anotación de retorno `-> int` | Se conectó `-> int` con PEP 484 explicando su comportamiento real en ejecución y la consistencia en tipos de retorno |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/MÉTODOS Y FUNCIONES/Funciones_Metodos_ejm.py` (L1-33) | `Funciones_Metodos_ejm.py` | Contraste sintáctico entre función independiente `funcion(variable)` (`len`, `dir`) y método `variable.metodo()` (`upper`, `lower`) | Se explicó la diferencia conceptual entre función libre y método enlazado a una instancia |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(2).py` (L11-39) | `EJERCICIO(2).py` | Descomposición funcional en `es_primo(num)` invocada por `numeros_primos(num)` y retorno de `(primos, n)` | Integrado como caso modelo de modularidad y retorno temprano dentro de un bucle |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/REFACTORIZACION_EJERCICIOS/Ejercicio_two.py` (L7-36) | `Ejercicio_two.py` | Separación en tres funciones (`num`, `isCousin`, `listaCousin`) y uso de `return` para salir del bucle sin `break` | Se vinculó con las convenciones `snake_case` de PEP 8 y el aislamiento entre entrada de usuario y algoritmo |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py` (L121, L143) | `One.py` | Anotación de parámetros con clases definidas por el usuario (`def Opcion(user: Estudiante):`) | Se contextualizó cómo las anotaciones de tipos documentan contratos sobre clases propias |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L86-199) | `BUENAS_PRACTICAS.py` | Separación entre `Pedir_Datos()` (interfaz de entrada) y la lógica/construcción de `Person` | Adoptado como criterio central de diseño de funciones puras y comprobables en producción |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Polimorfismo.py` (L50-53, L199-200) | `Polimorfismo.py` | Función polimórfica `Hacer_Sonido(animal)` y anotación `def hacer_sonido(animal: Animal):` | Se contrastó el enlace dinámico en tiempo de ejecución frente al carácter estático de las anotaciones |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores.py` (L48-66, L87-95) | `Decoradores.py` | Paso de funciones como argumento (`Ejecutar_operacion(Suma, 5, 3)`) y retorno de funciones envolventes con `*args, **kwargs` | Se amplió hacia tablas de despacho con funciones de primera clase e introspección de atributos |

**Fundamento complementario:** se añadieron cuatro pilares indispensables del estándar Python no detallados explícitamente en los apuntes base: (1) el modelo de paso de referencias a objetos (*call by sharing*); (2) el ciclo de evaluación única de valores por defecto en `__defaults__` y la prevención de defectos con contenedores mutables; (3) los delimitadores de parámetros solo posicionales `/` (**PEP 570**) y solo por palabra clave `*` (**PEP 3102**); y (4) las convenciones formales de *docstrings* (**PEP 257**) junto con el alcance real de **PEP 484** en tiempo de ejecución.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/controlflow.html#defining-functions> — Tutorial oficial de Python: definición de funciones, tabla de símbolos local y sentencia `return`.
- <https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions> — Tutorial oficial: valores por defecto, argumentos por palabra clave, `/`, `*`, `*args`, `**kwargs`, *docstrings* y anotaciones.
- <https://docs.python.org/3/reference/compound_stmts.html#function-definitions> — Referencia del lenguaje: gramática y semántica de ejecución de `def`.
- <https://peps.python.org/pep-0008/#function-and-variable-names> — PEP 8: guía oficial de estilo para nombres de funciones y parámetros (`snake_case`).
- <https://peps.python.org/pep-0257/> — PEP 257 (*Docstring Conventions*): convenciones estándar para cadenas de documentación en Python.
- <https://peps.python.org/pep-0484/> — PEP 484 (*Type Hints*): especificación del sistema de anotaciones de tipo y su no interferencia en tiempo de ejecución.
- <https://peps.python.org/pep-0570/> — PEP 570 (*Python Positional-Only Parameters*): especificación del separador `/` para parámetros exclusivamente posicionales.
- <https://peps.python.org/pep-3102/> — PEP 3102 (*Keyword-Only Arguments*): especificación de parámetros exclusivamente por palabra clave tras `*`.
