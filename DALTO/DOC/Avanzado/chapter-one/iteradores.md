# Protocolo de Iteración, Iterables frente a Iteradores, Generadores (`yield`) e `itertools`

## 2. Introducción

En Python, una misma construcción sintáctica —`for elemento in origen:`— recorre de manera uniforme estructuras tan dispares como una lista en memoria, los caracteres de una cadena, las líneas de un archivo de varios gigabytes, los resultados diferidos de una expresión regular o un flujo infinito de sensores (`BUCLE_FOR.py` L3-36, `Polimorfismo.py` L104-116). Esta generalidad [polimórfica](../../Intermedio/chapter-five/polimorfismo.md) no depende de una jerarquía rígida de herencia, sino del **protocolo de iteración** formalizado en **PEP 234** y ampliado con los generadores en **PEP 255**.

Comprender cómo coopera este protocolo bajo el capó transforma la manera de diseñar software eficiente y escalable en Python por cuatro razones técnicas:

1. **Distinción exacta entre `Iterable` e `Iterator`:** evita errores sutiles de cursores agotados al diferenciar contenedores reutilizables respecto de flujos consumibles de pasada única.
2. **Desazucarado mecánico del bucle `for`:** revela cómo cooperan `iter()`, `next()`, [métodos especiales](metodos_especiales.md) (`__iter__`, `__next__`, `__getitem__`) y la señal de control `StopIteration`.
3. **Diseño limpio de colecciones personalizadas:** separa la estructura de datos del cursor de recorrido para soportar múltiples pasadas simultáneas y bucles anidados sin corromper el estado.
4. **Procesamiento perezoso (*lazy evaluation*) en memoria constante $O(1)$:** permite encadenar funciones generadoras con `yield`, expresiones generadoras y combinadores de `itertools` para transformar grandes volúmenes de datos sin materializar listas intermedias en RAM.

## 3. Fundamentos y conceptos

**Iterable frente a Iterador (`collections.abc.Iterable` vs `collections.abc.Iterator`).** Aunque en el lenguaje cotidiano suelen confundirse, el módulo estándar `collections.abc` y los comentarios iniciales de `BUCLE_FOR.py` (L32-35) distinguen dos roles estrictamente separados:

| Concepto | Contrato en el Modelo de Datos | Función asociada | Estado de recorrido y reutilización | Ejemplos representativos |
|---|---|---|---|---|
| **Iterable** | Implementa `__iter__(self)` devolviendo un **nuevo iterador** (o el protocolo secuencial heredado `__getitem__(0, 1, ...)` hasta `IndexError`) | `iter(obj)` | **Sin cursor propio; reutilizable** en múltiples bucles independientes y concurrentes | `list`, `tuple`, `str`, `dict`, `set`, `frozenset`, `range` |
| **Iterador** | Implementa **`__next__(self)`** (entrega el siguiente valor o lanza `StopIteration`) **y** **`__iter__(self)`** retornando `self` | `next(it)` | **Con estado mutable interno; pasada única** (*single-pass*): una vez agotado, queda vacío permanentemente | `iter([1, 2])`, `filter()`, `map()`, `zip()`, `enumerate()`, `re.finditer()`, archivos abiertos y generadores |

Todo **iterador** es automáticamente un **iterable** (porque implementa `__iter__` devolviendo `self`, lo que permite usarlo directamente en un `for`), pero **ninguna colección estándar (`list`, `dict`, `range`) es un iterador**: llamar a `next([1, 2, 3])` lanza `TypeError: 'list' object is not an iterator`. Conviene notar que `range(1_000_000)` tampoco es un iterador, sino una secuencia perezosa reutilizable: ocupa memoria constante calculando sus valores aritméticamente bajo demanda y produce un `range_iterator` nuevo cada vez que se le aplica `iter()`.

**Desazucarado interno del bucle `for` y protocolo secuencial heredado (`__getitem__`).** Cuando Python ejecuta un [bucle `for`](../../Basico/chapter-two/bucles.md) como `for animal in animales:` (`BUCLE_FOR.py` L45-47), traduce internamente la sentencia a una estructura equivalente a la siguiente:

```text
_iterador = iter(animales)          # Invoca type(animales).__iter__(animales)
while True:
    try:
        animal = next(_iterador)    # Invoca type(_iterador).__next__(_iterador)
    except StopIteration:
        break                       # Terminación normal y limpia del recorrido
    # Cuerpo del bucle for ...
```

