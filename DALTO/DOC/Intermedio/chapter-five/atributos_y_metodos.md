# Atributos de Instancia y de Clase, Tipos de Métodos y Optimización con `__slots__`

## 2. Introducción

Una vez comprendido qué son las [clases y objetos](clases_y_objetos.md), el diseño efectivo en Programación Orientada a Objetos exige decidir con precisión **dónde reside cada dato** y **qué vínculo mantiene cada operación con la clase o con sus ejemplares**. En los scripts iniciales (`Clases_y_Objetos.py` L52-159, `Metodos.py` L37-84) aparecen atributos compartidos por todos los objetos frente a atributos propios de cada instancia, así como funciones incorporadas dentro de una clase que reciben `self`.

Profundizar en la mecánica interna de atributos y métodos en Python resulta determinante por cuatro razones de ingeniería:

1. **Resolución determinista de nombres y sombreado (*shadowing*):** comprender el orden de búsqueda entre `obj.__dict__` y `Clase.__dict__` evita errores al reasignar atributos de clase desde una instancia (`Clases_y_Objetos.py` L55-56).
2. **Prevención de estado mutable compartido:** declarar colecciones mutables a nivel de clase provoca contaminación cruzada entre instancias aparentemente independientes.
3. **Selección adecuada del tipo de método:** distinguir entre métodos de instancia (`self`), métodos de clase (`@classmethod` con `cls`, como `dict.fromkeys` en `CLASS_TWO_DICCIONARIOS.py` L75) y métodos estáticos (`@staticmethod`) habilita constructores alternativos polimórficos y utilidades cohesivas.
4. **Eficiencia de memoria a gran escala:** en cargas de producción sobre **CPython** con millones de instancias, sustituir diccionarios dinámicos por `__slots__` reduce drásticamente el consumo de RAM.

## 3. Fundamentos y conceptos

**Atributos de instancia frente a atributos de clase.** En `Clases_y_Objetos.py` (L53, L61, L95) se denominan "atributos estáticos" a las variables definidas directamente en el cuerpo de `class Celular:`. En la terminología oficial de Python se distinguen formalmente como **atributos de clase** frente a **atributos de instancia**:

- **Atributos de instancia (`self.atributo`):** se asignan habitualmente dentro de `__init__` (`Clases_y_Objetos.py` L139-148, `One.py` L107-109) y se almacenan en el diccionario privado de cada ejemplar (`obj.__dict__`, inspeccionado en `Crear_Clase.py` L89). Cada objeto conserva su propia copia independiente.
- **Atributos de clase (`Clase.atributo`):** se declaran en el nivel superior del bloque `class` fuera de cualquier método. Residen en un único espacio compartido (`Clase.__dict__`, expuesto como un `mappingproxy` de solo lectura directa) y son visibles tanto desde la clase (`Celular.marca`) como desde cualquiera de sus instancias (`celular1.marca`). Son idóneos para constantes simbólicas, tasas por defecto, esquemas de configuración o contadores globales de serie.

**Orden de búsqueda de atributos (*attribute lookup*) y sombreado (*shadowing*).** Cuando se evalúa la lectura `obj.x` (en ausencia de descriptores de datos como `@property`, estudiados en [encapsulamiento](encapsulamiento.md)), Python sigue una cadena estricta:

```text
Lectura: obj.x
   │
   ├──► 1. ¿'x' está en obj.__dict__? ─────────► Sí: retorna valor propio de la instancia
   │         │ No
   ├──► 2. ¿'x' está en type(obj).__dict__? ───► Sí: retorna atributo de la clase concreta
   │         │ No
   └──► 3. Busca en las superclases según el MRO ─► Si no existe en ninguna: AttributeError
```

