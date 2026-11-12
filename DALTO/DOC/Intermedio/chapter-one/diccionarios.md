# Diccionarios (`dict`) en Python

## 2. Introducción

En las [listas](../../Basico/chapter-two/listas.md) y [tuplas](tuplas.md), localizar un dato exige recordar el número de casilla donde fue guardado (`usuario[0]` para el nombre, `usuario[2]` para la edad). Cuando un registro crece o cuando se desea buscar el teléfono de `"María"` entre diez mil contactos, depender de posiciones numéricas resulta frágil y lento. En la vida cotidiana y en la ingeniería de software, la información suele consultarse mediante un **identificador con significado propio**: un documento de identidad, un código de producto o el nombre de un campo.

Un **diccionario** (`dict`) es la estructura de **mapeo asociativo** (*mapping*) fundamental de Python: almacena pares formados por una **clave** (*key*) única y un **valor** (*value*) asociado, escritos entre llaves con dos puntos `{"nombre": "Flavio", "edad": 18}`. En lugar de pedir "el elemento en la posición `1`", el programa solicita directamente `diccionario["edad"]` y obtiene `18`.

¿Por qué existe y cuál es su importancia dentro de Python?

1. **Expresividad semántica:** el código se vuelve autodescriptivo (`factura["total"]` frente a `factura[4]`).
2. **Acceso directo en tiempo constante:** al igual que los [conjuntos](conjuntos.md), un diccionario emplea internamente una tabla *hash* sobre sus claves, por lo que recuperar, insertar o eliminar un registro tarda prácticamente lo mismo con diez entradas que con un millón.
3. **Pilar del propio lenguaje:** Python utiliza diccionarios en su núcleo para organizar variables globales, módulos y los atributos internos de objetos en programación orientada a objetos (accesibles mediante el diccionario especial `objeto.__dict__`, anticipo de [clases y objetos](../chapter-five/clases_y_objetos.md)). Asimismo, constituye la representación natural en Python de mensajes JSON utilizados en APIs web y servicios modernos.

## 3. Fundamentos y conceptos

**Pares clave-valor y reglas sobre claves frente a valores.** Cada entrada de un diccionario vincula `clave: valor` bajo dos reglas asimétricas del lenguaje:

- **Las claves deben ser únicas y *hashables*:** pueden actuar como claves cadenas (`str`), enteros (`int`), flotantes (`float`), booleanos, [tuplas](tuplas.md) compuestas solo por objetos *hashables* y conjuntos inmutables `frozenset` (como practica `CLASS_TWO_DICCIONARIOS.py` L34-68). Las listas, los `set` mutables y otros diccionarios están prohibidos como claves (`TypeError: unhashable type`). Si una clave se repite en un literal o se vuelve a asignar, **no se duplica**: sobrescribe el valor previo asociado a esa clave. Incluso valores numéricamente equivalentes colisionan en la misma clave: en `{1: "uno", True: "verdadero"}`, como `1 == True` y ambos comparten `hash`, el diccionario resultante es `{1: "verdadero"}` (conserva la primera clave insertada y reemplaza el valor).
- **Los valores no tienen restricciones:** pueden ser de cualquier tipo (mutables o inmutables, incluidas listas, conjuntos, objetos propios u otros diccionarios anidados) y pueden repetirse libremente entre distintas claves (`CLASE_ONE.py` L159).

**El diccionario vacío y corrección al material original.** A diferencia de los conjuntos, donde se requiere `set()`, **el literal `{}` sí crea directamente un diccionario vacío**, equivalente a invocar `dict()`. Corresponde rectificar aquí la nota de `CLASS_TWO_DICCIONARIOS.py` (L6) y `CLASE_TWO_DESEMPAQUETAMIENTO.py` (L10-13), donde se afirma que no es posible crear diccionarios vacíos con la forma literal `{}`: en Python, `{}` es la forma idiomática, directa y más rápida de instanciar un diccionario sin elementos.

