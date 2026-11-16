# Clases de Datos Declarativas (`dataclasses`)

## 2. Introducción

En el desarrollo de software orientado a objetos, una proporción significativa de las [clases](../../Intermedio/chapter-five/clases_y_objetos.md) creadas actúan primordialmente como contenedores de datos o estructuras de transporte (*Data Transfer Objects*, DTOs, entidades de dominio o registros de configuración).

Escribir estas entidades manualmente en Python estándar exige redactar grandes volúmenes de código repetitivo (*boilerplate*): definir un inicializador `__init__` con asignaciones redundantes (`self.x = x`), escribir un método `__repr__` legible para depuración, implementar `__eq__` para comparar objetos por valor en lugar de por identidad de memoria (`id()`), y definir `__hash__` si el objeto debe almacenarse en [conjuntos](../../Intermedio/chapter-one/conjuntos.md) o actuar como clave de [diccionarios](../../Intermedio/chapter-one/diccionarios.md).

Para erradicar esta sobrecarga de mantenimiento sin comprometer la extensibilidad de las clases regulares, Python formalizó en **PEP 557** (Python 3.7) el módulo estándar **`dataclasses`** y el decorador **`@dataclass`**. 

Mediante `@dataclass`, el desarrollador declara los atributos de la entidad mediante [anotaciones de tipo](tipado_anotaciones.md) a nivel de clase, y el decorador genera automáticamente en tiempo de compilación métodos especiales altamente optimizados (`__init__`, `__repr__`, `__eq__`), habilitando además inmutabilidad estricta (`frozen=True`), ordenamiento por valor (`order=True`) y ganchos de validación posterior (`__post_init__`).

## 3. Fundamentos y conceptos

**Generación automática de métodos especiales.**
Al aplicar `@dataclass` sobre una clase, el decorador inspecciona el diccionario de anotaciones `__annotations__` y genera dinámicamente métodos nativos en CPython:
- **`__init__`:** inicializa los campos en el orden exacto en que fueron declarados.
- **`__repr__`:** produce una representación legible con formato `NombreClase(campo1=val1, campo2=val2)` para facilitar el registro en logs y la depuración.
- **`__eq__`:** compara dos instancias campo por campo evaluando sus valores (`self.campo == other.campo`), en lugar de comparar punteros de memoria como hace `object.__eq__` por defecto.

**La función `field()` y personalización granular de atributos.**
Cuando un campo requiere comportamiento especial más allá de un valor atómico predeterminado, se utiliza la función constructora `field()` de `dataclasses`:
- `default_factory`: asigna una función generadora para inicializar valores mutables independientes (como listas o diccionarios) sin compartir la misma instancia entre objetos.
- `repr=False`: excluye el atributo de la cadena generada por `__repr__` (indispensable para datos sensibles como contraseñas o tokens).
- `compare=False`: ignora el atributo al evaluar igualdades (`__eq__`) o relaciones de orden (`<`, `>`).
- `init=False`: omite el atributo del constructor `__init__`, indicando que será calculado o poblado internamente durante `__post_init__`.

**Inmutabilidad y seguridad ante concurrencia: `frozen=True`.**
Configurar `@dataclass(frozen=True)` convierte las instancias en objetos **inmutables**:
- Cualquier intento de asignación posterior (`instancia.campo = nuevo_valor`) o borrado (`del instancia.campo`) lanza inmediatamente una excepción `FrozenInstanceError`.
- Al garantizar la inmutabilidad de sus atributos, Python autogenera un método `__hash__` seguro, permitiendo que la instancia se utilice directamente como clave en diccionarios o se almacene en conjuntos `set`.

**Validación y cálculo derivado con `__post_init__`.**
Cuando una clase de datos necesita validar invariantes de negocio o calcular campos derivados a partir de los parámetros recibidos, define el método especial `__post_init__(self)`:
- El `__init__` autogenerado ejecuta primero todas las asignaciones normales y, como última instrucción, invoca `self.__post_init__()`.
- En clases inmutables (`frozen=True`), para asignar atributos derivados dentro de `__post_init__` se debe eludir la protección utilizando `object.__setattr__(self, 'nombre_campo', valor)`.