Este mecanismo explica un matiz crucial respecto de `Clases_y_Objetos.py` (L55-56, L97-98): cuando `camara = "48MP"` es un atributo de clase y se ejecuta la **asignación** `celular1.camara = "50MP"` sobre una instancia, Python **no modifica** `Celular.camara`. En su lugar, crea una entrada nueva `'camara': '50MP'` dentro de `celular1.__dict__`, la cual **oculta o sombrea** (*shadows*) al atributo de clase únicamente para `celular1`, mientras `celular2.camara` continúa leyendo `"48MP"`. Si posteriormente se ejecuta `del celular1.camara`, desaparece la clave local y `celular1.camara` vuelve a resolver `"48MP"` desde la clase. Para alterar el valor compartido para todas las instancias sin copia local, la asignación debe efectuarse explícitamente sobre la clase: `Celular.camara = "50MP"`.

**La trampa del atributo de clase mutable.** El comportamiento cambia radicalmente cuando el atributo de clase apunta a un objeto **mutable** ([listas](../../Basico/chapter-two/listas.md), [diccionarios](../chapter-one/diccionarios.md) o [conjuntos](../chapter-one/conjuntos.md)) y se muta *in situ* sin reasignación (`obj.lista.append(x)`): dado que `append` solo lee `obj.lista`, no encuentra `'lista'` en `obj.__dict__`, recupera la única lista alojada en `Clase.__dict__` y modifica ese contenedor compartido, afectando silenciosamente a todas las instancias pasadas y futuras. Todo estado mutable propio de un ejemplar debe inicializarse siempre dentro de `__init__`.

**Mecánica de los métodos de instancia (*bound methods*).** Como señala `Metodos.py` (L13, L46-48, L70-73), sintácticamente un método de instancia es una [función](../chapter-two/funciones.md) definida dentro del cuerpo de la clase cuyo primer parámetro es `self`. Internamente, `CellPhone.llamar` es un objeto `function` ordinario; sin embargo, al acceder a él a través de una instancia (`cel1.llamar`), entra en acción el protocolo descriptor (`function.__get__`), que construye al vuelo un **método enlazado** (*bound method*) que empaqueta la función junto con la referencia `cel1`. Por ello, estas dos expresiones son exactamente equivalentes:

```text
cel1.llamar()              # Invocación sobre método enlazado (idiomática)
CellPhone.llamar(cel1)     # Invocación desatada sobre la clase pasando self explícitamente
```

Conviene atender también la observación crítica de diseño anotada en el propio comentario de `Metodos.py` (L15): solicitar y validar el nombre de un usuario mediante `input()` (`funcion_name(self)` en L50-68) no modela una acción legítima de un teléfono móvil, sino captura de interfaz externa que debe residir fuera de la entidad.

**Métodos de clase (`@classmethod`) y constructores alternativos.** Aplicando el [decorador](../../Avanzado/chapter-one/decoradores.md) integrado `@classmethod` (presentado en la documentación interna de `Abastraccion.py` L116-131), el método deja de recibir una instancia `self` y recibe siempre la **propia clase `cls`** como primer argumento, tanto si se invoca como `Clase.metodo(...)` como si se llama desde un ejemplar `obj.metodo(...)`. Su aplicación primordial en arquitectura Python son los **constructores alternativos (fábricas)**: dado que Python solo admite un único método `__init__` por clase, `@classmethod` permite ofrecer puntos de entrada adicionales con nombres semánticos (`desde_json`, `desde_linea_csv`, `estandar`). La biblioteca estándar utiliza este patrón extensivamente: `dict.fromkeys(iterable, valor)` —empleado en `CLASS_TWO_DICCIONARIOS.py` (L75-88)— es un `@classmethod` de `dict`, al igual que `int.from_bytes()` o `datetime.fromisoformat()`. Usar `return cls(...)` en lugar de fijar el nombre rígido de la clase base garantiza que, cuando una subclase herede el método ([herencia](herencia.md)), `Subclase.desde_linea_csv(...)` retorne correctamente una instancia de `Subclase`.

