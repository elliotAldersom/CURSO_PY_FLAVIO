# Ámbito de Variables, Espacios de Nombres y Regla LEGB

## 2. Introducción

Cuando un programa crece y combina decenas de [variables](../../Basico/chapter-one/variables.md), [bucles](../../Basico/chapter-two/bucles.md), [funciones](funciones.md) y [módulos](../chapter-three/modulos.md), surge una pregunta esencial: si dos partes distintas del código utilizan el mismo identificador —por ejemplo `resultado`, `contador` o `usuario`—, ¿se trata de la misma variable en memoria o de entidades independientes? Y cuando una función referencia un nombre que no fue definido dentro de ella, ¿en qué orden exacto decide Python dónde buscarlo?

El **espacio de nombres** (*namespace*) y el **ámbito** (*scope*) constituyen el sistema de reglas con el que Python organiza la visibilidad y el ciclo de vida de cada identificador. Comprender este mecanismo con precisión evita errores sutiles y resuelve problemas fundamentales del desarrollo cotidiano:

1. **Aislamiento modular:** garantiza que las variables auxiliares de una función no sobrescriban accidentalmente datos homónimos del programa principal (`DEF_CLASS_TWO.py` L142-158).
2. **Diagnóstico exacto de errores de enlace:** explica por qué una lectura aparentemente válida lanza `UnboundLocalError` cuando existe una asignación líneas más abajo en la misma función, o por qué nombrar una variable `list` o `dict` inutiliza funciones integradas.
3. **Claridad sobre bloques de control:** corrige una confusión frecuente proveniente de lenguajes como C, Java o JavaScript al demostrar qué construcciones de Python crean realmente un ámbito nuevo y cuáles no.
4. **Base de clausuras y decoradores:** permite que una función interna conserve estado de su función externa mediante el ámbito envolvente y la sentencia `nonlocal`, cimiento directo de los [decoradores](../../Avanzado/chapter-one/decoradores.md).

## 3. Fundamentos y conceptos

**Espacio de nombres (*namespace*) frente a ámbito (*scope*).** Aunque están estrechamente relacionados, designan conceptos distintos:

- **Espacio de nombres (*namespace*):** es la estructura concreta en tiempo de ejecución que asocia nombres simbólicos con referencias a objetos (conceptualmente, un diccionario de identificadores a objetos). Ejemplos son el diccionario de nombres integrados (`builtins`), el diccionario global de cada módulo (`__dict__`, consultable con `globals()`) y el marco de ejecución creado cada vez que se invoca una función.
- **Ámbito (*scope*):** es la **región textual del código fuente** desde la cual un espacio de nombres determinado puede consultarse directamente sin necesidad de prefijo calificador (sin escribir `modulo.nombre` u `objeto.atributo`). El ámbito es una propiedad **léxica (estática)**: queda determinado por la ubicación física del código en el archivo antes de ejecutar la función.

**La regla LEGB de resolución de nombres.** Cada vez que una expresión lee un nombre no calificado, Python lo busca secuencialmente de adentro hacia afuera a través de cuatro niveles, deteniéndose en la primera coincidencia:

1. **L — *Local* (Local):** el espacio propio de la invocación actual de la función (`def` o [expresión `lambda`](funciones_lambda.md)), que incluye tanto sus parámetros como cualquier variable asignada dentro de su cuerpo (salvo declaración `global` o `nonlocal`). Se crea al llamar a la función y desaparece cuando esta retorna o lanza una excepción no capturada.
2. **E — *Enclosing* (Envolvente o no local):** los espacios locales de una o más funciones externas que contienen léxicamente a una función anidada, recorridos desde la más cercana hacia la más externa (`Funciones_Repaso.py` L91-96; `Decoradores.py` L190-206). Conviene destacar una regla importante del lenguaje: **el cuerpo de una sentencia `class` NO actúa como ámbito envolvente `E` para sus métodos**; por ello, dentro de un método siempre debe accederse a atributos o constantes de la clase mediante `self.nombre` o `NombreClase.nombre`.
3. **G — *Global* (Global de módulo):** el nivel superior del archivo `.py` actual. En Python no existe un ámbito "superglobal" compartido implícitamente entre todos los archivos de un proyecto; "global" significa siempre **global al módulo donde fue definida la función** (`Funciones_Repaso.py` L99-106).
4. **B — *Built-in* (Integrado):** el espacio del módulo estándar `builtins`, cargado al iniciar el intérprete, donde residen [funciones integradas](funciones_integradas.md) (`len`, `print`, `sum`, `range`) y excepciones base (`ValueError`, `TypeError`). Si el identificador tampoco existe allí, Python lanza `NameError`.

