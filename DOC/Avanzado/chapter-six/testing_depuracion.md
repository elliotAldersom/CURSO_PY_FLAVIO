# Pruebas Automatizadas y Depuración (`unittest`, `pytest` y `pdb`)

## 2. Introducción

En la ingeniería de software profesional, la calidad, estabilidad y mantenibilidad de un sistema no se evalúan únicamente por la elegancia de su arquitectura o por si "funciona en la máquina del desarrollador", sino por la existencia de una suite de **pruebas automatizadas rigurosa, reproducible y determinista**.

Sin pruebas automatizadas, cada nueva funcionalidad, refactorización o corrección de error introduce el riesgo inminente de regresiones (*regressions*): defectos colaterales en componentes preexistentes que pueden pasar inadvertidos hasta alcanzar el entorno de producción.

Python provee una infraestructura integral para la verificación de software:
1. **`unittest`:** marco de pruebas integrado en la biblioteca estándar basado en la arquitectura clásica xUnit, que provee clases base `TestCase`, aserciones formales y ciclo de vida de fixtures.
2. **`pytest`:** el estándar de la industria moderna en el ecosistema Python, caracterizado por una sintaxis declarativa limpia, el uso de sentencias `assert` nativas con introspección avanzada y un sistema modular de fixtures inyectables.
3. **`unittest.mock`:** subsistema para aislar componentes mediante dobles de prueba (*mocks* y *stubs*), simulando llamadas de red, bases de datos o reloj del sistema.
4. **`pdb` / `breakpoint()` (PEP 553):** depurador interactivo integrado que permite inspeccionar marcos de pila, evaluar expresiones y controlar la ejecución paso a paso en tiempo de desarrollo.

## 3. Fundamentos y conceptos

**La Pirámide de Pruebas y Tipologías de Testing.**
Una suite equilibrada distribuye sus pruebas en tres capas:
1. **Pruebas Unitarias (*Unit Tests*):** verifican funciones, métodos o clases individuales de forma completamente aislada del resto del sistema. Deben ser rápidas (milisegundos), deterministas y no interactuar con I/O real (red, disco, base de datos).
2. **Pruebas de Integración (*Integration Tests*):** verifican la interacción correcta entre dos o más subsistemas (p. ej. un repositorio con una base de datos de prueba o la serialización [JSON](../../Intermedio/chapter-three/archivos_json.md) de una entidad).
3. **Pruebas de Extremo a Extremo (*End-to-End / E2E Tests*):** validan flujos de negocio completos desde la perspectiva del usuario o cliente de la API.

**Marco Estándar `unittest` frente a `pytest`.**
- **`unittest` (Biblioteca Estándar):**
  - Orientado a objetos: las pruebas heredan de `unittest.TestCase`.
  - Aserciones mediante métodos dedicados: `self.assertEqual(a, b)`, `self.assertTrue(x)`, `self.assertRaises(ValueError)`.
  - Ciclo de vida con métodos `setUp()` (preparación previa a cada test) y `tearDown()` (limpieza posterior incondicional).
- **`pytest` (Estándar Moderno de la Industria):**
  - Orientado a funciones: las pruebas son simples funciones que inician con el prefijo `test_`.
  - Aserción nativa `assert a == b`: `pytest` reescribe el AST de la sentencia `assert` para mostrar una introspección detallada de las variables que causaron el fallo.
  - Fixtures declarativas con inyección de dependencias (`@pytest.fixture`).

**Aislamiento y Dobles de Prueba con `unittest.mock`.**
Para que una prueba unitaria sea rápida y determinista, no debe realizar peticiones HTTP reales ni modificar bases de datos productivas. El módulo `unittest.mock` permite sustituir colaboradores externos:
- **`Mock` y `MagicMock`:** objetos simulados que aceptan cualquier invocación o atributo, registran los argumentos recibidos (`assert_called_once_with(...)`) y devuelven valores predeterminados o configurados (`mock.return_value = 200`).
- **`patch()`:** decorador o gestor de contexto que reemplaza temporalmente un objeto o función en el módulo importado durante la prueba y lo restaura incondicionalmente al finalizar.

