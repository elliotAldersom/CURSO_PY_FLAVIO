# Polimorfismo, Sobrescritura, *Duck Typing*, Particularidades de la Sobrecarga y Enlace Dinámico

## 2. Introducción

Cuando una función procesadora necesita comprobar manualmente mediante largas cascadas `if isinstance(x, TipoA): ... elif isinstance(x, TipoB): ...` qué clase de objeto recibió antes de actuar, añadir una nueva variante obliga a abrir y modificar todos los puntos de control del sistema.

El **polimorfismo** (del griego *polus*, "muchos", y *morphé*, "forma") permite invocar una **misma interfaz o mensaje** sobre objetos de distinta naturaleza para que cada ejemplar ejecute su propia implementación específica. En Python, donde el modelo de objetos es intrínsecamente dinámico, dominar el polimorfismo exige precisión conceptual en cinco frentes:

1. **Sobrescritura en jerarquías (*method overriding*):** especializar métodos heredados manteniendo contratos sustituibles.
2. ***Duck typing* y subtipado estructural (`typing.Protocol`):** operar sobre comportamientos compartidos sin exigir una superclase común.
3. **Particularidades de la sobrecarga (*overloading*) en Python:** distinguir entre la **sobrecarga de operadores** (soportada mediante métodos especiales) y la **inexistencia de sobrecarga tradicional de métodos por firma**, empleando en su lugar valores por defecto o `@functools.singledispatchmethod`.
4. **Coerción y enlace dinámico (*dynamic binding*):** comprender cómo Python resuelve el método efectivo en tiempo de ejecución.
5. **Rigor terminológico:** corregir confusiones frecuentes entre reasignación dinámica de variables y polimorfismo de inclusión, así como entre **tipo declarado** y **tipo real**.

## 3. Fundamentos y conceptos

**Interfaz unificada sobre múltiples implementaciones.** El núcleo del polimorfismo consiste en separar **qué se solicita** (el contrato: `canal.notificar()`, `verificador.verificar_palabra(p)`, `len(contenedor)`) respecto de **cómo se ejecuta** internamente en cada clase. El código cliente permanece agnóstico a la clase concreta: envía el mismo mensaje a una colección heterogénea de objetos y cada uno responde según su tipo real.

**Polimorfismo de subtipado (inclusión) mediante sobrescritura (*method overriding*).** En una jerarquía de [herencia](herencia.md) (`Animal -> Gato, Perro` o `Notificador -> NotificarEmail, NotificarSMS`), las subclases redefinen un método de la clase base conservando una firma y semántica compatibles. Cualquier rutina diseñada para operar sobre `Notificador` acepta transparentemente cualquier subclase presente o futura sin alterar su propio código fuente. Para que el polimorfismo sea seguro, toda subclase debe respetar el contrato conductual de la base (evitando, por ejemplo, heredar `volar()` para retornar sorpresivamente `None` o fallar, aspecto profundizado en [principios SOLID](../../Avanzado/chapter-two/principios_solid.md)).

***Duck typing* (polimorfismo estructural implícito) y `typing.Protocol`.** En lenguajes estáticos nominales clásicos, dos clases solo son polimórficas si heredan explícitamente de una misma interfaz o clase base. En Python rige el principio de ***duck typing*** (*"si camina como un pato y grazna como un pato, se trata como un pato"*): la validez de un objeto en un contexto depende exclusivamente de **si posee los métodos y atributos requeridos en tiempo de ejecución**, sin importar su linaje de herencia. Por ejemplo, una función que invoca `fuente.read()` funciona igual con un archivo físico abierto mediante `open()` ([manejo de archivos](../chapter-three/manejo_archivos.md)), un flujo en memoria `io.StringIO` o una respuesta HTTP. Cuando se desea verificar estáticamente este contrato estructural con `mypy` o `pyright` sin imponer herencia nominal, la biblioteca estándar ofrece `typing.Protocol` (**PEP 544**).

**Particularidades de la sobrecarga (*overloading*) en Python.** El término "polimorfismo *ad hoc*" abarca dos mecanismos que Python trata de forma diametralmente opuesta:

1. **Sobrecarga de operadores (soportada nativamente):** un mismo [operador](../../Basico/chapter-one/operadores.md) (`+`, `*`, `==`) o [función integrada](../chapter-two/funciones_integradas.md) (`len()`, `str()`) actúa polimórficamente según los operandos: `3 + 5` suma enteros, `"py" + "thon"` concatena cadenas y `[1] + [2]` fusiona listas, delegando internamente en `__add__` y `__len__` (desarrollado en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md)).
2. **Ausencia de sobrecarga tradicional de métodos por firma (*method overloading*):** en Java, C++ o C# es válido declarar en una misma clase dos métodos `procesar(int x)` y `procesar(String x, int n)` diferenciados por número o tipo de parámetros. **En Python esto no existe**: dado que el espacio de nombres de una clase es un diccionario (`Clase.__dict__`) indexado únicamente por el nombre del identificador, escribir una segunda sentencia `def procesar(...)` dentro de la misma clase **sobrescribe y destruye silenciosamente la primera definición**. Para lograr firmas flexibles en Python idiomático se emplean tres mecanismos:
   - Parámetros con valores predeterminados (`def exportar(self, destino: str, comprimir: bool = False)`) o argumentos variables (`*args`, `**kwargs`) en [funciones](../chapter-two/funciones.md).
   - Constructores alternativos con nombres explícitos mediante `@classmethod` ([atributos y métodos](atributos_y_metodos.md)).
   - Despacho genérico basado en el tipo del primer argumento mediante **`@functools.singledispatch`** (para funciones) y **`@functools.singledispatchmethod`** (para métodos) de la biblioteca estándar.

**Coerción numérica implícita y enlace dinámico (*dynamic binding*).** Un mecanismo complementario es la **coerción** numérica: al evaluar `3 + 4.4`, Python evita un error de tipos promoviendo el `int` a `float` (técnicamente, `int.__add__(3, 4.4)` retorna el centinela `NotImplemented` y el intérprete delega en `float.__radd__(4.4, 3)` obteniendo `7.4`). Asimismo, en Python **toda invocación de método utiliza enlace dinámico (*late / dynamic binding*)** en tiempo de ejecución: el intérprete consulta `type(receptor).__mro__` en el instante exacto de ejecutar la llamada para decidir qué función invocar.

**Distinción conceptual rigurosa: tipado dinámico, tipo real y tipo declarado.** Para consolidar una base arquitectónica sólida:

1. **Reasignación dinámica de variables frente a polimorfismo de inclusión:** reasignar sucesivamente una variable (`x = 5`, `x = 5.4`, `x = "Hola"`) **no es polimorfismo de inclusión**, sino **tipado dinámico con reasignación de referencias**: en Python los nombres carecen de tipo fijo y apuntan dinámicamente a objetos en memoria. En la clasificación formal de lenguajes (Cardelli y Wegner), el **polimorfismo de inclusión** (o de subtipado) ocurre cuando una rutina escrita para un supertipo abstracto opera uniformemente sobre instancias de subtipos concretos (`Animal -> Perro, Gato`).
2. **Tipo real frente a tipo declarado:** conviene distinguirlos con precisión:
   - **Tipo declarado (*static / declared type*):** es la anotación estática escrita en la variable o parámetro (`mascota: Animal = Perro()`, o `def sonar(a: Animal)`), utilizada por verificadores estáticos para delimitar qué interfaz se promete usar (escribiendo siempre con dos puntos `ave: Ave` y no con signo igual `ave = Ave`, ya que `=` asigna la clase como valor por defecto en lugar de anotar el tipo).
   - **Tipo real o dinámico (*runtime / actual type*):** es la clase concreta con la que el objeto fue verdaderamente instanciado en memoria (`type(mascota)` -> `Perro`). El enlace dinámico de Python despacha siempre los métodos según el **tipo real** (`Perro`), nunca según la anotación estática (`Animal`).

## 4. Sintaxis y funcionamiento

Comparación de mecanismos polimórficos idiomáticos en Python:

```text
# A. Polimorfismo por sobrescritura (subtipado nominal)
class Exportador:
    def serializar(self, datos: dict[str, object]) -> str:
        raise NotImplementedError

class ExportadorCSV(Exportador):
    def serializar(self, datos: dict[str, object]) -> str: ...


# B. Polimorfismo estructural (Duck Typing documentado con typing.Protocol)
from typing import Protocol

class Cerrable(Protocol):
    def cerrar(self) -> str: ...


# C. Despacho por tipo de argumento (@singledispatchmethod)
from functools import singledispatchmethod

class Formateador:
    @singledispatchmethod
    def mostrar(self, valor: object) -> str: ...
    @mostrar.register
    def _(self, valor: int) -> str: ...
```

Referencia de herramientas y patrones polimórficos en Python:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | Sobrescritura (`def m`) | Redefine en la subclase un método de la superclase | `class Perro(Animal): def sonido(self):` |
| 2 | *Duck typing* | Invoca un método esperado sin comprobar herencia nominal | `return recurso.read()` |
| 3 | `typing.Protocol` | Formaliza contratos de *duck typing* para chequeo estático (**PEP 544**) | `class Enviable(Protocol):` |
| 4 | `var: Super = Sub()` | Distingue tipo declarado (`Super`) de tipo real en memoria (`Sub`) | `a: Animal = Perro()` |
| 5 | `@singledispatch` | Sobrecarga funcional limpia según el tipo del primer argumento | `@singledispatch def procesar(x):` |
| 6 | `@singledispatchmethod` | Variante de despacho simple para métodos de instancia o clase | `@singledispatchmethod def cargar(self, x):` |
| 7 | Coerción aritmética | Promoción implícita entre tipos numéricos compatibles (`int` -> `float`) | `3 + 4.4  # -> 7.4 (float)` |
| 8 | Operadores polimórficos | Uso uniforme de `+`, `len()`, `in` respaldado por métodos dunder | `len("abc"), len([1, 2])` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Despacho polimórfico uniforme combinando herencia, *duck typing* y verificación de tipo declarado frente a tipo real.**

```python
class CanalNotificacion:
    def enviar(self, destinatario: str, mensaje: str) -> str:
        raise NotImplementedError("Cada subclase debe implementar enviar()")


class NotificadorEmail(CanalNotificacion):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[EMAIL -> {destinatario}] {mensaje}"


class NotificadorSMS(CanalNotificacion):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[SMS -> {destinatario}] {mensaje[:25]}"


class WebhookAuditoria:
    """No hereda de CanalNotificacion, pero cumple el mismo protocolo (Duck Typing)."""

    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[WEBHOOK -> {destinatario}] payload={len(mensaje)}B"


def despachar_alerta(canales: list[object], destino: str, texto: str) -> None:
    for canal in canales:
        print(canal.enviar(destino, texto))


# Anotación estática (tipo declarado: CanalNotificacion) vs instancia (tipo real: NotificadorEmail)
canal_principal: CanalNotificacion = NotificadorEmail()
print("Tipo real en ejecución:", type(canal_principal).__name__)

activos = [canal_principal, NotificadorSMS(), WebhookAuditoria()]
despachar_alerta(activos, "operaciones", "Reinicio programado")
```

Explicación paso a paso:

- La función `despachar_alerta` invoca `canal.enviar(...)` sin ningún condicional `if/elif`: `NotificadorEmail` y `NotificadorSMS` participan por polimorfismo de herencia, mientras `WebhookAuditoria` se integra transparentemente por *duck typing*.
- En `canal_principal: CanalNotificacion = NotificadorEmail()`, el tipo declarado para herramientas estáticas es `CanalNotificacion`, pero `type(canal_principal).__name__` confirma que su **tipo real** en memoria es `NotificadorEmail`.

Resultado esperado:

```text
Tipo real en ejecución: NotificadorEmail
[EMAIL -> operaciones] Reinicio programado
[SMS -> operaciones] Reinicio programado
[WEBHOOK -> operaciones] payload=19B
```

### Intermedio

**Ejemplo 2 — Subtipado estructural verificable con `typing.Protocol` e inyección polimórfica de dependencias.**

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class VerificadorLexico(Protocol):
    def contiene(self, palabra: str) -> bool:
        ...