**Corrección crítica sobre `DEF_CLASS_TWO.py` (L165-193): los bloques `while`, `for` e `if` NO crean ámbito local.** En los comentarios de `DEF_CLASS_TWO.py` (L165-169 y L183-185) se afirma que los bucles `while` y `for` *"crean un scope local dentro del bucle, lo que significa que las variables definidas dentro del bucle solo son accesibles dentro de ese bloque"*. Sin embargo, las propias líneas ejecutables del mismo archivo demuestran lo contrario: `y = 5` asignada dentro del `while` se imprime sin error fuera de él en la línea 179 (`print(y)`), y `w = 2` asignada dentro del `for` (igual que la variable de iteración `i`) permanece viva y accesible tras finalizar el ciclo en la línea 192 (`print(w)`).

La regla formal del lenguaje Python es taxativa: **los bloques de control de flujo (`if`/`elif`/`else`, `for`, `while`, `try`/`except`/`finally`, `with` y `match`/`case`) NO crean un nuevo ámbito léxico**. Toda variable asignada por primera vez dentro de cualquiera de esos bloques pertenece al ámbito contenedor donde se encuentre el bloque (el módulo si está a nivel raíz, o la función si está dentro de un `def`). La única excepción puntual de limpieza automática es el alias de captura `except ValueError as err:`, que Python elimina explícitamente al salir del bloque `except` para evitar retener ciclos de referencias con la traza de pila. En Python 3, **únicamente crean ámbito léxico propio cuatro construcciones**:

- Los **módulos** (ámbito global del archivo).
- Las **funciones** (`def` y `lambda`).
- Las definiciones de **[clases](../chapter-five/clases_y_objetos.md)** (`class`, durante la ejecución de su bloque de definición).
- Las **[comprensiones](../chapter-one/comprensiones.md) y expresiones generadoras** (`[x for x in datos]`, `{x for x in datos}`, `(x for x in datos)`), cuya variable de iteración `x` sí queda aislada en un ámbito implícito propio desde Python 3 y no contamina las variables externas.

**Clasificación en tiempo de compilación y `UnboundLocalError`.** Python decide si una variable es local a una función **durante la compilación del bloque `def`**, no línea por línea durante la ejecución. Si en cualquier parte del cuerpo de una función aparece una operación de enlace sobre `x` (`x = ...`, `x += ...`, `for x in ...`, `import x`), el compilador marca `x` como variable **local** en todo el cuerpo de esa función, salvo que exista `global x` o `nonlocal x`. Si una línea anterior dentro de la misma función intenta leer `x` creyendo que leerá la global externa, la ranura local `x` aún no tendrá objeto asociado y se producirá `UnboundLocalError`.

**Reasignación de nombres frente a mutación de objetos.** Leer una referencia global o envolvente no requiere ninguna palabra clave especial: por eso `hello_python()` en `Funciones_Repaso.py` (L102-104) lee `global_var` directamente. Del mismo modo, invocar un método mutador sobre una colección existente (`registro_eventos.append("ok")` o `cache["clave"] = 1`) **no reasigna el identificador** `registro_eventos` ni `cache`; únicamente lee su referencia y modifica el interior del objeto mutable. Solo cuando se pretende **cambiar a qué objeto apunta el identificador** (`contador = contador + 1` o `registro_eventos = []`) entra en juego el enlace de nombres y se requiere `global` o `nonlocal`.

**Sentencias `global` y `nonlocal` (PEP 3104) y clausuras (*closures*).**

- **`global nombre`:** instruye al compilador para que toda referencia y asignación a `nombre` dentro de la función opere directamente sobre el espacio de nombres del módulo (`DEF_CLASS_TWO.py` L201-209). No "convierte" una variable local previa en global, sino que redirige el identificador hacia el ámbito `G`.
- **`nonlocal nombre` (PEP 3104):** utilizable únicamente dentro de funciones anidadas, indica que `nombre` pertenece al ámbito envolvente `E` más cercano (excluyendo el ámbito global del módulo). Esto permite que una **clausura** (*closure*) —una función interna retornada que recuerda las variables libres de su entorno envolvente a través de celdas en `__closure__`, tal como ocurre en `Decoradores.py` (L87-95, L190-206) y `Decoradores_Multiples.py` (L5-19)— no solo lea ese estado, sino que también pueda actualizarlo entre llamadas sucesivas.

