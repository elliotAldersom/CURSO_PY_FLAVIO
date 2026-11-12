# Módulos, Sistema de Importación y Espacios de Nombres en Python

## 2. Introducción

Cuando una aplicación crece más allá de un único guion, concentrar constantes, [funciones](../chapter-two/funciones.md) y [clases](../chapter-five/clases_y_objetos.md) en un solo archivo deteriora la legibilidad, multiplica las colisiones de identificadores en el espacio de nombres global e impide reutilizar componentes entre distintos programas.

Un **módulo** en Python es la unidad fundamental de organización y reutilización de código: físicamente suele corresponder a un archivo con extensión `.py` (o a una extensión compilada), y en tiempo de ejecución se materializa como un objeto de tipo `module` con su propio diccionario de atributos, aislado del resto del sistema.

Comprender con rigor la arquitectura de módulos y el sistema de importación resuelve cuatro problemas centrales de ingeniería de software:

1. **Aislamiento de espacios de nombres (*namespaces*):** cada módulo posee su propio [ámbito global](../chapter-two/ambito_variables.md), de modo que dos módulos distintos pueden definir funciones homónimas —como `Saludar()` en `Modulo_Saludar.py` y `Saludo()` en `saludar.py`— sin sobrescribirse mutuamente.
2. **Ejecución controlada frente a reutilización:** distinguir cuándo un archivo actúa como punto de entrada principal (`__name__ == "__main__"`, aplicado en `Decoradores_Clases.py` L57) y cuándo se importa como biblioteca evita efectos secundarios indeseados durante la carga, como las lecturas interactivas en el nivel superior de `division.py` (L28).
3. **Resolución determinista de dependencias:** conocer el orden exacto en que el intérprete consulta `sys.modules`, `sys.builtin_module_names` y `sys.path` permite diagnosticar conflictos de nombres y sustituir rutas locales frágiles (`sys.path.append("C:\\Users\\...")` en `MODULOS_TWO.py` L37) por mecanismos reproducibles.
4. **Extensibilidad modular:** cargar módulos de la biblioteca estándar (como `abc` en `Abastraccion.py` L135), bibliotecas de terceros o módulos de dominio propios sustenta arquitecturas desacopladas alineadas con los [principios SOLID](../../Avanzado/chapter-two/principios_solid.md) y la organización jerárquica en [paquetes](paquetes.md).

## 3. Fundamentos y conceptos

**El módulo como archivo fuente y como objeto en memoria.** Desde el punto de vista del sistema de archivos, un módulo propio es cualquier archivo `.py` cuyo nombre base (sin la extensión) actúa como identificador del módulo. Durante la ejecución, al importarse por primera vez, Python crea una instancia de `types.ModuleType` (`<class 'module'>`, verificada con `type(...)` en `MÓDULOS.py` L69), ejecuta secuencialmente todas las sentencias del nivel superior del archivo y almacena cada variable, función o clase definida dentro del diccionario interno `modulo.__dict__`.

**Comportamiento *singleton* y caché en `sys.modules`.** En un mismo proceso de Python, un módulo se carga y ejecuta **una única vez**. Antes de buscar archivos en disco, la sentencia `import` consulta el diccionario global `sys.modules`, que asocia nombres calificados de módulos con sus objetos `module` ya inicializados:

- Si el nombre ya existe en `sys.modules`, Python reutiliza inmediatamente la referencia en memoria con costo $O(1)$, sin releer ni reejecutar el archivo `.py`.
- Si no existe, el motor de importación (`importlib`) localiza el módulo, registra el objeto en `sys.modules` y ejecuta su cuerpo. Si se necesita forzar explícitamente una recarga en una sesión interactiva de depuración, debe emplearse `importlib.reload(modulo)`.

**Clasificación técnica de los módulos según su origen.** Ampliando con precisión la taxonomía introducida en `MÓDULOS.py` (L14-25), conviene distinguir cuatro categorías:

1. **Módulos integrados en el intérprete (*built-in modules*):** en la implementación de referencia **CPython**, son módulos escritos en C y enlazados directamente dentro del ejecutable del intérprete (por ejemplo, `sys`, `builtins`, `_io`, `time` según la plataforma). Sus nombres figuran en la tupla `sys.builtin_module_names` (`MODULOS_TWO.py` L12).
2. **Biblioteca estándar (*standard library*):** colección extensa de módulos y paquetes distribuidos oficialmente junto con Python —algunos escritos en Python puro (`pathlib`, `abc`, `importlib`) y otros respaldados por extensiones en C (`csv` sobre `_csv`, `math`)— disponibles sin instalar dependencias externas.
3. **Módulos y paquetes de terceros (*third-party*):** distribuciones externas publicadas en índices como PyPI e instaladas en el directorio `site-packages` de un entorno virtual mediante gestores como `pip` o `uv`.
4. **Módulos propios de la aplicación (*first-party*):** archivos `.py` creados dentro del proyecto para modelar reglas de negocio, utilidades e infraestructura.

**Modalidades de importación e impacto en el espacio de nombres.** El sistema de importación ofrece cuatro formas sintácticas principales (`MÓDULOS.py` L26-50):

- `import modulo`: enlaza únicamente el nombre `modulo` en el espacio de nombres actual. Exige acceso calificado (`modulo.funcion()`), lo que maximiza la claridad sobre el origen de cada símbolo en archivos extensos.
- `import modulo as alias`: enlaza el objeto módulo a un identificador local alternativo, útil para abreviar nombres largos o evitar colisiones con variables locales.
- `from modulo import simbolo [as alias]`: carga el módulo completo en `sys.modules` (si aún no estaba cargado) y copia en el espacio de nombres actual una referencia directa al atributo solicitado (`MODULOS.py` L1, `MÓDULOS.py` L87). Es importante recordar que enlaza la referencia actual del objeto: reasignar esa variable localmente no altera el atributo dentro del módulo original.
- `from modulo import *` (*importación comodín*): copia en el ámbito actual todos los nombres públicos del módulo (todos aquellos que no comienzan con `_`, o bien únicamente los listados en la secuencia `__all__` si el módulo la define). Como señala acertadamente `MÓDULOS.py` (L45), se desaconseja en código de aplicación porque contamina el espacio de nombres local, puede sobrescribir silenciosamente funciones previamente definidas e impide a lectores y analizadores estáticos rastrear de dónde proviene cada identificador.

**El atributo `__name__` y la guarda `if __name__ == "__main__":`.** Todo módulo posee el atributo especial `__name__` (`MÓDULOS.py` L116-119):

- Cuando el archivo se pasa directamente al intérprete como punto de entrada (`python archivo.py`), Python asigna a su atributo `__name__` la cadena literal `"__main__"`.
- Cuando ese mismo archivo es importado desde otro módulo (`import paquete.archivo`), su `__name__` contiene su nombre calificado real (`"paquete.archivo"`).

Cualquier instrucción situada en el nivel superior fuera de funciones o clases se ejecuta de inmediato al importar el módulo. En `DIVISION/division.py` (L28), la sentencia `numero_A = primer_valor()` está en el nivel superior: si otro archivo intenta importar únicamente la función `Division`, la importación quedará bloqueada esperando `input()` por consola. Proteger el código demostrativo o interactivo bajo `if __name__ == "__main__":` —tal como hace `Decoradores_Clases.py` (L57-62)— permite que un mismo archivo sea simultáneamente ejecutable como guion autónomo e importable limpiamente como biblioteca.

**Orden de búsqueda y resolución de módulos.** Cuando se ejecuta `import nombre`, el mecanismo estándar de **CPython** resuelve el identificador siguiendo esta secuencia estricta:

1. **Caché de sesión (`sys.modules`):** verifica si `nombre` ya fue cargado previamente en memoria.
2. **Buscadores de `sys.meta_path`:** consulta en orden los buscadores registrados:
   - `BuiltinImporter`: comprueba si `nombre` pertenece a `sys.builtin_module_names`. Tal como advierte `MODULOS_TWO.py` (L14-20), si se crea un archivo propio llamado `sys.py`, el módulo integrado en C tiene prioridad absoluta y el archivo local jamás será importado como `sys`.
   - `FrozenImporter`: localiza módulos congelados internamente por el intérprete.
   - `PathFinder`: recorre secuencialmente las rutas listadas en `sys.path` buscando un paquete o archivo `.py` / extensión compilada coincidente.
3. **Lista de rutas `sys.path`:** se inicializa al arrancar el intérprete con: (a) el directorio del guion ejecutado (o `""`, el directorio actual, al usar el intérprete interactivo o `python -m`), (b) las rutas definidas en la variable de entorno `PYTHONPATH` (si existe), (c) los directorios de la biblioteca estándar y (d) el directorio `site-packages` del entorno activo.

**Caché de *bytecode* en CPython (`__pycache__`).** En **CPython**, al importar un módulo `.py`, el intérprete compila su código fuente a instrucciones de *bytecode* y guarda el resultado en el subdirectorio `__pycache__/<nombre>.cpython-<XY>.pyc` (donde `<XY>` indica la versión mayor y menor, como `cpython-313.pyc`). Este mecanismo es un detalle de implementación de CPython: **no acelera la velocidad de ejecución de los algoritmos**, sino únicamente el tiempo de arranque e importación posterior al evitar recompilar el código fuente mientras su fecha de modificación y tamaño no hayan cambiado.

**Importaciones circulares y convenciones PEP 8 para nombres de archivo.** Una **importación circular** ocurre cuando el módulo `A` importa al módulo `B` en su encabezado y `B`, a su vez, intenta importar un símbolo de `A` antes de que `A` haya terminado de ejecutar su definición, provocando `ImportError: cannot import name '...' from partially initialized module '...'`. Se resuelve extrayendo las definiciones compartidas a un tercer módulo base o difiriendo la importación dentro de la función que la requiere. Finalmente, **PEP 8** establece que los nombres de módulos deben ser cortos, descriptivos y escritos exclusivamente en **minúsculas ASCII** con guiones bajos opcionales (`modulo_saludar.py`), evitando mayúsculas, espacios y tildes (`MÓDULOS.py`, `MÓDULO_SALUDAR.py`), ya que las diferencias de sensibilidad a mayúsculas y de normalización Unicode entre Windows, Linux y macOS generan fallos de importación difíciles de depurar.

## 4. Sintaxis y funcionamiento

Formas canónicas de importación, introspección y protección de ejecución:

```text
import <modulo>
import <modulo> as <alias>
from <modulo> import <nombre_1>, <nombre_2> as <alias_2>

if __name__ == "__main__":
    <instrucciones_exclusivas_de_ejecucion_directa>
```

