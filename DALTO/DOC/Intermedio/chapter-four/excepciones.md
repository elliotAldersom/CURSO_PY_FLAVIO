# Manejo de Excepciones, Jerarquía de Errores y Excepciones Personalizadas

## 2. Introducción

Durante la vida útil de un programa se presentan condiciones anómalas que impiden completar una instrucción de forma ordinaria: cadenas no numéricas recibidas desde una interfaz externa (`Excepciones.py` L35-39), divisiones entre cero (`division.py` L60), archivos inexistentes en [entrada/salida](../chapter-three/manejo_archivos.md) o índices fuera de rango (`Juego.py` L505). Si ninguno de los marcos de la pila de llamadas intercepta el fallo, el intérprete desenrolla la ejecución (*stack unwinding*), imprime la traza de pila (*traceback*) y finaliza el proceso con un código de salida distinto de cero.

Python modela estas interrupciones mediante **objetos excepción** organizados en una jerarquía de clases y gobernados por las sentencias estructuradas `try`, `except`, `else`, `finally` y `raise`. Dominar este mecanismo resulta esencial por cuatro razones arquitectónicas:

1. **Separación entre el flujo principal y la recuperación ante fallos:** evita contaminar cada línea de negocio con códigos numéricos de retorno o banderas de error.
2. **Especificidad en la captura:** distinguir entre la raíz `BaseException` y la subárbol `Exception` impide bloquear señales críticas del sistema como `KeyboardInterrupt` o `SystemExit`.
3. **Limpieza determinista e invariantes de estado:** articular `else` y `finally` garantiza tanto la reducción de la superficie protegida en `try` como la liberación incondicional de recursos.
4. **Expresividad de dominio y trazabilidad:** definir excepciones propias mediante [herencia](../chapter-five/herencia.md) (`Mi_Excepcion.py` L4) y encadenar causas con `raise ... from e` (**PEP 3134**) traduce errores técnicos de bajo nivel en contratos claros de aplicación sin perder el diagnóstico original.

## 3. Fundamentos y conceptos

**Errores de sintaxis (`SyntaxError`) frente a excepciones en tiempo de ejecución.** Antes de ejecutar la primera línea de un módulo, el analizador (*parser*) de CPython transforma el código fuente en un árbol de sintaxis abstracta (*AST*) y lo compila a *bytecode*. Si encuentra una construcción gramaticalmente inválida (unos paréntesis sin cerrar o dos puntos omitidos tras `def`), emite un `SyntaxError` o `IndentationError` en fase de compilación: el módulo ni siquiera inicia su ejecución y un bloque `try` dentro del mismo archivo no puede atraparlo. Las **excepciones en tiempo de ejecución**, en cambio, ocurren sobre código sintácticamente válido cuando los [tipos de datos](../../Basico/chapter-one/tipos_datos.md) o el entorno incumplen las precondiciones de una operación (`int("abc")` -> `ValueError`, `10 / 0` -> `ZeroDivisionError`).

**Jerarquía `BaseException` frente a `Exception` y peligro de `except:` desnudo.** Todas las excepciones integradas heredan de `BaseException`, pero esta raíz se bifurca deliberadamente en dos ramas con propósitos distintos:

```text
BaseException
 ├── KeyboardInterrupt      (interrupción del usuario: Ctrl+C / SIGINT)
 ├── SystemExit             (solicitud de cierre del proceso: sys.exit())
 ├── GeneratorExit          (cierre de un generador o corrutina)
 └── Exception              (raíz de todos los errores de aplicación y biblioteca)
      ├── ValueError
      ├── TypeError
      ├── AttributeError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    └── OverflowError
      ├── OSError
      │    ├── FileNotFoundError
      │    └── PermissionError
      └── RuntimeError
           └── NotImplementedError
```

En `Excepciones.py` (L57-58, L71, L106) y `Mi_Excepcion.py` (L15) se utiliza `except:` sin especificar clase alguna. Un `except:` desnudo equivale a `except BaseException:`: intercepta también `SystemExit` y `KeyboardInterrupt`. Si ocurre dentro de un [bucle](../../Basico/chapter-two/bucles.md) `while True:` —o si se captura explícitamente `KeyboardInterrupt` para imprimir un aviso y continuar iterando, como en `division.py` (L46-47) y `BUENAS_PRACTICAS.py` (L14-15)—, el usuario queda atrapado sin poder abortar el programa mediante `Ctrl+C`. Por regla general, solo deben capturarse subclases concretas de `Exception` (p. ej. `except (ValueError, ZeroDivisionError) as e:`).

