# Principios de Diseño SOLID Aplicados a la Arquitectura en Python

## 2. Introducción

En el desarrollo de software profesional, la diferencia fundamental entre una base de código frágil y una solución sostenible radica en su capacidad de evolucionar sin degradarse ante nuevos requerimientos de negocio (`Principios_Solid.py` L1-16). Conforme un sistema crece en escala y complejidad, las modificaciones inadvertidas pueden introducir regresiones en cascada, acoplamiento descontrolado y dificultades severas para la ejecución de pruebas automatizadas.

Para mitigar estos riesgos de degradación, Robert C. Martin compiló a inicios de la década de 2000 un conjunto de cinco principios fundamentales de diseño orientado a objetos conocidos por el acrónimo **SOLID**:

1. **S - Principio de Responsabilidad Única (*Single Responsibility Principle*, SRP):** una clase debe tener una, y solo una, razón para cambiar (`SRP.py` L47-60).
2. **O - Principio de Abierto/Cerrado (*Open/Closed Principle*, OCP):** las entidades de software deben estar abiertas para la extensión, pero cerradas para la modificación (`OCP.py` L1-28).
3. **L - Principio de Sustitución de Liskov (*Liskov Substitution Principle*, LSP):** los subtipos deben ser sustituibles por sus tipos base sin alterar la corrección del programa (`LSP.py` L1-8).
4. **I - Principio de Segregación de Interfaces (*Interface Segregation Principle*, ISP):** ningún cliente debe ser forzado a depender de métodos o contratos que no utiliza (`ISP.py` L1-9).
5. **D - Principio de Inversión de Dependencias (*Dependency Inversion Principle*, DIP):** los módulos de alto nivel no deben depender de módulos de bajo nivel; ambos deben depender de abstracciones (`DIP.py` L1-18).

En Python, el tipado dinámico y la ausencia de palabras clave rígidas como `interface` o `implements` no invalidan estos principios; por el contrario, los hacen aún más críticos. Mediante [clases base abstractas](abstraccion_abc.md), protocolos de tipado estructural (`typing.Protocol`), [polimorfismo](../../Intermedio/chapter-five/polimorfismo.md) y técnicas de inyección de dependencias en el constructor, es posible construir arquitecturas modulares, testeables y resistentes al cambio.

## 3. Fundamentos y conceptos

### S - Principio de Responsabilidad Única (SRP)

El Principio de Responsabilidad Única postula que cada clase, módulo o función debe encapsular una única responsabilidad de negocio cohesiva. En términos de mantenimiento, esto implica que una clase debe tener **una sola fuente de cambio** (un único actor o requerimiento que motive su alteración).

En implementaciones iniciales como `Auto` en `SRP.py` (L16-38), una sola clase asume simultáneamente la cinemática de traslación del vehículo (`mover()`), la gestión del depósito de combustible (`combustible`, `agregar_combustible()`) y la notificación de estado en consola. Si la política de recarga o la capacidad del tanque cambia, la clase `Auto` debe modificarse; si cambia la física de movimiento, también. La refactorización hacia `Auto` y `TanqueDeCombustible` (`SRP.py` L61-100) separa la cinemática de la termodinámica del depósito mediante composición, otorgando a cada entidad un propósito delimitado.

### O - Principio de Abierto/Cerrado (OCP)

Formulado originalmente por Bertrand Meyer, el principio prescribe que una entidad debe permitir extender su comportamiento sin necesidad de modificar su código fuente original preexistente.

En lugar de recurrir a cadenas de sentencias condicionales (`if/elif/else` o `match/case`) que inspeccionan el tipo de cliente o canal y que deben editarse cada vez que surge una nueva variante, OCP aprovecha el **polimorfismo dinámico**. Como se observa en `OCP.py` (L31-62), definir una abstracción base `Notificador` permite añadir canales (`NotificarEmail`, `NotificarSMS`, `NotificarWhatsApp`) simplemente creando nuevas subclases sin alterar la clase base ni a los consumidores que la invocan.

