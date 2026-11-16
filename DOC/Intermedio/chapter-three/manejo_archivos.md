# Manejo de Rutas, Archivos y Directorios con pathlib y Flujos de E/S

## 2. Introducción

Las variables y estructuras en memoria volátil desaparecen en el momento en que finaliza la ejecución de un script. Para conservar registros, configuraciones, bitácoras o reportes de manera permanente, una aplicación necesita interactuar con el sistema de archivos del sistema operativo anfitrión.

Tradicionalmente, Python gestionaba rutas mediante cadenas de texto en `os.path` y flujos con `open()`. A partir de Python 3.4 (PEP 428), el estándar moderno para modelar y operar rutas es el módulo `pathlib`, que ofrece una API orientada a objetos semántica, limpia y portable entre Linux, macOS y Windows.

Dominar la gestión de archivos y directorios con `pathlib` y flujos de entrada/salida (E/S) permite resolver con rigor técnico:

1. **Portabilidad de rutas entre sistemas operativos:** evitar separadores fijos como `\` o `/` mediante la clase `Path` y el operador `/`.
2. **Creación segura y automática de jerarquías de directorios:** crear carpetas y subcarpetas intermedias bajo demanda previniendo errores si ya existen.
3. **Liberación determinista de recursos:** emplear el gestor de contexto `with open(...)` para garantizar el cierre de descriptores y el vaciado de búferes incluso ante excepciones.
4. **Codificación universal UTF-8:** declarar explícitamente `encoding="utf-8"` (PEP 597) evitando corrupciones de texto (*mojibake*) en entornos heterogéneos.
5. **Prevención de sobrescrituras accidentales y condiciones de carrera:** utilizar modos exclusivos (`"x"`) y generación controlada de nombres correlativos (`archivo_1`, `archivo_2`).

## 3. Fundamentos y conceptos

**Rutas absolutas frente a relativas.** Una **ruta absoluta** especifica la ubicación completa de un archivo o carpeta desde la raíz del sistema de archivos (por ejemplo, `/home/usuario/datos/reporte.txt` en sistemas POSIX o `C:\Proyectos\datos\reporte.txt` en Windows). Una **ruta relativa** se define respecto al directorio de trabajo actual (*Current Working Directory* o CWD), por ejemplo `datos/reporte.txt`. En `pathlib`, el método `.is_absolute()` comprueba esta condición y `.resolve()` normaliza y convierte cualquier ruta relativa en absoluta resolviendo enlaces simbólicos.

**El módulo `pathlib` y la clase `Path`.** En lugar de concatenar cadenas manualmente, `Path` encapsula rutas como objetos del sistema de archivos:
- `Path.cwd()`: devuelve la ruta absoluta del directorio de trabajo actual.
- `Path.home()`: devuelve el directorio personal del usuario del sistema.
- Operador de composición `/`: `Path("carpeta") / "subcarpeta" / "archivo.txt"` concatena segmentos adaptando el separador correcto de la plataforma.

**Partes y anatomía de una ruta (`name`, `stem`, `suffix`, `parent`).** `Path` descompone una ruta sin necesidad de partir cadenas:
- `.name`: nombre completo con extensión (`"reporte_2025.csv"`).
- `.stem`: nombre base sin la extensión (`"reporte_2025"`).
- `.suffix`: extensión con el punto (`".csv"`).
- `.suffixes`: lista de extensiones múltiples (`[".tar", ".gz"]`).
- `.parent`: directorio contenedor inmediato.
- `.with_name(nuevo_nombre)`: retorna una nueva ruta sustituyendo el nombre completo.
- `.with_suffix(nueva_extension)`: retorna una nueva ruta reemplazando la extensión.

**Creación y verificación de existencia de directorios.**
- `.exists()`: comprueba si la ruta existe en el disco (sea archivo, directorio o enlace).
- `.is_file()` y `.is_dir()`: determinan el tipo específico de nodo.
- `.mkdir(parents=True, exist_ok=True)`: crea un directorio. El parámetro `parents=True` crea recursivamente cualquier directorio intermedio faltante en la ruta; `exist_ok=True` evita que se lance `FileExistsError` si la carpeta ya existía.

**Lectura y escritura: métodos directos frente a `open()`.**
1. **Métodos de conveniencia de `Path`:** para lecturas o escrituras directas de archivos completos, `Path.read_text(encoding="utf-8")` y `Path.write_text(contenido, encoding="utf-8")` gestionan internamente la apertura y cierre en una sola instrucción.
2. **Función `open()` con gestor de contexto `with`:** para flujos continuos, archivos grandes o control preciso de búferes, se utiliza `with open(ruta, mode=..., encoding="utf-8") as archivo:`. Garantiza el vaciado (`flush()`) y cierre (`close()`) del descriptor de archivo ante cualquier salida o excepción.

**Modos de apertura de archivos:**
- `"r"` (*read*): lectura (predeterminado); lanza `FileNotFoundError` si no existe.
- `"w"` (*write*): escritura; **trunca y vacía el archivo a 0 bytes de inmediato si ya existe**, o lo crea si no existe.
- `"a"` (*append*): adición al final; no borra contenido previo y crea el archivo si no existe.
- `"x"` (*exclusive creation*): creación exclusiva; crea el archivo para escritura, pero **lanza `FileExistsError` si el archivo ya existe**, previniendo sobrescrituras.
- Sufijo `"b"` (`"rb"`, `"wb"`): modo binario (imágenes, PDFs, bytes puros); en este modo no se especifica `encoding`.

**Renombrado y movimiento de archivos.**
- `.rename(destino)`: renombra o mueve un archivo o carpeta hacia `destino`. En Windows puede fallar si el destino ya existe.
- `.replace(destino)`: renombra o mueve sobrescribiendo atómicamente el destino si este ya existe (en sistemas que lo soporten).

**Prevención de colisiones y generación secuencial de nombres (`archivo_1`, `archivo_2`).** Cuando un programa no debe sobrescribir archivos previos bajo ninguna circunstancia, se inspecciona la ruta deseada; si ya existe, se itera generando sufijos numéricos correlativos antes de guardar.

**Condiciones de carrera (*Race Conditions* / TOCTOU).** En entornos multi-hilo, asíncronos o multi-proceso, comprobar si un archivo existe con `.exists()` y acto seguido crearlo con `"w"` introduce una ventana de vulnerabilidad conocida como **TOCTOU** (*Time-of-Check to Time-of-Use*): otro proceso puede crear el archivo entre la comprobación y la apertura. La forma robusta de evitar condiciones de carrera en el sistema de archivos a nivel atómico del kernel es abrir directamente con el modo `"x"` (`open(..., "x")`), o usar la llamada del sistema subyacente con `os.open(ruta, os.O_CREAT | os.O_EXCL | os.O_WRONLY)`.

## 4. Sintaxis y funcionamiento

Catálogo fundamental de métodos y sintaxis de `pathlib.Path`:

| N° | Operación | Método / Sintaxis | Descripción |
|---|---|---|---|
| 1 | Construcción | `ruta = Path("dir") / "archivo.txt"` | Concatena segmentos con el operador `/` |
| 2 | Verificación | `ruta.exists()`, `ruta.is_file()` | Comprueba existencia y tipo de elemento |
| 3 | Creación de carpetas | `directorio.mkdir(parents=True, exist_ok=True)` | Crea carpetas intermedias sin error si existen |
| 4 | Partes de la ruta | `ruta.stem`, `ruta.suffix`, `ruta.name` | Extrae nombre base, extensión o nombre completo |
| 5 | Mutación de nombre | `ruta.with_suffix(".csv")`, `ruta.with_name("x")` | Genera una nueva ruta con otra extensión o nombre |
| 6 | Lectura directa | `contenido = ruta.read_text(encoding="utf-8")` | Abre, lee y cierra texto completo en una instrucción |
| 7 | Escritura directa | `ruta.write_text("texto", encoding="utf-8")` | Abre, sobrescribe y cierra texto en una instrucción |
| 8 | Flujo con contexto | `with open(ruta, "r", encoding="utf-8") as f:` | Abre flujo asegurando cierre determinista |
| 9 | Creación exclusiva | `with open(ruta, "x", encoding="utf-8") as f:` | Lanza `FileExistsError` si el archivo ya existe |
| 10 | Renombrado | `ruta.rename(nueva_ruta)` | Mueve o cambia el nombre del nodo |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Inspección anatómica de rutas y lectura/escritura directa con `Path`.**

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    directorio_base = Path(tmp_dir)
    ruta_archivo = directorio_base / "reporte_ventas_2025.txt"

    print("Ruta relativa:", ruta_archivo)
    print("Nombre completo:", ruta_archivo.name)
    print("Nombre base (stem):", ruta_archivo.stem)
    print("Extensión (suffix):", ruta_archivo.suffix)
    print("Directorio padre:", ruta_archivo.parent.name)

    ruta_archivo.write_text("Línea 1: Ingresos\nLínea 2: Gastos\n", encoding="utf-8")

    print("¿Existe el archivo?:", ruta_archivo.exists())
    print("¿Es un archivo regular?:", ruta_archivo.is_file())

    contenido = ruta_archivo.read_text(encoding="utf-8")
    print("Contenido leído:")
    print(contenido.strip())
```