**Anatomía completa de `try` / `except` / `else` / `finally` e inspección del objeto excepción.** Cada cláusula cumple un rol preciso y mutuamente coordinado:

- `try`: delimita **únicamente** las instrucciones susceptibles de lanzar la excepción esperada. Cuanto más acotado sea el bloque `try`, menor es el riesgo de enmascarar errores ajenos (`Bug` de tipeo, `NameError` o `AttributeError` involuntario, como `.tile()` en `BUENAS_PRACTICAS.py` L43).
- `except (TipoA, TipoB) as e`: captura cualquier instancia que pertenezca a las clases listadas (o a sus subclases), evaluándose de arriba hacia abajo; por ello las subclases específicas (`ZeroDivisionError`) deben ubicarse **antes** que sus superclases (`ArithmeticError` o `Exception`, `Excepciones.py` L218-230). La variable enlazada con `as e` expone `type(e).__name__` (nombre exacto de la clase, `Excepciones.py` L175) y la tupla `e.args` con los argumentos pasados al instanciar el error. Al finalizar el bloque `except`, Python elimina automáticamente la variable `e` del ámbito local para evitar ciclos de referencias con el marco de pila (`__traceback__`).
- `else`: se ejecuta **si y solo si** el bloque `try` concluyó de principio a fin sin lanzar ninguna excepción y sin abandonar el bloque mediante `return`, `break` o `continue`. Permite ubicar código dependiente del éxito de `try` sin exponerlo accidentalmente a los manejadores `except` precedentes.
- `finally`: se ejecuta **siempre** al salir de la construcción `try`, tanto si todo tuvo éxito, como si una excepción fue capturada, como si una excepción no capturada sigue propagándose hacia arriba, o incluso si se ejecutó `return`, `break` o `continue`.

**Correcciones críticas al material original (`Excepciones.py`).** Al estudiar `Excepciones.py` deben tenerse presentes dos precisiones técnicas fundamentales sobre el comportamiento real de Python 3:

1. **Interacción de `return` dentro de `try` con `except`, `else` y `finally` (`Excepciones.py` L113-128):** el comentario original afirma que escribir `resultado = int(num_1) + int(num_2)` seguido de `return resultado` dentro de `try` "está mal, pues jamás llega al `except`, de frente nos vamos al `return`". Esa explicación es inexacta: Python evalúa las instrucciones secuencialmente; si `num_1` o `num_2` no representan un entero válido, `int(...)` lanza `ValueError` **antes** de alcanzar la sentencia `return`, transfiriendo el control de inmediato a `except`. Si la conversión tiene éxito, `return resultado` sí es funcionalmente válido y termina la [función](../chapter-two/funciones.md). Ahora bien, colocar `return` dentro de `try` tiene dos efectos concretos sobre las demás cláusulas: (a) **omite el bloque `else`**, porque el flujo abandonó `try` anticipadamente mediante `return`; y (b) **ejecuta igualmente el bloque `finally` justo antes de materializar la devolución del valor** al llamador. Preferir `else:` para el `break` o el `return` obedece al principio de mantener el bloque `try` reducido exclusivamente a la línea que puede fallar, no a que `return` impida entrar en `except`.
2. **Potenciación fraccionaria de negativos frente a `math.sqrt` (`Excepciones.py` L235-241):** el comentario sostiene que evaluar `(-9) ** 0.5` dentro de `try` lanza `ValueError` por tratarse de la raíz cuadrada de un número negativo. En Python 3 (tras la unificación numérica de operadores), elevar un número negativo a un exponente flotante mediante el [operador](../../Basico/chapter-one/operadores.md) `**` **no lanza ninguna excepción**: retorna un número complejo de tipo `complex` (`(1.8369701987210297e-16+3j)`). Quien sí restringe su dominio a los números reales no negativos y lanza explícitamente `ValueError` es `math.sqrt(-9)` del módulo estándar `math` (mientras que `cmath.sqrt(-9)` retorna `3j` de forma exacta).

