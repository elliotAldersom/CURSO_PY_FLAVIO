# Conjuntos (`set` y `frozenset`) en Python

## 2. Introducción

Al trabajar con [listas](../../Basico/chapter-two/listas.md) y [tuplas](tuplas.md), cada elemento ocupa una posición numérica y un mismo valor puede aparecer tantas veces como se agregue: `["ana", "luis", "ana"]` conserva tres elementos. Sin embargo, numerosos problemas reales no giran en torno a la posición ni a la repetición, sino a la **pertenencia** y a la **unicidad**: saber qué correos únicos se registraron en un evento, comprobar instantáneamente si una contraseña incluye al menos un símbolo especial o determinar qué clientes compraron en enero pero no en febrero.

Un **conjunto** (`set`) en Python es una **colección mutable, no indexada y sin elementos duplicados**, inspirada directamente en la teoría matemática de conjuntos. Junto a él, Python ofrece su contraparte inmutable, **`frozenset`** ("conjunto congelado"), que conserva las mismas propiedades matemáticas pero impide añadir o retirar elementos tras su creación.

¿Qué problema resuelven dentro del lenguaje? Principalmente dos:

1. **Eliminación automática de duplicados y álgebra de colecciones:** permiten calcular uniones, intersecciones, diferencias y relaciones de inclusión en una sola expresión declarativa, sin escribir [bucles](../../Basico/chapter-two/bucles.md) anidados ni condicionales manuales.
2. **Búsqueda de pertenencia de alta velocidad:** verificar `elemento in lista` obliga a recorrer la lista posición por posición hasta encontrarlo (costo lineal respecto al tamaño). Un conjunto organiza sus elementos mediante una **tabla *hash***, lo que permite comprobar si un valor está presente casi de inmediato sin importar si la colección contiene diez o un millón de elementos.

Su importancia en Python radica en complementar a las secuencias: cuando el orden posicional carece de relevancia y lo prioritario es garantizar unicidad o consultar pertenencia repetidamente, `set` y `frozenset` constituyen la herramienta idónea del lenguaje.

## 3. Fundamentos y conceptos

**Unicidad y equivalencia de valores.** Un conjunto jamás almacena dos elementos iguales según el operador `==`. Si se construye `{10, 20, 10, 30}`, el resultado contiene únicamente `{10, 20, 30}`. Una regla sutil del lenguaje Python es que la igualdad numérica entre tipos compatibles también unifica entradas: dado que `1 == 1.0 == True` y los tres producen el mismo valor `hash()`, evaluar `{1, True, 1.0}` conserva solo el primer objeto insertado (`{1}`).

**El conjunto vacío y corrección al material original.** Los conjuntos con elementos se escriben entre llaves separados por comas, como `{"a", "b"}`. No obstante, escribir llaves vacías `{}` **no** crea un conjunto vacío, sino un [diccionario](diccionarios.md) vacío (por razones históricas del lenguaje, ya que los diccionarios existían en Python antes de incorporarse los conjuntos literales). Por ello, **la única forma de crear un conjunto vacío es invocar `set()`**. Asimismo, corresponde corregir una afirmación errónea de `CLASE_ONE.py` (L355-356), donde se señala que un conjunto vacío se imprime como `()`: en Python, `()` representa una [tupla](tuplas.md) vacía, mientras que la representación en texto de un conjunto sin elementos es siempre `set()`.

**Ausencia de índice posicional y orden de recorrido.** A diferencia de cadenas, listas y tuplas, los conjuntos **no son secuencias**: carecen de posiciones `0, 1, 2...`, por lo que `conjunto[0]` o el rebanado `conjunto[1:3]` lanzan `TypeError: 'set' object is not subscriptable`. Tampoco es posible recorrerlos indexando con `range(len(conjunto))`, como bien advierte `BUCLE_FOR.py` (L167-170); en su lugar se iteran directamente con `for elemento in conjunto:` o con `enumerate(conjunto)` cuando se requiere un contador externo de vuelta. Además, el lenguaje Python no garantiza orden de inserción en `set`: en **CPython**, la disposición depende de las ranuras de la tabla *hash* y, para cadenas de texto, de una semilla aleatoria por proceso (`PYTHONHASHSEED`, activa por defecto desde Python 3.3 por seguridad), lo que hace que el orden impreso de un conjunto de textos varíe entre ejecuciones.

