# Programación Asíncrona Cooperativa con `asyncio`

## 2. Introducción

En el espectro de la computación concurrente, la gestión de operaciones limitadas por entrada/salida (*I/O-bound*) —como peticiones HTTP a microservicios, consultas a bases de datos o conexiones mediante WebSockets— enfrenta un desafío de escalabilidad con el modelo tradicional de [hilos](concurrencia_hilos.md): cada hilo del sistema operativo requiere una pila de memoria física reservada (típicamente entre 4 y 8 megabytes) y delega la conmutación de contexto en el planificador del núcleo (*kernel preemptive scheduling*). Gestionar 10 000 conexiones simultáneas con hilos saturaría la memoria RAM de un servidor convencional.

Python formalizó en **PEP 492** y **PEP 3156** el modelo de **programación asíncrona cooperativa** mediante el framework nativo **`asyncio`** y las palabras reservadas **`async`** y **`await`**.

A diferencia de los hilos, donde el sistema operativo arrebata el control de la CPU de forma imprevista (*preemptive multitasking*), en la programación asíncrona existe un único hilo de ejecución gobernado por un **bucle de eventos (*event loop*)**. Las tareas son **corrutinas colaborativas (*cooperative multitasking*)**: cuando una corrutina inicia una operación de I/O, cede voluntariamente el control mediante `await`, permitiendo que el bucle ejecute otras tareas en el mismo hilo sin sobrecarga de conmutación de hilos del sistema operativo.

## 3. Fundamentos y conceptos

**El Bucle de Eventos (*Event Loop*).**
El corazón de toda aplicación asíncrona en Python es el bucle de eventos:
- Es un despachador monohilo continuo que supervisa descriptores de sockets del sistema operativo (utilizando mecanismos de alto rendimiento en el kernel como `epoll` en Linux o `kqueue` en macOS).
- Mantiene una cola de tareas listas para ejecutar (*callbacks* y corrutinas) y las despacha secuencialmente.
- Cuando una corrutina espera un socket de red, el bucle delega la supervisión al sistema operativo y atiende de inmediato a la siguiente corrutina lista, regresando a la primera solo cuando los datos han arribado físicamente.

**Corrutinas (`async def`) y suspensión cooperativa (`await`).**
- **Función corrutina (`async def`):** al invocarse, **no ejecuta su código de inmediato**; devuelve un objeto `coroutine`.
- **Expresión `await`:** solo puede utilizarse dentro de funciones `async def`. Suspende temporalmente la ejecución de la corrutina actual y devuelve el control al bucle de eventos hasta que el objeto esperable (*awaitable*) complete su resultado.
- **Objetos esperables (*Awaitables*):** en Python, solo tres tipos de objetos pueden pasarse a `await`:
  1. **Corrutinas:** devueltas por otras funciones `async def`.
  2. **Tareas (`asyncio.Task`):** corrutinas empaquetadas y registradas activamente en el bucle de eventos para ejecución concurrente.
  3. **Futuros (`asyncio.Future`):** objetos de bajo nivel que representan un resultado pendiente que será completado en el futuro.

**Tareas Concurrentes con `asyncio.create_task` frente a `asyncio.gather`.**
- **`asyncio.create_task(coro)`:** agenda inmediatamente la corrutina en el bucle de eventos y devuelve un objeto `Task`. La tarea comienza a ejecutarse de forma concurrente en la siguiente iteración del bucle, sin requerir esperar su finalización en esa línea.
- **`asyncio.gather(*tareas)`:** coordina la ejecución concurrente de múltiples esperables y espera a que todos terminen, devolviendo una lista consolidada con sus valores de retorno en el orden exacto en que fueron suministrados.
- `return_exceptions=True`: parámetro crítico de `gather` que previene que el fallo de una tarea aborte a las demás, devolviendo la instancia de la excepción en la lista de resultados para inspección segura.

**Tabla comparativa: Hilos frente a Procesos frente a Asincronía:**

| Criterio | Hilos (`threading`) | Procesos (`multiprocessing`) | Asincronía (`asyncio`) |
| :--- | :--- | :--- | :--- |
| **Modelo de multitarea** | Preferente (*Preemptive*) | Paralelo real (*OS Processes*) | Cooperativo (*Cooperative*) |
| **Conmutación de contexto** | Gobernado por el Kernel del SO | Gobernado por el Kernel del SO | Gobernado en espacio de usuario por el bucle |
| **Consumo de memoria** | Medio (~8 MB por hilo) | Alto (memoria completa clonada) | Mínimo (~centenares de bytes por corrutina) |
| **Escenario ideal** | I/O de archivos o librerías C | Cómputo CPU intensivo | Miles de conexiones de red concurrentes (APIs, WebSockets) |
| **Limitación por GIL** | Sí (un solo hilo activo de Python) | No (múltiples GILs independientes) | Sí (opera en un único hilo) |

