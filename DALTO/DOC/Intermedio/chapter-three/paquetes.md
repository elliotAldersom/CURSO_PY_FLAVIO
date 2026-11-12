# Paquetes, Subpaquetes e Importaciones Relativas en Python

## 2. Introducción

Cuando un proyecto supera la decena de [módulos](modulos.md), mantener todos los archivos `.py` en un mismo directorio plano dificulta distinguir qué pertenece al dominio del negocio, qué corresponde a infraestructura y qué constituye la interfaz pública destinada a otros consumidores.

Un **paquete** en Python es un mecanismo de estructuración jerárquica del espacio de nombres de módulos mediante notación de puntos (`paquete.subpaquete.modulo`). En el sistema de archivos se organiza a través de directorios y subdirectorios, permitiendo agrupar módulos cohesionados bajo una raíz común sin riesgo de colisiones globales.

Dominar el modelo de paquetes en Python resulta esencial por cuatro motivos técnicos:

1. **Escalabilidad arquitectónica:** permite reflejar capas o dominios funcionales en árboles de directorios y **subpaquetes** (`PAQUETE/SUBPAQUETE/` en `PAQUETE.py` L26-33).
2. **Encapsulamiento de interfaz pública (patrón *Facade*):** mediante `__init__.py` y `__all__`, un paquete puede exponer una superficie limpia y estable ocultando su reorganización interna de archivos.
3. **Cohesión interna con importaciones absolutas y relativas:** conocer las reglas de **PEP 328** (`from . import ...`, `from .. import ...`) y la ejecución con `python -m` elimina errores de resolución entre submódulos.
4. **Distribución modular y paquetes de espacio de nombres:** diferenciar entre **paquetes regulares** (con `__init__.py`) y **paquetes de espacio de nombres implícitos** (**PEP 420**) permite comprender cómo se empaquetan y distribuyen bibliotecas modernas.

## 3. Fundamentos y conceptos

**Diferencia estructural entre módulo y paquete: el atributo `__path__`.** Tal como comprueba experimentalmente `PAQUETE.py` (L14-18 y L40-42), al evaluar `type(PAQUETE)` Python responde `<class 'module'>`. En el modelo de objetos del lenguaje, **todo paquete es un módulo, pero no todo módulo es un paquete**. La regla formal de la especificación de importación es inequívoca:

- Cualquier objeto `module` que posea el atributo `__path__` es tratado por Python como un **paquete**.
- Un módulo ordinario (cargado desde un archivo `.py` individual) tiene `__file__`, pero **carece de `__path__`**.
- El atributo `__path__` contiene una secuencia iterable de rutas de directorios donde el sistema de importación buscará los submódulos y subpaquetes anidados bajo ese nombre.

**Paquetes regulares (`__init__.py`) frente a paquetes de espacio de nombres (PEP 420).** En `PAQUETE.py` (L6-10) se indica que una carpeta necesita obligatoriamente un archivo `__init__.py` para ser reconocida como paquete. Conviene contextualizar históricamente esta afirmación para Python 3 moderno:

1. **Paquete regular (*regular package*):** directorio que contiene un archivo `__init__.py` (incluso vacío, como `PAQUETE/__init__.py` o `PAQUETE/SUBPAQUETE/__init__.py`). Al importarse el paquete, Python ejecuta `__init__.py` y asigna a `__path__` una `list` con la ruta de ese directorio (`PAQUETE.py` L41-42). Es el formato estándar y recomendado para la inmensa mayoría de proyectos y bibliotecas.
2. **Paquete de espacio de nombres implícito (*namespace package*, PEP 420 — Python 3.3+):** desde Python 3.3, si un directorio en `sys.path` **no** contiene `__init__.py`, Python aún puede importarlo como paquete de espacio de nombres. Su propósito principal es permitir que múltiples distribuciones independientes instaladas en distintos directorios compartan un mismo prefijo raíz (por ejemplo, `empresa.autenticacion` y `empresa.pagos`) fusionando sus rutas en un objeto especial `_NamespacePath`, con `__file__` igual a `None` y sin código de inicialización automático.

**Secuencia de inicialización jerárquica y subpaquetes.** Un **subpaquete** es un paquete anidado dentro de otro paquete (`PAQUETE/SUBPAQUETE/`). Cuando se ejecuta una importación profunda como `from paquete.subpaquete.saludar import Saludo` (`PAQUETE.py` L32), Python carga e inicializa de arriba hacia abajo cada nivel que aún no figure en `sys.modules`:

1. Carga `paquete` ejecutando `paquete/__init__.py` y lo registra en `sys.modules["paquete"]`.
2. Carga `paquete.subpaquete` ejecutando `paquete/subpaquete/__init__.py`, lo registra en `sys.modules["paquete.subpaquete"]` y lo enlaza como atributo `subpaquete` dentro de `paquete`.
3. Carga `paquete.subpaquete.saludar` ejecutando `saludar.py` y lo enlaza como atributo `saludar` de `subpaquete`.

Observación importante: importar únicamente `import paquete` ejecuta `paquete/__init__.py`, pero **no** carga automáticamente sus submódulos internos salvo que `paquete/__init__.py` los importe de forma explícita.

**Diseño de `__init__.py` y exportación controlada con `__all__`.** Aunque un `__init__.py` vacío basta para declarar un paquete regular, en arquitecturas limpias cumple dos funciones estratégicas:

- **Simplificar la API pública:** reexportar las clases o [funciones](../chapter-two/funciones.md) principales (`from .calculos import calcular_iva`) para que el código externo escriba `from facturacion import calcular_iva` sin acoplarse a la estructura interna de archivos.
- **Declarar `__all__`:** definir `__all__ = ["calcular_iva", "Factura"]` documenta explícitamente qué nombres constituyen el contrato público del paquete y restringe qué identificadores exporta una eventual sentencia `from paquete import *`. No debe colocarse lógica pesada en `__init__.py` para no penalizar el tiempo de arranque de cualquier submódulo.

**Importaciones absolutas frente a importaciones relativas explícitas (PEP 328).** Dentro de un paquete, un módulo puede referenciar a sus módulos hermanos o padres de dos maneras:

- **Importación absoluta:** especifica la ruta completa desde el paquete raíz visible en `sys.path` (`from mi_proyecto.servicios.pagos import cobrar`). PEP 8 la recomienda como opción preferente por su legibilidad inequívoca.
- **Importación relativa explícita (PEP 328):** utiliza puntos iniciales dentro de `from ... import ...` tomando como referencia el atributo `__package__` del módulo actual:
  - Un punto (`.`) indica el paquete actual (`from . import validador` o `from .validador import validar`).
  - Dos puntos (`..`) ascienden al paquete padre (`from ..compartido.moneda import formatear`).
  - Tres o más puntos ascienden niveles adicionales, aunque abusar de ellos suele indicar acoplamiento excesivo entre ramas lejanas. En Python 3 las antiguas importaciones relativas implícitas (sin punto inicial) fueron eliminadas definitivamente.

**Por qué falla ejecutar un submódulo por ruta de archivo frente a `python -m`.** Un error muy frecuente ocurre cuando un archivo interno `paquete/subpaquete/reporte.py` contiene una importación relativa (`from ..util import limpiar`) y se ejecuta directamente como `python paquete/subpaquete/reporte.py`:

- Al pasarse como ruta de archivo, Python fija `__name__ = "__main__"`, `__package__ = None` e inserta `paquete/subpaquete/` (no la raíz del proyecto) en `sys.path[0]`. Sin paquete padre conocido, Python lanza `ImportError: attempted relative import with no known parent package`.
- Al ejecutarse desde la raíz del proyecto mediante el modificador modular `python -m paquete.subpaquete.reporte`, Python conserva la raíz en `sys.path`, establece `__name__ = "__main__"` pero asigna correctamente `__package__ = "paquete.subpaquete"`, permitiendo que todas las importaciones relativas y absolutas funcionen sin alterar `sys.path`. Si además se incluye un archivo `__main__.py` en el paquete, este completo pasa a ser ejecutable con `python -m paquete`.

**Reglas de nomenclatura de directorios de paquetes.** Para que un directorio pueda importarse en Python, su nombre **debe ser un identificador léxico válido** (idealmente en minúsculas ASCII cortas según PEP 8):