**Requisito de elementos *hashables*.** Para ubicar cada miembro sin recorrer toda la colección, el conjunto calcula `hash(elemento)`. En consecuencia, **todo elemento introducido en un `set` o `frozenset` debe ser *hashable*** (inmutable en su valor de *hash*): se admiten números (`int`, `float`), booleanos, cadenas (`str`), [tuplas](tuplas.md) de elementos *hashables* y objetos `frozenset`. En cambio, intentar incluir una lista `[1, 2]`, un diccionario `{"a": 1}` u otro `set` mutable lanza inmediatamente `TypeError: unhashable type`.

**Diferencia entre `set` y `frozenset`.** Ambos tipos pertenecen a `builtins`:

- **`set`** es **mutable**: permite agregar (`add`) y quitar (`remove`, `discard`, `pop`, `clear`) elementos después de creado. Precisamente por ser mutable, un objeto `set` **no es *hashable*** y no puede guardarse dentro de otro `set` ni actuar como clave de diccionario.
- **`frozenset`** es **inmutable**: se construye con `frozenset(iterable)` (o `frozenset()` vacío) y bloquea toda modificación posterior. Gracias a esa inmutabilidad sí posee valor `hash()`, lo que permite crear conjuntos de conjuntos (`{frozenset([1, 2]), frozenset([3, 4])}`, tal como muestra `CLASS_TWO_SET.py` L23-25) o utilizarlo como clave en un diccionario (`CLASS_TWO_DICCIONARIOS.py` L50-57).

**Subconjunto (`<=`) frente a subconjunto propio (`<`).** Conviene precisar un matiz matemático que en `CLASS_TWO_SET.py` (L40-43 y L54-57) aparece tratado como equivalente:

- `A.issubset(B)` equivale al operador **`A <= B`** (subconjunto): devuelve `True` si todos los elementos de `A` están en `B`, **incluso cuando `A` y `B` son idénticos**.
- El operador **`A < B`** evalúa un **subconjunto propio** (*proper subset*): exige que `A <= B` **y además** `A != B` (`B` debe contener al menos un elemento adicional). De modo simétrico, `A.issuperset(B)` equivale a **`A >= B`**, mientras que **`A > B`** exige superconjunto propio.

**Operadores simbólicos frente a métodos con nombre.** Las operaciones algebraicas ofrecen dos sintaxis con una diferencia importante de flexibilidad: los operadores simbólicos (`|`, `&`, `-`, `^`, `<=`, `>=`) exigen que **ambos operandos sean conjuntos** (`set` o `frozenset`), mientras que los métodos equivalentes (`.union()`, `.intersection()`, `.difference()`, `.symmetric_difference()`, `.issubset()`, `.issuperset()`, `.isdisjoint()`) aceptan **cualquier iterable** como argumento (por ejemplo, una lista o una cadena), convirtiéndolo internamente al vuelo.

**Funcionamiento interno: lenguaje frente a CPython.** El lenguaje Python define únicamente el contrato de unicidad y las operaciones de conjunto. En la implementación **CPython**, `set` y `frozenset` se construyen sobre la estructura `PySetObject`, una tabla *hash* de direccionamiento abierto que almacena cada referencia junto con su entero de *hash* precalculado. Gracias a este diseño de **CPython**, la consulta `x in conjunto`, la inserción y el borrado operan en tiempo promedio constante **`O(1)`** (con peor caso teórico `O(n)` ante colisiones masivas de *hash*), a cambio de un consumo de memoria ligeramente mayor que el de una lista o tupla del mismo tamaño debido a las casillas libres de la tabla.

## 4. Sintaxis y funcionamiento

Formas de creación y consulta elemental:

```text
conjunto_vacio = set()
conjunto_literal = {<elem1>, <elem2>, ...}
conjunto_desde_iterable = set(<iterable>)
congelado = frozenset(<iterable>)
pertenece = <elem> in <conjunto>
```