**Ocultamiento de nombres integrados (*shadowing*) y optimización en CPython.** Dado que `B` (*Built-in*) es el último eslabón de la cadena LEGB, definir una variable local o global llamada `list`, `dict`, `set`, `str`, `max` o `sum` (como sucede en `CLASE_ONE.py` L633 y L643 al escribir `set = {...}` y `dict = {...}`) eclipsa al tipo o función integrada homónima en ese ámbito, provocando `TypeError: 'dict' object is not callable` si más abajo se intenta llamar a `dict()`. Finalmente, como detalle de implementación de **CPython**, conocer las variables locales en tiempo de compilación permite almacenarlas en un arreglo contiguo de ranuras fijas dentro del marco de pila y accederlas mediante la instrucción de *bytecode* `LOAD_FAST` (índice entero directo), sustancialmente más veloz que buscar claves en diccionarios hash con `LOAD_GLOBAL` (ámbitos `G` y `B`) o desreferenciar celdas de clausura con `LOAD_DEREF` (ámbito `E`).

## 4. Sintaxis y funcionamiento

Declaración e interacción explícita con los distintos niveles de ámbito en Python:

```text
TASA_MODULO = 0.18                 # Ámbito Global (G)

def crear_acumulador(inicial):     # 'inicial' en Ámbito Envolvente (E)
    total = inicial                # 'total' en Ámbito Envolvente (E)

    def agregar(monto):            # 'monto' en Ámbito Local (L)
        nonlocal total             # Enlaza 'total' con el ámbito E
        impuesto = monto * TASA_MODULO  # Lee 'TASA_MODULO' desde G
        total += round(monto + impuesto, 2)  # Usa 'round' desde Built-in (B)
        return total

    return agregar
```

Resumen de niveles, palabras clave y herramientas de inspección de espacios de nombres:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | Ámbito `L` (*Local*) | Nombres asignados o recibidos por parámetro en la función actual | `def f(x): y = x + 1` |
| 2 | Ámbito `E` (*Enclosing*) | Variables locales de funciones externas que envuelven a otra función | `wrapper` leyendo `func` en un decorador |
| 3 | Ámbito `G` (*Global*) | Nombres definidos en la raíz del módulo `.py` actual | `CONFIG_TIMEOUT = 10` |
| 4 | Ámbito `B` (*Built-in*) | Nombres predefinidos en el módulo estándar `builtins` | `len`, `sum`, `isinstance`, `ValueError` |
| 5 | `global x` | Redirige lecturas y asignaciones de `x` hacia el ámbito del módulo (`G`) | `global sesiones_activas` |
| 6 | `nonlocal x` | Redirige lecturas y asignaciones de `x` al ámbito envolvente (`E`) más próximo | `nonlocal intentos_restantes` |
| 7 | Comprensión `[x for ...]` | Crea un ámbito propio para la variable de iteración `x` (Python 3+) | `[i * 2 for i in range(3)]` |
| 8 | Bloques `if`/`for`/`while` | **No** crean ámbito nuevo; sus variables viven en el ámbito contenedor | `for i in range(3): pass` → `i == 2` |
| 9 | `globals()` / `locals()` | Retornan el diccionario del módulo y una vista de variables locales actuales | `"TASA_MODULO" in globals()` |
| 10 | `f.__closure__` | Tupla de celdas con los objetos capturados desde ámbitos envolventes `E` | `f.__closure__[0].cell_contents` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Cadena LEGB completa y aislamiento entre variables locales y globales.**

```python
unidad = "ms"


def formatear_latencia(tiempos: list[int]) -> str:
    unidad = "milisegundos"
    maximo = max(tiempos)
    return f"Pico registrado: {maximo} {unidad}"


print(formatear_latencia([42, 118, 75]))
print("Variable global intacta:", unidad)
```

Explicación línea por línea:

