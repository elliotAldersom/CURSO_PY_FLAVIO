# Herencia Múltiple, Algoritmo C3 de Linealización y Mecánica de super() en Python

## 2. Introducción

En el paradigma de programación orientada a objetos, la [herencia](../../Intermedio/chapter-five/herencia.md) permite a una clase derivar atributos y comportamientos a partir de clases preexistentes. Mientras que diversos lenguajes de tipado estático restringen la derivación a herencia simple —permitiendo únicamente la implementación de múltiples interfaces—, Python soporta de forma nativa la **herencia múltiple**, posibilitando que una clase hija herede simultáneamente de dos o más clases base (`Herencia_Multiple.py` L27).

Si bien esta capacidad aporta una flexibilidad arquitectónica sustancial para componer comportamientos ortogonales mediante el patrón *Mixin*, introduce desafíos teóricos y prácticos de gran complejidad:

1. **La ambigüedad del problema del diamante (*Diamond Problem*):** ocurre cuando dos clases intermedias heredan de una misma superclase y una subclase final hereda de ambas (`MRO.py` L105-131). Determinar qué método se ejecuta y en qué orden requiere un algoritmo matemático determinista.
2. **El Algoritmo de Linealización C3 (*C3 Superclass Linearization*):** introducido en Python 2.3 para unificar los tipos de estilo nuevo (*new-style classes*), garantiza dos propiedades axiomáticas: la preservación del orden de precedencia local y la monotonicidad. Si una jerarquía de herencia viola estas propiedades, Python aborta la definición de la clase en tiempo de compilación con una excepción `TypeError`.
3. **La semántica dinámica de `super()`:** en Python 3, la función integrada `super()` no referencia estáticamente a la clase madre léxica ni al ancestro inmediato declarado en el código fuente. Representa un objeto proxy dinámico que busca el siguiente método en el orden de resolución de métodos (*Method Resolution Order* o MRO) del objeto recibido en tiempo de ejecución (`type(self)`).
4. **El contrato de herencia cooperativa:** para que cadenas polimórficas de llamadas a través de `super()` funcionen de manera predecible, los constructores y métodos deben coordinar sus firmas mediante argumentos por palabra clave (`**kwargs`) y finalizar en una clase base terminal cooperativa, evitando colisiones posicionales como las observadas en implementaciones empíricas (`Herencia.py` L86-93).

## 3. Fundamentos y conceptos

### Herencia múltiple y el problema del diamante

La herencia múltiple permite declarar una clase receptora que enumera múltiples clases base en su signatura: `class Subclase(Base1, Base2):` (`Herencia_Multiple.py` L27-30). Cuando la clase `Base1` y la clase `Base2` heredan a su vez de un ancestro común —como mínimo la clase base universal `object` en Python 3, o una superclase de dominio como `Persona` en `Herencia.py` (L14-60) o `Animal` en `EJERCICIO_DOS_TWO.py` (L18-31)—, la estructura del grafo de herencia adquiere una topología en forma de rombo conocida como **el problema del diamante**:

```text
       ┌───────────┐
       │   Base    │
       └─────┬─────┘
         ▲       ▲
         │       │
    ┌────┴───┐ ┌─┴──────┐
    │ Sub_A  │ │ Sub_B  │
    └────┬───┘ └─┬──────┘
         ▲       ▲
         │       │
       ┌─┴───────┴─┐
       │ Derivada  │
       └───────────┘
```

Si tanto `Sub_A` como `Sub_B` sobrescriben un método declarado en `Base`, e invocamos dicho método desde una instancia de `Derivada`: ¿cuál de las dos implementaciones debe ejecutarse? En versiones tempranas de Python (clases de estilo clásico en Python 1.5 a 2.1), el intérprete utilizaba un recorrido en profundidad de izquierda a derecha (*depth-first, left-to-right*). Dicho esquema presentaba anomalías graves: si `Sub_A` no sobrescribía el método pero `Base` sí, el recorrido encontraba `Base` antes que `Sub_B`, violando la especialización de `Sub_B` que pretendía refinar a `Base`.

