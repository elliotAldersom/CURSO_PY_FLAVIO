# Funciones Anónimas (Expresiones Lambda) y Orden Superior

## 2. Introducción

Al trabajar con operaciones de ordenamiento, filtrado, agrupación o transformación de colecciones, con frecuencia se necesita entregar una pequeña regla de cálculo como argumento a otra función: extraer el segundo campo de una tupla para ordenar alumnos por edad (`EJERCICIO(1).py` L27), obtener el valor de un par clave-valor (`CLASE_ONE.py` L957) o normalizar una celda de texto (`Importando_con_pandas.py` L49). Definir con `def` una función auxiliar de dos líneas con nombre propio para usarla una única vez en la línea siguiente puede fragmentar la lectura cuando la regla es elemental.

Una **expresión `lambda`** permite construir **en línea** (*inline*) una [función](funciones.md) anónima —sin enlazarla obligatoriamente a un identificador— compuesta por una lista opcional de parámetros y una **única expresión** cuyo resultado se retorna de manera automática.

Comprender con criterio técnico las expresiones `lambda` permite:

1. **Parametrizar funciones de orden superior con concisión:** expresar criterios de orden (`sorted`, `min`, `max`) o transformación puntual (`map`, `filter`) justo en el punto de llamada.
2. **Conocer sus límites gramaticales exactos:** distinguir qué cabe en una expresión frente a algoritmos de múltiples sentencias que exigen `def`.
3. **Escribir código idiomático conforme a PEP 8:** evitar el antipatrón de asignar expresiones `lambda` a variables con nombre y elegir con fundamento cuándo una [comprensión](../chapter-one/comprensiones.md) o el módulo `operator` resultan más claros y eficientes.
4. **Prevenir errores de enlace tardío (*late binding*):** dominar cómo interactúan las funciones anónimas con los bucles y el [ámbito de variables](ambito_variables.md).

## 3. Fundamentos y conceptos

**Naturaleza de `lambda`: expresión frente a sentencia.** Mientras que `def` es una **sentencia compuesta** que ocupa un bloque indentado y enlaza un nombre en el espacio actual, `lambda` es una **expresión**: puede aparecer en cualquier lugar de Python donde se espere un valor (como argumento dentro de paréntesis, elemento de un diccionario de despacho o valor de retorno). Al evaluarse, construye un objeto de tipo `function` exactamente equivalente en capacidades de ejecución al producido por `def`.

**Equivalencia en tiempo de ejecución e identidad `<lambda>`.** No existe una categoría especial de "objeto lambda" distinta de las funciones ordinarias: `type(lambda x: x)` es `<class 'function'>`, y el compilador de **CPython** genera para `lambda x: x * 2` el mismo *bytecode* de cuerpo (`BINARY_OP`, `RETURN_VALUE`) que para `def duplicar(x): return x * 2`. La única diferencia observable en el objeto resultante radica en sus metadatos: dado que nació sin nombre, sus atributos `__name__` y `__qualname__` reciben la cadena genérica `"<lambda>"`, lo que afecta la claridad de las trazas de excepción (*tracebacks*) y herramientas de perfilado si la función falla.

**Restricción a una única expresión.** El cuerpo de una función `lambda` admite **exclusivamente una expresión**, cuyo valor evaluado se devuelve implícitamente sin escribir `return`. En consecuencia:

- **No se permiten sentencias** dentro del cuerpo: `return`, `pass`, `assert`, `raise`, bucles `for` o `while` (como los requeridos para generar la serie de Fibonacci en `EJERCICIO(3).py` L11-20 y `EJERCICIO(3.2).py` L10-20), bloques `try`/`except` ni asignaciones clásicas con `=`.
- **Sí se permiten expresiones compuestas**, tales como operaciones aritméticas o lógicas (`lambda n: n % 2 != 0`), llamadas a métodos, tuplas de retorno (`lambda x: (x, x ** 2)`) y la **expresión condicional ternaria** (`lambda x: x.strip() if isinstance(x, str) else x`, empleada en `Importando_con_pandas.py` L49).
- **Soporta todas las formas de parámetros de Python** salvo anotaciones de tipo con `:`: cero parámetros (`lambda: 0`), varios parámetros (`lambda a, b: a + b`), valores por defecto (`lambda x, factor=2: x * factor`), `*args`, parámetros *keyword-only* tras `*` y `**kwargs`.