**Métodos estáticos (`@staticmethod`) frente a funciones de módulo.** Un método decorado con `@staticmethod` no recibe implícitamente ni `self` ni `cls`: funciona como una función regular alojada dentro del espacio de nombres de la clase. No puede leer ni mutar el estado de una instancia ni construir polimórficamente subclases mediante `cls`. En Python idiomático conviene aplicar un criterio claro al elegir entre `@staticmethod` y una función a nivel de [módulo](../chapter-three/modulos.md):

- Se prefiere **`@staticmethod`** cuando se trata de una operación auxiliar pura estrechamente ligada al dominio conceptual de la clase (p. ej. `Dispositivo.validar_imei(cadena)` o `Temperatura.celsius_a_kelvin(c)`) que mejora la descubribilidad al viajar junto a la clase o que una subclase podría necesitar redefinir.
- Se prefiere una **función de módulo** (privada `_auxiliar()` o pública) cuando la utilidad es transversal a varias clases del archivo o no guarda relación semántica exclusiva con un único tipo.

**Optimización de memoria con `__slots__` en CPython.** Por defecto, cada instancia de una clase definida por el usuario aloja su propio diccionario dinámico `__dict__` (una tabla hash redimensionable). Cuando un servicio procesa unos pocos miles de objetos, esta flexibilidad resulta ideal; pero cuando mantiene en memoria **millones de instancias pequeñas** (puntos geográficos, velas financieras, nodos de un árbol sintáctico), la sobrecarga de miles de tablas hash domina el consumo de RAM. Declarar el atributo de clase `__slots__ = ("x", "y", "z")` instruye a **CPython** para suprimir la creación de `__dict__` (y `__weakref__`, salvo que se incluya explícitamente) en cada instancia, reservando en su lugar un arreglo compacto de punteros de tamaño fijo gestionado por descriptores a nivel de clase. Esto reduce notablemente la huella en memoria y acelera ligeramente la lectura de atributos, a cambio de impedir agregar atributos arbitrarios no declarados en `__slots__`.

## 4. Sintaxis y funcionamiento

Comparativa sintáctica integrada de atributos y los tres tipos de métodos:

```text
class Entidad:
    ATRIBUTO_CLASE = "valor_compartido"          # En Entidad.__dict__

    def __init__(self, dato: str) -> None:
        self.dato = dato                         # En instancia.__dict__

    def metodo_instancia(self) -> str:           # Recibe la instancia `self`
        return f"{self.dato} ({self.ATRIBUTO_CLASE})"

    @classmethod
    def desde_texto(cls, crudo: str) -> "Entidad":  # Recibe la clase `cls`
        return cls(crudo.strip().upper())

    @staticmethod
    def es_formato_valido(crudo: str) -> bool:   # No recibe ni `self` ni `cls`
        return len(crudo.strip()) >= 3
```

Referencia de elementos, accesos y mecanismos de almacenamiento:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `self.attr = val` | Crea o actualiza un atributo exclusivo en `self.__dict__` | `self.modelo = "S25"` |
| 2 | `attr_clase = val` | Declara en el bloque `class` un atributo compartido en `Clase.__dict__` | `iva_general = 0.18` |
| 3 | `Clase.attr_clase = v` | Modifica el atributo de clase para todas las instancias sin sombreado | `Producto.iva_general = 0.19` |
| 4 | `obj.attr_clase = v` | Crea una clave local en `obj.__dict__` que sombrea a `Clase.attr_clase` | `prod1.iva_general = 0.0` |
| 5 | `def m(self, ...):` | Método de instancia; enlaza automáticamente `obj` al parámetro `self` | `def llamar(self) -> str:` |
| 6 | `@classmethod` | Método de clase; enlaza la clase receptora `cls` (constructores fábrica) | `@classmethod def from_csv(cls, s):` |
| 7 | `@staticmethod` | Función agrupada en la clase sin inyección automática de `self` ni `cls` | `@staticmethod def validar(x):` |
| 8 | `getattr(o, k, def)` | Obtiene dinámicamente un atributo por nombre con respaldo opcional | `getattr(cel, "red", "5G")` |
| 9 | `hasattr(o, k)` / `setattr(o, k, v)` | Comprueba existencia o asigna dinámicamente un atributo por nombre | `setattr(cel, "activo", True)` |
| 10 | `__slots__ = (...)` | Suprime `__dict__` por instancia reemplazándolo por ranuras fijas | `__slots__ = ("lat", "lon")` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Contraste entre atributos de clase y atributos de instancia, sombreado local (*shadowing*) y restauración con `del`.**

