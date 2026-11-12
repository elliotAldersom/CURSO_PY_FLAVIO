# Decoradores de Funciones, Fábricas Parametrizadas y Decoradores de Clases

## 2. Introducción

En el desarrollo de sistemas modulares aparecen de forma recurrente requisitos transversales (*cross-cutting concerns*) como el registro de auditoría, el control de permisos, la validación de entradas, el almacenamiento en caché, la política de reintentos o la medición de tiempos de respuesta. Incrustar ese código auxiliar directamente dentro de cada función de dominio contamina la lógica de negocio y multiplica la duplicación; obligar al código cliente a envolver manualmente cada llamada (`Decoradores.py` L25, L180) traslada esa complejidad hacia el consumidor.

Un **decorador** resuelve este problema estructural actuando como un transformador declarativo de objetos invocables o de clases: recibe una [función](../../Intermedio/chapter-two/funciones.md) o una [clase](../../Intermedio/chapter-five/clases_y_objetos.md), extiende o adapta su comportamiento sin alterar su código fuente original y devuelve el objeto resultante (`Decoradores.py` L1-10, L79-85). Dominar este mecanismo en profundidad resulta indispensable por cuatro razones arquitectónicas:

1. **Composición limpia mediante funciones de orden superior y clausuras:** aprovecha las celdas léxicas (`__closure__`) para encapsular lógica previa y posterior alrededor de cualquier operación.
2. **Generalidad de firmas y transparencia de retorno:** permite interceptar funciones arbitrarias mediante `*args, **kwargs` propagando íntegramente su valor de retorno y sus [excepciones](../../Intermedio/chapter-four/excepciones.md).
3. **Preservación de identidad e introspección con `@functools.wraps`:** evita destruir metadatos esenciales (`__name__`, `__doc__`, `__annotations__`, `__wrapped__`) requeridos por depuradores, generadores de documentación y marcos web modernos.
4. **Escalabilidad hacia fábricas parametrizadas y decoradores de clases:** habilita configuraciones declarativas (`@reintentar(intentos=3)`), apilamiento controlado de capas y transformación *in situ* de clases conforme a **PEP 318** y **PEP 3129**.

## 3. Fundamentos y conceptos

**Funciones como objetos de primera clase y clausuras léxicas (*closures*).** En Python, toda función es una instancia de `function` que puede asignarse a variables, almacenarse en estructuras de datos, pasarse como argumento a otra función (`Ejecutar_operacion(Suma, 5, 3)` en `Decoradores.py` L48-66) y retornarse como resultado. Cuando una función externa define una función interna `wrapper` que referencia variables del [ámbito envolvente](../../Intermedio/chapter-two/ambito_variables.md) —en particular, la función original `func`—, el compilador construye una **clausura** (*closure*). Dichas variables libres quedan retenidas en objetos celda (`cell`) accesibles en la tupla `wrapper.__closure__`, permaneciendo vivas incluso después de que la función decoradora haya finalizado su ejecución.

**Azúcar sintáctico `@decorador` y momento de evaluación (PEP 318).** La notación con arroba introducida en **PEP 318** no añade una primitiva mágica al intérprete, sino una equivalencia sintáctica exacta ejecutada **en tiempo de definición** (habitualmente al importar el [módulo](../../Intermedio/chapter-three/modulos.md)):

```text
@decorador                      def saludo():
def saludo():          <===>        return "Hola Mundo"
    return "Hola Mundo"         saludo = decorador(saludo)
```

Esta distinción temporal es fundamental (`Decoradores.py` L30-35, L79-85): el cuerpo de `decorador(saludo)` se ejecuta **una sola vez**, justo cuando Python termina de compilar `def saludo`, reasignando el identificador `saludo` al objeto `wrapper` devuelto. En cambio, el cuerpo de `wrapper` se ejecuta **cada vez que el programa invoca `saludo()`**.

