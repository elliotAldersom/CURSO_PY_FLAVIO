# Funciones Integradas (Built-ins), Introspección y Seguridad

## 2. Introducción

En la programación cotidiana existen operaciones tan transversales —medir la longitud de una colección, sumar importes, recorrer dos secuencias en paralelo, comprobar el tipo de un objeto o evaluar si todos los campos cumplen una condición— que requerir una sentencia `import` en cada archivo volvería innecesariamente verboso cualquier módulo.

Las **funciones integradas** (*built-in functions*) son el conjunto selecto de utilidades y constructores que residen permanentemente en el módulo estándar `builtins`, el último nivel de la regla de [ámbito de variables](ambito_variables.md) (**LEGB**), por lo que están disponibles de inmediato en cualquier script de Python sin importación previa.

Estudiar estas funciones organizadas por familias técnicas resuelve cuatro objetivos clave:

1. **Expresividad y velocidad nativa:** reemplaza bucles manuales propensos a errores por primitivas implementadas en C dentro de **CPython** (`sum`, `min`, `max`, `all`, `any`, `sorted`).
2. **Iteración limpia y segura:** articula recorridos indexados (`enumerate`) y paralelos (`zip(..., strict=True)`) sin aritmética manual de índices.
3. **Introspección precisa de objetos:** distingue entre consultar identidad (`id`), representación técnica (`repr`), capacidades (`dir`) y pertenencia jerárquica a tipos (`isinstance`, `issubclass`).
4. **Criterio de seguridad en producción:** identifica funciones integradas peligrosas ante entradas externas —específicamente `eval()`, empleada sin advertencias en `Metodos_Especiales.py` (L44)— y establece sus reemplazos seguros en la biblioteca estándar (`ast.literal_eval`).

## 3. Fundamentos y conceptos

**El espacio `builtins` frente a la biblioteca estándar y conexión con protocolos *dunder*.** Python mantiene deliberadamente reducido el espacio `builtins` (alrededor de setenta funciones y tipos esenciales) frente a los cientos de [módulos](../chapter-three/modulos.md) específicos de la biblioteca estándar (`math`, `decimal`, `ast`, `itertools`), que sí requieren `import`. Muchas funciones integradas no contienen lógica rígida cerrada, sino que actúan como **puntos de entrada uniformes hacia métodos especiales** (*dunder methods*, profundizados en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md)): llamar a `len(obj)` invoca internamente `obj.__len__()`; `repr(obj)` delega en `obj.__repr__()`; `bool(obj)` consulta `obj.__bool__()` (o `obj.__len__()` si el primero no existe); e `iter(obj)` invoca `obj.__iter__()`.

**Familia 1 — Funciones numéricas y de agregación (`abs`, `divmod`, `round`, `sum`, `min`, `max`).**

- **`round(numero, ndigits=None)` y el redondeo bancario:** a diferencia del redondeo escolar tradicional que siempre lleva `.5` hacia arriba, Python 3 implementa el estándar **redondeo al par más cercano** (*round half to even* o redondeo bancario): ante un empate exacto en `.5`, redondea hacia el entero par inmediato (`round(2.5)` es `2` y `round(3.5)` es `4`), eliminando el sesgo estadístico acumulado al sumar miles de redondeos. Además, como los `float` se almacenan en base 2 (IEEE 754), fracciones decimales como `2.675` no tienen representación binaria exacta (su valor real en memoria es ligeramente menor que $2.675$), por lo que `round(2.675, 2)` entrega `2.67`. Cuando se exige aritmética financiera decimal exacta, debe emplearse el [módulo `decimal`](../chapter-four/decimal.md), tal como practica `redondeo.py` (L1-20) con `Decimal` y `ROUND_HALF_UP`.
- **`sum(iterable, start=0)`:** acumula elementos numéricos comenzando desde `start` (`INTEGRADAS_FUNCIONES.PY` L117-138). Para unir cadenas de texto no debe usarse `sum`, sino `"".join(textos)` (de hecho, `sum` rechaza `str` explícitamente con `TypeError` para evitar concatenaciones cuadráticas).
- **`min()` y `max()` con `key=` y `default=`:** devuelven el extremo de un iterable o de varios argumentos (`INTEGRADAS_FUNCIONES.PY` L31-39). Si el iterable puede venir vacío, pasar el argumento por palabra clave `default=None` (o `default=0`) evita que lancen `ValueError: max() iterable argument is empty`.