```python
class TerminalMovil:
    operadora_red = "RedGlobal-5G"  # Atributo de clase compartido

    def __init__(self, marca: str, modelo: str) -> None:
        self.marca = marca          # Atributo de instancia
        self.modelo = modelo        # Atributo de instancia

    def resumen_conexion(self) -> str:
        return f"{self.marca} {self.modelo} conectado a {self.operadora_red}"


t1 = TerminalMovil("Samsung", "S25")
t2 = TerminalMovil("Apple", "iPhone 16")

print("Inicial t1:", t1.resumen_conexion())
print("Inicial t2:", t2.resumen_conexion())
print("¿'operadora_red' en t1.__dict__?:", "operadora_red" in t1.__dict__)

# Asignar sobre t1 sombrea el atributo solo en t1.__dict__
t1.operadora_red = "Roaming-Local"
print("Tras sombrear t1 -> t1:", t1.operadora_red, "| t2:", t2.operadora_red)
print("¿'operadora_red' en t1.__dict__?:", "operadora_red" in t1.__dict__)

# Modificar el atributo en la clase actualiza a todas las instancias no sombreadas
TerminalMovil.operadora_red = "Satelital-6G"
print("Tras cambio en clase -> t1:", t1.operadora_red, "| t2:", t2.operadora_red)

# Eliminar la clave local de t1 descubre nuevamente el atributo de clase
del t1.operadora_red
print("Tras del t1.operadora_red -> t1:", t1.operadora_red)
```

Explicación paso a paso:

- Clarificando `Clases_y_Objetos.py` (L53-64, L95-98), al inicio `t1.__dict__` solo contiene `'marca'` y `'modelo'`; `t1.operadora_red` se resuelve subiendo a `TerminalMovil.__dict__`.
- Al asignar `t1.operadora_red = "Roaming-Local"` nace un atributo de instancia que oculta `TerminalMovil.operadora_red` exclusivamente para `t1`. Al borrar esa entrada con `del t1.operadora_red`, la búsqueda vuelve a alcanzar el valor vigente en la clase (`"Satelital-6G"`).

Resultado esperado:

```text
Inicial t1: Samsung S25 conectado a RedGlobal-5G
Inicial t2: Apple iPhone 16 conectado a RedGlobal-5G
¿'operadora_red' en t1.__dict__?: False
Tras sombrear t1 -> t1: Roaming-Local | t2: RedGlobal-5G
¿'operadora_red' en t1.__dict__?: True
Tras cambio en clase -> t1: Roaming-Local | t2: Satelital-6G
Tras del t1.operadora_red -> t1: Satelital-6G
```

### Intermedio

**Ejemplo 2 — Sinergia entre métodos de instancia, constructores alternativos con `@classmethod` (respetando subclases) y validación con `@staticmethod`.**