**Reenvío universal de argumentos (`*args, **kwargs`) y propagación del retorno.** En las primeras versiones didácticas de `Decoradores.py` (L11-19) y `REPASOS/Decoradores.py` (L1-16), la función interna se declara sin parámetros (`def funcion_modificada():`), lo que impide decorar funciones que reciban datos de entrada. Para escribir un decorador de propósito general se emplea [desempaquetamiento](../../Intermedio/chapter-one/desempaquetamiento.md) variádico (`Decoradores.py` L87-123):

1. `def wrapper(*args, **kwargs):` acepta cualquier combinación de argumentos posicionales y nombrados.
2. `resultado = func(*args, **kwargs)` transfiere esos mismos argumentos a la función original y captura su salida.
3. `return resultado` devuelve el valor al llamador. Omitir este `return` —como sucede en `Decoradores_Multiples.py` (L5-18)— provoca que cualquier función decorada pierda silenciosamente su resultado y retorne `None`.

**Preservación obligatoria de metadatos con `@functools.wraps(func)`.** En todos los ejemplos del material base (`Decoradores.py`, `Decoradores_Multiples.py`, `REPASOS/Decoradores.py`), la sustitución `Saludo = wrapper` sobrescribe la identidad de la función original: `Saludo.__name__` pasa a valer `'wrapper'`, `Saludo.__doc__` se pierde (`None`) y `Saludo.__annotations__` queda vacío (`{}`). En sistemas reales, esa pérdida rompe herramientas que inspeccionan firmas en tiempo de ejecución (`help()`, `inspect.signature()`, enrutadores con inyección de dependencias como FastAPI, CLI declarativas como Click y recolectores de pruebas). Aplicar `@functools.wraps(func)` sobre `wrapper` copia automáticamente `__module__`, `__name__`, `__qualname__`, `__doc__` y `__annotations__`, actualiza `__dict__` y añade el atributo **`__wrapped__`** apuntando a la función original sin decorar.

**Fábricas de decoradores parametrizados (anidamiento de tres niveles).** Cuando el propio decorador requiere opciones de configuración (`@Calcular_tiempo_ejecucion("Saludo")` en `Decoradores.py` L190-221), la expresión situada tras `@` es una **llamada** que debe evaluar a un decorador. Esto exige tres niveles de funciones anidadas:

```text
@reintentar(max_intentos=3)
def consultar_remoto(id_recurso: int) -> str: ...

1) reintentar(max_intentos=3)  ──► Fábrica: recibe configuración y retorna 'decorador'
2) decorador(consultar_remoto) ──► Decorador: recibe 'func' y retorna 'wrapper'
3) wrapper(*args, **kwargs)    ──► Envoltorio: se ejecuta en cada llamada usando ambos contextos
```

Conviene evitar fábricas vacías sin parámetros como `@User_decorator()` (`Decoradores_Clases.py` L5, L42) o `@Decorador_accion()` (`Decoradores_Multiples.py` L183, L194): si la fábrica no recibe configuración alguna, la capa exterior resulta superflua y basta un decorador directo `@decorador_usuario`.

**Decoradores apilados (*stacked decorators*): aplicación ascendente frente a ejecución descendente.** Al superponer múltiples decoradores sobre una misma definición (`Decoradores.py` L159-164, `Decoradores_Multiples.py` L20-54), operan dos órdenes complementarios:

```text
@decorador_1
@decorador_2                 Equivalencia en definición:
def operacion(): ...   ===>  operacion = decorador_1(decorador_2(operacion))
```

- **Orden de aplicación (de abajo hacia arriba / *bottom-up*):** primero `decorador_2` envuelve a `operacion`, y acto seguido `decorador_1` envuelve al `wrapper` resultante de `decorador_2`.
- **Orden de ejecución en llamada (de afuera hacia adentro / modelo de capas concéntricas):** al invocar `operacion()`, entra primero el bloque previo de `decorador_1`, luego el bloque previo de `decorador_2`, se ejecuta `operacion()`, finaliza el bloque posterior de `decorador_2` y cierra el bloque posterior de `decorador_1`.