**Preservación del orden de inserción: CPython frente al lenguaje Python.** Históricamente, los diccionarios de Python no conservaban el orden en que se agregaban sus claves. En **CPython 3.6** se rediseñó su estructura interna para ahorrar memoria y, como efecto derivado de esa implementación, las entradas quedaron ordenadas por inserción. A partir de **Python 3.7**, dicho comportamiento dejó de ser un detalle exclusivo de **CPython** y pasó a ser una **garantía oficial del lenguaje Python**: recorrer un diccionario entrega sus elementos en el orden exacto en que sus claves fueron insertadas por primera vez (sobrescribir el valor de una clave existente mantiene su posición original; borrarla y reinsertarla la envía al final). No obstante, la igualdad `d1 == d2` evalúa únicamente si ambos poseen los mismos pares `clave: valor`, sin importar el orden en que fueron insertados.

**Variantes de construcción (`{}`, `dict()` y `dict.fromkeys()`).**

- **Literal `{clave: valor}`:** acepta cualquier expresión *hashable* como clave.
- **Constructor `dict(...)`:** admite argumentos por nombre `dict(nombre="Flavio", edad=18)` siempre que las claves sean identificadores válidos de Python (cadenas sin espacios ni inicio numérico). Conviene notar la trampa observada en `EJM_DICT.py` (L7-9) y comentada en `REPASO(01).py` (L64): si existe una variable `t = ("nombre", "apellido")`, escribir `dict(t="Flavio")` **no** usa el contenido de `t`, sino literalmente la cadena `"t"` como clave. También acepta un iterable de pares `(clave, valor)`, como `dict([("a", 1), ("b", 2)])` o `dict(sorted(agenda.items()))`.
- **Método de clase `dict.fromkeys(iterable, valor=None)`:** recorre el primer argumento tomando cada elemento como clave y le asigna `valor` (`None` por defecto). Si se pasa una cadena como `"sol"`, recorre sus caracteres creando `{'s': None, 'o': None, 'l': None}`; para claves de palabras completas debe pasarse una colección como `["nombre", "edad"]` (`CLASS_TWO_DICCIONARIOS.py` L75-88). **Advertencia crítica:** si `valor` es un objeto mutable como `[]`, todas las claves apuntarán **a la misma lista en memoria** (véase la sección 8).

**Consulta directa `d[k]` frente a consulta segura `d.get(k, defecto)`.** Indexar con corchetes `d["clave"]` exige que la clave exista; de lo contrario detiene la ejecución lanzando `KeyError`. El método `d.get("clave", por_defecto)` devuelve el valor asociado si la clave existe y, si falta, devuelve `por_defecto` (`None` cuando se omite el segundo argumento) sin lanzar excepción. Para comprobar existencia sin extraer valor se utiliza `clave in d`, que inspecciona únicamente las claves en tiempo promedio `O(1)`.

**Objetos vista dinámicos (`keys()`, `values()`, `items()`).** En `CLASE_ONE.py` (L867) se comenta de manera informal que `keys()` "devuelve una lista". En Python 3, `.keys()`, `.values()` e `.items()` **no construyen listas independientes**, sino **vistas dinámicas** (`dict_keys`, `dict_values`, `dict_items`): objetos ligeros que no duplican los datos en memoria y que reflejan automáticamente cualquier alta o baja posterior sobre el diccionario. Si se necesita una instantánea estática o indexable por posición, se convierte explícitamente con `list(d.keys())`. Además, `d.keys()` y `d.items()` (cuando los valores son *hashables*) admiten operaciones de conjuntos como `&`, `|` y `-`.

**Fusión moderna en Python 3.9+ (`|` y `|=`).** Desde **Python 3.9** (PEP 584), el lenguaje incorporó el operador de unión `d1 | d2`, que devuelve un **diccionario nuevo** combinando ambos (si una clave se repite, prevalece el valor del operando derecho `d2`), y el operador de actualización en el sitio `d1 |= d2` (equivalente en efecto sobre claves a `d1.update(d2)`).