**Familia 2 — Veracidad (*truthiness*) y cuantificadores lógicos (`bool`, `all`, `any`).**

- **`bool(x)`:** evalúa el valor de verdad de cualquier objeto (`INTEGRADAS_FUNCIONES.PY` L50-85). Son falsos (`False`) las constantes `None` y `False`, cualquier cero numérico (`0`, `0.0`, `0j`) y cualquier colección o secuencia vacía (`""`, `[]`, `()`, `{}`, `set()`, `range(0)`). Todo lo demás se evalúa como `True` —incluidas colecciones no vacías que contengan ceros o `None` en su interior, como `[344, 0]` (`INTEGRADAS_FUNCIONES.PY` L106-110)—.
- **`all(iterable)` y `any(iterable)`:** actúan como cuantificadores universal ($\forall$) y existencial ($\exists$) con **evaluación en cortocircuito**: `all()` se detiene y retorna `False` en cuanto halla el primer elemento falso sin evaluar el resto del iterable; `any()` se detiene y retorna `True` en cuanto encuentra el primer elemento verdadero. Un caso límite matemático fundamental es el iterable vacío: **`all([])` retorna `True`** (*verdad vacua*: no existe ningún contraejemplo falso en la colección vacía), mientras que **`any([])` retorna `False`**.

**Familia 3 — Secuencias e iteración (`len`, `range`, `enumerate`, `zip`, `sorted`, `reversed`, `iter`, `next`).**

- **`len(s)`:** retorna la cantidad de elementos en tiempo constante $O(1)$ para colecciones nativas en memoria (`list`, `tuple`, `dict`, `set`, `str`), ya que lee directamente el contador de tamaño mantenido en la estructura del objeto sin recorrerlo; no funciona sobre iteradores perezosos arbitrarios porque no tienen longitud precalculada.
- **`enumerate(iterable, start=0)`:** produce pares `(indice, elemento)`, eliminando el antipatrón `for i in range(len(lista)):` señalado en `BUCLE_FOR.py` (L99-118) y permitiendo iniciar la numeración en `1` para menús de usuario como hace `Juego.py` (L482: `enumerate(lista_guerrero, 1)`).
- **`zip(*iterables, strict=False)`:** empareja posicionalmente varios iterables (`BUCLE_FOR.py` L67). Por defecto, si un iterable es más corto que otro, `zip()` **se detiene silenciosamente** al agotarse el menor, descartando los datos sobrantes. Desde **Python 3.10**, pasar `strict=True` (`zip(claves, valores, strict=True)`) exige longitudes idénticas y lanza `ValueError` si algún iterable termina antes, previniendo pérdidas inadvertidas de registros.
- **`sorted(iterable, *, key=None, reverse=False)` frente a `lista.sort()`:** `sorted()` acepta **cualquier iterable** (tuplas, conjuntos, diccionarios, generadores) y devuelve siempre una **nueva `list`** dejando intacto el original (`CLASE_ONE.py` L794-797, L945); el método `.sort()` solo existe en `list`, ordena en sitio y retorna `None`.
- **`iter(obj)` y `next(iterador, por_defecto)`:** exponen manualmente el protocolo de iteración explicado en `BUCLE_FOR.py` (L24-35). Pasar un segundo argumento a `next(it, None)` devuelve ese centinela cuando el iterador se agota en lugar de propagar `StopIteration` ([iteradores](../../Avanzado/chapter-one/iteradores.md)).

**Familia 4 — Introspección, identidad y representación (`isinstance`, `issubclass`, `type`, `id`, `repr`, `dir`, `hash`).**