Si el objeto pasado a `iter(obj)` no define `__iter__`, Python recurre como respaldo de compatibilidad al **protocolo secuencial clásico** mencionado en `BUCLE_FOR.py` (L21-22): construye un iterador interno que invoca `obj.__getitem__(0)`, `obj.__getitem__(1)`, `obj.__getitem__(2)` sucesivamente hasta capturar `IndexError`, convirtiéndolo en `StopIteration`. No obstante, toda clase moderna debe implementar explícitamente `__iter__` para ser reconocida por `isinstance(obj, collections.abc.Iterable)`.

**El escollo del agotamiento de pasada única (*single-pass exhaustion*).** En `LAMBDA_FUNCIONES.py` (L47-58, L82-83) se aplica `filter(par, listado)` y se convierte deliberadamente a `list(filtrado)` comentando que, de lo contrario, no podría recorrerse de nuevo. La razón exacta reside en la especificación de **PEP 234**: cuando un iterador alcanza el final de sus datos y lanza `StopIteration`, **debe continuar lanzando `StopIteration` en todas las llamadas posteriores**. Si una función recibe un iterador (`filter`, `zip`, un generador) y ejecuta primero `max(flujo)` y luego `sum(flujo)`, la segunda operación recibirá una secuencia vacía y devolverá `0` sin emitir advertencia ni error alguno.

**Arquitectura orientada a objetos: separación entre Contenedor (`Iterable`) y Cursor (`Iterator`).** Al diseñar una colección de dominio propia, un error clásico consiste en colocar `self._posicion = 0`, `__iter__(self): return self` y `__next__(self)` en la misma clase contenedora. Ese acoplamiento convierte a la colección en un objeto de un solo uso e inutiliza los bucles anidados (`for a in col: for b in col:`), ya que ambos bucles compiten por mutar el mismo `self._posicion`. La arquitectura correcta separa responsabilidades:

1. La clase **Contenedora** almacena los datos y define `__iter__(self)` devolviendo una **instancia nueva e independiente** del cursor (o delegando en una función generadora con `yield`).
2. La clase **Cursor** mantiene únicamente la referencia de lectura y su índice privado `_posicion`, implementando `__iter__(self) -> self` y `__next__(self)`.

**Funciones generadoras (`yield`, `yield from`) y expresiones generadoras en memoria $O(1)$.** Escribir una clase cursor explícita con `__iter__` y `__next__` requiere código ceremonial repetitivo. **PEP 255** introdujo la palabra clave **`yield`**: cualquier [función](../../Intermedio/chapter-two/funciones.md) cuyo cuerpo contenga `yield` deja de ser una función ordinaria y se compila como una **fábrica generadora**:

- Al llamarla (`flujo = producir_pares(limite)`), su cuerpo **no se ejecuta todavía**; retorna de inmediato un objeto `generator` que implementa el protocolo `Iterator` completo.
- En cada `next(flujo)`, la ejecución avanza hasta el siguiente `yield valor`, entrega `valor` al llamador y **congela su marco de pila** (*stack frame*: variables locales y puntero de instrucción) hasta que se solicite el elemento siguiente.
- Cuando la función termina o encuentra `return`, el generador lanza automáticamente `StopIteration`. Adicionalmente, **`yield from sub_iterable`** (**PEP 380**) delega de forma directa la producción en otro iterable o subgenerador sin escribir bucles intermedios manuales.

Este modelo extiende de forma natural las **expresiones generadoras** `(expresion for x in iterable)` presentes en el material original dentro de llamadas a `.join()` (`CLASE_ONE.py` L619, L629, L656, L660; `Juego.py` L167; `Decoradores_Multiples.py` L177) y estudiadas junto a las [comprensiones](../../Intermedio/chapter-one/comprensiones.md). Mientras una comprensión de lista `[transformar(x) for x in millon_datos]` reserva memoria $O(N)$ para alojar el millón de resultados a la vez, una expresión o función generadora procesa un elemento tras otro ocupando **memoria auxiliar constante $O(1)$**.

