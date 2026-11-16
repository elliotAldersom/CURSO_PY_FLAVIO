# Gestores de Contexto y Gestión Determinista de Recursos (`with` y `contextlib`)

## 2. Introducción

En el diseño de sistemas de producción, uno de los errores más frecuentes y difíciles de diagnosticar es la fuga de recursos (*resource leaks*): descriptores de archivos que permanecen abiertos consumiendo cuotas del sistema operativo, conexiones de red o bases de datos no devueltas al grupo de conexiones (*connection pool*), bloqueos de concurrencia (*locks*) que nunca se liberan provocando bloqueos mutuos (*deadlocks*), o estados globales alterados que no se restauran tras una excepción imprevista.

Tradicionalmente, la liberación de recursos se gestionaba mediante bloques `try...finally`. Aunque funcional, este patrón resulta verboso, propenso a descuidos manuales y difícil de componer cuando intervienen múltiples recursos dependientes.

Python formalizó en **PEP 343** la sentencia **`with`** y el **protocolo de gestión de contexto** (*Context Manager Protocol*): un mecanismo idiomático y determinista que garantiza que la fase de inicialización y la fase de limpieza o liberación de un recurso se ejecuten siempre, sin importar si el bloque de código finaliza con éxito o se interrumpe por una [excepción](../../Intermedio/chapter-four/excepciones.md) en tiempo de ejecución.

## 3. Fundamentos y conceptos

**El protocolo de gestión de contexto: `__enter__` y `__exit__`.**
Un objeto se califica formalmente como gestor de contexto en Python si implementa los dos métodos especiales del protocolo:

1. **`__enter__(self)`:**
   - Se ejecuta inmediatamente antes de que el flujo de control ingrese al cuerpo del bloque `with`.
   - Puede inicializar el recurso, abrir la conexión o adquirir el bloqueo.
   - Su valor de retorno se asigna opcionalmente al identificador especificado en la cláusula `as variable` (por ejemplo, `with open(...) as f:` asigna a `f` el objeto archivo devuelto por `__enter__`).
2. **`__exit__(self, exc_type, exc_val, exc_tb)`:**
   - Se garantiza su ejecución incondicional al salir del bloque `with`, ya sea de forma normal, mediante una sentencia `return`, `break`, `continue` o por una excepción no capturada.
   - Si no ocurrió ningún error, los tres parámetros de excepción son `None`: `(None, None, None)`.
   - Si se lanzó una excepción dentro del bloque, Python entrega:
     - `exc_type`: la clase de la excepción (p. ej. `ValueError`).
     - `exc_val`: la instancia de la excepción con el mensaje de error.
     - `exc_tb`: el objeto de rastreo de pila (*traceback*).
   - **Mecanismo de supresión de excepciones:** si `__exit__` devuelve un valor booleano evaluado como `True`, Python **suprime la excepción** y continúa la ejecución normal tras el bloque `with`. Si devuelve `None`, `False` o no retorna nada, la excepción se propaga hacia arriba en la pila de llamadas.

**Creación funcional con `@contextlib.contextmanager`.**
Escribir una clase completa con `__enter__` y `__exit__` puede resultar excesivamente verboso para gestiones simples. El módulo estándar `contextlib` provee el decorador `@contextmanager`, el cual transforma una [función generadora](iteradores.md) que contiene una única sentencia `yield` en un gestor de contexto completo:
- El código previo a `yield` se ejecuta como `__enter__`.
- El valor suministrado a `yield` se asigna a la variable en `as`.
- El código posterior a `yield` se envuelve en un bloque `finally` para actuar como `__exit__`.

**Utilidades avanzadas de `contextlib`.**
La biblioteca estándar proporciona herramientas especializadas para composición de contextos:
- `contextlib.suppress(*excepciones)`: suprime de forma declarativa excepciones específicas (reemplazando bloques `try: ... except Err: pass`).
- `contextlib.closing(objeto)`: garantiza invocar `.close()` sobre objetos que carecen del protocolo nativo `with` (como sockets o conexiones legadas).
- `contextlib.nullcontext(enter_result=None)`: gestor no-operacional (*no-op*) útil como comodín cuando el uso de un gestor de contexto es condicional.
- `contextlib.ExitStack`: contenedor programático dinámico que permite gestionar una cantidad variable de recursos desconocida en tiempo de codificación (p. ej. abrir una lista de 50 archivos simultáneos asegurando el cierre atómico de todos).

## 4. Sintaxis y funcionamiento

Implementación canónica basada en clases:

```python
class GestorRecurso:
    def __init__(self, identificador: str) -> None:
        self.identificador = identificador

    def __enter__(self) -> "GestorRecurso":
        # Inicializar y reservar recurso
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Liberar recurso incondicionalmente
        # Retornar True para suprimir la excepción si exc_type no es None
        return False
```