Operaciones algebraicas entre conjuntos (devuelven un conjunto nuevo o un booleano sin alterar los originales):

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `a \| b` / `a.union(b)` | **Unión**: elementos presentes en `a`, en `b` o en ambos | `{1, 2} \| {2, 3}` → `{1, 2, 3}` |
| 2 | `a & b` / `a.intersection(b)` | **Intersección**: elementos comunes a `a` y `b` | `{1, 2} & {2, 3}` → `{2}` |
| 3 | `a - b` / `a.difference(b)` | **Diferencia**: elementos de `a` que **no** están en `b` | `{1, 2, 3} - {2}` → `{1, 3}` |
| 4 | `a ^ b` / `a.symmetric_difference(b)` | **Diferencia simétrica**: elementos exclusivos de uno u otro, no comunes | `{1, 2} ^ {2, 3}` → `{1, 3}` |
| 5 | `a <= b` / `a.issubset(b)` | **Subconjunto**: `True` si todo miembro de `a` pertenece a `b` | `{1, 2} <= {1, 2}` → `True` |
| 6 | `a < b` | **Subconjunto propio**: `True` si `a <= b` y `a != b` | `{1} < {1, 2}` → `True` |
| 7 | `a >= b` / `a.issuperset(b)` | **Superconjunto**: `True` si `a` contiene todos los miembros de `b` | `{1, 2} >= {1}` → `True` |
| 8 | `a > b` | **Superconjunto propio**: `True` si `a >= b` y `a != b` | `{1, 2} > {1, 2}` → `False` |
| 9 | `a.isdisjoint(b)` | **Disjuntos**: `True` si la intersección entre `a` y `b` es vacía | `{1, 2}.isdisjoint({3, 4})` → `True` |

Métodos exclusivos de modificación sobre `set` (mutan el conjunto en el lugar y devuelven `None`, salvo `pop()`):

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `s.add(x)` | Inserta el elemento `x`; si ya existía, no produce cambios | `s.add(10)` |
| 2 | `s.update(iterable)` | Agrega todos los elementos de uno o varios iterables (equivale a `\|=`) | `s.update([20, 30])` |
| 3 | `s.remove(x)` | Elimina `x` del conjunto; si **no existe**, lanza `KeyError` | `s.remove(10)` |
| 4 | `s.discard(x)` | Elimina `x` si está presente; si **no existe**, no lanza error | `s.discard(99)` |
| 5 | `s.pop()` | Retira y **devuelve** un elemento arbitrario; lanza `KeyError` si está vacío | `extraido = s.pop()` |
| 6 | `s.clear()` | Elimina todos los elementos, dejando `set()` | `s.clear()` |
| 7 | `s.copy()` | Devuelve una copia superficial independiente del conjunto | `copia = s.copy()` |

Funcionamiento al combinar tipos: cuando se opera entre un `set` y un `frozenset` (por ejemplo `s | f` o `f | s`), Python construye el conjunto resultante adoptando **el tipo del operando izquierdo**: `set(...) | frozenset(...)` produce un `set`, mientras que `frozenset(...) | set(...)` produce un `frozenset`.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación, eliminación de duplicados y diferencia frente a `{}`.**

```python
vacio_conjunto = set()
vacio_diccionario = {}
codigos = {101, 102, 101, 103, 102}
letras_unicas = set("banana")

print(vacio_conjunto, type(vacio_conjunto))
print(type(vacio_diccionario))
print(codigos, len(codigos))
print(sorted(letras_unicas))
```

Explicación línea por línea:

- Líneas 1-2: contrastan la creación del conjunto vacío con `set()` frente al literal `{}`, que construye un diccionario.
- Línea 3: el literal `{101, 102, 101, 103, 102}` descarta automáticamente las repeticiones de `101` y `102`.
- Línea 4: `set("banana")` recorre carácter por carácter la cadena y retiene solo las letras distintas (`'a'`, `'b'`, `'n'`).
- Línea 6: muestra cómo Python representa el conjunto vacío (`set()`) junto con su clase `<class 'set'>`.
- Línea 7: confirma que `{}` pertenece a `<class 'dict'>`.
- Línea 8: imprime los tres códigos únicos y su longitud `3`.
- Línea 9: emplea `sorted(...)` para mostrar las letras únicas en una lista ordenada alfabéticamente, independizando la salida de la semilla aleatoria de *hash* sobre textos.

Resultado esperado:

```text
set() <class 'set'>
<class 'dict'>
{101, 102, 103} 3
['a', 'b', 'n']
```