**Tuberías declarativas con `itertools`.** El módulo estándar `itertools` proporciona bloques constructivos implementados en C para operar sobre iteradores sin materializar listas: `itertools.islice(it, inicio, fin)` extrae una ventana acotada de un flujo potencialmente infinito; `itertools.chain.from_iterable(fuentes)` concatena múltiples flujos de forma perezosa; e `itertools.batched(it, n)` (incorporado en Python 3.12) agrupa elementos consecutivos en tuplas de tamaño `n`, ideal para inserciones por lotes en bases de datos o envíos paginados a APIs.

## 4. Sintaxis y funcionamiento

Comparación estructural entre un contenedor iterable con cursor explícito y su formulación concisa mediante generador `yield`:

```text
# A. Separación explícita Contenedor (Iterable) + Cursor (Iterator)
class CursorVentana:
    def __init__(self, datos: tuple[int, ...]) -> None:
        self._datos = datos
        self._indice = 0

    def __iter__(self) -> "CursorVentana":
        return self

    def __next__(self) -> int:
        if self._indice >= len(self._datos):
            raise StopIteration
        valor = self._datos[self._indice]
        self._indice += 1
        return valor

class ColeccionNumeros:
    def __init__(self, datos: list[int]) -> None:
        self._datos = tuple(datos)

    def __iter__(self) -> CursorVentana:
        return CursorVentana(self._datos)   # Cursor nuevo en cada recorrido

# B. Equivalente idiomático usando función generadora en __iter__
class ColeccionConcisa:
    def __init__(self, datos: list[int]) -> None:
        self._datos = tuple(datos)

    def __iter__(self):
        for elemento in self._datos:
            yield elemento
```

Elementos principales del protocolo de iteración y evaluación perezosa:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `iter(objeto)` | Obtiene un iterador invocando `__iter__` (o el respaldo secuencial `__getitem__`) | `it = iter([10, 20])` |
| 2 | `next(it[, defecto])` | Extrae el siguiente ítem con `__next__`; retorna `defecto` o lanza `StopIteration` al agotarse | `next(it, None)` |
| 3 | `StopIteration` | Señal estándar lanzada por `__next__` para indicar el agotamiento definitivo del flujo | `raise StopIteration` |
| 4 | `collections.abc.Iterable` | Clase base abstracta para verificar soporte de `__iter__` | `isinstance(x, Iterable)` |
| 5 | `collections.abc.Iterator` | Subtipo de `Iterable` que exige además `__next__` | `isinstance(x, Iterator)` |
| 6 | `yield valor` | Suspende una función generadora emitiendo `valor` y preservando sus variables locales | `yield registro_limpio` |
| 7 | `yield from sub_it` | Delega la iteración completa en un subiterable o subgenerador (**PEP 380**) | `yield from lote` |
| 8 | `(expr for x in it)` | Expresión generadora en línea de evaluación perezosa y memoria $O(1)$ | `sum(x * x for x in rango)` |
| 9 | `itertools.islice` / `batched` | Rebanado perezoso y agrupación en bloques de tamaño fijo (Python >= 3.12) | `batched(flujo, 100)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Desazucarado manual con `iter()` y `next()`, verificación con `collections.abc` y contraste entre iterable reutilizable e iterador agotable.**

```python
from collections.abc import Iterable, Iterator

valores = [10, 25, 40]
rango = range(1, 4)
pares_filtrados = filter(lambda n: n % 2 == 0, valores)

print(
    "lista  -> Iterable:", isinstance(valores, Iterable),
    "| Iterator:", isinstance(valores, Iterator),
)
print(
    "range  -> Iterable:", isinstance(rango, Iterable),
    "| Iterator:", isinstance(rango, Iterator),
)
print(
    "filter -> Iterable:", isinstance(pares_filtrados, Iterable),
    "| Iterator:", isinstance(pares_filtrados, Iterator),
)

# Simulación exacta de lo que ejecuta internamente un bucle 'for'
cursor = iter(valores)
recorrido_manual: list[int] = []
while True:
    try:
        recorrido_manual.append(next(cursor))
    except StopIteration:
        break

print("Recorrido manual con next():", recorrido_manual)
print("Valor centinela tras agotarse:", next(cursor, -1))