```python
class CotizacionMoneda:
    MONEDA_BASE = "USD"

    def __init__(self, codigo_iso: str, tasa_cambio: float) -> None:
        if not self.es_codigo_iso_valido(codigo_iso):
            raise ValueError(f"Código ISO inválido: {codigo_iso!r}")
        if tasa_cambio <= 0:
            raise ValueError("La tasa de cambio debe ser positiva")
        self.codigo_iso = codigo_iso
        self.tasa_cambio = tasa_cambio

    def convertir_desde_base(self, monto_base: float) -> float:
        return round(monto_base * self.tasa_cambio, 2)

    @classmethod
    def desde_cadena(cls, registro: str) -> "CotizacionMoneda":
        codigo_crudo, tasa_cruda = registro.split(":")
        return cls(codigo_crudo.strip().upper(), float(tasa_cruda))

    @staticmethod
    def es_codigo_iso_valido(codigo: str) -> bool:
        return len(codigo) == 3 and codigo.isalpha() and codigo.isupper()


class CotizacionPreferencial(CotizacionMoneda):
    """Subclase que aplica una bonificación porcentual adicional."""

    def convertir_desde_base(self, monto_base: float) -> float:
        return round(monto_base * self.tasa_cambio * 1.02, 2)


pen = CotizacionMoneda.desde_cadena(" pen : 3.75 ")
pen_vip = CotizacionPreferencial.desde_cadena(" pen : 3.75 ")
plantilla_tasas = dict.fromkeys(("PEN", "EUR", "CLP"), 1.0)

print("Validez ISO ('PEN', 'pe1'):", CotizacionMoneda.es_codigo_iso_valido("PEN"), CotizacionMoneda.es_codigo_iso_valido("pe1"))
print("Tipo construido en base    :", type(pen).__name__, "->", pen.convertir_desde_base(100))
print("Tipo construido en subclase:", type(pen_vip).__name__, "->", pen_vip.convertir_desde_base(100))
print("Equivalencia bound/unbound :", pen.convertir_desde_base(50) == CotizacionMoneda.convertir_desde_base(pen, 50))
print("dict.fromkeys integrado    :", plantilla_tasas)
```

Explicación técnica:

- Siguiendo el patrón nativo de `dict.fromkeys` (`CLASS_TWO_DICCIONARIOS.py` L75-88) y la introducción a `@classmethod` de `Abastraccion.py` (L116-131), `desde_cadena(cls, ...)` parsea registros textuales e invoca `cls(...)`. Cuando se llama desde `CotizacionPreferencial`, `cls` apunta automáticamente a `CotizacionPreferencial` y entrega una instancia de la subclase.
- `es_codigo_iso_valido` se modela como `@staticmethod` porque verifica una regla léxica pura del dominio cambiario sin requerir estado de instancia (`self`) ni referencia de clase (`cls`).

Resultado esperado:

```text
Validez ISO ('PEN', 'pe1'): True False
Tipo construido en base    : CotizacionMoneda -> 375.0
Tipo construido en subclase: CotizacionPreferencial -> 382.5
Equivalencia bound/unbound : True
dict.fromkeys integrado    : {'PEN': 1.0, 'EUR': 1.0, 'CLP': 1.0}
```

### Avanzado

**Ejemplo 3 — Optimización estructural con `__slots__` frente a clases estándar con `__dict__` en telemetría de alto volumen.**

```python
import sys


class MuestraConDict:
    def __init__(self, sensor_id: str, temperatura: float, humedad: float) -> None:
        self.sensor_id = sensor_id
        self.temperatura = temperatura
        self.humedad = humedad


class MuestraConSlots:
    __slots__ = ("sensor_id", "temperatura", "humedad")

    def __init__(self, sensor_id: str, temperatura: float, humedad: float) -> None:
        self.sensor_id = sensor_id
        self.temperatura = temperatura
        self.humedad = humedad

    def indice_calor_simple(self) -> float:
        return round(self.temperatura + 0.05 * self.humedad, 2)


m_dict = MuestraConDict("S-01", 24.5, 60.0)
m_slot = MuestraConSlots("S-01", 24.5, 60.0)

bytes_dict = sys.getsizeof(m_dict) + sys.getsizeof(m_dict.__dict__)
bytes_slot = sys.getsizeof(m_slot)

print("¿m_dict tiene __dict__?:", hasattr(m_dict, "__dict__"))
print("¿m_slot tiene __dict__?:", hasattr(m_slot, "__dict__"))
print("¿__slots__ ahorra memoria frente a objeto+__dict__?:", bytes_slot < bytes_dict)
print("Índice calculado en m_slot:", m_slot.indice_calor_simple())

try:
    m_slot.ubicacion_extra = "Azotea"
except AttributeError as err:
    print("Bloqueo de atributo no declarado:", type(err).__name__)
```