**Ejemplo 2 — Modificación segura e insegura: `add`, `update`, `remove` y `discard`.**

```python
permisos = {"lectura"}
permisos.add("escritura")
permisos.update(["auditoria", "lectura"])
permisos.remove("escritura")
permisos.discard("administracion")

print(sorted(permisos))
print("lectura" in permisos)
```

Explicación línea por línea:

- Línea 1: se inicializa un conjunto con un único permiso.
- Línea 2: `add("escritura")` incorpora un elemento individual.
- Línea 3: `update([...])` añade los elementos de la lista; `"lectura"` ya estaba presente, por lo que no se duplica.
- Línea 4: `remove("escritura")` retira un valor cuya existencia es conocida.
- Línea 5: `discard("administracion")` intenta retirar un permiso inexistente sin interrumpir el programa con `KeyError`.
- Líneas 7-8: se presenta el estado final ordenado y se verifica en tiempo promedio constante que `"lectura"` permanece activo (`True`).

Resultado esperado:

```text
['auditoria', 'lectura']
True
```

### Intermedio

**Ejemplo 3 — Álgebra de conjuntos para conciliar asistentes entre dos talleres.**

```python
taller_python = {"Ana", "Luis", "Marta", "Diego"}
taller_datos = {"Marta", "Diego", "Elena", "Sofía"}

ambos_talleres = taller_python & taller_datos
todos_los_inscritos = taller_python | taller_datos
solo_python = taller_python - taller_datos
un_solo_taller = taller_python ^ taller_datos

print("En ambos:", sorted(ambos_talleres))
print("Total único:", len(todos_los_inscritos))
print("Solo Python:", sorted(solo_python))
print("Exactamente uno:", sorted(un_solo_taller))
```

Explicación de las decisiones tomadas:

- Resolver estas cuatro consultas únicamente con listas exigiría varios bucles `for` con condiciones `in` y `not in`, propensos a duplicados si la entrada no estuviera depurada.
- La intersección (`&`) aísla a quienes asistieron a los dos talleres; la unión (`|`) consolida el padrón total sin contar dos veces a `"Marta"` ni a `"Diego"`.
- La diferencia asimétrica (`taller_python - taller_datos`) conserva únicamente a quienes estuvieron en el primero y faltaron al segundo, mientras que la diferencia simétrica (`^`) reúne a quienes asistieron exclusivamente a uno de los dos.

Resultado esperado:

```text
En ambos: ['Diego', 'Marta']
Total único: 6
Solo Python: ['Ana', 'Luis']
Exactamente uno: ['Ana', 'Elena', 'Luis', 'Sofía']
```

**Ejemplo 4 — Validación de símbolos en contraseñas con intersección e `isdisjoint()`.**

```python
simbolos_requeridos = {"!", "@", "#", "$", "%", "&", "*"}
candidatas = ["ClaveSimple123", "Segura@2025!"]

for clave in candidatas:
    caracteres_clave = set(clave)
    tiene_simbolo = not caracteres_clave.isdisjoint(simbolos_requeridos)
    encontrados = sorted(caracteres_clave & simbolos_requeridos)
    print(f"{clave} -> válida={tiene_simbolo}, símbolos={encontrados}")
```

Explicación de las decisiones tomadas:

- Este patrón integra las dos variantes vistas en el material original (`CLASE_ONE.py` L339-353 con `&`, y `contraseña_2.py` / `REGISTRO_CONTRA.py` con `isdisjoint()`).
- `not caracteres_clave.isdisjoint(simbolos_requeridos)` es idiomático cuando solo interesa la respuesta booleana ("¿comparten al menos un carácter?"), porque puede detenerse apenas halla la primera coincidencia sin construir un conjunto nuevo en memoria.
- Por su parte, `caracteres_clave & simbolos_requeridos` sí construye el conjunto de coincidencias, útil cuando además se desea reportar cuáles fueron los símbolos detectados (`['!', '@']`). En lugar de comparar `== False` como hace el material original, se utiliza el operador lógico `not` por claridad semántica.

Resultado esperado:

```text
ClaveSimple123 -> válida=False, símbolos=[]
Segura@2025! -> válida=True, símbolos=['!', '@']
```

### Avanzado