- **`isinstance(obj, clase_o_tupla)` frente a `type(obj)`:** `type(obj)` devuelve la clase exacta de creación del objeto, sin considerar herencia; en cambio, `isinstance(person, Persona)` devuelve `True` tanto para instancias directas de `Persona` como para instancias de subclases como `Empleado_Artista` (`Herencia_Multiple.py` L65-72, estudiado en [herencia](../chapter-five/herencia.md)). Además, acepta múltiples tipos como tupla o unión (`isinstance(x, (int, float))` o `isinstance(x, int | float)`). Conviene recordar el apunte de `Metodos.py` (L21 y L55): aplicar `isinstance(entrada, int)` al resultado directo de `input()` siempre dará `False` porque `input()` entrega invariablemente un `str`.
- **`id(obj)` (modelo del lenguaje frente a CPython):** en la especificación del lenguaje Python, `id(obj)` devuelve un número entero que identifica de manera única y constante al objeto mientras este exista en memoria (dos objetos con tiempos de vida no solapados pueden reutilizar el mismo `id`), y el operador `a is b` equivale exactamente a `id(a) == id(b)`. Como detalle específico de implementación en **CPython**, dicho entero corresponde a la dirección virtual de memoria del objeto `PyObject*`.
- **`repr(obj)` frente a `str(obj)`:** `str()` busca una presentación legible para personas usuarias (`__str__`), mientras que `repr()` produce una representación inequívoca orientada a depuración y desarrollo (`__repr__`), preservando delimitadores y tipos (por ejemplo, `repr("18")` es `"'18'"` mientras `repr(18)` es `"18"`).
- **`hash(obj)`:** calcula el entero de resumen usado por conjuntos y claves de diccionarios sobre objetos inmutables (*hashables*), garantizando que objetos iguales tengan igual *hash* (`42 == 42.0` implica `hash(42) == hash(42.0)`). Por seguridad frente a ataques de colisión, Python aleatoriza el *hash* de cadenas y `bytes` en cada proceso mediante `PYTHONHASHSEED`.

**Advertencia crítica de seguridad sobre `eval()` (y `exec()`).** En `Metodos_Especiales.py` (L42-45 y L59-72) se muestra el patrón `repre = repr(one); resultado = eval(repre)` para reconstruir un objeto `Persona` a partir de texto. Si bien funciona en una prueba local controlada, **ejecutar `eval()` o `exec()` sobre cualquier cadena que provenga directa o indirectamente de un usuario, archivo externo, base de datos compartida o red constituye una vulnerabilidad crítica de Ejecución Remota de Código (*Arbitrary Code Execution*)**: `eval()` compila y ejecuta cualquier expresión Python válida con todos los permisos del sistema operativo que posea el proceso actual (pudiendo borrar archivos, leer credenciales o abrir conexiones externas).

Para analizar texto que representa estructuras de datos literales de Python sin riesgo de ejecución de código, la biblioteca estándar incluye **`ast.literal_eval(cadena)`**, que valida el árbol sintáctico y solo construye literales inocuos (`str`, `bytes`, `int`, `float`, `complex`, `tuple`, `list`, `dict`, `set`, `bool` y `None`), rechazando de inmediato cualquier llamada a función, operador arbitrario o acceso a atributos. Para intercambio de datos e instanciación de modelos en producción deben usarse formatos de serialización dedicados (`json.loads`) junto con constructores o métodos de fábrica explícitos.

## 4. Sintaxis y funcionamiento

Invocación representativa de las principales funciones integradas organizadas por propósito:

```text
# Agregación y redondeo
total = sum(<iterable>, start=0)
extremo = max(<iterable>, key=<fn>, default=None)
valor_redondeado = round(<numero>, <decimales>)

# Cuantificadores lógicos en cortocircuito
todos_cumplen = all(<iterable_condiciones>)
alguno_cumple = any(<iterable_condiciones>)

# Iteración coordinada y ordenamiento
for indice, item in enumerate(<iterable>, start=1): ...
for a, b in zip(<it1>, <it2>, strict=True): ...
ordenados = sorted(<iterable>, key=<fn>, reverse=False)

# Introspección y análisis seguro de literales
es_numero = isinstance(<obj>, (int, float))
estructura_segura = ast.literal_eval(<texto_literal>)
```