## 4. Sintaxis y funcionamiento

Parámetros del decorador `@dataclass`:

```python
from dataclasses import dataclass


@dataclass(
    init=True,  # Genera __init__
    repr=True,  # Genera __repr__
    eq=True,  # Genera __eq__
    order=False,  # Si True, genera métodos de ordenamiento rico: <, <=, >, >=
    unsafe_hash=False,  # Forzar generación de __hash__ manual
    frozen=False,  # Si True, convierte las instancias en inmutables (read-only)
    match_args=True,  # Soporte para Pattern Matching estructural (PEP 634)
    kw_only=False,  # En Python 3.10+, fuerza a que todos los campos sean por palabra clave
    slots=False,  # En Python 3.10+, genera __slots__ ahorrando memoria RAM
)
class DefinicionEjemplo:
    identificador: int
    descripcion: str = "Sin descripcion"
```

Uso de `field()` para listas y atributos calculados:

```python
from dataclasses import dataclass, field


@dataclass
class CarritoCompras:
    usuario_id: int
    # default_factory previene el error crítico de compartir la misma lista
    articulos: list[str] = field(default_factory=list)
    # Atributo excluido de __repr__ y de __init__
    total_acumulado: float = field(init=False, default=0.0, repr=False)
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación de una entidad de datos, comparación por valor e inspección con `asdict`.**

```python
from dataclasses import asdict, astuple, dataclass


@dataclass
class PuntoCoordenada:
    x: float
    y: float
    etiqueta: str = "Origen"


# 1. Instanciación y comparación por valor
p1 = PuntoCoordenada(10.5, 20.0, "Punto A")
p2 = PuntoCoordenada(10.5, 20.0, "Punto A")
p3 = PuntoCoordenada(0.0, 0.0)

# 2. Demostración de igualdad semántica autogenerada (__eq__)
print("Representación legible (repr) :", p1)
print("Son el mismo objeto en memoria:", p1 is p2)
print("Tienen el mismo valor (__eq__) :", p1 == p2)
print("Tercer punto con valor defecto:", p3)

# 3. Conversión rápida a estructuras nativas
diccionario_p1 = asdict(p1)
tupla_p1 = astuple(p1)

print("\nConversión a dict :", diccionario_p1)
print("Conversión a tuple:", tupla_p1)
```

Explicación paso a paso:

- `PuntoCoordenada` declara tres campos tipados; el decorador `@dataclass` genera automáticamente un constructor `__init__(self, x: float, y: float, etiqueta: str = "Origen")`.
- `p1 == p2` evalúa a `True` porque `@dataclass` implementa comparación por valor (`x == other.x and y == other.y and etiqueta == other.etiqueta`), a pesar de que residen en direcciones de memoria distintas (`p1 is p2` es `False`).
- `asdict()` y `astuple()` serializan recursivamente la instancia a diccionarios y tuplas nativas de Python, ideal para exportación a JSON o bases de datos.

Resultado esperado:

```text
Representación legible (repr) : PuntoCoordenada(x=10.5, y=20.0, etiqueta='Punto A')
Son el mismo objeto en memoria: False
Tienen el mismo valor (__eq__) : True
Tercer punto con valor defecto: PuntoCoordenada(x=0.0, y=0.0, etiqueta='Origen')

Conversión a dict : {'x': 10.5, 'y': 20.0, 'etiqueta': 'Punto A'}
Conversión a tuple: (10.5, 20.0, 'Punto A')
```

### Intermedio

**Ejemplo 2 — Colecciones mutables con `default_factory`, ordenamiento con `order=True` y exclusión de atributos.**

```python
from dataclasses import dataclass, field


