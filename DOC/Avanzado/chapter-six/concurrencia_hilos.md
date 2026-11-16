# Concurrencia con Hilos y Exclusión Mutua (`threading` y `concurrent.futures`)

## 2. Introducción

En el desarrollo de software moderno, una aplicación rara vez opera de forma aislada y puramente secuencial: debe comunicarse con APIs remotas, consultar bases de datos, leer archivos de disco o esperar eventos de usuarios de forma simultánea.

Si un programa ejecuta estas tareas de forma estrictamente síncrona, cada operación de entrada/salida (*I/O*) bloquea por completo el hilo principal de ejecución, desperdiciando ciclos de CPU mientras el procesador aguarda pasivamente respuestas de la red o del disco.

Para abordar este escenario, Python provee el modelo de **concurrencia basado en hilos de ejecución (*threads*)** a través de los módulos estándar `threading` y `concurrent.futures`. Dominar los hilos en Python exige comprender la distinción crítica entre tareas **I/O-bound** (limitadas por entrada/salida) y tareas **CPU-bound** (limitadas por cómputo matemático), el papel del **Bloqueo Global del Intérprete (*GIL*, Global Interpreter Lock)** en CPython, los riesgos de **condiciones de carrera (*race conditions*)** sobre el estado compartido y los mecanismos de sincronización mediante cerrojos de exclusión mutua (**`Lock`**).

## 3. Fundamentos y conceptos

**Concurrencia frente a Paralelismo real.**
- **Concurrencia:** es la capacidad de gestionar múltiples tareas simultáneas intercalando su avance en el tiempo (*interleaving*). Es ideal para operaciones I/O-bound donde la mayor parte del tiempo se consume esperando respuestas externas.
- **Paralelismo:** es la ejecución física de dos o más instrucciones en el mismo instante exacto sobre múltiples núcleos de CPU de forma simultánea. En Python estándar, el paralelismo puro de cómputo se alcanza mediante [multiprocesamiento](multiprocesamiento.md).

**El Bloqueo Global del Intérprete (GIL, *Global Interpreter Lock*) en CPython.**
En la implementación de referencia CPython, la gestión de memoria interna no es segura ante hilos concurrentes nativos (*thread-safe*): el conteo de referencias de los objetos `PyObject` podría corromperse si dos hilos modifican el mismo contador simultáneamente.
- Para prevenir la corrupción de memoria, CPython introduce el **GIL**: un cerrojo a nivel de proceso que garantiza que **solo un hilo de Python ejecute bytecode a la vez**, incluso si la máquina posee 32 núcleos de CPU físicos.
- **Consecuencia para tareas CPU-bound:** crear múltiples hilos para cálculos matemáticos intensivos (p. ej. calcular números primos o entrenar modelos) no acelera la ejecución; por el contrario, suele degradar el rendimiento debido a la sobrecarga de conmutación de contexto (*context switching*).
- **Consecuencia para tareas I/O-bound:** cuando un hilo inicia una operación bloqueante del sistema operativo (descarga HTTP, lectura de archivo, consulta de base de datos o llamada a funciones optimizadas en C como en [NumPy](../../Intermedio/chapter-six/numpy_fundamentos.md)), **CPython libera inmediatamente el GIL**, permitiendo que otros hilos de Python avancen concurrentemente.

**Condiciones de carrera (*Race Conditions*) y Exclusión Mutua (`Lock`).**
Aunque el GIL garantiza la integridad interna de CPython, **no protege la lógica de negocio ni el estado compartido de la aplicación**:
- El intérprete de Python puede alternar entre hilos en cualquier instrucción de bytecode intermedia (típicamente cada 5 milisegundos o 100 instrucciones).
- Una operación aparentemente atómica como `contador += 1` consta en realidad de tres pasos de bajo nivel: leer el valor actual (`BINARY_OP`), sumar 1 en la pila y escribir el resultado de vuelta (`STORE_NAME`). Si dos hilos leen el mismo valor antes de escribir, se produce una **condición de carrera** y una actualización se pierde irremediablemente.
- **`threading.Lock`:** cerrojo de sincronización que implementa el protocolo de [gestores de contexto](../chapter-one/context_managers.md) (`with lock:`). Garantiza que solo un hilo acceda a la sección crítica a la vez, serializando de forma segura las mutaciones del estado compartido.