## 4. Sintaxis y funcionamiento

Estructura canónica de una aplicación `asyncio`:

```python
import asyncio


async def tarea_asincrona(identificador: int, retardo: float) -> str:
    # Pausa cooperativa no bloqueante
    await asyncio.sleep(retardo)
    return f"Resultado {identificador}"


async def main() -> None:
    # 1. Ejecutar corrutina individual con await directo
    resultado_uno = await tarea_asincrona(1, 0.1)

    # 2. Orquestar múltiples corrutinas concurrentes con gather
    respuestas = await asyncio.gather(
        tarea_asincrona(2, 0.2),
        tarea_asincrona(3, 0.1),
    )


# Punto de entrada principal para arrancar el Event Loop
if __name__ == "__main__":
    asyncio.run(main())
```

Creación de tareas en segundo plano (*Background Tasks*):

```python
import asyncio


async def monitoreo_fondo() -> None:
    while True:
        await asyncio.sleep(1.0)
        # Tarea periódica


async def flujo_principal() -> None:
    # Inicia la tarea en el bucle sin bloquear el avance
    tarea = asyncio.create_task(monitoreo_fondo())
    # ... otras operaciones ...
    tarea.cancel()  # Cancelar de forma controlada al finalizar
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Corrutinas elementales, suspensión no bloqueante con `asyncio.sleep` y `asyncio.run`.**

```python
import asyncio
import time


async def simular_peticion_http(url: str, duracion_espera: float) -> dict[str, str | float]:
    """Simula una consulta HTTP asíncrona no bloqueante."""
    print(f"-> [INICIO] Enviando solicitud a: {url}")
    # await asyncio.sleep cede el control del hilo cooperativamente
    await asyncio.sleep(duracion_espera)
    print(f"<- [FIN] Respuesta recibida de: {url}")
    return {"url": url, "tiempo": duracion_espera, "status": "200 OK"}


async def main() -> None:
    tiempo_inicio = time.perf_counter()

    # Ejecución secuencial deliberada para contraste
    resp_1 = await simular_peticion_http("https://api.servicio.com/usuarios", 0.15)
    resp_2 = await simular_peticion_http("https://api.servicio.com/productos", 0.10)

    duracion = time.perf_counter() - tiempo_inicio

    print("\n--- Resultados Secuenciales ---")
    print("Respuesta 1:", resp_1)
    print("Respuesta 2:", resp_2)
    print(f"Tiempo total secuencial: {duracion:.3f} s (suma de esperas ~0.25 s)")


if __name__ == "__main__":
    # asyncio.run crea un bucle de eventos nuevo, ejecuta main y cierra el bucle
    asyncio.run(main())
```

Explicación paso a paso:

- `asyncio.run(main())` inicializa el bucle de eventos, registra la corrutina `main()` y gestiona el ciclo de vida del proceso de forma limpia.
- `await simular_peticion_http(...)` suspende la ejecución hasta que la primera solicitud se resuelve, y luego prosigue con la segunda.
- La ejecución secuencial tarda la suma de las duraciones ($0.15 + 0.10 = 0.25$ segundos), sirviendo como base comparativa para la concurrencia.

Resultado esperado:

```text
-> [INICIO] Enviando solicitud a: https://api.servicio.com/usuarios
<- [FIN] Respuesta recibida de: https://api.servicio.com/usuarios
-> [INICIO] Enviando solicitud a: https://api.servicio.com/productos
<- [FIN] Respuesta recibida de: https://api.servicio.com/productos

--- Resultados Secuenciales ---
Respuesta 1: {'url': 'https://api.servicio.com/usuarios', 'tiempo': 0.15, 'status': '200 OK'}
Respuesta 2: {'url': 'https://api.servicio.com/productos', 'tiempo': 0.1, 'status': '200 OK'}
Tiempo total secuencial: 0.250 s (suma de esperas ~0.25 s)
```

### Intermedio

**Ejemplo 2 — Orquestación concurrente masiva con `asyncio.gather`, tolerancia a fallos con `return_exceptions=True` y timeouts con `asyncio.wait_for`.**

```python
import asyncio
import time