Elementos clave del sistema de módulos e importación:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `import m` | Carga `m` (si no está en caché) y enlaza el objeto módulo `m` | `import math` → `math.sqrt(16)` |
| 2 | `import m as a` | Carga `m` y lo enlaza localmente con el alias `a` | `import datetime as dt` |
| 3 | `from m import x` | Enlaza directamente el atributo `x` de `m` en el ámbito actual | `from abc import ABC` |
| 4 | `from m import *` | Importa nombres públicos o listados en `__all__` (no recomendado) | `from math import *` |
| 5 | `__name__` | Cadena con `"__main__"` al ejecutar directo o el nombre del módulo al importar | `if __name__ == "__main__":` |
| 6 | `__file__` | Ruta en disco desde la cual se cargó el módulo (ausente en *built-ins* C) | `print(modulo.__file__)` |
| 7 | `__all__` | Lista de cadenas que define la interfaz pública para `import *` | `__all__ = ["saludar"]` |
| 8 | `dir(m)` | Lista ordenada de nombres de atributos definidos en el módulo `m` | ` [n for n in dir(m) if not n.startswith("_")]` |
| 9 | `sys.modules` | Diccionario caché global de módulos ya cargados en el proceso | `"sys" in sys.modules` |
| 10 | `sys.builtin_module_names` | Tupla de módulos compilados dentro del binario del intérprete | `"sys" in sys.builtin_module_names` |
| 11 | `sys.path` | Lista mutable de directorios donde `PathFinder` busca módulos y paquetes | `python -m paquete.modulo` |
| 12 | `importlib.import_module` | Función estándar para importar módulos dinámicamente a partir de un `str` | `importlib.import_module("json")` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación de un módulo reutilizable, variantes de `import` y guarda `__name__ == "__main__"`.**

```python
import sys
import tempfile
from pathlib import Path

CODIGO_MODULO = '''"""Módulo de utilidades de facturación."""

TASA_IMPUESTO = 0.18


def calcular_subtotal(precio_unitario: float, cantidad: int) -> float:
    return round(precio_unitario * cantidad, 2)


def aplicar_impuesto(monto: float, tasa: float = TASA_IMPUESTO) -> float:
    return round(monto * (1 + tasa), 2)


if __name__ == "__main__":
    print("Ejecución directa de prueba interna")
'''

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta_modulo = Path(tmp_dir) / "facturacion_util.py"
    ruta_modulo.write_text(CODIGO_MODULO, encoding="utf-8")

    sys.path.insert(0, tmp_dir)
    try:
        import facturacion_util as fact
        from facturacion_util import calcular_subtotal as subtotal

        monto_base = subtotal(25.50, 4)
        monto_final = fact.aplicar_impuesto(monto_base)

        print("Tipo de objeto:", type(fact))
        print("Nombre del módulo importado:", fact.__name__)
        print(f"Subtotal: {monto_base:.2f} | Total con impuesto: {monto_final:.2f}")
    finally:
        sys.path.remove(tmp_dir)
        sys.modules.pop("facturacion_util", None)
```

Explicación paso a paso:

- Se escribe en un directorio temporal el módulo `facturacion_util.py` siguiendo las convenciones de nombres en minúsculas ASCII de PEP 8 y aislando su mensaje de prueba bajo `if __name__ == "__main__":`.
- Al importar `facturacion_util`, el mensaje `"Ejecución directa de prueba interna"` **no** se imprime porque `fact.__name__` toma el valor `"facturacion_util"` en lugar de `"__main__"`.
- Se combinan `import ... as fact` y `from ... import calcular_subtotal as subtotal`, verificando que `fact` es una instancia de `<class 'module'>`.

Resultado esperado:

```text
Tipo de objeto: <class 'module'>
Nombre del módulo importado: facturacion_util
Subtotal: 102.00 | Total con impuesto: 120.36
```

### Intermedio

**Ejemplo 2 — Verificación del caché *singleton* en `sys.modules` y prioridad de `sys.builtin_module_names`.**

```python
import sys
import tempfile
from pathlib import Path

CODIGO_CONTADOR = '''contador_cargas = 0
contador_cargas += 1
registro = []
'''

with tempfile.TemporaryDirectory() as tmp_dir:
    (Path(tmp_dir) / "estado_sesion.py").write_text(CODIGO_CONTADOR, encoding="utf-8")
    (Path(tmp_dir) / "sys.py").write_text("VERSION_FALSA = 999\n", encoding="utf-8")

    sys.path.insert(0, tmp_dir)
    try:
        import estado_sesion as ref_a
        ref_a.registro.append("evento_1")

        import estado_sesion as ref_b
        from estado_sesion import registro as lista_compartida

        print("Mismo objeto en memoria:", ref_a is ref_b)
        print("Veces ejecutado el módulo:", ref_b.contador_cargas)
        print("Estado compartido:", lista_compartida)
        print("Registrado en sys.modules:", "estado_sesion" in sys.modules)
        print("'sys' es módulo integrado:", "sys" in sys.builtin_module_names)
        print("Archivo sys.py local ignorado:", not hasattr(sys, "VERSION_FALSA"))
    finally:
        sys.path.remove(tmp_dir)
        sys.modules.pop("estado_sesion", None)
```