**Decoradores de clases (PEP 3129) y decoradores con estado mediante `__call__`.** A partir de **PEP 3129**, la sintaxis `@decorador` se aplica también sobre declaraciones `class`. En `Decoradores_Clases.py` (L10-40) y `Decoradores_Multiples.py` (L140-192) se implementa creando y retornando una **subclase dinámica local** (`class SuperUser(cls): ... return SuperUser`). Aunque funcional en guiones breves, este enfoque presenta limitaciones importantes en arquitectura de software —visibles en `Decoradores_Clases.py` L62, donde `type(user)` imprime `<class '__main__.User_decorator.<locals>.super_user.<locals>.SuperUser'>`—:

| Enfoque en decorador de clase | Identidad (`__name__`, `type`) | Árbol [MRO](../chapter-two/mro_herencia_multiple.md) | Serialización (`pickle`) y análisis estático |
|---|---|---|---|
| **Retornar subclase local `<locals>`** (`Decoradores_Clases.py` L14-36) | Reemplazada por el nombre interno de la subclase anidada | Añade capas extra por cada decorador apilado | Falla en `pickle` (no puede resolver clases alojadas en `<locals>`) y oculta cambios de `__init__` al analizador de tipos |
| **Modificar la clase *in situ* y retornar `cls`** (estándar en `@dataclass`, `@total_ordering`) | Intacta (`cls.__name__` y `cls.__qualname__` originales) | Sin clases intermedias artificiales | Totalmente compatible con `pickle`, introspección e importación estándar |

Por ello, en código de producción un decorador de clase suele inspeccionar o inyectar métodos directamente sobre `cls` (`setattr(cls, nombre, metodo)`) o registrar la clase en un catálogo, retornando el mismo objeto `cls`; si se requiere alterar el contrato de `__init__` añadiendo nuevos atributos de dominio (`altura`, `peso`, `rango`), la [herencia](../../Intermedio/chapter-five/herencia.md) explícita o la composición resultan más transparentes. Complementariamente, una clase que implementa el [método especial](metodos_especiales.md) `__call__` y llama a `functools.update_wrapper(self, func)` en `__init__` puede actuar como **decorador con estado** para funciones independientes, encapsulando contadores o cachés en atributos de instancia sin recurrir a variables `nonlocal`.

## 4. Sintaxis y funcionamiento

Estructura canónica de un decorador profesional con preservación de metadatos y de una fábrica parametrizada:

```text
from functools import wraps

# 1. Decorador simple
def auditar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Lógica previa
        resultado = func(*args, **kwargs)
        # Lógica posterior
        return resultado
    return wrapper

# 2. Fábrica de decoradores con argumentos
def limitar_rango(minimo: float, maximo: float):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            valor = func(*args, **kwargs)
            if not (minimo <= valor <= maximo):
                raise ValueError(f"Resultado {valor} fuera de [{minimo}, {maximo}]")
            return valor
        return wrapper
    return decorador
```

Elementos sintácticos y mecanismos del sistema de decoradores en Python:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `@decorador` | Reasigna en tiempo de definición `f = decorador(f)` (**PEP 318**) | `@auditar` |
| 2 | `*args, **kwargs` | Captura y reenvía cualquier firma posicional o nombrada hacia `func` | `return func(*args, **kwargs)` |
| 3 | `@functools.wraps(func)` | Copia `__name__`, `__doc__`, `__annotations__` y define `__wrapped__` | `@wraps(func)` sobre `def wrapper` |
| 4 | `func.__wrapped__` | Referencia directa al objeto original subyacente previa decoración | `funcion_decorada.__wrapped__` |
| 5 | `wrapper.__closure__` | Tupla de celdas léxicas con las variables libres capturadas | `len(f.__closure__)` |
| 6 | `@fabrica(arg1, arg2)` | Evalúa `fabrica(...)` para obtener el decorador que envolverá a `func` | `@reintentar(veces=3)` |
| 7 | `@d1` sobre `@d2` | Composición anidada equivalente a `f = d1(d2(f))` | Aplicación `d2 -> d1`; ejecución `d1 -> d2` |
| 8 | `@decorador_clase` | Recibe `cls`, añade métodos o registros *in situ* y retorna `cls` (**PEP 3129**) | `setattr(cls, "to_dict", ...); return cls` |
| 9 | Decorador basado en clase | Clase con `__init__(self, func)` y `__call__(self, *args, **kwargs)` | `update_wrapper(self, func)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Decorador genérico con `@functools.wraps`, propagación de retorno e inspección de clausura (`__closure__`) y `__wrapped__`.**

```python
from functools import wraps