**Lanzamiento manual (`raise`), encadenamiento (`raise ... from e`, PEP 3134) y excepciones personalizadas.** La sentencia `raise` permite señalar violaciones de precondiciones o invariantes (`division.py` L60, `OCP.py` L40):

- `raise ClaseExcepcion("detalle")`: instancia y lanza una nueva excepción. En propiedades y métodos validadores —como `@Datos.setter` en `Decorador_Property.py` (L35-52), donde originalmente solo se imprimen mensajes con `print()` dejando al código cliente sin enterarse del rechazo—, la práctica idiomática consiste en lanzar `TypeError` si el tipo es incorrecto o `ValueError` si el valor viola el dominio permitido, tal como L82-86 captura `AttributeError` tras eliminar atributos con `del`. Análogamente, en `OCP.py` (L39-40), `raise NotImplementedError` actúa al **invocar el método** no sobrescrito (no al instanciar la clase base; para impedir la instanciación misma se emplea `abc.ABC`, estudiado en [clases abstractas](../../Avanzado/chapter-two/abstraccion_abc.md)).
- `raise` sin argumentos (únicamente válido dentro de un bloque `except`): relanza la misma excepción activa preservando intacta su traza de pila original (útil tras registrar un error en bitácora o revertir una transacción, como se aplicó en `manejo_archivos.md`).
- `raise ExcepcionDeDominio("mensaje") from e` (**PEP 3134**): traduce una excepción de infraestructura (`KeyError`, `ValueError`, `OSError`) a una excepción semántica del negocio, almacenando explícitamente el error original en el atributo `__cause__` (`The above exception was the direct cause of the following exception`). Si se necesita ocultar deliberadamente un detalle interno irrelevante, `raise NuevaExcepcion(...) from None` suprime el contexto automático (`__context__`).
- **Excepciones personalizadas:** se definen creando clases que heredan de `Exception` (detallado en [herencia](../chapter-five/herencia.md)). A diferencia de `Mi_Excepcion.py` (L4-6), donde `__init__` ejecuta un `print()` en consola y omite inicializar la superclase, una excepción profesional invoca `super().__init__(mensaje_legible)` para fijar la representación textual exacta de `str(e)` (evitando que `BaseException.__new__` exponga tuplas crudas o falle ante argumentos por palabra clave), almacenando datos estructurados como atributos de instancia sin producir efectos secundarios en la salida estándar.

**Filosofía EAFP frente a LBYL.** La comunidad Python distingue dos estilos de control defensivo:

- **LBYL** (*Look Before You Leap*, "mirar antes de saltar"): verificar mediante múltiples [condicionales](../../Basico/chapter-one/condicionales.md) previos si una clave existe, si una cadena contiene dígitos o si un archivo está disponible antes de operar. En entornos concurrentes o de sistema de archivos, LBYL sufre condiciones de carrera (*TOCTOU*: el archivo puede borrarse entre la comprobación y la apertura) y duplica búsquedas en [diccionarios](../chapter-one/diccionarios.md).
- **EAFP** (*Easier to Ask for Forgiveness than Permission*, "es más fácil pedir perdón que permiso"): ejecutar directamente la operación asumiendo el caso válido y capturar la excepción específica (`KeyError`, `ValueError`, `FileNotFoundError`) solo cuando el supuesto falla. En Python, entrar en un bloque `try` donde **no** ocurre excepción tiene costo computacional casi nulo (especialmente desde los *zero-cost exceptions* introducidos en CPython 3.11); el costo de construir la traza se paga únicamente cuando el fallo sucede de verdad, por lo que EAFP resulta óptimo siempre que las excepciones sean genuinamente excepcionales y no el flujo ordinario de un bucle intensivo.

## 4. Sintaxis y funcionamiento

Estructura completa del manejo y encadenamiento de excepciones:

```text
try:
    <operacion_riesgosa_acotada>
except <SubclaseEspecifica> as err:
    <recuperacion_o_traduccion_con_raise_from>
except (<OtraExcepcionA>, <OtraExcepcionB>) as err:
    <manejo_agrupado>
else:
    <codigo_ejecutado_solo_si_try_termino_sin_excepcion_ni_return>
finally:
    <limpieza_determinista_ejecutada_siempre>
```