### Algoritmo de Linealización C3 y monotonicidad

Para resolver de manera rigurosa las limitaciones del recorrido clásico, Python 2.3 adoptó el **Algoritmo de Linealización C3**, desarrollado originalmente por Barrett et al. para el lenguaje Dylan. El objetivo de C3 es transformar el grafo acíclico dirigido (DAG) de herencia en una lista totalmente ordenada y determinista de clases: el **MRO** (*Method Resolution Order*).

El algoritmo opera satisfaciendo tres restricciones indispensables:

1. **Precedencia de la subclase sobre la superclase:** los hijos siempre se consultan antes que sus respectivos padres.
2. **Preservación del orden de precedencia local:** si una clase se define como `class C(A, B):`, la clase `A` siempre debe preceder a la clase `B` en el MRO de `C`.
3. **Monotonicidad (*Monotonicity*):** si la clase `A` precede a la clase `B` en el MRO de cualquier clase base, `A` debe preceder a `B` en el MRO de todas las subclases derivadas de dicha base. Esto garantiza que la derivación no altere el orden relativo de resolución ya consolidado en los ancestros.

Matemáticamente, la linealización de una clase $C$ con padres inmediatos $B_1, B_2, \dots, B_n$ se expresa formalmente como:

$$L(C) = [C] + \operatorname{merge}\left(L(B_1), L(B_2), \dots, L(B_n), [B_1, B_2, \dots, B_n]\right)$$

Donde la operación $\operatorname{merge}$ extrae secuencialmente la cabeza (*head*) de la primera lista candidata que no aparezca en la cola (*tail*, todos los elementos salvo el primero) de ninguna de las listas restantes. Si una cabeza cumple esta condición, se agrega al MRO acumulado y se remueve de todas las listas del $\operatorname{merge}$; el proceso se repite hasta vaciar todas las listas.

Si en algún punto todas las cabezas de las listas candidatas aparecen en las colas de otras listas, se produce una contradicción cíclica insoluble: el algoritmo se detiene y Python rechaza la creación de la clase en tiempo de compilación lanzando:

```text
TypeError: Cannot create a consistent method resolution order (MRO)
```

### Introspección del MRO: `__mro__` y `.mro()`

Python expone el orden lineal calculado a través de dos mecanismos de introspección:

- **`Clase.__mro__`:** una tupla inmutable de tipos que enumera la secuencia exhaustiva de búsqueda, finalizando invariablemente en la clase base universal `object`.
- **`Clase.mro()`:** un método de clase que retorna una nueva lista con los mismos elementos (`MRO.py` L225, `EJERCICIO_DOS.py` L40, `EJERCICIO_DOS_TWO.py` L39).

Cuando se accede a un atributo o método `instancia.metodo()`, el intérprete consulta internamente las clases presentes en `type(instancia).__mro__` en estricto orden de izquierda a derecha, ejecutando la primera implementación encontrada.

### La mecánica interna de `super()`

Un error recurrente en el aprendizaje de la orientación a objetos radica en asumir que `super()` apunta mecánicamente al "padre léxico" (la clase superior en el texto del archivo fuente). En Python, **`super()` no es un enlace estático al padre, sino un despachador dinámico sobre el MRO**.

En Python 3, la invocación sin argumentos `super()` dentro de un método equivale formalmente a `super(__class__, self)`:

- `__class__`: la clase donde el método actual está sintácticamente definido (inyectada por el compilador como una celda de cierre).
- `self`: la instancia sobre la cual se originó la llamada en tiempo de ejecución.

Cuando se evalúa `super().metodo()`, el objeto proxy realiza el siguiente procedimiento:

1. Obtiene la lista completa de linealización a partir del tipo real de la instancia: `mro = type(self).__mro__`.
2. Localiza la posición de la clase actual (`__class__`) dentro de dicho `mro`.
3. Inicia la búsqueda del método solicitado a partir del **siguiente índice** en el MRO: `mro[indice + 1:]`.
4. Enlaza el primer método coincidente con la instancia `self` y lo ejecuta.

En consecuencia, el método invocado por `super()` dentro de una clase `A` puede pertenecer a una clase hermana `B` con la que `A` no guarda ninguna relación directa de parentesco en el código fuente, siempre que `B` suceda a `A` en el MRO de la subclase concreta instanciada.

### Contrato de herencia múltiple cooperativa

Debido a que `super()` encadena llamadas a lo largo del MRO dinámico, las jerarquías de herencia múltiple exigen cooperación explícita entre todas las clases participantes:

1. **Reenvío uniforme de argumentos (`*args, **kwargs`):** si una clase espera parámetros que otra no requiere, los constructores o métodos deben capturar y reenviar los argumentos adicionales mediante `super().__init__(**kwargs)` hacia el siguiente eslabón del MRO.
2. **Clase terminal cooperativa:** la clase base universal `object.__init__` rechaza argumentos arbitrarios (salvo cuando ningún ancestro intermedio sobrescribe `__init__`). Por ello, la clase base que encabeza la jerarquía debe consumir los argumentos restantes o definir un método base sin propagación cuando ya no queden parámetros.
3. **Peligro de las llamadas directas desvinculadas:** invocar constructores explícitos por nombre (`Padre.__init__(self, ...)`) como se realiza en `Herencia.py` (L88-89), `Herencia_Multiple.py` (L34-35) o `MRO.py` (L45-46) elude el mecanismo de `super()`. Si una de las clases internas a su vez invoca `super()`, se producirá una bifurcación descontrolada con llamadas duplicadas o fallos posicionales por incompatibilidad de argumentos.

### Patrón *Mixin* frente a composición

Un **Mixin** es una clase especializada diseñada para suministrar un conjunto cohesivo de métodos adicionales a otras clases, sin pretender actuar como una entidad autónoma ni definir un ciclo de vida independiente:

- **Características de un Mixin:** no posee estado interno mutable en su propio constructor (generalmente carece de `__init__` o únicamente invoca `super().__init__(**kwargs)`), no se instancia de forma aislada, y se ubica al principio de la tupla de bases de la subclase para interceptar métodos antes que la clase base principal.
- **Herencia múltiple vs. Composición (*Composition over Inheritance*):** la herencia múltiple modela relaciones de identidad cruzada ("es un tipo de"). Cuando el objetivo es reutilizar comportamiento o delegar responsabilidades sin acoplar fuertemente la jerarquía de tipos, la **composición** (incorporar una referencia a otro objeto como atributo, delegando la ejecución) constituye la alternativa arquitectónicamente preferible y más desacoplada.

## 4. Sintaxis y funcionamiento

### Sintaxis de definición y resolución de herencia

```text
# Declaración de herencia múltiple
class Subclase(Base1, Base2, BaseN):
    def metodo(self, *args, **kwargs):
        # Despacho cooperativo hacia el siguiente elemento del MRO
        return super().metodo(*args, **kwargs)
```

Tabla descriptiva de componentes sintácticos del MRO y despacho cooperativo:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `class C(A, B):` | Declaración de herencia múltiple con orden de precedencia local $A \succ B$. | `class Murcielago(Mamifero, Ave):` |
| 2 | `super()` | Proxy dinámico en Python 3 que enlaza con el siguiente tipo en `type(self).__mro__`. | `super().describir(**kwargs)` |
| 3 | `super(Clase, instancia)` | Forma explícita tradicional de `super()` para delegar a partir de una clase específica. | `super(Mamifero, self).alimentar()` |
| 4 | `Clase.__mro__` | Tupla inmutable que almacena la secuencia lineal calculada por el algoritmo C3. | `D.__mro__` |
| 5 | `Clase.mro()` | Método que retorna una copia en formato de lista de la secuencia del MRO. | `Murcielago.mro()` |
| 6 | `**kwargs` en `super()` | Patrón idiomático de absorción y reenvío de parámetros en jerarquías cooperativas. | `super().__init__(**kwargs)` |
| 7 | `issubclass(Sub, Base)` | Función integrada que verifica si una clase deriva directa o indirectamente de otra. | `issubclass(Murcielago, Animal)` |
| 8 | `isinstance(obj, Tipo)` | Función integrada que valida si un objeto implementa el tipo en cualquier punto de su MRO. | `isinstance(m, Ave)` |