class DiccionarioEnMemoria:
    def __init__(self, vocabulario: set[str]) -> None:
        self._vocabulario = {p.lower() for p in vocabulario}

    def contiene(self, palabra: str) -> bool:
        return palabra.lower() in self._vocabulario


class FiltroPrefijoTecnico:
    """Acepta términos que comiencen con un prefijo válido sin heredar de Diccionario."""

    def __init__(self, prefijo: str) -> None:
        self._prefijo = prefijo.lower()

    def contiene(self, palabra: str) -> bool:
        return palabra.lower().startswith(self._prefijo)


class CorrectorDocumentos:
    def __init__(self, verificador: VerificadorLexico) -> None:
        self._verificador = verificador

    def detectar_desconocidas(self, texto: str) -> list[str]:
        palabras = texto.split()
        return [p for p in palabras if not self._verificador.contiene(p)]


dic_local = DiccionarioEnMemoria({"python", "clase", "objeto", "metodo"})
regla_py = FiltroPrefijoTecnico("py")

print("¿Cumple Protocol en ejecución?:", isinstance(dic_local, VerificadorLexico))
print("Con diccionario:", CorrectorDocumentos(dic_local).detectar_desconocidas("python define clase y tupla"))
print("Con prefijo    :", CorrectorDocumentos(regla_py).detectar_desconocidas("python pytest mypy ruff"))
```

Explicación técnica:

- `VerificadorLexico(Protocol)` define un contrato estructural sin obligar a `DiccionarioEnMemoria` ni a `FiltroPrefijoTecnico` a heredar de una clase abstracta común.
- `CorrectorDocumentos` opera contra la abstracción `VerificadorLexico`, permitiendo alternar estrategias de verificación sin tocar una sola línea del algoritmo `detectar_desconocidas`.

Resultado esperado:

```text
¿Cumple Protocol en ejecución?: True
Con diccionario: ['define', 'y', 'tupla']
Con prefijo    : ['mypy', 'ruff']
```

### Avanzado

**Ejemplo 3 — Despacho polimórfico por tipo de argumento con `@functools.singledispatchmethod` frente a la ausencia de sobrecarga por firma.**

```python
from functools import singledispatchmethod


class ProcesadorPagos:
    """Procesa importes expresados como entero (centavos), flotante o diccionario."""

    @singledispatchmethod
    def normalizar_centavos(self, entrada: object) -> int:
        raise TypeError(f"Formato de pago no soportado: {type(entrada).__name__}")

    @normalizar_centavos.register
    def _(self, entrada: int) -> int:
        if isinstance(entrada, bool) or entrada < 0:
            raise ValueError("Los centavos deben ser un entero no negativo")
        return entrada

    @normalizar_centavos.register
    def _(self, entrada: float) -> int:
        if entrada < 0.0:
            raise ValueError("El monto flotante no puede ser negativo")
        return round(entrada * 100)

    @normalizar_centavos.register
    def _(self, entrada: dict) -> int:
        unidades = int(entrada["unidades"])
        centavos = int(entrada.get("centavos", 0))
        return unidades * 100 + centavos


pasarela = ProcesadorPagos()
print("Desde int  :", pasarela.normalizar_centavos(1599))
print("Desde float:", pasarela.normalizar_centavos(15.99))
print("Desde dict :", pasarela.normalizar_centavos({"unidades": 15, "centavos": 99}))

try:
    pasarela.normalizar_centavos(["15", "99"])
except TypeError as err:
    print("Rechazo tipado:", err)