**Pools de hilos con `concurrent.futures.ThreadPoolExecutor`.**
Crear y destruir hilos manualmente con `threading.Thread` es costoso y propenso a desbordamiento de recursos. El módulo estándar `concurrent.futures` provee la abstracción de alto nivel `ThreadPoolExecutor`:
- Gestiona un grupo predeterminado de hilos reutilizables (*worker threads*).
- Asigna tareas de forma desacoplada y retorna objetos `Future` que encapsulan el estado de la tarea (pendiente, ejecutando, completada o fallida con excepción).
- Ofrece métodos declarativos de mapeo concurrente (`executor.map()`) y procesamiento por orden de finalización (`as_completed()`).

## 4. Sintaxis y funcionamiento

Uso básico de `threading.Thread` y sincronización con `Lock`:

```python
import threading

bloqueo = threading.Lock()
saldo_compartido = 1000


def retirar_dinero(monto: int) -> None:
    global saldo_compartido
    # Sección crítica protegida con exclusión mutua
    with bloqueo:
        if saldo_compartido >= monto:
            saldo_compartido -= monto
```

Gestión concurrente con `concurrent.futures.ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def consultar_servicio(url: str) -> str:
    # Simula llamada I/O de red
    return f"Respuesta de {url}"


urls = ["https://api.servicio.com/a", "https://api.servicio.com/b"]

# Context manager que asegura el cierre ordenado de todos los hilos
with ThreadPoolExecutor(max_workers=5) as executor:
    # Mapeo directo conservando el orden de entrada
    respuestas = list(executor.map(consultar_servicio, urls))
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Lanzamiento y coordinación de hilos con `threading.Thread` y espera determinista con `.join()`.**

```python
import threading
import time


def tarea_descarga(archivo_id: int, duracion_segundos: float) -> None:
    """Simula la descarga de un recurso remoto I/O-bound."""
    nombre_hilo = threading.current_thread().name
    print(f"[{nombre_hilo}] Iniciando descarga de archivo {archivo_id}...")
    time.sleep(duracion_segundos)  # Simula espera pasiva de red (libera el GIL)
    print(f"[{nombre_hilo}] Archivo {archivo_id} descargado exitosamente.")


# 1. Crear hilos de ejecución independientes
hilo_1 = threading.Thread(target=tarea_descarga, args=(101, 0.2), name="Worker-A")
hilo_2 = threading.Thread(target=tarea_descarga, args=(102, 0.1), name="Worker-B")

tiempo_inicio = time.perf_counter()

# 2. Iniciar ejecución concurrente
hilo_1.start()
hilo_2.start()

# 3. Esperar deterministamente a que ambos hilos finalicen (join)
hilo_1.join()
hilo_2.join()

duracion_total = time.perf_counter() - tiempo_inicio

print(f"\nTodas las descargas han concluido.")
print(f"Tiempo total transcurrido: {duracion_total:.2f} s (esperado ~0.2 s, no 0.3 s)")
```

Explicación paso a paso:

- `hilo.start()` solicita al sistema operativo la creación del hilo nativo y comienza a ejecutar la función objetivo en segundo plano de forma no bloqueante.
- `time.sleep()` cede voluntariamente el GIL al sistema operativo; mientras el `Worker-A` duerme esperando sus datos de red, el `Worker-B` avanza en paralelo.
- `hilo.join()` bloquea el hilo principal hasta que el hilo correspondiente termine; si no se invoca `join()`, el hilo principal continuaría de inmediato sin esperar los resultados.
- La duración total es aproximadamente 0.2 segundos (el máximo de las duraciones individuales), demostrando la concurrencia frente a la ejecución secuencial acumulativa (0.3 s).

Resultado esperado:

```text
[Worker-A] Iniciando descarga de archivo 101...
[Worker-B] Iniciando descarga de archivo 102...
[Worker-B] Archivo 102 descargado exitosamente.
[Worker-A] Archivo 101 descargado exitosamente.

Todas las descargas han concluido.
Tiempo total transcurrido: 0.20 s (esperado ~0.2 s, no 0.3 s)
```

### Intermedio

**Ejemplo 2 — Demostración de Condición de Carrera (*Race Condition*) y solución con exclusión mutua (`threading.Lock`).**

```python
import threading
from concurrent.futures import ThreadPoolExecutor

