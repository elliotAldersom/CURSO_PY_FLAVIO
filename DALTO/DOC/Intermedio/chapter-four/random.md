# Generación Pseudoaleatoria, Muestreo Reproducible y Seguridad Criptográfica (`random` y `secrets`)

## 2. Introducción

Numerosos problemas computacionales requieren introducir variabilidad controlada o seleccionar elementos al azar: mecánicas de videojuegos y sorteos (`numero_secreto.py` L22, `Juego.py` L537), simulaciones numéricas de Monte Carlo, partición de conjuntos de datos para entrenamiento y validación estadística, o pruebas automatizadas con entradas sintéticas.

La **biblioteca estándar de Python** aborda la aleatoriedad mediante dos [módulos](../chapter-three/modulos.md) separados con garantías radicalmente distintas:

1. **`random`:** implementa un **generador de números pseudoaleatorios** (*PRNG*, *Pseudorandom Number Generator*) rápido, determinista y completamente reproducible a partir de una semilla (*seed*), diseñado para modelado estadístico, simulaciones, juegos y muestreo de colecciones.
2. **`secrets` (introducido en Python 3.6 mediante PEP 506):** provee un **generador pseudoaleatorio criptográficamente seguro** (*CSPRNG*) respaldado por la fuente de entropía física del sistema operativo (`os.urandom`), indispensable para contraseñas, tokens de sesión, enlaces de recuperación y códigos de verificación.

Comprender cómo funcionan las semillas, las instancias aisladas `random.Random`, las diferencias entre muestreo con y sin reemplazo, y **por qué jamás debe emplearse `random` para generar credenciales de seguridad** (corrigiendo el ejercicio de `Importando_Random.py` L35-78) constituye una competencia esencial de ingeniería de software.

## 3. Fundamentos y conceptos

**Algoritmo Mersenne Twister (MT19937) y determinismo pseudoaleatorio.** El módulo estándar `random` no produce azar físico verdadero: utiliza por defecto el algoritmo determinista **Mersenne Twister**, con un período astronómico de $2^{19937} - 1$ y equidistribución en 623 dimensiones, implementado en C para máxima velocidad:

- Al importarse o iniciarse sin semilla explícita, Python inicializa el estado interno utilizando entropía del sistema operativo (o la marca temporal actual si aquella no estuviese disponible), produciendo secuencias distintas en cada ejecución.
- Si se fija una semilla conocida (`int`, `str`, `bytes`), la secuencia matemática completa queda unívocamente determinada: dos ejecuciones en cualquier sistema operativo con la misma versión del algoritmo y la misma semilla producirán **exactamente los mismos resultados en idéntico orden**.

**`random.seed(...)` global frente a instancias aisladas `random.Random(semilla)`.** Las funciones de nivel de módulo (`random.randint`, `random.choice`, `random.shuffle`) son en realidad métodos enlazados a una **única instancia global oculta** compartida por todo el proceso:

- Llamar a `random.seed(42)` reinicia ese generador global compartido, lo que puede afectar inadvertidamente a otras bibliotecas o verse alterado si otro hilo consume números entre dos llamadas propias.
- Instanciar `rng = random.Random(42)` crea un generador independiente con su propio estado interno aislado (`rng.randint(...)`, `rng.sample(...)`), garantizando reproducibilidad estricta en pruebas unitarias, simulaciones científicas y componentes concurrentes sin interferencia global.

**Generación numérica discreta y continua: intervalos cerrados frente a semiabiertos.** Una fuente frecuente de errores de borde (*off-by-one*) radica en los extremos de las funciones enteras, contrastadas en `Importando_Random.py` (L5, L94-108):

- `randrange(stop)` o `randrange(start, stop[, step])`: sigue la misma convención **semiabierta** $[\text{start}, \text{stop})$ que `range()`. Así, `random.randrange(1, 100)` (`Importando_Random.py` L5) devuelve enteros entre `1` y `99` (**excluye el `100`**), y `random.randrange(0, 100, 2)` (L13) devuelve pares entre `0` y `98`.
- `randint(a, b)`: es un caso excepcional en Python donde el intervalo es **cerrado en ambos extremos** $[a, b]$, equivaliendo internamente a `randrange(a, b + 1)`. Por tanto, `randint(1, 4)` (`Importando_Random.py` L103) sí puede devolver `1`, `2`, `3` o `4`.
- `random()`: función base del generador; devuelve un `float` distribuido uniformemente en el intervalo semiabierto $[0.0, 1.0)$.
- `uniform(a, b)`: devuelve un `float` distribuido uniformemente entre `a` y `b` ($a + (b - a) \cdot \text{random}()$). El módulo incluye además distribuciones estadísticas continuas como `gauss(mu, sigma)` (normal), `expovariate(lambd)` y `triangular(low, high, mode)`.