**Funciones de orden superior habituales (`sorted`, `min`, `max`, `filter`, `map`).** Se denomina función de orden superior a toda aquella que recibe una o más funciones como argumento o devuelve otra función:

- **`sorted(iterable, key=..., reverse=...)` y `lista.sort(key=...)`:** invocan la función `key` **una sola vez por cada elemento** (patrón *Decorate-Sort-Undecorate*) para calcular su clave de comparación sin modificar el elemento original (`CLASE_ONE.py` L957; `Ejercicio_one.py` L20). Conviene notar que en `EJERCICIO(1).py` (L27) se llamaba a `compañeros.sort(key=lambda x: x[1])` dentro del bucle `for` en cada registro, reordenando innecesariamente la lista $N$ veces; `Ejercicio_one.py` (L20) y `EJERCICOS(6).py` (L31) corrigen esto ordenando una sola vez al finalizar la carga.
- **`min(iterable, key=...)` y `max(iterable, key=...)`:** seleccionan el elemento mínimo o máximo evaluando el criterio devuelto por `key`.
- **`filter(funcion, iterable)` y `map(funcion, iterable)`:** tal como practica `LAMBDA_FUNCIONES.py` (L47-51, L82-96), aplican una función predicado o transformadora sobre un iterable y devuelven un **iterador perezoso** (*lazy iterator*) que produce valores bajo demanda y se agota tras un único recorrido (profundizado en [iteradores](../../Avanzado/chapter-one/iteradores.md)). Si se necesita recorrer el resultado varias veces o indexarlo, debe materializarse en `list(...)` o `tuple(...)`.

**Criterio PEP 8 (regla E731) sobre `nombre = lambda ...`.** En `LAMBDA_FUNCIONES.py` (L29 y L92) se muestran ejemplos didácticos como `multiplicar_por_dos = lambda x: x * 2` y `es_par = lambda n: not (n % 2 == 0)` para ilustrar su sintaxis inicial. Sin embargo, la guía oficial de estilo **PEP 8** establece explícitamente que **siempre debe usarse una sentencia `def` en lugar de asignar una expresión `lambda` directamente a un identificador**. La razón es técnica: `def multiplicar_por_dos(x): return x * 2` ocupa una sola línea adicional o incluso la misma longitud, permite añadir *docstrings* y anotaciones de tipo, y registra `"multiplicar_por_dos"` en `__name__` en vez de `"<lambda>"` cuando ocurre un error en producción.

**Comparación con comprensiones y el módulo estándar `operator`.** En Python moderno:

- Para transformar y filtrar secuencias en memoria, una [comprensión de lista](../chapter-one/comprensiones.md) o expresión generadora (`[n for n in listado if n % 2 != 0]`) suele resultar más legible y directa que combinar `list(filter(lambda n: n % 2 != 0, listado))` o `list(map(lambda x: x * 2, datos))`, evitando además el sobrecoste de llamada a función Python por cada elemento.
- Cuando la función `key` solo extrae un índice, clave o atributo (`lambda item: item[1]` o `lambda u: u.edad`), el módulo estándar `operator` ofrece `itemgetter(1)` y `attrgetter("edad")`, implementados en C dentro de **CPython**, que expresan la intención declarativamente y ejecutan más rápido sobre colecciones grandes.

**La trampa del enlace tardío (*late binding*) en bucles.** Cuando se crean varias funciones `lambda` dentro de un bucle o lista por comprensión (`acciones = [lambda: i for i in range(3)]`), cada función captura la **variable** `i` del ámbito envolvente, no el **valor numérico** que tenía `i` en ese instante. Al terminar el bucle, `i` vale `2`, por lo que todas las funciones creadas devuelven `2`. Para fijar el valor de cada iteración en el momento de crear la función, se captura como valor por defecto de un parámetro local: `lambda i=i: i`.

## 4. Sintaxis y funcionamiento

Gramática de una expresión `lambda`:

```text
lambda <parametros_opcionales>: <unica_expresion>
```