# Estado compartido
contador_inseguro = 0
contador_seguro = 0
bloqueo_cerrojo = threading.Lock()

ITERACIONES_POR_HILO = 10_000
NUM_HILOS = 10


def incrementar_sin_proteccion() -> None:
    global contador_inseguro
    for _ in range(ITERACIONES_POR_HILO):
        # Operación vulnerable a intercalado de hilos: no atómica
        actual = contador_inseguro
        contador_inseguro = actual + 1


def incrementar_con_lock() -> None:
    global contador_seguro
    for _ in range(ITERACIONES_POR_HILO):
        # Sección crítica protegida
        with bloqueo_cerrojo:
            contador_seguro += 1


# 1. Ejecutar sin protección
with ThreadPoolExecutor(max_workers=NUM_HILOS) as executor:
    futuros_inseguros = [executor.submit(incrementar_sin_proteccion) for _ in range(NUM_HILOS)]

# 2. Ejecutar con cerrojo de exclusión mutua
with ThreadPoolExecutor(max_workers=NUM_HILOS) as executor:
    futuros_seguros = [executor.submit(incrementar_con_lock) for _ in range(NUM_HILOS)]

valor_esperado = NUM_HILOS * ITERACIONES_POR_HILO

print(f"Total esperado exacto         : {valor_esperado:,}")
print(f"Resultado CONcurrente INSEGURO : {contador_inseguro:,}")
print(f"Resultado CONcurrente SEGURO   : {contador_seguro:,}")
print(f"¿Ocurrió pérdida de datos?     : {contador_inseguro != valor_esperado}")
print(f"¿El cerrojo fue 100% efectivo? : {contador_seguro == valor_esperado}")
```

Explicación técnica:

- En `incrementar_sin_proteccion`, dos o más hilos leen simultáneamente la variable `contador_inseguro` antes de que el otro hilo haya completado la reasignación, produciendo colisiones de sobrescritura que mutilan miles de actualizaciones.
- En `incrementar_con_lock`, la cláusula `with bloqueo_cerrojo:` adquiere el cerrojo antes de la mutación y lo libera incondicionalmente tras escribir, garantizando atomicidad lógica y alcanzando los $100\,000$ incrementos exactos sin pérdida de datos.

Resultado esperado:

```text
Total esperado exacto         : 100,000
Resultado CONcurrente INSEGURO : 73,421
Resultado CONcurrente SEGURO   : 100,000
¿Ocurrió pérdida de datos?     : True
¿El cerrojo fue 100% efectivo? : True
```

### Avanzado

**Ejemplo 3 — Sistema de recolección de métricas I/O concurrentes con `ThreadPoolExecutor`, timeouts y manejo de excepciones con `as_completed`.**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import random
import time


@dataclass(frozen=True)
class ResultadoSonda:
    endpoint_id: int
    latencia_ms: float
    exitoso: bool
    mensaje: str


def sondear_endpoint(endpoint_id: int) -> ResultadoSonda:
    """Sondea un microservicio remoto con simulación de latencia variable y fallos controlados."""
    # Simular latencia de red entre 20ms y 120ms
    latencia = random.uniform(0.02, 0.12)
    time.sleep(latencia)

    # Simular un fallo controlado en el endpoint 3
    if endpoint_id == 3:
        raise ConnectionResetError("Servicio remoto cerró la conexión abruptamente")

    return ResultadoSonda(
        endpoint_id=endpoint_id,
        latencia_ms=round(latencia * 1000, 2),
        exitoso=True,
        mensaje="HTTP 200 OK",
    )


# Lista de 6 microservicios a sondear concurrentemente
ENDPOINTS = [1, 2, 3, 4, 5, 6]
resultados_procesados: list[ResultadoSonda] = []

tiempo_inicio = time.perf_counter()

# Usar un pool acotado de 4 hilos de trabajo
with ThreadPoolExecutor(max_workers=4, thread_name_prefix="SondaPool") as executor:
    # Mapear cada tarea con su futuro correspondiente
    mapa_futuros = {executor.submit(sondear_endpoint, ep): ep for ep in ENDPOINTS}

    # Procesar resultados a medida que van terminando (as_completed)
    for futuro in as_completed(mapa_futuros):
        ep_id = mapa_futuros[futuro]
        try:
            # Obtener resultado con timeout de seguridad de 2 segundos
            res = futuro.result(timeout=2.0)
            resultados_procesados.append(res)
            print(f"[OK] Endpoint {res.endpoint_id} respondió en {res.latencia_ms} ms")
        except Exception as err:
            # Captura y aislamiento de la excepción sin quebrar el pool
            res_fallido = ResultadoSonda(
                endpoint_id=ep_id,
                latencia_ms=-1.0,
                exitoso=False,
                mensaje=f"Error: {type(err).__name__}",
            )
            resultados_procesados.append(res_fallido)
            print(f"[FALLO] Endpoint {ep_id} falló con: {err}")

duracion_total = time.perf_counter() - tiempo_inicio

# Métricas consolidadas
exitos = sum(1 for r in resultados_procesados if r.exitoso)
fallos = sum(1 for r in resultados_procesados if not r.exitoso)

print("\n--- Resumen de Monitoreo Concurrente ---")
print(f"Total sondeados   : {len(resultados_procesados)}")
print(f"Sondeos exitosos  : {exitos}")
print(f"Sondeos fallidos  : {fallos}")
print(f"Tiempo total pool : {duracion_total:.2f} s (frente a suma secuencial de latencias)")
```