**Operaciones sobre secuencias: `choice`, `choices` (con reemplazo), `sample` (sin reemplazo) y `shuffle`.** Al operar sobre colecciones ([listas](../../Basico/chapter-two/listas.md), [tuplas](../chapter-one/tuplas.md), [cadenas](../../Basico/chapter-two/cadenas.md)), cada función responde a un modelo combinatorio específico:

- `choice(seq)`: extrae un único elemento al azar de una secuencia no vacía (`Importando_Random.py` L19, y forma idiomática para sustituir el par `id_azar = random.randrange(num)` + `lista_guerrero[id_azar]` de `Juego.py` L537-538). Requiere que `seq` soporte indexación por posición (`__getitem__` y `__len__`); esto responde con precisión la duda anotada en `Importando_Random.py` (L16): pasar un [conjunto](../chapter-one/conjuntos.md) `set` lanza `TypeError: 'set' object is not subscriptable`, y pasar una secuencia vacía lanza `IndexError`.
- `choices(population, weights=None, *, cum_weights=None, k=1)`: realiza $k$ extracciones independientes **con reemplazo** (un mismo elemento puede repetirse varias veces en la lista resultante, incluso con $k > \text{len}(\text{population})$). Admite pesos proporcionales `weights` (`Importando_Random.py` L139-156) o pesos acumulados `cum_weights` (que aceleran búsquedas repetidas de $O(n)$ a $O(\log n)$ mediante bisección).
- `sample(population, k, *, counts=None)`: selecciona una lista de $k$ elementos distintos **sin reemplazo** (`Importando_Random.py` L29, L167), sin modificar la colección original. Exige $0 \le k \le \text{len}(\text{population})$; si $k$ supera el tamaño de la población o es negativo, lanza `ValueError` ([excepciones](excepciones.md)). Tampoco acepta conjuntos `set` directamente (desde Python 3.9 está desaconsejado y en Python 3.11+ lanza `TypeError`), debiendo convertirse explícitamente a `tuple(conjunto)` o `list(conjunto)`.
- `shuffle(x)`: permuta los elementos de una secuencia **mutable** (`list`) directamente **en el lugar (*in-place*)** mediante el algoritmo de Fisher-Yates y **retorna `None`**. Tal como observa acertadamente `Importando_Random.py` (L71-88), no puede aplicarse sobre un `str` ni una `tuple` por ser inmutables; cuando se desea obtener una nueva lista mezclada sin alterar el original (o a partir de una tupla/cadena), se utiliza `random.sample(secuencia, k=len(secuencia))`.

**Advertencia crítica de seguridad: por qué `random` nunca debe usarse para contraseñas (`secrets`, PEP 506).** En `Importando_Random.py` (L35-78) se construye un generador de contraseñas combinando `random.sample` y `random.shuffle`. Aunque útil como ejercicio sintáctico de listas y `.join()`, en un sistema real constituye una **vulnerabilidad grave de seguridad**:

- El estado completo de Mersenne Twister consta únicamente de 624 enteros de 32 bits. Si un atacante observa suficientes salidas generadas por la aplicación (por ejemplo, identificadores de sorteo, códigos públicos o marcas temporales de reinicio), puede invertir algebraicamente la función de *tempering*, reconstruir el estado interno exacto y **predecir el 100 % de las contraseñas o tokens pasados y futuros**.
- La documentación oficial de Python advierte explícitamente contra el uso de `random` con fines de seguridad y estandariza en **PEP 506** el módulo estándar `secrets`, basado en `secrets.SystemRandom` (que delega cada byte aleatorio al generador criptográfico del núcleo del sistema operativo: `getrandom()` en Linux, `BCryptGenRandom` en Windows):
  - `secrets.choice(alfabeto)` para construir contraseñas o códigos OTP carácter a carácter.
  - `secrets.token_hex(nbytes)` y `secrets.token_urlsafe(nbytes)` para tokens de sesión, llaves API o enlaces de restablecimiento de contraseña.
  - `secrets.compare_digest(a, b)` para comparar secretos en tiempo constante previniendo ataques de temporización (*timing attacks*).

## 4. Sintaxis y funcionamiento