async def consultar_microservicio(servicio_id: int, latencia: float) -> str:
    """Simula una consulta de red con posible timeout o error de servidor."""
    if servicio_id == 4:
        # Simular un microservicio que falla con excepción
        await asyncio.sleep(0.05)
        raise ConnectionRefusedError("Servicio de facturación no disponible")

    await asyncio.sleep(latencia)
    return f"Servicio {servicio_id} OK"


async def main() -> None:
    print("--- Orquestación Concurrente con asyncio.gather ---")
    tiempo_inicio = time.perf_counter()

    # Definir 4 consultas concurrentes con latencias dispares
    coros = [
        consultar_microservicio(1, 0.20),
        consultar_microservicio(2, 0.05),
        consultar_microservicio(3, 0.15),
        consultar_microservicio(4, 0.05),  # Fallará con excepción
    ]

    # return_exceptions=True asegura que una excepción no cancele las demás tareas
    resultados = await asyncio.gather(*coros, return_exceptions=True)

    duracion = time.perf_counter() - tiempo_inicio

    print(f"Tiempo total concurrente: {duracion:.3f} s (gobernado por el más lento: ~0.20 s)")
    print("\nResultados recolectados:")
    for idx, res in enumerate(resultados, start=1):
        if isinstance(res, Exception):
            print(f"  Consulta {idx}: FALLIDA -> {type(res).__name__}: {res}")
        else:
            print(f"  Consulta {idx}: EXITOSA -> {res}")

    # Demostración de Timeout de seguridad con asyncio.wait_for
    print("\n--- Demostración de Timeout ---")
    try:
        # El servicio tarda 0.5s pero el timeout es 0.1s
        await asyncio.wait_for(consultar_microservicio(5, 0.50), timeout=0.10)
    except TimeoutError:
        print("Timeout disparado con éxito: la tarea tardó más de 100 ms y fue abortada.")


if __name__ == "__main__":
    asyncio.run(main())
```

Explicación técnica:

- `asyncio.gather(*coros)` arranca las cuatro corrutinas de manera simultánea en el bucle de eventos. La duración total del bloque es de 0.20 segundos (la latencia de la tarea más lenta), reduciendo el tiempo a una fracción de la suma secuencial.
- Al activar `return_exceptions=True`, la excepción `ConnectionRefusedError` del servicio 4 no interrumpe el flujo: se almacena como elemento en la lista de resultados para que el código llamador pueda auditarla y aplicar degradación elegante.
- `asyncio.wait_for(coro, timeout)` cancela automáticamente la corrutina si no completa su ejecución dentro del umbral estipulado, lanzando `TimeoutError` para proteger la respuesta al usuario final.

Resultado esperado:

```text
--- Orquestación Concurrente con asyncio.gather ---
Tiempo total concurrente: 0.200 s (gobernado por el más lento: ~0.20 s)

Resultados recolectados:
  Consulta 1: EXITOSA -> Servicio 1 OK
  Consulta 2: EXITOSA -> Servicio 2 OK
  Consulta 3: EXITOSA -> Servicio 3 OK
  Consulta 4: FALLIDA -> ConnectionRefusedError: Servicio de facturación no disponible

--- Demostración de Timeout ---
Timeout disparado con éxito: la tarea tardó más de 100 ms y fue abortada.
```

### Avanzado

**Ejemplo 3 — Sistema de Colas Asíncronas (`asyncio.Queue`) con Productores y Consumidores concurrentes y cancelación limpia de tareas (`asyncio.CancelledError`).**

```python
import asyncio
import random


async def productor(cola: asyncio.Queue[str], id_productor: int, total_items: int) -> None:
    """Genera eventos y los encola asíncronamente."""
    for i in range(1, total_items + 1):
        item = f"Evento-{id_productor}-{i}"
        await cola.put(item)  # Si la cola estuviese llena, cede el control cooperativamente
        await asyncio.sleep(0.02)
    print(f"[Productor {id_productor}] Emisión completada.")