## 5. Ejemplos prácticos progresivos

### Básico

El siguiente ejemplo ilustra una jerarquía de herencia múltiple directa, contrastando cómo el orden de declaración en la signatura de la subclase determina la precedencia en el MRO y el despacho de métodos idénticos.

```python
class DispositivoElectronico:
    def encender(self) -> str:
        return "Dispositivo: energizando componentes primarios."


class ConectividadRed:
    def encender(self) -> str:
        return "ConectividadRed: iniciando interfaz de red y sincronizando IP."


class CamaraSeguridad(DispositivoElectronico, ConectividadRed):
    """Hereda primero de DispositivoElectronico y luego de ConectividadRed."""
    pass


class SensorIoT(ConectividadRed, DispositivoElectronico):
    """Orden inverso: prioriza ConectividadRed sobre DispositivoElectronico."""
    pass


# Instanciación y verificación de MRO
camara = CamaraSeguridad()
sensor = SensorIoT()

print("MRO Cámara:", [cls.__name__ for cls in CamaraSeguridad.mro()])
print("Acción Cámara:", camara.encender())

print("MRO Sensor:", [cls.__name__ for cls in SensorIoT.mro()])
print("Acción Sensor:", sensor.encender())
```

Resultado esperado:

```text
MRO Cámara: ['CamaraSeguridad', 'DispositivoElectronico', 'ConectividadRed', 'object']
Acción Cámara: Dispositivo: energizando componentes primarios.
MRO Sensor: ['SensorIoT', 'ConectividadRed', 'DispositivoElectronico', 'object']
Acción Sensor: ConectividadRed: iniciando interfaz de red y sincronizando IP.
```

### Intermedio

En este nivel se implementa el patrón del diamante resolviendo la inicialización mediante herencia cooperativa estricta. Se emplean constructores parametrizados con `**kwargs` para permitir que cada clase extraiga sus argumentos propios y propague el resto hacia el siguiente eslabón del MRO, garantizando una única ejecución armónica sin saltos ni omisiones.

```python
class EntidadJuego:
    """Clase base terminal que detiene la propagación cooperativa hacia object."""
    def __init__(self, identificador: str, **kwargs) -> None:
        self.identificador = identificador
        # super().__init__() sin kwargs evita que object.__init__ falle
        super().__init__()
        self.historial: list[str] = [f"Entidad [{self.identificador}] inicializada"]

    def ejecutar_turno(self) -> list[str]:
        return [f"Turno base procesado para {self.identificador}"]


class Guerrero(EntidadJuego):
    def __init__(self, fuerza: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.fuerza = fuerza
        self.historial.append(f"Guerrero: fuerza asignada a {self.fuerza}")

    def ejecutar_turno(self) -> list[str]:
        eventos = super().ejecutar_turno()
        eventos.append(f"Guerrero ataca infligiendo {self.fuerza} puntos de dano")
        return eventos


class Mago(EntidadJuego):
    def __init__(self, mana: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mana = mana
        self.historial.append(f"Mago: reserva de mana configurada en {self.mana}")

    def ejecutar_turno(self) -> list[str]:
        eventos = super().ejecutar_turno()
        eventos.append(f"Mago conjura barrera magica consumiendo 10/{self.mana} mana")
        return eventos


class Paladin(Guerrero, Mago):
    """Cierra el diamante: Paladin -> Guerrero -> Mago -> EntidadJuego -> object."""
    def __init__(self, fe: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.fe = fe
        self.historial.append(f"Paladin: fe consagrada en {self.fe}")

    def ejecutar_turno(self) -> list[str]:
        eventos = super().ejecutar_turno()
        eventos.append(f"Paladin bendice la batalla con fervor de fe {self.fe}")
        return eventos


# Creación del objeto cooperativo con argumentos nombrados
heroe = Paladin(
    identificador="PAL-001",
    fuerza=85,
    mana=120,
    fe=50,
)

print("Secuencia de MRO:")
for idx, clase in enumerate(Paladin.mro(), start=1):
    print(f"  {idx}. {clase.__name__}")

print("\nTraza de inicialización cooperativa:")
for entrada in heroe.historial:
    print(f"  - {entrada}")

print("\nDespacho de ejecutar_turno():")
for evento in heroe.ejecutar_turno():
    print(f"  > {evento}")
```