Patrón dual recomendado (instancia aislada `random.Random` para simulaciones reproducibles; `secrets` para seguridad):

```text
import random
import secrets

# 1. Simulación estadística o juego reproducible y aislado
rng = random.Random(<semilla_entera>)
muestra = rng.sample(<secuencia>, k=<cantidad>)

# 2. Credenciales, tokens o códigos de seguridad (no predecibles)
token = secrets.token_urlsafe(32)
```

Referencia de clases y funciones de `random` y `secrets`:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `random.Random(seed)` | Instancia PRNG aislada e independiente del estado global | `rng = random.Random(42)` |
| 2 | `rng.randint(a, b)` | Entero uniforme en el intervalo **cerrado** $[a, b]$ (incluye `b`) | `dado = rng.randint(1, 6)` |
| 3 | `rng.randrange(ini, fin, paso)` | Entero en el intervalo **semiabierto** $[\text{ini}, \text{fin})$ | `par = rng.randrange(0, 100, 2)` |
| 4 | `rng.random()` | `float` uniforme en $[0.0, 1.0)$ | `p = rng.random()` |
| 5 | `rng.uniform(a, b)` | `float` uniforme continuo entre `a` y `b` | `x = rng.uniform(1.0, 10.0)` |
| 6 | `rng.choice(seq)` | Devuelve 1 elemento aleatorio de una secuencia no vacía | `rng.choice(concursantes)` |
| 7 | `rng.choices(pob, weights, k)` | Lista de `k` elementos **con reemplazo** y pesos opcionales | `rng.choices(items, weights=[8, 2], k=5)` |
| 8 | `rng.sample(pob, k)` | Lista nueva de `k` elementos únicos **sin reemplazo** | `rng.sample(concursantes, k=3)` |
| 9 | `rng.shuffle(lista)` | Mezcla `lista` mutable *in-place* y devuelve `None` | `rng.shuffle(mazo)` |
| 10 | `secrets.choice` / `token_urlsafe` | Selección y tokens **criptográficamente seguros** (**PEP 506**) | `secrets.token_urlsafe(32)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Reproducibilidad determinista con `random.Random(semilla)` y diferencia exacta entre `randint` y `randrange`.**

```python
import random

rng_a = random.Random(7)
rng_b = random.Random(7)

enteros_cerrados = [rng_a.randint(1, 4) for _ in range(8)]
enteros_semiabiertos = [rng_a.randrange(1, 4) for _ in range(8)]
pares = [rng_a.randrange(0, 20, 2) for _ in range(5)]
unitario = round(rng_a.random(), 4)
continuo = round(rng_a.uniform(1.0, 10.0), 4)

# Una segunda instancia con la misma semilla reproduce idéntica secuencia inicial
replica_cerrados = [rng_b.randint(1, 4) for _ in range(8)]

print("randint(1, 4) [incluye 4]   :", enteros_cerrados)
print("randrange(1, 4) [excluye 4] :", enteros_semiabiertos)
print("randrange(0, 20, 2) [pares] :", pares)
print("random() en [0.0, 1.0)      :", unitario)
print("uniform(1.0, 10.0)          :", continuo)
print("Reproducibilidad verificada :", enteros_cerrados == replica_cerrados)
```

Explicación paso a paso:

- Al instanciar `random.Random(7)` la salida deja de variar al azar entre corridas y se vuelve 100 % reproducible (`enteros_cerrados == replica_cerrados` es `True`).
- Se comprueba visualmente la diferencia documentada en `Importando_Random.py` (L94-108): `randint(1, 4)` incluye el extremo superior `4` (`[3, 2, 4, ...]`), mientras que `randrange(1, 4)` jamás alcanza el `4`, tomando valores únicamente en `{1, 2, 3}`.

Resultado esperado:

```text
randint(1, 4) [incluye 4]   : [3, 2, 4, 1, 1, 1, 3, 1]
randrange(1, 4) [excluye 4] : [3, 1, 1, 1, 2, 2, 1, 1]
randrange(0, 20, 2) [pares] : [2, 16, 12, 0, 18]
random() en [0.0, 1.0)      : 0.1238
uniform(1.0, 10.0)          : 3.0092
Reproducibilidad verificada : True
```

### Intermedio

**Ejemplo 2 — Selección sobre colecciones: `choice`, muestreo sin reemplazo (`sample`), muestreo ponderado con reemplazo (`choices`) y permutación `shuffle`.**

```python
import random