Explicación línea por línea:

- Se utiliza un directorio temporal controlado para garantizar un ejemplo reproducible.
- `directorio_base / "reporte_ventas_2025.txt"` compone la ruta sin barras invertidas manuales.
- `.stem` extrae `"reporte_ventas_2025"` y `.suffix` extrae `".txt"`.
- `ruta_archivo.write_text(...)` crea y escribe en el archivo garantizando codificación UTF-8.
- `.exists()` e `.is_file()` verifican el estado en disco en tiempo constante.
- `ruta_archivo.read_text(...)` lee el archivo y cierra el flujo automáticamente.

Resultado esperado:

```text
Nombre completo: reporte_ventas_2025.txt
Nombre base (stem): reporte_ventas_2025
Extensión (suffix): .txt
¿Existe el archivo?: True
¿Es un archivo regular?: True
Contenido leído:
Línea 1: Ingresos
Línea 2: Gastos
```

### Intermedio

**Ejemplo 2 — Guardado seguro con creación automática de carpetas y resolución de colisiones (`archivo_1`, `archivo_2`).**

Este ejemplo resuelve de manera completa el escenario requerido: verificar si la carpeta existe, crearla junto con carpetas intermedias si es necesario, construir la ruta del archivo, verificar si ya existe y generar nombres secuenciales disponibles sin sobrescribir información previa.

