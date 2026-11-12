# Desempaquetamiento de Iterables y Diccionarios en Python

## 2. Introducción

Cuando los datos viajan agrupados en [listas](../../Basico/chapter-two/listas.md), [tuplas](tuplas.md), [conjuntos](conjuntos.md) o [diccionarios](diccionarios.md), una tarea constante consiste en extraer sus partes para asignarlas a [variables](../../Basico/chapter-one/variables.md) con nombre propio o enviarlas hacia otra operación. Sin una herramienta específica del lenguaje, el programador tendría que escribir líneas repetitivas basadas en índices numéricos (`nombre = datos[0]`, `apellido = datos[1]`, `edad = datos[2]`), haciendo el código verboso, rígido y propenso a equivocaciones de posición.

El **desempaquetamiento** (*unpacking*) es el mecanismo sintáctico de Python que permite **descomponer automáticamente los elementos de una colección** en una sola expresión, ya sea para asignarlos a varias variables a la vez, recorrer pares en un [bucle](../../Basico/chapter-two/bucles.md), combinar colecciones literales o entregar argumentos individuales a una función o constructor de clase.

¿Qué problemas resuelve y por qué es tan importante en Python?

1. **Claridad inmediata:** sustituye accesos crípticos como `par[0]` y `par[1]` por nombres semánticos como `clave, valor` o `minimo, maximo`.
2. **Actualizaciones simultáneas seguras:** permite intercambiar variables (`a, b = b, a`) o avanzar recurrencias matemáticas (`a, b = b, a + b`) sin variables auxiliares temporales.
3. **Flexibilidad con tamaños variables:** mediante los operadores de expansión `*` (para iterables) y `**` (para mapeos), captura tramos de longitud arbitraria y conecta de forma limpia la salida de una operación con la entrada de otra, como `Person(*Pedir_Datos())`.

En Python moderno, el desempaquetamiento no es un atajo cosmético, sino el pegamento idiomático que articula tuplas, bucles con `enumerate()` y `zip()`, retornos múltiples de [funciones](../chapter-two/funciones.md) e instanciación de objetos.

## 3. Fundamentos y conceptos

**Empaquetamiento frente a desempaquetamiento.** Ambos procesos son operaciones inversas y complementarias:

- **Empaquetar (*packing*):** reunir varios valores sueltos dentro de una sola colección, por ejemplo al escribir `coordenada = -12.04, -77.04` (que construye una [tupla](tuplas.md)).
- **Desempaquetar (*unpacking*):** distribuir los elementos contenidos en una colección existente hacia destinos individuales, por ejemplo `latitud, longitud = coordenada`.

**Cualquier iterable puede desempaquetarse.** Aunque por tradición suele llamarse "desempaquetamiento de tuplas", el lenguaje Python ejecuta esta operación mediante el **protocolo de iteración** (`iter()` y `next()`, profundizado en [iteradores](../../Avanzado/chapter-one/iteradores.md)). En consecuencia, el lado derecho de la asignación puede ser **cualquier objeto iterable**: una tupla, una lista (`CLASE_TWO_DESEMPAQUETAMIENTO.py` L19-23), una [cadena de texto](../../Basico/chapter-two/cadenas.md) (`a, b = "OK"`), un `range(2)`, un [conjunto](conjuntos.md) (recordando que en `set` el orden de entrega no es posicional) o un [diccionario](diccionarios.md) (desempaquetar `d` directamente entrega sus **claves**; para extraer valores o pares se emplea `d.values()` o `d.items()`). En el lado izquierdo, las variables receptoras pueden escribirse separadas por comas (`a, b = datos`), entre paréntesis (`(a, b) = datos`) o entre corchetes (`[a, b] = datos`) con idéntico comportamiento.