> [!NOTE]
> En `OCP.py` (L63), la instanciación `one = NotificarEmail("flavioestrada1412@gmail.com", "hola")` pasa una cadena literal en lugar de un objeto `Usuario`. Al invocar `Notificar()`, el código intenta acceder a `self.usuario.email`, arrojando un error `AttributeError: 'str' object has no attribute 'email'`. En un diseño orientado a objetos riguroso, los datos del destinatario deben modelarse como un objeto de dominio o un tipo estructurado inmutable.

### L - Principio de Sustitución de Liskov (LSP)

Introducido por Barbara Liskov en 1987, el principio establece una definición rigurosa del **subtipado conductual**: si $S$ es un subtipo de $T$, los objetos de tipo $T$ en un programa deben poder ser reemplazados por objetos de tipo $S$ sin alterar ninguna de las propiedades deseables de dicho programa (corrección, invariantes de estado y cumplimiento de contratos).

LSP impone reglas precisas sobre los contratos de métodos:

1. **Contravarianza en los argumentos:** una subclase no puede exigir precondiciones más estrictas que las de la clase base (no puede rechazar parámetros válidos en el padre).
2. **Covarianza en el retorno:** una subclase no puede debilitar las postcondiciones (no puede retornar un rango de valores más amplio o inesperado que el garantizado por el padre).
3. **Invariantes preservadas:** las restricciones de estado del padre deben respetarse en el hijo.
4. **Excepciones coherentes:** una subclase no debe lanzar excepciones no declaradas o conceptualmente incompatibles con las esperadas por el consumidor del tipo base.

En `LSP.py` (L9-22, L26-68), el problema clásico se ilustra mediante la jerarquía de aves: si una clase base `Ave` define `volar()`, derivar una subclase `Pinguino` o `AveNoVoladora` que lance `CantFlyError` o retorne una cadena pasiva como `"Yo no puedo volar"` viola la sustitución de Liskov. Una función diseñada para calcular trayectorias aéreas esperando que `ave.volar()` desplace al animal fallará en tiempo de ejecución. La solución arquitectónica exige segregar la jerarquía: `Ave` agrupa comportamientos universales (`alimentarse()`), mientras que solo `AveVoladora(Ave)` introduce la capacidad `volar()`.

### I - Principio de Segregación de Interfaces (ISP)

El Principio de Segregación de Interfaces dicta que los clientes no deben ser forzados a depender de contratos o métodos que no requieren. Cuando una interfaz acumula responsabilidades dispares, se convierte en una **interfaz obesa (*Fat Interface*)**.

En `ISP.py` (L14-56), una interfaz monolítica `Trabajador(ABC)` define simultáneamente `trabajar()`, `comer()` y `dormir()`. Al intentar derivar una clase `Robot(Trabajador)`, esta se ve obligada a implementar `comer()` y `dormir()` con cuerpos vacíos (`pass`), carentes de significado operativo. La refactorización (`ISP.py` L62-97) descompone el contrato en interfaces independientes y cohesivas: `Trabajador(ABC)`, `Comedor(ABC)` y `Durmiente(ABC)`. De este modo, `Humano` implementa las tres interfaces mediante [herencia múltiple](mro_herencia_multiple.md), mientras que `Robot` implementa exclusivamente `Trabajador`.

### D - Principio de Inversión de Dependencias (DIP)

El Principio de Inversión de Dependencias formaliza la regla cardinal del desacoplamiento arquitectónico en dos postulados:

1. Los módulos de alto nivel (los que contienen las políticas y reglas de negocio esenciales) no deben depender de módulos de bajo nivel (los que ejecutan detalles de infraestructura como bases de datos, redes o APIs de terceros). Ambos deben depender de **abstracciones**.
2. Las abstracciones no deben depender de los detalles; los detalles deben depender de las abstracciones.

En `DIP.py` (L26-38), la clase `CorrectorOrtografico` instancia directamente una dependencia concreta `self.diccionario = Diccionario()` en su constructor. Esto impide reemplazar el diccionario local por un servicio web remoto o por un doble de prueba (*mock*) durante tests unitarios sin modificar la clase principal. Al introducir la interfaz abstracta `VerificadorOrtografico(ABC)` e **inyectar la dependencia en el constructor** (`DIP.py` L45-73), `CorrectorOrtografico` pasa a depender únicamente del contrato abstracto, permitiendo suministrar cualquier proveedor compatible en tiempo de ejecución.