**Ejemplo 5 — Conjuntos anidados y control jerárquico de roles mediante `frozenset`.**

```python
rol_lector = frozenset(["leer_reportes"])
rol_editor = frozenset(["leer_reportes", "editar_articulos"])
rol_admin = frozenset(["leer_reportes", "editar_articulos", "borrar_usuarios"])

catalogo_roles = {rol_lector, rol_editor, rol_admin}
permisos_sesion = {"leer_reportes", "editar_articulos"}

print("Roles registrados en catálogo:", len(catalogo_roles))
print("Editor incluye a lector:", rol_lector < rol_editor)
print("Sesión cubre rol editor (<=):", rol_editor <= permisos_sesion)
print("Sesión supera estrictamente a editor (<):", rol_editor < permisos_sesion)
```

Explicación de rendimiento y mantenibilidad:

- Si cada rol se definiera como `set`, la línea `catalogo_roles = {rol_lector, ...}` fallaría con `TypeError: unhashable type: 'set'`. Al declararlos como `frozenset` (tal como introducen `CLASS_TWO_SET.py` y `EJM_SET.py`), cada perfil queda protegido contra alteraciones accidentales en tiempo de ejecución y se vuelve *hashable*, pudiendo almacenarse dentro de otro conjunto o indexar políticas en un diccionario.
- Las dos últimas comparaciones evidencian por qué distinguir `<=` de `<` resulta crítico en sistemas de autorización: `rol_editor <= permisos_sesion` evalúa `True` porque el usuario posee exactamente los permisos exigidos por el rol editor, mientras que `rol_editor < permisos_sesion` evalúa `False` porque ambos conjuntos contienen los mismos elementos. Usar `<` por error en una validación de permisos rechazaría a usuarios que tienen el perfil exacto requerido.

Resultado esperado:

```text
Roles registrados en catálogo: 3
Editor incluye a lector: True
Sesión cubre rol editor (<=): True
Sesión supera estrictamente a editor (<): False
```

## 6. Aplicaciones en el mundo real

- **Control de acceso basado en roles y alcances (*RBAC / OAuth scopes*):** verificar en un servidor backend si el conjunto de permisos concedidos a un *token* es superconjunto (`>=`) de los permisos requeridos por un *endpoint*.
- **Depuración y limpieza de datos (*deduplication*):** eliminar identificadores de cliente, direcciones IP o etiquetas repetidas antes de ingerir lotes en bases de datos o canalizaciones analíticas.
- **Sistemas de filtrado y listas de bloqueo (*allowlists / blocklists*):** almacenar miles de dominios bloqueados, extensiones prohibidas o palabras vacías (*stopwords* en procesamiento de lenguaje natural) en un `set` o `frozenset` para consultar cada entrada en `O(1)` promedio.
- **Comparación de inventarios y sincronización de archivos:** dado el conjunto de archivos locales y el conjunto de archivos en un servidor remoto, `locales - remotos` determina qué archivos falta subir y `remotos - locales` cuáles falta descargar.
- **Grafos y redes sociales:** modelar vecinos de un nodo como conjuntos permite obtener amigos en común entre dos usuarios mediante una simple intersección `amigos_a & amigos_b`.

## 7. Uso en producción

- **Convertir listas de consulta repetida en conjuntos una sola vez:** si una función comprueba `if id_producto in productos_activos:` dentro de un bucle de `m` pedidos sobre una lista de `n` productos, el costo combinado asciende a `O(m * n)`. Convertir previamente `productos_activos = set(lista_productos)` (`O(n)`) reduce las `m` consultas posteriores a `O(m)` en promedio en **CPython**.
- **Conservar el orden al eliminar duplicados cuando la secuencia importa:** `list(set(datos))` elimina repetidos, pero **destruye el orden original** de aparición. En producción, cuando es necesario deduplicar preservando el orden exacto de llegada, el idioma estándar desde Python 3.7 es `list(dict.fromkeys(datos))` (explicado en [diccionarios](diccionarios.md)).
- **Usar `frozenset` para constantes de módulo:** igual que se prefieren tuplas frente a listas para secuencias fijas, declarar constantes de pertenencia como `ESTADOS_FINALES = frozenset({"entregado", "cancelado"})` ofrece consulta `O(1)` e impide que cualquier módulo importador altere el conjunto con `.add()` o `.clear()`.
- **Elegir `discard()` frente a `remove()` según la semántica del dominio:** si la ausencia del elemento constituye un estado normal e idempotente (por ejemplo, asegurar que una sesión ya no esté en el conjunto de conectados), usar `discard()` evita capturar excepciones innecesarias; si su ausencia revela un fallo lógico del programa, `remove()` visibiliza inmediatamente la anomalía mediante `KeyError`.