Referencia de elementos sintácticos, clases e inspección de errores:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `try:` | Delimita la sección mínima susceptible de lanzar una excepción | `try: x = int(texto)` |
| 2 | `except Tipo as e:` | Captura instancias de `Tipo` (o subclases) y las enlaza a `e` | `except ValueError as e:` |
| 3 | `except (A, B) as e:` | Agrupa múltiples tipos de excepción bajo un mismo manejador | `except (KeyError, IndexError) as e:` |
| 4 | `else:` | Se ejecuta si `try` concluyó normalmente sin lanzar excepción ni `return` | `else: procesar(x)` |
| 5 | `finally:` | Se ejecuta siempre al abandonar `try` (con o sin error o `return`) | `finally: recurso.cerrar()` |
| 6 | `raise Excepcion(...)` | Instancia e inicia manualmente la propagación de una excepción | `raise ValueError("Edad negativa")` |
| 7 | `raise` (sin argumentos) | Relanza en `except` la excepción actual conservando su *traceback* | `registrar(e); raise` |
| 8 | `raise Nueva(...) from e` | Encadena explícitamente `e` en `Nueva.__cause__` (**PEP 3134**) | `raise ErrorConfig("...") from e` |
| 9 | `type(e).__name__` / `e.args` | Nombre de la clase del error y tupla de argumentos de construcción | `f"{type(e).__name__}: {e.args}"` |
| 10 | `class MiError(Exception):` | Define una excepción de dominio inicializando `super().__init__` | `class CupoAgotadoError(Exception): pass` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Captura específica (`ValueError`, `ZeroDivisionError`), flujo `else`/`finally` y contraste real entre `(-9) ** 0.5` y `math.sqrt(-9)`.**

```python
import math


def dividir_entradas(numerador_txt: str, denominador_txt: str) -> float | None:
    try:
        numerador = float(numerador_txt)
        denominador = float(denominador_txt)
        cociente = numerador / denominador
    except ValueError as err:
        print(f"[Error de formato] {type(err).__name__}: {err.args[0]}")
        return None
    except ZeroDivisionError as err:
        print(f"[Error aritmético] {type(err).__name__}: {err.args[0]}")
        return None
    else:
        print(f"[Éxito] Cociente calculado: {cociente:.2f}")
        return cociente
    finally:
        print(f"[Finally] Cierre de intento para ({numerador_txt!r}, {denominador_txt!r})")


dividir_entradas("15", "4")
dividir_entradas("15", "0")
dividir_entradas("quince", "4")

# Verificación experimental de la corrección a Excepciones.py (L235-241)
potencia_compleja = (-9) ** 0.5
print("Tipo de (-9) ** 0.5:", type(potencia_compleja).__name__)
try:
    math.sqrt(-9)
except ValueError as err:
    print("Excepción en math.sqrt(-9):", type(err).__name__)
```

Explicación paso a paso:

- Se refactorizan `Excepciones.py` y `division.py` desacoplando los datos de entrada respecto de `input()` y capturando clases concretas (`ValueError` y `ZeroDivisionError`) en lugar de `except:` desnudo.
- En el caso válido `("15", "4")` se ejecutan `try` -> `else` -> `finally`; en los dos casos fallidos se ejecutan `try` (hasta la línea que falla) -> `except` correspondiente -> `finally`.
- Al final se comprueba que `(-9) ** 0.5` produce un objeto `complex` sin lanzar error alguno, mientras que `math.sqrt(-9)` sí dispara `ValueError`.

Resultado esperado:

```text
[Éxito] Cociente calculado: 3.75
[Finally] Cierre de intento para ('15', '4')
[Error aritmético] ZeroDivisionError: division by zero
[Finally] Cierre de intento para ('15', '0')
[Error de formato] ValueError: could not convert string to float: 'quince'
[Finally] Cierre de intento para ('quince', '4')
Tipo de (-9) ** 0.5: complex
Excepción en math.sqrt(-9): ValueError
```

### Intermedio

**Ejemplo 2 — Trazabilidad exacta de `return` dentro de `try` frente a `else` y `finally`, y procesamiento EAFP de registros.**