Explicación de arquitectura:

- `MuestraConDict` aloja tanto la cabecera del objeto como un diccionario `__dict__` independiente; `MuestraConSlots` prescinde de `__dict__` y almacena las tres referencias en ranuras contiguas predefinidas (`bytes_slot < bytes_dict` resulta garantizadamente `True` en CPython).
- Además del ahorro de memoria, `__slots__` actúa como barrera contra errores tipográficos al asignar atributos (`m_slot.ubicacion_extra = ...` dispara inmediatamente `AttributeError` en lugar de crear silenciosamente un atributo fantasma).

Resultado esperado:

```text
¿m_dict tiene __dict__?: True
¿m_slot tiene __dict__?: False
¿__slots__ ahorra memoria frente a objeto+__dict__?: True
Índice calculado en m_slot: 27.5
Bloqueo de atributo no declarado: AttributeError
```

## 6. Aplicaciones en el mundo real

- **Constructores fábrica de deserialización (`@classmethod`):** modelos de dominio y clientes SDK exponen métodos como `EventoPago.from_webhook_payload(data)` o `Configuracion.from_env()`, concentrando la conversión de formatos crudos sin sobrecargar `__init__`.
- **Procesamiento masivo de grafos, ASTs y series temporales (`__slots__`):** motores de plantillas, compiladores, bibliotecas financieras y clientes de métricas definen `__slots__` en nodos o *ticks* que se instancian por millones en memoria RAM.
- **Introspección dinámica en serializadores y adaptadores (`getattr` / `__dict__`):** exportadores a JSON/CSV (siguiendo la idea embrionaria de `Crear_Clase.py` L89-93) inspeccionan dinámicamente atributos registrados para construir filas o esquemas sin repetir nombres campo por campo.
- **Constantes y políticas por clase:** definición de códigos de versión de protocolo, tablas de transición o tiempos máximos de espera (`TIMEOUT_SEGUNDOS = 5.0`) como atributos de clase sobrescribibles por subclase.

## 7. Uso en producción

- **Inicializar todo estado mutable dentro de `__init__`:** a nivel de clase solo deben residir valores inmutables (`int`, `float`, `str`, `tuple`, `frozenset`). Si se requiere una estructura constante de consulta en la clase, utilice tuplas o `types.MappingProxyType` para impedir mutaciones accidentales en tiempo de ejecución.
- **Fijar el nombre en mayúsculas para constantes de clase (`PEP 8`):** distinguir visualmente constantes compartidas (`MAX_REINTENTOS = 3`) respecto de atributos de estado por instancia (`self.intentos_actuales = 0`) evita asignaciones equívocas `self.MAX_REINTENTOS = ...`.
- **Usar siempre `cls(...)` dentro de `@classmethod`:** jamás codificar el nombre literal de la clase anfitriona dentro de un método de clase fábrica; delegar en `cls(...)` garantiza compatibilidad automática con futuras subclases.
- **Considerar `__slots__` de forma deliberada en jerarquías:** si una subclase hereda de una clase con `__slots__`, la subclase también debe declarar su propio `__slots__` (conteniendo únicamente los atributos nuevos, sin repetir los de la base); de lo contrario, la subclase volverá a crear `__dict__` en sus instancias, diluyendo la optimización de memoria.

## 8. Errores comunes y recomendaciones

1. **Declarar una lista o diccionario mutable como atributo de clase creyendo que cada instancia tendrá el suyo.**