**Estructura interna compacta en CPython.** En la implementación **CPython** (`PyDictObject`), la tabla *hash* se divide en dos arreglos: un arreglo disperso muy pequeño de índices enteros (`dk_indices`) y una tabla densa (`dk_entries`) que guarda contiguamente `(hash, clave, valor)` en orden de llegada. Este diseño propio de **CPython** explica simultáneamente tres propiedades prácticas: búsqueda promedio **`O(1)`**, preservación natural del orden de inserción y menor consumo de memoria RAM frente a las tablas *hash* tradicionales.

## 4. Sintaxis y funcionamiento

Sintaxis esencial de creación, lectura, escritura y borrado:

```text
vacio = {}
registro = {<clave1>: <valor1>, <clave2>: <valor2>}
valor = registro[<clave>]
valor_seguro = registro.get(<clave>, <valor_por_defecto>)
registro[<clave>] = <nuevo_valor>
del registro[<clave>]
combinado = <dict1> | <dict2>
```

Formas de creación y operadores generales:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `{}` | Literal de diccionario vacío | `d = {}` |
| 2 | `{k: v, ...}` | Literal con pares `clave: valor` | `{"id": 10, "activo": True}` |
| 3 | `dict(k=v, ...)` | Constructor con argumentos por nombre (claves tipo cadena identificadora) | `dict(nombre="Ana", edad=20)` |
| 4 | `dict(pares)` | Constructor desde un iterable de pares `(clave, valor)` | `dict([("a", 1), ("b", 2)])` |
| 5 | `dict.fromkeys(it, v)` | Crea diccionario con claves de `it` e igual valor `v` (`None` por defecto) | `dict.fromkeys(["x", "y"], 0)` |
| 6 | `d[k]` | Lee el valor de `k` (lanza `KeyError` si falta); en asignación crea o sobrescribe | `d["edad"]` |
| 7 | `del d[k]` | Elimina el par asociado a `k`; lanza `KeyError` si `k` no existe | `del d["edad"]` |
| 8 | `k in d` | Comprueba si `k` existe entre las **claves** del diccionario (`O(1)` promedio) | `"id" in d` → `True` |
| 9 | `d1 \| d2` | Devuelve un **nuevo** diccionario fusionado; ante colisión gana `d2` (Python ≥ 3.9) | `{"a": 1} \| {"a": 9, "b": 2}` |
| 10 | `d1 \|= d2` | Actualiza `d1` en el lugar con los pares de `d2` (Python ≥ 3.9) | `d1 \|= {"b": 2}` |

Catálogo de métodos de consulta y modificación:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `d.get(k[, def])` | Devuelve `d[k]` si existe; en caso contrario devuelve `def` (`None` por omisión) | `d.get("pais", "Perú")` |
| 2 | `d.keys()` | Devuelve vista dinámica `dict_keys` con las claves | `list(d.keys())` |
| 3 | `d.values()` | Devuelve vista dinámica `dict_values` con los valores | `list(d.values())` |
| 4 | `d.items()` | Devuelve vista dinámica `dict_items` con tuplas `(clave, valor)` | `for k, v in d.items():` |
| 5 | `d.pop(k[, def])` | Elimina `k` y **devuelve** su valor; sin `def`, lanza `KeyError` si `k` falta | `extraido = d.pop("edad")` |
| 6 | `d.popitem()` | Elimina y devuelve el **último** par `(clave, valor)` insertado (LIFO desde 3.7) | `par = d.popitem()` |
| 7 | `d.setdefault(k, def)` | Si `k` existe devuelve su valor; si falta, inserta `k: def` y devuelve `def` | `d.setdefault("visitas", 0)` |
| 8 | `d.update(otro)` | Incorpora o sobrescribe pares desde otro diccionario, iterable de pares o `k=v` | `d.update({"activo": False})` |
| 9 | `d.clear()` | Vacía todas las entradas en el lugar y devuelve `None` | `d.clear()` |
| 10 | `d.copy()` | Devuelve una copia superficial independiente del diccionario | `respaldo = d.copy()` |

Funcionamiento en bucles y conversiones: iterar directamente `for x in d:` recorre **únicamente las claves** (equivale a `for x in d.keys():`); del mismo modo, `list(d)` o `", ".join(d)` operan sobre las claves (`CLASE_ONE.py` L652). Cuando se necesita acceder simultáneamente a clave y valor en cada iteración, se recorre `d.items()`.

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación, lectura segura frente a directa, actualización y borrado.**