**Regla de correspondencia exacta.** En un desempaquetamiento básico sin asterisco, la cantidad de variables a la izquierda debe coincidir exactamente con la cantidad de elementos producidos por el iterable a la derecha. Si sobran o faltan valores, Python aborta la asignación lanzando `ValueError` para impedir pérdidas silenciosas de información o variables sin inicializar.

**Evaluación simultánea e intercambio sin variable temporal.** En toda asignación múltiple `x, y = expr1, expr2`, la regla del lenguaje Python ordena **evaluar por completo todo el lado derecho de izquierda a derecha antes de realizar cualquier asignación en el lado izquierdo**. Esto explica por qué en `EJERCICIO(3.2).py` (L18) la instrucción `a, b = b, a + b` calcula correctamente la sucesión de Fibonacci: primero obtiene los valores antiguos de `b` y `a + b`, y recién después actualiza `a` y `b`. Como detalle de implementación en **CPython**, cuando el compilador detecta asignaciones cortas como `a, b = b, a`, optimiza el *bytecode* intercambiando directamente las referencias en la pila de evaluación virtual (instrucción `SWAP`) sin siquiera reservar un objeto tupla temporal en el montículo de memoria (*heap*).

**Desempaquetamiento extendido con `*` (PEP 3132).** Cuando no se conoce cuántos elementos centrales trae una secuencia o solo interesan sus extremos, Python 3 permite anteponer un asterisco `*` a **una** variable receptora: `primero, *resto, ultimo = secuencia`. Sus dos reglas formales son:

1. Solo puede existir **una única expresión con `*`** por nivel de asignación (escribir `*a, *b = datos` es un `SyntaxError` porque resultaría ambiguo saber dónde termina `a` y dónde empieza `b`).
2. La variable precedida por `*` **recibe siempre una `list`**, incluso cuando el iterable original era una tupla, una cadena o un rango, e incluso cuando no sobran elementos para ella (en cuyo caso recibe la lista vacía `[]`).

**Convención de descarte `_` y `*_`.** Cuando una posición del registro no se utilizará, la convención profesional en Python consiste en asignarla al identificador `_` (por ejemplo, `nombre, _, correo = fila` o `cabecera, *_ = lineas`). Para el intérprete, `_` sigue siendo una variable ordinaria que recibe el valor descartado, pero comunica explícitamente a quien lee el código (y a herramientas de análisis estático) que esa omisión es deliberada.

**Desempaquetamiento anidado y en encabezados `for`.** El mismo mecanismo opera recursivamente sobre estructuras anidadas y en cada iteración de un bucle `for`. Mientras que en `BUCLE_FOR.py` (L115-116 y L205-206) se escribía primero `for a in diccionario.items():` y debajo `key = a[0]; value = a[1]`, Python permite desempaquetar directamente en el encabezado: `for key, value in diccionario.items():`. Incluso en estructuras de dos niveles como `Con_TextBlob.py` (`((-0.6, -0.3), Sentimiento(...))`), es posible escribir `for (minimo, maximo), sentimiento in rangos:` para obtener los dos extremos del intervalo ya separados.

**Desempaquetamiento generalizado en literales y llamadas (PEP 448, Python 3.5+).** Además del lado izquierdo de una asignación, Python permite usar `*iterable` (expansión posicional) y `**mapeo` (expansión de pares clave-valor) en dos contextos de construcción y envío:

- **Dentro de colecciones literales:** `[*lista_1, *lista_2]` concatena iterables en una lista nueva; `(*t1, *t2)` en una tupla; `{*s1, *s2}` en un conjunto; y `{**d1, **d2}` fusiona mapeos en un diccionario nuevo (antecesor general de `d1 | d2`, compatible desde Python 3.5 con cualquier objeto mapeo). En `CREAR_FUNCIONES.py` (L146) aparece `sum([*numeros])`: allí `[*numeros]` desempaqueta `numeros` dentro de una nueva lista literal, aunque conviene notar que pasar `sum(numeros)` directamente evita crear esa copia intermedia en memoria.
- **Al invocar funciones o constructores (*call-site unpacking*):** escribir `Person(*datos)` expande cada elemento de `datos` como un argumento posicional independiente (`BUENAS_PRACTICAS.py` L187), mientras que `Celular(**configuracion)` entrega cada par `"clave": valor` del diccionario como un argumento por palabra clave (`marca="Xiaomi", modelo="XP30"`). La contraparte en la **definición** de funciones (`def funcion(*args, **kwargs):`, vista en `Decoradores_Multiples.py` L6) realiza la operación inversa (empaquetar argumentos recibidos) y se desarrolla en [funciones](../chapter-two/funciones.md).

