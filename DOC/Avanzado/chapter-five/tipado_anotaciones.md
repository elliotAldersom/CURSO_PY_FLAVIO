# Sistema de Tipos Gradual y Anotaciones de Tipos (`typing`)

## 2. Introducción

Python es un lenguaje de **tipado dinámico y fuertemente tipado**: los nombres de variables carecen de tipo fijo y son meras referencias a objetos en memoria que conocen su propio tipo en tiempo de ejecución. Aunque esta flexibilidad permite un prototipado extremadamente rápido, en sistemas de gran escala la ausencia de contratos de tipos explícitos introduce fragilidad: errores de tipo inadvertidos (`AttributeError`, `TypeError`) detectados tardíamente en producción, refactorizaciones inseguras y documentación que queda desactualizada con el código.

A partir de **PEP 484** (Python 3.5), el lenguaje incorporó el concepto de **tipado gradual (*Gradual Typing*)** a través del módulo estándar `typing` y la sintaxis formal de anotaciones de tipo (*Type Hints*). 

Bajo el tipado gradual, las anotaciones de tipos son completamente opcionales y **no imponen penalizaciones de rendimiento en tiempo de ejecución**: el intérprete de Python no valida tipos al ejecutar el programa, sino que delega dicha comprobación a herramientas de análisis estático como `mypy` o `pyright`, habilitando autocompletado inteligente en IDEs, verificación matemática de contratos y detección temprana de defectos antes de compilar o desplegar.

## 3. Fundamentos y conceptos

**Tipado gradual: coexistencia entre lo dinámico y lo estático.**
El sistema de tipos de Python permite mezclar código dinámico no anotado con módulos rigurosamente tipados:
- Si un componente no incluye anotaciones, el analizador estático lo asume como el tipo comodín **`Any`**, permitiendo cualquier operación sin emitir advertencias.
- Conforme se añaden anotaciones (`int`, `str`, `list[int]`), el verificador de tipos aplica reglas de inferencia y coherencia matemática sobre las llamadas, parámetros y retornos.

**Evolución sintáctica: Tipado moderno en Python 3.10+ (PEP 604 y PEP 585).**
- **Sintaxis de unión con tubería (`|`):** en Python 3.10+, la unión de tipos se expresa directamente con el operador `|` (`int | str`), reemplazando la importación de `Union[int, str]` de versiones anteriores.
- **`Optional[T]`:** representa un valor que puede ser de tipo `T` o `None`. En Python 3.10+ se escribe de forma idiomática como `T | None`.
- **Contenedores genéricos nativos (PEP 585):** desde Python 3.9 no es necesario importar `List`, `Dict`, `Tuple` o `Set` desde `typing`; se utilizan directamente los tipos integrados con corchetes: `list[str]`, `dict[str, int]`, `tuple[int, ...]`, `set[float]`.

**Tipos especiales del módulo `typing`:**
- **`Any`:** desactiva la comprobación estática para esa variable específica. Debe usarse con estricta moderación como puente de migración.
- **`Callable[[TipoArg1, TipoArg2], TipoRetorno]`:** anota funciones, métodos o cualquier objeto que implemente `__call__`.
- **`Literal['opcionA', 'opcionB']`:** restringe el valor a una lista cerrada de literales exactos (ideal para configuraciones o estados finitos).
- **`TypeVar` y `Generic[T]`:** habilita la programación genérica paramétrica, donde una función o clase opera sobre un tipo abstracto que se preserva entre la entrada y la salida.
- **`Protocol` (PEP 544):** define interfaces estructurales (*duck typing* estático); una clase satisface el protocolo si posee los métodos requeridos, sin necesidad de heredar explícitamente de él.

## 4. Sintaxis y funcionamiento

Anotación de funciones con parámetros opcionales, valores por defecto y uniones modernas:

```python
from collections.abc import Sequence
from typing import Literal


def buscar_registro(
    identificador: int | str,
    campos: Sequence[str] | None = None,
    formato: Literal["json", "csv"] = "json",
) -> dict[str, str] | None:
    # Retorna un diccionario o None si no se encuentra
    if not identificador:
        return None
    return {"id": str(identificador), "formato": formato}
```

Genéricos paramétricos con `TypeVar`:

```python
from typing import TypeVar

# T representa cualquier tipo consistente entre entrada y salida
T = TypeVar("T")


def primer_elemento(secuencia: list[T]) -> T:
    if not secuencia:
        raise IndexError("La lista no puede estar vacía")
    return secuencia[0]  # Si entra list[int], mypy infiere retorno int
```