```python
perfil = {"nombre": "Flavio", "edad": 18}
perfil["ciudad"] = "Lima"
perfil["edad"] = 19

print(perfil["nombre"])
print(perfil.get("telefono", "No registrado"))

edad_retirada = perfil.pop("edad")
del perfil["ciudad"]
print("Edad extraída:", edad_retirada)
print("Diccionario final:", perfil)
```

Explicación línea por línea:

- Línea 1: define un diccionario inicial con dos pares clave-valor.
- Línea 2: al asignar sobre una clave inexistente (`"ciudad"`), Python agrega la nueva entrada al final.
- Línea 3: al asignar sobre una clave ya existente (`"edad"`), sobrescribe su valor de `18` a `19` conservando su lugar.
- Línea 5: accede directamente a `"nombre"` sabiendo que la clave está presente.
- Línea 6: consulta `"telefono"` con `.get(..., "No registrado")`, evitando un `KeyError` ante el campo opcional faltante.
- Línea 8: `.pop("edad")` elimina la clave y retorna `19` para conservarlo en `edad_retirada`.
- Línea 9: `del perfil["ciudad"]` elimina el par directamente sin devolver su valor (`Keyword_del.py` L74).
- Líneas 10-11: muestran el dato recuperado y el diccionario reducido a `{'nombre': 'Flavio'}`.

Resultado esperado:

```text
Flavio
No registrado
Edad extraída: 19
Diccionario final: {'nombre': 'Flavio'}
```

**Ejemplo 2 — Vistas dinámicas (`keys`, `values`, `items`) y `dict.fromkeys()`.**

```python
inventario = dict.fromkeys(["teclado", "raton"], 0)
claves_vista = inventario.keys()

print("Antes de agregar:", list(claves_vista))
inventario["monitor"] = 5
print("Vista actualizada sola:", list(claves_vista))

for producto, stock in inventario.items():
    print(f"{producto}: {stock}")
```

Explicación línea por línea:

- Línea 1: `dict.fromkeys(["teclado", "raton"], 0)` inicializa ambas claves con el entero inmutable `0`.
- Línea 2: guarda la vista `inventario.keys()` en `claves_vista` **antes** de añadir `"monitor"`.
- Líneas 4-6: al insertar `inventario["monitor"] = 5`, `claves_vista` refleja automáticamente la tercera clave sin haber vuelto a llamar a `.keys()`, demostrando que es una vista viva y no una lista estática.
- Líneas 8-9: `.items()` entrega cada par `(producto, stock)` respetando el orden exacto de inserción.

Resultado esperado:

```text
Antes de agregar: ['teclado', 'raton']
Vista actualizada sola: ['teclado', 'raton', 'monitor']
teclado: 0
raton: 0
monitor: 5
```

### Intermedio

**Ejemplo 3 — Agrupación con `setdefault()`, fusión con `|` y ordenamiento por valor.**

```python
config_base = {"reintentos": 3, "tiempo_espera": 10, "modo": "desarrollo"}
config_produccion = {"modo": "produccion", "registro": "estricto"}
config_final = config_base | config_produccion
print("Configuración fusionada:", config_final)

ventas_vendedor = {"flavio": 120, "juan": 310, "maria": 95, "ana": 240}
ranking = dict(sorted(ventas_vendedor.items(), key=lambda par: par[1], reverse=True))
print("Ranking descendente:", ranking)
```

Explicación de las decisiones tomadas:

- `config_base | config_produccion` (Python ≥ 3.9) fusiona ambos diccionarios sin alterar `config_base`; en la clave repetida `"modo"` prevalece `"produccion"` por encontrarse a la derecha.
- En la segunda parte, siguiendo y ampliando el patrón de `CLASE_ONE.py` (L954-959), `ventas_vendedor.items()` expone los pares `(nombre, monto)`, `sorted(..., key=lambda par: par[1], reverse=True)` los ordena de mayor a menor según el segundo elemento de cada tupla (las funciones anónimas `lambda` se estudian en detalle en [funciones lambda](../chapter-two/funciones_lambda.md)) y `dict(...)` reconstruye un diccionario que conserva ese nuevo orden gracias a la garantía del lenguaje vigente desde Python 3.7.