Implementación funcional con `@contextlib.contextmanager`:

```python
from contextlib import contextmanager
from typing import Generator


@contextmanager
def contexto_temporal(etiqueta: str) -> Generator[str, None, None]:
    # 1. Fase de preparación (__enter__)
    print(f"Preparando: {etiqueta}")
    try:
        yield etiqueta.upper()  # Valor asignado a la cláusula 'as'
    finally:
        # 2. Fase de limpieza incondicional (__exit__)
        print(f"Limpiando: {etiqueta}")
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Cronómetro de alta precisión (`time.perf_counter`) y gestor de supresión segura.**

```python
from contextlib import suppress
import time


class CronometroBloque:
    """Mide con precisión de nanosegundos el tiempo transcurrido en un bloque with."""

    def __init__(self, etiqueta: str) -> None:
        self.etiqueta = etiqueta
        self.tiempo_inicio: float = 0.0
        self.duracion_segundos: float = 0.0

    def __enter__(self) -> "CronometroBloque":
        self.tiempo_inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.duracion_segundos = time.perf_counter() - self.tiempo_inicio
        print(f"[{self.etiqueta}] Ejecutado en: {self.duracion_segundos * 1000:.3f} ms")


# 1. Medir tiempo de un cálculo
with CronometroBloque("Calculo de suma vectorial") as crono:
    acumulado = sum(i**2 for i in range(100_000))

# 2. Uso de contextlib.suppress para omitir excepciones esperadas sin bloques try/except verbosos
archivo_opcional = {"configurado": False}
with suppress(KeyError):
    valor = archivo_opcional["puerto_inexistente"]

print("Cálculo finalizado exitosamente. Acumulado:", acumulado > 0)
print("Supresión completada sin interrumpir el flujo.")
```

Explicación paso a paso:

- `CronometroBloque` implementa `__enter__` registrando la marca temporal de alta resolución mediante `time.perf_counter()`.
- Al finalizar el bloque, `__exit__` se ejecuta automáticamente y calcula la diferencia en milisegundos, imprimiendo el resultado antes de que el programa continúe.
- `suppress(KeyError)` captura la excepción de clave ausente y silencia el error limpiamente sin propagarlo, permitiendo un código compacto y declarativo.

Resultado esperado:

```text
[Calculo de suma vectorial] Ejecutado en: 18.450 ms
Cálculo finalizado exitosamente. Acumulado: True
Supresión completada sin interrumpir el flujo.
```

### Intermedio

**Ejemplo 2 — Gestor funcional `@contextmanager` para redirección temporal de configuración y gestión transaccional.**

```python
from contextlib import contextmanager
from typing import Any, Generator


class ConfiguracionSistema:
    def __init__(self) -> None:
        self.parametros = {"modo": "PROD", "nivel_log": "WARNING", "reintentos": 3}


@contextmanager
def configurar_temporalmente(
    config: ConfiguracionSistema, **cambios: Any
) -> Generator[dict[str, Any], None, None]:
    """Sobrescribe temporalmente parámetros del sistema y restaura el estado previo incondicionalmente."""
    # 1. Respaldar estado original
    respaldo = config.parametros.copy()

    # 2. Aplicar modificaciones temporales
    config.parametros.update(cambios)
    print("-> Parámetros temporales activados:", config.parametros)

    try:
        yield config.parametros  # Cede el control al bloque with
    except Exception as err:
        print(f"-> Error detectado durante el bloque: {type(err).__name__} ({err})")
        raise  # Re-lanzar para que el llamador decida
    finally:
        # 3. Restaurar obligatoriamente el estado original en el finally
        config.parametros = respaldo
        print("-> Parámetros restaurados al estado original:", config.parametros)


# Demostración práctica
sistema = ConfiguracionSistema()
print("Configuración inicial:", sistema.parametros)

# Aplicar contexto temporal para una tarea de diagnóstico
with configurar_temporalmente(sistema, modo="DEBUG", nivel_log="DEBUG") as parametros_activos:
    print("   Ejecutando tarea bajo:", parametros_activos["modo"])

print("Configuración final verificada:", sistema.parametros)
```

Explicación técnica:

- El decorador `@contextmanager` de `contextlib` captura las excepciones que ocurran dentro del bloque `with` en el punto exacto donde se encuentra la sentencia `yield`.
- La cláusula `finally` garantiza que, incluso si el código del cliente lanza una excepción fatal dentro del bloque `with`, los parámetros del sistema se reestablezcan con exactitud a su copia de respaldo previa, evitando contaminación del entorno global en pruebas o producción.

Resultado esperado:

```text
Configuración inicial: {'modo': 'PROD', 'nivel_log': 'WARNING', 'reintentos': 3}
-> Parámetros temporales activados: {'modo': 'DEBUG', 'nivel_log': 'DEBUG', 'reintentos': 3}
   Ejecutando tarea bajo: DEBUG