Contratos estructurales con `typing.Protocol`:

```python
from typing import Protocol


class Renderizable(Protocol):
    def renderizar_html(self) -> str: ...
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Anotación de funciones puras, colecciones nativas y parámetros nulos opcionales.**

```python
def calcular_estadisticas_basicas(
    puntuaciones: list[float], redondear_decimales: int | None = None
) -> dict[str, float]:
    """Calcula el promedio, mínimo y máximo de una lista de puntuaciones numéricas."""
    if not puntuaciones:
        raise ValueError("La colección de puntuaciones no puede estar vacía")

    total = sum(puntuaciones)
    promedio = total / len(puntuaciones)
    minimo = min(puntuaciones)
    maximo = max(puntuaciones)

    if redondear_decimales is not None:
        promedio = round(promedio, redondear_decimales)
        minimo = round(minimo, redondear_decimales)
        maximo = round(maximo, redondear_decimales)

    return {
        "promedio": promedio,
        "minimo": minimo,
        "maximo": maximo,
    }


# Comprobación de invocación
notas_alumnos: list[float] = [14.5, 18.2, 12.0, 19.5, 16.8]
resultado_exacto = calcular_estadisticas_basicas(notas_alumnos)
resultado_redondeado = calcular_estadisticas_basicas(notas_alumnos, redondear_decimales=1)

print("Tipo de resultado        :", type(resultado_exacto).__name__)
print("Estadísticas exactas     :", resultado_exacto)
print("Estadísticas redondeadas :", resultado_redondeado)
```

Explicación paso a paso:

- `puntuaciones: list[float]` exige que la entrada sea una lista homogénea cuyos elementos sean números de coma flotante.
- `redondear_decimales: int | None = None` documenta formalmente que el argumento es opcional; si no se suministra, su valor por defecto es `None`.
- `-> dict[str, float]` establece un contrato estricto sobre el valor de retorno: cualquier herramienta estática inferirá que las claves del diccionario son cadenas (`str`) y los valores asociados son flotantes (`float`).

Resultado esperado:

```text
Tipo de resultado        : dict
Estadísticas exactas     : {'promedio': 16.2, 'minimo': 12.0, 'maximo': 19.5}
Estadísticas redondeadas : {'promedio': 16.2, 'minimo': 12.0, 'maximo': 19.5}
```

### Intermedio

**Ejemplo 2 — Funciones de orden superior con `Callable`, literales restrictivos (`Literal`) y mapeos estructurados.**

```python
from collections.abc import Callable
from typing import Literal

TipoOperacion = Literal["multiplicar", "sumar"]


def aplicar_transformacion(
    valores: list[int],
    operacion: TipoOperacion,
    transformador: Callable[[int], int],
) -> list[int]:
    """Aplica un transformador funcional sobre una lista de enteros según la política elegida."""
    salida: list[int] = []
    factor = 2 if operacion == "multiplicar" else 0

    for item in valores:
        valor_procesado = transformador(item)
        if operacion == "multiplicar":
            salida.append(valor_procesado * factor)
        else:
            salida.append(valor_procesado + 10)
    return salida


# Funciones de transformación con firma int -> int
def duplicar(x: int) -> int:
    return x * 2


def elevar_cuadrado(x: int) -> int:
    return x * x


# Invocación verificable
datos_entrada = [2, 4, 6]
res_mult = aplicar_transformacion(datos_entrada, "multiplicar", duplicar)
res_suma = aplicar_transformacion(datos_entrada, "sumar", elevar_cuadrado)

print("Entrada original     :", datos_entrada)
print("Transformado mult    :", res_mult)
print("Transformado suma    :", res_suma)
```

Explicación técnica:

- `TipoOperacion = Literal["multiplicar", "sumar"]` restringe los valores permitidos para el argumento `operacion`. Si un desarrollador pasa `"dividir"`, el analizador de tipos estático `mypy` señalará un error de compilación sin necesidad de ejecutar el código.
- `Callable[[int], int]` anota funciones de primera clase que reciben un único argumento de tipo `int` y devuelven un `int`. Pasar una función con signatura incompatible disparará una alerta estática inmediata.

Resultado esperado:

```text
Entrada original     : [2, 4, 6]
Transformado mult    : [8, 16, 24]
Transformado suma    : [14, 26, 46]
```

### Avanzado

**Ejemplo 3 — Clases genéricas reutilizables con `Generic[T]`, límites superiores (`bound`) y subtipado estructural con `Protocol`.**

```python
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


