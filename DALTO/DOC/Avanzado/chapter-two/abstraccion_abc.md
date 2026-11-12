# Abstracción Formal con Clases Base Abstractas (módulo abc) y Protocolos en Python

## 2. Introducción

La **abstracción** constituye uno de los pilares esenciales de la programación orientada a objetos y del diseño arquitectónico de software. Consiste en definir un límite cognitivo riguroso que oculta los detalles de implementación interna y expone únicamente los contratos esenciales y la especificación de comportamiento relevante para los consumidores (`Abastraccion.py` L2-7).

En Python conviven dos aproximaciones metodológicas para modelar la abstracción:

1. **Abstracción informal mediante excepciones en tiempo de ejecución:** una clase base convencional cuyos métodos declaran `raise NotImplementedError` (`OCP.py` L40). Bajo este esquema, la omisión de un método requerido solo se manifiesta cuando el flujo del programa llega a invocar la función específica en tiempo de ejecución, permitiendo crear instancias incompletas de manera silenciosa.
2. **Abstracción formal garantizada en tiempo de instanciación:** mediante el módulo estándar `abc` (*Abstract Base Classes*, PEP 3119), el intérprete de Python intercepta el ciclo de vida del objeto impidiendo que cualquier clase con métodos abstractos no resueltos sea instanciada, lanzando inmediatamente un error inequívoco:
   ```text
   TypeError: Can't instantiate abstract class Subclase with abstract method ...
   ```

Comprender en profundidad el módulo `abc`, la combinación de `@abstractmethod` con descriptores como `@property`, `@classmethod` y `@staticmethod`, el mecanismo de registro de subclases virtuales (`ABCMeta.register` y `__subclasshook__`), y la comparación con el subtipado estructural estático (*Protocols*, PEP 544) resulta indispensable para estructurar arquitecturas desacopladas, patrones de puertos y adaptadores (*Hexagonal Architecture*) y sistemas de extensiones o complementos (*plugins*).

## 3. Fundamentos y conceptos

### La abstracción como límite cognitivo y contrato formal

El propósito primario de una abstracción es desacoplar el **qué** (la interfaz de comportamiento garantizada) del **cómo** (la implementación concreta y particular en algoritmos o tecnologías de persistencia).

En `Abastraccion.py` (L9-41), se expone una primera aproximación mediante la clase `Auto`, donde métodos de alto nivel como `conducir()` o `parar()` coordinan internamente el atributo privado `self.__estado`. No obstante, cuando múltiples clases deben compartir una interfaz común intercambiable de forma polimórfica —como notificadores (`OCP.py` L31-41), trabajadores (`ISP.py` L14-27) o verificadores ortográficos (`DIP.py` L45-49)—, la mera encapsulación interna resulta insuficiente: se requiere un **contrato formal de interfaz**.

### Abstracción informal vs. formalización con `abc.ABC`

| Criterio técnico | Abstracción informal (`raise NotImplementedError`) | Abstracción formal (`abc.ABC` + `@abstractmethod`) |
|---|---|---|
| Mecanismo de definición | Clases regulares que lanzan `raise NotImplementedError` en el cuerpo del método. | Clases que heredan de `abc.ABC` o usan `metaclass=abc.ABCMeta`, decorando métodos con `@abstractmethod`. |
| Momento de detección | **Tardío:** en tiempo de ejecución, únicamente al invocar el método omitido. | **Temprano:** en tiempo de instanciación, al evaluar `Subclase()`. |
| ¿Permite instanciar la clase base? | Sí, la clase base puede instanciarse por error si no se valida en `__init__`. | No; el intérprete bloquea la instanciación de cualquier clase con métodos abstractos. |
| Detección en herramientas estáticas | Difícil de rastrear mediante linters o comprobadores de tipos como `mypy`. | Nativa: analizadores estáticos y entornos de desarrollo alertan de inmediato sobre métodos faltantes. |

### La metaclase `ABCMeta` y el decorador `@abstractmethod`

El módulo estándar `abc` funciona mediante una metaclase especializada denominada `ABCMeta`. La clase utilitaria `abc.ABC` se proporciona por ergonomía sintáctica para no requerir la especificación manual `class MiBase(metaclass=ABCMeta):`.

Cuando una clase hereda de `ABC` y decora uno o varios métodos con `@abstractmethod`:

1. El decorador marca la función agregando internamente el atributo booleano `__isabstractmethod__ = True`.
2. Al crearse la clase, la metaclase `ABCMeta` recopila todos los identificadores que poseen dicha marca y los almacena en el atributo interno `__abstractmethods__` (un conjunto inmutable de nombres de métodos).
3. Al invocar el constructor `Subclase(*args, **kwargs)` para instanciar un objeto, el despachador de CPython en `tp_new` verifica si `__abstractmethods__` contiene elementos. Si el conjunto no está vacío, aborta la instanciación con `TypeError`.

### Composición de `@abstractmethod` con descriptores y métodos de clase

En Python moderno, `@abstractmethod` puede combinarse armónicamente con otros decoradores del lenguaje. Para que el despacho funcione correctamente, **`@abstractmethod` debe situarse siempre como el decorador más interno** (más próximo a la sentencia `def`):

- **Propiedades abstractas:**
  ```text
  @property
  @abstractmethod
  def identificador(self) -> str:
      pass
  ```
- **Métodos de clase abstractos:**
  ```text
  @classmethod
  @abstractmethod
  def desde_configuracion(cls, ruta: str) -> "MiClase":
      pass
  ```
- **Métodos estáticos abstractos:**
  ```text
  @staticmethod
  @abstractmethod
  def validar_formato(cadena: str) -> bool:
      pass
  ```

> [!IMPORTANT]
> En la documentación original de `Abastraccion.py` (L124), el docstring presenta el fragmento erróneo `from abc import ABC, classmethod, abstractmethod`. En Python, `classmethod` y `staticmethod` son funciones integradas en el espacio global (*built-ins*), no componentes del módulo `abc`. Intentar importar `classmethod` desde `abc` produce un error inmediato `ImportError: cannot import name 'classmethod' from 'abc'`.

### Subclases virtuales: `ABCMeta.register` y `__subclasshook__`

Una de las facultades más potentes de las ABCs en Python reside en la posibilidad de registrar **subclases virtuales**. Una subclase virtual no hereda en su grafo de MRO de la clase base abstracta (evitando acoplamiento rígido de implementación), pero el sistema de tipos de Python la reconoce como miembro formal al invocar `isinstance()` o `issubclass()`:

1. **Registro explícito mediante `ABCMeta.register`:** invocar `MiABC.register(ClaseExterna)` incorpora la clase foránea en el registro de tipos reconocidos por `MiABC`.
2. **Validación estructural dinámica mediante `__subclasshook__`:** permite a una ABC inspeccionar si una clase candidata implementa determinados métodos o atributos requeridos, retornando `True` para formalizar la relación sin herencia explícita.

### Clases Base Abstractas frente a `typing.Protocol` (PEP 544)

Con la adopción de PEP 544, Python introdujo el soporte formal para el **subtipado estructural estático** (*Static Duck Typing*) a través de `typing.Protocol`:

- **ABCs (Subtipado nominal):** una clase debe derivar explícitamente de la base `class RepositorioSQL(RepositorioBase):` o registrarse mediante `.register()`. Su verificación opera tanto estáticamente como en tiempo de ejecución.
- **Protocols (Subtipado estructural):** cualquier clase que satisfaga los métodos y atributos tipados en el protocolo es compatible automáticamente, sin requerir declaración de herencia ni importación de la interfaz por parte del módulo que provee la implementación.

En arquitecturas empresariales, las ABCs se prefieren cuando se desea compartir código base protegido o forzar validaciones estrictas en tiempo de instanciación; los protocolos se eligen para desacoplar librerías independientes y habilitar contratos abiertos entre paquetes heterogéneos.

## 4. Sintaxis y funcionamiento

### Sintaxis idiomática de definición de interfaces abstractas

```text
from abc import ABC, abstractmethod

class ContratoServicio(ABC):
    @property
    @abstractmethod
    def clave(self) -> str:
        """Propiedad obligatoria que cada subclase debe proveer."""
        pass

    @abstractmethod
    def ejecutar(self, carga: bytes) -> bool:
        """Metodo de negocio obligatorio."""
        pass
```