**Depuración Interactiva con `breakpoint()` (PEP 553) y `pdb`.**
A partir de Python 3.7, la función integrada `breakpoint()` invoca el depurador estándar de Python (`pdb`) pausando la ejecución en ese punto exacto e interactuando en la consola:
- `n` (*next*): avanza a la siguiente línea del código en el marco actual.
- `s` (*step*): ingresa dentro de la función que se está invocando (*step into*).
- `c` (*continue*): reanuda la ejecución normal hasta el siguiente punto de interrupción.
- `p variable` (*print*): evalúa e imprime el valor de una variable o expresión.
- `l` (*list*): muestra el código fuente circundante al punto actual.
- `q` (*quit*): aborta inmediatamente la ejecución del programa.

## 4. Sintaxis y funcionamiento

Estructura de prueba con `unittest.TestCase`:

```python
import unittest


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("División por cero")
    return a / b


class TestOperaciones(unittest.TestCase):
    def setUp(self) -> None:
        # Preparación previa a cada método de prueba
        self.dividendo = 10.0

    def test_division_exitosa(self) -> None:
        resultado = dividir(self.dividendo, 2.0)
        self.assertEqual(resultado, 5.0)

    def test_division_por_cero_lanza_excepcion(self) -> None:
        with self.assertRaises(ValueError):
            dividir(self.dividendo, 0.0)
```

Estructura de prueba moderna y parametrizada con `pytest`:

```python
# Con pytest:
# pip install pytest
# Ejecutar: pytest tests/

# import pytest
# @pytest.mark.parametrize("entrada, esperado", [
#     (2, 4),
#     (3, 9),
#     (4, 16),
# ])
# def test_cuadrados(entrada: int, esperado: int) -> None:
#     assert entrada ** 2 == esperado
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Suite de pruebas unitarias completa con `unittest`: aserciones de valor, excepciones y ciclo de vida.**

```python
import unittest


class BilleteraDigital:
    def __init__(self, saldo_inicial: float = 0.0) -> None:
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    def recargar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto de recarga debe ser estrictamente positivo")
        self._saldo += monto

    def debitar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto a debitar debe ser positivo")
        if monto > self._saldo:
            raise RuntimeError("Saldo insuficiente para completar la operación")
        self._saldo -= monto


class TestBilleteraDigital(unittest.TestCase):
    def setUp(self) -> None:
        """Se ejecuta antes de cada método de test individual."""
        self.billetera = BilleteraDigital(saldo_inicial=100.0)

    def test_saldo_inicial_correcto(self) -> None:
        self.assertEqual(self.billetera.saldo, 100.0)

    def test_recarga_incrementa_saldo(self) -> None:
        self.billetera.recargar(50.0)
        self.assertEqual(self.billetera.saldo, 150.0)

    def test_debito_valido_descuenta_saldo(self) -> None:
        self.billetera.debitar(40.0)
        self.assertEqual(self.billetera.saldo, 60.0)

    def test_saldo_inicial_negativo_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            BilleteraDigital(saldo_inicial=-10.0)

    def test_debito_excedente_lanza_runtime_error(self) -> None:
        with self.assertRaises(RuntimeError) as contexto:
            self.billetera.debitar(150.0)
        self.assertIn("Saldo insuficiente", str(contexto.exception))


# Ejecución programática del runner de unittest
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBilleteraDigital)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    print("\nPruebas exitosas:", resultado.wasSuccessful())
```

Explicación paso a paso:

- `setUp()` instancia una `BilleteraDigital` limpia con saldo de \$100 antes de cada prueba, asegurando que los métodos de test no compartan estado ni dependan del orden de ejecución.
- `self.assertEqual` verifica que la mutación numérica sea exacta.
- `with self.assertRaises(RuntimeError) as contexto:` valida que el sistema lance la excepción correcta ante saldos insuficientes e inspecciona el mensaje semántico de error con `assertIn`.
- El runner de `unittest` ejecuta los 5 métodos de prueba de forma determinista y reporta estadísticas de éxito.

Resultado esperado:

```text
test_debito_excedente_lanza_runtime_error (__main__.TestBilleteraDigital) ... ok
test_debito_valido_descuenta_saldo (__main__.TestBilleteraDigital) ... ok
test_recarga_incrementa_saldo (__main__.TestBilleteraDigital) ... ok
test_saldo_inicial_correcto (__main__.TestBilleteraDigital) ... ok
test_saldo_inicial_negativo_lanza_value_error (__main__.TestBilleteraDigital) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK

Pruebas exitosas: True
```

### Intermedio

**Ejemplo 2 — Aislamiento de servicios externos mediante dobles de prueba con `unittest.mock.patch` y verificación de contratos.**

```python
from dataclasses import dataclass
import unittest
from unittest.mock import MagicMock, patch


