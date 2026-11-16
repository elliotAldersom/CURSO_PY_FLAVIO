# Paralelismo Real y Cómputo Intensivo (`multiprocessing` y `ProcessPoolExecutor`)

## 2. Introducción

Cuando una aplicación necesita ejecutar cálculos matemáticos masivos, procesar grandes lotes de imágenes, comprimir archivos pesados o realizar simulaciones científicas complejas, el modelo de [concurrencia basado en hilos](concurrencia_hilos.md) resulta insuficiente debido a la presencia del Bloqueo Global del Intérprete (*GIL*) en CPython, el cual restringe la ejecución de bytecode a un único núcleo de la CPU a la vez.

Para desatar el potencial de las arquitecturas multinúcleo modernas y lograr **paralelismo real**, la biblioteca estándar de Python provee el módulo **`multiprocessing`** y la abstracción de alto nivel **`concurrent.futures.ProcessPoolExecutor`**.

A diferencia de los hilos, que comparten el mismo espacio de memoria dentro de un único proceso, el multiprocesamiento genera **múltiples procesos del sistema operativo independientes**, cada uno con su propio intérprete de Python, su propio recolector de basura y su propio GIL aislado. 

Dominar el multiprocesamiento exige comprender los métodos de creación de procesos (`fork` frente a `spawn`), la cláusula de guardia obligatoria `if __name__ == '__main__':`, la serialización de datos interprocesos (*IPC*) mediante `pickle`, y la gestión coordinada de colas y piscinas de trabajo (*pools*).

## 3. Fundamentos y conceptos

**Paralelismo de procesos frente a Concurrencia de hilos.**
- **Hilos (`threading`):** múltiples flujos de control ligeros dentro de un mismo espacio de direcciones virtuales de memoria. Comparten el estado global, consumen pocos recursos, pero están limitados por el GIL a un solo núcleo de CPU en tareas de cómputo.
- **Procesos (`multiprocessing`):** instancias completamente independientes del sistema operativo con memoria aislada. Evaden el GIL al 100 % y ejecutan cálculos físicos simultáneos sobre todos los núcleos de CPU disponibles, pero conllevan un mayor consumo de memoria y requieren serialización explícita para intercambiar datos.

**Métodos de inicio de procesos: `fork`, `spawn` y `forkserver`.**
El mecanismo mediante el cual el sistema operativo da a luz a un proceso hijo varía según la plataforma:
- **`spawn` (estándar en Windows y macOS):** el proceso padre inicia un ejecutable de Python completamente nuevo desde cero. El proceso hijo importa nuevamente el módulo principal, requiriendo obligatoriamente proteger el punto de entrada con `if __name__ == '__main__':` para no entrar en un bucle recursivo infinito de creación de procesos.
- **`fork` (estándar tradicional en Linux/Unix):** el proceso hijo clona el espacio de memoria completo del padre utilizando la optimización *Copy-on-Write* (COW) del núcleo del sistema operativo. Aunque es sumamente rápido al inicio, puede provocar bloqueos mutuos (*deadlocks*) si se combina con hilos preexistentes que poseían cerrojos adquiridos al momento de clonar.
- **`forkserver`:** crea un servidor monohilo dedicado que actúa como fábrica exclusiva para clonar nuevos procesos limpios, combinando la velocidad de `fork` con la seguridad de `spawn`.

**Serialización con `pickle` y Comunicación Interprocesos (IPC).**
Debido a que cada proceso reside en su propia memoria virtual aislada, los datos transferidos entre el padre y los hijos (argumentos de entrada y valores de retorno) deben ser **serializados a bytes** mediante el módulo nativo `pickle` y transmitidos a través de canales IPC del sistema operativo (tuberías o sockets locales):
- Las funciones pasadas como objetivo (*target*) a un proceso **deben estar definidas al nivel superior del módulo** para que el proceso hijo pueda importarlas por su nombre calificado; no se admiten funciones `lambda` ni funciones anidadas dentro de otros métodos (*closures*).
- Los argumentos pasados deben ser *pickleables*: tipos nativos, listas, diccionarios, arrays de NumPy y clases regulares. Objetos que dependan de recursos del sistema operativo (como sockets abiertos, descriptores de archivos o bloqueos `threading.Lock`) no pueden transferirse directamente.