- **Prohibición de sufijos `.py` / `.PY` en carpetas:** en el repositorio original existe el directorio `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/`. Incluir un punto en el nombre de una carpeta impide importarla normalmente porque en `import A.B` el analizador interpreta el punto como acceso al submódulo `B` dentro de `A`.
- **Prohibición de espacios y paréntesis:** carpetas como `MÉTODOS Y FUNCIONES` o `EJEMPLOS (CLASS_ONE)` tampoco constituyen identificadores Python válidos para sentencias `import`.
- **Evitar colisión entre carpeta `paquete/` y archivo `paquete.py`:** en `CLASE_TERCERA/` coexisten el directorio `PAQUETE/` (con `__init__.py`) y el archivo `PAQUETE.py`. Cuando un paquete regular y un módulo homónimo conviven en el mismo directorio de `sys.path`, Python prioriza el paquete regular (el directorio con `__init__.py`), ocultando al archivo `.py` ante cualquier `import`.

## 4. Sintaxis y funcionamiento

Estructura típica de un paquete regular con subpaquete, fachada pública y punto de entrada modular:

```text
proyecto_raiz/
└── comercio/
    ├── __init__.py          # API pública del paquete (__all__)
    ├── __main__.py          # Punto de entrada para: python -m comercio
    ├── catalogo.py          # Módulo de primer nivel
    └── pagos/
        ├── __init__.py      # Inicializador del subpaquete
        └── procesador.py    # Usa: from ..catalogo import obtener_precio
```

Elementos sintácticos y atributos de paquetes:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `__init__.py` | Convierte un directorio en paquete regular y ejecuta su inicialización | `comercio/__init__.py` |
| 2 | `__main__.py` | Define el bloque de ejecución al invocar el paquete con `python -m` | `python -m comercio` |
| 3 | `paquete.__path__` | Secuencia de rutas donde se buscan submódulos; distingue paquetes de módulos | `hasattr(comercio, "__path__")` |
| 4 | `modulo.__package__` | Nombre del paquete contenedor usado para resolver importaciones relativas | `"comercio.pagos"` |
| 5 | `import p.sub.mod` | Importación absoluta con ruta completa; exige acceso calificado completo | `p.sub.mod.ejecutar()` |
| 6 | `from p.sub import mod` | Importación absoluta que enlaza directamente el submódulo `mod` | `mod.ejecutar()` |
| 7 | `from . import mod` | Importación relativa explícita de un módulo hermano en el mismo paquete | `from . import catalogo` |
| 8 | `from ..a import x` | Importación relativa desde el paquete padre (`..`) hacia otro submódulo | `from ..catalogo import Producto` |
| 9 | `__all__` en `__init__.py` | Lista explícita de símbolos públicos exportados por el paquete | `__all__ = ["Producto", "cobrar"]` |
| 10 | Sin `__init__.py` | Paquete de espacio de nombres implícito (PEP 420, Python 3.3+) | `__file__ is None` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Construcción de un paquete regular con subpaquete, verificación de `__path__` y fachada en `__init__.py`.**

```python
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    raiz = Path(tmp_dir)
    pkg = raiz / "inventario"
    sub = pkg / "reportes"
    sub.mkdir(parents=True)

    (pkg / "__init__.py").write_text(
        '__all__ = ["Producto", "resumir_stock"]\n'
        'from .modelos import Producto\n'
        'from .reportes.resumen import resumir_stock\n',
        encoding="utf-8",
    )
    (pkg / "modelos.py").write_text(
        'class Producto:\n'
        '    def __init__(self, nombre: str, unidades: int) -> None:\n'
        '        self.nombre = nombre\n'
        '        self.unidades = unidades\n',
        encoding="utf-8",
    )
    (sub / "__init__.py").write_text("", encoding="utf-8")
    (sub / "resumen.py").write_text(
        'def resumir_stock(items: list) -> str:\n'
        '    total = sum(p.unidades for p in items)\n'
        '    return f"Productos: {len(items)} | Unidades totales: {total}"\n',
        encoding="utf-8",
    )

    sys.path.insert(0, tmp_dir)
    try:
        import inventario
        from inventario import Producto, resumir_stock

        lote = [Producto("Teclado", 12), Producto("Monitor", 5)]
        print("Tipo de inventario:", type(inventario))
        print("¿Tiene __path__?:", hasattr(inventario, "__path__"), type(inventario.__path__))
        print("¿modelos.py tiene __path__?:", hasattr(inventario.modelos, "__path__"))
        print("API pública (__all__):", inventario.__all__)
        print(resumir_stock(lote))
    finally:
        sys.path.remove(tmp_dir)
        for mod in list(sys.modules):
            if mod == "inventario" or mod.startswith("inventario."):
                sys.modules.pop(mod, None)
```

Explicación paso a paso:

- Se crea una jerarquía real `inventario/` con un subpaquete `inventario/reportes/`, reproduciendo y profesionalizando el esquema de `PAQUETE/SUBPAQUETE/` (`PAQUETE.py` L31-47).
- Se comprueba la diferencia estructural clave: tanto `inventario` como `inventario.modelos` son `<class 'module'>`, pero solo el paquete `inventario` posee `__path__` (de tipo `list`), mientras que el módulo hoja `modelos` devuelve `False`.
- Gracias a la reexportación en `inventario/__init__.py`, el consumidor importa `Producto` y `resumir_stock` directamente desde la raíz del paquete sin acoplarse a las rutas internas.

Resultado esperado:

```text
Tipo de inventario: <class 'module'>
¿Tiene __path__?: True <class 'list'>
¿modelos.py tiene __path__?: False
API pública (__all__): ['Producto', 'resumir_stock']
Productos: 2 | Unidades totales: 17
```

### Intermedio

**Ejemplo 2 — Importaciones relativas explícitas (`.` y `..`) entre subpaquetes hermanos y atributo `__package__`.**

```python
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    raiz = Path(tmp_dir)
    (raiz / "finanzas" / "moneda").mkdir(parents=True)
    (raiz / "finanzas" / "facturacion").mkdir(parents=True)

    (raiz / "finanzas" / "__init__.py").write_text("", encoding="utf-8")
    (raiz / "finanzas" / "moneda" / "__init__.py").write_text("", encoding="utf-8")
    (raiz / "finanzas" / "moneda" / "formato.py").write_text(
        'def formatear_usd(monto: float) -> str:\n'
        '    return f"USD {monto:,.2f}"\n',
        encoding="utf-8",
    )
    (raiz / "finanzas" / "facturacion" / "__init__.py").write_text("", encoding="utf-8")
    (raiz / "finanzas" / "facturacion" / "impuestos.py").write_text(
        'def aplicar_igv(base: float) -> float:\n'
        '    return round(base * 1.18, 2)\n',
        encoding="utf-8",
    )
    (raiz / "finanzas" / "facturacion" / "emisor.py").write_text(
        'from .impuestos import aplicar_igv\n'
        'from ..moneda.formato import formatear_usd\n\n'
        'def emitir_comprobante(cliente: str, neto: float) -> str:\n'
        '    bruto = aplicar_igv(neto)\n'
        '    return f"Cliente: {cliente} | Total: {formatear_usd(bruto)}"\n',
        encoding="utf-8",
    )

    sys.path.insert(0, tmp_dir)
    try:
        from finanzas.facturacion import emisor

        print("Nombre calificado (__name__):", emisor.__name__)
        print("Paquete contenedor (__package__):", emisor.__package__)
        print(emisor.emitir_comprobante("Elena", 1000.0))
    finally:
        sys.path.remove(tmp_dir)
        for mod in list(sys.modules):
            if mod == "finanzas" or mod.startswith("finanzas."):
                sys.modules.pop(mod, None)
```

Explicación técnica:

- Dentro de `emisor.py`, `from .impuestos import aplicar_igv` resuelve un módulo hermano en `finanzas.facturacion`, mientras que `from ..moneda.formato import formatear_usd` asciende un nivel hasta `finanzas` y desciende al subpaquete hermano `moneda`.
- Python calcula ambos desplazamientos usando `emisor.__package__`, cuyo valor es `"finanzas.facturacion"`.

Resultado esperado:

```text
Nombre calificado (__name__): finanzas.facturacion.emisor
Paquete contenedor (__package__): finanzas.facturacion
Cliente: Elena | Total: USD 1,180.00
```

### Avanzado

**Ejemplo 3 — Paquetes de espacio de nombres implícitos (PEP 420) distribuidos en múltiples directorios y ejecución con `python -m`.**