@dataclass(frozen=True)
class RespuestaNotificacion:
    mensaje_id: str
    entregado: bool


class ClienteServicioSMS:
    """Cliente que interactúa con una pasarela externa de telecomunicaciones."""

    def enviar_sms(self, telefono: str, mensaje: str) -> RespuestaNotificacion:
        # En producción realizaría una petición HTTP de red al proveedor (Twilio, AWS SNS)
        raise NotImplementedError("Llamada real a red externa no permitida en tests")


class GestorAutenticacion:
    """Servicio de dominio que genera códigos OTP y los envía vía SMS."""

    def __init__(self, cliente_sms: ClienteServicioSMS) -> None:
        self.cliente_sms = cliente_sms

    def enviar_codigo_seguridad(self, telefono: str, codigo: str) -> bool:
        if len(codigo) != 6:
            raise ValueError("El código de verificación debe tener exactamente 6 caracteres")

        mensaje = f"Su código de acceso temporal es: {codigo}"
        respuesta = self.cliente_sms.enviar_sms(telefono=telefono, mensaje=mensaje)
        return respuesta.entregado


class TestGestorAutenticacion(unittest.TestCase):
    def test_enviar_codigo_exitoso_con_mock_inyectado(self) -> None:
        # 1. Crear un mock que simula el cliente externo
        mock_cliente_sms = MagicMock(spec=ClienteServicioSMS)
        mock_cliente_sms.enviar_sms.return_value = RespuestaNotificacion(
            mensaje_id="msg_9988", entregado=True
        )

        # 2. Instanciar el servicio inyectando el mock (Principio DIP)
        gestor = GestorAutenticacion(cliente_sms=mock_cliente_sms)
        resultado = gestor.enviar_codigo_seguridad("+54911223344", "458921")

        # 3. Aserciones sobre el resultado y sobre la interacción con el mock
        self.assertTrue(resultado)
        mock_cliente_sms.enviar_sms.assert_called_once_with(
            telefono="+54911223344",
            mensaje="Su código de acceso temporal es: 458921",
        )

    def test_codigo_invalido_no_invoca_servicio_sms(self) -> None:
        mock_cliente_sms = MagicMock(spec=ClienteServicioSMS)
        gestor = GestorAutenticacion(cliente_sms=mock_cliente_sms)

        with self.assertRaises(ValueError):
            gestor.enviar_codigo_seguridad("+54911223344", "12")  # Código corto

        # Asegurar que no se envió ningún mensaje ni se consumieron créditos
        mock_cliente_sms.enviar_sms.assert_not_called()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGestorAutenticacion)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```

Explicación técnica:

- `MagicMock(spec=ClienteServicioSMS)` crea un doble de prueba que simula la interfaz exacta de `ClienteServicioSMS`. Si el código de producción intenta invocar un método inexistente sobre el mock, fallará inmediatamente.
- `mock.return_value` define qué debe responder el servicio falso sin tocar la red física.
- `mock_cliente_sms.enviar_sms.assert_called_once_with(...)` valida el contrato conductual: verifica no solo que se llamó al servicio, sino que se invocó exactamente una vez y con los argumentos exactos esperados.
- En el segundo test, se constata que ante un código inválido (`"12"`), la validación defensiva detiene el flujo antes de invocar al proveedor (`assert_not_called()`), ahorrando costos en APIs de pago.

Resultado esperado:

```text
test_codigo_invalido_no_invoca_servicio_sms (__main__.TestGestorAutenticacion) ... ok
test_enviar_codigo_exitoso_con_mock_inyectado (__main__.TestGestorAutenticacion) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

### Avanzado

**Ejemplo 3 — Sistema de Fixtures modulares, pruebas de persistencia con directorios temporales seguros y simulación de fallos.**