Tabla de componentes y decoradores para abstracción formal:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `abc.ABC` | Clase auxiliar que vincula la metaclase `ABCMeta` a la definición. | `class Repositorio(ABC):` |
| 2 | `@abstractmethod` | Decorador que marca un método como pendiente de implementación obligatoria. | `@abstractmethod\ndef guardar(self):` |
| 3 | `@property` + `@abstractmethod` | Declara un getter obligatorio en las subclases concretas. | `@property\n@abstractmethod\ndef uri(self):` |
| 4 | `@classmethod` + `@abstractmethod` | Declara un método de clase abstracto (constructores alternativos). | `@classmethod\n@abstractmethod\ndef crear(cls):` |
| 5 | `@staticmethod` + `@abstractmethod` | Declara una función utilitaria obligatoria asociada al espacio de la clase. | `@staticmethod\n@abstractmethod\ndef validar():` |
| 6 | `ABCMeta.register(Clase)` | Registra una clase independiente como subclase virtual sin herencia física. | `Notificador.register(CanalWebhook)` |
| 7 | `__subclasshook__(cls, C)` | Método de clase en una ABC que valida duck-typing para `issubclass()`. | `def __subclasshook__(cls, C):` |
| 8 | `typing.Protocol` | Base para contratos estructurales estáticos evaluables mediante comprobadores de tipos. | `class Serializable(Protocol):` |

## 5. Ejemplos prácticos progresivos

### Básico

Contrato formal mediante `abc.ABC` y `@abstractmethod`. Se define un contrato unificado para procesadores de pago que previene la creación de clases incompletas y garantiza un despacho polimórfico determinista.

```python
from abc import ABC, abstractmethod


class ProcesadorPago(ABC):
    """Contrato formal que define las operaciones de pasarelas de pago."""
    def __init__(self, moneda: str) -> None:
        self.moneda = moneda.upper()

    @abstractmethod
    def procesar(self, monto_centavos: int) -> dict[str, str | int]:
        """Debe retornar el comprobante estructurado de la transaccion."""
        pass


class PasarelaTarjeta(ProcesadorPago):
    def procesar(self, monto_centavos: int) -> dict[str, str | int]:
        return {
            "estado": "APROBADO",
            "canal": "TARJETA_CREDITO",
            "monto": monto_centavos,
            "moneda": self.moneda,
        }


class PasarelaTransferencia(ProcesadorPago):
    def procesar(self, monto_centavos: int) -> dict[str, str | int]:
        return {
            "estado": "PENDIENTE_CONCILIACION",
            "canal": "TRANSFERENCIA_BANCARIA",
            "monto": monto_centavos,
            "moneda": self.moneda,
        }


def despachar_cobro(procesador: ProcesadorPago, monto: int) -> None:
    resultado = procesador.procesar(monto)
    print(f"[{resultado['canal']}] Estado: {resultado['estado']} por {resultado['monto']} {resultado['moneda']}")


tarjeta = PasarelaTarjeta("USD")
transferencia = PasarelaTransferencia("EUR")

despachar_cobro(tarjeta, 4500)
despachar_cobro(transferencia, 12000)
```

Resultado esperado:

```text
[TARJETA_CREDITO] Estado: APROBADO por 4500 USD
[TRANSFERENCIA_BANCARIA] Estado: PENDIENTE_CONCILIACION por 12000 EUR
```

### Intermedio

En este nivel se combinan propiedades abstractas (`@property` + `@abstractmethod`) con métodos de fábrica abstractos (`@classmethod` + `@abstractmethod`), implementando un contrato de repositorio para acceso a datos en arquitecturas desacopladas.

```python
from abc import ABC, abstractmethod
from typing import Any


class RepositorioEntidad(ABC):
    """Contrato con propiedad obligatoria y metodo de clase constructor."""
    @property
    @abstractmethod
    def nombre_tabla(self) -> str:
        """Debe devolver el identificador fisico del almacen de datos."""
        pass

    @classmethod
    @abstractmethod
    def desde_uri(cls, uri_conexion: str) -> "RepositorioEntidad":
        """Fabrica de instancia a partir de una cadena de conexion."""
        pass

    @abstractmethod
    def guardar(self, id_registro: str, datos: dict[str, Any]) -> bool:
        """Persiste el registro en la tabla."""
        pass


class RepositorioMemoria(RepositorioEntidad):
    def __init__(self, uri_conexion: str) -> None:
        self._uri = uri_conexion
        self._almacen: dict[str, dict[str, Any]] = {}

    @property
    def nombre_tabla(self) -> str:
        return "t_usuarios_cache"

    @classmethod
    def desde_uri(cls, uri_conexion: str) -> "RepositorioMemoria":
        return cls(uri_conexion=uri_conexion)

    def guardar(self, id_registro: str, datos: dict[str, Any]) -> bool:
        self._almacen[id_registro] = datos.copy()
        return True

    def obtener(self, id_registro: str) -> dict[str, Any] | None:
        return self._almacen.get(id_registro)


# Uso del contrato y de la implementacion concreta
repo = RepositorioMemoria.desde_uri("memory://cluster-local/cache")
repo.guardar("USR-101", {"nombre": "Ana Morales", "rol": "Auditor"})

print(f"Tabla vinculada: {repo.nombre_tabla}")
print(f"Registro USR-101: {repo.obtener('USR-101')}")
```