## 8. Errores comunes y recomendaciones

1. **Escribir `{}` esperando crear un conjunto vacío.**

```python
supuesto_conjunto = {}
print(type(supuesto_conjunto))
```

Resultado esperado:

```text
<class 'dict'>
```

Diagnóstico: `{}` instancia un diccionario vacío, por lo que llamar luego a `supuesto_conjunto.add(1)` fallará con `AttributeError: 'dict' object has no attribute 'add'`. Solución: inicializar siempre conjuntos vacíos con `set()`.

2. **Intentar acceder a un elemento por índice posicional.**

```python
# ERROR INTENCIONAL: TypeError porque los conjuntos no admiten indexación
vocales = {"a", "e", "i", "o", "u"}
primera = vocales[0]
```

Diagnóstico: lanza `TypeError: 'set' object is not subscriptable`. Los conjuntos carecen de posiciones secuenciales. Solución: iterar con `for`, comprobar pertenencia con `in` o convertir explícitamente con `sorted(vocales)` cuando se requiere una lista ordenada indexable.

3. **Incluir listas, diccionarios u otros `set` mutables como elementos.**

```python
# ERROR INTENCIONAL: TypeError al insertar una lista mutable dentro de un set
grupos = {[1, 2], [3, 4]}
```

Diagnóstico: lanza `TypeError: unhashable type: 'list'`. Un conjunto necesita que el *hash* de sus miembros sea invariante. Solución: representar colecciones internas con tipos inmutables: `{(1, 2), (3, 4)}` si el orden interno importa, o `{frozenset([1, 2]), frozenset([3, 4])}` si son subconjuntos sin orden.

4. **Invocar `remove()` sobre un elemento ausente o `pop()` sobre un conjunto vacío.**

```python
# ERROR INTENCIONAL: KeyError al eliminar con remove() un valor inexistente
activos = {10, 20}
activos.remove(99)
```

Diagnóstico: lanza `KeyError: 99`. A diferencia de `list.remove()` (que lanza `ValueError`), `set.remove()` lanza `KeyError` por su arquitectura interna de tabla *hash*. Solución: emplear `activos.discard(99)` cuando la ausencia no sea un error, o comprobar antes `if 99 in activos:`. Asimismo, evitar `s.pop()` creyendo que retira "el último" elemento: a diferencia de las listas, no recibe índice y extrae un elemento arbitrario según la tabla interna.

5. **Ocultar el tipo integrado `set` usándolo como nombre de variable.** En `CLASE_ONE.py` (L633) y `Ejm_Datos_Compuestos.py` (L25) aparece `set = {"hola", ...}`:

```python
# ERROR INTENCIONAL: TypeError al sobrescribir el constructor integrado 'set'
set = {1, 2, 3}
nuevo = set([4, 5])
```

Diagnóstico: lanza `TypeError: 'set' object is not callable` porque el nombre `set` dejó de apuntar al constructor integrado. Solución: emplear identificadores descriptivos (`conjunto`, `simbolos`, `usuarios_activos`).

## 9. Resumen