@dataclass(order=True)
class TareaProgramada:
    # El ordenamiento por defecto evalúa los campos de arriba hacia abajo
    prioridad: int
    descripcion: str = field(compare=False)
    etiquetas: list[str] = field(default_factory=list, compare=False)
    token_autenticacion: str = field(default="", repr=False, compare=False)


# 1. Creación de tareas con prioridades numéricas (menor número = mayor urgencia)
t1 = TareaProgramada(
    prioridad=2,
    descripcion="Generar reporte PDF",
    etiquetas=["reportes", "cron"],
    token_autenticacion="secret_123",
)
t2 = TareaProgramada(
    prioridad=1,
    descripcion="Parchar vulnerabilidad de seguridad",
    etiquetas=["seguridad", "urgente"],
    token_autenticacion="secret_456",
)
t3 = TareaProgramada(
    prioridad=3,
    descripcion="Optimizar índices de base de datos",
)

# 2. Ordenamiento automático de una colección de tareas
cola_tareas = [t1, t2, t3]
cola_tareas.sort()

print("--- Representación segura (sin token sensible) ---")
print(t1)

print("\n--- Tareas ordenadas por prioridad ---")
for t in cola_tareas:
    print(f"Prioridad {t.prioridad}: {t.descripcion}")

# 3. Comprobación de independencia de listas (default_factory)
t3.etiquetas.append("mantenimiento")
print("\nEtiquetas de t1 (intactas) :", t1.etiquetas)
print("Etiquetas de t3 (mutadas)  :", t3.etiquetas)
```

Explicación técnica:

- Al habilitar `order=True`, `@dataclass` implementa los métodos de ordenamiento rico (`__lt__`, `__le__`, `__gt__`, `__ge__`) comparando los campos en forma de tupla sintética. Al marcar `compare=False` en la descripción y etiquetas, el ordenamiento se calcula **exclusivamente sobre la prioridad**.
- `field(default_factory=list)` asegura que cada tarea reciba su propia lista nueva e independiente de etiquetas en lugar de compartir una lista global estática.
- `repr=False` oculta `token_autenticacion` de las cadenas generadas por `print(t1)` o registradas en logs, previniendo la fuga involuntaria de credenciales.

Resultado esperado:

```text
--- Representación segura (sin token sensible) ---
TareaProgramada(prioridad=2, descripcion='Generar reporte PDF', etiquetas=['reportes', 'cron'])

--- Tareas ordenadas por prioridad ---
Prioridad 1: Parchar vulnerabilidad de seguridad
Prioridad 2: Generar reporte PDF
Prioridad 3: Optimizar índices de base de datos

Etiquetas de t1 (intactas) : ['reportes', 'cron']
Etiquetas de t3 (mutadas)  : ['mantenimiento']
```

### Avanzado

**Ejemplo 3 — Inmutabilidad estricta (`frozen=True`), validación defensiva con `__post_init__` y uso en conjuntos y diccionarios.**

```python
from dataclasses import dataclass, field
import uuid


@dataclass(frozen=True)
class ClaveIdentidadFiscal:
    pais: str
    numero_identificacion: str
    digito_verificador: int = field(init=False)

    def __post_init__(self) -> None:
        # 1. Validación de reglas de negocio
        if len(self.pais) != 2:
            raise ValueError(f"El código de país debe ser ISO de 2 letras: {self.pais}")
        if not self.numero_identificacion.isdigit():
            raise ValueError("El número fiscal debe contener únicamente dígitos")

        # 2. Cálculo de atributo derivado en clase inmutable (frozen)
        suma_digitos = sum(int(d) for d in self.numero_identificacion)
        calculado = suma_digitos % 10

        # En frozen=True no se puede hacer self.x = val; se elude mediante object.__setattr__
        object.__setattr__(self, "pais", self.pais.upper())
        object.__setattr__(self, "digito_verificador", calculado)