## 4. Sintaxis y funcionamiento

Formas sintácticas del desempaquetamiento en asignaciones, bucles, literales y llamadas:

```text
<var1>, <var2>, ... = <iterable>
<primero>, *<intermedios>, <ultimo> = <iterable>
(<sub1>, <sub2>), <var3> = <iterable_anidado>
for <var1>, <var2> in <iterable_de_pares>:
nueva_lista = [*<iterable1>, *<iterable2>]
nuevo_dict = {**<mapeo1>, **<mapeo2>}
resultado = <funcion>(*<iterable>, **<mapeo_claves_str>)
```

Patrones de desempaquetamiento y su comportamiento:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `a, b = iterable` | Asignación exacta posición a posición; exige igual longitud | `x, y = (10, 20)` |
| 2 | `a, b = b, a` | Intercambio simultáneo evaluando primero el lado derecho completo | `a, b = b, a` |
| 3 | `a, *resto = it` | Asigna el primero a `a` y captura los restantes en una **`list`** `resto` (PEP 3132) | `a, *r = (1, 2, 3)` → `r == [2, 3]` |
| 4 | `*inicio, z = it` | Captura todos salvo el último en la lista `inicio` y el último en `z` | `*ini, z = "sol"` → `ini == ['s', 'o']` |
| 5 | `a, _, c = it` | Descarta por convención el valor intermedio usando `_` | `dia, _, anio = (15, 8, 2025)` |
| 6 | `(a, b), c = it` | Desempaquetamiento estructural anidado respetando la forma interna | `(x, y), tag = ((4, 5), "A")` |
| 7 | `for k, v in it:` | Desempaqueta cada elemento producido por el bucle en el propio encabezado | `for i, val in enumerate(lista):` |
| 8 | `[*it1, *it2]` | Expande múltiples iterables dentro de un literal `list`, `tuple` o `set` (PEP 448) | `[0, *(1, 2), *range(3, 5)]` |
| 9 | `{**d1, **d2}` | Expande pares clave-valor en un literal `dict`; ante colisión gana el último | `{**{"a": 1}, **{"a": 9}}` → `{'a': 9}` |
| 10 | `f(*it, **map)` | Desempaqueta argumentos posicionales (`*`) y por nombre (`**`) al llamar a `f` | `divmod(*(17, 5))` → `(3, 2)` |

Funcionamiento y restricciones en llamadas: al emplear `funcion(**diccionario)`, todas las claves del diccionario deben ser **cadenas de texto** que correspondan a nombres de parámetros válidos de `funcion`, y ningún parámetro puede recibir valor dos veces (por ejemplo, una vez por posición mediante `*tupla` y otra vez por nombre mediante `**diccionario`), pues de lo contrario Python lanza `TypeError: got multiple values for argument`.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Desempaquetamiento básico sobre distintos iterables e intercambio simultáneo.**

```python
datos_lista = ["Flavio", "Silva"]
nombre, apellido = datos_lista

inicial_1, inicial_2 = "PY"

a, b = 0, 1
a, b = b, a + b
a, b = b, a + b

print(f"Usuario: {nombre} {apellido}")
print(f"Iniciales: {inicial_1}-{inicial_2}")
print(f"Estado Fibonacci tras dos pasos: a={a}, b={b}")
```

Explicación línea por línea:

- Líneas 1-2: extraen los dos textos de `datos_lista` directamente en `nombre` y `apellido`, tal como introduce `CLASE_TWO_DESEMPAQUETAMIENTO.py` (L19-23).
- Línea 4: demuestra que una cadena de longitud `2` también es un iterable desempaquetable carácter a carácter (`'P'` y `'Y'`).
- Línea 6: inicializa simultáneamente `a = 0` y `b = 1` (`EJERCICIO(3.2).py` L11).
- Líneas 7-8: avanzan dos pasos de la sucesión de Fibonacci evaluando primero `(b, a + b)` antes de reasignar: tras la línea 7 quedan `a=1, b=1`; tras la línea 8 quedan `a=1, b=2`.
- Líneas 10-12: muestran los valores extraídos y actualizados.

Resultado esperado:

```text
Usuario: Flavio Silva
Iniciales: P-Y
Estado Fibonacci tras dos pasos: a=1, b=2
```

**Ejemplo 2 — Captura flexible con asterisco (`*`) y descarte con `_`.**

```python
registro_csv = ("ORD-900", "2025-05-10", "teclado", "raton", "cable", 189.90)
codigo, _, *articulos, total = registro_csv

primero, *intermedios, ultimo = (10, 20)

print("Código:", codigo, "| Total:", total)
print("Artículos:", articulos, type(articulos))
print("Intermedios vacíos:", intermedios)
```

Explicación línea por línea:

- Línea 1: simula una fila con código, fecha, una cantidad variable de productos y el monto final.
- Línea 2: `codigo` toma el primer valor, `_` descarta explícitamente la fecha, `*articulos` absorbe los tres productos centrales en una lista y `total` recibe el último elemento (`189.90`).
- Línea 4: comprueba el caso extremo donde la tupla solo tiene dos elementos `(10, 20)`: `primero` recibe `10`, `ultimo` recibe `20` e `*intermedios` queda como lista vacía `[]` sin lanzar error.
- Líneas 6-8: confirman que `articulos` es siempre de tipo `list` aunque el origen fuera una `tuple`.

Resultado esperado:

```text
Código: ORD-900 | Total: 189.9
Artículos: ['teclado', 'raton', 'cable'] <class 'list'>
Intermedios vacíos: []
```

### Intermedio

**Ejemplo 3 — Desempaquetamiento limpio en bucles con `enumerate()`, `zip()`, `.items()` y pares anidados.**

```python
productos = ["Laptop", "Monitor", "Teclado"]
precios = (3200, 850, 180)

for indice, (producto, precio) in enumerate(zip(productos, precios), start=1):
    print(f"{indice}. {producto}: S/ {precio}")

rangos = [((-1.0, -0.2), "Bajo"), ((-0.2, 0.5), "Medio")]
for (minimo, maximo), nivel in rangos:
    print(f"Nivel {nivel} cubre desde {minimo} hasta {maximo}")
```

Explicación de las decisiones tomadas:

- En el primer bucle se combinan `enumerate(..., start=1)` y `zip(productos, precios)`. Cada iteración produce una estructura anidada `(indice, (producto, precio))`. Usar el patrón anidado `indice, (producto, precio)` elimina por completo los accesos manuales `item[0]` e `item[1]` que se escribían en las primeras prácticas de `BUCLE_FOR.py` (L115-116).
- En el segundo bucle se refina el patrón de `Con_TextBlob.py` (L20-21): en vez de recibir `rango, nivel` y luego indexar `rango[0]` y `rango[1]`, el patrón `(minimo, maximo), nivel` desarma el intervalo en el propio encabezado, haciendo la condición matemática mucho más legible.

Resultado esperado:

```text
1. Laptop: S/ 3200
2. Monitor: S/ 850
3. Teclado: S/ 180
Nivel Bajo cubre desde -1.0 hasta -0.2
Nivel Medio cubre desde -0.2 hasta 0.5
```