```

Explicación de arquitectura:

- En lugar de construir un único método monolítico plagado de ramas `if isinstance(entrada, ...)` o caer en el error de definir `def normalizar_centavos` tres veces seguidas, `@singledispatchmethod` registra implementaciones independientes asociadas a cada tipo (`int`, `float`, `dict`) con un caso base seguro que lanza `TypeError` para entradas desconocidas.

Resultado esperado:

```text
Desde int  : 1599
Desde float: 1599
Desde dict : 1599
Rechazo tipado: Formato de pago no soportado: list
```

## 6. Aplicaciones en el mundo real

- **Pasarelas de pago y proveedores logísticos multiproveedor:** un servicio de *checkout* invoca `proveedor.cobrar(orden)` de manera idéntica tanto si la instancia inyectada corresponde a Stripe, MercadoPago, transferencia bancaria o una pasarela simulada de pruebas.
- **Protocolos de archivos y flujos de E/S (*streams*):** compresores (`gzip`), lectores CSV ([archivos CSV](../chapter-three/archivos_csv.md)) y serializadores JSON aceptan cualquier objeto *file-like* que exponga `.read()` o `.write()`, permitiendo procesar datos en RAM (`BytesIO`/`StringIO`) o sockets sin tocar el disco.
- **Serializadores extensibles por tipo (`@singledispatch`):** convertidores personalizados para JSON o motores de reportes que registran funciones de formateo específicas para `datetime`, `Decimal`, `UUID` o entidades propias sin modificar el serializador central.
- **Ecosistema científico y de aprendizaje automático (`fit` / `predict`):** bibliotecas como scikit-learn estructuran decenas de algoritmos (regresión lineal, árboles, redes) bajo la misma interfaz polimórfica `modelo.fit(X, y)` y `modelo.predict(X)`, haciendo intercambiables los estimadores dentro de un mismo *pipeline*.

## 7. Uso en producción

- **Reemplazar condicionales de tipo (`isinstance` en cascada) por polimorfismo:** cuando un mismo bloque `if isinstance(x, A): ... elif isinstance(x, B): ...` reaparece en varios módulos del proyecto, es señal inequívoca de que la operación debe trasladarse como método polimórfico a las clases `A` y `B` (o registrarse mediante `@singledispatch`).
- **Mantener firmas y tipos de retorno consistentes entre implementaciones polimórficas:** si tres canales retornan un objeto `ResultadoEnvio` pero un cuarto retorna `None` o un booleano (donde una variante retorna implícitamente `None` mientras otra retorna `str`), el código cliente terminará fallando con `AttributeError`. Todas las variantes deben honrar la misma poscondición.
- **Combinar *duck typing* con `typing.Protocol` en fronteras entre paquetes:** en bases de código medianas y grandes, documentar los métodos esperados mediante `Protocol` ofrece la flexibilidad sin herencia del *duck typing* junto con detección temprana de firmas incompatibles en integración continua.
- **Distinguir rigurosamente anotación de parámetro (`param: Tipo`) de valor por defecto (`param = Valor`):** evitar errores sutiles como `def hacer_volar(ave = Ave):`, donde omitir el argumento entregaría el objeto clase `Ave` en lugar de una instancia, usando siempre dos puntos `def hacer_volar(ave: Ave) -> str:`.

## 8. Errores comunes y recomendaciones

1. **Definir dos métodos con el mismo nombre en una clase esperando sobrecarga al estilo Java o C++.**

```python
class CalculadoraSobrescrita:
    def sumar(self, a: int, b: int) -> int:
        return a + b

    # Esta segunda definición SOBRESCRIBE y elimina la primera en CalculadoraSobrescrita.__dict__
    def sumar(self, a: int, b: int, c: int) -> int:
        return a + b + c


calc = CalculadoraSobrescrita()
try:
    print(calc.sumar(2, 3))
except TypeError as err:
    print(f"{type(err).__name__}: {err}")


class CalculadoraIdiomatica:
    def sumar(self, a: int, b: int, c: int = 0) -> int:
        return a + b + c


print("Con valor por defecto (2 args):", CalculadoraIdiomatica().sumar(2, 3))
print("Con valor por defecto (3 args):", CalculadoraIdiomatica().sumar(2, 3, 4))
```

Resultado esperado:

```text
TypeError: CalculadoraSobrescrita.sumar() missing 1 required positional argument: 'c'
Con valor por defecto (2 args): 5
Con valor por defecto (3 args): 9
```

Diagnóstico: al evaluar el cuerpo de `CalculadoraSobrescrita`, la segunda sentencia `def sumar` reasigna la clave `'sumar'` en el diccionario de la clase descartando la versión de dos argumentos. Recomendación: emplear parámetros opcionales con valor por defecto, `*args` o `@singledispatchmethod`.

2. **Romper el contrato polimórfico retornando `None` silenciosamente en métodos no soportados o pasando datos sin la interfaz esperada.**

```python
# ERROR INTENCIONAL: violación de interfaz esperada en despacho polimórfico
class NotificarEmailRoto:
    def __init__(self, usuario: object, mensaje: str) -> None:
        self.usuario = usuario
        self.mensaje = mensaje

    def notificar(self) -> str:
        return f"Enviando a {self.usuario.email}: {self.mensaje}"