# 1. Creación de registros inmutables
id_fiscal_1 = ClaveIdentidadFiscal(pais="es", numero_identificacion="12345678")
id_fiscal_2 = ClaveIdentidadFiscal(pais="ES", numero_identificacion="12345678")
id_fiscal_3 = ClaveIdentidadFiscal(pais="ar", numero_identificacion="20448899")

# 2. Demostración de hashability: utilizables como claves de diccionario y elementos de set
conjunto_fiscales = {id_fiscal_1, id_fiscal_2, id_fiscal_3}
mapa_empresas = {
    id_fiscal_1: "Soluciones Cloud S.L.",
    id_fiscal_3: "Servicios Digitales S.A.",
}

# 3. Comprobación de protección contra mutación accidental
intento_modificacion_exitoso = False
try:
    # Debe fallar con FrozenInstanceError
    id_fiscal_1.pais = "FR"  # type: ignore
except Exception as err:
    tipo_error = type(err).__name__

print("Registro 1 normalizado:", id_fiscal_1)
print("Dígito verificador     :", id_fiscal_1.digito_verificador)
print("Son equivalentes (1 y 2):", id_fiscal_1 == id_fiscal_2)
print("Elementos en el set    :", len(conjunto_fiscales))  # 1 y 2 colapsan al ser idénticos
print("Búsqueda en diccionario :", mapa_empresas[id_fiscal_2])
print("Excepción al intentar mutar:", tipo_error)
```

Explicación de ingeniería:

- `frozen=True` garantiza que los atributos de la entidad no puedan ser alterados tras la construcción, protegiendo contra mutaciones accidentales en arquitecturas concurrentes o distribuidas.
- Al ser inmutable, `@dataclass` genera automáticamente un método `__hash__` que combina los hashes de sus campos, permitiendo indexar las instancias en estructuras de búsqueda $O(1)$ como `dict` o `set`.
- El método `__post_init__` normaliza el código de país a mayúsculas (`ES`) y calcula el dígito verificador matemático. Debido a que la clase es inmutable, se utiliza `object.__setattr__(self, ...)` para escribir los campos calculados antes de sellar el objeto definitivamente.

Resultado esperado:

```text
Registro 1 normalizado: ClaveIdentidadFiscal(pais='ES', numero_identificacion='12345678', digito_verificador=6)
Dígito verificador     : 6
Son equivalentes (1 y 2): True
Elementos en el set    : 2
Búsqueda en diccionario : Soluciones Cloud S.L.
Excepción al intentar mutar: FrozenInstanceError
```

## 6. Aplicaciones en el mundo real

- **Modelos de Dominio y Value Objects en Arquitectura Hexagonal / DDD:** representación pura de conceptos inmutables de negocio (importes monetarios, direcciones físicas, coordenadas GPS, identificadores compuestos).
- **Consumo y Deserialización de APIs REST:** estructuración de cargas útiles tipadas intermedias entre formatos de red ([JSON](../../Intermedio/chapter-three/archivos_json.md)) y la lógica de aplicación.
- **Configuraciones de Despliegue e Infraestructura:** lectura estructurada de archivos de configuración donde los valores no deben mutar durante el ciclo de vida del servicio.
- **Pipeline de Datos y Machine Learning:** estructuración de lotes de entrenamiento heterogéneos con metadatos asociados.

## 7. Uso en producción

- **Habilitar `slots=True` en Python 3.10+ para reducir el consumo de RAM:** declarar `@dataclass(slots=True)` genera clases que utilizan `__slots__` en lugar del diccionario dinámico `__dict__`, ahorrando hasta un 40 % de memoria por instancia y acelerando el acceso a atributos.
- **Utilizar `frozen=True` por defecto en Objetos de Valor (*Value Objects*):** diseñar entidades inmutables siempre que sea posible; los objetos inmutables son inherentemente seguros ante hilos concurrentes y eliminan efectos secundarios inesperados.
- **Nunca asignar listas o diccionarios mutables directamente como valor por defecto:** escribir `etiquetas: list[str] = []` dispara un error inmediato de Python (`ValueError: mutable default ... is not allowed`); debe utilizarse obligatoriamente `field(default_factory=list)`.
- **Elegir entre `dataclass` y `pydantic` según el caso de uso:** utilizar `dataclass` nativo para modelos de dominio puros y estructuras internas de alto rendimiento sin dependencias externas; reservar Pydantic para los límites del sistema (validación de peticiones HTTP externas, coerciones complejas y generación de esquemas OpenAPI).

## 8. Errores comunes y recomendaciones

1. **Definir campos obligatorios después de campos con valores predeterminados (`SyntaxError`).**

```python
from dataclasses import dataclass