-> Parámetros restaurados al estado original: {'modo': 'PROD', 'nivel_log': 'WARNING', 'reintentos': 3}
Configuración final verificada: {'modo': 'PROD', 'nivel_log': 'WARNING', 'reintentos': 3}
```

### Avanzado

**Ejemplo 3 — Gestor de transacciones atómicas de base de datos en memoria con Rollback automático y composición dinámica con `ExitStack`.**

```python
from contextlib import ExitStack
import tempfile
from pathlib import Path


class BaseDatosEnMemoria:
    """Simula un almacén transaccional clave-valor con aislamiento y rollback."""

    def __init__(self) -> None:
        self._datos: dict[str, int] = {"saldo_ana": 1000, "saldo_luis": 500}

    def transaccion(self) -> "GestorTransaccion":
        return GestorTransaccion(self)

    @property
    def datos(self) -> dict[str, int]:
        return self._datos.copy()


class GestorTransaccion:
    def __init__(self, bd: BaseDatosEnMemoria) -> None:
        self.bd = bd
        self.respaldo: dict[str, int] = {}

    def __enter__(self) -> dict[str, int]:
        # Copia defensiva de respaldo para rollback
        self.respaldo = self.bd._datos.copy()
        return self.bd._datos

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            # Ocurrió un error en la transacción: aplicar ROLLBACK inmediato
            self.bd._datos = self.respaldo
            print(f"[TRANSACCIÓN FALLIDA] Rollback ejecutado. Motivo: {exc_val}")
            # Supresión controlada si es un error de negocio esperado (SaldoInsuficienteError)
            return True if issubclass(exc_type, ValueError) else False
        else:
            # Confirmar cambios (COMMIT)
            print("[TRANSACCIÓN EXITOSA] Commit confirmado.")
            return False


# Demostración 1: Transacción atómica con fallo provocado
bd = BaseDatosEnMemoria()
print("Estado inicial BD:", bd.datos)

with bd.transaccion() as sesion:
    sesion["saldo_ana"] -= 200
    sesion["saldo_luis"] += 200
    # Simular regla de negocio violada
    if sesion["saldo_ana"] < 900:
        raise ValueError("Límite de transferencia diario excedido")

print("Estado BD tras rollback automático:", bd.datos)

# Demostración 2: Apertura dinámica de múltiples archivos con ExitStack
with tempfile.TemporaryDirectory() as temp_dir:
    raiz = Path(temp_dir)
    rutas = [raiz / f"log_{i}.txt" for i in range(3)]

    # Abrir N archivos de forma determinista asegurando el cierre atómico de todos
    with ExitStack() as stack:
        manejadores = [stack.enter_context(open(r, "w", encoding="utf-8")) for r in rutas]
        for idx, f in enumerate(manejadores):
            f.write(f"Registro en archivo {idx}\n")

    # Verificar que todos los archivos se cerraron automáticamente
    todos_cerrados = all(m.closed for m in manejadores)
    print("Todos los archivos cerrados por ExitStack:", todos_cerrados)