async def consumidor(cola: asyncio.Queue[str], id_consumidor: int) -> None:
    """Consume eventos de la cola indefinidamente hasta ser cancelado."""
    try:
        while True:
            item = await cola.get()  # Espera asíncrona no bloqueante
            print(f"   [Consumidor {id_consumidor}] Procesado: {item}")
            await asyncio.sleep(0.04)  # Simula tiempo de procesamiento de base de datos
            cola.task_done()  # Notifica que la tarea del ítem terminó
    except asyncio.CancelledError:
        # Gancho de limpieza determinista ante cancelación de la tarea
        print(f"   [Consumidor {id_consumidor}] Señal de cancelación recibida. Cerrando recursos...")
        raise  # Re-lanzar para confirmar la cancelación al bucle


async def main() -> None:
    # Cola acotada a máximo 5 elementos para aplicar backpressure
    cola_eventos: asyncio.Queue[str] = asyncio.Queue(maxsize=5)

    # 1. Crear 2 consumidores concurrentes en segundo plano
    tareas_consumidores = [
        asyncio.create_task(consumidor(cola_eventos, 1)),
        asyncio.create_task(consumidor(cola_eventos, 2)),
    ]

    # 2. Ejecutar 2 productores que emitirán 3 eventos cada uno
    await asyncio.gather(
        productor(cola_eventos, 10, 3),
        productor(cola_eventos, 20, 3),
    )

    # 3. Esperar a que todos los elementos encolados sean procesados (task_done)
    await cola_eventos.join()
    print("\nTodos los eventos encolados han sido procesados satisfactoriamente.")

    # 4. Cancelar limpiamente las tareas de los consumidores que están en bucle infinito
    for t in tareas_consumidores:
        t.cancel()

    # Esperar confirmación de cancelación
    await asyncio.gather(*tareas_consumidores, return_exceptions=True)
    print("Pipeline asíncrono cerrado de forma determinista.")


if __name__ == "__main__":
    asyncio.run(main())
```

Explicación de ingeniería:

- `asyncio.Queue` permite desacoplar los ritmos de generación y consumo de eventos. Al fijar `maxsize=5`, la cola implementa **contrapresión (*backpressure*)**: si los consumidores son más lentos que los productores, `await cola.put()` suspende automáticamente a los productores hasta que haya espacio disponible, impidiendo desbordamientos de memoria RAM.
- `await cola_eventos.join()` bloquea la corrutina `main` hasta que cada elemento encolado haya recibido su correspondiente llamada `cola.task_done()`.
- La cancelación con `t.cancel()` inyecta una excepción `asyncio.CancelledError` dentro de la corrutina en su siguiente punto de suspensión `await`. El bloque `try...except asyncio.CancelledError` permite cerrar conexiones de red o archivos de forma ordenada antes de finalizar.

Resultado esperado:

```text
   [Consumidor 1] Procesado: Evento-10-1
   [Consumidor 2] Procesado: Evento-20-1
   [Consumidor 1] Procesado: Evento-10-2
   [Consumidor 2] Procesado: Evento-20-2
[Productor 10] Emisión completada.
[Productor 20] Emisión completada.
   [Consumidor 1] Procesado: Evento-10-3
   [Consumidor 2] Procesado: Evento-20-3

Todos los eventos encolados han sido procesados satisfactoriamente.
   [Consumidor 1] Señal de cancelación recibida. Cerrando recursos...
   [Consumidor 2] Señal de cancelación recibida. Cerrando recursos...
Pipeline asíncrono cerrado de forma determinista.
```

## 6. Aplicaciones en el mundo real

- **Frameworks web modernos de alto rendimiento:** motores HTTP asíncronos como FastAPI, Starlette, Sanic y Aiohttp capaces de despachar decenas de miles de solicitudes por segundo en un único proceso.
- **Servidores de Chat y Streaming en Tiempo Real:** gestión masiva de conexiones persistentes mediante WebSockets o gRPC bidireccional.
- **Clientes de Bases de Datos Asíncronas:** consultas no bloqueantes con drivers como `asyncpg` (PostgreSQL), `motor` (MongoDB) o `redis-py` asíncrono.
- **Bots de Mensajería y Redes Sociales:** automatización con bibliotecas como `discord.py` o `python-telegram-bot` escuchando miles de canales concurrentemente.

## 7. Uso en producción

- **NUNCA ejecutar código bloqueante síncrono dentro del bucle de eventos:** invocar `time.sleep()`, operaciones pesadas de CPU o llamadas síncronas (`requests.get()`) congela por completo el hilo del bucle de eventos, bloqueando todas las demás corrutinas activas. Para operaciones de CPU o bibliotecas síncronas legadas, delegar su ejecución a un pool externo mediante `asyncio.to_thread(funcion_bloqueante)` o `loop.run_in_executor()`.
- **Proteger tareas de fondo contra recolección de basura prematura:** si se crea una tarea con `asyncio.create_task()`, conservar siempre una referencia fuerte a la tarea en un conjunto `set` global hasta que termine; de lo contrario, el recolector de basura de Python puede destruir la tarea a mitad de ejecución.
- **Controlar la concurrencia con semáforos (`asyncio.Semaphore`):** enviar 5000 solicitudes HTTP simultáneas con `gather` agotará los sockets del sistema operativo y provocará bloqueos por límite de tasa en el servidor destino. Envolver las llamadas en un `async with asyncio.Semaphore(50):` para acotar la concurrencia a un máximo de 50 peticiones en vuelo.
- **Gestionar la cancelación limpia de tareas:** capturar siempre `asyncio.CancelledError` en corrutinas de larga duración para liberar recursos y confirmar la salida sin dejar procesos zombis en el bucle.

## 8. Errores comunes y recomendaciones

1. **Olvidar la palabra reservada `await` al invocar una función corrutina.**

```python
async def obtener_datos():
    return "datos"