> [!WARNING]
> En `Ejercicio-Final.py` (L34) y `Ejercicio-Final_Optimizado.py` (L4), se incorporaron credenciales fijas en el código fuente (`openai.api_key = "..."`). Esta práctica compromete severamente la seguridad operativa y viola el principio DIP al acoplar rígidamente la lógica a un proveedor externo específico sin parametrización. En sistemas de producción, las credenciales deben suministrarse mediante variables de entorno (`os.getenv`), y los clientes de servicios externos deben inyectarse mediante interfaces desacopladas.

## 4. Sintaxis y funcionamiento

### Matriz conceptual de los principios SOLID

| N° | Principio | Síntoma de violación en código | Patrón o solución técnica en Python | Mecanismo del lenguaje |
|---|---|---|---|---|
| 1 | **SRP** (*Single Responsibility*) | Clases que mezclan lógica de negocio, persistencia SQL y formateo de presentación en pantalla. | Descomposición en clases de dominio, repositorios y presentadores. | Composición y separación modular en [paquetes](../../Intermedio/chapter-three/paquetes.md). |
| 2 | **OCP** (*Open/Closed*) | Bloques `if/elif/else` extensos que se editan cada vez que se agrega un nuevo caso o tipo. | Polimorfismo mediante clases base abstractas o protocolos de estrategia. | `abc.ABC`, `@abstractmethod` y despacho dinámico. |
| 3 | **LSP** (*Liskov Substitution*) | Subclases que sobrescriben métodos para lanzar `NotImplementedError` o alterar firmas de retorno. | Reestructuración de jerarquías; favorecer composición sobre herencia inapropiada. | Tipado estático con `typing` y diseño por contrato. |
| 4 | **ISP** (*Interface Segregation*) | Clases que implementan métodos con `pass` o `raise NotImplementedError` porque la interfaz los obliga. | Descomposición de interfaces voluminosas en contratos de grano fino. | Múltiples clases `ABC` o `typing.Protocol` especializados. |
| 5 | **DIP** (*Dependency Inversion*) | Constructores que instancian dependencias directamente con `self.cliente = ClienteExterno()`. | Inyección de dependencias en el constructor (*Constructor Dependency Injection*). | Parámetros en `__init__(self, servicio: Interfaz)` y contenedores IoC. |

## 5. Ejemplos prácticos progresivos

### Básico

Refactorización guiada por **SRP** y **OCP**. Se transforma un sistema de facturación monolítico que viola ambos principios (acumulando cálculo de impuestos, descuentos acoplados por condicionales e impresión en consola) en componentes cohesivos y extensibles mediante estrategias polimórficas.

```python
from abc import ABC, abstractmethod


# 1. OCP: Contrato abstracto para estrategias de descuento
class EstrategiaDescuento(ABC):
    @abstractmethod
    def calcular_descuento(self, subtotal: float) -> float:
        pass


class SinDescuento(EstrategiaDescuento):
    def calcular_descuento(self, subtotal: float) -> float:
        return 0.0


class DescuentoPorcentual(EstrategiaDescuento):
    def __init__(self, porcentaje: float) -> None:
        self.porcentaje = porcentaje

    def calcular_descuento(self, subtotal: float) -> float:
        return subtotal * (self.porcentaje / 100.0)


# 2. SRP: La clase Pedido gestiona unicamente su coleccion de lineas y su estado de negocio
class Pedido:
    def __init__(self, id_pedido: str) -> None:
        self.id_pedido = id_pedido
        self._items: list[tuple[str, int, float]] = []

    def agregar_item(self, descripcion: str, cantidad: int, precio_unitario: float) -> None:
        self._items.append((descripcion, cantidad, precio_unitario))

    def calcular_subtotal(self) -> float:
        return sum(cantidad * precio for _, cantidad, precio in self._items)


# 3. SRP: Calculadora dedicada que orquesta el total aplicando la estrategia (DIP + OCP)
class CalculadoraTotales:
    def __init__(self, tasa_impuesto: float = 0.18) -> None:
        self.tasa_impuesto = tasa_impuesto

    def liquidar(self, pedido: Pedido, estrategia_descuento: EstrategiaDescuento) -> dict[str, float]:
        subtotal = pedido.calcular_subtotal()
        descuento = estrategia_descuento.calcular_descuento(subtotal)
        base_imponible = max(0.0, subtotal - descuento)
        impuesto = base_imponible * self.tasa_impuesto
        total = base_imponible + impuesto
        return {
            "subtotal": subtotal,
            "descuento": descuento,
            "impuesto": impuesto,
            "total": total,
        }


pedido = Pedido("ORD-2026-001")
pedido.agregar_item("Monitor 27 Pulgadas", 2, 300.0)
pedido.agregar_item("Teclado Mecanico", 1, 100.0)

calculadora = CalculadoraTotales(tasa_impuesto=0.18)
liquidacion = calculadora.liquidar(pedido, DescuentoPorcentual(10.0))

print(f"Pedido: {pedido.id_pedido}")
print(f"Subtotal: {liquidacion['subtotal']:.2f}")
print(f"Descuento (10%): {liquidacion['descuento']:.2f}")
print(f"Impuesto (18%): {liquidacion['impuesto']:.2f}")
print(f"Total Liquidado: {liquidacion['total']:.2f}")
```