```python
class CarritoDefectuoso:
    items: list[str] = []  # Trampa: lista única compartida en CarritoDefectuoso.__dict__

    def agregar(self, producto: str) -> None:
        self.items.append(producto)


class CarritoCorrecto:
    def __init__(self) -> None:
        self.items: list[str] = []  # Lista nueva e independiente por cada instancia

    def agregar(self, producto: str) -> None:
        self.items.append(producto)


mal_a = CarritoDefectuoso()
mal_b = CarritoDefectuoso()
mal_a.agregar("Teclado")
print("Defectuoso (mal_b contaminado):", mal_b.items, "| misma lista:", mal_a.items is mal_b.items)

bien_a = CarritoCorrecto()
bien_b = CarritoCorrecto()
bien_a.agregar("Teclado")
print("Correcto   (bien_b aislado)   :", bien_b.items, "| misma lista:", bien_a.items is bien_b.items)
```

Resultado esperado:

```text
Defectuoso (mal_b contaminado): ['Teclado'] | misma lista: True
Correcto   (bien_b aislado)   : [] | misma lista: False
```

Diagnóstico: `self.items.append(...)` no reasigna `self.items`, sino que muta el objeto lista recuperado desde `CarritoDefectuoso.__dict__`. Recomendación: crear siempre colecciones mutables dentro de `__init__`.

2. **Incrementar un contador global mediante `self.contador += 1` en lugar de `Clase.contador += 1`.**

```python
class TicketSoporte:
    emitidos = 0

    def registrar_mal(self) -> None:
        # Equivale a self.emitidos = self.emitidos + 1 -> sombrea en self.__dict__
        self.emitidos += 1

    @classmethod
    def registrar_bien(cls) -> None:
        cls.emitidos += 1


t1 = TicketSoporte()
t2 = TicketSoporte()
t1.registrar_mal()
t2.registrar_mal()
print("Tras registrar_mal -> TicketSoporte.emitidos:", TicketSoporte.emitidos, "| t1:", t1.emitidos)

TicketSoporte.registrar_bien()
TicketSoporte.registrar_bien()
print("Tras registrar_bien -> TicketSoporte.emitidos:", TicketSoporte.emitidos)
```

Resultado esperado:

```text
Tras registrar_mal -> TicketSoporte.emitidos: 0 | t1: 1
Tras registrar_bien -> TicketSoporte.emitidos: 2
```

Diagnóstico: la sentencia aumentada `self.emitidos += 1` lee `0` desde la clase, suma `1` y escribe el resultado `1` en `self.__dict__['emitidos']`, dejando intacto `TicketSoporte.emitidos == 0`. Recomendación: mutar el estado de clase explícitamente a través de la clase o mediante un `@classmethod` (`cls.emitidos += 1`).

3. **Confundir la firma de `@classmethod` y `@staticmethod` omitiendo `cls` o esperando `self`.**

```python
# ERROR INTENCIONAL: un @staticmethod no recibe self ni cls de manera implícita
class ConversorUnidades:
    factor_base = 1000

    @staticmethod
    def km_a_metros(distancia_km: float) -> float:
        return distancia_km * self.factor_base  # NameError: name 'self' is not defined
```

Diagnóstico: `@staticmethod` desactiva por completo la inyección de instancia o clase. Si el método necesita consultar `cls.factor_base` (permitiendo que una subclase redefina `factor_base`), debe declararse como `@classmethod` recibiendo `cls` como primer parámetro.

## 9. Resumen