Explicación técnica:

- Aunque `estado_sesion` se importa tres veces con distintas sintaxis, su cuerpo superior solo se ejecuta una vez (`contador_cargas` permanece en `1`) y tanto `ref_a` como `ref_b` apuntan exactamente al mismo objeto en `sys.modules`.
- Aunque existe un archivo `sys.py` en la primera posición de `sys.path`, `BuiltinImporter` actúa antes que `PathFinder` y conserva el módulo nativo `sys`, confirmando experimentalmente el principio expuesto en `MODULOS_TWO.py` (L14-20).

Resultado esperado:

```text
Mismo objeto en memoria: True
Veces ejecutado el módulo: 1
Estado compartido: ['evento_1']
Registrado en sys.modules: True
'sys' es módulo integrado: True
Archivo sys.py local ignorado: True
```

### Avanzado

**Ejemplo 3 — Carga dinámica de estrategias con `importlib.import_module` y control de API pública (`__all__`).**

```python
import importlib
import sys
import tempfile
from pathlib import Path

MODULO_PE = '''__all__ = ["calcular_total"]
_FACTOR_INTERNO = 0.18


def calcular_total(neto: float) -> float:
    return round(neto * (1 + _FACTOR_INTERNO), 2)
'''

MODULO_ES = '''__all__ = ["calcular_total"]
_FACTOR_INTERNO = 0.21


def calcular_total(neto: float) -> float:
    return round(neto * (1 + _FACTOR_INTERNO), 2)
'''

with tempfile.TemporaryDirectory() as tmp_dir:
    base = Path(tmp_dir)
    (base / "impuesto_pe.py").write_text(MODULO_PE, encoding="utf-8")
    (base / "impuesto_es.py").write_text(MODULO_ES, encoding="utf-8")

    sys.path.insert(0, tmp_dir)
    try:
        for codigo_pais in ("pe", "es"):
            nombre_modulo = f"impuesto_{codigo_pais}"
            estrategia = importlib.import_module(nombre_modulo)
            total = estrategia.calcular_total(200.0)
            print(f"[{codigo_pais.upper()}] API pública={estrategia.__all__} -> Total: {total:.2f}")
    finally:
        sys.path.remove(tmp_dir)
        sys.modules.pop("impuesto_pe", None)
        sys.modules.pop("impuesto_es", None)
```

Explicación de arquitectura:

- En lugar de encadenar condicionales rígidos cada vez que se añade una jurisdicción fiscal, `importlib.import_module` resuelve en tiempo de ejecución el módulo correspondiente a partir de un identificador de configuración, respetando el principio abierto/cerrado estudiado en `OCP.py`.
- El prefijo de guion bajo en `_FACTOR_INTERNO` y la declaración explícita de `__all__` delimitan con claridad qué símbolos forman parte del contrato público del módulo.

Resultado esperado:

```text
[PE] API pública=['calcular_total'] -> Total: 236.00
[ES] API pública=['calcular_total'] -> Total: 242.00
```

## 6. Aplicaciones en el mundo real