**Piscinas de procesos con `ProcessPoolExecutor`.**
La creación continua de procesos del sistema operativo impone una sobrecarga apreciable de tiempo y memoria. La clase `concurrent.futures.ProcessPoolExecutor` crea un grupo fijo de procesos de trabajo que permanecen vivos esperando tareas en una cola interna, reutilizando recursos de forma elástica y gestionando la recolección de resultados mediante objetos `Future`.

## 4. Sintaxis y funcionamiento

Estructura canónica y guardia obligatoria de proceso principal:

```python
from multiprocessing import Process
import os


def tarea_intensiva(identificador: int) -> None:
    # Código ejecutado en el proceso hijo independiente
    pid = os.getpid()
    print(f"Hijo {identificador} corriendo en PID {pid}")


if __name__ == "__main__":
    # Guardia obligatoria para evitar recursión infinita bajo el método 'spawn'
    proceso = Process(target=tarea_intensiva, args=(1,))
    proceso.start()
    proceso.join()
```

Paralelismo declarativo con `ProcessPoolExecutor`:

```python
# NO EJECUTAR (requiere archivo .py en disco para serialización IPC de ProcessPoolExecutor)
from concurrent.futures import ProcessPoolExecutor
import os


def procesar_fragmento(numero: int) -> int:
    return numero * numero


if __name__ == "__main__":
    datos = [10, 20, 30, 40]
    # Determinar automáticamente el número de trabajadores según los núcleos de CPU
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        resultados = list(executor.map(procesar_fragmento, datos))
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación de procesos con `multiprocessing.Process` y verificación de aislamiento de PID y memoria.**

```python
from multiprocessing import Process, current_process
import os
import time

# Variable global: en hilos se compartiría; en procesos se aísla por completo
acumulador_global = 0


def trabajador_conteo(nombre: str) -> None:
    global acumulador_global
    pid = os.getpid()
    print(f"[{nombre}] Iniciado en PID {pid} (acumulador local inicial: {acumulador_global})")

    # Mutación local al proceso hijo
    for _ in range(50_000):
        acumulador_global += 1

    print(f"[{nombre}] Finalizado con acumulador local: {acumulador_global}")