```

Explicación de ingeniería:

- En `GestorTransaccion`, `__enter__` almacena una copia exacta del estado previo. Si se lanza una excepción dentro de la transacción, `__exit__` intercepta el fallo (`exc_type is not None`) y restaura inmediatamente los saldos originales.
- Al retornar `True` cuando `issubclass(exc_type, ValueError)`, el gestor suprime la excepción de negocio controlada, permitiendo al sistema reanudar la operación sin interrupción abrupta de la API.
- `ExitStack` resuelve el problema arquitectónico de anidar dinámicamente una lista arbitraria de recursos en tiempo de ejecución. Permite apilar llamadas a `enter_context()` y garantiza que se invoque el método `__exit__` de cada manejador en orden LIFO estricto cuando el bloque finaliza.

Resultado esperado:

```text
Estado inicial BD: {'saldo_ana': 1000, 'saldo_luis': 500}
[TRANSACCIÓN FALLIDA] Rollback ejecutado. Motivo: Límite de transferencia diario excedido
Estado BD tras rollback automático: {'saldo_ana': 1000, 'saldo_luis': 500}
Todos los archivos cerrados por ExitStack: True
```

## 6. Aplicaciones en el mundo real

- **Gestión de conexiones a bases de datos y sesiones ORM:** transacciones atómicas con SQLAlchemy o Django ORM, asegurando `commit` ante éxito y `rollback` automático ante fallos de integridad referencial.
- **Sistemas de concurrencia y exclusión mutua:** adquisición y liberación segura de cerrojos (`threading.Lock` o `multiprocessing.Lock`), previniendo bloqueos mutuos (*deadlocks*) por excepciones imprevistas.
- **Redirección de flujos estándar y mocking en pruebas:** aislamiento de salidas de consola con `contextlib.redirect_stdout` y parchado temporal de servicios externos con `unittest.mock.patch`.
- **Gestión de recursos de hardware y GPU:** asignación de dispositivos en PyTorch/TensorFlow (`with torch.no_grad():` o `with tf.device('/GPU:0'):`).

## 7. Uso en producción

- **No suprimir excepciones de forma indiscriminada:** devolver `True` en `__exit__` silencia la excepción por completo. Solo debe suprimirse si el error fue completamente gestionado, reparado o mitigado; de lo contrario, oculta errores fatales de lógica o de sintaxis que dificultan el diagnóstico en logs de producción.
- **Utilizar `ExitStack` para listas variables de recursos:** nunca abrir colecciones de archivos mediante comprensiones de listas directas dentro de un `with`, pues si el quinto archivo falla, los cuatro anteriores quedan desprotegidos. `ExitStack` garantiza la limpieza coordinada de todos los recursos previamente abiertos.
- **Mantener los métodos `__enter__` y `__exit__` libres de bloqueos pesados:** el protocolo de contexto debe ser rápido y confiable; cálculos de CPU masivos o llamadas de red lentas deben ejecutarse dentro del cuerpo del bloque `with`, no en los métodos de ciclo de vida del gestor.
- **Preferir `@contextlib.contextmanager` para gestores de corta vida:** cuando la lógica de limpieza sea lineal, la función generadora con `try...finally` es más legible, concisa y mantenible que una clase completa.

## 8. Errores comunes y recomendaciones

1. **Olvidar la cláusula `finally` en funciones decoradas con `@contextmanager`.**

```python
from contextlib import contextmanager


# ERROR: si ocurre una excepción en el yield, el código posterior nunca se ejecuta
@contextmanager
def gestor_inseguro():
    print("Inicio")
    yield  # Si el usuario lanza un error aquí, la línea siguiente no se alcanza
    print("Fin")  # Fuga de recurso latente
```

Diagnóstico: el generador pausa su ejecución en `yield`. Si el bloque `with` lanza una excepción, esta se reinyecta en el generador en esa misma instrucción; sin un bloque `try...finally`, el código de limpieza es omitido. Recomendación: escribir siempre `try: yield finally: limpieza()`.

2. **Retornar el valor equivocado en `__enter__`.**

```python
class ConexionBD:
    def __enter__(self):
        self.conectar()
        # ERROR: si no se escribe "return self" o el cliente de conexión,
        # la cláusula "as var" asignará None
```

Diagnóstico: si `__enter__` omite la sentencia `return`, devuelve implícitamente `None`. Al escribir `with ConexionBD() as c:`, la variable `c` valdrá `None` y cualquier método posterior fallará con `AttributeError`. Recomendación: retornar explícitamente `self` o el objeto que el cliente deba manipular.

3. **Confundir la invocación de `contextlib.suppress` pasando instancias en lugar de clases.**

```python
from contextlib import suppress

# ERROR: suppress recibe tipos/clases de excepciones, no instancias
# with suppress(FileNotFoundError("archivo no existe")):  # Incorrecto
with suppress(FileNotFoundError):  # Correcto
    pass
```

Diagnóstico: `suppress` compara tipos mediante `issubclass(exc_type, expected)`. Pasar una instancia lanza un `TypeError`.

## 9. Resumen

- La sentencia **`with`** (**PEP 343**) implementa la gestión determinista de recursos, garantizando la ejecución de la fase de limpieza incondicionalmente.
- El protocolo se compone de **`__enter__`** (inicialización y asignación a `as`) y **`__exit__`** (liberación e inspección de excepciones).
- Si `__exit__` retorna `True`, la excepción ocurrida en el bloque es **suprimida**; de lo contrario, se propaga normalmente.
- El decorador **`@contextlib.contextmanager`** permite construir gestores de contexto de forma funcional y concisa a partir de generadores con `yield` envueltos en `try...finally`.
- La clase **`contextlib.ExitStack`** resuelve la gestión programática y dinámica de múltiples recursos simultáneos en tiempo de ejecución.

## 10. Referencias oficiales

- <https://docs.python.org/3/reference/datamodel.html#context-managers> — Referencia del modelo de datos de Python: especificación formal del protocolo `__enter__` y `__exit__`.
- <https://docs.python.org/3/library/contextlib.html> — Biblioteca estándar (`contextlib`): utilidades `contextmanager`, `suppress`, `closing` y `ExitStack`.
- <https://peps.python.org/pep-0343/> — PEP 343 (*The "with" Statement*): especificación histórica y diseño de la sentencia `with`.
- <https://docs.python.org/3/library/exceptions.html> — Jerarquía estándar de excepciones y propagación de errores en Python.