Formas válidas y patrones de uso con funciones de orden superior:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `lambda: expr` | Función anónima sin parámetros (útil para fábricas por defecto) | `defaultdict(lambda: "N/A")` |
| 2 | `lambda x: expr` | Función anónima de un parámetro | `lambda x: x.lower().strip()` |
| 3 | `lambda a, b: expr` | Varios parámetros posicionales o con valor por defecto | `lambda base, tasa=0.18: base * (1 + tasa)` |
| 4 | `lambda *a, **kw: expr` | Acepta argumentos variádicos igual que `def` | `lambda *nums: sum(nums)` |
| 5 | Ternario en cuerpo | Bifurcación mediante expresión condicional `A if cond else B` | `lambda n: "par" if n % 2 == 0 else "impar"` |
| 6 | `sorted(it, key=...)` | Ordena elementos según el criterio calculado por la función `key` | `sorted(pares, key=lambda p: p[1])` |
| 7 | `min`/`max(it, key=...)` | Halla el extremo según la métrica devuelta por `key` | `max(alumnos, key=lambda a: a[1])` |
| 8 | `filter(fn, it)` | Iterador perezoso con los elementos donde `bool(fn(x))` es `True` | `list(filter(lambda x: x > 0, datos))` |
| 9 | `map(fn, it)` | Iterador perezoso aplicando `fn` a cada elemento de uno o más iterables | `list(map(lambda a, b: a + b, l1, l2))` |
| 10 | `operator.itemgetter(k)` | Alternativa estándar en C a `lambda x: x[k]` para claves de orden | `sorted(pares, key=itemgetter(1))` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Criterios `key` en `sorted()`, `min()` y `max()` sobre tuplas y diccionarios.**

```python
compañeros = [("Elena", 22), ("Flavio", 19), ("Mateo", 25), ("Lucía", 18)]

ordenados_edad = sorted(compañeros, key=lambda alumno: alumno[1])
asistente = min(compañeros, key=lambda alumno: alumno[1])
profesor = max(compañeros, key=lambda alumno: alumno[1])

agenda_codigos = {"flavio": "12345", "juan": "67890", "maria": "11223", "ana": "33445"}
agenda_por_codigo = dict(sorted(agenda_codigos.items(), key=lambda par: par[1]))

print("Ordenados por edad:", ordenados_edad)
print(f"Asistente: {asistente[0]} ({asistente[1]}) | Profesor: {profesor[0]} ({profesor[1]})")
print("Agenda por valor:", agenda_por_codigo)
```

Explicación línea por línea:

- Líneas 1-5: refinan el problema de `EJERCICIO(1).py` (L27-30) y `Ejercicio_one.py` (L20-21): `sorted(..., key=lambda alumno: alumno[1])` ordena toda la colección en $O(n \log n)$ si se requiere el listado completo, mientras que si únicamente interesan los dos extremos (menor y mayor), `min(..., key=...)` y `max(..., key=...)` los obtienen directamente en tiempo lineal $O(n)$.
- Líneas 7-8: reproducen de forma limpia la ordenación de diccionario por valor practicada en `CLASE_ONE.py` (L954-959).

Resultado esperado:

```text
Ordenados por edad: [('Lucía', 18), ('Flavio', 19), ('Elena', 22), ('Mateo', 25)]
Asistente: Lucía (18) | Profesor: Mateo (25)
Agenda por valor: {'maria': '11223', 'flavio': '12345', 'ana': '33445', 'juan': '67890'}
```

### Intermedio

**Ejemplo 2 — `filter()`, `map()`, agotamiento de iteradores perezosos y comparativa con comprensiones.**

```python
mediciones_brutas = [" 12.5 ", "-3.0", " 8.0", "0.0", " 15.5 "]

normalizadas = list(map(lambda texto: float(texto.strip()), mediciones_brutas))
iterador_positivas = filter(lambda valor: valor > 0, normalizadas)

primera_pasada = list(iterador_positivas)
segunda_pasada = list(iterador_positivas)

equivalente_comprension = [
     v for texto in mediciones_brutas if (v := float(texto.strip())) > 0
]

print("Normalizadas con map:", normalizadas)
print("Primera lectura del iterador filter:", primera_pasada)
print("Segunda lectura del iterador agotado:", segunda_pasada)
print("Con comprensión equivalente:", equivalente_comprension)
```

Explicación de las decisiones tomadas:

- `map(...)` convierte y limpia cada cadena, y `filter(...)` retiene solo los valores estrictamente positivos.
- Al evaluar `primera_pasada = list(iterador_positivas)`, se consume íntegramente el iterador perezoso; por eso `segunda_pasada` queda vacía `[]`, confirmando el comentario técnico de `LAMBDA_FUNCIONES.py` (L48-58) acerca de almacenar la lista resultante cuando se necesite recorrerla más de una vez.
- `equivalente_comprension` muestra cómo una sola comprensión unifica transformación y filtrado en un paso legible.