- Línea 1: crea `unidad = "ms"` en el ámbito global `G` del módulo.
- Líneas 4-7: dentro de `formatear_latencia`, la asignación `unidad = "milisegundos"` crea una variable **local (`L`)** completamente independiente de la global (`DEF_CLASS_TWO.py` L142-158), mientras que `max` no existe en `L`, `E` ni `G`, por lo que se resuelve en el ámbito integrado `B`.
- Líneas 10-11: confirman que la función utiliza su `unidad` local sin alterar la variable `unidad` del módulo (`"ms"`).

Resultado esperado:

```text
Pico registrado: 118 milisegundos
Variable global intacta: ms
```

**Ejemplo 2 — Verificación práctica: los bucles `for`/`while` no crean ámbito, pero las comprensiones sí.**

```python
i = "valor_previo"
cuadrados = [i * i for i in range(4)]
print("Tras comprensión, i conserva:", i, "| cuadrados:", cuadrados)

for indice_bucle in range(3):
    ultimo_doble = indice_bucle * 2

if ultimo_doble >= 2:
    estado_bloque = "umbral alcanzado"

print(f"Fuera de for e if -> indice_bucle={indice_bucle}, ultimo_doble={ultimo_doble}, estado='{estado_bloque}'")
```

Explicación línea por línea:

- Líneas 1-3: aunque la lista por comprensión usa el identificador `i`, Python 3 ejecuta la comprensión en un ámbito implícito aislado; al terminar, la variable externa `i` mantiene intacto `"valor_previo"`.
- Líneas 5-9: corrigen empíricamente lo comentado en `DEF_CLASS_TWO.py` (L165-193): tanto `indice_bucle` como `ultimo_doble` (definidas en el `for`) y `estado_bloque` (definida dentro del `if`) pertenecen al mismo ámbito contenedor y siguen plenamente accesibles en la línea 11.

Resultado esperado:

```text
Tras comprensión, i conserva: valor_previo | cuadrados: [0, 1, 4, 9]
Fuera de for e if -> indice_bucle=2, ultimo_doble=4, estado='umbral alcanzado'
```

### Intermedio

**Ejemplo 3 — Clausuras (*closures*) con estado privado encapsulado mediante `nonlocal`.**

```python
def crear_limitador_intentos(max_intentos: int):
    intentos_usados = 0

    def registrar_intento(usuario: str) -> str:
        nonlocal intentos_usados
        if intentos_usados >= max_intentos:
            return f"{usuario}: cuenta bloqueada ({intentos_usados}/{max_intentos})"
        intentos_usados += 1
        return f"{usuario}: intento {intentos_usados} de {max_intentos}"

    return registrar_intento


control_login = crear_limitador_intentos(2)
print(control_login("flavio"))
print(control_login("flavio"))
print(control_login("flavio"))
print("Variables libres capturadas:", control_login.__code__.co_freevars)
print("Valores actuales en celdas:", [c.cell_contents for c in control_login.__closure__])
```

Explicación de las decisiones tomadas:

- `crear_limitador_intentos` define `intentos_usados` en su ámbito local, que actúa como ámbito envolvente `E` para `registrar_intento`.
- Sin `nonlocal intentos_usados`, la línea `intentos_usados += 1` intentaría crear una variable local nueva sin inicializar y fallaría con `UnboundLocalError`. Con `nonlocal`, la clausura actualiza la celda compartida entre invocaciones sin contaminar el ámbito global con variables sueltas.
- Las dos últimas líneas inspeccionan `__code__.co_freevars` y `__closure__`, haciendo visible el mecanismo interno con el que Python conserva `intentos_usados` y `max_intentos` después de que `crear_limitador_intentos` ya finalizó.

Resultado esperado:

```text
flavio: intento 1 de 2
flavio: intento 2 de 2
flavio: cuenta bloqueada (2/2)
Variables libres capturadas: ('intentos_usados', 'max_intentos')
Valores actuales en celdas: [2, 2]
```

### Avanzado

**Ejemplo 4 — Contraste entre estado global acoplado y diseño puro/clausurado desacoplado, e inspección de clasificación del compilador.**