**Ejemplo 4 — Retorno múltiple de funciones e instanciación con `*` y `**`.**

```python
class Persona:
    def __init__(self, nombre, edad, ciudad):
        self.nombre = nombre
        self.edad = edad
        self.ciudad = ciudad

    def resumen(self):
        return f"{self.nombre} ({self.edad} años) - {self.ciudad}"


def cargar_ficha_validada():
    return "Flavio", 19, "Huaral"


usuario_1 = Persona(*cargar_ficha_validada())

datos_api = {"ciudad": "Lima", "nombre": "Elena", "edad": 24}
usuario_2 = Persona(**datos_api)

print(usuario_1.resumen())
print(usuario_2.resumen())
```

Explicación de las decisiones tomadas:

- Siguiendo el principio arquitectónico de separación de responsabilidades explicado en `BUENAS_PRACTICAS.py` (L95-193), la clase `Persona` no solicita entradas por teclado dentro de `__init__`; recibe datos ya listos.
- `cargar_ficha_validada()` retorna una tupla de tres valores, y `Persona(*cargar_ficha_validada())` expande esa tupla directamente sobre los tres parámetros posicionales del constructor.
- Para `usuario_2`, los datos provienen de un diccionario `datos_api` cuyas claves están en distinto orden al de `__init__`. El desempaquetamiento `Persona(**datos_api)` empareja cada valor por nombre de parámetro (`nombre=..., edad=..., ciudad=...`), haciendo irrelevante el orden en el diccionario.

Resultado esperado:

```text
Flavio (19 años) - Huaral
Elena (24 años) - Lima
```

### Avanzado

**Ejemplo 5 — Composición inmutable de colecciones y fusión de configuraciones con PEP 448.**

```python
ruta_base = ("/srv", "datos")
subcarpetas = ["2025", "reportes"]
ruta_completa = (*ruta_base, *subcarpetas, "ventas.csv")
print("Ruta ensamblada:", "/".join(ruta_completa))

ajustes_defecto = {"timeout": 5, "reintentos": 2, "compresion": True}
ajustes_entorno = {"timeout": 15}
ajustes_ejecucion = {**ajustes_defecto, **ajustes_entorno, "reintentos": 4}

print("Original intacto:", ajustes_defecto)
print("Ajustes efectivos:", ajustes_ejecucion)
```

Explicación de rendimiento y mantenibilidad:

- `(*ruta_base, *subcarpetas, "ventas.csv")` ensambla una nueva tupla combinando una tupla previa, una lista y un literal final en un único paso declarativo, sin convertir manualmente `list(ruta_base)` ni concatenar objetos intermedios.
- `{**ajustes_defecto, **ajustes_entorno, "reintentos": 4}` implementa el patrón de **inmutabilidad por copia** (*non-destructive override*) habitual en arquitecturas de software limpias: superpone múltiples fuentes de configuración de izquierda a derecha (donde la última clave repetida prevalece: `timeout` pasa a `15` y `reintentos` a `4`) garantizando que `ajustes_defecto` no sufra mutaciones colaterales.

Resultado esperado:

```text
Ruta ensamblada: /srv/datos/2025/reportes/ventas.csv
Original intacto: {'timeout': 5, 'reintentos': 2, 'compresion': True}
Ajustes efectivos: {'timeout': 15, 'reintentos': 4, 'compresion': True}
```

## 6. Aplicaciones en el mundo real