rng = random.Random(10)
concursantes = ["Juan", "Pedro", "Luis", "Carlos"]

ganador_unico = rng.choice(concursantes)
podio_sin_repeticion = rng.sample(concursantes, k=3)
botin_ponderado = rng.choices(
    ["comun", "raro", "legendario"],
    weights=[60, 30, 10],
    k=6,
)

orden_turnos = concursantes.copy()
retorno_shuffle = rng.shuffle(orden_turnos)

print("choice (1 elemento)          :", ganador_unico)
print("sample k=3 (sin reemplazo)   :", podio_sin_repeticion)
print("choices k=6 (con reemplazo)  :", botin_ponderado)
print("shuffle in-place (sobre copia):", orden_turnos)
print("Retorno de shuffle()         :", retorno_shuffle)
```

Explicación técnica:

- `rng.choice(concursantes)` reemplaza de manera directa y legible la indexación manual `concursantes[random.randrange(len(concursantes))]` empleada en `Juego.py` (L537-538).
- `rng.sample(concursantes, k=3)` garantiza tres ganadores distintos sin alterar `concursantes`, mientras que `rng.choices(..., weights=[60, 30, 10], k=6)` permite extraer 6 recompensas de una lista de solo 3 categorías respetando sus probabilidades relativas ($60\,\%, 30\,\%, 10\,\%$).
- Antes de invocar `rng.shuffle`, se copia la lista (`concursantes.copy()`) para no mutar la colección original y se constata que el método devuelve `None`.

Resultado esperado:

```text
choice (1 elemento)          : Juan
sample k=3 (sin reemplazo)   : ['Carlos', 'Pedro', 'Juan']
choices k=6 (con reemplazo)  : ['comun', 'raro', 'raro', 'raro', 'comun', 'comun']
shuffle in-place (sobre copia): ['Pedro', 'Carlos', 'Juan', 'Luis']
Retorno de shuffle()         : None
```

### Avanzado

**Ejemplo 3 — Simulación Monte Carlo reproducible con `random.Random` frente a generación criptográfica de credenciales con `secrets` (PEP 506).**

```python
import random
import secrets
import string


def estimar_pi_monte_carlo(muestras: int, semilla: int = 2025) -> float:
    rng = random.Random(semilla)
    dentro_circulo = 0
    for _ in range(muestras):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            dentro_circulo += 1
    return 4.0 * dentro_circulo / muestras


def generar_contrasena_segura(longitud: int = 16) -> str:
    if longitud < 12:
        raise ValueError("La longitud mínima recomendada es de 12 caracteres")
    simbolos = "!@#$%^&*_-+="
    alfabeto = string.ascii_letters + string.digits + simbolos
    while True:
        candidata = "".join(secrets.choice(alfabeto) for _ in range(longitud))
        if (
            any(c.islower() for c in candidata)
            and any(c.isupper() for c in candidata)
            and any(c.isdigit() for c in candidata)
            and any(c in simbolos for c in candidata)
        ):
            return candidata


pi_aprox = estimar_pi_monte_carlo(muestras=50_000, semilla=2025)
contrasena = generar_contrasena_segura(longitud=16)
token_url = secrets.token_urlsafe(32)