Resultado esperado:

```text
Tabla vinculada: t_usuarios_cache
Registro USR-101: {'nombre': 'Ana Morales', 'rol': 'Auditor'}
```

### Avanzado

Arquitectura hexagonal (Puertos y Adaptadores) que demuestra el registro de subclases virtuales mediante `__subclasshook__` en una ABC y su interoperabilidad con protocolos de tipado estructural (`typing.Protocol`, PEP 544). Permite desacoplar adaptadores secundarios sin forzarlos a importar o heredar físicamente de la interfaz del núcleo.

```python
from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


class EmisorAuditoria(ABC):
    """Puerto de salida de auditoria con soporte dinamico de subclasshook."""
    @abstractmethod
    def emitir(self, evento: str, detalle: dict[str, Any]) -> bool:
        pass

    @classmethod
    def __subclasshook__(cls, subclase: type) -> bool:
        """Reconoce como subclase virtual a cualquier tipo con metodo emitir callable."""
        if cls is EmisorAuditoria:
            tiene_metodo = any("emitir" in b.__dict__ for b in subclase.__mro__)
            if tiene_metodo:
                return True
        return NotImplemented


@runtime_checkable
class ProtocoloExportador(Protocol):
    """Protocolo estructural equivalente conforme a PEP 544."""
    def emitir(self, evento: str, detalle: dict[str, Any]) -> bool:
        ...


class AdaptadorSplunkExterno:
    """Clase independiente de terceros: NO hereda de EmisorAuditoria ni de Protocol."""
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def emitir(self, evento: str, detalle: dict[str, Any]) -> bool:
        print(f"[SPLUNK @ {self.endpoint}] Evento={evento} Carga={detalle}")
        return True


# Verificacion de pertenencia estructural y virtual
adaptador = AdaptadorSplunkExterno("https://siem.empresa.corp:8088")

es_subclase_abc = issubclass(AdaptadorSplunkExterno, EmisorAuditoria)
es_instancia_abc = isinstance(adaptador, EmisorAuditoria)
cumple_protocolo = isinstance(adaptador, ProtocoloExportador)

print(f"Es subclase virtual de EmisorAuditoria (ABC): {es_subclase_abc}")
print(f"Es instancia de EmisorAuditoria (ABC): {es_instancia_abc}")
print(f"Cumple con ProtocoloExportador (PEP 544): {cumple_protocolo}")

# Invocacion del puerto
adaptador.emitir("LOGIN_FALLIDO", {"usuario": "admin", "ip": "192.168.1.50"})
```

Resultado esperado:

```text
Es subclase virtual de EmisorAuditoria (ABC): True
Es instancia de EmisorAuditoria (ABC): True
Cumple con ProtocoloExportador (PEP 544): True
[SPLUNK @ https://siem.empresa.corp:8088] Evento=LOGIN_FALLIDO Carga={'usuario': 'admin', 'ip': '192.168.1.50'}
```

## 6. Aplicaciones en el mundo real

El uso riguroso de Clases Base Abstractas y Protocolos sustenta pilares tecnológicos fundamentales en Python:

1. **Colecciones y Modelo de Datos de la Biblioteca Estándar (`collections.abc`):** la biblioteca estándar de Python define toda su taxonomía de contenedores mediante ABCs (`Iterable`, `Iterator`, `Sequence`, `Mapping`, `MutableMapping`). Cuando una función valida `isinstance(datos, collections.abc.Mapping)`, acepta transparentemente diccionarios nativos, objetos de configuración de frameworks o estructuras personalizadas inmutables.
2. **Frameworks de Inteligencia Artificial y Machine Learning:** bibliotecas como PyTorch (`torch.utils.data.Dataset`) o LangChain utilizan clases abstractas para forzar que los desarrolladores definan métodos específicos de indexación (`__getitem__` y `__len__`) o invocación de modelos (`_call`), garantizando canalizaciones seguras antes del entrenamiento.
3. **Controladores de Base de Datos y Mapeo Objeto-Relacional:** herramientas como SQLAlchemy o Django DB Engines declaran capas abstractas para dialectos de bases de datos. Los adaptadores para PostgreSQL, SQLite u Oracle implementan obligatoriamente los mismos métodos abstractos de compilación de sentencias SQL y manejo de conexiones.

## 7. Uso en producción

Para mantener la robustez arquitectónica en entornos corporativos, deben aplicarse las siguientes directrices:

1. **Diseñar contratos cohesivos y pequeños:** evitar interfaces abultadas que obliguen a las subclases a incorporar métodos innecesarios (principio de segregación de interfaces).
2. **Combinar ABCs con anotaciones estrictas de tipado (`typing`):** las firmas de los métodos abstractos deben especificar anotaciones de tipos completas tanto para parámetros como para el valor de retorno, permitiendo que `mypy` verifique el cumplimiento del contrato durante la integración continua.
3. **No utilizar `raise NotImplementedError` dentro de métodos decorados con `@abstractmethod`:** el decorador previene por sí mismo la invocación en instancias incompletas; colocar `pass` o una cadena de documentación descriptiva (*docstring*) resulta suficiente y idiomático.
4. **Respetar el orden estricto de apilamiento de decoradores:** situar siempre `@abstractmethod` en el nivel más interior frente a `@property`, `@classmethod` o `@staticmethod`. Invertir el orden deshace la envoltura y oculta la marca de abstracción ante `ABCMeta`.

## 8. Errores comunes y recomendaciones

### Caso 1: Intentar instanciar una subclase sin implementar todos los métodos abstractos

El error más frecuente al extender una clase abstracta ocurre cuando una subclase olvida sobrescribir uno de los métodos marcados con `@abstractmethod`.

```python
# ERROR INTENCIONAL: Demuestra la proteccion en tiempo de instanciacion provista por ABC
from abc import ABC, abstractmethod


class ValidadorDatos(ABC):
    @abstractmethod
    def validar(self, valor: str) -> bool:
        pass

    @abstractmethod
    def formatear(self, valor: str) -> str:
        pass


class ValidadorIncompleto(ValidadorDatos):
    def validar(self, valor: str) -> bool:
        return len(valor) > 0
    # Omite deliberadamente la implementacion de 'formatear'


# Intentar instanciar lanza TypeError inmediato
objeto = ValidadorIncompleto()
```

Al ejecutar la instanciación, Python aborta la operación:

```text
TypeError: Can't instantiate abstract class ValidadorIncompleto without an implementation for abstract method 'formatear'
```

**Recomendación:** implementar todos los métodos abstractos requeridos o declarar explícitamente a la subclase también como abstracta si se trata de un paso intermedio en la jerarquía.

### Caso 2: Orden erróneo de apilamiento o importación incorrecta de decoradores

Un error conceptual crítico consiste en invertir el orden de los decoradores, o intentar importar decoradores integrados como `classmethod` desde el módulo `abc` (error presente en el docstring de `Abastraccion.py` L124).

```python
# ERROR INTENCIONAL: Muestra la falla de importacion y apilamiento invertido
# Intentar importar classmethod desde abc produce ImportError:
# from abc import ABC, classmethod, abstractmethod  <-- Falla inmediata

from abc import ABC, abstractmethod


class ConfiguracionServicio(ABC):
    # ERROR DE APILAMIENTO: @abstractmethod fuera de @property
    @abstractmethod
    @property
    def url_base(self) -> str:
        pass
```

**Recomendación:** recordar que `classmethod` y `staticmethod` son funciones globales integradas. El apilamiento correcto ubica siempre a `@abstractmethod` en la posición interna:

```text
@property
@abstractmethod
def url_base(self) -> str:
    """Implementacion correcta: @property exterior, @abstractmethod interior."""
    pass
```

### Caso 3: Utilizar `raise NotImplementedError` en lugar de `abc.ABC`

En bases de código heredadas, se utiliza a menudo `raise NotImplementedError` sin `abc.ABC`. La deficiencia de este enfoque radica en que el error permanece latente hasta que el método específico es invocado en producción, habiendo permitido que el objeto circule previamente por el sistema con un estado inconsistente.