- Los **atributos de instancia** se alojan individualmente en `obj.__dict__`, mientras que los **atributos de clase** viven de forma compartida en `Clase.__dict__`.
- Al leer `obj.attr`, Python inspecciona primero `obj.__dict__`, luego `type(obj).__dict__` y finalmente las superclases; asignar `obj.attr = valor` escribe en `obj.__dict__` y sombrea cualquier atributo homónimo de la clase.
- Nunca deben declararse colecciones mutables (`list`, `dict`, `set`) como atributos de clase si representan estado individual de cada ejemplar.
- Python ofrece tres categorías de métodos: **de instancia** (`self`, enlazados al ejemplar), **de clase** (`@classmethod` con `cls`, idóneos para constructores fábrica polimórficos como `dict.fromkeys`) y **estáticos** (`@staticmethod`, funciones auxiliares cohesivas sin acceso implícito a instancia ni clase).
- En **CPython**, definir `__slots__` elimina el diccionario `__dict__` por ejemplar, optimizando sustancialmente el consumo de memoria en colecciones masivas de objetos e impidiendo atributos accidentales por errores de escritura.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clases_y_Objetos.py` (L52-159) | `Clases_y_Objetos.py` | Contraste entre "atributos estáticos" en `class Celular` (L59-64) y "atributos de instancia" inicializados en `CellPhone.__init__` (L135-159) | Se precisó la terminología formal (**atributos de clase**), el orden de búsqueda de atributos y el efecto real de sombreado al ejecutar `celular1.camara = "50MP"` (L56, L98) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clase_One_2.py` (L4-6, L32-34) | `Clase_One_2.py` | Distinción conceptual entre propiedades/atributos (características) y métodos (acciones) | Se articuló con el protocolo descriptor que transforma funciones de clase en métodos enlazados (*bound methods*) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Metodos.py` (L1-85) | `Metodos.py` | Comparación entre función externa `funcion_name()` y métodos `llamar(self)` / `cortar(self)` en `CellPhone` | Se demostró la equivalencia `obj.m() == Clase.m(obj)` y se retomó la nota crítica de L15 sobre no modelar capturas de consola como acciones de negocio |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py` (L107-115) | `One.py` | Atributos `self.name`, `self.age`, `self.grado` consumidos por `estudiar(self)` y `descansar(self)` | Se relacionó con el ciclo de vida del diccionario de instancia `self.__dict__` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Abastraccion.py` (L116-131) | `Abastraccion.py` | Explicación documental de `@classmethod` recibiendo `cls` para operar sobre la clase en lugar de una instancia | Se desarrolló su uso principal como constructor alternativo/fábrica compatible con herencia (`cls(...)`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_TWO/CLASE_TWO_PY/CLASS_TWO_DICCIONARIOS.py` (L72-94) | `CLASS_TWO_DICCIONARIOS.py` | Uso práctico de `dict.fromkeys(...)` con iterables y valores predeterminados | Se identificó `dict.fromkeys` como ejemplo canónico de `@classmethod` integrado en los tipos nativos de Python |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Crear_Clase.py` (L1-9, L87-98) | `Crear_Clase.py` | Método `moverse(self)` e iteración explícita sobre `(roca_One.__dict__).items()` | Se contrastó el almacenamiento flexible en `__dict__` con las ranuras fijas de `__slots__` |

**Fundamento complementario:** se incorporaron cuatro aspectos esenciales para un dominio completo del modelo de objetos: (1) el diseño y criterio de uso de **`@staticmethod`** frente a funciones a nivel de módulo (ausente en el material práctico original); (2) la trampa del atributo de clase mutable (`items = []`) y el error de incremento con `self.contador += 1`; (3) la mecánica de enlace de métodos (`Clase.m(obj)` frente a `obj.m()`) e introspección con `getattr`/`setattr`/`hasattr`; y (4) la optimización de memoria en **CPython** mediante `__slots__`.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables> — Tutorial oficial de Python (*Class and Instance Variables*): distinción entre variables de clase e instancia y riesgo con objetos mutables compartidos.
- <https://docs.python.org/3/library/functions.html#classmethod> — Biblioteca estándar (`@classmethod`): semántica del decorador de métodos de clase y constructores alternativos.
- <https://docs.python.org/3/library/functions.html#staticmethod> — Biblioteca estándar (`@staticmethod`): definición de métodos estáticos y diferencia respecto de funciones de módulo.
- <https://docs.python.org/3/reference/datamodel.html#slots> — Referencia del modelo de datos (*`__slots__`*): reserva de espacio fijo, supresión de `__dict__` y reglas de herencia con ranuras.