Resultado esperado:

```text
Configuración fusionada: {'reintentos': 3, 'tiempo_espera': 10, 'modo': 'produccion', 'registro': 'estricto'}
Ranking descendente: {'juan': 310, 'ana': 240, 'flavio': 120, 'maria': 95}
```

**Ejemplo 4 — Historial estructurado de mensajes e indexación por claves compuestas.**

```python
mensajes = [
    {"rol": "system", "contenido": "Analizador numérico de polaridad"},
    {"rol": "user", "contenido": "Excelente servicio técnico"},
]
mensajes.append({"rol": "assistant", "contenido": "0.85"})

for entrada in mensajes:
    print(f"[{entrada['rol']}] -> {entrada['contenido']}")

permisos_ruta = {
    frozenset(["admin", "auditor"]): "acceso_total",
    frozenset(["invitado"]): "solo_lectura",
}
print("Nivel:", permisos_ruta[frozenset(["auditor", "admin"])])
```

Explicación de las decisiones tomadas:

- La primera sección modela de forma limpia y sin credenciales externas la estructura de conversación empleada en `Ejercicio-Final.py`: una lista ordenada de diccionarios homogéneos con claves `"rol"` y `"contenido"`, formato estándar de intercambio JSON en APIs conversacionales.
- La segunda sección retoma la técnica de `CLASS_TWO_DICCIONARIOS.py` (L48-68): usar un `frozenset` como clave permite consultar `frozenset(["auditor", "admin"])` sin importar el orden en que lleguen las etiquetas del conjunto, algo que ni siquiera una tupla haría automáticamente sin ordenarla antes.

Resultado esperado:

```text
[system] -> Analizador numérico de polaridad
[user] -> Excelente servicio técnico
[assistant] -> 0.85
Nivel: acceso_total
```

### Avanzado

**Ejemplo 5 — Agrupación eficiente por categoría e introspección del diccionario interno `__dict__`.**

```python
transacciones = [
    ("alimentacion", 45.0),
    ("transporte", 12.5),
    ("alimentacion", 30.0),
    ("salud", 80.0),
    ("transporte", 15.0),
]

agrupado = {}
for categoria, monto in transacciones:
    agrupado.setdefault(categoria, []).append(monto)

totales = {cat: sum(montos) for cat, montos in agrupado.items()}
print("Totales por categoría:", totales)


class Dispositivo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo


equipo = Dispositivo("Samsung", "S25")
print("Atributos en __dict__:", equipo.__dict__)
```

Explicación de rendimiento y mantenibilidad:

- `agrupado.setdefault(categoria, []).append(monto)` resuelve la acumulación de listas por clave en una sola búsqueda de tabla *hash* cuando la categoría ya existe, evitando escribir bloques condicionales repetitivos. Para volúmenes intensivos en producción también existe `collections.defaultdict(list)` en la **biblioteca estándar**.
- La línea `totales = {cat: sum(montos) ...}` construye un diccionario resumen mediante una comprensión de diccionario (desarrollada en [comprensiones](comprensiones.md)).
- Finalmente, la clase `Dispositivo` conecta `CLASES_PYTHON` con `CLASS_PY_POO` (`Clases_y_Objetos.py`, `Crear_Clase.py` L89 y `Herencia_Multiple.py` L81): cuando una instancia estándar asigna `self.marca = marca`, Python almacena ese atributo como un par `'marca': 'Samsung'` dentro del diccionario interno `equipo.__dict__`. Comprender los diccionarios equivale a comprender cómo Python gestiona los espacios de nombres de sus propios objetos.

Resultado esperado:

```text
Totales por categoría: {'alimentacion': 75.0, 'transporte': 27.5, 'salud': 80.0}
Atributos en __dict__: {'marca': 'Samsung', 'modelo': 'S25'}
```