# Agotamiento en filter (Iterator) frente a reutilización en range (Iterable)
print("filter 1ª pasada:", list(pares_filtrados), "| 2ª pasada:", list(pares_filtrados))
print("range  1ª pasada:", list(rango), "| 2ª pasada:", list(rango))
```

Explicación paso a paso:

- Se comprueba formalmente lo expuesto en `BUCLE_FOR.py` (L24-35) y `LAMBDA_FUNCIONES.py` (L47-58): ni `list` ni `range` son iteradores (`Iterator` es `False`), por lo que pueden recorrerse indefinidamente; `filter`, en cambio, es un `Iterator` que produce `[10, 40]` en la primera pasada y `[]` en la segunda al quedar agotado.
- El segundo argumento opcional de `next(cursor, -1)` evita capturar `StopIteration` cuando se desea un valor centinela predeterminado ante el fin del flujo.

Resultado esperado:

```text
lista  -> Iterable: True | Iterator: False
range  -> Iterable: True | Iterator: False
filter -> Iterable: True | Iterator: True
Recorrido manual con next(): [10, 25, 40]
Valor centinela tras agotarse: -1
filter 1ª pasada: [10, 40] | 2ª pasada: []
range  1ª pasada: [1, 2, 3] | 2ª pasada: [1, 2, 3]
```

### Intermedio

**Ejemplo 2 — Colección de dominio personalizada con clase Cursor independiente compatible con pasadas sucesivas y bucles anidados.**

```python
from collections.abc import Iterator


class _CursorSecuenciaAritmetica(Iterator[int]):
    """Mantiene el estado de avance de un único recorrido activo."""

    def __init__(self, inicio: int, paso: int, cantidad: int) -> None:
        self._actual = inicio
        self._paso = paso
        self._restantes = cantidad

    def __iter__(self) -> "_CursorSecuenciaAritmetica":
        return self

    def __next__(self) -> int:
        if self._restantes <= 0:
            raise StopIteration
        valor = self._actual
        self._actual += self._paso
        self._restantes -= 1
        return valor


class SecuenciaAritmetica:
    """Contenedor Iterable inmutable y reutilizable."""

    def __init__(self, inicio: int, paso: int, cantidad: int) -> None:
        if cantidad < 0:
            raise ValueError("La cantidad de términos no puede ser negativa")
        self._inicio = inicio
        self._paso = paso
        self._cantidad = cantidad

    def __len__(self) -> int:
        return self._cantidad

    def __iter__(self) -> Iterator[int]:
        return _CursorSecuenciaAritmetica(self._inicio, self._paso, self._cantidad)


progresion = SecuenciaAritmetica(inicio=5, paso=10, cantidad=3)

primera_pasada = list(progresion)
segunda_pasada = list(progresion)
producto_cartesiano = [(a, b) for a in progresion for b in progresion if a != b]

print("1ª pasada:", primera_pasada, "| 2ª pasada:", segunda_pasada)
print("Pares distintos en bucle anidado:", producto_cartesiano)
```

Explicación técnica:

- Cada vez que `list(progresion)` o el bucle anidado invoca `iter(progresion)`, `SecuenciaAritmetica.__iter__` instancia un `_CursorSecuenciaAritmetica` independiente con su propio contador `_restantes`.
- Gracias a este desacoplamiento, el bucle interior `for b in progresion` avanza hasta agotarse sin alterar en absoluto la posición del bucle exterior `for a in progresion`.

Resultado esperado:

```text
1ª pasada: [5, 15, 25] | 2ª pasada: [5, 15, 25]
Pares distintos en bucle anidado: [(5, 15), (5, 25), (15, 5), (15, 25), (25, 5), (25, 15)]
```

### Avanzado

**Ejemplo 3 — Tubería perezosa en memoria $O(1)$ combinando funciones generadoras (`yield`, `yield from`), cortocircuito e `itertools` (`islice`, `batched`).**

```python
from collections.abc import Iterable, Iterator
from itertools import batched, islice


def unificar_fuentes(particiones: list[list[str]], estadisticas: dict[str, int]) -> Iterator[str]:
    """Emite líneas de múltiples particiones contabilizando cuántas se leyeron realmente."""
    def _leer_particion(lineas: list[str]) -> Iterator[str]:
        for linea in lineas:
            estadisticas["lineas_leidas"] += 1
            yield linea

    for particion in particiones:
        yield from _leer_particion(particion)


