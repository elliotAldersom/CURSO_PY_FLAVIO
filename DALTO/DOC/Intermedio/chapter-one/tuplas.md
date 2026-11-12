# Tuplas en Python

## 2. Introducción

En el nivel básico se estudió cómo agrupar colecciones ordenadas de datos dentro de una [lista](../../Basico/chapter-two/listas.md), cuya característica central es la capacidad de agregar, reemplazar o eliminar elementos durante la ejecución del programa. Sin embargo, muchos conjuntos de valores representan una unidad fija cuya estructura no debería alterarse una vez creada: las coordenadas geográficas `(latitud, longitud)` de una ciudad, un color `(rojo, verde, azul)`, una fila leída desde una base de datos o un intervalo numérico `(-0.3, -0.1)`.

Una **tupla** (`tuple`) es una **secuencia ordenada e inmutable** de referencias a objetos en Python. **Ordenada** significa que cada elemento conserva una posición numérica fija (índice) desde `0` hasta `len(tupla) - 1`; **inmutable** significa que, una vez construida la tupla, el lenguaje impide añadir, eliminar o sustituir cualquiera de sus posiciones.

¿Por qué existe si ya se dispone de listas? Porque en el diseño de software la restricción explícita protege la integridad de los datos. Al utilizar una tupla, el programa garantiza que ninguna función o bucle intermedio alterará accidentalmente la cantidad ni el orden de sus componentes. Además, esta inmutabilidad resuelve un problema técnico fundamental en Python: permite calcular una huella numérica constante (**valor *hash***) sobre la colección cuando sus elementos también son inmutables, habilitando a las tuplas para funcionar como claves en [diccionarios](diccionarios.md) y como miembros de [conjuntos](conjuntos.md), lugares donde las listas están prohibidas.

Dentro de Python, las tuplas cumplen un papel estructural en el propio lenguaje: el retorno de múltiples valores desde una [función](../chapter-two/funciones.md), los pares `(índice, valor)` generados por `enumerate()`, las combinaciones producidas por `zip()` y gran parte del mecanismo de [desempaquetamiento](desempaquetamiento.md) descansan directamente sobre ellas.

## 3. Fundamentos y conceptos

**La coma construye la tupla; los paréntesis agrupan.** Una confusión habitual al iniciarse en Python consiste en atribuir la creación de la tupla a los paréntesis `(...)`. En la gramática del lenguaje Python, salvo en el caso de la tupla vacía, **el operador sintáctico que crea una tupla es la coma (`,`)**. La instrucción `datos = "Flavio", "Silva", 17` construye una tupla de tres elementos sin necesidad de paréntesis. Los paréntesis se añaden por legibilidad o cuando es obligatorio desambiguar la precedencia frente a otros [operadores](../../Basico/chapter-one/operadores.md) —por ejemplo, al pasar una tupla literal como argumento dentro de `print((1, 2))` o al incluirla dentro de una lista `[(-0.6, -0.3), (-0.3, -0.1)]`—.

**Tupla de un solo elemento (*singleton*).** Como los paréntesis por sí solos sirven también para agrupar expresiones matemáticas o de texto, escribir `valor = ("dato")` **no** produce una tupla, sino simplemente la [cadena de texto](../../Basico/chapter-two/cadenas.md) `"dato"`. Para indicar a Python que se desea una tupla de longitud `1`, resulta indispensable colocar una coma final: `valor = ("dato",)` o `valor = "dato",`.

**Tupla vacía y corrección al material original.** La única excepción donde los paréntesis vacíos definen por sí mismos la estructura es la **tupla vacía**: tanto el literal `()` como la llamada al constructor integrado `tuple()` crean una tupla de cero elementos (`len(()) == 0`). Conviene corregir aquí una afirmación imprecisa presente en el material original (`CLASS_TWO_TUPLA.py` L7 y `CLASE_TWO_DESEMPAQUETAMIENTO.py` L10-13), donde se indica que no es posible crear tuplas vacías mediante la forma literal y que debe recurrirse obligatoriamente a `tuple()`. En el lenguaje Python, `()` es sintaxis oficial y directa para representar la tupla vacía.