```python
FACTOR_CONVERSION = 3.6


def convertir_rapidez_ms_a_kmh(metros_por_segundo: float) -> float:
    """Lee una constante de módulo inmutable sin mutar estado externo."""
    return round(metros_por_segundo * FACTOR_CONVERSION, 2)


def crear_acumulador_metricas():
    muestras: list[float] = []

    def agregar_muestra(ms: float) -> tuple[int, float]:
        kmh = convertir_rapidez_ms_a_kmh(ms)
        muestras.append(kmh)
        promedio = round(sum(muestras) / len(muestras), 2)
        return len(muestras), promedio

    return agregar_muestra


sensor_norte = crear_acumulador_metricas()
sensor_sur = crear_acumulador_metricas()

print("Norte lectura 1:", sensor_norte(10.0))
print("Norte lectura 2:", sensor_norte(15.0))
print("Sur lectura 1 (aislado):", sensor_sur(20.0))
print("Locales de convertir_rapidez_ms_a_kmh:", convertir_rapidez_ms_a_kmh.__code__.co_varnames)
```

Explicación de arquitectura y rendimiento:

- A diferencia de modificar una variable global con `global` (`DEF_CLASS_TWO.py` L201-209) —lo que impediría tener dos sensores independientes funcionando a la vez—, cada llamada a `crear_acumulador_metricas()` fabrica su propia lista `muestras` aislada en su clausura (`sensor_norte` no interfiere con `sensor_sur`).
- Observando `agregar_muestra`, nótese que `muestras.append(kmh)` **no requiere `nonlocal muestras`**, porque muta la lista existente en lugar de reasignar el identificador `muestras`.
- En `FACTOR_CONVERSION = 3.6`, el ámbito global se emplea de forma legítima: como **constante de módulo de solo lectura** nombrada en `UPPER_SNAKE_CASE`.

Resultado esperado:

```text
Norte lectura 1: (1, 36.0)
Norte lectura 2: (2, 45.0)
Sur lectura 1 (aislado): (1, 72.0)
Locales de convertir_rapidez_ms_a_kmh: ('metros_por_segundo',)
```

## 6. Aplicaciones en el mundo real

- **Decoradores de autenticación, registro y medición de tiempos:** tal como implementan `Decoradores.py` (L134-145, L190-206) y `Decoradores_Multiples.py` (L58-72), la función `wrapper` accede a la función decorada y a sus parámetros de configuración gracias al ámbito envolvente `E` ([decoradores](../../Avanzado/chapter-one/decoradores.md)).
- **Constantes de configuración a nivel de módulo:** definir `TIMEOUT_SEGUNDOS = 10` o expresiones regulares precompiladas en el ámbito global del módulo permite reutilizarlas desde múltiples funciones con coste de compilación único al importar el archivo.
- **Fábricas de funciones parametrizadas (*function factories*):** construir validadores, serializadores o clientes con prefijos de URL preconfigurados devolviendo una función interna que captura la configuración en su clausura.
- **Funciones auxiliares privadas de orquestación:** tal como esboza `Juego.py` (L273-434) al anidar subtareas de edición que comparten acceso de lectura a la instancia recibida por la función principal, evitando pasar el mismo contexto repetidamente cuando las funciones auxiliares solo tienen sentido dentro de esa operación.

## 7. Uso en producción

- **Evitar el uso de `global` para gestionar estado mutable de negocio:** modificar variables globales desde funciones dificulta razonar sobre el flujo de datos, hace que el orden de ejecución de las pruebas unitarias altere sus resultados (*flaky tests*) y provoca condiciones de carrera (*race conditions*) en servidores multihilo o concurrentes. Cuando varias operaciones deban compartir y mutar estado, debe encapsularse en una [clase](../chapter-five/clases_y_objetos.md) o pasarse explícitamente como parámetro y valor de retorno.
- **Restringir el ámbito global a constantes inmutables, funciones y clases:** en módulos de producción, todo identificador de datos en la raíz del archivo debe ser inmutable y escribirse en `UPPER_SNAKE_CASE` (`MAX_REINTENTOS = 3`, `COLUMNAS_VALIDAS = ("id", "total")`), señalizando que ninguna función debe reasignarlo.
- **No abusar de anidamientos profundos de funciones:** si una función interna no necesita capturar variables del ámbito envolvente `E`, suele ser preferible definirla a nivel de módulo con prefijo de uso interno (`def _normalizar_texto(...):`). Así no se reconstruye un nuevo objeto `function` en cada llamada a la función externa y puede probarse unitariamente de forma directa.
- **Configurar analizadores de código contra el ocultamiento de integrados (*shadowing*):** herramientas como `ruff` (reglas `A001`–`A003`) o `flake8-builtins` detectan automáticamente asignaciones a identificadores como `id`, `type`, `list`, `dict`, `set`, `input` o `filter` antes de que causen fallos en producción.