```python
import os
import tempfile
import unittest
from pathlib import Path


class RepositorioArchivosSeguro:
    """Gestiona la persistencia de reportes en disco."""

    def __init__(self, directorio_base: Path) -> None:
        self.directorio_base = directorio_base

    def escribir_reporte(self, nombre_archivo: str, contenido: str) -> Path:
        if not nombre_archivo.endswith(".txt"):
            raise ValueError("Solo se admiten extensiones .txt")
        ruta_completa = self.directorio_base / nombre_archivo
        ruta_completa.write_text(contenido, encoding="utf-8")
        return ruta_completa

    def leer_reporte(self, nombre_archivo: str) -> str:
        ruta = self.directorio_base / nombre_archivo
        if not ruta.is_file():
            raise FileNotFoundError(f"El reporte {nombre_archivo} no existe")
        return ruta.read_text(encoding="utf-8")


class TestPersistenciaArchivos(unittest.TestCase):
    def setUp(self) -> None:
        # Fixture de aislamiento: crear un directorio temporal seguro del sistema
        self.temp_dir_context = tempfile.TemporaryDirectory()
        self.directorio_prueba = Path(self.temp_dir_context.name)
        self.repo = RepositorioArchivosSeguro(self.directorio_prueba)

    def tearDown(self) -> None:
        # Limpieza determinista incondicional: eliminar el directorio temporal tras cada test
        self.temp_dir_context.cleanup()

    def test_escribir_y_leer_reporte_exitoso(self) -> None:
        nombre = "auditoria_2025.txt"
        contenido = "Resumen de operaciones: Todo correcto."

        ruta_creada = self.repo.escribir_reporte(nombre, contenido)

        # 1. Verificar que el archivo existe físicamente en el disco temporal
        self.assertTrue(ruta_creada.is_file())
        # 2. Verificar que el contenido leído coincide exactamente
        recuperado = self.repo.leer_reporte(nombre)
        self.assertEqual(recuperado, contenido)

    def test_extension_invalida_lanza_error_sin_crear_archivo(self) -> None:
        with self.assertRaises(ValueError):
            self.repo.escribir_reporte("archivo_malicioso.exe", "codigo peligroso")

        # Asegurar que no se creó ningún archivo espurio en el directorio
        archivos_en_directorio = list(self.directorio_prueba.iterdir())
        self.assertEqual(len(archivos_en_directorio), 0)

    def test_leer_archivo_inexistente_lanza_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.repo.leer_reporte("inexistente.txt")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPersistenciaArchivos)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```

Explicación de ingeniería:

- El par `setUp()` / `tearDown()` implementa el ciclo de vida clásico de fixtures: cada test se ejecuta en una carpeta temporal totalmente nueva y aislada generada por `tempfile.TemporaryDirectory()`.
- Al finalizar cada test (incluso si la prueba falla por aserción), `tearDown()` invoca `cleanup()`, destruyendo todos los archivos generados en disco para no dejar basura residual en el sistema de archivos ni interferir con pruebas subsiguientes.
- Se valida la robustez del repositorio ante extensiones inválidas, verificando además el estado del sistema de archivos (`len(archivos) == 0`).

Resultado esperado:

```text
test_escribir_y_leer_reporte_exitoso (__main__.TestPersistenciaArchivos) ... ok
test_extension_invalida_lanza_error_sin_crear_archivo (__main__.TestPersistenciaArchivos) ... ok
test_leer_archivo_inexistente_lanza_file_not_found (__main__.TestPersistenciaArchivos) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.003s

OK
```

## 6. Aplicaciones en el mundo real

- **Pipelines de Integración y Entrega Continua (CI/CD):** ejecución obligatoria de pruebas en cada *Pull Request* antes de permitir la fusión a la rama de producción (`main`).
- **Desarrollo Guiado por Pruebas (*Test-Driven Development*, TDD):** metodología donde las pruebas se escriben antes del código de producción (Ciclo Red-Green-Refactor).
- **Prevención de Regresiones en Sistemas Financieros:** auditoría de cálculos de balances, impuestos y redondeos decimales para asegurar que ninguna modificación viole las reglas contables.
- **Auditoría de Seguridad y Pruebas de Límites (*Edge Cases*):** verificación de que caracteres inesperados, valores nulos o inyecciones no deseadas sean rechazados limpiamente por las validaciones defensivas.

## 7. Uso en producción

- **Seguir los principios F.I.R.S.T. para pruebas unitarias:**
  - **F** (*Fast*): las pruebas unitarias deben ejecutarse en pocos segundos; pruebas lentas desincentivan su ejecución frecuente.
  - **I** (*Independent*): ningún test debe depender del resultado o del estado dejado por una prueba anterior.
  - **R** (*Repeatable*): una prueba debe arrojar el mismo resultado en cualquier entorno (local, Docker, servidor de CI) sin importar la hora o la fecha.
  - **S** (*Self-validating*): la prueba debe informar claramente si pasó o falló mediante un booleano sin requerir interpretación humana de logs.
  - **T** (*Timely*): deben escribirse en conjunto con el código de producción.