alerta = NotificarEmailRoto("usuario@dominio.com", "Aviso")
alerta.notificar()  # AttributeError: 'str' object has no attribute 'email'
```

Diagnóstico: el *duck typing* difiere la comprobación de interfaz hasta el instante en que se ejecuta `.email`. Acompañar los constructores y funciones polimórficas con anotaciones de tipos (`usuario: DestinatarioConEmail`) detecta esta discrepancia estáticamente antes de ejecutar el código.

3. **Abusar de comprobaciones rígidas `type(obj) is Clase` que bloquean el polimorfismo.**

```python
class Documento:
    def exportar(self) -> str:
        return "DOC-BASE"


class FacturaElectronica(Documento):
    def exportar(self) -> str:
        return "FACTURA-XML-FIRMADA"


def emitir_rigido(doc: Documento) -> str:
    if type(doc) is Documento:  # Antipatrón: rechaza cualquier subclase válida
        return doc.exportar()
    return "RECHAZADO"


def emitir_polimorfico(doc: Documento) -> str:
    return doc.exportar()


factura = FacturaElectronica()
print("Con type() rígido      :", emitir_rigido(factura))
print("Con despacho polimórfico:", emitir_polimorfico(factura))
```

Resultado esperado:

```text
Con type() rígido      : RECHAZADO
Con despacho polimórfico: FACTURA-XML-FIRMADA
```

Diagnóstico: verificar `type(doc) is Documento` anula por completo la extensibilidad de las subclases y de los dobles de prueba. Recomendación: confiar directamente en la invocación polimórfica del método (EAFP / *duck typing*) o, cuando sea imprescindible validar linaje, emplear `isinstance(doc, Documento)`.

## 9. Resumen

- El **polimorfismo** permite que distintos objetos respondan a una misma llamada de método con comportamientos específicos según su implementación, eliminando cascadas rígidas de condicionales.
- Python soporta de forma natural el **polimorfismo de subtipado** (sobrescritura en [herencia](herencia.md)), el ***duck typing*** (polimorfismo estructural basado en comportamiento, formalizable estáticamente con `typing.Protocol`), la **sobrecarga de operadores** y la **coerción numérica**.
- Python **no posee sobrecarga tradicional de métodos por firma de parámetros**: redeclarar un método con el mismo nombre sobrescribe al anterior. En su lugar se usan argumentos por defecto, `*args`, constructores `@classmethod` o `@functools.singledispatchmethod`.
- Toda invocación de método en Python emplea **enlace dinámico** en tiempo de ejecución gobernado por el **tipo real** (`type(obj)`), el cual nunca debe invertirse con el **tipo declarado** (la anotación estática de la variable) ni confundirse con la simple reasignación dinámica de variables (`x = 5; x = "Hola"`).

## 10. Referencias oficiales

- <https://docs.python.org/3/glossary.html#term-duck-typing> — Glosario oficial de Python (*duck-typing*): definición canónica del polimorfismo basado en comportamiento frente a comprobaciones explícitas de tipo.
- <https://docs.python.org/3/library/functools.html#functools.singledispatch> — Biblioteca estándar (`functools.singledispatch` y `singledispatchmethod`): despacho genérico polimórfico por tipo de argumento.
- <https://docs.python.org/3/library/typing.html#typing.Protocol> — Biblioteca estándar (`typing.Protocol`): subtipado estructural estático para formalizar contratos de *duck typing*.
- <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types> — Referencia del modelo de datos (*Emulating numeric types*): reglas de resolución de operadores binarios, `NotImplemented` y coerción aritmética.
- <https://peps.python.org/pep-0544/> — PEP 544 (*Protocols: Structural subtyping — static duck typing*): especificación oficial de protocolos en el sistema de tipos de Python.