- Un **`set`** es una colección mutable, no ordenada posicionalmente y compuesta exclusivamente por elementos **únicos** y ***hashables***.
- El conjunto vacío se crea únicamente con `set()` (su representación impresa es `set()`, mientras que `{}` crea un diccionario vacío y `()` una tupla vacía).
- **`frozenset`** es la variante inmutable y *hashable* de `set`, apta para anidarse dentro de otros conjuntos o servir como clave de diccionario.
- El álgebra de conjuntos proporciona unión (`|` / `union`), intersección (`&` / `intersection`), diferencia (`-` / `difference`), diferencia simétrica (`^` / `symmetric_difference`), inclusión (`<=` / `issubset`, `<`, `>=` / `issuperset`, `>`) y disjunción (`isdisjoint`).
- Para modificar un `set` existen `add()`, `update()`, `remove()` (lanza `KeyError` si falta), `discard()` (silencioso si falta), `pop()` y `clear()`.
- En **CPython**, la estructura interna de tabla *hash* (`PySetObject`) permite resolver consultas de pertenencia `x in conjunto` en tiempo promedio `O(1)`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L143-151, L339-356, L633-639) | `CLASE_ONE.py` | Creación literal con llaves, unicidad, ausencia de índice, intersección `set(contrasena) & signos` y uso de `.join()` | Se corrigió la nota de las L355-356 aclarando que el conjunto vacío imprime `set()` y no `()`, y se advirtió sobre el sombreado `set = {...}` de la L633 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Datos_Compuestos.py` (L25-27) | `Ejm_Datos_Compuestos.py` | Contraste de `set` frente a listas, tuplas y diccionarios | Se precisó que `set` sí es mutable mediante métodos propios (`add`, `discard`), aunque no admita mutación por índice |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/contraseña_2.py` (L6-11) | `contraseña_2.py` | Validación de caracteres especiales en contraseñas con `set(registro)` e `isdisjoint(simbolos)` | Se integró y estilizó con `not ...isdisjoint(...)` en el Ejemplo 4 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASS_TWO_SET.py` (L1-78) | `CLASS_TWO_SET.py` | Constructor `set([...])`, anidamiento con `frozenset()`, `issubset()`, `<`, `issuperset()`, `>`, `isdisjoint()` e `intersection()` | Se distinguió con precisión matemática `<=` (`issubset`) frente a `<` (subconjunto propio), que el archivo trata como equivalentes |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/EJM_SET.py` (L1-22) | `EJM_SET.py` | Conversión a `frozenset`, conjuntos de conjuntos `{b, a_1}` y verificaciones jerárquicas | Sirvió de base para el modelado de roles inmutables del Ejemplo 5 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/REGISTRO_CONTRA.py` (L4, L10, L14) | `REGISTRO_CONTRA.py` | Validación interactiva de símbolos requeridos con `set([...])` e `isdisjoint()` | Se conectó con el uso en producción de listas de control de pertenencia rápida |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L143-171) | `BUCLE_FOR.py` | Iteración sobre conjuntos con `for`, `zip()` y `enumerate()`, explicando por qué `range(len(set))` no aplica | Se articuló con la ausencia de orden secuencial y la aleatorización de *hash* |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASE_TWO_DESEMPAQUETAMIENTO.py` (L43-73, L103-109) | `CLASE_TWO_DESEMPAQUETAMIENTO.py` | Práctica integrada de `set`, `frozenset` anidados y `frozenset` como claves de diccionario | Se vinculó formalmente con el requisito de *hashability* |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/REPASO(01).py` (L22-40, L75-83, L156-163) | `REPASO(01).py` | Repaso de `frozenset`, `intersection()`, `isdisjoint()` y recorrido con `enumerate()` | Consolidado en las tablas de operaciones de la sección 4 |

**Fundamento complementario:** el material original de `CLASES_PYTHON/` presenta la creación de conjuntos, `frozenset`, intersección, subconjuntos y disjunción, pero no aparece en `CLASS_PY_POO/` ni cubre el catálogo completo de operaciones y mutación. Se incorporaron como fundamento complementario: (1) unión (`|` / `union`), diferencia (`-` / `difference`) y diferencia simétrica (`^` / `symmetric_difference`); (2) los métodos de mutación de `set` (`add`, `update`, `remove` frente a `discard`, `pop`, `clear`); (3) la colisión por igualdad entre `1`, `1.0` y `True`; y (4) el análisis de complejidad promedio `O(1)` sobre `PySetObject` y la semilla `PYTHONHASHSEED` en **CPython**.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/datastructures.html#sets> — Tutorial oficial de Python: introducción a conjuntos, eliminación de duplicados y operaciones algebraicas.
- <https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset> — Referencia completa de la biblioteca estándar para `set` y `frozenset`, operadores frente a métodos y operaciones de mutación.
- <https://docs.python.org/3/reference/datamodel.html#object.__hash__> — Modelo de datos oficial: contrato de `__hash__()`, equivalencia con `__eq__()` y aleatorización de *hash* por proceso.