def registrar_llamada(historial: list[str]):
    """Fábrica sencilla que registra entradas y salidas de forma determinista."""
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            argumentos = ", ".join(
                [*(repr(a) for a in args), *(f"{k}={v!r}" for k, v in kwargs.items())]
            )
            resultado = func(*args, **kwargs)
            historial.append(f"{func.__name__}({argumentos}) -> {resultado!r}")
            return resultado
        return wrapper
    return decorador


bitacora: list[str] = []


@registrar_llamada(bitacora)
def calcular_importe(subtotal: float, impuesto: float = 0.18) -> float:
    """Calcula el total final aplicando la tasa impositiva indicada."""
    return round(subtotal * (1.0 + impuesto), 2)


total_1 = calcular_importe(100.0)
total_2 = calcular_importe(250.0, impuesto=0.10)

nombres_celdas = sorted(
    type(celda.cell_contents).__name__ for celda in (calcular_importe.__closure__ or ())
)

print("Resultados:", total_1, "|", total_2)
print("Metadatos :", calcular_importe.__name__, "| Doc:", calcular_importe.__doc__)
print("Tipos en __closure__:", nombres_celdas)
print("Bitácora  :", bitacora)
print("Llamada directa a __wrapped__:", calcular_importe.__wrapped__(50.0))
print("Tamaño de bitácora tras __wrapped__:", len(bitacora))
```

Explicación paso a paso:

- Evolucionando `Decoradores.py` (L87-131), `wrapper` reenvía cualquier combinación de parámetros posicionales y con valor por defecto (`impuesto=0.18`), retornando intacto el `float` calculado.
- Gracias a `@wraps(func)`, `calcular_importe.__name__` y `__doc__` conservan la identidad original de la función de dominio, mientras que `__closure__` retiene la función original (`function`) y la lista `bitacora` (`list`). Invocar `__wrapped__` ejecuta la lógica pura eludiendo el decorador, técnica habitual en pruebas unitarias aisladas.

Resultado esperado:

```text
Resultados: 118.0 | 275.0
Metadatos : calcular_importe | Doc: Calcula el total final aplicando la tasa impositiva indicada.
Tipos en __closure__: ['function', 'list']
Bitácora  : ['calcular_importe(100.0) -> 118.0', 'calcular_importe(250.0, impuesto=0.1) -> 275.0']
Llamada directa a __wrapped__: 59.0
Tamaño de bitácora tras __wrapped__: 2
```

### Intermedio

**Ejemplo 2 — Fábrica parametrizada de reintentos controlados y orden exacto de composición en decoradores apilados.**

```python
from functools import wraps


def trazar_capa(etiqueta: str, eventos: list[str]):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            eventos.append(f"entrada:{etiqueta}")
            valor = func(*args, **kwargs)
            eventos.append(f"salida:{etiqueta}")
            return valor
        return wrapper
    return decorador