```python
import subprocess
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as dir_a, tempfile.TemporaryDirectory() as dir_b:
    # Dos raíces distintas sin __init__.py en 'ecosistema/' conforman un namespace package unificado
    (Path(dir_a) / "ecosistema" / "auth").mkdir(parents=True)
    (Path(dir_a) / "ecosistema" / "auth" / "__init__.py").write_text(
        'def autenticar(usuario: str) -> bool:\n'
        '    return bool(usuario.strip())\n',
        encoding="utf-8",
    )

    (Path(dir_b) / "ecosistema" / "metricas").mkdir(parents=True)
    (Path(dir_b) / "ecosistema" / "metricas" / "__init__.py").write_text("", encoding="utf-8")
    (Path(dir_b) / "ecosistema" / "metricas" / "__main__.py").write_text(
        'from ecosistema.auth import autenticar\n'
        'print("Ejecución vía -m exitosa | Usuario válido:", autenticar("flavio"))\n',
        encoding="utf-8",
    )

    sys.path.insert(0, dir_b)
    sys.path.insert(0, dir_a)
    try:
        import ecosistema
        from ecosistema.auth import autenticar

        print("Archivo __file__ en namespace PEP 420:", ecosistema.__file__)
        print("Cantidad de rutas fusionadas en __path__:", len(list(ecosistema.__path__)))
        print("Subpaquete auth operativo:", autenticar("ana"))
    finally:
        sys.path.remove(dir_a)
        sys.path.remove(dir_b)
        for mod in list(sys.modules):
            if mod == "ecosistema" or mod.startswith("ecosistema."):
                sys.modules.pop(mod, None)

    env = {"PYTHONPATH": f"{dir_a}:{dir_b}" if sys.platform != "win32" else f"{dir_a};{dir_b}"}
    resultado = subprocess.run(
        [sys.executable, "-m", "ecosistema.metricas"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    print(resultado.stdout.strip())
```

Explicación de arquitectura:

- Ni `dir_a/ecosistema` ni `dir_b/ecosistema` tienen `__init__.py`. Conforme a **PEP 420**, Python une ambas ubicaciones bajo un único paquete de espacio de nombres `ecosistema` (`__file__` es `None` y `__path__` agrupa las `2` rutas), permitiendo que `ecosistema.metricas` importe `ecosistema.auth` aunque residan en árboles físicos separados.
- La presencia de `__main__.py` dentro de `ecosistema/metricas/` habilita su invocación limpia mediante `python -m ecosistema.metricas`.

Resultado esperado:

```text
Archivo __file__ en namespace PEP 420: None
Cantidad de rutas fusionadas en __path__: 2
Subpaquete auth operativo: True
Ejecución vía -m exitosa | Usuario válido: True
```

## 6. Aplicaciones en el mundo real

- **Arquitectura hexagonal o limpia por dominios:** organizar grandes aplicaciones web en paquetes como `dominio/`, `aplicacion/`, `infraestructura/` y `presentacion/`, aislando reglas de negocio de bases de datos y controladores HTTP.
- **Bibliotecas científicas y SDKs con fachada pública:** bibliotecas como NumPy, Pandas o FastAPI dividen su implementación en decenas de subpaquetes internos (`pandas.core`, `pandas.io`), pero reexportan en su `__init__.py` superior las clases esenciales (`DataFrame`, `Series`, `read_csv`).
- **Ecosistemas corporativos multipaquete (PEP 420):** organizaciones que publican conectores independientes bajo un espacio de nombres común (`google.cloud.storage`, `google.cloud.bigquery` o `azure.storage.blob`) instalables por separado sin pisar un único `__init__.py`.
- **Herramientas de línea de comandos empaquetadas:** utilidades como `python -m venv`, `python -m unittest` o `python -m http.server` que aprovechan `__main__.py` dentro de un paquete para ofrecer ejecución directa.

## 7. Uso en producción

- **Adoptar la disposición `src/` (*src layout*) con `pyproject.toml`:** ubicar el paquete principal en `src/mi_paquete/__init__.py` e instalarlo con `pip install -e .` evita importar accidentalmente carpetas locales sin instalar durante la ejecución de pruebas con `pytest`, asegurando que el entorno de desarrollo se comporte exactamente igual que el paquete desplegado en producción.
- **Ejecutar siempre puntos de entrada internos con `python -m`:** sustituir ejecuciones directas por ruta (`python src/mi_paquete/tareas/sincronizar.py`) por invocaciones modulares (`python -m mi_paquete.tareas.sincronizar`) o puntos de entrada declarados en `[project.scripts]` dentro de `pyproject.toml`.
- **Mantener los archivos `__init__.py` ligeros y deterministas:** limitar `__init__.py` a metadatos de versión, definición de `__all__` y reexportaciones ligeras. Si un submódulo importa dependencias costosas o opcionales, no debe reexportarse ansiosamente en la raíz del paquete (o puede diferirse mediante `__getattr__` a nivel de módulo según **PEP 562**).
- **Preferir importaciones absolutas entre dominios y reservar las relativas para cohesión local:** usar rutas absolutas (`from mi_paquete.usuarios.servicio import ...`) facilita buscar y mover archivos en proyectos grandes, reservando importaciones relativas de un nivel (`from .esquemas import ...`) para archivos estrechamente acoplados dentro de un mismo subpaquete.