Tabla de referencia de funciones integradas esenciales:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `abs(x)` / `divmod(a, b)` | Valor absoluto y par `(a // b, a % b)` en un solo paso | `divmod(17, 5)` → `(3, 2)` |
| 2 | `round(x, n)` | Redondeo al par más cercano (*banker's rounding*) | `round(2.5)` → `2`; `round(3.5)` → `4` |
| 3 | `sum(it, start=0)` | Suma numérica de un iterable a partir de `start` | `sum([10, 20], start=5)` → `35` |
| 4 | `min` / `max(it, default=...)` | Menor o mayor elemento; `default` evita fallo si está vacío | `max([], default=0)` → `0` |
| 5 | `bool(x)` | Valor de verdad según protocolo `__bool__` / `__len__` | `bool([])` → `False`; `bool([0])` → `True` |
| 6 | `all(it)` / `any(it)` | `True` si todos / al menos uno son verdaderos (cortocircuito) | `all([])` → `True`; `any([])` → `False` |
| 7 | `len(s)` | Cantidad de elementos de una colección medida ($O(1)$) | `len({"a": 1, "b": 2})` → `2` |
| 8 | `enumerate(it, start=0)` | Iterador de tuplas `(indice, valor)` | `list(enumerate("AB", 1))` → `[(1, 'A'), (2, 'B')]` |
| 9 | `zip(*its, strict=False)` | Empareja iterables; `strict=True` (3.10+) exige igual longitud | `list(zip([1, 2], "AB", strict=True))` |
| 10 | `sorted(it, key=..., reverse=...)` | Nueva `list` ordenada a partir de cualquier iterable | `sorted({3, 1, 2})` → `[1, 2, 3]` |
| 11 | `isinstance(obj, cls)` / `issubclass` | Comprobación de tipo o subclase respetando herencia | `isinstance(True, int)` → `True` |
| 12 | `repr(obj)` / `id(obj)` | Representación técnica inequívoca e identificador único | `repr("hola\n")` → `'hola\\n'` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Agregaciones seguras, redondeo bancario y cuantificadores `all()` / `any()`.**

```python
ventas_dia = [120.50, 340.00, 89.50]
ventas_sin_movimiento: list[float] = []

print("Suma total:", sum(ventas_dia))
print("Venta máxima (con datos):", max(ventas_dia, default=0.0))
print("Venta máxima (lista vacía segura):", max(ventas_sin_movimiento, default=0.0))
print("Redondeo al par: round(2.5) =", round(2.5), "| round(3.5) =", round(3.5))

campos_formulario = ["Flavio", "flavio@ejemplo.com", "Huaral"]
print("¿Formulario completo?:", all(campos_formulario))
print("¿Algún monto supera 300?:", any(monto > 300 for monto in ventas_dia))
print("Verdad vacua all([]) vs any([]):", all([]), any([]))
```

Explicación línea por línea:

- Líneas 4-6: amplían los ejemplos de `INTEGRADAS_FUNCIONES.PY` (L31-39, L117-138) añadiendo `default=0.0` en `max()`, lo que impide un fallo cuando aún no existen registros en el día.
- Línea 7: comprueba el redondeo bancario hacia el número par en empates exactos (`2.5` → `2` y `3.5` → `4`).
- Líneas 9-12: muestran cómo `all()` verifica que ninguna cadena esté vacía, cómo `any()` se combina con una expresión generadora sin crear una lista intermedia, y cuál es el comportamiento exacto sobre colecciones vacías.

Resultado esperado:

```text
Suma total: 550.0
Venta máxima (con datos): 340.0
Venta máxima (lista vacía segura): 0.0
Redondeo al par: round(2.5) = 2 | round(3.5) = 4
¿Formulario completo?: True
¿Algún monto supera 300?: True
Verdad vacua all([]) vs any([]): True False
```

### Intermedio

**Ejemplo 2 — Iteración coordinada con `enumerate(..., start=1)`, `zip(..., strict=True)`, `sorted()` y `next()`.**

```python
modulos = ["Autenticación", "Pagos", "Reportes"]
latencias_ms = (45, 130, 62)

pares = list(zip(modulos, latencias_ms, strict=True))
ranking = sorted(pares, key=lambda par: par[1], reverse=True)

for puesto, (nombre, ms) in enumerate(ranking, start=1):
    print(f"{puesto}) {nombre}: {ms} ms")

primer_lento = next((nombre for nombre, ms in pares if ms > 100), "Ninguno")
primer_critico = next((nombre for nombre, ms in pares if ms > 500), "Ninguno")
print(f" >100 ms: {primer_lento} | >500 ms: {primer_critico}".strip())
```

Explicación de las decisiones tomadas:

- `zip(modulos, latencias_ms, strict=True)` garantiza que no falte ninguna medición respecto de la lista de nombres.
- `sorted(..., reverse=True)` crea una nueva lista ordenada de mayor a menor latencia sin mutar la tupla ni la lista originales (`CLASE_ONE.py` L794-797).
- `enumerate(..., start=1)` numera el reporte desde `1` (`Juego.py` L482), y `next(generador, "Ninguno")` localiza en cortocircuito la primera coincidencia o devuelve el valor por defecto sin lanzar `StopIteration`.

Resultado esperado:

```text
1) Pagos: 130 ms
2) Reportes: 62 ms
3) Autenticación: 45 ms
>100 ms: Pagos | >500 ms: Ninguno
```

### Avanzado

**Ejemplo 3 — Introspección jerárquica con `isinstance`/`issubclass`, `repr` y reemplazo seguro de `eval()` mediante `ast.literal_eval()`.**

```python
import ast


class Dispositivo:
    pass


class SensorTemperatura(Dispositivo):
    def __init__(self, codigo: str, lectura: float) -> None:
        self.codigo = codigo
        self.lectura = lectura

    def __repr__(self) -> str:
        return f"SensorTemperatura(codigo={self.codigo!r}, lectura={self.lectura!r})"


sensor = SensorTemperatura("TMP-01", 23.4)
print("type exacto vs isinstance en herencia:", type(sensor) is Dispositivo, isinstance(sensor, Dispositivo))
print("issubclass:", issubclass(SensorTemperatura, Dispositivo))
print("Identidad coherente con is:", (sensor is sensor) == (id(sensor) == id(sensor)))
print("Representación técnica repr():", repr(sensor))

carga_externa = "{'codigo': 'TMP-02', 'lectura': 19.8}"
datos_validados = ast.literal_eval(carga_externa)
sensor_reconstruido = SensorTemperatura(**datos_validados)
print("Reconstruido sin eval():", repr(sensor_reconstruido))
```

Explicación de arquitectura y seguridad:

- Mientras que `type(sensor) is Dispositivo` da `False` porque la clase concreta es `SensorTemperatura`, `isinstance(sensor, Dispositivo)` respeta el polimorfismo y la herencia (`Herencia_Multiple.py` L56-72).
- Usar `{self.codigo!r}` dentro de `__repr__` aplica automáticamente `repr()` a cada campo, conservando las comillas de las cadenas.
- En lugar del patrón inseguro `eval(cadena)` de `Metodos_Especiales.py` (L44), `ast.literal_eval(carga_externa)` convierte de forma segura el literal de diccionario y construye la instancia explícitamente con `SensorTemperatura(**datos_validados)`.

Resultado esperado:

```text
type exacto vs isinstance en herencia: False True
issubclass: True
Identidad coherente con is: True
Representación técnica repr(): SensorTemperatura(codigo='TMP-01', lectura=23.4)
Reconstruido sin eval(): SensorTemperatura(codigo='TMP-02', lectura=19.8)
```

## 6. Aplicaciones en el mundo real

- **Validación declarativa de reglas de dominio:** verificar precondiciones de un lote completo con `if not all(item.stock > 0 for item in carrito):` deteniendo la revisión apenas aparece el primer artículo agotado.
- **Búsqueda eficiente del primer elemento válido:** extraer con `next((u for u in usuarios if u.id == buscado), None)` un registro puntual sin recorrer el resto de la colección ni construir listas filtradas completas.
- **Inspección dinámica y serialización de modelos:** emplear `isinstance`, `getattr` y `repr` en sistemas de registro de auditoría (*logging*) para formatear objetos heterogéneos con precisión diagnóstica.
- **Verificación de integridad en tuberías de datos paralelas:** combinar encabezados de columnas y filas de valores con `dict(zip(columnas, fila, strict=True))` asegurando que ninguna fila corrupta con columnas de menos se inserte silenciosamente.

## 7. Uso en producción

- **Prohibir `eval()` y `exec()` sobre entradas no confiables:** analizadores de seguridad estática como `Bandit` (regla `B307`) marcan el uso de `eval()` como hallazgo de severidad media/alta. Para configuraciones o cargas de red deben utilizarse `json.loads()`, `tomllib.loads()` o `ast.literal_eval()` seguidos de validación explícita de esquema.
- **Preferir `isinstance(x, Tipo)` frente a `type(x) == Tipo`:** comprobar con `type()` rompe la sustitución polimórfica cuando alguien pasa una subclase válida o un doble de prueba. Solo se recurre a `type(x) is int` en el caso particular donde deba excluirse explícitamente a `bool` (ya que en Python `bool` es subclase de `int` y `isinstance(True, int)` devuelve `True`).
- **Activar `strict=True` en `zip()` por defecto en lógica de negocio:** salvo que truncar al iterable menor sea intencional y esté documentado, `strict=True` convierte errores silenciosos de desalineación de datos en fallos inmediatos y rastreables.
- **No emplear `round()` sobre `float` para contabilidad ni facturación:** debido a la representación binaria en coma flotante, los cálculos monetarios en producción deben realizarse en céntimos enteros (`int`) o mediante objetos `decimal.Decimal` configurados con la regla de redondeo fiscal correspondiente ([módulo decimal](../chapter-four/decimal.md)).

## 8. Errores comunes y recomendaciones

1. **Intentar evaluar código ejecutable con `ast.literal_eval()` frente al peligro real de `eval()`.**

```python
import ast

entrada_maliciosa = "__import__('os').getcwd()"
try:
    ast.literal_eval(entrada_maliciosa)
except (ValueError, SyntaxError) as err:
    print("Ejecución bloqueada con excepción:", type(err).__name__)
```

Resultado esperado:

```text
Ejecución bloqueada con excepción: ValueError
```

Diagnóstico: si esa misma cadena se hubiera pasado a `eval()`, Python habría importado `os` y ejecutado la llamada al sistema operativo. `ast.literal_eval` detecta un nodo de llamada (`ast.Call`) no permitido en el árbol sintáctico y aborta con `ValueError` sin ejecutar absolutamente nada.

2. **Pérdida silenciosa de datos al omitir `strict=True` en `zip()` con listas desalineadas.**

```python
# ERROR INTENCIONAL: ValueError detectado a tiempo gracias a strict=True ante longitudes distintas
usuarios = ["Ana", "Luis", "Carla"]
correos = ["ana@dominio.com", "luis@dominio.com"]

asignaciones = list(zip(usuarios, correos, strict=True))
```

Diagnóstico: sin `strict=True`, `"Carla"` habría desaparecido del resultado sin ningún aviso; con `strict=True`, Python lanza `ValueError: zip() argument 2 is shorter than argument 1`, alertando de inmediato la inconsistencia en los datos de origen.

3. **Confundir `lista.sort()` (que muta y devuelve `None`) con `sorted(lista)`.**

```python
notas = [14, 19, 11, 17]
intento_erroneo = notas.sort()
copia_ordenada = sorted([14, 19, 11, 17])

print("Retorno de .sort():", intento_erroneo, "| Lista mutada:", notas)
print("Retorno de sorted():", copia_ordenada)
```

Resultado esperado:

```text
Retorno de .sort(): None | Lista mutada: [11, 14, 17, 19]
Retorno de sorted(): [11, 14, 17, 19]
```

Diagnóstico: asignar `notas = notas.sort()` destruye la referencia a la lista reemplazándola por `None`. Solución: usar `sorted(notas)` cuando se requiera recibir la nueva lista en una expresión o preservar el original, y llamar a `notas.sort()` en una línea independiente solo cuando se desee ordenar en sitio.

4. **Sorprenderse por `all([]) == True` al validar lotes que pueden llegar vacíos.**

```python
pagos_procesados: list[bool] = []
validacion_ingenua = all(pagos_procesados)
validacion_no_vacia = bool(pagos_procesados) and all(pagos_procesados)

print("Solo all([]):", validacion_ingenua)
print("Exigiendo al menos un elemento:", validacion_no_vacia)
```

Resultado esperado:

```text
Solo all([]): True
Exigiendo al menos un elemento: False
```

Diagnóstico: si una regla de negocio requiere *"que exista al menos un pago y que todos hayan sido exitosos"*, escribir únicamente `if all(pagos):` aprobará por error una lista vacía `[]`. Solución: combinar explícitamente `if pagos and all(pagos):`.

## 9. Resumen

- Las funciones integradas viven en el espacio de nombres `builtins` (nivel `B` de LEGB) y delegan de forma uniforme sobre los métodos especiales del modelo de datos (`__len__`, `__repr__`, `__bool__`, `__iter__`).
- `round()` aplica redondeo al par más cercano (*banker's rounding*) sobre `float` binarios; para precisión monetaria exacta debe preferirse `decimal.Decimal`.
- `min()` y `max()` admiten `key=` y `default=`; `sum()` acepta `start=` para colecciones numéricas.
- `all()` y `any()` evalúan iterables en cortocircuito; sobre un iterable vacío, `all([])` es `True` (verdad vacua) y `any([])` es `False`.
- `enumerate(..., start=...)`, `zip(..., strict=True)`, `sorted()` y `next(it, defecto)` permiten escribir iteraciones expresivas, seguras y libres de índices manuales.
- `isinstance()` e `issubclass()` respetan la herencia (a diferencia de comparar `type(x) is ...`), `id()` expone la identidad única del objeto (dirección de memoria en **CPython**) y `ast.literal_eval()` debe reemplazar siempre a `eval()` al interpretar literales externos.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/INTEGRADAS_FUNCIONES.PY` (L24-139) | `INTEGRADAS_FUNCIONES.PY` | Uso práctico de `max()`, `min()`, `round()`, tabla de valores verdaderos/falsos con `bool()`, cuantificador `all()` y `sum()` sobre colecciones | Se añadieron `any()`, `default=` en `min`/`max`, verdad vacua `all([])`, redondeo bancario y cortocircuito lógico |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/BUCLE_FOR.py` (L24-35, L66-86, L101-118) | `BUCLE_FOR.py` | Protocolo `iter()` / `next()`, recorridos con `zip()`, `range()`, `len()` y contraste con `enumerate()` | Se incorporó `zip(..., strict=True)` (Python 3.10+) y el centinela por defecto en `next(it, defecto)` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L200, L364-387, L792-807, L942-960) | `CLASE_ONE.py` | Introspección inicial con `type()` y `dir()`, `len()` y ordenamiento no destructivo con `sorted()` | Se contrastó sistemáticamente `sorted()` frente a `.sort()` y `type()` frente a `isinstance()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/redondeo.py` (L1-20) | `redondeo.py` | Uso de `Decimal` y `ROUND_HALF_UP` para redondear `"2.675"` a `2.68` | Conectado con los límites de coma flotante binaria IEEE 754 al usar `round()` integrado |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Metodos.py` (L21, L55) | `Metodos.py` | Observación comentada de por qué `isinstance(name, int)` no detecta dígitos sobre la cadena devuelta por `input()` | Se formalizó el alcance de `isinstance` con tuplas de tipos y la particularidad `isinstance(True, int)` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/Herencia_Multiple.py` (L55-72) | `Herencia_Multiple.py` | Comprobación de relaciones de herencia con `issubclass()` e `isinstance()` en herencia múltiple | Integrado en la familia de introspección polimórfica (Ejemplo 3) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Metodos_Especiales.py` (L42-45, L51-73) | `Metodos_Especiales.py` | Uso conjunto de `repr(one)` y reconstrucción del objeto mediante `eval(repre)` | **Ampliación crítica de seguridad:** se explicó el riesgo de ejecución arbitraria de código en `eval()` y su reemplazo por `ast.literal_eval()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L80-87, L474, L482-485) | `Juego.py` | Aplicación combinada de `len()`, `round()`, `range()` y numeración desde 1 con `enumerate(lista_guerrero, 1)` | Destacado como integración real de múltiples funciones de `builtins` en una aplicación interactiva |