```python
import tempfile
from pathlib import Path


def guardar_documento_seguro(
    carpeta_destino: Path, nombre_base: str, extension: str, contenido: str
) -> Path:
    """Guarda un archivo garantizando la existencia de la carpeta y evitando sobrescrituras.

    Si el archivo ya existe, genera nombres correlativos: nombre_1, nombre_2, etc.
    """
    if not carpeta_destino.exists():
        carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension_limpia = f".{extension.lstrip('.')}"
    ruta_candidata = carpeta_destino / f"{nombre_base}{extension_limpia}"

    contador = 1
    while ruta_candidata.exists():
        nuevo_nombre = f"{nombre_base}_{contador}{extension_limpia}"
        ruta_candidata = carpeta_destino / nuevo_nombre
        contador += 1

    ruta_candidata.write_text(contenido, encoding="utf-8")
    return ruta_candidata


with tempfile.TemporaryDirectory() as tmp_dir:
    directorio_salida = Path(tmp_dir) / "proyectos" / "2026" / "reportes"

    doc1 = guardar_documento_seguro(
        directorio_salida, "balance", "txt", "Balance inicial v1"
    )
    doc2 = guardar_documento_seguro(
        directorio_salida, "balance", "txt", "Balance revisado v2"
    )
    doc3 = guardar_documento_seguro(
        directorio_salida, "balance", "txt", "Balance final v3"
    )

    print("Primer archivo guardado:", doc1.name)
    print("Segundo archivo guardado:", doc2.name)
    print("Tercer archivo guardado:", doc3.name)

    print("\nArchivos creados en la carpeta:")
    for archivo in sorted(directorio_salida.glob("*.txt")):
        print(f" - {archivo.name}: {archivo.read_text(encoding='utf-8')}")
```

Explicación de las decisiones tomadas:

- `carpeta_destino.mkdir(parents=True, exist_ok=True)` comprueba y crea automáticamente toda la jerarquía de subcarpetas intermedias (`proyectos/2026/reportes`) sin lanzar excepciones si ya existían.
- La función limpia la extensión para admitir tanto `"txt"` como `".txt"`.
- El bucle `while ruta_candidata.exists():` comprueba si el archivo ya existe y genera secuencialmente `balance_1.txt`, `balance_2.txt`, etc., hasta encontrar un nombre disponible.
- Se escribe el archivo con `write_text(..., encoding="utf-8")`, preservando íntegramente los archivos creados con anterioridad.