## 6. Aplicaciones en el mundo real

- **APIs web, microservicios y serialización JSON:** todo objeto JSON recibido o enviado por un backend (FastAPI, Django, Flask, clientes HTTP) se traduce directamente a un diccionario `dict` en Python mediante el módulo estándar `json`.
- **Cachés en memoria e índices de búsqueda rápida:** indexar registros de base de datos por `id_usuario` o `codigo_sku` en un diccionario transforma búsquedas lineales repetidas en consultas instantáneas `O(1)`.
- **Conteo de frecuencias e histogramas:** contabilizar palabras en documentos, códigos de estado HTTP en archivos de registro (*logs*) o eventos por minuto.
- **Tablas de despacho (*dispatch tables*):** asociar nombres de comandos (`{"crear": crear_item, "borrar": borrar_item}`) directamente a funciones ejecutables reemplaza largas cadenas de `if / elif / else` por una búsqueda limpia.
- **Configuración jerárquica de aplicaciones:** archivos YAML, TOML (`tomllib`) o variables de entorno estructuradas se cargan en diccionarios anidados para parametrizar conexiones, puertos y banderas de funcionalidad.

## 7. Uso en producción

- **Distinguir `clave in d` frente a `if d.get(clave):` con valores falsos legítimos:** si un diccionario almacena `{"descuento": 0, "comentario": ""}`, evaluar `if d.get("descuento"):` dará `False` porque `0` es evaluado como falso en contexto booleano, tratando erróneamente el dato como ausente. Cuando se necesita saber si la clave existe independientemente de que su valor sea `0`, `False`, `""` o `[]`, se debe verificar `if "descuento" in d:` o comparar `if d.get("descuento") is not None:`.
- **Deduplicación preservando el orden de aparición:** dado que `dict` garantiza orden de inserción desde Python 3.7, `list(dict.fromkeys(secuencia))` constituye la técnica idiomática en producción para eliminar elementos repetidos conservando exactamente su primera posición original, superando a `list(set(secuencia))` cuando el orden importa.
- **No mutar claves de un diccionario mientras se lo itera:** agregar o eliminar claves dentro de `for k in d:` lanza `RuntimeError: dictionary changed size during iteration`. Si un proceso debe depurar claves durante el recorrido, debe iterar sobre una copia estática de las claves: `for k in list(d.keys()):`.
- **Alternativas especializadas en `collections` (biblioteca estándar):** para contadores de frecuencias conviene emplear `collections.Counter`; para inicialización automática de listas o conjuntos por clave, `collections.defaultdict`; y para superponer múltiples capas de configuración sin copiarlas, `collections.ChainMap`.

## 8. Errores comunes y recomendaciones

1. **Acceder con `d[clave]` a una clave ausente sin validación previa.**

```python
# ERROR INTENCIONAL: KeyError al indexar una clave que no existe en el diccionario
usuario = {"nombre": "Ana"}
print(usuario["correo"])
```

Diagnóstico: lanza `KeyError: 'correo'` y detiene el programa (`CLASE_ONE.py` L892). Solución: emplear `usuario.get("correo")` cuando la clave es opcional, o validar antes con `if "correo" in usuario:`.

2. **Trampa de referencia compartida al pasar un objeto mutable a `dict.fromkeys()`.**

```python
equipos = dict.fromkeys(["grupo_a", "grupo_b"], [])
equipos["grupo_a"].append("Elena")
print(equipos)
```

Resultado esperado:

```text
{'grupo_a': ['Elena'], 'grupo_b': ['Elena']}
```

Diagnóstico: `dict.fromkeys(...)` **no** crea una lista nueva por cada clave; asigna la misma referencia `[]` tanto a `"grupo_a"` como a `"grupo_b"`. Al mutar una, cambian todas. Solución: usar `fromkeys` únicamente con valores inmutables (`0`, `None`, `""`) y, cuando cada clave requiera su propia lista independiente, emplear una comprensión `{k: [] for k in ["grupo_a", "grupo_b"]}` (ver [comprensiones](comprensiones.md)).

3. **Intentar utilizar una lista o un `set` como clave.**