**Conversión mediante `tuple(iterable)`.** El tipo integrado `tuple` pertenece al espacio de nombres `builtins` del lenguaje. Invocado sin argumentos devuelve `()`; invocado con cualquier objeto **iterable** (aquel capaz de entregar sus elementos uno por uno, como una lista, una cadena, un rango o un conjunto) recorre dicho objeto y construye una tupla con sus elementos: `tuple(["a", "b"])` produce `('a', 'b')` y `tuple("sol")` produce `('s', 'o', 'l')`.

**Inmutabilidad de referencias frente a mutabilidad de objetos internos.** Una tupla almacena **referencias** (direcciones lógicas hacia objetos), no copias aisladas de valores. La regla del lenguaje establece que el contenedor tupla no permite reasignar ninguna de sus casillas (`tupla[0] = "otro"` lanza `TypeError`). Sin embargo, si una de esas casillas apunta a un objeto mutable —como una [lista](../../Basico/chapter-two/listas.md)—, ese objeto interno conserva sus propios métodos de modificación. Así, en `registro = ([10, 20], "activo")`, la operación `registro[0].append(30)` es válida porque modifica el contenido de la lista referenciada sin cambiar a qué lista apunta la posición `0` de la tupla.

**Reasignación de variable frente a mutación.** En el archivo original `Ejm_Datos_Compuestos.py` (L20) se observa que tras definir `tupla = ("Flavio", ..., 61088098)` es posible ejecutar `tupla = ("Estrada", "Flavio")`. Esto **no** contradice la inmutabilidad: la segunda instrucción crea un objeto tupla completamente nuevo y cambia la [variable](../../Basico/chapter-one/variables.md) `tupla` para que apunte al nuevo objeto, dejando intacta (o lista para ser recolectada de memoria) la tupla anterior.

**Capacidad de *hash* (*hashability*).** En Python, un objeto es ***hashable*** cuando posee un número entero identificativo calculable mediante la función integrada `hash(objeto)` que permanece invariante durante toda su vida útil y puede compararse por igualdad (`==`). Las listas no son *hashables* porque su contenido cambia. En cambio, una tupla **es *hashable* si y solo si todos sus elementos son también *hashables***. Por ello `hash(("Perú", "Lima"))` funciona y permite usar esa tupla como clave de un diccionario, mientras que `hash(([1, 2], "Lima"))` lanza `TypeError: unhashable type: 'list'`.

**Registros heterogéneos frente a colecciones homogéneas.** Más allá de la diferencia técnica de mutabilidad, en Python existe una convención semántica de diseño: las listas suelen emplearse para colecciones homogéneas de longitud variable (muchos nombres, muchos precios), mientras que las tuplas suelen representar **registros estructurados** donde cada posición tiene un significado propio, como `(nombre, edad)` en `EJERCICIO(1).py` o `(rango_polaridad, objeto_sentimiento)` en `Con_TextBlob.py`.

**Representación en memoria: lenguaje frente a CPython.** El lenguaje Python solo especifica el comportamiento inmutable y secuencial de `tuple`. A nivel de implementación en **CPython** (el intérprete oficial escrito en C), una tupla se representa mediante la estructura `PyTupleObject`, cuyo encabezado y arreglo de punteros se reservan en **un único bloque contiguo de memoria** de tamaño fijo. En contraste, `PyListObject` requiere dos bloques separados (encabezado y arreglo dinámico sobreasignado para absorber futuros `append()`). Como consecuencia específica de **CPython**, una tupla ocupa menos memoria RAM y se instancia más rápido que una lista equivalente, además de reutilizar un único objeto vacío en caché cuando se evalúa `()`.

## 4. Sintaxis y funcionamiento