Resultado esperado:

```text
Pedido: ORD-2026-001
Subtotal: 700.00
Descuento (10%): 70.00
Impuesto (18%): 113.40
Total Liquidado: 743.40
```

### Intermedio

Aplicación estricta de **LSP** e **ISP** en un ecosistema de procesamiento y digitalización de documentos. Se segregan interfaces monolíticas en contratos específicos (`Imprimible`, `Digitalizable`) para que cada dispositivo físico implemente solo sus capacidades reales, demostrando que cualquier consumidor de `Imprimible` puede sustituir dispositivos de forma transparente sin fallas imprevistas.

```python
from abc import ABC, abstractmethod


# ISP: Segregacion de interfaces en contratos atomicos
class Imprimible(ABC):
    @abstractmethod
    def imprimir(self, contenido: str) -> str:
        pass


class Digitalizable(ABC):
    @abstractmethod
    def escanear(self) -> str:
        pass


# Clases concretas que implementan solo las capacidades que verdaderamente soportan
class ImpresoraTermicaTicket(Imprimible):
    """Dispositivo basico que solo sabe imprimir recibos simples."""
    def imprimir(self, contenido: str) -> str:
        return f"[TICKET FISICO] >>> {contenido.strip()}"


class CentroMultifuncional(Imprimible, Digitalizable):
    """Equipo de oficina que soporta impresion y escaneo."""
    def imprimir(self, contenido: str) -> str:
        return f"[DOCUMENTO A4 ALTA RESOLUCION] >>> {contenido}"

    def escanear(self) -> str:
        return "[DIGITALIZACION OCR] Documento digitalizado en PDF/A-1b"


# LSP: Funcion polimorfica que consume cualquier subtipo de Imprimible sin asumir metodos ajenos
def despachar_reporte(dispositivo: Imprimible, texto: str) -> None:
    # Cumple LSP: garantiza sustituibilidad total sin verificaciones de tipo 'isinstance'
    salida = dispositivo.imprimir(texto)
    print(salida)


termica = ImpresoraTermicaTicket()
multifuncional = CentroMultifuncional()

despachar_reporte(termica, "Total abonado: $45.00 - Gracias por su compra.")
despachar_reporte(multifuncional, "Informe Trimestral de Auditoria Contable.")
print(multifuncional.escanear())
```

Resultado esperado:

```text
[TICKET FISICO] >>> Total abonado: $45.00 - Gracias por su compra.
[DOCUMENTO A4 ALTA RESOLUCION] >>> Informe Trimestral de Auditoria Contable.
[DIGITALIZACION OCR] Documento digitalizado en PDF/A-1b
```

### Avanzado

Arquitectura integral de análisis de sentimientos que demuestra la interacción armónica de los **cinco principios SOLID**. Resuelve de forma limpia el problema planteado en los ejercicios de Dalto (`Con_TextBlob.py`, `Ejercicio-Final.py`, `Ejercicio-Final_Optimizado.py`) sin depender de credenciales externas ni bibliotecas rígidas, permitiendo alternar entre analizadores léxicos locales y clientes de modelos de lenguaje mediante inyección de dependencias en el constructor.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os


