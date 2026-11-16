# Recursividad, Casos Base y Gestión de la Pila de Ejecución

## 2. Introducción

En ciencias de la computación, la **recursividad** es una técnica de diseño algorítmico donde una [función](funciones.md) resuelve un problema subdividiéndolo en subproblemas más pequeños de la misma naturaleza, invocándose a sí misma de manera directa o indirecta hasta alcanzar una condición terminal elemental.

Frente a la computación puramente iterativa gobernada por [bucles](../../Basico/chapter-two/bucles.md) `for` o `while`, el enfoque recursivo proporciona soluciones declarativas elegantes y matemáticamente naturales para estructuras auto-similares: recorridos de árboles jerárquicos, análisis sintáctico de gramáticas formales, algoritmos de divide y vencerás (*divide and conquer*) y algoritmos de exploración exhaustiva (*backtracking*).

No obstante, en Python la recursividad no es una abstracción sin costo. El intérprete CPython no implementa optimización de llamada de cola (*Tail Call Optimization*, TCO) y mantiene un registro estricto en la pila de llamadas (*call stack*). Comprender el caso base, el progreso hacia el caso base, el límite de recursión (`sys.getrecursionlimit`) y la gestión de memoria resulta indispensable para evitar desbordamientos de pila (`RecursionError`) y diseñar software escalable.

## 3. Fundamentos y conceptos

**Anatomía de una función recursiva: caso base y caso inductivo.** Toda función recursiva correcta debe articular dos componentes indivisibles:

1. **Caso base (condición de parada):** es la instancia mínima del problema que puede resolverse de forma directa sin requerir nuevas llamadas recursivas. Sin este anclaje, la función incurriría en una recursión infinita hasta agotar la memoria de la pila.
2. **Caso recursivo (paso inductivo):** divide el problema en uno o más subproblemas estrictamente más cercanos al caso base y combina sus resultados. Cada llamada recursiva debe reducir el tamaño de los datos de entrada hacia la condición de parada.

**La pila de llamadas (*Call Stack*) y los marcos de activación (*Stack Frames*).** Cada vez que se invoca una función en Python, el entorno de ejecución aloja un **marco de activación (*frame*)** en la pila de memoria del intérprete. Dicho marco almacena:

- Los argumentos suministrados a la llamada.
- Las variables locales declaradas dentro del ámbito de la función.
- El puntero de retorno a la instrucción que debe ejecutarse cuando la función termine.

En una ejecución recursiva con profundidad $N$, existen simultáneamente $N$ marcos de activación apilados en memoria. La memoria espacial auxiliar consumida es proporcional a la profundidad máxima alcanzada: $O(N)$. Cuando la llamada más profunda alcanza el caso base, los marcos comienzan a resolverse y desapilarse en orden inverso (*LIFO: Last In, First Out*), propagando sus resultados hacia arriba.

**Límite de recursión en CPython y prevención de desbordamiento.** Para proteger el proceso del sistema operativo contra fallos de segmentación (*segfaults*) debidos a desbordamiento de la pila nativa en C, Python impone un límite de seguridad en la profundidad de la pila accesible mediante el módulo estándar `sys`:

- `sys.getrecursionlimit()`: consulta el número máximo permitido de marcos anidados (típicamente `1000` en entornos estándar).
- `sys.setrecursionlimit(limite)`: permite ajustar este umbral, aunque incrementarlo de forma indiscriminada puede provocar la terminación abrupta del proceso si se agota la pila del sistema operativo.
- Al exceder este límite, Python lanza de forma controlada la excepción integrada `RecursionError: maximum recursion depth exceeded`.