Resultado esperado:

```text
Secuencia de MRO:
  1. Paladin
  2. Guerrero
  3. Mago
  4. EntidadJuego
  5. object

Traza de inicialización cooperativa:
  - Entidad [PAL-001] inicializada
  - Mago: reserva de mana configurada en 120
  - Guerrero: fuerza asignada a 85
  - Paladin: fe consagrada en 50

Despacho de ejecutar_turno():
  > Turno base procesado para PAL-001
  > Mago conjura barrera magica consumiendo 10/120 mana
  > Guerrero ataca infligiendo 85 puntos de dano
  > Paladin bendice la batalla con fervor de fe 50
```

### Avanzado

El escenario avanzado implementa una arquitectura modular de producción basada en **Mixins ortogonales**. Se combinan clases auxiliares desprovistas de estado propio (`AuditableMixin` para trazabilidad de modificaciones y `SerializacionJSONMixin` para exportación normalizada) con una clase de dominio base (`RegistroTransaccional`). Este patrón ejemplifica cómo desacoplar responsabilidades transversales sin comprometer la jerarquía del modelo.

```python
import json
import time
from typing import Any


class AuditableMixin:
    """Mixin ortogonal para registrar marcas temporales y eventos de auditoria."""
    def registrar_evento(self, accion: str) -> None:
        if not hasattr(self, "_auditoria"):
            self._auditoria: list[dict[str, Any]] = []
        registro = {
            "timestamp": time.time(),
            "accion": accion,
            "origen": self.__class__.__name__,
        }
        self._auditoria.append(registro)

    def obtener_auditoria(self) -> list[dict[str, Any]]:
        return getattr(self, "_auditoria", [])


class SerializacionJSONMixin:
    """Mixin ortogonal que serializa propiedades publicas a JSON canonico."""
    def a_json(self) -> str:
        datos_exportables = {}
        for clave, valor in self.__dict__.items():
            if not clave.startswith("_"):
                datos_exportables[clave] = valor
        return json.dumps(datos_exportables, sort_keys=True, ensure_ascii=False)


class EntidadBase:
    """Base de dominio pura con identidad."""
    def __init__(self, codigo: str) -> None:
        self.codigo = codigo


class OperacionBancaria(AuditableMixin, SerializacionJSONMixin, EntidadBase):
    """Integra mixins funcionales antes de la clase base sustantiva."""
    def __init__(self, codigo: str, titular: str, importe_centavos: int) -> None:
        super().__init__(codigo=codigo)
        self.titular = titular
        self.importe_centavos = importe_centavos
        self.estado = "CREADA"
        self.registrar_evento("CREACION_INICIAL")

    def autorizar(self) -> None:
        self.estado = "AUTORIZADA"
        self.registrar_evento("AUTORIZACION_FONDOS")

    def liquidar(self) -> None:
        self.estado = "LIQUIDADA"
        self.registrar_evento("LIQUIDACION_COMPLETADA")


operacion = OperacionBancaria(
    codigo="TRX-99812",
    titular="Elena Rostova",
    importe_centavos=154000,
)

operacion.autorizar()
operacion.liquidar()

print("MRO de OperacionBancaria:")
print([c.__name__ for c in OperacionBancaria.mro()])

print("\nPayload exportado (SerializacionJSONMixin):")
print(operacion.a_json())

print("\nEventos auditados (AuditableMixin):")
for evento in operacion.obtener_auditoria():
    print(f"  [{evento['origen']}] -> {evento['accion']}")
```