class Identificable(Protocol):
    """Protocolo estructural: cualquier objeto con atributo id entero satisface el contrato."""

    id: int


# TypeVar restringido: T debe satisfacer el protocolo Identificable
T = TypeVar("T", bound=Identificable)


class RepositorioEnMemoria(Generic[T]):
    """Repositorio genérico de persistencia fuertemente tipado."""

    def __init__(self) -> None:
        self._almacen: dict[int, T] = {}

    def guardar(self, entidad: T) -> None:
        self._almacen[entidad.id] = entidad

    def obtener_por_id(self, id_entidad: int) -> T | None:
        return self._almacen.get(id_entidad)

    def listar_todos(self) -> list[T]:
        return list(self._almacen.values())


# Entidades de dominio concretas que satisfacen implícitamente el protocolo Identificable
@dataclass
class Usuario:
    id: int
    correo: str
    activo: bool


@dataclass
class Factura:
    id: int
    importe_total: float


# Instanciación de repositorios especializados con tipado exacto
repo_usuarios: RepositorioEnMemoria[Usuario] = RepositorioEnMemoria()
repo_facturas: RepositorioEnMemoria[Factura] = RepositorioEnMemoria()

user_1 = Usuario(id=101, correo="dev@empresa.com", activo=True)
fact_1 = Factura(id=5001, importe_total=1450.50)

repo_usuarios.guardar(user_1)
repo_facturas.guardar(fact_1)

usuario_recuperado = repo_usuarios.obtener_por_id(101)
factura_recuperada = repo_facturas.obtener_por_id(5001)

print("Usuario recuperado   :", usuario_recuperado)
print("Factura recuperada   :", factura_recuperada)
print("Tipo de usuario      :", type(usuario_recuperado).__name__)
print("Tipo de factura      :", type(factura_recuperada).__name__)
```

Explicación de ingeniería:

- `T = TypeVar('T', bound=Identificable)` define una variable de tipo genérica con límite superior (*upper bound*). Cualquier tipo que pretenda ser administrado por `RepositorioEnMemoria` debe implementar obligatoriamente el atributo `id: int`.
- La clase `RepositorioEnMemoria[Usuario]` es completamente genérica pero estáticamente segura: el analizador de tipos sabe que `obtener_por_id()` retornará una instancia de `Usuario | None` (no un `Any`), garantizando autocompletado y validación de atributos (`usuario_recuperado.correo`) sin necesidad de conversiones manuales.
- Ni `Usuario` ni `Factura` heredan explícitamente de `Identificable`: cumplen el protocolo mediante *duck typing* estático verificado por el compilador (*Structural Subtyping*, PEP 544).

Resultado esperado:

```text
Usuario recuperado   : Usuario(id=101, correo='dev@empresa.com', activo=True)
Factura recuperada   : Factura(id=5001, importe_total=1450.5)
Tipo de usuario      : Usuario
Tipo de factura      : Factura
```

## 6. Aplicaciones en el mundo real

- **Frameworks modernos de backend:** frameworks como FastAPI, Pydantic y SQLModel utilizan las anotaciones de tipo de Python para autogenerar esquemas OpenAPI, validar entradas JSON de solicitudes HTTP y documentar APIs en tiempo real.
- **Herramientas de análisis estático en Integración Continua (CI):** ejecución de `mypy --strict` en pipelines de GitHub Actions o GitLab CI para impedir que código con errores de tipo llegue a la rama principal.
- **Bases de código de gran escala y microservicios:** refactorizaciones seguras en proyectos con cientos de miles de líneas de código donde el cambio de signatura de una función se valida automáticamente en todo el repositorio.
- **Desarrollo de bibliotecas reutilizables:** provisión de archivos de definición de tipos (`.pyi` o paquete `py.typed`) para que los consumidores de una biblioteca disfruten de autocompletado exacto en sus editores.

## 7. Uso en producción

- **Adoptar tipado gradual de forma incremental:** no intentar tipar un sistema legado de 100 000 líneas en un solo paso; comenzar tipando las interfaces públicas de dominio, modelos y utilidades centrales con `mypy` configurado en modo permisivo, activando reglas estrictas gradualmente.
- **Utilizar `Sequence` e `Iterable` para parámetros y `list` para retornos:** en las firmas de funciones, aceptar interfaces genéricas amplias (`collections.abc.Sequence[str]`) para permitir que el cliente pase listas, tuplas o rangos indistintamente; retornar tipos concretos (`list[str]`) para que el consumidor conozca las operaciones mutables disponibles.
- **Evitar el abuso de `Any`:** utilizar `Any` equivale a desactivar el verificador estático para esa línea; si un tipo es dinámico o desconocido, preferir `object` (que exige comprobaciones con `isinstance()` antes de acceder a sus métodos).
- **Asegurar la presencia del marcador `py.typed`:** si se publica un paquete o módulo interno para ser consumido por otros equipos, incluir un archivo vacío llamado `py.typed` en la raíz del paquete según PEP 561 para indicar a los analizadores estáticos que deben inspeccionar sus anotaciones.

## 8. Errores comunes y recomendaciones

1. **Creer que Python valida tipos en tiempo de ejecución (`Runtime Myth`).**

```python
def sumar_enteros(a: int, b: int) -> int:
    return a + b