# ERROR: un campo sin valor por defecto no puede ir tras uno con valor por defecto
# @dataclass
# class ErrorOrden:
#     nombre: str = "Desconocido"
#     edad: int  # SyntaxError: non-default argument 'edad' follows default argument
```

Diagnóstico: el constructor `__init__` autogenerado respeta el orden léxico de los campos; en la sintaxis de Python los parámetros obligatorios deben preceder siempre a los parámetros opcionales. Recomendación: declarar primero todos los atributos obligatorios y al final los atributos con valores por defecto.

2. **Intentar modificar atributos en una clase `frozen=True` dentro de `__post_init__` mediante asignación regular.**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class InmutableRoto:
    precio: float

    def __post_init__(self):
        # ERROR: FrozenInstanceError: cannot assign to field 'precio'
        # self.precio = round(self.precio, 2)
        object.__setattr__(self, "precio", round(self.precio, 2))  # Corrección correcta
```

Diagnóstico: al estar congelada la clase, el descriptor intercepta cualquier asignación sobre `self`. Recomendación: utilizar la llamada de bajo nivel `object.__setattr__(self, 'campo', valor)`.

3. **Modificar colecciones mutables dentro de una clase declarada como `frozen=True`.**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SeguridadEnganosa:
    roles: list[str]


instancia = SeguridadEnganosa(roles=["lector"])
# frozen=True impide reasignar instancia.roles = ["admin"],
# pero NO impide mutar la lista interna:
instancia.roles.append("superadmin")  # Modifica la lista sin error
```

Diagnóstico: `frozen=True` congela las referencias de los atributos, no los objetos a los que apuntan (*shallow immutability*). Recomendación: si se requiere inmutabilidad profunda, utilizar tipos inmutables como `tuple` en lugar de `list`: `roles: tuple[str, ...]`.

## 9. Resumen

- El módulo **`dataclasses`** (**PEP 557**) automatiza la generación de métodos especiales (`__init__`, `__repr__`, `__eq__`) para clases centradas en almacenar datos.
- La función **`field()`** permite configurar valores por defecto mutables mediante `default_factory`, excluir campos sensibles de la representación con `repr=False` o del cálculo de igualdad con `compare=False`.
- El parámetro **`frozen=True`** crea objetos inmutables de solo lectura y genera automáticamente `__hash__`, permitiendo utilizarlos en `set` y como claves de `dict`.
- El método especial **`__post_init__`** actúa como gancho de validación de invariantes y cálculo de atributos derivados tras la inicialización.
- Las funciones auxiliares **`asdict()`** y **`astuple()`** facilitan la conversión bidireccional entre clases de datos y estructuras nativas de Python.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/dataclasses.html> — Biblioteca estándar (`dataclasses`): especificación formal, parámetros de `@dataclass`, funciones de campo y funciones de conveniencia.
- <https://peps.python.org/pep-0557/> — PEP 557 (*Data Classes*): diseño fundacional y justificación arquitectónica de las clases de datos en Python.
- <https://peps.python.org/pep-0681/> — PEP 681 (*Data Class Transforms*): compatibilidad estática y transformación de clases de datos en analizadores estáticos.