def reintentar(max_intentos: int, excepciones: tuple[type[Exception], ...]):
    if max_intentos < 1:
        raise ValueError("max_intentos debe ser al menos 1")

    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ultimo_error: Exception | None = None
            for intento in range(1, max_intentos + 1):
                try:
                    return func(*args, **kwargs)
                except excepciones as err:
                    ultimo_error = err
                    if intento == max_intentos:
                        raise
            raise RuntimeError("Estado inalcanzable") from ultimo_error
        return wrapper
    return decorador


flujo: list[str] = []
respuestas_simuladas = iter([ConnectionError("fallo 1"), ConnectionError("fallo 2"), "OK:200"])


@trazar_capa("externa", flujo)
@reintentar(max_intentos=3, excepciones=(ConnectionError,))
@trazar_capa("interna", flujo)
def consultar_servicio() -> str:
    flujo.append("ejecucion:nucleo")
    actual = next(respuestas_simuladas)
    if isinstance(actual, Exception):
        raise actual
    return actual


respuesta = consultar_servicio()
print("Respuesta final:", respuesta)
print("Secuencia de eventos:", flujo)
```

Explicación técnica:

- Se formaliza el apilamiento de `Decoradores_Multiples.py` (L20-54): la composición equivale a `trazar_capa("externa")(reintentar(...)(trazar_capa("interna")(consultar_servicio)))`.
- `trazar_capa("externa")` se ejecuta una sola vez alrededor de toda la operación global, mientras que `reintentar` envuelve a `trazar_capa("interna")`: en los dos primeros fallos (`ConnectionError`), la excepción interrumpe `salida:interna` y activa el siguiente intento; en el tercer intento tiene éxito y cierra ordenadamente `salida:interna` seguida de `salida:externa`.

Resultado esperado:

```text
Respuesta final: OK:200
Secuencia de eventos: ['entrada:externa', 'entrada:interna', 'ejecucion:nucleo', 'entrada:interna', 'ejecucion:nucleo', 'entrada:interna', 'ejecucion:nucleo', 'salida:interna', 'salida:externa']
```

### Avanzado

**Ejemplo 3 — Decorador de clase *in situ* (preservando tipo, `__qualname__` y MRO) frente a decorador con estado basado en `__call__`.**

```python
from functools import update_wrapper


def serializable_publico(cls: type) -> type:
    """Inyecta un método to_dict() en la clase original sin crear subclases <locals>."""
    def to_dict(self) -> dict[str, object]:
        return {
            clave: valor
            for clave, valor in self.__dict__.items()
            if not clave.startswith("_")
        }

    cls.to_dict = to_dict
    return cls


class ContadorInvocaciones:
    """Decorador con estado implementado mediante protocolo __call__."""

    def __init__(self, func) -> None:
        update_wrapper(self, func)
        self._func = func
        self.llamadas = 0

    def __call__(self, *args, **kwargs):
        self.llamadas += 1
        return self._func(*args, **kwargs)


@serializable_publico
class CuentaServicio:
    def __init__(self, usuario: str, rol: str, token_interno: str) -> None:
        self.usuario = usuario
        self.rol = rol
        self._token_interno = token_interno


@ContadorInvocaciones
def normalizar_codigo(prefijo: str, numero: int) -> str:
    """Genera un identificador canónico con relleno de ceros."""
    return f"{prefijo.upper()}-{numero:04d}"


cuenta = CuentaServicio("flavio", "arquitecto", "secreto-interno")
print("Nombre real de clase :", type(cuenta).__qualname__)
print("Jerarquía MRO        :", [c.__name__ for c in CuentaServicio.__mro__])
print("Diccionario público  :", cuenta.to_dict())