- **Separación por capas en servicios *backend*:** dividir controladores HTTP, casos de uso de negocio, validadores y adaptadores de persistencia en módulos independientes para mantener responsabilidades acotadas y facilitar pruebas unitarias aisladas.
- **Módulos de configuración y constantes de dominio:** centralizar códigos de error, tasas, expresiones de validación o esquemas en un módulo único importado por todo el proyecto, evitando valores literales dispersos.
- **Sistemas de *plugins* y conectores extensibles:** herramientas como `pytest`, Django o marcos ETL descubren y cargan conectores dinámicamente mediante `importlib.import_module()` según archivos de configuración.
- **Guiones híbridos de línea de comandos y biblioteca:** utilidades de automatización que exponen funciones puras importables por otros módulos y, al mismo tiempo, ofrecen una interfaz CLI bajo `if __name__ == "__main__":`.

## 7. Uso en producción

- **Sustituir `sys.path.append(...)` por ejecución modular o instalación editable:** insertar rutas absolutas dependientes de la máquina local como `sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")` (`MODULOS_TWO.py` L37, `PAQUETE.py` L50) rompe la aplicación en cuanto se despliega en Linux, en un contenedor Docker o en el equipo de otro desarrollador. En entornos profesionales se ejecuta desde la raíz del repositorio con `python -m paquete.modulo` o se declara un archivo `pyproject.toml` instalando el proyecto en el entorno virtual mediante `pip install -e .`.
- **Mantener la importación libre de efectos secundarios pesados:** un módulo nunca debe abrir conexiones de red, ejecutar consultas costosas, modificar archivos ni invocar `input()` (`division.py` L28) en el nivel superior durante `import`. Toda operación de entrada/salida o inicialización costosa debe encapsularse en funciones explícitas o bajo `if __name__ == "__main__":`.
- **Ordenar y agrupar las importaciones conforme a PEP 8:** al inicio de cada archivo, las sentencias `import` se colocan en tres bloques separados por una línea en blanco: (1) biblioteca estándar (`import sys`, `from pathlib import Path`), (2) bibliotecas de terceros (`import pandas as pd`) y (3) módulos propios de la aplicación. Herramientas como `ruff` o `isort` automatizan esta convención en integración continua.
- **No versionar directorios `__pycache__` ni archivos `.pyc`:** dado que los archivos `.pyc` dependen de la versión exacta de CPython, deben excluirse siempre en `.gitignore`. En contenedores inmutables de producción suele definirse `PYTHONDONTWRITEBYTECODE=1` o precompilarse el *bytecode* durante la construcción de la imagen con `python -m compileall`.

## 8. Errores comunes y recomendaciones

1. **Nombrar un archivo propio igual que un módulo de la biblioteca estándar (*module shadowing*).**

```python
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    # Un archivo local llamado 'math.py' oculta el módulo 'math' si PathFinder lo evalúa primero,
    # o en el caso de nombres no integrados como 'random.py' o 'csv.py', sombrea la biblioteca estándar.
    (Path(tmp_dir) / "csv.py").write_text("VALOR = 1\n", encoding="utf-8")
    sys.path.insert(0, tmp_dir)
    try:
        modulo_csv_previo = sys.modules.pop("csv", None)
        import csv as csv_sombreado

        tiene_reader = hasattr(csv_sombreado, "reader")
        print("¿Tiene atributo reader?:", tiene_reader)
    finally:
        sys.path.remove(tmp_dir)
        sys.modules.pop("csv", None)
        if modulo_csv_previo is not None:
            sys.modules["csv"] = modulo_csv_previo
```

Resultado esperado:

```text
¿Tiene atributo reader?: False
```

Diagnóstico: si un guion de práctica se llama `csv.py`, `random.py` o `email.py`, el directorio del guion encabeza `sys.path` y Python importa el archivo del usuario en vez del módulo oficial, lanzando `AttributeError: module 'csv' has no attribute 'reader'` (parcialmente inicializado). Recomendación: usar nombres específicos de dominio (`reporte_csv.py`, `sorteo_clientes.py`) en minúsculas ASCII.

2. **Provocar una importación circular con `from ... import ...` en el nivel superior (`ImportError`).**