```python
def evaluar_flujo_retorno(
    texto: str,
    usar_return_en_try: bool,
) -> tuple[int | None, list[str]]:
    traza: list[str] = []
    try:
        traza.append("try:inicio")
        valor = int(texto)
        traza.append("try:convertido")
        if usar_return_en_try:
            return valor * 2, traza
    except ValueError:
        traza.append("except:ValueError")
        return None, traza
    else:
        traza.append("else:sin_excepcion")
        return valor * 2, traza
    finally:
        traza.append("finally:limpieza")


res_a, traza_a = evaluar_flujo_retorno("21", usar_return_en_try=True)
res_b, traza_b = evaluar_flujo_retorno("21", usar_return_en_try=False)
res_c, traza_c = evaluar_flujo_retorno("abc", usar_return_en_try=True)

print("Con return en try :", res_a, "->", traza_a)
print("Con return en else:", res_b, "->", traza_b)
print("Con texto inválido:", res_c, "->", traza_c)
```

Explicación técnica:

- Cuando `usar_return_en_try=True` y la entrada es `"21"`, `return` abandona `try` directamente: el bloque `else` no llega a ejecutarse, pero `finally` **sí** añade `"finally:limpieza"` a la lista antes de entregar el resultado `42` al llamador.
- Cuando `usar_return_en_try=True` pero la entrada es `"abc"`, `int("abc")` falla en la línea previa al `return` y salta de inmediato a `except ValueError` (aclarando la confusión de `Excepciones.py` L113-128).

Resultado esperado:

```text
Con return en try : 42 -> ['try:inicio', 'try:convertido', 'finally:limpieza']
Con return en else: 42 -> ['try:inicio', 'try:convertido', 'else:sin_excepcion', 'finally:limpieza']
Con texto inválido: None -> ['try:inicio', 'except:ValueError', 'finally:limpieza']
```

### Avanzado

**Ejemplo 3 — Jerarquía de excepciones personalizadas de dominio con atributos estructurados y encadenamiento explícito `raise ... from e` (PEP 3134).**

```python
class ErrorDominioInventario(Exception):
    """Raíz de todas las excepciones de negocio del subsistema de inventario."""


class StockInsuficienteError(ErrorDominioInventario):
    def __init__(self, sku: str, solicitado: int, disponible: int) -> None:
        self.sku = sku
        self.solicitado = solicitado
        self.disponible = disponible
        super().__init__(
            f"SKU {sku}: solicitado={solicitado}, disponible={disponible}"
        )


class ConfiguracionTarifaInvalidaError(ErrorDominioInventario):
    """Error al interpretar parámetros de tarifas o impuestos."""


def leer_tasa_impuesto(config: dict[str, str], clave: str) -> float:
    try:
        tasa = float(config[clave])
    except (KeyError, ValueError) as err:
        raise ConfiguracionTarifaInvalidaError(
            f"Parámetro inválido o ausente para {clave!r}"
        ) from err
    if not (0.0 <= tasa <= 1.0):
        raise ConfiguracionTarifaInvalidaError(
            f"La tasa {tasa} debe encontrarse en el intervalo [0.0, 1.0]"
        )
    return tasa


def reservar_unidades(inventario: dict[str, int], sku: str, cantidad: int) -> int:
    if cantidad <= 0:
        raise ValueError("La cantidad a reservar debe ser un entero positivo")
    disponible = inventario.get(sku, 0)
    if cantidad > disponible:
        raise StockInsuficienteError(sku, cantidad, disponible)
    inventario[sku] = disponible - cantidad
    return inventario[sku]


almacen = {"TECLADO-MEC": 4}
try:
    reservar_unidades(almacen, "TECLADO-MEC", 10)
except StockInsuficienteError as err:
    faltante = err.solicitado - err.disponible
    print(f"{type(err).__name__} -> {err} (faltan {faltante} unidades)")

try:
    leer_tasa_impuesto({"igv": "dieciocho"}, "igv")
except ConfiguracionTarifaInvalidaError as err:
    causa = err.__cause__
    print(f"{type(err).__name__}: {err}")
    print(f"Causa raíz preservada (__cause__): {type(causa).__name__}")
```

Explicación de arquitectura:

- Evolucionando `Mi_Excepcion.py` (L4-6), se establece una clase raíz del paquete (`ErrorDominioInventario(Exception)`) que permite a capas superiores capturar cualquier fallo del subsistema en un solo punto si lo desean, o bien tratar con precisión `StockInsuficienteError` inspeccionando sus atributos tipados (`err.sku`, `err.solicitado`, `err.disponible`) sin imprimir nada dentro de `__init__`.
- En `leer_tasa_impuesto`, `raise ConfiguracionTarifaInvalidaError(...) from err` desacopla al llamador de si el fallo interno fue `KeyError` o `ValueError`, pero conserva intacto el error subyacente en `err.__cause__` para auditoría y registro en bitácoras.

Resultado esperado:

```text
StockInsuficienteError -> SKU TECLADO-MEC: solicitado=10, disponible=4 (faltan 6 unidades)
ConfiguracionTarifaInvalidaError: Parámetro inválido o ausente para 'igv'
Causa raíz preservada (__cause__): ValueError
```

## 6. Aplicaciones en el mundo real

- **APIs web y microservicios HTTP:** capas intermedias (*middlewares* en FastAPI o Django) traducen excepciones de dominio (`StockInsuficienteError`, `PermisoDenegadoError`) a respuestas HTTP estructuradas (`409 Conflict`, `403 Forbidden`) con cargas JSON uniformes, reservando `500 Internal Server Error` para fallos imprevistos.
- **Clientes de red y bases de datos con reintentos exponenciales:** capturar selectivamente errores transitorios (`TimeoutError`, `ConnectionError`) para aplicar reintentos con retroceso (*exponential backoff*), dejando propagar de inmediato errores permanentes de lógica (`ValueError`, `IntegrityError`).
- **Validación de modelos y propiedades encapsuladas:** lanzar `ValueError` o `TypeError` dentro de constructores y `@property.setter` ([encapsulamiento](../chapter-five/encapsulamiento.md)) para impedir que una entidad entre en un estado inconsistente.
- **Transacciones atómicas de persistencia:** envolver operaciones de múltiples pasos en bloques `try` que ejecutan `commit()` en `else:`, `rollback()` y `raise` en `except Exception:`, y cierre de sesión o conexión en `finally:`.

## 7. Uso en producción

- **Prohibir el silenciamiento de excepciones (`except Exception: pass`):** tragar un error sin registrarlo ni actuar convierte fallos detectables en corrupción silenciosa de datos. Cuando un error debe propagarse tras realizar tareas locales de contingencia, se registra con `logging.exception("...")` (que adjunta automáticamente el *traceback* completo) y se ejecuta `raise` sin argumentos.
- **Jerarquías propias por paquete o capa de dominio:** todo paquete reutilizable o capa de aplicación define una excepción base propia (`class ErrorFacturacion(Exception): pass`) de la que heredan las demás excepciones específicas del módulo, facilitando contratos estables para consumidores externos.
- **Preservar siempre la cadena causal con `from e`:** al capturar una excepción de infraestructura (driver SQL, cliente HTTP, sistema de archivos) dentro de un adaptador y lanzar una excepción del dominio, emplear sistemáticamente `raise ErrorRepositorio(...) from e` para no amputar la causa raíz en herramientas de observabilidad (Sentry, OpenTelemetry).
- **Respetar las señales de terminación del proceso:** nunca interceptar `BaseException`, `SystemExit` ni `KeyboardInterrupt` dentro de bucles de trabajo ordinarios; estas excepciones deben alcanzar el punto de entrada superior del programa para ejecutar un apagado ordenado (*graceful shutdown*).

## 8. Errores comunes y recomendaciones

1. **Colocar una clase base antes que sus subclases en bloques `except` sucesivos.**

```python
try:
    _ = 10 / 0
except ArithmeticError:
    print("Capturado por ArithmeticError general (ZeroDivisionError queda inalcanzable)")
except ZeroDivisionError:
    print("Capturado por ZeroDivisionError específico")
```

Resultado esperado:

```text
Capturado por ArithmeticError general (ZeroDivisionError queda inalcanzable)
```

Diagnóstico: dado que `ZeroDivisionError` es subclase de `ArithmeticError` (`issubclass(ZeroDivisionError, ArithmeticError) == True`), ubicar primero `ArithmeticError` o `Exception` hace que las ramas posteriores sean código muerto. Recomendación: ordenar siempre las cláusulas `except` desde la subclase más específica hasta la más general (`Excepciones.py` L215-230).