- **Procesamiento de archivos tabulares y encabezados:** al leer líneas de un CSV o de un registro de texto, `encabezado, *filas_datos = lineas` separa limpiamente la primera fila de nombres de columna respecto del cuerpo de datos.
- **Adaptadores e inyección de parámetros en backends:** transformar un diccionario validado de filtros de búsqueda en argumentos de consulta hacia un repositorio o servicio mediante `repositorio.buscar(**filtros)`.
- **Decoradores y funciones envolventes (*wrappers*):** como se aprecia en `Decoradores_Multiples.py` (L6-9), un decorador genérico captura cualquier combinación de argumentos con `def wrapper(*args, **kwargs):` y los reenvía intactos a la función original mediante `func(*args, **kwargs)` (tema profundizado en [decoradores](../../Avanzado/chapter-one/decoradores.md)).
- **Algoritmos matemáticos y de programación dinámica:** actualizar estados recurrentes (`anterior, actual = actual, anterior + actual`) o rotar punteros en grafos y matrices sin variables intermedias que introduzcan errores de orden de sobrescritura.
- **Desestructuración de respuestas de bases de datos o servicios internos:** recibir `exito, carga, codigo_error = servicio.procesar()` asignando cada pieza a una variable explícita desde el primer instante.

## 7. Uso en producción

- **Evitar desempaquetar por posición registros demasiado extensos:** escribir `a, b, c, d, e, f, g = obtener_datos()` obliga a contar comas mentalmente y se rompe si alguien inserta un campo intermedio. Pasados tres o cuatro valores, en producción conviene devolver un objeto con atributos con nombre (`NamedTuple`, `dataclass` o diccionario tipado) en lugar de una tupla posicional larga.
- **Nunca depender del orden al desempaquetar un `set`:** aunque Python permite sintácticamente `x, y = {"A", "B"}` (como menciona `CLASE_TWO_DESEMPAQUETAMIENTO.py` L16), en un conjunto qué variable recibe `"A"` y cuál `"B"` es arbitrario y puede variar entre procesos por `PYTHONHASHSEED`. Solo deben desempaquetarse posicionalmente iterables con orden determinista (tuplas, listas, cadenas, diccionarios o resultados de `sorted()`).
- **Cuidar el consumo de memoria de `*resto` sobre flujos gigantes:** si `lineas_archivo` es un iterador perezoso sobre un archivo de varios gigabytes, escribir `primera, *resto = lineas_archivo` forzará a cargar **todo el archivo restante en una lista RAM**. Para extraer únicamente la primera línea sin agotar el flujo en memoria, debe usarse `primera = next(iterador)` (estudiado en [iteradores](../../Avanzado/chapter-one/iteradores.md)).
- **Validar el origen antes de ejecutar `funcion(**datos_externos)`:** expandir con `**` un diccionario proveniente directamente de una petición externa sin filtrar sus claves puede provocar `TypeError: got an unexpected keyword argument` o sobrescribir parámetros sensibles con valores por defecto. Siempre debe validarse o filtrarse el esquema antes de desempaquetarlo sobre funciones internas.

## 8. Errores comunes y recomendaciones

1. **Desajuste entre la cantidad de variables y la longitud del iterable (`ValueError`).**

```python
# ERROR INTENCIONAL: ValueError porque hay 3 valores para solo 2 variables
coordenadas_3d = (10, 20, 30)
x, y = coordenadas_3d
```

Diagnóstico: lanza `ValueError: too many values to unpack (expected 2)` (y si hubiera menos elementos que variables, `ValueError: not enough values to unpack (expected 3, got 2)`). Solución: alinear la aridad exacta (`x, y, z = coordenadas_3d`) o absorber el excedente de forma explícita con `x, y, *_ = coordenadas_3d`.

2. **Colocar más de un operador `*` en el mismo nivel de asignación.**

```python
# ERROR INTENCIONAL: SyntaxError al usar dos expresiones con asterisco en el mismo nivel
primero, *medio_1, *medio_2, ultimo = [1, 2, 3, 4, 5]
```

Diagnóstico: lanza `SyntaxError: multiple starred expressions in assignment` en tiempo de compilación, ya que la repartición entre `medio_1` y `medio_2` sería indeterminada. Solución: utilizar a lo sumo un `*` por nivel de estructura.

3. **Olvidar `.values()` o `.items()` al desempaquetar un diccionario.**