## 8. Errores comunes y recomendaciones

1. **Disparar `UnboundLocalError` al leer y luego reasignar el mismo nombre sin declaración explícita.**

```python
# ERROR INTENCIONAL: UnboundLocalError porque 'contador += 1' clasifica 'contador' como local en toda la función
contador = 10


def incrementar():
    print("Valor previo:", contador)
    contador += 1


incrementar()
```

Diagnóstico: al compilar `incrementar`, Python detecta `contador += 1` (equivalente a `contador = contador + 1`) y registra `contador` como variable **local**. Al ejecutarse antes `print("Valor previo:", contador)`, busca `contador` en el marco local aún vacío y lanza `UnboundLocalError: cannot access local variable 'contador' where it is not associated with a value`. Solución: pasar `contador` por parámetro y retornar el nuevo valor (`def incrementar(c): return c + 1`), o usar `nonlocal`/`global` únicamente si el diseño lo justifica.

2. **Asumir que una variable definida en una rama condicional `if` siempre existirá fuera del bloque.**

```python
# ERROR INTENCIONAL: NameError / UnboundLocalError cuando la rama que inicializa la variable no se ejecuta
def clasificar_temperatura(grados: float) -> str:
    if grados > 30:
        etiqueta = "caluroso"
    return etiqueta


print(clasificar_temperatura(18.0))
```

Diagnóstico: `if` no crea un ámbito separado, por lo que `etiqueta` pertenece al ámbito local de `clasificar_temperatura`; sin embargo, cuando `grados <= 30`, la línea `etiqueta = "caluroso"` nunca llega a ejecutarse y `return etiqueta` falla con `UnboundLocalError`. Solución: inicializar siempre un valor por defecto antes del condicional o cubrir exhaustivamente todas las ramas con `else`.

3. **Eclipsar (*shadowing*) nombres del módulo `builtins` como `dict`, `set`, `list` o `sum`.**

```python
import builtins

datos = [10, 20, 30]
sum = 999
print("Identificador local 'sum' oculta a la función integrada:", sum)

del sum
print("Tras eliminar el sombreado, sum(datos) funciona:", builtins.sum(datos), sum(datos))
```

Resultado esperado:

```text
Identificador local 'sum' oculta a la función integrada: 999
Tras eliminar el sombreado, sum(datos) funciona: 60 60
```

Diagnóstico: en `CLASE_ONE.py` (L633, L643) se asignaron variables llamadas `set = {...}` y `dict = {...}`. A partir de esa línea, el ámbito global contiene entradas `"set"` y `"dict"` que tapan al ámbito `B` (*Built-in*), impidiendo construir nuevos conjuntos o diccionarios con `set()` o `dict()`. Solución: emplear nombres descriptivos (`conjunto_palabras`, `mapa_numeros`, `total_suma`) que nunca coincidan con identificadores de `builtins`.

4. **Intentar acceder directamente a un atributo de clase desde un método sin `self.` ni el nombre de la clase.**

```python
# ERROR INTENCIONAL: NameError porque el bloque 'class' no forma parte de los ámbitos envolventes E de sus métodos
class Impuesto:
    tasa = 0.18

    def calcular(self, monto: float) -> float:
        return monto * tasa


print(Impuesto().calcular(100))
```

Diagnóstico: lanza `NameError: name 'tasa' is not defined` porque la búsqueda LEGB dentro de `calcular` salta desde el ámbito local del método directamente al ámbito global del módulo, omitiendo el espacio de nombres de `class Impuesto`. Solución: calificar explícitamente el acceso con `self.tasa` o `Impuesto.tasa`.

## 9. Resumen