Formas sintácticas de construcción y consulta sobre tuplas:

```text
tupla_vacia = ()
tupla_unitaria = (<elemento>,)
tupla_explicita = (<elemento1>, <elemento2>, ...)
tupla_empaquetada = <elemento1>, <elemento2>, ...
tupla_convertida = tuple(<iterable>)
elemento = <tupla>[<índice>]
subtupla = <tupla>[<inicio>:<fin>:<paso>]
```

Formas de creación y particularidades sintácticas:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `()` | Literal de tupla vacía (cero elementos) | `vacia = ()` |
| 2 | `(<x>,)` o `<x>,` | Tupla de un único elemento; la coma final es obligatoria | `uno = ("dato",)` |
| 3 | `(<a, b, ...>)` | Literal entre paréntesis; recomendado cuando mejora la claridad | `par = (10, 20)` |
| 4 | `<a, b, ...>` | Empaquetado por comas sin paréntesis exteriores | `par = 10, 20` |
| 5 | `tuple()` | Constructor integrado sin argumentos; devuelve tupla vacía | `tuple()` → `()` |
| 6 | `tuple(<iterable>)` | Construye una tupla recorriendo cualquier iterable | `tuple([1, 2])` → `(1, 2)` |

Operaciones de secuencia y métodos disponibles:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `tupla[i]` | Devuelve el elemento en el índice `i` (`0` o negativo); lanza `IndexError` fuera de rango | `(10, 20, 30)[-1]` → `30` |
| 2 | `tupla[i:j:k]` | Rebanado (*slicing*); devuelve una **nueva tupla** con el tramo indicado | `(1, 2, 3, 4)[1:3]` → `(2, 3)` |
| 3 | `t1 + t2` | Concatenación; genera una nueva tupla uniendo ambos operandos | `(1, 2) + (3,)` → `(1, 2, 3)` |
| 4 | `tupla * n` | Repetición entera; genera una nueva tupla repitiendo sus referencias `n` veces | `(0,) * 3` → `(0, 0, 0)` |
| 5 | `x in tupla` | Comprobación booleana de pertenencia secuencial | `2 in (1, 2, 3)` → `True` |
| 6 | `len(tupla)` | Función integrada que retorna la cantidad de elementos | `len((10, 20))` → `2` |
| 7 | `tupla.count(x)` | Método que cuenta cuántas veces aparece un valor igual a `x` | `(1, 2, 1).count(1)` → `2` |
| 8 | `tupla.index(x[, i[, j]])` | Devuelve el primer índice de `x` (opcionalmente entre `i` y `j`); lanza `ValueError` si no está | `("a", "b").index("b")` → `1` |
| 9 | `hash(tupla)` | Calcula el entero de *hash* si todos sus componentes son *hashables* | `isinstance(hash((1, 2)), int)` → `True` |

Funcionamiento general: a diferencia de `list`, el tipo `tuple` **carece por completo de métodos de mutación** (`append`, `extend`, `insert`, `remove`, `pop`, `clear`, `sort`, `reverse`) y rechaza la sentencia `del tupla[i]`. Sus únicos dos métodos públicos son de consulta (`.count()` e `.index()`). Cuando se requiere obtener una versión ordenada de los elementos de una tupla, se emplea la función integrada `sorted(tupla)`, la cual devuelve siempre una **lista** nueva sin alterar la tupla original; si se necesita conservar el tipo inmutable, basta envolver el resultado con `tuple(sorted(tupla))`.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Variantes de creación, tupla unitaria y consulta posicional.**

```python
vacia_literal = ()
vacia_funcion = tuple()
unitaria = ("Flavio",)
sin_parentesis = "Silva", "Estrada", 18
desde_lista = tuple(["Lima", "Perú"])

print(vacia_literal == vacia_funcion, len(vacia_literal))
print(unitaria, type(unitaria))
print(sin_parentesis[0], sin_parentesis[-1])
print(desde_lista)
```

Explicación línea por línea:

- Líneas 1-2: se crean dos tuplas vacías, la primera con el literal `()` y la segunda con `tuple()`. Ambas producen el mismo valor vacío de longitud `0`.
- Línea 3: la coma posterior a `"Flavio"` convierte la expresión en una tupla de un solo elemento; sin esa coma, `unitaria` sería de tipo `str`.
- Línea 4: las comas empaquetan dos textos y un entero en una tupla de tres posiciones sin requerir paréntesis exteriores.
- Línea 5: `tuple([...])` recorre la lista temporal y construye una tupla con sus dos cadenas.
- Línea 7: comprueba que ambas formas vacías son iguales (`True`) y que su longitud es `0`.
- Línea 8: muestra la representación `('Flavio',)` —Python conserva siempre la coma en pantalla en tuplas de longitud `1` para evidenciar su tipo— junto con `<class 'tuple'>`.
- Línea 9: accede al primer elemento (`índice 0`) y al último (`índice -1`).
- Línea 10: imprime la tupla convertida desde la lista.

Resultado esperado:

```text
True 0
('Flavio',) <class 'tuple'>
Silva 18
('Lima', 'Perú')
```

**Ejemplo 2 — Métodos `.count()`, `.index()` y extracción mediante rebanadas.**

```python
asistencias = ("danilo", "carlos", "juan", "fabio", "juan", "juan")
repeticiones = asistencias.count("juan")
primera_posicion = asistencias.index("juan")
ultimos_dos = asistencias[4:]

print(f"Apariciones de juan: {repeticiones}")
print(f"Primer índice de juan: {primera_posicion}")
print(ultimos_dos)
```

Explicación línea por línea:

- Línea 1: define una tupla de seis cadenas con valores repetidos, análoga a la trabajada en `CLASS_TWO_TUPLA.py`.
- Línea 2: `.count("juan")` recorre la tupla y contabiliza las tres apariciones exactas de `"juan"`.
- Línea 3: `.index("juan")` devuelve `2`, correspondiente a la primera posición donde aparece dicho nombre.
- Línea 4: la rebanada `asistencias[4:]` extrae desde el índice `4` hasta el final, devolviendo una **nueva tupla** de dos elementos.
- Líneas 6-8: se presentan en salida estándar los conteos, el índice hallado y la subtupla resultante.

Resultado esperado:

```text
Apariciones de juan: 3
Primer índice de juan: 2
('juan', 'juan')
```

### Intermedio

**Ejemplo 3 — Tabla inmutable de rangos para clasificación por intervalos.**

```python
rangos_calificacion = (
    ((-1.0, -0.3), "Negativo"),
    ((-0.3, 0.3), "Neutral"),
    ((0.3, 1.0), "Positivo"),
)

lecturas = [-0.55, 0.0, 0.72]
for polaridad in lecturas:
    etiqueta_asignada = "Fuera de rango"
    for limites, etiqueta in rangos_calificacion:
        if limites[0] <= polaridad <= limites[1]:
            etiqueta_asignada = etiqueta
            break
    print(f"Polaridad {polaridad:>5}: {etiqueta_asignada}")
```

Explicación de las decisiones tomadas:

- Inspirado en el diseño de `Con_TextBlob.py`, cada regla asocia un par numérico `(mínimo, máximo)` con su categoría textual. Aquí no solo cada par interior es una tupla, sino también la tabla completa `rangos_calificacion`, asegurando que ninguna parte del programa añada o desordene umbrales accidentalmente en tiempo de ejecución.
- Durante el recorrido exterior sobre `lecturas`, el [bucle](../../Basico/chapter-two/bucles.md) interno separa cada registro en `limites` y `etiqueta` (técnica estudiada a fondo en [desempaquetamiento](desempaquetamiento.md)) y consulta `limites[0]` y `limites[1]` mediante indexación posicional constante.
- El uso de `break` detiene la búsqueda interna apenas se encuentra el intervalo correspondiente, evitando comparaciones innecesarias sobre el resto de reglas.