```python
usuario = {"nombre": "Flavio", "apellido": "Silva"}
campo_1, campo_2 = usuario
valor_1, valor_2 = usuario.values()

print("Sin .values() extrae claves:", campo_1, campo_2)
print("Con .values() extrae valores:", valor_1, valor_2)
```

Resultado esperado:

```text
Sin .values() extrae claves: nombre apellido
Con .values() extrae valores: Flavio Silva
```

Diagnóstico: iterar un diccionario recorre sus **claves**, por lo que `campo_1, campo_2 = usuario` asigna `"nombre"` y `"apellido"` en lugar de `"Flavio"` y `"Silva"`. Tal como señala `CLASE_TWO_DESEMPAQUETAMIENTO.py` (L17) y practica `REPASO(01).py` (L3), para extraer los valores debe invocarse `usuario.values()`.

4. **Omitir los paréntesis al desempaquetar una estructura anidada en un bucle.**

```python
# ERROR INTENCIONAL: ValueError porque cada elemento de enumerate(zip(...)) tiene longitud 2, no 3
nombres = ["Ana", "Luis"]
edades = [20, 22]
for indice, nombre, edad in enumerate(zip(nombres, edades)):
    print(indice, nombre, edad)
```

Diagnóstico: `enumerate(zip(...))` entrega tuplas de **dos** posiciones `(indice, (nombre, edad))`, no de tres; al escribir tres variables planas lanza `ValueError: not enough values to unpack (expected 3, got 2)`. Solución: reflejar la estructura interna con paréntesis: `for indice, (nombre, edad) in enumerate(zip(nombres, edades)):`.

5. **Desempaquetar innecesariamente dentro de una lista nueva para funciones que ya aceptan cualquier iterable.** Escribir `sum([*numeros])` (`CREAR_FUNCIONES.py` L146) o `list([*datos])` construye una lista extra sin necesidad; `sum(numeros)` consume directamente cualquier iterable sin duplicar memoria.

## 9. Resumen