# 1. SRP: Entidad inmutable de valor para el resultado de analisis
@dataclass(frozen=True)
class SentimientoClasificado:
    etiqueta: str
    polaridad: float
    confianza: float


# 2. ISP + DIP: Contratos minimos e independientes para componentes del sistema
class ClasificadorSentimiento(ABC):
    """Abstraccion para proveedores de computo de sentimiento."""
    @abstractmethod
    def clasificar(self, texto: str) -> float:
        """Debe retornar un valor continuo entre -1.0 (negativo) y +1.0 (positivo)."""
        pass


class RepositorioAuditoria(ABC):
    """Abstraccion para persistencia de registros de auditoria."""
    @abstractmethod
    def guardar_analisis(self, texto: str, resultado: SentimientoClasificado) -> None:
        pass


# 3. OCP + LSP: Implementaciones intercambiables de clasificadores
class ClasificadorReglasLexicas(ClasificadorSentimiento):
    """Implementacion local determinista basada en conteo de terminos valorativos."""
    def __init__(self) -> None:
        self._positivos = {"excelente", "bueno", "eficiente", "satisfecho", "positivo"}
        self._negativos = {"pesimo", "malo", "deficiente", "inaceptable", "lento"}

    def clasificar(self, texto: str) -> float:
        palabras = texto.lower().split()
        if not palabras:
            return 0.0
        score = 0.0
        for palabra in palabras:
            if palabra in self._positivos:
                score += 1.0
            elif palabra in self._negativos:
                score -= 1.0
        return max(-1.0, min(1.0, score / max(1, len(palabras))))


class ClasificadorModeloRemotoMock(ClasificadorSentimiento):
    """Simulador de LLM o API externa que recibe credenciales de entorno seguras."""
    def __init__(self, api_key_env_var: str = "PROD_API_KEY") -> None:
        # Se verifica la variable sin cablear ningun valor sensible en el codigo fuente
        self._clave_configurada = bool(os.getenv(api_key_env_var, "clave_simulada_segura"))

    def clasificar(self, texto: str) -> float:
        # Simulacion de inferencia
        if "falla" in texto.lower() or "error" in texto.lower():
            return -0.85
        if "exito" in texto.lower() or "aprobado" in texto.lower():
            return 0.90
        return 0.05


# Implementacion concreta de persistencia
class RepositorioMemoria(RepositorioAuditoria):
    def __init__(self) -> None:
        self.historial: list[tuple[str, SentimientoClasificado]] = []

    def guardar_analisis(self, texto: str, resultado: SentimientoClasificado) -> None:
        self.historial.append((texto, resultado))


# 4. DIP + SRP: Servicio de alto nivel coordinado por Inyeccion de Dependencias
class ServicioAnalisisSentimientos:
    def __init__(
        self,
        clasificador: ClasificadorSentimiento,
        repositorio: RepositorioAuditoria,
    ) -> None:
        self._clasificador = clasificador
        self._repositorio = repositorio

    def _interpretar_polaridad(self, polaridad: float) -> str:
        if polaridad > 0.2:
            return "POSITIVO"
        elif polaridad < -0.2:
            return "NEGATIVO"
        return "NEUTRAL"

    def analizar(self, texto: str) -> SentimientoClasificado:
        polaridad = self._clasificador.clasificar(texto)
        etiqueta = self._interpretar_polaridad(polaridad)
        resultado = SentimientoClasificado(
            etiqueta=etiqueta,
            polaridad=round(polaridad, 3),
            confianza=round(abs(polaridad) if abs(polaridad) > 0.1 else 0.5, 2),
        )
        self._repositorio.guardar_analisis(texto, resultado)
        return resultado


# Ensamble de la aplicacion mediante Inversion de Control manual
repo = RepositorioMemoria()
clasificador_local = ClasificadorReglasLexicas()
servicio_local = ServicioAnalisisSentimientos(clasificador=clasificador_local, repositorio=repo)

res1 = servicio_local.analizar("El servicio fue excelente y eficiente")
res2 = servicio_local.analizar("El sistema presento un rendimiento pesimo")