**Recursividad simple frente a recursividad múltiple y memoización.**
- **Recursividad lineal:** cada invocación genera a lo sumo una nueva llamada recursiva (p. ej., cálculo factorial o búsqueda binaria). Su complejidad temporal es $O(N)$ y su pila alcanza $O(N)$.
- **Recursividad de árbol (múltiple):** cada invocación genera dos o más llamadas recursivas (p. ej., la definición matemática ingenua de la sucesión de Fibonacci: $F(n) = F(n-1) + F(n-2)$). Sin optimizaciones, el árbol de llamadas experimenta un crecimiento exponencial $O(2^N)$ debido al recálculo redundante de los mismos subproblemas.
- **Memoización:** técnica de programación dinámica que almacena en caché los resultados de subproblemas previamente evaluados. En Python se implementa de manera transparente mediante el decorador de la biblioteca estándar `@functools.lru_cache` o `@functools.cache`, reduciendo la complejidad temporal de $O(2^N)$ a $O(N)$ lineal.

## 4. Sintaxis y funcionamiento

Estructura canónica de una función recursiva con tipado estático y validación defensiva:

```python
def algoritmo_recursivo(entrada: int) -> int:
    # 1. Validación defensiva de precondiciones
    if entrada < 0:
        raise ValueError("La entrada no puede ser negativa")

    # 2. Caso base (parada)
    if entrada == 0:
        return 1

    # 3. Caso recursivo (progreso hacia el caso base)
    return entrada * algoritmo_recursivo(entrada - 1)
```

Patrón de recorrido recursivo de estructuras jerárquicas (árboles o diccionarios anidados):

```python
from typing import Any


def recorrer_arbol(nodo: dict[str, Any]) -> None:
    # Procesar nodo actual
    print(f"Visitando: {nodo.get('nombre')}")

    # Paso recursivo sobre hijos
    hijos = nodo.get("hijos", [])
    for hijo in hijos:
        recorrer_arbol(hijo)
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Factorial matemático y suma acumulada con verificación de límites.**

```python
import sys


def factorial(n: int) -> int:
    """Calcula el factorial de n mediante recursividad lineal."""
    if not isinstance(n, int):
        raise TypeError(f"Se esperaba int, se obtuvo {type(n).__name__}")
    if n < 0:
        raise ValueError("El factorial no está definido para enteros negativos")

    # Caso base
    if n in (0, 1):
        return 1

    # Caso recursivo
    return n * factorial(n - 1)


def suma_recursiva(coleccion: list[int]) -> int:
    """Suma los elementos de una lista dividiendo la cabeza del resto."""
    # Caso base: lista vacía
    if not coleccion:
        return 0
    # Caso recursivo: primer elemento + suma recursiva del resto
    return coleccion[0] + suma_recursiva(coleccion[1:])


# Verificación de ejecución
limite_actual = sys.getrecursionlimit()
res_factorial = factorial(5)
res_suma = suma_recursiva([10, 20, 30, 40])

print("Límite de recursión del sistema:", limite_actual)
print("Factorial de 5                  :", res_factorial)
print("Suma recursiva                  :", res_suma)
```

Explicación paso a paso:

- `factorial(5)` apila llamadas descendentes: `5 * factorial(4)`, luego `4 * factorial(3)`, hasta `factorial(1)` que retorna `1`. A partir de allí, se desapilan los marcos resolviendo las multiplicaciones pendientes: `1 * 2 * 3 * 4 * 5 = 120`.
- `suma_recursiva` toma la cabeza `coleccion[0]` y avanza recursivamente consumiendo la rodaja `coleccion[1:]` hasta alcanzar la lista vacía (`[]`), devolviendo `0` y desapilando las adiciones.

Resultado esperado:

```text
Límite de recursión del sistema: 1000
Factorial de 5                  : 120
Suma recursiva                  : 100
```

### Intermedio

**Ejemplo 2 — Búsqueda binaria recursiva y aplanamiento de estructuras anidadas arbitrarias.**

```python
from typing import Any