Resultado esperado:

```text
Polaridad -0.55: Negativo
Polaridad   0.0: Neutral
Polaridad  0.72: Positivo
```

**Ejemplo 4 — Tuplas como claves compuestas e inmutabilidad superficial frente a objetos anidados.**

```python
tarifas_envio = {
    ("Perú", "estándar"): 15.0,
    ("Perú", "exprés"): 28.5,
    ("Chile", "estándar"): 22.0,
}

consulta = ("Perú", "exprés")
print("Tarifa consultada:", tarifas_envio[consulta])

lote_auditoria = ("LOTE-2025", ["revisión_inicial"])
lote_auditoria[1].append("aprobado_calidad")
print("Tupla con lista interna mutada:", lote_auditoria)
```

Explicación de las decisiones tomadas:

- En `tarifas_envio`, cada clave necesita combinar dos datos: país y modalidad. Una lista `["Perú", "exprés"]` fallaría porque no es *hashable*, mientras que la tupla `("Perú", "exprés")` contiene únicamente cadenas inmutables y puede indexar el [diccionario](diccionarios.md) directamente.
- En la segunda parte, `lote_auditoria` combina un identificador fijo (`str`) con un historial dinámico (`list`). No es posible reemplazar la lista por otra (`lote_auditoria[1] = ...` fallaría), pero sí invocar `.append()` sobre la lista ya referenciada. Este contraste demuestra que la inmutabilidad de la tupla protege sus enlaces, no el estado interno de objetos mutables anidados; a la vez, debido a esa lista interna, `lote_auditoria` **no** podría usarse como clave en `tarifas_envio`.

Resultado esperado:

```text
Tarifa consultada: 28.5
Tupla con lista interna mutada: ('LOTE-2025', ['revisión_inicial', 'aprobado_calidad'])
```

### Avanzado

**Ejemplo 5 — Registros legibles con `collections.namedtuple` y comparación de memoria en CPython.**

```python
import sys
from collections import namedtuple

Coordenada = namedtuple("Coordenada", ["latitud", "longitud", "altitud_m"])

estacion = Coordenada(latitud=-12.0464, longitud=-77.0428, altitud_m=154)
print(f"Latitud: {estacion.latitud}, Altitud: {estacion[2]} m")
print("Es subclase de tuple:", isinstance(estacion, tuple))

muestra_tupla = tuple(range(100))
muestra_lista = list(range(100))
print("Tupla más compacta o igual que lista:", sys.getsizeof(muestra_tupla) <= sys.getsizeof(muestra_lista))
```

Explicación de rendimiento y mantenibilidad:

- Cuando una tupla supera dos o tres campos, recordar qué significa `registro[0]` frente a `registro[2]` deteriora la mantenibilidad del código. La fábrica `namedtuple` del módulo `collections` (perteneciente a la **biblioteca estándar** de Python) genera una subclase de `tuple` que conserva la inmutabilidad, el orden, la compatibilidad con indexación numérica (`estacion[2]`) y la capacidad de *hash*, añadiendo acceso autodescriptivo por nombre de atributo (`estacion.latitud`).
- `isinstance(estacion, tuple)` devuelve `True`, lo que garantiza interoperabilidad total con cualquier código que espere una tupla convencional.
- En las últimas líneas, `sys.getsizeof()` mide el tamaño directo del contenedor. En **CPython**, `muestra_tupla` (`PyTupleObject` de tamaño exacto) emplea menos bytes que `muestra_lista` (`PyListObject` con búfer dinámico sobreasignado). Se expresa la verificación como relación lógica (`<=`) porque los bytes exactos dependen de la arquitectura de 32 o 64 bits y de la implementación del intérprete.

Resultado esperado:

```text
Latitud: -12.0464, Altitud: 154 m
Es subclase de tuple: True
Tupla más compacta o igual que lista: True
```