def filtrar_errores_criticos(lineas: Iterable[str]) -> Iterator[tuple[str, str]]:
    """Extrae pares (servicio, mensaje) únicamente para eventos ERROR."""
    for cruda in lineas:
        nivel, servicio, detalle = (parte.strip() for parte in cruda.split("|"))
        if nivel == "ERROR":
            yield (servicio, detalle)


particiones_log = [
    [
        "INFO  | auth  | Sesion iniciada",
        "ERROR | pagos | Timeout en pasarela",
        "ERROR | auth  | Token expirado",
    ],
    [
        "WARN  | cache | Memoria al 80%",
        "ERROR | db    | Conexion rechazada",
        "ERROR | api   | Payload invalido",
        "ERROR | cola  | Reintento agotado",
        "INFO  | salud | Latido OK",
    ],
]

metricas = {"lineas_leidas": 0}
flujo_unificado = unificar_fuentes(particiones_log, metricas)
flujo_errores = filtrar_errores_criticos(flujo_unificado)

# Tomamos solo los primeros 2 lotes de tamaño 2 (máximo 4 errores) sin leer el resto
primeros_lotes = list(islice(batched(flujo_errores, 2), 2))

print("Lotes procesados (2x2):", primeros_lotes)
print(
    f"Líneas leídas de origen: {metricas['lineas_leidas']} de "
    f"{sum(len(p) for p in particiones_log)} totales"
)
```

Explicación de arquitectura:

- Ni `unificar_fuentes` ni `filtrar_errores_criticos` construyen listas intermedias: los registros fluyen uno a uno bajo demanda desde el origen hasta `batched(..., 2)` e `islice(..., 2)`.
- En cuanto `islice` completa el segundo lote de 2 errores (alcanzando el cuarto `ERROR` en la línea 6 de 8), **detiene la extracción inmediatamente**: las líneas 7 y 8 jamás llegan a leerse (`Líneas leídas de origen: 6 de 8 totales`), demostrando la eficiencia computacional y espacial de la evaluación perezosa en flujos masivos.

Resultado esperado:

```text
Lotes procesados (2x2): [(('pagos', 'Timeout en pasarela'), ('auth', 'Token expirado')), (('db', 'Conexion rechazada'), ('api', 'Payload invalido'))]
Líneas leídas de origen: 6 de 8 totales
```

## 6. Aplicaciones en el mundo real

- **Ingesta ETL de archivos masivos (CSV, JSON Lines, registros de servidor):** recorrer un objeto archivo abierto (`with open(...) as f: for linea in f:`) emplea su iterador nativo línea por línea, procesando archivos de decenas de gigabytes con pocos megabytes de RAM.
- **Consumo transparente de APIs REST y GraphQL paginadas:** un generador cliente solicita la página `1`, emite sus elementos con `yield from respuesta["items"]` y solo realiza la petición HTTP de la página `2` si el consumidor sigue iterando.
- **Escrituras transaccionales por bloques en bases de datos:** agrupar un flujo de millones de filas mediante `itertools.batched(registros, 1000)` equilibra el uso de memoria y el rendimiento de red en sentencias `executemany` o `COPY`.
- **Análisis léxico y búsqueda de patrones sobre textos extensos:** `re.finditer(patron, texto)` (`Z-Conejo_De_Indias.py` L39-42) produce objetos `Match` perezosamente uno a uno, evitando reservar toda la lista en memoria como hace `re.findall()`.

## 7. Uso en producción

- **Anotar con precisión `Iterable[T]` frente a `Iterator[T]` en contratos públicos:** si una función necesita recorrer sus datos más de una vez (por ejemplo, calcular el promedio en una pasada y normalizar en otra), debe exigir `collections.abc.Sequence[T]` o `Collection[T]` (o materializar explícitamente si es pequeña) en lugar de `Iterable[T]`, ya que `Iterable[T]` admite iteradores agotables.
- **Gestionar deterministamente recursos abiertos dentro de generadores:** cuando una función generadora abre conexiones o cursores externos con `with`, si el consumidor interrumpe el bucle prematuramente con `break` sin agotar el generador, el cierre del bloque `with` podría demorarse hasta la recolección de basura en intérpretes no basados en conteo de referencias. En recursos críticos, conviene abrir el recurso fuera del generador o usar `contextlib.closing(generador)`.
- **Aprovechar expresiones generadoras directas en funciones reductoras:** al invocar `sum()`, `any()`, `all()`, `min()`, `max()` o `", ".join()`, debe pasarse la expresión generadora sin corchetes (`sum(x * x for x in datos)` como en `CLASE_ONE.py` L619), ahorrando la construcción y destrucción de una lista temporal innecesaria.
- **Preferir `re.finditer()` sobre `re.findall()` en grandes volúmenes de texto:** especialmente cuando solo interesa verificar las primeras coincidencias o acceder a las posiciones `.span()` sin duplicar subcadenas en RAM.

## 8. Errores comunes y recomendaciones

1. **Iterar dos veces sobre un iterador o generador asumiendo que conserva sus elementos.**

```python
# ERROR INTENCIONAL: agotamiento silencioso al reutilizar un objeto generador/iterador
importes_iva = (monto * 1.18 for monto in [100.0, 200.0, 300.0])