cod_1 = normalizar_codigo("ped", 7)
cod_2 = normalizar_codigo("ped", 42)
print("Códigos generados    :", cod_1, "|", cod_2)
print("Llamadas acumuladas  :", normalizar_codigo.llamadas, "| Nombre:", normalizar_codigo.__name__)
```

Explicación de arquitectura:

- Contrastando con `Decoradores_Clases.py` (L14-36, L62), `serializable_publico` añade `to_dict` directamente sobre `CuentaServicio` y retorna `cls`: `type(cuenta).__qualname__` sigue siendo `'CuentaServicio'` y el MRO consta únicamente de `['CuentaServicio', 'object']`, manteniendo compatibilidad plena con `pickle` y herramientas de tipado.
- Por su parte, `ContadorInvocaciones` emplea `update_wrapper(self, func)` e implementa `__call__` para contabilizar ejecuciones en un atributo público `.llamadas` sin variables globales.

Resultado esperado:

```text
Nombre real de clase : CuentaServicio
Jerarquía MRO        : ['CuentaServicio', 'object']
Diccionario público  : {'usuario': 'flavio', 'rol': 'arquitecto'}
Códigos generados    : PED-0007 | PED-0042
Llamadas acumuladas  : 2 | Nombre: normalizar_codigo
```

## 6. Aplicaciones en el mundo real

- **Enrutamiento HTTP, autenticación y control de acceso:** marcos como Flask, FastAPI y Django emplean `@app.get("/ruta")`, `@login_required` o `@requiere_permiso("admin")` para registrar *endpoints* y verificar credenciales antes de ejecutar el controlador.
- **Memoización y almacenamiento en caché transparente:** la biblioteca estándar provee `@functools.lru_cache(maxsize=256)` y `@functools.cache` para recordar resultados de funciones deterministas costosas sin modificar su algoritmo interno.
- **Tolerancia a fallos en sistemas distribuidos:** bibliotecas como `tenacity` aplican `@retry(...)` con espera exponencial (*exponential backoff*) sobre clientes HTTP o consultas de base de datos sujetas a cortes transitorios de red.
- **Generación automática de métodos en modelos de datos:** `@dataclasses.dataclass` y `@functools.total_ordering` son decoradores de clase estándar que inspeccionan anotaciones o métodos existentes e inyectan `__init__`, `__repr__`, `__eq__` u operadores relacionales *in situ*.
- **Instrumentación de pruebas automatizadas:** `pytest` y `unittest` utilizan `@pytest.mark.parametrize` y `@unittest.mock.patch` para inyectar casos tabulados o dobles de prueba alrededor de cada función de verificación.

## 7. Uso en producción

- **Incluir `@functools.wraps(func)` sin excepción en todo decorador funcional:** omitirlo degrada trazas de auditoría, documentación automática e inyección de dependencias basada en firmas (`inspect.signature`).
- **Medir rendimiento con relojes monotónicos (`time.perf_counter`) y sistemas de *logging*, nunca con `time.time()` ni `print()`:** en `Decoradores.py` (L134-144, L190-206) se utiliza `time.time()`, reloj de pared sujeto a saltos hacia atrás por sincronización NTP, e impresiones directas en consola. En producción debe emplearse `time.perf_counter()` reportando métricas al subsistema `logging` o a colectores de telemetría (OpenTelemetry, Prometheus).
- **Evitar efectos secundarios pesados durante la importación:** dado que `@decorador` se ejecuta al cargar el módulo, el cuerpo externo del decorador nunca debe abrir conexiones de red, consultar bases de datos ni leer archivos de configuración remotos; cualquier operación de E/S debe diferirse al interior de `wrapper`.
- **No alterar de forma implícita el tipo de retorno de la función decorada:** en `Decoradores.py` (L11-33) una función que devolvía `"Hola Mundo"` pasa a devolver `"Tu función es de longitud 10"`, y en `Decoradores_Multiples.py` (L58-72) una función que retorna `int` pasa a retornar `str`. Cambiar el contrato de salida sorprende a los llamadores y rompe la verificación estática de tipos (`mypy`, `pyright`).
- **Preferir modificación *in situ* en decoradores de clases:** salvo casos muy justificados, retornar el mismo objeto `cls` evita contaminar la jerarquía de herencia y conserva la serialización estándar.

## 8. Errores comunes y recomendaciones

1. **Olvidar la sentencia `return` al invocar `func(*args, **kwargs)` dentro de `wrapper`.**

```python
# ERROR INTENCIONAL: wrapper ejecuta func pero descarta su valor de retorno (Decoradores_Multiples.py L5-10)
from functools import wraps