print(f"Estimación reproducible de pi : {pi_aprox:.4f}")
print("Longitud de contraseña CSPRNG :", len(contrasena))
print(
    "Cumple política de complejidad:",
    any(c.islower() for c in contrasena)
    and any(c.isupper() for c in contrasena)
    and any(c.isdigit() for c in contrasena),
)
print("Token URL-safe (>= 40 caract.):", len(token_url) >= 40)
```

Explicación de ingeniería y seguridad:

- La función `estimar_pi_monte_carlo` lanza $50\,000$ puntos uniformes en el cuadrado unitario $[0, 1]^2$; la proporción que cae dentro del cuarto de círculo $x^2 + y^2 \le 1$ tiende a $\frac{\pi}{4}$. Aquí el determinismo de `random.Random(2025)` es una **virtud científica**, pues cualquier investigador obtiene exactamente `3.1414` al auditar el experimento.
- En sentido opuesto, `generar_contrasena_segura` corrige el enfoque de `Importando_Random.py` (L35-78) empleando `secrets.choice` sobre el CSPRNG del sistema operativo: ningún observador externo puede deducir la clave ni el `token_urlsafe(32)` a partir de salidas previas.

Resultado esperado:

```text
Estimación reproducible de pi : 3.1414
Longitud de contraseña CSPRNG : 16
Cumple política de complejidad: True
Token URL-safe (>= 40 caract.): True
```

## 6. Aplicaciones en el mundo real

- **Ciencia de datos y aprendizaje automático:** partición reproducible de conjuntos de datos en entrenamiento y prueba (*train/test split*), barajado por épocas y submuestreo estratificado fijando una semilla explícita de experimento.
- **Simulación financiera, logística e investigación operativa (*Monte Carlo*):** modelado de colas de espera, tiempos entre llegadas (`expovariate`), escenarios de riesgo y pruebas de carga con tráfico sintético.
- **Pruebas basadas en propiedades (*Property-Based Testing* / *Fuzzing*):** generar miles de combinaciones aleatorias de entradas válidas y de borde conservando la semilla que disparó un fallo para reproducirlo determinísticamente en integración continua.
- **Videojuegos y sistemas de recompensas (*loot tables*):** selección de eventos o ítems según tablas de rareza ponderadas con `choices(..., cum_weights=...)`.
- **Seguridad y autenticación (exclusivamente con `secrets`):** emisión de códigos OTP, identificadores de sesión, *salts* criptográficos, claves API y enlaces de restablecimiento de credenciales.

## 7. Uso en producción

- **Separación taxativa entre `random` y `secrets`:** auditar mediante herramientas de análisis estático (como Ruff/Bandit, regla `S311`) que ninguna ruta vinculada a autenticación, autorización, criptografía o tokens invoque funciones del módulo `random`.
- **Evitar mutar el generador global en bibliotecas reutilizables:** un paquete o servicio nunca debe llamar a `random.seed(...)` a nivel global porque alteraría silenciosamente el comportamiento de otros módulos del consumidor; debe recibir o construir su propia instancia `random.Random(semilla)`.
- **Registrar la semilla en ejecuciones de pruebas y experimentos:** cuando una suite de tests aleatoriza el orden de ejecución o genera datos dinámicos, imprimir la semilla utilizada en los registros de CI permite reproducir cualquier fallo intermitente (*flaky test*) pasando esa misma semilla en local.
- **Colocar las importaciones en el encabezado del módulo (**PEP 8**):** en `Juego.py` (L516) se ejecuta `import random` dentro de una rama `elif` de un bucle interactivo; aunque Python cachea el módulo en `sys.modules`, ubicar `import random` al inicio del archivo explicita las dependencias del módulo y evita sobrecarga innecesaria en bucles frecuentes.

## 8. Errores comunes y recomendaciones

1. **Asignar el valor de retorno de `random.shuffle(lista)` perdiendo la lista (`None`).**

```python
import random

cartas = ["A", "K", "Q", "J"]
mal_asignado = random.Random(7).shuffle(cartas)

print("Valor asignado por error:", mal_asignado)
print("Lista original mutada   :", cartas)
```

Resultado esperado:

```text
Valor asignado por error: None
Lista original mutada   : ['J', 'K', 'A', 'Q']
```

Diagnóstico: igual que `list.sort()`, `shuffle()` opera *in-place* y retorna `None`. Si se escribe `cartas = random.shuffle(cartas)`, la variable pasa a valer `None`. Recomendación: llamar a `rng.shuffle(cartas)` sin reasignar, o usar `barajadas = rng.sample(cartas, k=len(cartas))` si se requiere conservar intacta la secuencia original.

2. **Pasar un conjunto `set` a `random.choice()` (`TypeError`) o pedir en `sample()` más elementos de los disponibles (`ValueError`).**

```python
# ERROR INTENCIONAL: TypeError porque un objeto set no admite indexación por posición en choice()
import random

conjunto_ids = {101, 102, 103}
elegido = random.choice(conjunto_ids)
```

Diagnóstico: `random.choice` calcula un índice entero aleatorio `i` y evalúa `seq[i]`; como un `set` carece de orden posicional e indexación (`Importando_Random.py` L16), lanza `TypeError: 'set' object is not subscriptable`. Solución: convertir previamente a tupla o lista ordenada (`rng.choice(tuple(conjunto_ids))`). Análogamente, si se necesitan repeticiones cuando $k > \text{len}(\text{poblacion})$, debe usarse `choices(..., k=...)` en lugar de `sample(..., k=...)`.

3. **Reinicializar `seed()` con una constante dentro de un bucle o función llamada repetidamente.**

```python
import random

secuencia_defectuosa = []
for _ in range(4):
    random.seed(100)
    secuencia_defectuosa.append(random.randint(1, 100))