Resultado esperado:

```text
Normalizadas con map: [12.5, -3.0, 8.0, 0.0, 15.5]
Primera lectura del iterador filter: [12.5, 8.0, 15.5]
Segunda lectura del iterador agotado: []
Con comprensión equivalente: [12.5, 8.0, 15.5]
```

### Avanzado

**Ejemplo 3 — Ordenamiento multicriterio con tupla de claves y uso profesional de `operator.itemgetter`.**

```python
from operator import itemgetter

productos = [
    {"sku": "B-20", "categoria": "Audio", "precio": 150.0},
    {"sku": "A-10", "categoria": "Video", "precio": 420.0},
    {"sku": "C-05", "categoria": "Audio", "precio": 150.0},
    {"sku": "D-01", "categoria": "Audio", "precio": 89.0},
]

# Ordena por categoría ascendente, luego precio descendente (-p["precio"]), y desempata por SKU
ranking = sorted(
    productos,
    key=lambda p: (p["categoria"], -p["precio"], p["sku"]),
)

# Cuando todos los criterios tienen el mismo sentido ascendente, itemgetter evita llamadas Python
por_categoria_y_sku = sorted(productos, key=itemgetter("categoria", "sku"))

print("Multicriterio mixto:", [p["sku"] for p in ranking])
print("Con itemgetter:", [p["sku"] for p in por_categoria_y_sku])
```

Explicación de rendimiento y diseño:

- Devolver una tupla `(p["categoria"], -p["precio"], p["sku"])` dentro de `lambda` aprovecha la comparación lexicográfica de [tuplas](../chapter-one/tuplas.md) para resolver criterios mixtos (texto ascendente y número descendente negando el monto) en una única llamada a `sorted()`.
- Cuando no hace falta transformar signos ni normalizar cadenas, `itemgetter("categoria", "sku")` delega la extracción directamente a código nativo de la biblioteca estándar, evitando crear e invocar un marco de función Python por cada registro.

Resultado esperado:

```text
Multicriterio mixto: ['B-20', 'C-05', 'D-01', 'A-10']
Con itemgetter: ['B-20', 'C-05', 'D-01', 'A-10']
```

## 6. Aplicaciones en el mundo real

- **Ordenación y selección sobre colecciones de registros o respuestas JSON:** clasificar resultados de consultas, tableros de puntuaciones o catálogos comerciales por múltiples atributos combinados (`sorted`, `min`, `max`, `heapq.nlargest`).
- **Transformaciones tabulares en ciencia de datos:** aplicar reglas breves por fila o celda sobre estructuras de `pandas` (`df.map(...)` o `serie.apply(lambda x: ...)`, anticipado en `Importando_con_pandas.py` L49 y desarrollado en [fundamentos de pandas](../chapter-three/pandas_fundamentos.md) y [pandas avanzado](../../Avanzado/chapter-four/pandas_avanzado.md)).
- **Fábricas ligeras para valores por defecto en estructuras de datos:** inicializar contadores compuestos o diccionarios anidados mediante `collections.defaultdict(lambda: {"intentos": 0, "activo": True})`.
- **Manejadores breves de eventos (*callbacks*) en interfaces gráficas o pruebas:** adaptar la firma de un comando o sustituir temporalmente una dependencia (*stub*) en una prueba unitaria (`monkeypatch.setattr(servicio, "obtener_tasa", lambda moneda: 3.75)`).

## 7. Uso en producción