Resultado esperado:

```text
Primer archivo guardado: balance.txt
Segundo archivo guardado: balance_1.txt
Tercer archivo guardado: balance_2.txt

Archivos creados en la carpeta:
 - balance.txt: Balance inicial v1
 - balance_1.txt: Balance revisado v2
 - balance_2.txt: Balance final v3
```

### Avanzado

**Ejemplo 3 — Creación atómica libre de condiciones de carrera con modo `"x"` y renombrado atómico.**

```python
import os
import tempfile
from pathlib import Path


def guardar_atomico_sin_carrera(
    carpeta: Path, prefijo: str, extension: str, datos: str
) -> Path:
    """Crea un archivo nuevo garantizando atómicamente a nivel de sistema operativo

    que ningún otro proceso pueda sobrescribirlo durante la verificación (anti-TOCTOU).
    """
    carpeta.mkdir(parents=True, exist_ok=True)
    extension_norm = f".{extension.lstrip('.')}"

    intento = 0
    while True:
        sufijo = f"_{intento}" if intento > 0 else ""
        nombre_propuesto = f"{prefijo}{sufijo}{extension_norm}"
        ruta_posible = carpeta / nombre_propuesto

        try:
            with open(ruta_posible, mode="x", encoding="utf-8") as descriptor:
                descriptor.write(datos)
            return ruta_posible
        except FileExistsError:
            intento += 1


with tempfile.TemporaryDirectory() as tmp_dir:
    carpeta_trabajo = Path(tmp_dir) / "almacen_concurrente"

    r1 = guardar_atomico_sin_carrera(carpeta_trabajo, "transaccion", "log", "Registro A")
    r2 = guardar_atomico_sin_carrera(carpeta_trabajo, "transaccion", "log", "Registro B")

    print("Archivo atómico 1:", r1.name)
    print("Archivo atómico 2:", r2.name)

    ruta_renombrada = r2.with_suffix(".audit")
    r2.replace(ruta_renombrada)
    print("Archivo 2 tras replace:", ruta_renombrada.name, "| Existe:", ruta_renombrada.exists())
```

Explicación de rendimiento y seguridad:

- En lugar de comprobar `if ruta.exists():` antes de abrir (lo que deja una ventana de tiempo vulnerable donde otro hilo o proceso puede crear el archivo), se usa directamente `open(..., mode="x")`.
- El modo `"x"` solicita al núcleo del sistema operativo la bandera atómica `O_CREAT | O_EXCL`. La creación y la verificación ocurren en una única operación atómica indivisible.
- Si el archivo ya existía, el kernel lanza de inmediato `FileExistsError`, capturado por el bloque `except` para avanzar el contador al siguiente número de forma segura.
- `.replace(destino)` renombra atómicamente el archivo en el sistema de ficheros sin estados intermedios.

Resultado esperado:

```text
Archivo atómico 1: transaccion.log
Archivo atómico 2: transaccion_1.log
Archivo 2 tras replace: transaccion_1.audit | Existe: True
```

## 6. Aplicaciones en el mundo real

- **Sistemas de exportación e informes periódicos:** generar descargas de reportes diarios en carpetas `reportes/YYYY/MM/` asegurando nombres únicos como `ventas_2026_03_15_1.xlsx` sin pisar exportaciones de otros operadores.
- **Tuberías de ingesta y procesamiento de datos (ETL):** vigilar un directorio de entrada con `Path.glob("*.csv")`, procesar cada archivo y moverlo con `.replace()` hacia un directorio `procesados/` o `errores/`.
- **Servidores web y almacenamiento de subidas de usuarios:** normalizar nombres de archivos cargados por usuarios, aislar extensiones con `.suffix` y forzar nombres hash o correlativos para impedir ataques de sobrescritura deliberada.
- **Bitácoras (*logging*) con rotación de archivos:** segmentar archivos de log cuando alcanzan un tamaño límite, renombrando a `app.log.1`, `app.log.2` de forma segura.

## 7. Uso en producción