```python
# ERROR INTENCIONAL: TypeError porque list no es un tipo hashable
coordenadas = {[10, 20]: "punto_control"}
```

Diagnóstico: lanza `TypeError: unhashable type: 'list'`. Solución: convertir la clave a [tupla](tuplas.md) `{(10, 20): "punto_control"}` si importa el orden posicional, o a `frozenset` si importa el conjunto sin orden.

4. **Guardar el retorno de `clear()` o `update()` esperando el diccionario.** En `Métodos_Diccionarios.py` (L74-76) se escribe `limpiar = diccionario.clear()` y se imprime `limpiar`, obteniendo `None`:

```python
datos = {"a": 1}
resultado = datos.clear()
print(resultado, datos)
```

Resultado esperado:

```text
None {}
```

Diagnóstico: al igual que en las listas, los métodos que mutan toda la colección en el sitio (`clear`, `update`) devuelven `None`. Solución: invocar `datos.clear()` sin asignar su retorno e inspeccionar `datos`.

5. **Confundir `del d[k]` con vaciar el valor (`d[k] = None`).** Como muestra `Keyword_del.py` (L74-79), `d["d"] = None` conserva la clave `"d"` dentro del diccionario (`"d" in d` sigue siendo `True` y `len(d)` no disminuye), mientras que `del d["d"]` o `d.pop("d")` retiran completamente el par clave-valor. Asimismo, nunca debe nombrarse una variable como `dict` (`CLASE_ONE.py` L643), pues sombrea el constructor integrado `builtins.dict`.

## 9. Resumen