total = sum(importes_iva)               # Consume por completo el generador (708.0)
promedio_erroneo = sum(importes_iva) / 3  # Segunda lectura sobre iterador agotado: retorna 0.0
```

Diagnóstico: tal como advertía empíricamente `LAMBDA_FUNCIONES.py` (L48-58), un generador, `filter`, `map` o `zip` solo puede recorrerse una vez. Si el conjunto cabe cómodamente en memoria y requiere múltiples lecturas, debe materializarse en `tuple` o `list`; si es un flujo masivo, deben calcularse ambos agregados (suma y conteo) en una única pasada.

2. **Convertir un contenedor de dominio en su propio iterador (`def __iter__(self): return self`).**

```python
# ERROR INTENCIONAL: antipatrón de cursor acoplado en el propio contenedor
class CarritoDeUnSoloUso:
    def __init__(self, items: list[str]) -> None:
        self._items = items
        self._indice = 0

    def __iter__(self) -> "CarritoDeUnSoloUso":
        return self  # Error de diseño: comparte un único _indice y no se reinicia al terminar

    def __next__(self) -> str:
        if self._indice >= len(self._items):
            raise StopIteration
        item = self._items[self._indice]
        self._indice += 1
        return item


# Tras un primer 'for x in carrito:', cualquier recorrido posterior obtiene cero elementos
```

Diagnóstico: un contenedor nunca debe ser su propio iterador. La solución más limpia y concisa consiste en implementar `def __iter__(self): return iter(self._items)` o usar `yield from self._items`, produciendo un cursor independiente en cada llamada a `iter()`.

3. **Modificar el tamaño de un diccionario o conjunto mientras se itera sobre sus vistas.**

```python
# ERROR INTENCIONAL: mutación estructural de dict durante la iteración (RuntimeError)
sesiones = {"u1": False, "u2": True, "u3": False}

for usuario, activa in sesiones.items():
    if not activa:
        del sesiones[usuario]  # Lanza RuntimeError: dictionary changed size during iteration