Resultado esperado:

```text
MRO de OperacionBancaria:
['OperacionBancaria', 'AuditableMixin', 'SerializacionJSONMixin', 'EntidadBase', 'object']

Payload exportado (SerializacionJSONMixin):
{"codigo": "TRX-99812", "estado": "LIQUIDADA", "importe_centavos": 154000, "titular": "Elena Rostova"}

Eventos auditados (AuditableMixin):
  [OperacionBancaria] -> CREACION_INICIAL
  [OperacionBancaria] -> AUTORIZACION_FONDOS
  [OperacionBancaria] -> LIQUIDACION_COMPLETADA
```

## 6. Aplicaciones en el mundo real

La herencia múltiple y la resolución MRO estructuran componentes críticos en el ecosistema Python:

1. **Vistas Basadas en Clases en Django (*Class-Based Views*):** el framework web Django implementa su arquitectura de vistas mediante mixins modulares. Clases como `TemplateView` o `UpdateView` combinan `ContextMixin`, `TemplateResponseMixin` y `ModelFormMixin`. El orden de herencia en la declaración garantiza que la autenticación (`LoginRequiredMixin`) preceda a la lógica de procesamiento HTTP, interceptando la solicitud antes de invocar la consulta a base de datos.
2. **Serializadores y Controladores en Django REST Framework:** clases como `ModelViewSet` heredan simultáneamente de mixins discretos (`CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`, `ListModelMixin`) y de `GenericAPIView`. Esto permite a los desarrolladores habilitar o inhabilitar verbos REST con granularidad fina simplemente alterando la tupla de clases base.
3. **Mapeo Objeto-Relacional en SQLAlchemy:** el sistema declarativo de SQLAlchemy utiliza mixins de persistencia (`TimestampMixin`, `AuditColumnsMixin`) para inyectar automáticamente columnas comunes de auditoría (`created_at`, `updated_at`, `created_by_id`) en múltiples entidades de base de datos sin duplicar definiciones de esquemas.

## 7. Uso en producción

Al implementar jerarquías con herencia múltiple en entornos empresariales, deben observarse los siguientes principios de ingeniería:

1. **Favorecer la composición sobre la herencia compleja:** la herencia múltiple debe restringirse al ensamblado de Mixins sin estado o contratos estrictos de comportamiento. Cuando se requiere reutilizar lógica con estado mutable persistente, la composición mediante inyección de dependencias genera arquitecturas significativamente más testeables y desacopladas.
2. **Mantener los Mixins estrictamente ortogonales:** cada Mixin debe aportar una única responsabilidad aislada (auditoría, serialización, seguridad). No deben asumir la presencia de métodos arbitrarios en clases hermanas a menos que se declaren como requisitos formales mediante protocolos tipados.
3. **Firmas de inicialización universales con `**kwargs`:** si las clases participan en jerarquías diamantinas, ningún constructor intermedio debe exigir únicamente parámetros posicionales fijos si planea invocar `super().__init__()`. Los argumentos deben consumirse selectivamente y propagarse mediante `kwargs`.
4. **Verificación automatizada de consistencia de MRO en pruebas unitarias:** para evitar que refactorizaciones en bibliotecas dependientes alteren inadvertidamente el orden de resolución, las suites de pruebas continuas deben incluir aserciones explícitas sobre `Clase.__mro__`.