```python
# ERROR INTENCIONAL: ImportError por dependencia circular entre dos módulos parcialmente inicializados
# En pedidos.py:
from clientes import validar_cliente

def crear_pedido():
    return validar_cliente()

# En clientes.py:
from pedidos import crear_pedido  # 'pedidos' aún no terminó de definir 'crear_pedido'

def validar_cliente():
    return True
```

Diagnóstico: cuando `pedidos` importa `clientes`, la ejecución de `pedidos` se pausa antes de ejecutar `def crear_pedido():`; al intentar `clientes` hacer `from pedidos import crear_pedido`, el atributo todavía no existe en el objeto módulo `pedidos` registrado en `sys.modules`. Solución: mover la lógica común a un tercer módulo independiente (`validaciones.py`) que no dependa de ninguno de los dos.

3. **Abusar de `from modulo import *` y sobrescribir símbolos silenciosamente.**

```python
from math import sqrt


def calcular(x: float) -> float:
    return sqrt(x)


# Si más abajo se hiciera 'from cmath import *', 'sqrt' pasaría silenciosamente
# a devolver números complejos (4+0j) en lugar de float (4.0).
print("Raíz real controlada:", calcular(16))
```

Resultado esperado:

```text
Raíz real controlada: 4.0
```

Recomendación: importar siempre nombres explícitos (`from math import sqrt`) o calificar mediante el módulo (`cmath.sqrt`), garantizando trazabilidad completa.

4. **Ejecutar código interactivo en el nivel superior sin guarda `__main__`.** Como ocurre en `DIVISION/division.py` (L28), invocar `input()` o funciones de negocio fuera de `if __name__ == "__main__":` impide reutilizar o probar unitariamente las funciones del archivo sin bloquear el proceso.

## 9. Resumen