# Python NO lanza error al ejecutar esto:
resultado = sumar_enteros("Hola ", "Mundo")  # Devuelve "Hola Mundo"
```

Diagnóstico: el intérprete de CPython ignora las anotaciones de tipo durante la ejecución; son metadatos pasivos alojados en `__annotations__`. Recomendación: para validación estricta en tiempo de ejecución (como en APIs web), utilizar herramientas como Pydantic o comprobaciones explícitas con `isinstance()`.

2. **Usar `list` o `dict` mutables como valores por defecto en firmas anotadas.**

```python
# ANTIPATRÓN GRAVE: el argumento por defecto mutable se comparte entre llamadas
def registrar_evento(evento: str, lista: list[str] = []) -> list[str]:
    lista.append(evento)
    return lista


# CORRECCIÓN: usar None y tipar con unión
def registrar_evento_seguro(evento: str, lista: list[str] | None = None) -> list[str]:
    if lista is None:
        lista = []
    lista.append(evento)
    return lista
```

Diagnóstico: el objeto lista se evalúa una sola vez al cargar la función en memoria; llamadas sucesivas compartirán el mismo acumulador. Recomendación: tipar siempre el parámetro como `list[str] | None = None` y crear la lista nueva dentro del cuerpo.

3. **Confundir `TypeVar` con una unión de tipos.**

```python
from typing import TypeVar

# ERROR: T se resuelve a un único tipo consistente por llamada; no es una unión
T = TypeVar("T")


def combinar_incorrecto(a: T, b: T) -> T:
    return a + b


# Si se llama con combinar(10, "texto"), mypy lanza error:
# "TypeVar T is bound to incompatible types int and str"
```

Diagnóstico: `TypeVar` preserva la identidad del tipo en todos los lugares donde aparece; si el primer argumento es `int`, el segundo debe ser forzosamente `int`. Si se desea permitir tipos mixtos, debe utilizarse una unión `int | str`.

## 9. Resumen

- El **tipado gradual** (**PEP 484**) incorpora anotaciones de tipo opcionales sin costo de rendimiento en tiempo de ejecución, delegando la verificación en analizadores estáticos como `mypy`.
- En Python 3.10+, las uniones se expresan mediante el operador **`|`** (`int | None`), y los contenedores nativos soportan tipado directo (`list[str]`, `dict[str, int]`).
- El tipo **`Callable`** permite tipar funciones de orden superior y **`Literal`** restringe variables a conjuntos cerrados de valores constantes.
- **`TypeVar`** y **`Generic`** habilitan algoritmos y estructuras de datos genéricas conservando la precisión de tipos entre entradas y salidas.
- **`typing.Protocol`** (**PEP 544**) formaliza el *duck typing* estático mediante subtipado estructural sin necesidad de herencia nominal.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/typing.html> — Biblioteca estándar (`typing`): catálogo exhaustivo de tipos, genéricos y protocolos.
- <https://peps.python.org/pep-0484/> — PEP 484 (*Type Hints*): especificación fundacional del sistema de tipos gradual de Python.
- <https://peps.python.org/pep-0585/> — PEP 585 (*Type Hinting Generics In Standard Collections*): parametrización directa de tipos nativos (`list`, `dict`).
- <https://peps.python.org/pep-0604/> — PEP 604 (*Allow writing union types as X | Y*): sintaxis del operador de unión por tubería.
- <https://mypy.readthedocs.io/en/stable/> — Documentación oficial de Mypy: verificador estático de tipos de referencia para Python.