**Fundamento complementario:** se incorporaron cinco aspectos técnicos esenciales: (1) la correspondencia entre funciones de `builtins` y métodos especiales del modelo de datos; (2) la regla exacta de redondeo al par (*round-half-to-even*) en `round()`; (3) el parámetro de integridad `strict=True` de `zip()` introducido en Python 3.10; (4) la distinción entre el contrato abstracto de `id()` en el lenguaje Python y su correspondencia con direcciones de memoria en **CPython**, junto con `hash()`; y (5) el análisis de seguridad sobre `eval()` y la alternativa estándar `ast.literal_eval()`.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/functions.html> — Biblioteca estándar de Python: catálogo completo y especificación de todas las funciones integradas (`builtins`).
- <https://docs.python.org/3/library/builtins.html> — Biblioteca estándar: documentación del módulo `builtins` y su carga automática en el intérprete.
- <https://docs.python.org/3/library/stdtypes.html#truth-value-testing> — Biblioteca estándar: reglas formales de evaluación de veracidad (*truth value testing*) para `bool()`, `all()` y `any()`.
- <https://docs.python.org/3/tutorial/floatingpoint.html> — Tutorial oficial: aritmética en coma flotante binaria y causas de resultados como `round(2.675, 2)`.
- <https://docs.python.org/3/library/ast.html#ast.literal_eval> — Biblioteca estándar: especificación de `ast.literal_eval()` para evaluar literales de Python de forma segura sin ejecutar código arbitrario.