- **Definir siempre `encoding="utf-8"` explícito:** jamás omitir `encoding` en llamadas a `open()`, `read_text()` o `write_text()`. En Windows, la omisión recurre a `cp1252` o la configuración regional del sistema, provocando fallos silenciosos de decodificación al desplegar en servidores Linux.
- **Evitar comprobaciones manuales antes de escribir en entornos concurrentes:** las comprobaciones `if ruta.exists():` son vulnerables a condiciones de carrera (TOCTOU) si múltiples procesos o tareas asíncronas acceden al mismo directorio compartido. Utilizar modo `"x"` o nombres con identificadores universales únicos (`uuid.uuid4()`).
- **Limpieza de nombres y prevención de Path Traversal:** nunca concatenar rutas a partir de cadenas suministradas por el usuario sin validación. Si un usuario envía `../../etc/passwd`, el operador `/` ascenderá en la jerarquía. Utilizar `Path(nombre).name` para extraer estrictamente el nombre base antes de unirlo a la carpeta de destino.
- **Cierre determinista con gestores de contexto:** todo flujo `open()` debe ejecutarse dentro de un bloque `with`. Dejar archivos abiertos agota los descriptores de archivo del sistema operativo (*Too many open files*).

## 8. Errores comunes y recomendaciones

1. **Sobrescribir y destruir un archivo existente por usar `"w"`.**

```python
# ERROR COMÚN: el modo "w" trunca inmediatamente a 0 bytes al abrir
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "datos_criticos.txt"
    ruta.write_text("Información que no debe perderse", encoding="utf-8")

    with open(ruta, mode="w", encoding="utf-8") as f:
        pass

    print("Tamaño tras open('w') sin escribir:", ruta.stat().st_size, "bytes")
```

Resultado esperado:

```text
Tamaño tras open('w') sin escribir: 0 bytes
```

Diagnóstico: el modo `"w"` vacía el archivo en el instante exacto de abrirlo, incluso antes de ejecutar cualquier llamada a `.write()`. Recomendación: si se desea preservar el contenido anterior, usar modo `"a"` (añadir al final) o verificar previamente con sufijos correlativos.

2. **Operar sobre un flujo de archivo una vez cerrado el bloque `with` (`ValueError`).**

```python
# ERROR INTENCIONAL: ValueError al intentar leer fuera del bloque with
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "prueba.txt"
    ruta.write_text("contenido", encoding="utf-8")

    with open(ruta, "r", encoding="utf-8") as flujo:
        pass

    contenido = flujo.read()
```

Diagnóstico: al salir de la indentación de `with`, Python invoca garantizadamente `__exit__()` y cierra el descriptor. Invocar `.read()` o `.write()` fuera produce `ValueError: I/O operation on closed file`. Solución: realizar todas las lecturas dentro del bloque `with`.

3. **Construir rutas mediante concatenación manual de cadenas con barras invertidas.**
Escribir `"C:\\datos\\" + carpeta + "\\" + archivo` rompe la compatibilidad en Linux y macOS. Solución: usar siempre `Path("C:/datos") / carpeta / archivo`.

## 9. Resumen

- La clase `pathlib.Path` es el estándar moderno en Python para modelar rutas como objetos de primera clase independientes del sistema operativo.
- `Path.mkdir(parents=True, exist_ok=True)` crea directorios y cualquier carpeta intermedia necesaria de forma segura.
- Las propiedades `.name`, `.stem` y `.suffix` permiten descomponer nombres y extensiones con precisión.
- `with open(ruta, mode=..., encoding="utf-8") as f:` garantiza la liberación determinista de descriptores y el vaciado de búferes.
- El modo `"r"` lee, `"w"` trunca y sobrescribe, `"a"` añade al final y `"x"` exige creación exclusiva lanzando `FileExistsError` si la ruta ya existe.
- Para prevenir la pérdida de datos se implementa una rutina de comprobación correlativa (`archivo_1`, `archivo_2`).
- Para entornos concurrentes de alta exigencia, el modo `"x"` previene condiciones de carrera (TOCTOU) a nivel atómico del sistema operativo.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/pathlib.html> — Documentación oficial de Python sobre el módulo `pathlib` y la clase `Path`.
- <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files> — Tutorial oficial sobre lectura y escritura de archivos y gestores de contexto.
- <https://docs.python.org/3/library/functions.html#open> — Referencia de la función integrada `open()` y sus modos de operación.
- <https://peps.python.org/pep-0428/> — PEP 428 (*The pathlib Module — object-oriented filesystem paths*): propuesta original de `pathlib`.
- <https://peps.python.org/pep-0597/> — PEP 597 (*Add optional EncodingWarning*): justificación técnica de la codificación explícita `encoding="utf-8"`.