rng_correcto = random.Random(100)
secuencia_correcta = [rng_correcto.randint(1, 100) for _ in range(4)]

print("Sembrando dentro del bucle :", secuencia_defectuosa)
print("Instanciando una sola vez  :", secuencia_correcta)
```

Resultado esperado:

```text
Sembrando dentro del bucle : [19, 19, 19, 19]
Instanciando una sola vez  : [19, 59, 59, 99]
```

Diagnóstico: fijar la misma semilla antes de cada extracción rebobina el generador exactamente al primer elemento de la sucesión una y otra vez (`19`). La semilla o instancia `random.Random(semilla)` se inicializa **una única vez** al comienzo del flujo o experimento.

4. **Generar contraseñas o tokens de seguridad con `random` (`Importando_Random.py` L35-78).** Debe reemplazarse sin excepción por el módulo estándar `secrets` (`secrets.choice`, `secrets.token_urlsafe`, `secrets.token_hex`).

## 9. Resumen

- El módulo `random` de la **biblioteca estándar de Python** implementa el generador pseudoaleatorio determinista Mersenne Twister (MT19937), idóneo para simulaciones, juegos y muestreo estadístico, pero **nunca** apto para seguridad criptográfica.
- Para lograr reproducibilidad limpia sin contaminar el estado global del proceso, debe preferirse crear instancias aisladas `rng = random.Random(semilla)` frente a invocar `random.seed(...)` globalmente.
- Entre las funciones enteras, `randint(a, b)` incluye ambos extremos $[a, b]$, mientras que `randrange(start, stop, step)` es semiabierta $[\text{start}, \text{stop})$.
- Para colecciones, `choice(seq)` elige un elemento, `choices(..., weights=..., k=...)` muestrea **con reemplazo**, `sample(..., k=...)` muestrea **sin reemplazo** devolviendo una lista nueva, y `shuffle(lista)` permuta *in-place* retornando `None`.
- Toda generación de contraseñas, tokens de recuperación, claves o códigos OTP en producción debe realizarse con el módulo estándar `secrets` (**PEP 506**).

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/RANDOM/Importando_Random.py` (L1-183) | `Importando_Random.py` | `randrange`, `randint`, `uniform`, `choice`, `choices` con `weights`, `sample`, `shuffle` y ejercicio de generación de contraseña con `join` | Se explicó el algoritmo MT19937, se resolvió la duda de L16 sobre `set` (`TypeError`), se introdujo reproducibilidad con `random.Random(semilla)` y se corrigió la vulnerabilidad de seguridad de L35-78 sustituyendo `random` por `secrets` (**PEP 506**) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/RANDOM/numero_secreto.py` (L1-44) | `numero_secreto.py` | Juego de adivinanza acotado por intentos usando `from random import randint` y `while ... else:` | Se contrastó el intervalo cerrado $[1, N]$ de `randint` con `randrange` y el diseño desacoplado de entradas interactivas para pruebas deterministas |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L516-540) | `Juego.py` | Selección aleatoria de un objeto `Guerrero` mediante `id_azar = random.randrange(num)` e indexación `lista_guerrero[id_azar]` | Se propuso la alternativa idiomática directa `random.choice(lista_guerrero)` y la ubicación de `import random` en el nivel superior del archivo conforme a PEP 8 |

**Fundamento complementario:** se incorporaron cuatro fundamentos esenciales de la biblioteca estándar para completar el tratamiento riguroso del tema: (1) la naturaleza matemática determinista del generador Mersenne Twister y su estado interno de 624 palabras; (2) el aislamiento de estado mediante `random.Random(semilla)` frente al estado global compartido; (3) la función base continua `random()` y su aplicación en simulaciones de Monte Carlo; y (4) el módulo estándar `secrets` (**PEP 506**: `secrets.choice`, `secrets.token_urlsafe`, `secrets.compare_digest`) para criptografía y credenciales en producción.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/random.html> — Biblioteca estándar (`random`): generador Mersenne Twister, clase `Random`, funciones para enteros, secuencias y distribuciones reales, y advertencia de seguridad.
- <https://docs.python.org/3/library/secrets.html> — Biblioteca estándar (`secrets`): generación de números aleatorios criptográficamente fuertes para gestión de contraseñas, tokens de cuenta y secretos de seguridad.
- <https://peps.python.org/pep-0506/> — PEP 506 (*Adding A Secrets Module To The Standard Library*): motivación de seguridad y diseño del módulo `secrets` frente al uso indebido de `random`.