# Sustitucion de proveedor sin modificar el servicio de aplicacion (LSP + OCP + DIP)
clasificador_remoto = ClasificadorModeloRemotoMock()
servicio_remoto = ServicioAnalisisSentimientos(clasificador=clasificador_remoto, repositorio=repo)
res3 = servicio_remoto.analizar("Operacion culminada con exito aprobado")

print(f"Texto 1 -> Etiqueta: {res1.etiqueta} | Polaridad: {res1.polaridad}")
print(f"Texto 2 -> Etiqueta: {res2.etiqueta} | Polaridad: {res2.polaridad}")
print(f"Texto 3 (Remoto) -> Etiqueta: {res3.etiqueta} | Polaridad: {res3.polaridad}")
print(f"Registros totales auditados en repositorio: {len(repo.historial)}")
```

Resultado esperado:

```text
Texto 1 -> Etiqueta: POSITIVO | Polaridad: 0.333
Texto 2 -> Etiqueta: NEGATIVO | Polaridad: -0.167
Texto 3 (Remoto) -> Etiqueta: POSITIVO | Polaridad: 0.9
Registros totales auditados en repositorio: 3
```

## 6. Aplicaciones en el mundo real

Los principios SOLID guían la estructura de los frameworks de referencia en el ecosistema empresarial:

1. **Framework Web FastAPI y su Inyector de Dependencias (`Depends`):** FastAPI implementa el principio de Inversión de Dependencias en el núcleo de su diseño. Los manejadores de rutas declaran dependencias abstractas (`db: Session = Depends(obtener_db)`); el framework inyecta la sesión de base de datos o el usuario autenticado automáticamente, permitiendo sustituir conexiones reales por dobles de pruebas en entornos de integración continua.
2. **Arquitectura Limpia (*Clean Architecture*) y Puertos y Adaptadores:** los microservicios en Python aíslan la lógica de dominio en el núcleo. Los adaptadores de entrada (controladores REST, eventos Kafka) y los adaptadores de salida (SQLAlchemy, clientes Redis, servicios S3) implementan interfaces abstractas definidas en el dominio, protegiendo las reglas de negocio ante cambios tecnológicos en la infraestructura.
3. **Controladores de Almacenamiento en Django (`Storage`):** la clase base abstracta `django.core.files.storage.Storage` define contratos de persistencia de archivos. El código de la aplicación interactúa con métodos como `save()` y `open()` sin acoplarse al sistema de archivos local; cambiar a Amazon S3 o Google Cloud Storage requiere únicamente registrar un nuevo adaptador sin alterar el modelo de datos.

## 7. Uso en producción

Para maximizar los beneficios de SOLID en sistemas distribuidos de misión crítica, conviene adoptar las siguientes prácticas:

1. **Inyección en constructores (*Constructor Injection*) sobre contenedores mágicos:** favorecer la inyección explícita a través de parámetros tipados en `__init__`. El paso explícito de dependencias facilita la legibilidad estática y la detección temprana de errores mediante herramientas como `mypy` y `pytest`.
2. **Evitar la sobreingeniería prematura:** no crear jerarquías de interfaces abstractas para clases simples que tienen una sola implementación prevista y ninguna variabilidad esperada. SOLID debe aplicarse donde existe volatilidad real de requerimientos o necesidad probada de desacoplamiento para pruebas unitarias.
3. **Cero secretos fijos en el código fuente:** toda clave de API, contraseña o cadena de conexión a bases de datos debe externalizarse mediante variables de entorno gestionadas por el orquestador de contenedores o un gestor de secretos (*Vault*, *AWS Secrets Manager*).
4. **Verificación de contratos mediante pruebas unitarias exhaustivas:** escribir pruebas parametrizadas que validen que todas las implementaciones de una interfaz abstracta satisfacen idénticas aserciones de invariantes y manejo de errores (garantía práctica de LSP).

## 8. Errores comunes y recomendaciones

### Caso 1: Violación de LSP al lanzar excepciones incompatibles

Ocurre cuando una subclase altera el contrato conductual de la clase base lanzando excepciones que el cliente no anticipa.

```python
# ERROR INTENCIONAL: Demuestra la violacion de LSP al romper el contrato de una interfaz
class ManejadorArchivo:
    def leer(self, ruta: str) -> str:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()