## 6. Aplicaciones en el mundo real

- **Retorno estructurado en funciones y servicios:** cuando una operación calcula simultáneamente varios datos relacionados —como `(contraseña, digito_base)` en `CREAR_FUNCIONES.py` o `(codigo_estado, cuerpo_respuesta)` en un cliente HTTP—, Python empaqueta el resultado en una tupla para devolverlo como una sola entidad coherente.
- **Acceso a bases de datos relacionales (PEP 249 / DB-API 2.0):** conectores estándar como `sqlite3`, `psycopg` o `mysql-connector` entregan cada fila resultante de una consulta `SELECT` como una tupla inmutable, reflejando que el registro leído representa una instantánea fija de las columnas consultadas.
- **Claves compuestas en cachés y tableros analíticos:** almacenar métricas indexadas por `(año, mes, sucursal)` o coordenadas `(fila, columna)` en tableros dispersos aprovecha la naturaleza *hashable* de las tuplas sin concatenar cadenas artificiales como `"2025-03-Lima"`.
- **Configuración de constantes de dominio:** rutas permitidas, dimensiones de imagen `(ancho, alto)`, colores RGB `(255, 128, 0)` o tablas de rangos numéricos como la de `Con_TextBlob.py` se declaran como tuplas para impedir mutaciones accidentales durante la vida del proceso.
- **Validación de tipos múltiples:** funciones integradas del lenguaje como `isinstance(valor, (int, float))` o el manejo de múltiples errores en bloques `except (ValueError, EOFError):` (visibles en `BUENAS_PRACTICAS.py`) exigen específicamente una tupla de clases, no una lista.

## 7. Uso en producción

- **Preferir tuplas para colecciones constantes en configuración global:** declarar constantes de módulo como `FORMATOS_PERMITIDOS = (".csv", ".json", ".parquet")` en lugar de listas evita que una función receptora ejecute `.append()` por error y contamine el estado global del servicio.
- **Evitar anidar objetos mutables dentro de tuplas:** aunque Python permite construir `([1, 2], "activo")`, combinar un contenedor inmutable con elementos mutables rompe las garantías de seguridad frente a efectos secundarios e inhabilita el cálculo de `hash()`. Si todo el registro debe ser inmutable, los elementos internos también deben convertirse a tipos inmutables (`tuple`, `frozenset`, `str`).
- **Reemplazar tuplas posicionales largas por registros con nombre:** en código profesional, una tupla cruda de cinco o seis posiciones (`usuario[4]`) es propensa a errores silenciosos cuando cambia el orden de los campos. A partir de tres campos heterogéneos conviene emplear `collections.namedtuple`, `typing.NamedTuple` o `@dataclass(frozen=True)` (estudio que conecta con [clases y objetos](../chapter-five/clases_y_objetos.md)).
- **No simular mutación concatenando tuplas repetidamente en un bucle:** escribir `acumulado = acumulado + (nuevo,)` dentro de un bucle de `n` iteraciones copia la tupla entera en cada vuelta, elevando el costo temporal a `O(n²)`. El patrón correcto en producción consiste en acumular sobre una `list` temporal en tiempo amortizado `O(1)` por inserción y, al concluir, convertir una sola vez mediante `tuple(acumulado)`.

## 8. Errores comunes y recomendaciones

1. **Intentar modificar o eliminar una posición mediante índice.** Es el error demostrado en `CLASE_ONE.py` (L134):

```python
# ERROR INTENCIONAL: TypeError al intentar reasignar un elemento de una tupla
tupla = ("Flavio Silva", "Flavio.G.S.E", 17, "Guitarrista")
tupla[3] = "hola"
```

Diagnóstico: lanza `TypeError: 'tuple' object does not support item assignment` (y `del tupla[3]` lanza `TypeError: 'tuple' object doesn't support item deletion`). Si los datos necesitan actualizarse posición por posición durante su ciclo de vida, la estructura apropiada es una [lista](../../Basico/chapter-two/listas.md); si solo se requiere generar una versión derivada puntual, se construye una nueva tupla por rebanado o conversión temporal.