## 8. Errores comunes y recomendaciones

1. **Intentar una importación relativa ejecutando el archivo directamente (`ImportError`).**

```python
import subprocess
import sys
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    pkg = Path(tmp_dir) / "app"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "auxiliar.py").write_text("CONSTANTE = 42\n", encoding="utf-8")
    guion = pkg / "tarea.py"
    guion.write_text("from .auxiliar import CONSTANTE\nprint(CONSTANTE)\n", encoding="utf-8")

    fallo = subprocess.run([sys.executable, str(guion)], capture_output=True, text=True)
    exito = subprocess.run(
        [sys.executable, "-m", "app.tarea"], cwd=tmp_dir, capture_output=True, text=True
    )

    print("Ejecución directa falló con ImportError:", "ImportError" in fallo.stderr)
    print("Ejecución con 'python -m app.tarea':", exito.stdout.strip())
```

Resultado esperado:

```text
Ejecución directa falló con ImportError: True
Ejecución con 'python -m app.tarea': 42
```

Diagnóstico: al ejecutar `python app/tarea.py`, Python desconoce que `app/` es un paquete (`__package__` vale `None`) y aborta con `ImportError: attempted relative import with no known parent package`. Solución: situarse en el directorio contenedor y ejecutar `python -m app.tarea`.

2. **Colocar puntos, espacios o extensiones `.PY` en el nombre de un directorio de paquete (`SyntaxError` / `ModuleNotFoundError`).**

```python
# ERROR INTENCIONAL: un directorio llamado 'EJERCICIOS_DE_CLASE_ONE.PY' no puede importarse directamente
import EJERCICIOS_DE_CLASE_ONE.PY.calculadora_simple
```

Diagnóstico: en `import EJERCICIOS_DE_CLASE_ONE.PY.calculadora_simple`, Python busca un paquete llamado `EJERCICIOS_DE_CLASE_ONE` y dentro de él un subpaquete llamado `PY`, lanzando `ModuleNotFoundError` (y si el directorio tuviese espacios o paréntesis, produciría directamente `SyntaxError`). Recomendación: nombrar todos los directorios de paquetes exclusivamente con identificadores en minúsculas ASCII sin puntos ni espacios (`ejercicios_clase_uno`).

3. **Asumir que `import paquete` carga automáticamente todos sus submódulos (`AttributeError`).**

```python
# ERROR INTENCIONAL: AttributeError al acceder a un submódulo no importado en __init__.py
import urllib

# Si nadie importó previamente 'urllib.parse', el atributo 'parse' aún no existe en 'urllib'
partes = urllib.parse.urlparse("https://docs.python.org/3/")
```

Diagnóstico: importar un paquete superior solo ejecuta su `__init__.py`; si dicho archivo no importa sus submódulos internos, estos no se enlazan como atributos del paquete. Solución: importar explícitamente el submódulo requerido (`import urllib.parse` o `from urllib import parse`).

4. **Crear un archivo `paquete.py` en la misma carpeta que un directorio `paquete/`.** Tal como ocurre en `CLASE_TERCERA/` con `PAQUETE.py` y `PAQUETE/`, el paquete regular tiene precedencia sobre el archivo `.py` homónimo durante cualquier `import`, impidiendo importar las definiciones del archivo suelto. Nunca debe reutilizarse el nombre de un paquete para un guion situado en el mismo nivel.

## 9. Resumen

