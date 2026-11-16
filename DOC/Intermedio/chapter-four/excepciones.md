# Manejo de Excepciones, Jerarquía de Errores y Excepciones Personalizadas

## 2. Introducción

Durante la vida útil de un programa se presentan condiciones anómalas que impiden completar una instrucción de forma ordinaria: cadenas no numéricas recibidas desde una interfaz externa, divisiones entre cero, archivos inexistentes en [entrada/salida](../chapter-three/manejo_archivos.md) o índices fuera de rango. Si ninguno de los marcos de la pila de llamadas intercepta el fallo, el intérprete desenrolla la ejecución (*stack unwinding*), imprime la traza de pila (*traceback*) y finaliza el proceso con un código de salida distinto de cero.

Python modela estas interrupciones mediante **objetos excepción** organizados en una jerarquía de clases y gobernados por las sentencias estructuradas `try`, `except`, `else`, `finally` y `raise`. Dominar este mecanismo resulta esencial por cuatro razones arquitectónicas:

1. **Separación entre el flujo principal y la recuperación ante fallos:** evita contaminar cada línea de negocio con códigos numéricos de retorno o banderas de error.
2. **Especificidad en la captura:** distinguir entre la raíz `BaseException` y la subárbol `Exception` impide bloquear señales críticas del sistema como `KeyboardInterrupt` o `SystemExit`.
3. **Limpieza determinista e invariantes de estado:** articular `else` y `finally` garantiza tanto la reducción de la superficie protegida en `try` como la liberación incondicional de recursos.
4. **Expresividad de dominio y trazabilidad:** definir excepciones propias mediante [herencia](../chapter-five/herencia.md) y encadenar causas con `raise ... from e` (**PEP 3134**) traduce errores técnicos de bajo nivel en contratos claros de aplicación sin perder el diagnóstico original.

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

Un `except:` desnudo (sin clase) equivale a `except BaseException:`: intercepta también `SystemExit` y `KeyboardInterrupt`. Si ocurre dentro de un [bucle](../../Basico/chapter-two/bucles.md) `while True:` —o si se captura explícitamente `KeyboardInterrupt` para reiniciar la iteración—, el usuario queda atrapado sin poder abortar el programa mediante `Ctrl+C`. Por regla general, solo deben capturarse subclases concretas de `Exception` (p. ej. `except (ValueError, ZeroDivisionError) as e:`).

**Anatomía completa de `try` / `except` / `else` / `finally` e inspección del objeto excepción.** Cada cláusula cumple un rol preciso y mutuamente coordinado:

- `try`: delimita **únicamente** las instrucciones susceptibles de lanzar la excepción esperada. Cuanto más acotado sea el bloque `try`, menor es el riesgo de enmascarar errores ajenos involuntarios.
- `except (TipoA, TipoB) as e`: captura cualquier instancia que pertenezca a las clases listadas (o a sus subclases), evaluándose de arriba hacia abajo; por ello las subclases específicas (`ZeroDivisionError`) deben ubicarse **antes** que sus superclases (`ArithmeticError` o `Exception`). La variable enlazada con `as e` expone `type(e).__name__` (nombre exacto de la clase) y la tupla `e.args` con los argumentos pasados al instanciar el error. Al finalizar el bloque `except`, Python elimina automáticamente la variable `e` del ámbito local para evitar ciclos de referencias con el marco de pila (`__traceback__`).
- `else`: se ejecuta **si y solo si** el bloque `try` concluyó de principio a fin sin lanzar ninguna excepción y sin abandonar el bloque mediante `return`, `break` o `continue`. Permite ubicar código dependiente del éxito de `try` sin exponerlo accidentalmente a los manejadores `except` precedentes.
- `finally`: se ejecuta **siempre** al salir de la construcción `try`, tanto si todo tuvo éxito, como si una excepción fue capturada, como si una excepción no capturada sigue propagándose hacia arriba, o incluso si se ejecutó `return`, `break` o `continue`.

**Precisiones técnicas fundamentales sobre el flujo de excepciones.**

1. **Interacción de `return` dentro de `try` con `except`, `else` y `finally`:** Python evalúa las instrucciones secuencialmente; si una expresión falla, lanza la excepción **antes** de alcanzar cualquier sentencia `return` posterior en el bloque, transfiriendo el control de inmediato a `except`. Si la operación tiene éxito, `return` finaliza la [función](../chapter-two/funciones.md). Colocar `return` dentro de `try` omite la rama `else:` (pues el bloque se abandonó anticipadamente) pero ejecuta igualmente el bloque `finally` justo antes de devolver el valor al llamador.
2. **Potenciación fraccionaria de negativos frente a `math.sqrt`:** en Python 3, elevar un número negativo a un exponente flotante mediante el [operador](../../Basico/chapter-one/operadores.md) `**` (`(-9) ** 0.5`) **no lanza excepción**: retorna un número complejo de tipo `complex` (`(1.8369701987210297e-16+3j)`). En cambio, `math.sqrt(-9)` del módulo estándar `math` restringe su dominio a números reales no negativos y lanza explícitamente `ValueError`.

**Lanzamiento manual (`raise`), encadenamiento (`raise ... from e`, PEP 3134) y excepciones personalizadas.** La sentencia `raise` permite señalar violaciones de precondiciones o invariantes:

- `raise ClaseExcepcion("detalle")`: instancia y lanza una nueva excepción. En propiedades y métodos validadores, la práctica idiomática consiste en lanzar `TypeError` si el tipo es incorrecto o `ValueError` si el valor viola el dominio permitido. Análogamente, en métodos de interfaz que exigen sobrescritura puede utilizarse `raise NotImplementedError`.
- `raise` sin argumentos (únicamente válido dentro de un bloque `except`): relanza la misma excepción activa preservando intacta su traza de pila original (útil tras registrar un error en bitácora o revertir una transacción).
- `raise ExcepcionDeDominio("mensaje") from e` (**PEP 3134**): traduce una excepción de infraestructura (`KeyError`, `ValueError`, `OSError`) a una excepción semántica del negocio, almacenando explícitamente el error original en el atributo `__cause__` (`The above exception was the direct cause of the following exception`). Si se necesita ocultar deliberadamente un detalle interno irrelevante, `raise NuevaExcepcion(...) from None` suprime el contexto automático (`__context__`).
- **Excepciones personalizadas:** se definen creando clases que heredan de `Exception` (detallado en [herencia](../chapter-five/herencia.md)). Una excepción profesional invoca `super().__init__(mensaje_legible)` para fijar la representación textual exacta de `str(e)`, almacenando datos estructurados como atributos de instancia sin producir efectos secundarios en la salida estándar.

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

# Verificación de operaciones numéricas
potencia_compleja = (-9) ** 0.5
print("Tipo de (-9) ** 0.5:", type(potencia_compleja).__name__)
try:
    math.sqrt(-9)
except ValueError as err:
    print("Excepción en math.sqrt(-9):", type(err).__name__)
```

Explicación paso a paso:

- Se desacoplan los datos de entrada respecto de llamadas interactivas a consola y se capturan clases concretas (`ValueError` y `ZeroDivisionError`) en lugar de usar un `except:` desnudo.
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
- Cuando `usar_return_en_try=True` pero la entrada es `"abc"`, `int("abc")` falla en la línea previa al `return` y salta de inmediato a `except ValueError`.

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

- Se establece una clase raíz del paquete (`ErrorDominioInventario(Exception)`) que permite a capas superiores capturar cualquier fallo del subsistema en un solo punto si lo desean, o bien tratar con precisión `StockInsuficienteError` inspeccionando sus atributos tipados (`err.sku`, `err.solicitado`, `err.disponible`) sin imprimir nada dentro de `__init__`.
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

Diagnóstico: dado que `ZeroDivisionError` es subclase de `ArithmeticError` (`issubclass(ZeroDivisionError, ArithmeticError) == True`), ubicar primero `ArithmeticError` o `Exception` hace que las ramas posteriores sean código muerto. Recomendación: ordenar siempre las cláusulas `except` desde la subclase más específica hasta la más general.

2. **Imprimir en consola dentro de `__init__` y omitir `super().__init__(...)` en una excepción personalizada.**

```python
class ExcepcionConEfectoSecundario(Exception):
    def __init__(self, codigo: int, detalle: str) -> None:
        # Antipatrón: ensucia stdout y no formatea super().__init__
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

4. **Usar `except:` desnudo o capturar `KeyboardInterrupt` dentro de `while True:`.** Si se atrapa `KeyboardInterrupt` dentro de un bucle infinito solo para volver a solicitar datos, el usuario no podrá abortar el proceso. Si se requiere cerrar ordenadamente ante `Ctrl+C`, `KeyboardInterrupt` debe capturarse **fuera** del bucle principal para despedirse y finalizar, nunca para reiniciar la iteración.

## 9. Resumen

- Python diferencia entre errores gramaticales detectados en compilación (`SyntaxError`) y excepciones dinámicas en tiempo de ejecución organizadas bajo `BaseException`.
- Todo código de aplicación debe capturar subclases específicas de `Exception`, evitando `except:` desnudo para no interceptar `SystemExit` ni `KeyboardInterrupt`.
- En una estructura completa `try` / `except` / `else` / `finally`, el bloque `try` se mantiene mínimo, `else` corre solo cuando `try` finaliza sin excepciones ni `return`, y `finally` se ejecuta incondicionalmente (incluso justo antes de completarse un `return` originado en `try` o `except`).
- En Python 3, `(-9) ** 0.5` produce un número `complex` sin error, mientras que `math.sqrt(-9)` lanza `ValueError`.
- Las excepciones de dominio deben heredar de `Exception`, invocar `super().__init__(...)` y encadenarse mediante `raise NuevaExcepcion(...) from err` (**PEP 3134**) para preservar la causa raíz en `__cause__`.

## 10. Referencias oficiales

- <https://docs.python.org/3/tutorial/errors.html> — Tutorial oficial de Python (*Errors and Exceptions*): errores de sintaxis, captura con `try`/`except`/`else`/`finally`, lanzamiento con `raise`, encadenamiento y excepciones definidas por el usuario.
- <https://docs.python.org/3/library/exceptions.html> — Biblioteca estándar (*Built-in Exceptions*): árbol jerárquico completo encabezado por `BaseException` y `Exception`, atributos `args` y trazas.
- <https://docs.python.org/3/reference/compound_stmts.html#the-try-statement> — Referencia del lenguaje (*The `try` statement*): reglas formales de evaluación de `except`, `else`, `finally` e interacción con `return`, `break` y `continue`.
- <https://peps.python.org/pep-3134/> — PEP 3134 (*Exception Chaining and Embedded Tracebacks*): especificación de `raise ... from ...`, `__cause__`, `__context__` y `__traceback__`.
- <https://peps.python.org/pep-0765/> — PEP 765 (*Disallow return/break/continue that exit a finally block*): justificación técnica de `SyntaxWarning` al abandonar `finally` mediante sentencias de salto.