2. **Omitir la coma en una tupla de un solo elemento.** Este descuido no produce error de sintaxis, pero altera silenciosamente el tipo del dato:

```python
falsa_tupla = ("Python")
tupla_real = ("Python",)

print(type(falsa_tupla), len(falsa_tupla))
print(type(tupla_real), len(tupla_real))
```

Resultado esperado:

```text
<class 'str'> 6
<class 'tuple'> 1
```

Diagnóstico: `("Python")` evalúa los paréntesis como simple agrupación y deja una cadena de longitud `6`; iterar sobre `falsa_tupla` recorrerá seis letras individuales (`'P'`, `'y'`, ...) en lugar de un único elemento `"Python"`. Solución: incluir siempre la coma final `("Python",)` en tuplas unitarias.

3. **Intentar usar una tupla con elementos mutables como clave de diccionario o miembro de conjunto.**

```python
# ERROR INTENCIONAL: TypeError porque la tupla contiene una lista no hashable
clave_invalida = ("usuario", [10, 20])
registro = {clave_invalida: "activo"}
```

Diagnóstico: produce `TypeError: unhashable type: 'list'`. Ser una tupla no garantiza automáticamente ser *hashable*; cada componente interno debe serlo también. Solución: transformar la colección interna a tupla `("usuario", (10, 20))` o a `frozenset` antes de emplearla como clave.

4. **Pasar múltiples valores sueltos a `tuple(...)` en lugar de un único iterable.**

```python
# ERROR INTENCIONAL: TypeError porque tuple() acepta como máximo 1 argumento iterable
datos = tuple("Flavio", "Silva")
```

Diagnóstico: lanza `TypeError: tuple expected at most 1 argument, got 2`. El constructor `tuple()` convierte **un** iterable existente, tal como advierte el material en `CLASS_TWO_TUPLA.py` (L13-15). Solución: usar directamente el literal `("Flavio", "Silva")` sin llamar a `tuple()`, o pasar un único iterable cuando se convierte otra colección.

5. **Sobrescribir el identificador integrado `tuple`.** Asignar `tuple = (1, 2)` oculta el tipo integrado en el ámbito actual e impide invocar `tuple(lista)` más adelante (`TypeError: 'tuple' object is not callable`). Conviene emplear nombres descriptivos del dominio como `coordenadas`, `rango` o `registro`.

## 9. Resumen