- **Cumplir estrictamente PEP 8 (E731):** nunca escribir `calcular_iva = lambda monto: monto * 0.18`; definir `def calcular_iva(monto: float) -> float:` proporciona un nombre real en los registros de errores (*logs*), admite anotaciones de tipo y facilita colocar puntos de interrupción en el depurador.
- **Limitar `lambda` a expresiones genuinamente breves y evidentes:** si una expresión `lambda` empieza a anidar múltiples operadores ternarios (`a if c1 else (b if c2 else d)`), llamadas encadenadas largas o manejo de casos borde, debe extraerse de inmediato a una función `def` con nombre semántico y pruebas propias.
- **Preferir operaciones vectorizadas sobre `lambda` en `pandas` cuando existan:** aunque `Importando_con_pandas.py` (L49) usa `df.applymap(lambda x: ...)` (método renombrado a `DataFrame.map` desde pandas 2.1), ejecutar una función Python celda por celda sobre millones de registros es órdenes de magnitud más lento que emplear métodos vectorizados de columnas (`df[col].str.replace('"', '').str.strip()`).
- **Sustituir `lambda` triviales por constructores o funciones existentes:** como muestra acertadamente `CLASE_ONE.py` (L805 y L826) al escribir `sorted(mi_lista, key=str)`, nunca debe escribirse `key=lambda x: str(x)` ni `key=lambda x: len(x)` cuando puede pasarse directamente la referencia `key=str` o `key=len`.

## 8. Errores comunes y recomendaciones

1. **Incluir `return` o sentencias imperativas dentro de una expresión `lambda` (`SyntaxError`).**

```python
# ERROR INTENCIONAL: SyntaxError porque 'return' es una sentencia y lambda solo admite una expresión
duplicar = lambda x: return x * 2
```

Diagnóstico: lanza `SyntaxError: invalid syntax` porque el retorno en `lambda` ya es implícito y su gramática rechaza cualquier sentencia. Solución: escribir solo la expresión (`lambda x: x * 2`) en contextos anónimos, o usar `def` si se requieren varias sentencias.

2. **Caer en el enlace tardío (*late binding*) al crear funciones `lambda` dentro de un bucle.**

```python
multiplicadores_erroneos = [lambda x: x * factor for factor in range(1, 4)]
multiplicadores_correctos = [lambda x, f=factor: x * f for factor in range(1, 4)]

print("Enlace tardío (todos usan factor=3):", [fn(10) for fn in multiplicadores_erroneos])
print("Captura por defecto (1, 2 y 3):", [fn(10) for fn in multiplicadores_correctos])
```

Resultado esperado:

```text
Enlace tardío (todos usan factor=3): [30, 30, 30]
Captura por defecto (1, 2 y 3): [10, 20, 30]
```

Diagnóstico: en `multiplicadores_erroneos`, la variable `factor` se consulta recién cuando se llama a `fn(10)`, instante en el que el bucle ya terminó con `factor == 3`. Solución: capturar el valor actual como valor por defecto (`lambda x, f=factor: x * f`), ya que los valores por defecto se evalúan en el momento exacto en que se crea cada función, o emplear `functools.partial`.

3. **Asignar una `lambda` a una variable perdiendo trazabilidad en errores (antipatrón PEP 8 E731).**

```python
operacion_anonima = lambda x: 100 / x


def operacion_nombrada(x: float) -> float:
    return 100 / x


print("Nombre interno con lambda:", operacion_anonima.__name__)
print("Nombre interno con def:", operacion_nombrada.__name__)
```

Resultado esperado:

```text
Nombre interno con lambda: <lambda>
Nombre interno con def: operacion_nombrada
```

Diagnóstico: cuando `operacion_anonima(0)` lanza `ZeroDivisionError` en un servidor con decenas de funciones similares, la traza de error solo reporta `in <lambda>`, ocultando qué regla falló. Solución: emplear siempre `def` cuando la función se guardará en un identificador con nombre.

4. **Reordenar repetidamente dentro de un bucle de inserción en lugar de hacerlo una sola vez al final.** Como ocurría en `EJERCICIO(1).py` (L18-27), invocar `compañeros.sort(key=lambda x: x[1])` dentro del `for` eleva innecesariamente el coste algorítmico a $O(n^2 \log n)$. La corrección aplicada en `Ejercicio_one.py` (L20) y `EJERCICOS(6).py` (L31) —agregar todos los elementos primero y ordenar una sola vez fuera del bucle— reduce el coste total a $O(n \log n)$.

## 9. Resumen