2. **Imprimir en consola dentro de `__init__` y omitir `super().__init__(...)` en una excepción personalizada.**

```python
class ExcepcionConEfectoSecundario(Exception):
    def __init__(self, codigo: int, detalle: str) -> None:
        # Antipatrón (Mi_Excepcion.py L5-6): ensucia stdout y no formatea super().__init__
        print(f"[Salida forzada en __init__] {detalle}")
        self.codigo = codigo


class ExcepcionLimpia(Exception):
    def __init__(self, codigo: int, detalle: str) -> None:
        self.codigo = codigo
        self.detalle = detalle
        super().__init__(f"[Código {codigo}] {detalle}")


try:
    raise ExcepcionConEfectoSecundario(400, "parámetro inválido")
except ExcepcionConEfectoSecundario as e_mal:
    print("Antipatrón str(e):", repr(str(e_mal)))

try:
    raise ExcepcionLimpia(400, "parámetro inválido")
except ExcepcionLimpia as e_bien:
    print("Correcta   str(e):", repr(str(e_bien)))
```

Resultado esperado:

```text
[Salida forzada en __init__] parámetro inválido
Antipatrón str(e): "(400, 'parámetro inválido')"
Correcta   str(e): '[Código 400] parámetro inválido'
```

Diagnóstico: incluir `print()` en `__init__` contamina la salida estándar incluso cuando un llamador captura y resuelve legítimamente la excepción, y omitir `super().__init__(mensaje)` deja en `e.args` la tupla cruda pasada a `BaseException.__new__` (además de provocar `TypeError` si se invoca con argumentos por nombre).

3. **Incluir `return`, `break` o `continue` dentro de `finally` (advertido por PEP 765 en Python 3.14+).**

```python
# ERROR INTENCIONAL: antipatrón PEP 765 — usar return dentro de finally descarta excepciones activas
def dividir_ocultando_fallo(a: float, b: float) -> float:
    try:
        return a / b
    finally:
        return -1.0


print(dividir_ocultando_fallo(10, 0))
```

Diagnóstico: una sentencia `return` dentro de `finally` aborta y descarta silenciosamente cualquier excepción no capturada que estuviera propagándose desde `try` (como `ZeroDivisionError`), además de sobrescribir el valor de retorno legítimo. Desde Python 3.14 (**PEP 765**), el compilador emite explícitamente `SyntaxWarning: 'return' in a 'finally' block`. Recomendación: reservar `finally` únicamente para limpieza de estado o liberación de recursos, sin sentencias de salto de control.

4. **Usar `except:` desnudo o capturar `KeyboardInterrupt` dentro de `while True:`.** En `division.py` (L46-47, L69-70) y `Juego.py` (L29) se atrapa `KeyboardInterrupt` dentro de un bucle infinito solo para volver a solicitar datos. Si se requiere cerrar ordenadamente ante `Ctrl+C`, `KeyboardInterrupt` debe capturarse **fuera** del bucle principal para despedirse y finalizar, nunca para reiniciar la iteración.

## 9. Resumen