class ManejadorSoloLecturaVirtual(ManejadorArchivo):
    def leer(self, ruta: str) -> str:
        if ruta.endswith(".sys"):
            # Lanza una excepcion no prevista por el consumidor generico de ManejadorArchivo
            raise PermissionError("Acceso denegado a archivos de sistema")
        return super().leer(ruta)


def procesar_archivos(manejador: ManejadorArchivo, lista_rutas: list[str]) -> None:
    for r in lista_rutas:
        # Falla catastroficamente al recibir ManejadorSoloLecturaVirtual si no esperaba PermissionError
        contenido = manejador.leer(r)
        print(f"Longitud: {len(contenido)}")
```

**Recomendación:** estructurar jerarquías donde las subclases no impongan precondiciones arbitrarias más restrictivas; si una clase requiere restricciones de seguridad distintas, modelarla como un componente de seguridad separado mediante composición.

### Caso 2: Acoplamiento rígido directo violando DIP

Este error reproduce el patrón anti-patrón de instanciación directa de clientes externos dentro del cuerpo del constructor (`DIP.py` L32-34).

```python
# ERROR INTENCIONAL: Demuestra el acoplamiento directo sin inyeccion de dependencias
import os


class ProveedorSMSLocal:
    def enviar(self, telefono: str, mensaje: str) -> bool:
        return True


class GestorNotificaciones:
    def __init__(self) -> None:
        # Viola DIP: acopla directamente el gestor a la implementacion concreta ProveedorSMSLocal
        self.proveedor = ProveedorSMSLocal()

    def alertar(self, telefono: str, texto: str) -> None:
        self.proveedor.enviar(telefono, texto)
```

**Recomendación:** recibir el proveedor como parámetro en `__init__`, tipado contra una clase base abstracta `ProveedorNotificacion(ABC)`:

```text
def __init__(self, proveedor: ProveedorNotificacion) -> None:
    self.proveedor = proveedor
```

### Caso 3: Interfaz obesa con implementaciones vacías violando ISP

Presente en `ISP.py` (L41-56), donde clases concretas se ven forzadas a incorporar métodos que no tienen sentido operativo en su dominio.

```python
# ERROR INTENCIONAL: Muestra una clase forzada a implementar metodos ficticios por ISP roto
from abc import ABC, abstractmethod


class OperacionesDispositivo(ABC):
    @abstractmethod
    def capturar_video(self) -> bytes:
        pass

    @abstractmethod
    def reproducir_audio(self) -> None:
        pass


class AltavozSimple(OperacionesDispositivo):
    def reproducir_audio(self) -> None:
        print("Reproduciendo sonido...")

    def capturar_video(self) -> bytes:
        # Altavoz no tiene camara: forzado a rellenar con cuerpo nulo o excepcion
        raise NotImplementedError("Un altavoz no posee camara")