def registrar_defectuoso(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)  # Falta 'return': wrapper devuelve implícitamente None
    return wrapper


@registrar_defectuoso
def sumar(a: int, b: int) -> int:
    return a + b


print("Valor recibido:", sumar(4, 6))  # Recibe None en lugar de 10
```

Diagnóstico: toda función en Python sin sentencia `return` explícita retorna `None`. Salvo que el propósito documentado del decorador sea suprimir la salida, `wrapper` debe capturar `resultado = func(*args, **kwargs)` y finalizar con `return resultado`.

2. **Omitir `@functools.wraps(func)` provocando colisiones de nombres y pérdida de documentación.**

```python
# ERROR INTENCIONAL: pérdida de __name__, __doc__ y __annotations__ al omitir @wraps
def decorador_sin_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorador_sin_wraps
def procesar_pago(monto: float) -> bool:
    """Ejecuta el cargo bancario validado."""
    return monto > 0


# procesar_pago.__name__ pasa a ser 'wrapper' y __doc__ pasa a ser None
```

Diagnóstico: en marcos web que registran rutas tomando `func.__name__` como identificador interno (por ejemplo, Flask), decorar dos vistas distintas con `decorador_sin_wraps` lanza un `AssertionError` al intentar registrar dos veces el nombre `'wrapper'`. Recomendación: añadir siempre `@wraps(func)`.

3. **Confundir la referencia a la función con su invocación al decorar (`@fabrica` vs `@fabrica()`) o retornar subclases `<locals>` no serializables.**

```python
# ERROR INTENCIONAL: subclase dinámica local que rompe pickle y altera la identidad de clase
import pickle


def envolver_en_subclase(cls):
    class SubclaseInterna(cls):
        pass
    return SubclaseInterna


@envolver_en_subclase
class Pedido:
    def __init__(self, codigo: str) -> None:
        self.codigo = codigo


# pickle.dumps(Pedido("A-1")) lanza PicklingError porque SubclaseInterna vive en <locals>
```

Diagnóstico: tal como sucede en `Decoradores_Clases.py` (L14-36), crear una clase dentro del ámbito local de una función impide a `pickle` localizar su ruta calificada a nivel de módulo (`Can't pickle local object`). Si solo se desea añadir métodos auxiliares a `Pedido`, deben asignarse sobre `cls` y retornar `cls`. Asimismo, al usar una fábrica con parámetros obligatorios o con paréntesis (`@reintentar(max_intentos=3)`), olvidar la llamada o pasar la función ejecutada (`Decorador(Saludo())`) produce un `TypeError` inmediato en tiempo de definición.

## 9. Resumen