- Todo archivo `.py` constituye un módulo independiente que en ejecución se instancia una única vez como `<class 'module'>` y queda almacenado en caché dentro de `sys.modules`.
- Python distingue módulos integrados en el intérprete (`sys.builtin_module_names` en CPython), módulos de la biblioteca estándar, distribuciones de terceros y módulos propios.
- Las importaciones explícitas (`import m`, `import m as alias`, `from m import simbolo`) preservan la legibilidad de los espacios de nombres, mientras que `from m import *` debe evitarse en código de producción.
- El atributo `__name__` vale `"__main__"` únicamente cuando el archivo se ejecuta como guion principal; el patrón `if __name__ == "__main__":` aísla el punto de entrada respecto de la carga como biblioteca.
- La resolución de nombres recorre `sys.modules` → `sys.meta_path` (`BuiltinImporter`, `FrozenImporter`, `PathFinder` sobre `sys.path`); en proyectos reales se reemplaza `sys.path.append(...)` por `python -m` o paquetes instalables con `pyproject.toml`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/MÓDULOS.py` (L1-120) | `MÓDULOS.py` | Concepto de módulo `.py`, tipos de módulos, `import`, `import ... as`, `from ... import ... as`, `import *`, `type(...)`, `dir(...)` y `__name__` | Se formalizó el modelo de objeto `module`, el caché *singleton* en `sys.modules`, `__all__` y las reglas de nombres ASCII de PEP 8 frente a nombres con tilde |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/MÓDULO_SALUDAR.py` (L9-18) | `MÓDULO_SALUDAR.py` | Módulo proveedor con funciones puras `saludar(name)` y `despedida(name)` | Se contrastó su diseño libre de efectos laterales al importar frente a módulos acoplados a `input()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/MODULOS.py` (L1-4) | `MODULOS.py` | Importación específica `from ...Modulo_Saludar import Saludar` e invocación | Se integró dentro de las reglas de resolución de rutas calificadas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/Modulo_Saludar.py` (L2-10) | `Modulo_Saludar.py` | Definición de `Name()` y `Saludar()` consumidas desde otro archivo | Se analizó el desacoplamiento entre interfaz de consola y funciones de biblioteca |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/MODULOS_TWO.py` (L9-45) | `MODULOS_TWO.py` | Módulo nativo `sys`, `sys.builtin_module_names`, prioridad sobre módulos propios y `sys.path.append(...)` | Se precisó qué partes corresponden a la implementación CPython y cómo reemplazar rutas absolutas de Windows por `python -m` o `pip install -e .` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/Enrrutamiento_Modulo.py` (L11-43) | `Enrrutamiento_Modulo.py` | Importación de módulos ubicados en subcarpetas frente a carpetas externas | Se sistematizó la secuencia completa de búsqueda de `sys.meta_path` y `PathFinder` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/MODULOS_IMPORT/saludo_name.py` (L2-10) | `saludo_name.py` | Módulo externo al directorio inmediato importado en `MODULOS_TWO.py` | Se empleó para ilustrar la resolución desde la raíz del proyecto sin alterar `sys.path` manualmente |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/IMPORTAR/saludar.py` (L1-8) | `saludar.py` | Primer módulo de saludo reutilizado transversalmente desde `PAQUETE.py` (L51) | Se vinculó su archivo compilado en `__pycache__/saludar.cpython-313.pyc` con el funcionamiento real del caché de *bytecode* en CPython |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/DIVISION/division.py` (L1-40) | `division.py` | Ejecución en nivel superior `numero_A = primer_valor()` (L28) fuera de funciones | Se diagnosticó por qué ejecutar `input()` en el nivel superior bloquea cualquier importación del módulo |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_Clases.py` (L57-62) | `Decoradores_Clases.py` | Uso explícito de `if __name__ == "__main__":` para aislar la instanciación de prueba | Se tomó como referencia práctica dentro del propio repositorio para la guarda de ejecución principal |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Abastraccion.py` (L135) | `Abastraccion.py` | Importación selectiva de la biblioteca estándar (`from abc import ABC, abstractmethod`) | Se diferenció formalmente entre módulos integrados en C y módulos de la biblioteca estándar |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/CLASE_CUARTA/OCP.py` (L1-8) | `OCP.py` | Extensibilidad de módulos y clases sin modificar el código cliente | Se materializó mediante carga dinámica de módulos con `importlib.import_module` |

**Fundamento complementario:** se incorporaron cinco aspectos esenciales del estándar Python ausentes o solo esbozados en los apuntes originales: (1) el ciclo de vida *singleton* en `sys.modules` y `importlib`; (2) la distinción exacta entre módulos integrados de CPython, biblioteca estándar y paquetes instalables; (3) el propósito real de los archivos `.pyc` en `__pycache__`; (4) el control explícito de exportación mediante `__all__`; y (5) el diagnóstico y resolución de importaciones circulares y sombreamiento de módulos (*shadowing*).

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/modules.html> — Tutorial oficial de Python: módulos, variantes de `import`, ejecución como guion (`__main__`), ruta de búsqueda de módulos y directorio `__pycache__`.
- <https://docs.python.org/3/reference/import.html> — Referencia del lenguaje: especificación completa del sistema de importación, `sys.modules`, buscadores (`sys.meta_path`) y cargadores.
- <https://docs.python.org/3/library/sys.html> — Biblioteca estándar (`sys`): documentación de `sys.modules`, `sys.path` y `sys.builtin_module_names`.
- <https://docs.python.org/3/library/importlib.html> — Biblioteca estándar (`importlib`): interfaz programática de importación (`import_module`, `reload`).
- <https://docs.python.org/3/library/__main__.html> — Biblioteca estándar (`__main__`): entorno de código de nivel superior y modismos recomendados para puntos de entrada.
- <https://peps.python.org/pep-0008/#package-and-module-names> — PEP 8: convenciones oficiales para nombres de módulos y ordenamiento de sentencias `import`.