## 8. Errores comunes y recomendaciones

### Caso 1: Suponer que `super()` referencia al padre sintáctico directo

Un error habitual consiste en asumir que invocar `super()` dentro de una clase hija llamará necesariamente al padre declarado en su definición. En el contexto de herencia múltiple diamantina, `super()` invoca al siguiente elemento en el MRO de la instancia final concreta, el cual puede ser una clase hermana y no su progenitor inmediato.

### Caso 2: Intento de linealización C3 inconsistente (violación de monotonicidad)

Si dos clases intermedias discrepan sobre el orden relativo de sus ancestros y una tercera clase hereda de ambas simultáneamente, el algoritmo C3 no puede generar un orden compatible con el principio de monotonicidad. Python rechaza la definición inmediatamente con `TypeError`.

```python
# ERROR INTENCIONAL: Demuestra el fallo de compilacion por contradiccion de MRO en C3
class X:
    pass


class Y:
    pass


class A(X, Y):
    pass


class B(Y, X):
    pass


# Intentar definir C violando el orden relativo de X e Y produce TypeError inmediato
class C(A, B):
    pass
```

Al intentar ejecutar la definición de la clase `C`, el compilador lanza:

```text
TypeError: Cannot create a consistent method resolution order (MRO) for bases X, Y
```

**Recomendación:** alinear el orden de las clases base en toda la jerarquía para que no existan dependencias cruzadas contradictorias ($A$ declara $X \succ Y$ mientras $B$ declara $Y \succ X$).

### Caso 3: Colisión de firmas en constructores rígidos no cooperativos

Este error reproduce exactamente la falla arquitectónica presente en el código original de `Herencia.py` (L86-93). Al crear una clase derivada de dos jerarquías que utilizan `super().__init__` con parámetros posicionales rígidos y dispares, el MRO despacha la llamada hacia una clase cuyos parámetros no coinciden.

```python
# ERROR INTENCIONAL: Muestra la ruptura de super() al omitir el diseno cooperativo con kwargs
class Persona:
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = nombre
        self.edad = edad


class Empleado(Persona):
    def __init__(self, nombre: str, edad: int, salario: float) -> None:
        super().__init__(nombre, edad)
        self.salario = salario


class Estudiante(Persona):
    def __init__(self, nombre: str, edad: int, matricula: str) -> None:
        # En Estudiante_Trabajador, el siguiente en MRO es Empleado, NO Persona.
        # Empleado.__init__ espera (nombre, edad, salario), pero super() aqui envia (nombre, edad).
        super().__init__(nombre, edad)
        self.matricula = matricula


class Estudiante_Trabajador(Estudiante, Empleado):
    pass


# Falla al instanciar porque Estudiante invoca super().__init__(nombre, edad)
# resolviendo hacia Empleado.__init__, al que le falta el argumento posicional 'salario'.
instancia = Estudiante_Trabajador("Carlos", 22, "MAT-909")
```

El intérprete aborta la ejecución indicando:

```text
TypeError: Empleado.__init__() missing 1 required positional argument: 'salario'
```

**Recomendación:** migrar los constructores a la convención cooperativa utilizando `**kwargs` o separar las responsabilidades mediante agregación y composición funcional.

## 9. Resumen