- El **desempaquetamiento** extrae los elementos de cualquier objeto **iterable** hacia variables individuales siguiendo el protocolo de iteración.
- Sin asterisco, el número de variables debe coincidir exactamente con la cantidad de elementos o se produce `ValueError`.
- Python evalúa íntegramente el lado derecho antes de asignar el izquierdo, habilitando intercambios limpios (`a, b = b, a`) y recurrencias simultáneas (`a, b = b, a + b`).
- El desempaquetamiento extendido `a, *resto, z = iterable` (PEP 3132) admite un único `*` por nivel y entrega siempre una `list` en `resto`; `_` señala valores descartados deliberadamente.
- En encabezados `for`, combinaciones como `enumerate()`, `zip()` y `.items()` se desempaquetan directamente sin requerir índices `[0]` y `[1]`.
- Los operadores `*` y `**` (PEP 448) también permiten ensamblar literales (`[*a, *b]`, `{**d1, **d2}`) y expandir argumentos posicionales o por nombre al invocar funciones y constructores (`Clase(*tupla, **diccionario)`).

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASE_TWO_DESEMPAQUETAMIENTO.py` (L15-28, L139-140) | `CLASE_TWO_DESEMPAQUETAMIENTO.py` | Asignación `nombre, apellido = datos`, compatibilidad con listas, tuplas, conjuntos y `datos.values()`, y bucle `for palabra, numero in zip(t1, t2):` | Se formalizó el protocolo de iteración subyacente, los errores `ValueError` por aridad y el riesgo de orden arbitrario sobre `set` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/REPASO(01).py` (L1-8) | `REPASO(01).py` | Desempaquetamiento de valores de diccionario `name, name_2 = tp.values()` | Contrastado en la sección 8 frente al desempaquetamiento directo del diccionario (que entrega claves) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L67, L110-117, L157-164, L204-207) | `BUCLE_FOR.py` | Desempaquetamiento en `zip()` frente a indexación manual `num[0]` / `num[1]` en `enumerate()` y `diccionario.items()` | Se unificó la forma idiomática de desempaquetar directamente en el encabezado `for` e incluso anidar `enumerate(zip(...))` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CREAR_FUNCIONES.py` (L90, L106, L146) | `CREAR_FUNCIONES.py` | Retorno múltiple `return contraseña, num`, captura `contra, primer_numero = ...` y expansión literal `sum([*numeros])` | Se explicó la sintaxis `[*numeros]` (PEP 448) y por qué `sum(numeros)` evita crear una lista intermedia |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(1).py` (L30-32) | `EJERCICIO(1).py` | Desempaquetamiento del par `(ordenado, final)` retornado por una función | Relacionado con el empaquetamiento implícito en sentencias `return` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(3.2).py` (L11, L18) | `EJERCICIO(3.2).py` | Inicialización múltiple `a, b = 0, 1` y recurrencia simultánea `a, b = b, a + b` en Fibonacci | Se demostró el orden de evaluación del lenguaje Python y la optimización de pila en **CPython** (Ejemplo 1) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L184-192) | `BUENAS_PRACTICAS.py` | Contraste directo entre `Person(*Pedir_Datos())` y el desempaquetamiento previo en seis variables antes de instanciar `Person(...)` | Sirvió como modelo central del Ejemplo 4, ampliándolo con `**diccionario` para argumentos por nombre |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L6-9, L59-61) | `Decoradores_Multiples.py` | Reenvío transparente de argumentos mediante `func(*args, **kwargs)` dentro de funciones decoradoras | Conectado como aplicación real y puente hacia [funciones](../chapter-two/funciones.md) y [decoradores](../../Avanzado/chapter-one/decoradores.md) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L169, L178-179) | `Juego.py` | Retorno de `(mensaje, estadisticas)` en sobrecarga de operador y desempaquetamiento `mensaje, tabla = three` | Evidencia cómo los métodos especiales de POO también aprovechan el retorno y desempaquetamiento de tuplas |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Crear_Clase.py` (L83-91) | `Crear_Clase.py` | Desempaquetamiento `tipo, color, tamaño = Pedir_Datos()` y `for key, values in valores` sobre `__dict__.items()` | Integrado en la trazabilidad entre funciones auxiliares e instanciación de objetos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` (L20-21) | `Con_TextBlob.py` | Bucle `for rango, sentimiento in self.rangos:` sobre lista de pares estructurados | Ampliado en el Ejemplo 3 al desempaquetamiento estructural anidado `for (minimo, maximo), nivel in rangos:` |

**Fundamento complementario:** se incorporaron tres mecanismos estándar del lenguaje que completan lo visto en ambas carpetas: (1) el desempaquetamiento extendido en asignaciones `primero, *resto, ultimo = datos` especificado por **PEP 3132**; (2) la convención profesional `_` y `*_` para posiciones descartadas; y (3) la fusión declarativa de mapeos `{**d1, **d2}` y de argumentos por palabra clave `Clase(**datos)` definidos en **PEP 448**.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences> — Tutorial oficial de Python: empaquetamiento de tuplas y desempaquetamiento de secuencias.
- <https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists> — Tutorial oficial: desempaquetamiento de listas y diccionarios de argumentos con `*` y `**` en llamadas a funciones.
- <https://docs.python.org/3/reference/simple_stmts.html#assignment-statements> — Referencia del lenguaje: reglas formales de evaluación y asignación sobre listas de objetivos (*target lists*) e iterables.
- <https://peps.python.org/pep-3132/> — PEP 3132 (*Extended Iterable Unpacking*): especificación del operador `*` en el lado izquierdo de asignaciones.
- <https://peps.python.org/pep-0448/> — PEP 448 (*Additional Unpacking Generalizations*): generalización de `*` y `**` en llamadas y literales de listas, tuplas, conjuntos y diccionarios.