def busqueda_binaria_recursiva(
    lista_ordenada: list[int], objetivo: int, inicio: int, fin: int
) -> int:
    """Retorna el índice del objetivo o -1 si no existe en el rango."""
    # Caso base: espacio de búsqueda agotado
    if inicio > fin:
        return -1

    medio = (inicio + fin) // 2
    valor_medio = lista_ordenada[medio]

    if valor_medio == objetivo:
        return medio
    elif objetivo < valor_medio:
        # Explorar mitad izquierda
        return busqueda_binaria_recursiva(lista_ordenada, objetivo, inicio, medio - 1)
    else:
        # Explorar mitad derecha
        return busqueda_binaria_recursiva(lista_ordenada, objetivo, medio + 1, fin)


def aplanar_estructura(datos: Any) -> list[Any]:
    """Aplana recursivamente listas y tuplas anidadas en una lista unidimensional."""
    resultado: list[Any] = []
    if isinstance(datos, (list, tuple)):
        for elemento in datos:
            resultado.extend(aplanar_estructura(elemento))
    else:
        resultado.append(datos)
    return resultado


datos_anidados = [1, [2, [3, 4], 5], [[6]], (7, 8)]
ordenados = [10, 25, 33, 47, 52, 68, 79, 91]

idx_33 = busqueda_binaria_recursiva(ordenados, 33, 0, len(ordenados) - 1)
idx_99 = busqueda_binaria_recursiva(ordenados, 99, 0, len(ordenados) - 1)
plano = aplanar_estructura(datos_anidados)

print("Índice de 33 encontrado :", idx_33)
print("Índice de 99 (ausente)  :", idx_99)
print("Estructura aplanada     :", plano)
```

Explicación técnica:

- La búsqueda binaria divide el espacio de búsqueda a la mitad en cada paso, logrando complejidad temporal logarítmica $O(\log n)$ y consumiendo únicamente $O(\log n)$ marcos de pila.
- `aplanar_estructura` utiliza recursividad estructural: si el elemento actual es una colección iterable ([listas](../../Basico/chapter-two/listas.md) o [tuplas](../chapter-one/tuplas.md)), delega recursivamente sobre cada componente; si es un valor atómico, lo almacena en el acumulador.

Resultado esperado:

```text
Índice de 33 encontrado : 2
Índice de 99 (ausente)  : -1
Estructura aplanada     : [1, 2, 3, 4, 5, 6, 7, 8]
```

### Avanzado

**Ejemplo 3 — Recorrido de sistema de archivos jerárquico con `pathlib.Path` y memoización de estados con `@functools.lru_cache`.**

```python
import functools
import tempfile
from pathlib import Path


@functools.lru_cache(maxsize=128)
def particiones_monedas(objetivo: int, denominaciones: tuple[int, ...]) -> int:
    """Calcula cuántas combinaciones de monedas suman el objetivo exacto (con memoización)."""
    # Casos base
    if objetivo == 0:
        return 1
    if objetivo < 0 or not denominaciones:
        return 0

    moneda_actual = denominaciones[0]
    resto_monedas = denominaciones[1:]

    # Usar la moneda actual + no usar la moneda actual
    con_moneda = particiones_monedas(objetivo - moneda_actual, denominaciones)
    sin_moneda = particiones_monedas(objetivo, resto_monedas)

    return con_moneda + sin_moneda