Explicación de ingeniería:

- `as_completed(mapa_futuros)` devuelve un iterador que cede cada `Future` en el instante exacto en que termina, permitiendo procesar y despachar respuestas inmediatamente sin tener que esperar a que los endpoints más lentos finalicen.
- `futuro.result(timeout=2.0)` extrae el valor de retorno o reinyecta la excepción ocurrida dentro del hilo de trabajo. El bloque `try...except` aísla los fallos de un endpoint específico (como la excepción simulada en el endpoint 3), impidiendo que un error puntual colapse la totalidad del sondeo.
- Al emplear un pool acotado (`max_workers=4`), se previene la sobrecarga de conexiones y la saturación de memoria RAM, administrando la concurrencia de forma elástica y predecible.

Resultado esperado:

```text
[OK] Endpoint 2 respondió en 45.12 ms
[OK] Endpoint 1 respondió en 62.30 ms
[FALLO] Endpoint 3 falló con: Servicio remoto cerró la conexión abruptamente
[OK] Endpoint 4 respondió en 80.15 ms
[OK] Endpoint 5 respondió en 55.40 ms
[OK] Endpoint 6 respondió en 90.25 ms

--- Resumen de Monitoreo Concurrente ---
Total sondeados   : 6
Sondeos exitosos  : 5
Sondeos fallidos  : 1
Tiempo total pool : 0.15 s (frente a suma secuencial de latencias)
```

## 6. Aplicaciones en el mundo real

- **Web Scraping y Descargas Concurrentes:** recolección masiva de catálogos web, imágenes o documentos PDF a través de múltiples conexiones HTTP paralelas.
- **Microservicios y Pasarelas API (*API Gateways*):** orquestación de llamadas dispersas (*scatter-gather*) consultando simultáneamente servicios de autenticación, inventario y facturación.
- **Interfaces Gráficas de Usuario (GUI con Tkinter / PyQt):** descarga de archivos o ejecución de consultas pesadas en un hilo secundario para no congelar el hilo principal de la interfaz visual.
- **Monitoreo de Infraestructura y Redes:** sondeo concurrente de disponibilidad (*ping*, puertos TCP) sobre cientos de servidores remotos.

## 7. Uso en producción

- **Utilizar hilos exclusivamente para operaciones I/O-bound:** jamás emplear `threading` para cálculos matemáticos intensivos o algoritmos de compresión; para acelerar cómputo en CPU utilizar [multiprocesamiento](multiprocesamiento.md).
- **Dimensionar el tamaño del pool de forma racional:** para tareas I/O-bound, una regla empírica estándar es configurar `max_workers = min(32, (os.cpu_count() or 1) + 4)` o basarse en los límites de concurrencia del servicio remoto para no incurrir en bloqueos por límite de tasa (*Rate Limiting*).
- **Evitar retener cerrojos durante llamadas de red o I/O:** dentro de un bloque `with lock:` solo debe ejecutarse la actualización inmediata del estado en memoria; si se coloca una llamada de red o un `sleep` dentro del cerrojo, todos los demás hilos se bloquearán innecesariamente, destruyendo la concurrencia.
- **Establecer siempre un `timeout` en `futuro.result()`:** un servicio remoto caído puede no responder jamás; invocar `.result()` sin tiempo límite dejará al hilo bloqueado indefinidamente consumiendo memoria y descriptores.