- Un **diccionario** (`dict`) asocia **claves únicas y *hashables*** con **valores arbitrarios** mediante una tabla *hash* con acceso promedio `O(1)`.
- El literal vacío es `{}` (equivalente a `dict()`); desde **Python 3.7**, el lenguaje garantiza oficialmente que los diccionarios preservan el **orden de inserción** de sus claves.
- `d[k]` recupera el valor o lanza `KeyError` si falta; `d.get(k, defecto)` permite consultas seguras con valor de respaldo.
- `.keys()`, `.values()` e `.items()` devuelven **vistas dinámicas** que reflejan cambios en tiempo real sin copiar memoria.
- Para insertar, extraer, combinar o limpiar entradas se dispone de `d[k] = v`, `del d[k]`, `pop()`, `popitem()`, `setdefault()`, `update()`, `clear()` y los operadores de fusión `|` y `|=` (Python ≥ 3.9).
- `dict.fromkeys()` solo debe recibir valores por defecto inmutables; en el modelo de objetos de Python, los atributos de instancia residen comúnmente en el diccionario interno `objeto.__dict__`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L153-163, L643-662, L865-964) | `CLASE_ONE.py` | Creación literal, valores duplicados, `.join()` sobre vistas, métodos `keys()`, `get()`, `clear()`, `pop()`, `items()`, `values()` y ordenación con `dict(sorted(agenda.items(), key=...))` | Se precisó que `keys()`, `values()` e `items()` devuelven vistas dinámicas y no listas (L867), y se advirtió sobre el sombreado `dict = {...}` (L643) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L71-80) | `Keyword_del.py` | Borrado de clave con `del dic['a']` frente a asignación de cadena vacía o `None` | Se contrastó semánticamente eliminar la entrada frente a mantener la clave con valor nulo en la sección 8 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Datos_Compuestos.py` (L30-39) | `Ejm_Datos_Compuestos.py` | Consulta por clave y sobrescritura `diccionario['nombre'] = "FLAVITO"` | Integrado en el Ejemplo 1 y en las reglas de mutación |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/MÉTODOS Y FUNCIONES/Métodos_Diccionarios.py` (L1-78) | `Métodos_Diccionarios.py` | Práctica guiada de `keys()`, `values()`, `get()`, `pop()`, `items()` y `clear()` | Se explicó por qué `limpiar = diccionario.clear()` (L74) almacena `None` en lugar de `{}` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L480-575) | `REPASO(02)_CLASS_ONE.py` | Repaso interactivo de los métodos principales de `dict` | Consolidado sin dependencia de `input()` en los ejemplos ejecutables |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASS_TWO_DICCIONARIOS.py` (L1-144) | `CLASS_TWO_DICCIONARIOS.py` | `dict(k=v)`, claves *hashables* con `tuple` y `frozenset`, `hash()`, `dict.fromkeys()`, alta/sobrescritura de claves y colecciones anidadas como valores | Se corrigió la afirmación de la L6 demostrando que `{}` sí crea un diccionario vacío, y se documentó el riesgo de pasar mutables a `fromkeys()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/EJEMPLOS_CLASE_TWO/EJM_DICT.py` (L1-26) | `EJM_DICT.py` | Contraste entre `dict(t=...)` con clave literal `'t'` y `{t[0]: ...}`, además de `frozenset` como clave | Se explicó el motivo sintáctico de los argumentos por palabra clave en `dict(...)` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L182-210) | `BUCLE_FOR.py` | Recorrido de claves con `for a in diccionario:` y de pares con `diccionario.items()` | Integrado con el desempaquetamiento directo `for k, v in d.items():` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASE_TWO_DESEMPAQUETAMIENTO.py` (L10-13, L75-127) | `CLASE_TWO_DESEMPAQUETAMIENTO.py` | Variantes de `dict`, claves tupla y `frozenset`, `dict.fromkeys()` | Se rectificó el comentario de las L10-13 sobre `{}` vacío |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/REPASO(01).py` (L1-8, L41-101, L165-177) | `REPASO(01).py` | Desempaquetamiento de `.values()`, nota sobre `dict(t1=name)` y `fromkeys()` sobre tuplas | Articulado en las secciones 3 y 4 |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clases_y_Objetos.py` (L135-159) | `Clases_y_Objetos.py` | Definición de atributos de instancia `self.marca`, `self.modelo`, `self.camara` | Se conectó en el Ejemplo 5 con el almacenamiento subyacente en `objeto.__dict__` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Crear_Clase.py` (L89-93) | `Crear_Clase.py` | Inspección explícita de `(roca_One.__dict__).items()` para recorrer los atributos de un objeto | Demuestra el vínculo directo entre diccionarios y el modelo de objetos de POO |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Herencia_Multiple.py` (L81-84) | `Herencia_Multiple.py` | Consulta de `(Juan.__dict__).items()` sobre una instancia con herencia | Refuerza el papel estructural de `dict` en clases e instancias |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L145-167) | `Juego.py` | Registro dinámico de resultados por categoría en `dicci` y formateo con `dicci.items()` | Contextualiza el uso de diccionarios para acumular reportes de dominio |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Ejercicio-Final.py` (L42, L66, L74-75) | `Ejercicio-Final.py` | Lista de diccionarios `{"role": ..., "content": ...}` e indexación `message["content"]` para una API externa | Inspiró el Ejemplo 4 sobre cargas tipo JSON sin exponer credenciales |

**Fundamento complementario:** se añadieron cuatro elementos esenciales para el dominio profesional de `dict`: (1) la evolución histórica del orden de inserción (optimización interna de **CPython 3.6** convertida en regla oficial del lenguaje en **Python 3.7**) y el diseño de tabla compacta `PyDictObject`; (2) los métodos `setdefault()`, `update()` y `popitem()`; (3) los operadores modernos de fusión `|` y `|=` incorporados en **Python 3.9** (PEP 584); y (4) la trampa de referencias mutables compartidas en `dict.fromkeys(claves, [])`.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/datastructures.html#dictionaries> — Tutorial oficial de Python: concepto de diccionario, operaciones básicas, constructores e iteración.
- <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict> — Referencia completa del tipo `dict`, garantías de orden de inserción (Python 3.7+) y operadores de unión `|` / `|=` (Python 3.9+).
- <https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects> — Especificación oficial de los objetos vista dinámicos (`dict_keys`, `dict_values`, `dict_items`).
- <https://peps.python.org/pep-0584/> — PEP 584 (*Add Union Operators To dict*): diseño y semántica de los operadores `|` y `|=` en diccionarios.