- Un **espacio de nombres** (*namespace*) mapea identificadores a objetos en memoria; un **ámbito** (*scope*) es la región léxica del código donde ese espacio es accesible sin prefijo.
- Python resuelve nombres no calificados siguiendo estrictamente el orden **LEGB**: *Local* → *Enclosing* → *Global* (de módulo) → *Built-in*.
- En Python 3, solo crean ámbito léxico propio los **módulos**, las **funciones** (`def` y `lambda`), las **clases** (no heredado como `E` por sus métodos) y las **comprensiones / expresiones generadoras**.
- Los bloques `if`, `for`, `while`, `try`, `with` y `match` **no** crean ámbito local: las variables enlazadas en ellos pertenecen al ámbito contenedor.
- Cualquier asignación a un nombre dentro de una función lo convierte en local para **toda** esa función en tiempo de compilación; leerlo antes de asignarlo produce `UnboundLocalError`.
- `global` redirige asignaciones al módulo y `nonlocal` (PEP 3104) al ámbito envolvente `E` de una clausura; en código de producción se prefiere el paso explícito de parámetros, constantes inmutables u objetos frente al estado global mutable.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/DEF_CLASS_TWO.py` (L133-210) | `DEF_CLASS_TWO.py` | Contraste entre `media_0` global y local, ejemplos de variables en `while` (`y`) y `for` (`w`, `i`), y palabra clave `global variable` | **Corrección crítica** a los comentarios de L165-193: se demostró por qué `while` y `for` **no** crean ámbito local en Python y se precisó la semántica real de `global` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CREAR_FUNCIONES.py` (L26-30, L58-62) | `CREAR_FUNCIONES.py` | Independencia entre el parámetro local `name` dentro de `nombre_1` y las variables globales del script | Se explicó mediante los marcos de pila locales creados en cada invocación |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/Funciones_Repaso.py` (L91-106) | `Funciones_Repaso.py` | Funciones anidadas (`outer_function` / `inner_function`) y lectura directa de `global_var` junto a `local_var` | Se integraron ambos fragmentos dentro de la jerarquía unificada LEGB (`L`, `E`, `G`, `B`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L633, L643) | `CLASE_ONE.py` | Asignación de colecciones a variables llamadas `set = {...}` y `dict = {...}` | Analizado en la sección 8 como caso real de *shadowing* que oculta tipos del ámbito `Built-in` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores.py` (L11-20, L87-95, L190-206) | `Decoradores.py` | Clausuras de uno y dos niveles (`Calcular_tiempo_ejecucion` → `wrapper` → `wrapper_2`) capturando `name_funcion` y `function` | Se explicó la retención de variables libres en celdas (`__closure__`) más allá de la vida de la función externa |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L5-19, L58-72) | `Decoradores_Multiples.py` | Captura de `func` / `f` en ámbitos envolventes independientes al apilar decoradores | Relacionado con el aislamiento léxico entre distintas instancias de clausuras |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decoradores.py` (L1-16) | `Decoradores.py` | Función interna `Funcion_Nueva` que invoca `funcion()` retenida en el entorno de `Delimitar` | Conectado como puente hacia el estudio avanzado de [decoradores](../../Avanzado/chapter-one/decoradores.md) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L258-434) | `Juego.py` | Funciones anidadas (`New_Name`, `New_Fuerza`, etc.) dentro de `Editar_Guerrero(guerrero)` accediendo al parámetro envolvente `guerrero` | Evaluado en las secciones 6 y 7 respecto a cuándo conviene anidar funciones y cuándo extraerlas a nivel de módulo |

**Fundamento complementario:** se incorporaron cinco conceptos fundamentales del modelo de ejecución de Python: (1) la distinción rigurosa entre *namespace* y *scope* junto con la regla **LEGB** completa (incluida la exclusión del bloque `class` como ámbito `E`); (2) el aislamiento léxico propio de las comprensiones en Python 3; (3) el origen en tiempo de compilación de `UnboundLocalError`; (4) la sentencia `nonlocal` especificada en **PEP 3104** para clausuras con estado; y (5) la diferencia de rendimiento en **CPython** entre ranuras locales indexadas (`LOAD_FAST`), diccionarios globales (`LOAD_GLOBAL`) y celdas de clausura (`LOAD_DEREF`).

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces> — Tutorial oficial de Python: espacios de nombres, regla de búsqueda de ámbitos y comparativa entre lectura local, `nonlocal` y `global`.
- <https://docs.python.org/3/reference/executionmodel.html#naming-and-binding> — Referencia del lenguaje: modelo formal de enlace de nombres, bloques de código, variables libres y excepciones `NameError` / `UnboundLocalError`.
- <https://docs.python.org/3/reference/simple_stmts.html#the-global-statement> — Referencia del lenguaje: especificación de la sentencia `global`.
- <https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement> — Referencia del lenguaje: especificación de la sentencia `nonlocal`.
- <https://peps.python.org/pep-3104/> — PEP 3104 (*Access to Names in Outer Scopes*): diseño y motivación de la palabra clave `nonlocal` para clausuras léxicas.