- Una expresión `lambda parametros: expresion` construye en línea un objeto `function` de primera clase sin necesidad de asignarle un identificador previo.
- Su cuerpo admite **únicamente una expresión** cuyo resultado se devuelve de forma automática; no permite `return`, bucles, `try` ni sentencias de asignación clásicas.
- Su uso idóneo son los argumentos de corta extensión para funciones de orden superior (`sorted`, `min`, `max`, `defaultdict` o *callbacks* puntuales).
- `filter()` y `map()` retornan **iteradores perezosos de un solo uso**; para transformaciones y filtrados en memoria, las comprensiones suelen ofrecer mayor legibilidad.
- **PEP 8** desaconseja asignar `lambda` a una variable (`f = lambda ...`); cuando una función merece un nombre o supera una expresión simple, debe declararse con `def`, y para extracciones puras de índices o atributos conviene preferir `operator.itemgetter` o `operator.attrgetter`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/LAMBDA_FUNCIONES.py` (L1-30, L43-100) | `LAMBDA_FUNCIONES.py` | Sintaxis `lambda x: x * 2`, retorno implícito, restricción a una instrucción y filtrado de pares/impares con `filter()` convirtiendo a `list` y `tuple` | Se contextualizó `multiplicar_por_dos = lambda ...` frente a **PEP 8 (E731)**, se sumó `map()` y se comparó con comprensiones |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L805, L826, L945, L957) | `CLASE_ONE.py` | Ordenamiento de diccionario por valor `sorted(agenda.items(), key=lambda item: item[1])` y paso directo `key=str` | Se explicó el patrón de función clave (`key`) y por qué `key=str` es preferible a envolver `str` en una `lambda` redundante |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(1).py` (L27) | `EJERCICIO(1).py` | Ordenamiento de tuplas `(nombre, edad)` mediante `compañeros.sort(key=lambda x: x[1])` | Se señaló el sobrecoste de invocar `.sort()` dentro del bucle `for` y cómo `min`/`max(..., key=...)` resuelven los extremos en $O(n)$ |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICOS(6).py` (L31) | `EJERCICOS(6).py` | Llamada única a `listado.sort(key=lambda x: x[1])` fuera del ciclo `while` | Contrastado con `EJERCICIO(1).py` para ilustrar la complejidad algorítmica correcta |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/REFACTORIZACION_EJERCICIOS/Ejercicio_one.py` (L20) | `Ejercicio_one.py` | Uso no destructivo `sorted(lista, key=lambda x: x[1])` preservando la lista original | Vinculado con la inmutabilidad y con la alternativa estándar `operator.itemgetter(1)` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(3).py` (L11-20) | `EJERCICIO(3).py` | Función `def fib(numero, veces):` basada en estado mutable y bucle `while` | Citado como contraejemplo estructural: los algoritmos iterativos con estado requieren `def` y no caben en una `lambda` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJERCICIOS_CLASS_TWO/EJERCICIO(3.2).py` (L10-20) | `EJERCICIO(3.2).py` | Función `def fibonacci(numero):` con bucle `for` y retorno condicional | Complementa el límite gramatical entre expresiones (`lambda`) y bloques de sentencias (`def`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Importando_con_pandas.py` (L49) | `Importando_con_pandas.py` | Limpieza condicional en línea `df.applymap(lambda x: x.replace('"', '').strip() if isinstance(x, str) else x)` | Se explicó el operador ternario dentro de `lambda`, su evolución a `DataFrame.map` y la preferencia por métodos vectorizados |

**Fundamento complementario:** se añadieron cuatro elementos esenciales para el dominio profesional del tema: (1) la identidad interna `"<lambda>"` en `__name__` y la recomendación normativa **PEP 8 (E731)**; (2) el ordenamiento multicriterio con tuplas de claves; (3) las funciones nativas `itemgetter` y `attrgetter` del módulo estándar `operator`; y (4) el diagnóstico y solución del problema de enlace tardío (*late binding*) al definir expresiones `lambda` dentro de bucles.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions> — Tutorial oficial de Python: introducción y usos idiomáticos de las expresiones `lambda`.
- <https://docs.python.org/3/reference/expressions.html#lambda> — Referencia del lenguaje: gramática formal y semántica de evaluación de `lambda`.
- <https://docs.python.org/3/howto/sorting.html> — Guía oficial (*Sorting HOW TO*): funciones `key`, ordenamiento multicriterio y uso de `operator.itemgetter` / `attrgetter`.
- <https://docs.python.org/3/library/operator.html> — Biblioteca estándar: módulo `operator` (`itemgetter`, `attrgetter`, `methodcaller`).
- <https://peps.python.org/pep-0008/#programming-recommendations> — PEP 8: recomendación oficial de utilizar `def` en lugar de asignar expresiones `lambda` a identificadores.