async def main():
    # ERROR: sin await, resultado es un objeto <coroutine>, no la cadena
    resultado = obtener_datos()
    # Emite RuntimeWarning: coroutine 'obtener_datos' was never awaited
```

Diagnóstico: una función declarada con `async def` devuelve un objeto corrutina al ser llamada; si no se antepone `await`, la corrutina nunca se programa en el bucle y su código jamás se ejecuta. Recomendación: anteponer siempre `await` a toda llamada asíncrona: `resultado = await obtener_datos()`.

2. **Utilizar `time.sleep` en lugar de `asyncio.sleep`.**

```python
import asyncio
import time


async def tarea_rota():
    time.sleep(5)  # ERROR CRÍTICO: bloquea TODO el hilo y congela el bucle
    # Corrección:
    # await asyncio.sleep(5)
```

Diagnóstico: `time.sleep()` suspende el hilo del sistema operativo por completo; al no ceder el control al bucle de eventos, ninguna otra corrutina del programa podrá avanzar durante esos 5 segundos. Recomendación: en código asíncrono, utilizar taxativamente `await asyncio.sleep()`.

3. **Lanzar corrutinas con bucles síncronos convencionales.**

```python
# ANTIPATRÓN: no hay concurrencia, se ejecutan en serie
# for url in urls:
#     await descargar(url)

# CORRECCIÓN: ejecutar concurrentemente
# await asyncio.gather(*(descargar(url) for url in urls))
```

Diagnóstico: iterar con un bucle `for` convencional y hacer `await` dentro de cada ciclo fuerza la ejecución estrictamente secuencial de las tareas. Recomendación: orquestar las corrutinas mediante `asyncio.gather` o `asyncio.TaskGroup` (Python 3.11+).

## 9. Resumen

- **`asyncio`** implementa el modelo de multitarea cooperativa basado en un **bucle de eventos (*event loop*)** monohilo, optimizado para operaciones masivas de entrada y salida (**I/O-bound**).
- Las funciones declaradas con **`async def`** producen corrutinas cuyo avance se suspende y reanuda voluntariamente mediante la sentencia **`await`**.
- La función **`asyncio.gather`** permite orquestar múltiples corrutinas simultáneamente, gestionando tiempos límite (*timeouts*) y tolerancia a fallos mediante `return_exceptions=True`.
- **`asyncio.create_task`** registra corrutinas en el bucle para su ejecución en segundo plano, permitiendo cancelaciones limpias mediante `asyncio.CancelledError`.
- **`asyncio.Queue`** provee canales seguros de contrapresión (*backpressure*) para arquitecturas de productores y consumidores asíncronos.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/asyncio.html> — Biblioteca estándar (`asyncio`): corrutinas, bucle de eventos, tareas, colas y sincronización.
- <https://docs.python.org/3/library/concurrent.futures.html> — Biblioteca estándar (`concurrent.futures`): ejecutores e interoperabilidad entre bucle de eventos y pools de hilos/procesos.
- <https://peps.python.org/pep-0492/> — PEP 492 (*Coroutines with async and await syntax*): diseño e introducción de la sintaxis formal de asincronía en Python.
- <https://peps.python.org/pep-3156/> — PEP 3156 (*Asynchronous IO Support Rebooted: the "asyncio" Module*): arquitectura original del bucle de eventos de Python.