- **Parchear dónde se utiliza el objeto, no dónde se define (*Where to patch*):** al usar `unittest.mock.patch('paquete.modulo.Cliente')`, especificar la ruta donde el objeto es **importado y consumido**, no el archivo original donde fue declarado.
- **Mantener los tests libres de lógica condicional compleja:** un test no debe contener bucles intrincados ni bloques `if/else` profundos; el código de prueba debe ser directo, lineal y evidente para que la propia prueba no requiera sus propias pruebas.
- **Controlar la cobertura de código (*Code Coverage*) con cautela:** apuntar a una cobertura razonable (80 % - 90 %) con `coverage.py`, recordando que una alta cobertura de líneas no garantiza por sí sola que se hayan probado todos los casos de borde semánticos.

## 8. Errores comunes y recomendaciones

1. **Parchear la ruta equivocada con `unittest.mock.patch` (*The Where-to-Patch Trap*).**

```python
# Si en mi_servicio.py escribiste:
# from datetime import datetime

# ERROR: parchear datetime.datetime no afectará a mi_servicio.py si ya fue importado
# @patch('datetime.datetime.now')  # Incorrecto

# CORRECCIÓN: parchear el nombre dentro del espacio de nombres que lo consume:
# @patch('mi_servicio.datetime')   # Correcto
```

Diagnóstico: Python resuelve las importaciones enlazando referencias al espacio de nombres local del módulo que las importa. Parchear el módulo original no altera la referencia local ya enlazada en el módulo de destino. Recomendación: aplicar la regla canónica de Mocking: *"Patch where the object is looked up, not where it is defined"*.

2. **Compartir estado mutable entre tests sin limpieza en `tearDown` o fixtures.**

```python
# ANTIPATRÓN: lista global compartida entre métodos de test
import unittest

registros_globales = []


class TestContaminado(unittest.TestCase):
    def test_a(self):
        registros_globales.append(1)
        self.assertEqual(len(registros_globales), 1)

    def test_b(self):
        # Fallará si test_a corrió antes: registros_globales tendrá longitud 1 o más!
        self.assertEqual(len(registros_globales), 0)
```

Diagnóstico: la contaminación del estado global rompe la independencia de las pruebas. Si el orden de ejecución cambia o se ejecutan en paralelo, las pruebas comenzarán a fallar de forma intermitente (*flaky tests*). Recomendación: inicializar el estado dentro de `setUp()` o utilizar fixtures con ámbito por función.

3. **Dejar llamadas a `breakpoint()` o `pdb.set_trace()` en el código de producción.**

Diagnóstico: si un proceso desatendido en el servidor de producción alcanza una instrucción `breakpoint()`, detendrá el proceso esperando entrada del teclado en una terminal que nadie está mirando, congelando el servicio web. Recomendación: configurar reglas de linter en CI (como Ruff o Flake8) que rechacen confirmaciones (*commits*) que contengan llamadas a `breakpoint()`.

## 9. Resumen

- Las **pruebas automatizadas** son el pilar de la confiabilidad del software, estructuradas en la pirámide de testing (unitarias, de integración y extremo a extremo).
- El marco estándar **`unittest`** organiza pruebas en clases derivadas de `TestCase`, implementando el ciclo de vida `setUp()` / `tearDown()` y aserciones rigurosas.
- El marco moderno **`pytest`** simplifica la sintaxis utilizando sentencias `assert` directas y un sistema potente de fixtures modulares.
- El módulo **`unittest.mock`** (`Mock`, `MagicMock`, `@patch`) aísla el código bajo prueba reemplazando dependencias de red, bases de datos o reloj del sistema.
- La función integrada **`breakpoint()`** (**PEP 553**) invoca interactivamente el depurador estándar **`pdb`** para análisis y resolución de defectos paso a paso en tiempo de desarrollo.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/unittest.html> — Biblioteca estándar (`unittest`): marco de pruebas unitarias, TestCase, suites y runners.
- <https://docs.python.org/3/library/unittest.mock.html> — Biblioteca estándar (`unittest.mock`): objetos simulados, decoradores `patch` y verificación de llamadas.
- <https://docs.python.org/3/library/pdb.html> — Biblioteca estándar (`pdb`): depurador interactivo de Python y catálogo completo de comandos.
- <https://peps.python.org/pep-0553/> — PEP 553 (*Built-in breakpoint()*): especificación de la función integrada de punto de interrupción.