- En Python todo paquete es un objeto `module` caracterizado por poseer el atributo `__path__`, el cual define las rutas de búsqueda de sus submódulos y subpaquetes.
- Los **paquetes regulares** contienen un archivo `__init__.py` que se ejecuta una sola vez al cargarse el paquete y permite exponer una API pública controlada junto con `__all__`.
- Los **paquetes de espacio de nombres implícitos** (**PEP 420**, Python 3.3+) carecen de `__init__.py` y permiten distribuir subpaquetes de un mismo prefijo a través de múltiples directorios independientes.
- Las importaciones absolutas parten de `sys.path`, mientras que las importaciones relativas explícitas (`from . import ...`, `from .. import ...`, **PEP 328**) resuelven rutas usando `__package__`.
- Los módulos internos de un paquete nunca deben ejecutarse por ruta de archivo si emplean importaciones del paquete; deben invocarse desde la raíz mediante `python -m paquete.modulo` o un archivo `__main__.py`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE.py` (L1-54) | `PAQUETE.py` | Definición de paquete y subpaquete, `type(PAQUETE)` como `<class 'module'>`, consulta de `PAQUETE.__path__` e importación punteada | Se precisó el rol formal de `__path__`, se contrastó con paquetes de espacio de nombres (PEP 420) y se advirtió sobre la colisión entre `PAQUETE.py` y el directorio `PAQUETE/` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE/__init__.py` | `__init__.py` | Archivo inicializador vacío para declarar el paquete regular `PAQUETE` | Se amplió su uso profesional como fachada de API pública y definición de `__all__` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE/Saludar.py` (L2-12) | `Saludar.py` | Módulo de primer nivel dentro de `PAQUETE` con impresión de `__name__` al cargarse | Se explicó el orden descendente de inicialización de paquetes y el valor calificado de `__name__` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE/SUBPAQUETE/__init__.py` | `__init__.py` | Declaración de `SUBPAQUETE` como subpaquete importable dentro de `PAQUETE` | Se detalló cómo cada nivel intermedio requiere resolución previa en `sys.modules` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE/SUBPAQUETE/saludar.py` (L1-3) | `saludar.py` | Función `Saludo(name)` consumida desde un subpaquete anidado | Se utilizó como base para contrastar importaciones absolutas frente a relativas explícitas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE/SUBPAQUETE/saludo_raro.py` (L2-17) | `saludo_raro.py` | Múltiples funciones en un submódulo de segundo nivel | Se vinculó con las buenas prácticas de cohesión y nombres en `snake_case` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/Enrrutamiento_Modulo.py` (L11-20) | `Enrrutamiento_Modulo.py` | Comparación entre `import ...PAQUETE.Saludar` y `from ...PAQUETE.Saludar import Saludar` | Se formalizó por qué `import paquete` no carga automáticamente submódulos no referenciados |
| `CLASES_PYTHON/` | `CLASES_PYTHON/__init__.py` | `__init__.py` | Marcador de paquete en la raíz de apuntes procedimentales | Se relacionó con la estructuración moderna `src/` y `pyproject.toml` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/__init__.py` | `__init__.py` | Marcador de paquete en la raíz de apuntes de programación orientada a objetos | Integrado en el análisis general de jerarquías multipaquete del repositorio |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/__init__.py` | `__init__.py` | Carpeta con sufijo `.PY` en su nombre a pesar de contener `__init__.py` | Se documentó por qué incluir puntos, espacios o extensiones `.PY` en nombres de carpetas invalida su importación en Python |

**Fundamento complementario:** se añadieron cuatro pilares de la especificación moderna de Python no cubiertos en el material base: (1) los paquetes de espacio de nombres implícitos introducidos por **PEP 420** en Python 3.3+; (2) las reglas sintácticas y semánticas de las importaciones relativas explícitas (**PEP 328**) basadas en `__package__`; (3) el diagnóstico de `ImportError` al ejecutar submódulos directamente frente a `python -m` y `__main__.py`; y (4) el diseño de fachadas públicas con `__all__` y estructura `src/`.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/modules.html#packages> — Tutorial oficial de Python: paquetes, subpaquetes, `__init__.py`, `__all__` e importaciones intrapaquete.
- <https://docs.python.org/3/reference/import.html#packages> — Referencia del lenguaje: definición formal de paquetes mediante `__path__`, paquetes regulares y paquetes de espacio de nombres.
- <https://docs.python.org/3/reference/import.html#package-relative-imports> — Referencia del lenguaje: resolución de importaciones relativas explícitas a partir de `__package__`.
- <https://peps.python.org/pep-0328/> — PEP 328 (*Imports: Multi-Line and Absolute/Relative*): introducción de importaciones absolutas por defecto y sintaxis relativa con puntos.
- <https://peps.python.org/pep-0420/> — PEP 420 (*Implicit Namespace Packages*): especificación oficial de paquetes de espacio de nombres sin `__init__.py`.
- <https://peps.python.org/pep-0008/#package-and-module-names> — PEP 8: convenciones de nomenclatura para nombres de paquetes.