- Una **tupla** (`tuple`) es una secuencia ordenada e **inmutable** de referencias a objetos.
- El elemento sintáctico que construye tuplas no vacías es la **coma** (`,`); por ello una tupla de un solo elemento exige coma final `("dato",)`, mientras que la tupla vacía puede crearse indistintamente con `()` o con `tuple()`.
- Soporta indexación (`tupla[0]`, `tupla[-1]`), rebanado (`tupla[a:b]`), concatenación (`+`), repetición (`*`), `len()`, pertenencia (`in`) y únicamente dos métodos: `.count(x)` e `.index(x)`.
- La inmutabilidad impide cambiar qué objetos referencian sus posiciones, pero no congela objetos mutables anidados (como una lista interna).
- Una tupla es ***hashable*** únicamente cuando todos sus elementos lo son, cualidad que le permite actuar como clave en diccionarios y elemento en conjuntos.
- En **CPython**, `PyTupleObject` utiliza una única asignación contigua de tamaño fijo, lo que reduce el consumo de memoria frente a `PyListObject`; en producción, `collections.namedtuple` aporta nombres de campo legibles manteniendo todas las ventajas de `tuple`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L124-140, L624-630) | `CLASE_ONE.py` | Creación literal con paréntesis, acceso por índice `tupla[0]`, error al intentar mutar `tupla[3] = "hola"` y uso de `.join()` sobre tuplas | Se formalizó la causa del `TypeError` distinguiendo contenedor inmutable frente a objetos referenciados |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Datos_Compuestos.py` (L13-22) | `Ejm_Datos_Compuestos.py` | Contraste entre bloqueo de mutación posicional y redefinición completa de la variable `tupla = ("Estrada", "Flavio")` | Se explicó técnicamente la diferencia entre mutación en el lugar y reasignación de nombres a un nuevo objeto en memoria |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASS_TWO_TUPLA.py` (L1-53) | `CLASS_TWO_TUPLA.py` | Conversión `tuple([...])`, creación sin paréntesis por comas, tupla unitaria con coma final, `.count()`, `.index()` y rebanado `miTupla[4:]` | Se corrigió la afirmación de la L7 aclarando que `()` sí crea una tupla vacía válida sin requerir `tuple()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/EJM_TUPLA.py` (L1-15) | `EJM_TUPLA.py` | Práctica de `tuple()`, empaquetado sin paréntesis, tupla de un elemento y anidamiento `b = a, a_1, a_2` | Se integró en la explicación de la coma como constructor real y en el Ejemplo 1 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASE_TWO_DESEMPAQUETAMIENTO.py` (L10-13, L33-41, L90-98) | `CLASE_TWO_DESEMPAQUETAMIENTO.py` | Variantes de creación de tuplas, anidamiento `(t1, t2, t3, t4)` y uso de tuplas como claves de diccionario | Se rectificó el comentario de las L10-13 sobre literales vacíos y se formalizó la regla de *hashability* recursiva |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/REPASO(01).py` (L10-20, L56-100) | `REPASO(01).py` | Consolidación de tuplas anidadas, tuplas unitarias y su empleo como claves e insumo de `dict.fromkeys()` | Se conectó con la inmutabilidad estructural y con el uso de claves compuestas en el Ejemplo 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(1).py` (L23-32) | `EJERCICIO(1).py` | Agrupación de registros heterogéneos `(nombre, edad)` dentro de una lista y retorno múltiple como tupla | Se contextualizó la diferencia de diseño entre registros fijos (tuplas) y colecciones dinámicas (listas) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` (L20-32) | `Con_TextBlob.py` | Pares estructurados `((-0.6, -0.3), Sentimiento(...))` para asociar intervalos inmutables de polaridad con instancias de clase | Inspiró el Ejemplo 3 y la recomendación de declarar tablas completas de reglas como tuplas inmutables |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L37-51, L78) | `Decorador_Property.py` | Asignación `xd.Datos = "Flavio Gerardo", 19` validada en un *setter* mediante `isinstance(new_Data, tuple) and len(new_Data) == 2` | Ilustra cómo Python empaqueta automáticamente expresiones separadas por coma al asignarlas a propiedades de objetos |

**Fundamento complementario:** se incorporaron tres aspectos no detallados explícitamente en las clases originales: (1) el caso límite de tuplas que contienen referencias a objetos mutables (`([1, 2], "a")`) y su efecto sobre `hash()`; (2) la diferencia interna en **CPython** entre `PyTupleObject` (bloque único de tamaño fijo) y `PyListObject` (doble bloque con sobreasignación dinámica); y (3) el uso profesional de `collections.namedtuple` de la **biblioteca estándar** para dotar de nombres descriptivos a los campos de una tupla.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences> — Tutorial oficial de Python: tuplas, secuencias, empaquetado con comas y construcción de tuplas vacías y unitarias.
- <https://docs.python.org/3/library/stdtypes.html#tuples> — Referencia de la biblioteca estándar sobre el tipo `tuple` y las operaciones comunes de secuencia inmutable.
- <https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy> — Modelo de datos oficial de Python: especificación de secuencias inmutables y condiciones de *hashability* (`__hash__` y `__eq__`).
- <https://docs.python.org/3/library/collections.html#collections.namedtuple> — Documentación oficial de `collections.namedtuple` en la biblioteca estándar.