def listar_arbol_directorios(ruta_raiz: Path, prefijo: str = "") -> list[str]:
    """Genera una representación visual jerárquica del árbol de directorios recursivamente."""
    lineas: list[str] = []
    if not ruta_raiz.exists():
        return lineas

    elementos = sorted(ruta_raiz.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    total = len(elementos)

    for i, elemento in enumerate(elementos):
        es_ultimo = i == (total - 1)
        conector = "└── " if es_ultimo else "├── "
        lineas.append(f"{prefijo}{conector}{elemento.name}")

        if elemento.is_dir():
            extension_prefijo = "    " if es_ultimo else "│   "
            lineas.extend(listar_arbol_directorios(elemento, prefijo + extension_prefijo))

    return lineas


# Demostración práctica
formas_de_cambio = particiones_monedas(50, (25, 10, 5, 1))

with tempfile.TemporaryDirectory() as temp_dir:
    raiz = Path(temp_dir)
    (raiz / "src" / "api").mkdir(parents=True)
    (raiz / "src" / "models").mkdir(parents=True)
    (raiz / "src" / "main.py").touch()
    (raiz / "tests").mkdir()
    (raiz / "tests" / "test_api.py").touch()

    arbol_visual = listar_arbol_directorios(raiz)

print("Combinaciones para sumar 50 centavos:", formas_de_cambio)
print("Estructura de árbol generada:")
for linea in arbol_visual:
    print(linea)
```

Explicación de ingeniería:

- La función `particiones_monedas` modela el problema de cambio de moneda mediante recursividad de árbol. Sin memoización, calcular el valor requeriría decenas de miles de llamadas duplicadas; al aplicar `@functools.lru_cache`, Python almacena en memoria los resultados de cada par `(objetivo, denominaciones)`, convirtiendo una complejidad exponencial en cuadrática y resolviendo la consulta en milisegundos.
- `listar_arbol_directorios` recorre estructuras jerárquicas arbitrarias de disco utilizando [pathlib.Path](../chapter-three/manejo_archivos.md). Ordena primero los directorios y luego los archivos, construyendo los conectores gráficos de árbol (`├──`, `└──`) y profundizando recursivamente en cada subdirectorio con el prefijo identado correspondiente.

Resultado esperado:

```text
Combinaciones para sumar 50 centavos: 49
Estructura de árbol generada:
├── src
│   ├── api
│   ├── models
│   └── main.py
└── tests
    └── test_api.py
```

## 6. Aplicaciones en el mundo real

- **Recorrido y manipulación de estructuras jerárquicas:** navegación de árboles DOM en HTML/XML, análisis sintáctico de árboles de sintaxis abstracta (*AST*) en compiladores e introspección de esquemas JSON/YAML anidados arbitrariamente.
- **Sistemas de archivos y gestión de almacenamiento:** eliminación recursiva segura de directorios, búsqueda en profundidad de archivos por extensión y sincronización de carpetas distribuidas.
- **Algoritmos clásicos de grafos y optimización combinatoria:** búsqueda en profundidad (*DFS*, *Depth-First Search*), detección de ciclos, ordenamiento topológico y resolución de laberintos o juegos mediante *backtracking*.
- **Algoritmos de ordenamiento y partición de alto rendimiento:** implementación formal de *MergeSort* y *QuickSort*, que dividen recurrentemente arreglos hasta alcanzar listas triviales de longitud cero o uno.
- **Resolución de gramáticas y lenguajes formales:** evaluadores de expresiones aritméticas con paréntesis y analizadores léxicos descendentes recursivos (*recursive descent parsers*).

## 7. Uso en producción

- **Preferir iteración cuando la profundidad de entrada sea impredecible o masiva:** debido a la ausencia de TCO en CPython y al límite por defecto de 1000 marcos, algoritmos lineales sobre colecciones de gran tamaño (como recorrer una lista enlazada o un flujo de $100\,000$ elementos) deben implementarse mediante un bucle iterativo ordinario o con una pila explícita en memoria heap (`list.append` y `list.pop`).
- **Blindar funciones recursivas con memoización:** toda función recursiva que calcule subproblemas superpuestos (algoritmos matemáticos, particiones, planificación) debe protegerse con `@functools.lru_cache(maxsize=...)` para prevenir explosiones combinatorias de tiempo y desbordamientos evitables de pila.
- **Validar precondiciones antes de iniciar la cadena recursiva:** comprobar tipos y rangos numéricos al inicio previene que valores fuera de dominio (como números negativos en factoriales o flotantes) eludan el caso base y desencadenen llamadas infinitas.
- **Medir el consumo de memoria en arquitecturas críticas:** recordar que cada marco de activación en CPython reserva espacio en la memoria de la pila nativa; monitorizar la profundidad máxima con métricas o pruebas de carga evita caídas imprevistas por desbordamiento de pila en servicios web concurrentes.

## 8. Errores comunes y recomendaciones

1. **Olvidar el caso base o escribir una condición inalcanzable (`RecursionError`).**

```python
# ERROR: la condición de parada decrementa saltando el caso base
def conteo_defectuoso(n: int) -> None:
    if n == 0:
        return
    conteo_defectuoso(n - 2)


# conteo_defectuoso(5) llamará con 3, 1, -1, -3... hasta colapsar la pila:
# RecursionError: maximum recursion depth exceeded while calling a Python object
```

Diagnóstico: cuando la entrada inicial es un número impar (`5`), restar de a 2 nunca iguala exactamente a `0`, cruzando hacia los negativos de forma indefinida. Recomendación: utilizar operadores de desigualdad (`if n <= 0: return`) para capturar casos de borde y saltos imprevistos.

2. **Copiar colecciones masivas en cada llamada mediante slicing (`lista[1:]`).**

```python
# ANTIPATRÓN: genera una copia física de la lista en cada marco de llamada
def suma_ineficiente(elementos: list[int]) -> int:
    if not elementos:
        return 0
    return elementos[0] + suma_ineficiente(elementos[1:])
```

Diagnóstico: la rodaja `elementos[1:]` aloja una nueva lista en memoria en cada nivel de recursión. Si la colección tiene $1000$ elementos, la función reserva copias sucesivas consumiendo memoria espacial $O(N^2)$. Recomendación: en lugar de seccionar colecciones, pasar la lista intacta junto con un índice de avance entero (`def suma(elem, idx=0):`), o utilizar directamente un bucle iterativo con `sum()`.

3. **Confundir el valor de retorno del caso recursivo olvidando la sentencia `return`.**

```python
# ERROR: se invoca recursivamente pero se descarta el valor devuelto
def busqueda_rota(arbol: dict, clave: str):
    if clave in arbol:
        return arbol[clave]
    for sub in arbol.get("hijos", []):
        busqueda_rota(sub, clave)  # Falta return o acumulación
```

Diagnóstico: si se ejecuta `busqueda_rota(sub, clave)` sin asignar ni retornar su resultado, la llamada interna evaluará correctamente pero la función devolverá implícitamente `None`. Recomendación: retornar explícitamente el resultado de la llamada hija cuando sea válido: `hallado = busqueda_rota(sub, clave); if hallado is not None: return hallado`.

## 9. Resumen

- La **recursividad** modela la solución de un problema definiéndolo en términos de versiones más simples de sí mismo, integrando obligatoriamente un **caso base** directo y un **caso recursivo** que avanza de manera convergente hacia la parada.
- CPython gestiona cada llamada mediante un **marco de activación** en la pila de ejecución, reservando memoria espacial $O(N)$ proporcional a la profundidad máxima alcanzada y limitando el apilamiento por defecto a aproximadamente 1000 niveles (`RecursionError`).
- Al carecer de optimización de llamada de cola (*Tail Call Optimization*), los algoritmos lineales sobre grandes volúmenes de datos deben implementarse mediante iteración con bucles o estructuras de datos en heap.
- Los problemas con subproblemas recurrentes (como árboles de decisión o sucesiones combinatorias) deben optimizarse mediante **memoización** (`@functools.lru_cache`) para colapsar complejidades exponenciales en tiempos lineales o polinomiales.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/sys.html#sys.getrecursionlimit> — Biblioteca estándar (`sys`): consulta y configuración del límite de profundidad de la pila de llamadas del intérprete.
- <https://docs.python.org/3/library/functools.html#functools.lru_cache> — Biblioteca estándar (`functools`): decoradores `lru_cache` y `cache` para optimización de funciones recursivas mediante memoización.
- <https://docs.python.org/3/library/pathlib.html> — Biblioteca estándar (`pathlib`): navegación y manipulación orientada a objetos de sistemas de archivos jerárquicos.
- <https://docs.python.org/3/library/exceptions.html#RecursionError> — Excepciones integradas (`RecursionError`): jerarquía y condiciones de lanzamiento de errores de desbordamiento de recursión.