```python
# ERROR INTENCIONAL: Demuestra el fallo tardio de la abstraccion informal
class CanalNotificacionInformal:
    def enviar(self, destinatario: str, mensaje: str) -> None:
        raise NotImplementedError("Las subclases deben implementar enviar()")


class CanalSlack(CanalNotificacionInformal):
    # Olvida implementar enviar()
    pass


# La instanciacion ocurre con exito de forma silenciosa
canal = CanalSlack()

# El fallo ocurre tardiamente durante el procesamiento de un evento critico
canal.enviar("U12345", "Alerta de sistema")
```

El programa aborta con:

```text
NotImplementedError: Las subclases deben implementar enviar()
```

**Recomendación:** migrar siempre a `abc.ABC` y `@abstractmethod` para garantizar que la detección de contratos rotos ocurra en el instante mismo de la instanciación.

## 9. Resumen

1. La **abstracción** define límites de comportamiento claros aislando la especificación pública respecto de los detalles internos de implementación.
2. A diferencia de las clases base informales con `raise NotImplementedError`, el módulo **`abc`** previene la creación de instancias con métodos abstractos no implementados en tiempo de instanciación con `TypeError`.
3. La metaclase **`ABCMeta`** registra y valida el conjunto de métodos requeridos verificando el atributo `__isabstractmethod__`.
4. El decorador **`@abstractmethod`** se compone con `@property`, `@classmethod` y `@staticmethod` ubicándose siempre como el decorador más interno.
5. `classmethod` y `staticmethod` son **funciones integradas del lenguaje**, no miembros del paquete `abc`.
6. Las **subclases virtuales** (`register` y `__subclasshook__`) permiten integrar clases foráneas al ecosistema polimórfico de una ABC sin herencia física.
7. Los **Protocolos (`typing.Protocol`, PEP 544)** ofrecen subtipeado estructural estático (*duck typing* comprobable), complementando el subtipeado nominal de las ABCs.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO` | `CLASE_THREE/Clase_Tercera/Abastraccion.py` | `Abastraccion.py` | Encapsulamiento con `Auto` (L9-41), conceptos de plantilla abstracta con `Persona(ABC)` (L138-154), y decorador `@abstractmethod`. | Corrección del error de importación del docstring (L124) que intentaba importar `classmethod` desde `abc`; formalización del ciclo de vida en `ABCMeta` y apilamiento canónico con descriptores. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/OCP.py` | `OCP.py` | Clase base `Notificador` empleando `raise NotImplementedError` (L31-41) como técnica de abstracción informal. | Análisis comparativo entre abstracción informal (detección en ejecución al invocar método) y formalización estricta con `abc.ABC` (detección temprana al instanciar). |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/ISP.py` | `ISP.py` | Segregación de interfaces mediante múltiples clases abstractas independientes (`Trabajador`, `Comedor`, `Durmiente`). | Vinculación del diseño de interfaces mínimas con el desacoplamiento mediante `abc.ABC` y contraste con protocolos de tipado estructural (`typing.Protocol`). |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/DIP.py` | `DIP.py` | Inversión de dependencias basada en la interfaz `VerificadorOrtografico(ABC)` inyectada en `CorrectorOrtografico`. | Aplicación de clases base abstractas en el patrón de puertos y adaptadores (Arquitectura Hexagonal) y registro de subclases virtuales mediante `__subclasshook__`. |

**Fundamento complementario:** los ejemplos originales introducen el concepto de clases abstractas mediante jerarquías lineales de personas y notificadores. El presente documento formaliza el comportamiento interno de `ABCMeta`, la protección de constructores mediante el Modelo de Datos de CPython, la integración con descriptores idiomáticos y la coexistencia con `typing.Protocol` según PEP 544.

## 11. Referencias oficiales

- Biblioteca Estándar de Python: Módulo `abc` (Abstract Base Classes):
  https://docs.python.org/3/library/abc.html
- Biblioteca Estándar de Python: Módulo `typing` y soporte de protocolos:
  https://docs.python.org/3/library/typing.html
- PEP 3119: Introducing Abstract Base Classes:
  https://peps.python.org/pep-3119/
- PEP 544: Protocols: Structural subtyping (static duck typing):
  https://peps.python.org/pep-0544/