1. La **herencia múltiple** permite a una clase incorporar comportamientos y atributos de múltiples clases base simultáneamente.
2. El **problema del diamante** surge cuando dos ramas de herencia derivan de una superclase común; Python lo resuelve mediante el **Algoritmo de Linealización C3**.
3. El algoritmo C3 asegura la preservación del orden local de declaración y la **monotonicidad**, rechazando con `TypeError` cualquier jerarquía conceptualmente contradictoria.
4. `Clase.__mro__` y `Clase.mro()` exponen la secuencia exacta y determinista de búsqueda utilizada en tiempo de ejecución.
5. La instrucción `super()` no enlaza estáticamente con el padre del archivo fuente; consulta dinámicamente el siguiente nodo en el MRO del tipo de la instancia (`type(self)`).
6. La herencia múltiple sana requiere **cooperación**: métodos coordinados mediante `*args, **kwargs` y clases base terminales que consuman los parámetros antes de alcanzar `object`.
7. El patrón **Mixin** proporciona capacidades complementarias desacopladas sin estado mutable ni acoplamiento estructural.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO` | `CLASE_TWO/CLASE_SEGUNDA/Herencia.py` | `Herencia.py` | Herencia jerárquica, sobreescritura de métodos (`saludar`), uso de `super()` e intento empírico de herencia múltiple en `Estudiante_Trabajador` (L86-93). | Diagnóstico formal del fallo por ruptura de contrato en `super()`: demostración matemática de por qué la llamada ingenua en `Estudiante` resuelve hacia `Empleado` y colisiona con sus argumentos requeridos. |
| `CLASS_PY_POO` | `CLASE_TWO/CLASE_SEGUNDA/Herencia_Multiple.py` | `Herencia_Multiple.py` | Declaración de clase `Empleado_Artista(Persona, Artista)`, llamadas directas `Persona.__init__(self)` y validación con `issubclass` e `isinstance`. | Se explica la diferencia entre invocar constructores explícitos por nombre frente a `super()`, contrastando la fragilidad de las llamadas manuales con el patrón cooperativo. |
| `CLASS_PY_POO` | `CLASE_TWO/CLASE_SEGUNDA/MRO.py` | `MRO.py` | Casos de búsqueda en diamante con clases `A`, `B`, `C`, `D`, invocación de `D.mro()` y llamadas directas `B.hablar(d)`. | Formalización analítica del algoritmo de linealización C3, definición de la fórmula de fusión ($\operatorname{merge}$), explicación de la monotonicidad y condiciones exactas del error de linealización. |
| `CLASS_PY_POO` | `CLASE_TWO/EJERCICIOS/EJERCICIO_DOS.py` | `EJERCICIO_DOS.py` | Especialización de `Estudiante(Persona)`, reutilización de inicializador con `super()` y visualización de `Estudiante.mro()`. | Progresión didáctica de herencia simple a jerarquías complejas, vinculando la linealización trivial con cadenas extendidas de objetos. |
| `CLASS_PY_POO` | `CLASE_TWO/EJERCICIOS/EJERCICIO_DOS_TWO.py` | `EJERCICIO_DOS_TWO.py` | Jerarquía múltiple `Murcielago(Mamifero, Ave)` sobre base común `Animal`. | Análisis del problema del diamante zoológico clásico, demostrando la propagación ordenada de capacidades ortogonales. |
| `CLASS_PY_POO` | `REPASOS/Herencia_Multiple.py` | `Herencia_Multiple.py` | Derivaciones compuestas `Artista_Alumno(Artista, Estudiante)`, orden de linealización e inspección de `__dict__`. | Sistematización del patrón *Mixin* moderno, desacoplamiento de estado y comparativa con el principio de composición sobre herencia. |

**Fundamento complementario:** los archivos originales abordan el MRO de forma intuitiva mediante jerarquías de prueba con salidas en consola. La presente guía complementa dicho material proporcionando la base matemática rigurosa del algoritmo C3, el análisis de monotonicidad, la resolución de conflictos mediante `kwargs` y el estándar de diseño de Mixins aplicado en frameworks profesionales.

## 11. Referencias oficiales

- Tutorial de Python: Herencia múltiple y resolución de clases:
  https://docs.python.org/3/tutorial/classes.html#multiple-inheritance
- Documentación de funciones integradas: mecánica de `super()`:
  https://docs.python.org/3/library/functions.html#super
- Modelo de Datos de Python: Jerarquía estándar de tipos y atributos especiales:
  https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy
- PEP 3135: Sintaxis simplificada de `super` en Python 3:
  https://peps.python.org/pep-3135/