- Python diferencia entre errores gramaticales detectados en compilación (`SyntaxError`) y excepciones dinámicas en tiempo de ejecución organizadas bajo `BaseException`.
- Todo código de aplicación debe capturar subclases específicas de `Exception`, evitando `except:` desnudo para no interceptar `SystemExit` ni `KeyboardInterrupt`.
- En una estructura completa `try` / `except` / `else` / `finally`, el bloque `try` se mantiene mínimo, `else` corre solo cuando `try` finaliza sin excepciones ni `return`, y `finally` se ejecuta incondicionalmente (incluso justo antes de completarse un `return` originado en `try` o `except`).
- En Python 3, `(-9) ** 0.5` produce un número `complex` sin error, mientras que `math.sqrt(-9)` lanza `ValueError`.
- Las excepciones de dominio deben heredar de `Exception`, invocar `super().__init__(...)` y encadenarse mediante `raise NuevaExcepcion(...) from err` (**PEP 3134**) para preservar la causa raíz en `__cause__`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_FOUR/CLASE_CUARTA/EXCEPCIONES/Excepciones.py` (L1-245) | `Excepciones.py` | Concepto de evento frente a excepción, `try`/`except`, `Exception as e`, `type(e).__name__`, `else` y `finally` | Se corrigieron las dos imprecisiones de L113-128 (`return` en `try` frente a `except`/`else`/`finally`) y L235-241 (`(-9) ** 0.5` retorna `complex`, `math.sqrt(-9)` lanza `ValueError`), reemplazando `except:` desnudo |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_FOUR/CLASE_CUARTA/EXCEPCIONES/division.py` (L1-99) | `division.py` | Captura de `ValueError` y `ZeroDivisionError`, lanzamiento manual con `raise ZeroDivisionError` | Se analizó por qué la primera versión (L3-25) ubicaba `ZeroDivisionError` donde no había división y por qué atrapar `KeyboardInterrupt` dentro de `while True:` (L46, L69) bloquea `Ctrl+C` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_FOUR/CLASE_CUARTA/EXCEPCIONES/Mi_Excepcion.py` (L1-16) | `Mi_Excepcion.py` | Subclase `class MiExcepcion(Exception):` y disparo con `raise MiExcepcion(...)` | Se sustituyó el `print()` en `__init__` por inicialización mediante `super().__init__(...)`, atributos estructurados de dominio y captura tipada |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py` (L20-106, L121-142) | `One.py` | Bloques `try` con múltiples cláusulas `except` (`ValueError`, `KeyboardInterrupt`, `EOFError`) y `else:` | Se contrastó la validación interactiva acoplada a `__init__` frente al lanzamiento de excepciones en constructores desacoplados |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L14-15, L109-184) | `BUENAS_PRACTICAS.py` | Captura agrupada en tupla `except (ValueError, EOFError, KeyboardInterrupt):` y extracción de `Pedir_Datos()` fuera de la clase | Se explicó cómo un bloque `try` extenso llega a camuflar errores de programación internos (como `AttributeError` por `.tile()` en L43) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L29, L480-514, L544-566) | `Juego.py` | Captura combinada incorporando `IndexError` en selección de elementos por índice | Se relacionó con el principio EAFP frente a comprobaciones redundantes de rangos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/CLASE_CUARTA/OCP.py` (L36-40) | `OCP.py` | Uso de `raise NotImplementedError` en método base `Notificar(self)` | Se precisó que `NotImplementedError` actúa al invocar el método en tiempo de ejecución y no al instanciar la clase base (diferenciándolo de `abc.ABC`) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L35-52, L82-86) | `Decorador_Property.py` | Captura de `AttributeError` tras `del xd.Datos` (L82-86) y validación manual en `@Datos.setter` | Se contrastó el uso de `print()` en `@Datos.setter` (L35-52) con la señalización correcta de invariantes mediante `raise TypeError` y `raise ValueError` |

**Fundamento complementario:** se incorporaron cinco pilares esenciales de la especificación del lenguaje para un dominio riguroso del tema: (1) la distinción entre compilación (`SyntaxError`) y ejecución; (2) el árbol completo `BaseException` frente a `Exception`; (3) el encadenamiento explícito de excepciones mediante `raise ... from e` e inspección de `__cause__` (**PEP 3134**); (4) el contraste arquitectónico entre **EAFP** y **LBYL**; y (5) la advertencia sobre saltos de control dentro de `finally` estandarizada en **PEP 765**.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/errors.html> — Tutorial oficial de Python (*Errors and Exceptions*): errores de sintaxis, captura con `try`/`except`/`else`/`finally`, lanzamiento con `raise`, encadenamiento y excepciones definidas por el usuario.
- <https://docs.python.org/3/library/exceptions.html> — Biblioteca estándar (*Built-in Exceptions*): árbol jerárquico completo encabezado por `BaseException` y `Exception`, atributos `args` y trazas.
- <https://docs.python.org/3/reference/compound_stmts.html#the-try-statement> — Referencia del lenguaje (*The `try` statement*): reglas formales de evaluación de `except`, `else`, `finally` e interacción con `return`, `break` y `continue`.
- <https://peps.python.org/pep-3134/> — PEP 3134 (*Exception Chaining and Embedded Tracebacks*): especificación de `raise ... from ...`, `__cause__`, `__context__` y `__traceback__`.
- <https://peps.python.org/pep-0765/> — PEP 765 (*Disallow return/break/continue that exit a finally block*): justificación técnica de `SyntaxWarning` al abandonar `finally` mediante sentencias de salto.