- Un **decorador** es un objeto invocable que recibe una función o clase y devuelve un reemplazo enriquecido, evaluándose **en tiempo de definición** mediante el azúcar sintáctico `@decorador` (**PEP 318** y **PEP 3129**).
- Su funcionamiento se apoya en **funciones de primera clase** y **clausuras léxicas** (`__closure__`), que preservan la referencia a la función original y a los parámetros de configuración.
- Un `wrapper` reutilizable debe aceptar **`*args, **kwargs`**, retornar explícitamente el resultado de `func(*args, **kwargs)` y decorarse siempre con **`@functools.wraps(func)`** para conservar `__name__`, `__doc__`, `__annotations__` y `__wrapped__`.
- Las **fábricas de decoradores parametrizados** emplean tres niveles (`fabrica -> decorador -> wrapper`), mientras que los **decoradores apilados** (`@d1` sobre `@d2`) se aplican de abajo hacia arriba (`d1(d2(f))`) y ejecutan sus bloques previos de afuera hacia adentro.
- En **decoradores de clases**, modificar y retornar la clase original `cls` resulta preferible frente a generar subclases dinámicas en `<locals>`, reservando las clases con `__call__` para decoradores funcionales que requieran estado estructurado.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores.py` (L1-225) | `Decoradores.py` | Decorador básico `@Decorador`, funciones de orden superior (`Ejecutar_operacion`), fórmula `A(B) -> C`, `*args`/`**kwargs`, medición con `time.time()`, apilamiento y fábrica de 3 niveles `@Calcular_tiempo_ejecucion("Saludo")` | Se incorporó `@functools.wraps`, inspección de `__closure__` y `__wrapped__`, sustitución de `time.time()` por `time.perf_counter()` y preservación del tipo de retorno |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Multiples.py` (L1-267) | `Decoradores_Multiples.py` | Apilamiento `@decorador_1` / `@decorador_2`, encadenamiento `@Decorador_extra` / `@Decorador_edad` y apilamiento en clases `@Decorador_accion()` / `@Decorador_info()` | Se corrigió la omisión de `return` en `wrapper` (L5-18), se eliminó el acoplamiento con `input()` y se formalizó la diferencia entre orden de aplicación (*bottom-up*) y orden de ejecución (*top-down*) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Clases.py` (L1-62) | `Decoradores_Clases.py` | Fábrica `@User_decorator()` que retorna una subclase local `SuperUser(cls)` extendiendo `__init__` y métodos | Se analizó críticamente por qué `type(user)` cambia a `<locals>.SuperUser` rompiendo `pickle` y MRO, contrastándolo con decoradores de clase *in situ* que retornan `cls` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_@Property.py` (L1-84) | `Decoradores_@Property.py` | Uso de decoradores descriptores integrados (`@property`, `@nombre.setter`, `@Borrar_Datos.deleter`) | Se conectó el uso de `@property` como caso especializado de decorador basado en descriptores dentro del modelo de objetos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decoradores.py` (L1-33) | `Decoradores.py` | Decorador `@Delimitar` envolviendo `Pedir_Edad()` con validación de rango `[18, 130]` | Se desacopló la lógica de validación respecto de la lectura interactiva por consola (`input()`) y se generalizó la firma con `*args, **kwargs` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L1-86) | `Decorador_Property.py` | Decoradores `@property`, `@Datos.setter` y `@Datos.deleter` sobre la clase `Person` | Se articuló su relación con los decoradores de métodos de instancia dentro de clases |

**Fundamento complementario:** se incorporaron cuatro ejes indispensables para ingeniería de software en producción ausentes en los guiones originales: (1) el uso estricto de `@functools.wraps` y `functools.update_wrapper` junto con el atributo `__wrapped__`; (2) el modelo interno de celdas léxicas en `__closure__`; (3) la implementación de decoradores con estado mediante clases ejecutables (`__call__`); y (4) las implicaciones sobre serialización (`pickle`), tipado estático y MRO al decorar clases según **PEP 3129**.

## 11. Referencias oficiales

- <https://docs.python.org/3/glossary.html#term-decorator> — Glosario oficial de Python (*decorator*): definición concisa de decoradores y equivalencia sintáctica.
- <https://docs.python.org/3/library/functools.html#functools.wraps> — Biblioteca estándar (`functools.wraps` y `update_wrapper`): preservación de metadatos e introspección mediante `__wrapped__`.
- <https://docs.python.org/3/reference/compound_stmts.html#function-definitions> — Referencia del lenguaje (*Function definitions* y *Class definitions*): gramática formal y semántica de evaluación de expresiones `@decorator`.
- <https://peps.python.org/pep-0318/> — PEP 318 (*Decorators for Functions and Methods*): motivación histórica, diseño y reglas de apilamiento.
- <https://peps.python.org/pep-3129/> — PEP 3129 (*Class Decorators*): extensión formal de la sintaxis de decoradores a declaraciones de clase.