```

Diagnóstico: los iteradores de `dict` y `set` vigilan la integridad estructural de la tabla hash subyacente y abortan con `RuntimeError` si se insertan o eliminan claves durante el recorrido. Recomendación: iterar sobre una instantánea estática (`for usuario, activa in list(sesiones.items()):`) o construir un nuevo diccionario filtrado por comprensión.

## 9. Resumen

- El **protocolo de iteración** desacopla los algoritmos de recorrido respecto de las estructuras de datos mediante dos interfaces de `collections.abc`: **`Iterable`** (`__iter__`, contenedor capaz de entregar cursores nuevos) e **`Iterator`** (`__iter__` retornando `self` más `__next__` lanzando `StopIteration`).
- Todo bucle **`for`** desazucara internamente en una llamada inicial a `iter()` seguida de invocaciones sucesivas a `next()` hasta capturar `StopIteration`, admitiendo como respaldo heredado clases con `__getitem__(0, 1, ...)`.
- Los **iteradores son flujos de pasada única**: una vez agotados devuelven secuencias vacías en lecturas posteriores, por lo que las colecciones personalizadas deben delegar su recorrido en cursores separados o en generadores para seguir siendo reutilizables.
- Las **funciones generadoras (`yield`, `yield from`)** y las **expresiones generadoras `(expr for x in it)`** producen iteradores de forma declarativa suspendiendo su estado local, permitiendo procesar flujos arbitrariamente grandes en **memoria constante $O(1)$**.
- El módulo estándar **`itertools`** (`islice`, `chain`, `batched`) complementa a los generadores proporcionando combinadores de alto rendimiento con cortocircuito automático.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L3-36, L67, L80, L110, L200-207) | `BUCLE_FOR.py` | Definición conceptual de iterables frente a iteradores (`iter()`, `next()`, `__iter__`, respaldo `__getitem__` desde índice 0) y uso de `zip()`, `range()`, `enumerate()` y `.items()` | Se formalizó la jerarquía `collections.abc.Iterable` vs `Iterator`, el desazucarado exacto del bucle `for` con `StopIteration` y la diferencia entre secuencias perezosas (`range`) e iteradores |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/LAMBDA_FUNCIONES.py` (L34-58, L82-99) | `LAMBDA_FUNCIONES.py` | Uso del iterador perezoso `filter()` y materialización explícita en `list(filtrado)` / `tuple(filtrar)` para evitar perder los elementos en recorridos posteriores | Se explicó rigurosamente el mecanismo de agotamiento de pasada única (*single-pass exhaustion*) definido en **PEP 234** |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Z-Conejo_De_Indias.py` (L31-42) | `Z-Conejo_De_Indias.py` | Contraste práctico entre `re.findall()` (lista materializada) y `re.finditer()` (iterador `callable_iterator` de objetos `Match`) | Se analizó la ventaja de complejidad espacial $O(1)$ de `re.finditer()` en procesamiento de grandes textos y registros |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L618-661) | `CLASE_ONE.py` | Expresiones generadoras pasadas directamente a `", ".join(str(x) for x in ...)` sobre listas, tuplas, conjuntos y diccionarios | Se conectaron las expresiones generadoras con las funciones generadoras basadas en `yield` y la optimización de memoria en funciones reductoras |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Polimorfismo.py` (L104-116) | `Polimorfismo.py` | Función polimórfica `Recorrer(coleccion)` operando sobre cualquier tipo iterable mediante *duck typing* | Se vinculó el polimorfismo estructural con la anotación estática `Iterable[T]` en interfaces profesionales |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L167, L482, L522) | `Juego.py` | Uso combinado de expresiones generadoras en `" \|\| ".join(...)` e iteradores `enumerate(lista_guerrero, 1)` | Se integró con patrones de transformación y paginación por lotes sin acoplamiento con consola |

**Fundamento complementario:** dado que los guiones originales utilizaban expresiones generadoras `(expr for x in it)` e iteradores nativos (`filter`, `zip`, `enumerate`, `re.finditer`) sin llegar a definir **funciones generadoras con `yield` / `yield from`** (**PEP 255** y **PEP 380**) ni clases personalizadas con `__iter__` y `__next__`, esta unidad incorporó como fundamento complementario esencial: (1) el diseño orientado a objetos separando contenedor `Iterable` y cursor `Iterator`; (2) la suspensión de marcos de pila mediante `yield` y delegación con `yield from`; y (3) la composición de tuberías en memoria constante $O(1)$ mediante el módulo estándar `itertools` (`islice`, `chain`, `batched`).

## 11. Referencias oficiales

- <https://docs.python.org/3/reference/datamodel.html#specialnames> — Referencia del lenguaje (*Special method names*): especificación de `__iter__`, `__next__`, generadores y protocolo secuencial `__getitem__`.
- <https://docs.python.org/3/tutorial/classes.html#iterators> — Tutorial oficial de Python (*Iterators*): mecánica interna de `for`, `iter()`, `next()` y `StopIteration`.
- <https://docs.python.org/3/tutorial/classes.html#generators> — Tutorial oficial de Python (*Generators* y *Generator Expressions*): creación de iteradores con `yield` y evaluación perezosa.
- <https://docs.python.org/3/library/itertools.html> — Biblioteca estándar (`itertools`): funciones generadoras de iteradores rápidos y eficientes en memoria (`islice`, `chain`, `batched`).
- <https://docs.python.org/3/library/collections.abc.html> — Biblioteca estándar (`collections.abc`): clases base abstractas `Iterable`, `Iterator` y `Generator`.
- <https://peps.python.org/pep-0234/> — PEP 234 (*Iterators*): diseño fundacional del protocolo unificado de iteración en Python.
- <https://peps.python.org/pep-0255/> — PEP 255 (*Simple Generators*): especificación original de funciones generadoras y la sentencia `yield`.