```

**Recomendación:** segregar `OperacionesDispositivo` en dos contratos independientes: `ReproductorAudio(ABC)` y `CapturadorVideo(ABC)`.

## 9. Resumen

1. El **Principio de Responsabilidad Única (SRP)** busca la alta cohesión asignando una única razón de cambio a cada clase o módulo.
2. El **Principio de Abierto/Cerrado (OCP)** permite extender el comportamiento del sistema añadiendo nuevas clases polimórficas sin modificar el código fuente establecido.
3. El **Principio de Sustitución de Liskov (LSP)** garantiza que los subtipos respeten fielmente las precondiciones, postcondiciones e invariantes de sus tipos base.
4. El **Principio de Segregación de Interfaces (ISP)** combate las interfaces monolíticas dividiéndolas en contratos específicos y enfocados en las necesidades de cada cliente.
5. El **Principio de Inversión de Dependencias (DIP)** desacopla la política de negocio de los detalles de infraestructura haciendo que ambos dependan de abstracciones.
6. En Python, la combinación de `abc.ABC`, `typing.Protocol` y la **Inyección de Dependencias en el constructor** permite materializar SOLID de manera idiomática, segura y altamente comprobable.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/Principios_Solid.py` | `Principios_Solid.py` | Definición de atributos de calidad de software: mantenibilidad, reusabilidad, legibilidad y extensibilidad (L12-32). | Fundamentación teórica y taxonómica formal de los 5 principios SOLID y su impacto en el ciclo de vida del software en producción. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/SRP.py` | `SRP.py` | Clase inicial `Auto` con responsabilidades mezcladas y refactorización desacoplada mediante `TanqueDeCombustible`. | Formalización de la cohesión funcional y separación estricta entre modelos de dominio, reglas de cálculo y persistencia. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/OCP.py` | `OCP.py` | Jerarquía `Notificador` con métodos abstractos manuales y especializaciones por canal (`Email`, `SMS`, `WhatsApp`). | Diagnóstico y corrección del error de tipo en línea 63 (paso de `str` en lugar de `Usuario`); sustitución de `raise NotImplementedError` por contratos formales con `abc.ABC`. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/LSP.py` | `LSP.py` | Modelado de aves voladoras y no voladoras (`Ave`, `AveVoladora`, `AveNoVoladora`). | Análisis formal de precondiciones y postcondiciones conductuales; demostración de por qué una subclase no voladora que retorna cadenas de advertencia en `volar()` quebranta la sustitución polimórfica. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/ISP.py` | `ISP.py` | Interfaz unificada `Trabajador` frente a interfaces segregadas `Trabajador`, `Comedor`, `Durmiente`. | Análisis de la sobrecarga de métodos en clases de dominio y demostración de combinación limpia mediante herencia múltiple de interfaces mínimas. |
| `CLASS_PY_POO` | `CLASE_FOUR/CLASE_CUARTA/DIP.py` | `DIP.py` | Acoplamiento rígido de `CorrectorOrtografico` con `Diccionario` y solución desacoplada con `VerificadorOrtografico(ABC)`. | Sistematización del patrón de Inyección de Dependencias por Constructor y su vinculación con la Arquitectura Hexagonal y pruebas unitarias con dobles. |
| `CLASS_PY_POO` | `CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` | `Con_TextBlob.py` | Clasificación de sentimientos mediante polaridad de TextBlob y asignación de rangos a objetos `Sentimiento`. | Desacoplamiento del algoritmo de análisis léxico mediante el patrón de estrategia polimórfica, permitiendo alternar librerías de PLN sin alterar clientes. |
| `CLASS_PY_POO` | `CLASE_FOUR/EJERCICIO_FINAL/Ejercicio-Final.py` | `Ejercicio-Final.py` | ChatBot con API de OpenAI cableando credenciales en texto plano en el archivo y reglas rígidas condicionales. | Eliminación de credenciales sensibles en código; implementación de inyección segura con variables de entorno (`os.getenv`) y abstracciones de modelos de lenguaje. |
| `CLASS_PY_POO` | `CLASE_FOUR/EJERCICIO_FINAL/Ejercicio-Final_Optimizado.py` | `Ejercicio-Final_Optimizado.py` | Estructuración modular con clases `Sentimiento` y mapeo de rangos con llamada de inferencia a OpenAI. | Integración global de los 5 principios SOLID en un sistema de análisis de sentimientos completamente testeable, extensible y desacoplado de dependencias de terceros. |

**Fundamento complementario:** los ejemplos originales introducen los principios mediante ejercicios independientes y proyectos prácticos de análisis de sentimientos con APIs externas. Esta guía complementa el material original corrigiendo fallos de seguridad (erradicación total de claves de API expuestas), subsanando excepciones de tipado y proporcionando una arquitectura integral donde los cinco principios colaboran de forma sinérgica.

## 11. Referencias oficiales

- Biblioteca Estándar de Python: Módulo `abc` (Abstract Base Classes):
  https://docs.python.org/3/library/abc.html
- Biblioteca Estándar de Python: Módulo `typing` (Type Hints y protocolos de diseño):
  https://docs.python.org/3/library/typing.html
- PEP 3119: Introducing Abstract Base Classes:
  https://peps.python.org/pep-3119/
- PEP 544: Protocols: Structural subtyping (static duck typing):
  https://peps.python.org/pep-0544/