## 8. Errores comunes y recomendaciones

1. **Usar hilos esperando acelerar cálculos matemáticos intensivos (CPU-bound).**

```python
from concurrent.futures import ThreadPoolExecutor


def calculo_pesado(n: int) -> int:
    return sum(i * i for i in range(n))


# ERROR: debido al GIL, 4 hilos tardarán LO MISMO o MÁS que 1 solo hilo
# with ThreadPoolExecutor(max_workers=4) as executor:
#     executor.map(calculo_pesado, [10_000_000] * 4)
```

Diagnóstico: el GIL fuerza a que un solo hilo ejecute bytecode a la vez. La sobrecarga de alternar entre hilos en la CPU incrementa el tiempo total. Recomendación: sustituir `ThreadPoolExecutor` por `ProcessPoolExecutor` de [multiprocesamiento](multiprocesamiento.md).

2. **Bloqueo mutuo (*Deadlock*) por adquisición de múltiples cerrojos en orden inverso.**

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()


# Hilo 1 toma A y espera B
# Hilo 2 toma B y espera A -> DEADLOCK PERMANENTE
def rutina_1():
    with lock_a:
        with lock_b:
            pass


def rutina_2():
    with lock_b:
        with lock_a:
            pass
```

Diagnóstico: si dos hilos intentan adquirir los mismos cerrojos en órdenes cruzados, el sistema se congelará permanentemente. Recomendación: establecer siempre un orden de adquisición global estricto o unificar los recursos bajo un único cerrojo.

3. **No marcar hilos de fondo como `daemon` en scripts de larga duración.**

```python
import threading


# Un hilo no daemon mantendrá vivo el proceso de Python incluso
# si la función principal main() ya terminó
# hilo = threading.Thread(target=bucle_infinito, daemon=True)  # daemon=True permite salir
```

Diagnóstico: por defecto, Python espera a que todos los hilos no daemon finalicen antes de cerrar el proceso. Recomendación: configurar `daemon=True` para tareas auxiliares de telemetría o limpieza que deban terminar cuando el programa principal se cierre.

## 9. Resumen

- La **concurrencia con hilos** permite intercalar la ejecución de múltiples tareas simultáneas, siendo altamente efectiva para operaciones limitadas por entrada/salida (**I/O-bound**).
- En CPython, el **GIL (*Global Interpreter Lock*)** previene la corrupción de memoria garantizando que solo un hilo ejecute bytecode a la vez, liberándose incondicionalmente durante operaciones de I/O o extensiones en C.
- Las **condiciones de carrera** ocurren cuando múltiples hilos modifican el estado compartido sin sincronización; se resuelven mediante cerrojos de exclusión mutua (**`threading.Lock`**).
- La clase **`concurrent.futures.ThreadPoolExecutor`** provee una interfaz declarativa de alto nivel para gestionar pools de hilos, facilitando el control de tiempos límite (*timeouts*), excepciones y recolección de resultados con **`as_completed`**.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/threading.html> — Biblioteca estándar (`threading`): especificación de hilos, cerrojos `Lock`, `RLock`, `Event` y variables de condición.
- <https://docs.python.org/3/library/concurrent.futures.html> — Biblioteca estándar (`concurrent.futures`): ejecutores de pools de hilos (`ThreadPoolExecutor`), objetos `Future` y utilidades de coordinación.
- <https://docs.python.org/3/glossary.html#term-global-interpreter-lock> — Glosario oficial de Python (*Global Interpreter Lock*): definición formal del GIL y su interacción con extensiones en C y llamadas al sistema.
- <https://peps.python.org/pep-3148/> — PEP 3148 (*futures - execute computations asynchronously*): especificación y diseño del módulo `concurrent.futures`.