if __name__ == "__main__":
    pid_padre = os.getpid()
    print(f"--- Proceso Padre corriendo en PID {pid_padre} ---")

    p1 = Process(target=trabajador_conteo, args=("Proceso-A",))
    p2 = Process(target=trabajador_conteo, args=("Proceso-B",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"\n--- Verificación en Proceso Padre ---")
    print(f"PID del Padre                 : {os.getpid()}")
    print(f"Acumulador en Proceso Padre   : {acumulador_global} (esperado 0, no 100,000)")
    print("Demostración: los procesos hijos NO comparten variables globales.")
```

Explicación paso a paso:

- El proceso padre inicia en un PID específico y crea dos procesos hijos (`p1` y `p2`).
- Cada hijo recibe una copia aislada de la memoria; cuando `Proceso-A` y `Proceso-B` incrementan su `acumulador_global`, modifican exclusivamente su propia memoria física.
- Al regresar al proceso padre tras `join()`, el `acumulador_global` del padre permanece inmutable en `0`, constatando el aislamiento total de memoria y la ausencia de condiciones de carrera directas sobre variables globales.

Resultado esperado:

```text
--- Proceso Padre corriendo en PID 14210 ---
[Proceso-A] Iniciado en PID 14211 (acumulador local inicial: 0)
[Proceso-B] Iniciado en PID 14212 (acumulador local inicial: 0)
[Proceso-A] Finalizado con acumulador local: 50000
[Proceso-B] Finalizado con acumulador local: 50000

--- Verificación en Proceso Padre ---
PID del Padre                 : 14210
Acumulador en Proceso Padre   : 0 (esperado 0, no 100,000)
Demostración: los procesos hijos NO comparten variables globales.
```

### Intermedio

**Ejemplo 2 — Comunicación Interprocesos segura con `multiprocessing.Queue` (Patrón Productor-Consumidor).**

```python
from multiprocessing import Process, Queue
import time


def productor(cola: Queue, total_mensajes: int) -> None:
    """Genera datos calculados y los deposita de forma segura en la cola IPC."""
    for i in range(1, total_mensajes + 1):
        paquete = {"id": i, "valor": i * 10}
        cola.put(paquete)
        time.sleep(0.01)

    # Centinela de finalización (None indica al consumidor que no hay más datos)
    cola.put(None)
    print("[Productor] Todos los paquetes han sido emitidos.")


def consumidor(cola: Queue) -> None:
    """Consume datos de la cola IPC hasta recibir el centinela None."""
    paquetes_recibidos = []
    while True:
        item = cola.get()  # Operación bloqueante hasta que haya un elemento disponible
        if item is None:
            break
        paquetes_recibidos.append(item)

    total_calculado = sum(p["valor"] for p in paquetes_recibidos)
    print(f"[Consumidor] Recibidos {len(paquetes_recibidos)} paquetes. Suma total: {total_calculado}")


if __name__ == "__main__":
    # Cola de comunicación interprocesos sincronizada mediante tuberías y locks internos
    cola_ipc: Queue = Queue()

    proceso_prod = Process(target=productor, args=(cola_ipc, 5))
    proceso_cons = Process(target=consumidor, args=(cola_ipc,))

    proceso_prod.start()
    proceso_cons.start()

    proceso_prod.join()
    proceso_cons.join()

    print("Pipeline de comunicación interprocesos finalizado con éxito.")
```

Explicación técnica:

- `multiprocessing.Queue` es un canal de comunicación de tipo FIFO que utiliza internamente un búfer en memoria compartido mediante tuberías (*pipes*) del sistema operativo y cerrojos de sincronización.
- `cola.put(paquete)` serializa automáticamente el diccionario mediante `pickle` y lo transfiere al canal del sistema operativo; `cola.get()` deserializa el objeto en el proceso receptor.
- El envío del valor centinela `None` es el patrón canónico para notificar de forma elegante el fin del flujo sin forzar terminaciones abruptas (`terminate()`).

Resultado esperado:

```text
[Productor] Todos los paquetes han sido emitidos.
[Consumidor] Recibidos 5 paquetes. Suma total: 150
Pipeline de comunicación interprocesos finalizado con éxito.
```

### Avanzado

**Ejemplo 3 — Benchmark de aceleración real en cómputo intensivo CPU-bound: Ejecución secuencial frente a `ProcessPoolExecutor` paralelo.**

```python
# NO EJECUTAR (requiere archivo .py en disco para serialización IPC de ProcessPoolExecutor)
from concurrent.futures import ProcessPoolExecutor
import os
import time


def es_primo(n: int) -> bool:
    """Verificación determinista de primalidad intensiva en operaciones de CPU."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def contar_primos_en_rango(rango: tuple[int, int]) -> int:
    """Cuenta cuántos números primos existen en un intervalo numérico cerrado."""
    inicio, fin = rango
    conteo = 0
    for num in range(inicio, fin):
        if es_primo(num):
            conteo += 1
    return conteo


if __name__ == "__main__":
    # Dividir un dominio de búsqueda de 1,000,000 en 8 bloques de cómputo
    LIMITE_SUPERIOR = 1_000_000
    CANTIDAD_BLOQUES = 8
    tamano_bloque = LIMITE_SUPERIOR // CANTIDAD_BLOQUES

    bloques = [
        (i * tamano_bloque, (i + 1) * tamano_bloque)
        for i in range(CANTIDAD_BLOQUES)
    ]

    print(f"--- Benchmark CPU-bound: Búsqueda de primos hasta {LIMITE_SUPERIOR:,} ---")
    print(f"Núcleos de CPU detectados en el sistema: {os.cpu_count()}")

    # 1. Medición de ejecución puramente secuencial (1 solo proceso)
    t_inicio_seq = time.perf_counter()
    primos_seq = sum(contar_primos_en_rango(b) for b in bloques)
    t_seq = time.perf_counter() - t_inicio_seq

    # 2. Medición de ejecución en paralelo real con ProcessPoolExecutor
    t_inicio_par = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        # Repartir los bloques entre los núcleos físicos disponibles
        resultados_parciales = list(executor.map(contar_primos_en_rango, bloques))
        primos_par = sum(resultados_parciales)
    t_par = time.perf_counter() - t_inicio_par

    aceleracion = t_seq / t_par

    print(f"\nPrimos hallados (Secuencial) : {primos_seq:,} en {t_seq:.3f} s")
    print(f"Primos hallados (Paralelo)   : {primos_par:,} en {t_par:.3f} s")
    print(f"Factor de aceleración real   : {aceleracion:.2f}x más rápido")
    print("Consistencia de cálculo     :", primos_seq == primos_par)
```

Explicación de ingeniería:

- El cálculo de números primos es un problema netamente **CPU-bound**: cada ciclo de cómputo se dedica a evaluar operaciones aritméticas de módulo y raíz cuadrada sin ninguna espera de red o disco. En este escenario, `threading` no ofrecería ganancia alguna debido al GIL.
- `ProcessPoolExecutor` crea un proceso trabajador por cada núcleo físico de la máquina. Cada proceso recibe un bloque `(inicio, fin)` y ejecuta el cálculo en paralelo real sobre su propio núcleo sin interferencias del GIL.
- En una máquina con 4 o más núcleos, la versión paralela se completa típicamente entre 3x y 6x más rápido que la versión secuencial, logrando un aprovechamiento integral de la capacidad del procesador.

Resultado esperado:

```text
--- Benchmark CPU-bound: Búsqueda de primos hasta 1,000,000 ---
Núcleos de CPU detectados en el sistema: 8

Primos hallados (Secuencial) : 78,498 en 1.150 s
Primos hallados (Paralelo)   : 78,498 en 0.260 s
Factor de aceleración real   : 4.42x más rápido
Consistencia de cálculo     : True
```

## 6. Aplicaciones en el mundo real

- **Cómputo Científico y Simulaciones Numéricas:** cálculo paralelo de trayectorias en física computacional, modelos climáticos y simulaciones biológicas.
- **Procesamiento de Video e Imágenes en Lote:** renderizado y transcodificación de fotogramas de video o aplicación de filtros sobre bibliotecas de imágenes distribuyendo fotogramas entre procesos.
- **Entrenamiento y Ajuste de Hiperparámetros en Machine Learning:** evaluación paralela de múltiples combinaciones de modelos (*Grid Search* o *Random Search*) con Scikit-Learn (parámetro `n_jobs=-1`).
- **Indexación y Minería de Datos Masivos:** compresión, descompresión y parseo de terabytes de registros o volcados de bases de datos divididos en particiones de disco.

## 7. Uso en producción

- **Proteger SIEMPRE el punto de entrada con `if __name__ == '__main__':`:** omitir esta cláusula provocará que los procesos hijos ejecuten el código de inicialización de nuevo al arrancar bajo el método `spawn`, provocando una bifurcación descontrolada (*fork bomb*) que congelará el sistema operativo.
- **Configurar `max_workers` acorde a los núcleos reales de CPU:** para tareas CPU-bound, configurar `max_workers = os.cpu_count()` (o `cpu_count() - 1` para no congelar la máquina); asignar más procesos que núcleos de hardware disponibles no aporta rendimiento y degrada la velocidad debido a la sobrecarga del planificador del sistema operativo.
- **Minimizar el volumen de datos transferido mediante IPC:** recordar que todo argumento y retorno se serializa con `pickle`; pasar arreglos gigantes de varios gigabytes por argumentos de funciones puede saturar la memoria y el bus IPC. En tales casos, es preferible utilizar memoria compartida explícita (`multiprocessing.shared_memory`) o escribir los datos en archivos de disco mapeados en memoria (`numpy.memmap`).
- **Definir funciones objetivo a nivel de módulo:** nunca pasar funciones locales anidadas o expresiones `lambda` a ejecutores de procesos; `pickle` requiere importar la función por su ruta global en el módulo hijo.

## 8. Errores comunes y recomendaciones

1. **Olvidar la cláusula `if __name__ == '__main__':` (`RuntimeError`).**

```python
from multiprocessing import Process


def tarea():
    pass


# ERROR CRÍTICO: bajo spawn (Windows/macOS) produce RuntimeError
# p = Process(target=tarea)
# p.start()
```

Diagnóstico: el proceso hijo debe importar el archivo fuente para conocer la función `tarea`. Si el código de instanciación está libre fuera del bloque principal, el hijo volverá a lanzar nuevos procesos recursivamente hasta agotar los PIDs del sistema operativo. Recomendación: encerrar siempre el código de ejecución en `if __name__ == '__main__':`.

2. **Intentar pasar funciones `lambda` o métodos locales como target (`PicklingError`).**

```python
from multiprocessing import Process

# ERROR: AttributeError o PicklingError: Can't pickle local object
# p = Process(target=lambda: print("Hola"))
# p.start()
```

Diagnóstico: `pickle` no puede serializar el código de bytecode de funciones anónimas o locales; solo puede serializar referencias a funciones definidas a nivel global en un módulo accesible por `sys.modules`. Recomendación: declarar siempre la función con `def nombre_funcion():` en el ámbito superior del archivo.

3. **Compartir cerrojos `threading.Lock` entre procesos en lugar de `multiprocessing.Lock`.**

```python
import threading
from multiprocessing import Process

lock_invalido = threading.Lock()  # NO funciona entre procesos distintos
```

Diagnóstico: un cerrojo de `threading` vive en la memoria de un solo proceso; al ser clonado o copiado a otro proceso, se convierte en un objeto completamente independiente y desconectado, fallando en proveer sincronización. Recomendación: utilizar cerrojos específicos de procesos: `multiprocessing.Lock()`.

## 9. Resumen

- El **multiprocesamiento** provee paralelismo real en arquitecturas multinúcleo al evadir el GIL de CPython mediante la creación de procesos independientes con memoria y recolector de basura aislados.
- Es el modelo idóneo para tareas intensivas en procesamiento matemático (**CPU-bound**).
- El método de inicio **`spawn`** exige proteger rigurosamente el código de entrada con la cláusula **`if __name__ == '__main__':`** para evitar la creación recursiva descontrolada de procesos.
- La comunicación entre procesos se realiza a través de canales IPC serializados mediante **`pickle`**, requiriendo que las funciones y datos sean completamente serializables.
- La abstracción **`concurrent.futures.ProcessPoolExecutor`** automatiza la gestión de piscinas de procesos reutilizables y la recolección paralela de resultados.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/multiprocessing.html> — Biblioteca estándar (`multiprocessing`): especificación de procesos, colas `Queue`, tuberías `Pipe` y memoria compartida.
- <https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor> — Biblioteca estándar (`concurrent.futures.ProcessPoolExecutor`): interfaz declarativa para piscinas de procesos.
- <https://docs.python.org/3/library/multiprocessing.shared_memory.html> — Biblioteca estándar (`shared_memory`): asignación de bloques de memoria compartida sin serialización IPC.
- <https://docs.python.org/3/library/pickle.html> — Biblioteca estándar (`pickle`): reglas de serialización de objetos de Python entre procesos.
