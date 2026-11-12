# Manejo de Archivos de Texto, Flujos de E/S y Gestores de Contexto

## 2. Introducción

Las [variables](../../Basico/chapter-one/variables.md) y estructuras en memoria volátil desaparecen en el instante en que finaliza el proceso del intérprete. Para conservar registros, configuraciones, bitácoras o reportes más allá de una ejecución, un programa necesita interactuar con el sistema de almacenamiento persistente a través de **archivos**.

En Python, el acceso a archivos se articula mediante la función integrada `open()` y la jerarquía de flujos (*streams*) del módulo estándar `io`, complementados modernamente por las rutas orientadas a objetos de `pathlib.Path`.

Comprender con precisión el modelo de entrada/salida de archivos permite resolver cuatro exigencias críticas de calidad y confiabilidad:

1. **Liberación determinista de recursos del sistema operativo:** emplear el gestor de contexto `with open(...) as archivo:` (`Leer_TXT_Optimamente.py` L9) garantiza el vaciado de búferes y el cierre inmediato del descriptor de archivo, incluso si ocurre una [excepción](../chapter-four/excepciones.md) a mitad de la operación.
2. **Portabilidad de texto e internacionalización:** declarar siempre `encoding="utf-8"` (**PEP 597**) evita la corrupción de tildes, eñes o diéresis (`"agüita"` en `Editar_TXT.py` L14) al mover código entre Windows, Linux y macOS.
3. **Escalabilidad en memoria:** distinguir entre cargar un archivo completo en RAM (`.read()`, `.readlines()`) y recorrerlo perezosamente línea por línea (`for linea in archivo:`) permite procesar desde archivos de pocos kilobytes hasta bitácoras de decenas de gigabytes con consumo constante $O(1)$.
4. **Independencia del sistema de archivos anfitrión:** construir rutas portables con `pathlib.Path` sustituye cadenas absolutas rígidas como `"C:\\Users\\Administrador\\..."` (`archivos_txt.py` L19, `problema_txt.py` L81).

## 3. Fundamentos y conceptos

**Descriptores del sistema operativo y capas de búfer (`io`).** Abrir un archivo no carga su contenido mágicamente en una variable; solicita al núcleo (*kernel*) del sistema operativo un **descriptor de archivo**, un identificador numérico finito por proceso. Sobre ese recurso de bajo nivel, el módulo estándar `io` de Python construye hasta tres capas:

1. **Capa cruda sin búfer (`io.FileIO`):** interactúa directamente con llamadas al sistema leyendo o escribiendo secuencias de bytes.
2. **Capa binaria con búfer (`io.BufferedReader` / `io.BufferedWriter`):** agrupa lecturas y escrituras en bloques de memoria (típicamente de 4 KiB u 8 KiB) para minimizar costosas transiciones hacia el sistema operativo.
3. **Capa de texto (`io.TextIOWrapper`):** se activa en los modos de texto (predeterminados), encargándose de decodificar `bytes` a objetos `str` al leer, codificar `str` a `bytes` al escribir y normalizar los saltos de línea universales (`\r\n` en Windows y `\n` en sistemas POSIX se entregan uniformemente como `"\n"` dentro de Python).

**Modos de apertura y advertencia sobre el truncado en `"w"`.** El segundo parámetro de `open(ruta, mode="r", ...)` determina qué operaciones admite el flujo y cómo trata un archivo preexistente:

- `"r"` (*read*, valor por defecto): abre para lectura de texto desde el inicio; lanza `FileNotFoundError` si el archivo no existe.
- `"w"` (*write*, `Editar_TXT.py` L7): abre para escritura de texto. Si el archivo no existe, lo crea; **si ya existe, trunca y destruye inmediatamente todo su contenido previo dejándolo en 0 bytes en el instante mismo de ejecutar `open()`**, incluso si nunca se llega a invocar `.write()`.
- `"a"` (*append*, `Agregar_TXT.py` L11, `problema_txt.py` L81): abre para adición al final del archivo sin borrar los datos existentes, creándolo si no existe.
- `"x"` (*exclusive creation*): crea un archivo nuevo para escritura, pero lanza `FileExistsError` si la ruta ya existe, protegiendo contra sobrescrituras accidentales.
- `"r+"`: habilita lectura y escritura sobre un archivo existente sin truncarlo al abrir.
- Sufijo `"b"` (`"rb"`, `"wb"`, `"ab"`): desactiva la capa `TextIOWrapper` y opera directamente con objetos `bytes` sin traducción de codificación ni de saltos de línea (indispensable para imágenes PNG, documentos PDF, audio MP4 o archivos comprimidos). En modo binario **no** se admite el parámetro `encoding`.

**Codificación explícita obligatoria (`encoding="utf-8"`, PEP 597).** Cuando se abre un archivo de texto omitiendo `encoding` (`archivos_txt.py` L19), Python consulta la codificación regional preferida del sistema operativo (`locale.getpreferredencoding(False)`):

- En distribuciones modernas de Linux y macOS suele ser `UTF-8`.
- En configuraciones tradicionales de Windows en español suele ser `cp1252` (Windows-1252).

Un archivo guardado en UTF-8 que contenga `"agüita"` o `"año"` y se lea sin `encoding="utf-8"` en Windows producirá caracteres corruptos (*mojibake*, como `"agÃ¼ita"`) o lanzará `UnicodeDecodeError`. Como estandariza **PEP 597** (que introdujo la advertencia `EncodingWarning` activable con `-X warn_default_encoding`), toda llamada a `open()` en modo texto debe especificar explícitamente `encoding="utf-8"` salvo que se trabaje deliberadamente con un formato heredado.

**El gestor de contexto `with open(...) as f:` frente a `.close()` manual.** En `archivos_txt.py` (L19 y L45) el archivo se abre manualmente y se cierra al final con `archivo_sin_leer.close()`. Si entre ambas líneas ocurre cualquier excepción, `close()` no llega a ejecutarse: el descriptor permanece retenido y los datos pendientes en el búfer de escritura pueden no volcarse a disco.

La sentencia `with` (`Leer_TXT_Optimamente.py` L9) implementa el **protocolo de gestor de contexto** mediante los [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md) `__enter__()` y `__exit__()`:

- Al entrar al bloque, `__enter__()` devuelve el flujo abierto y lo enlaza a la variable tras `as`.
- Al abandonar el bloque —ya sea por terminación normal, `return`, `break` o por una excepción no capturada—, Python invoca garantizadamente `__exit__()`, que vacía el búfer (`flush()`) y cierra el archivo (`close()`). Conviene precisar una observación sobre el comentario de `Leer_TXT_Optimamente.py` (L4): `with open` **no oculta ni suprime excepciones** (si el archivo no existe, seguirá lanzando `FileNotFoundError`), sino que garantiza la limpieza determinista del recurso ante cualquier fallo. Una vez fuera del bloque `with`, `archivo.closed` vale `True` y cualquier intento ulterior de lectura o escritura lanza `ValueError: I/O operation on closed file`.

**El cursor de flujo (`tell()` y `seek()`) y por qué una segunda lectura devuelve vacío.** En `archivos_txt.py` (L23-30) aparece una duda conceptual clásica: tras descomentar `archivo_sin_leer.read()`, una llamada inmediata a `archivo_sin_leer.readlines()` devuelve una lista vacía `[]`, atribuida en el comentario a que "no está cerrado el archivo". La causa real es el **puntero o cursor interno de posición** del flujo:

- Al abrirse en modo `"r"`, el cursor se ubica en el byte `0`.
- Cada operación de lectura avanza el cursor tantos bytes como haya consumido; `.read()` sin argumentos consume hasta el final del archivo (*EOF*).
- Una vez situado en *EOF*, cualquier llamada subsiguiente a `.read()`, `.readline()` o `.readlines()` retorna inmediatamente `""` o `[]` porque no quedan caracteres hacia adelante.
- El método `f.tell()` informa la posición actual del cursor y `f.seek(0)` lo rebobina al inicio del flujo sin necesidad de reabrir el archivo. Asimismo, respecto a `readline(21)` (`archivos_txt.py` L38-41), el argumento entero fija el **máximo** de caracteres a leer dentro de la línea actual; si la línea es más corta, se detiene en `"\n"` sin rellenar con espacios adicionales.

**Estrategias de lectura y eficiencia en memoria.** Existen cuatro formas de consumir un flujo de texto, con perfiles de memoria muy distintos:

- `f.read()`: carga todo el contenido en una única cadena `str` ($O(N)$ en memoria). Adecuado solo para archivos pequeños o medianos de tamaño controlado.
- `f.readlines()`: construye en memoria una `list[str]` con todas las líneas del archivo, conservando el `"\n"` final de cada una ($O(N)$ en memoria).
- `f.readline()`: lee una sola línea por llamada; retorna `""` únicamente al alcanzar *EOF* (una línea en blanco vacía retorna `"\n"`).
- **Iteración directa sobre el flujo (`for linea in f:`):** los objetos archivo son [iteradores](../../Avanzado/chapter-one/iteradores.md) perezosos que producen una línea en cada paso del bucle descartando la anterior si no se almacena, logrando un consumo de RAM constante $O(1)$ independientemente de si el archivo pesa 10 KB o 50 GB.

**Diferencia exacta entre `.write()` y `.writelines()`.** Ninguno de los dos métodos añade saltos de línea `"\n"` por su cuenta:

- `f.write(cadena)` escribe un único `str` y retorna la cantidad de caracteres escritos (`int`).
- `f.writelines(iterable_de_cadenas)` recorre cualquier iterable de `str` y escribe cada elemento uno tras otro (`Editar_TXT.py` L13-14), retornando `None`.
- **Corrección importante sobre `problema_txt.py` (L86 y L94):** allí se escribió `archivo.writelines(f"Nombre: {name}\n...")` pasando una cadena formateada en lugar de una lista de cadenas. En Python esa instrucción no falla únicamente porque un `str` es iterable carácter por carácter, lo que fuerza a `writelines` a iterar letra por letra sobre toda la cadena. Cuando ya se dispone de una única cadena `f"..."`, el método correcto y directo es siempre `archivo.write(...)`.

**Rutas multiplataforma con `pathlib.Path`.** La biblioteca estándar ofrece desde Python 3.4 el módulo `pathlib`, cuya clase `Path` reemplaza la concatenación manual de barras invertidas (`"C:\\Users\\..."`) por el operador `/` que adapta automáticamente el separador al sistema operativo (`/` en Linux/macOS, `\` en Windows) y provee atajos seguros como `ruta.read_text(encoding="utf-8")` y `ruta.write_text(contenido, encoding="utf-8")` (que internamente abren y cierran el archivo mediante un bloque `with`).

## 4. Sintaxis y funcionamiento

Patrón estándar de lectura y escritura segura con `pathlib.Path` y `with open(...)`:

```text
from pathlib import Path

ruta = Path(<directorio>) / "<nombre_archivo>.txt"

with open(ruta, mode="<modo>", encoding="utf-8") as <flujo>:
    <operaciones_sobre_el_flujo>
```

Referencia de modos, métodos y operaciones sobre archivos:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `open(p, "r", encoding="utf-8")` | Abre archivo de texto existente solo para lectura | `with open(p, "r", encoding="utf-8") as f:` |
| 2 | `open(p, "w", encoding="utf-8")` | Crea o **trunca a 0 bytes** el archivo para escritura | `with open(p, "w", encoding="utf-8") as f:` |
| 3 | `open(p, "a", encoding="utf-8")` | Abre para agregar al final sin borrar contenido previo | `with open(p, "a", encoding="utf-8") as f:` |
| 4 | `open(p, "x", encoding="utf-8")` | Crea archivo nuevo; lanza `FileExistsError` si ya existe | `with open(p, "x", encoding="utf-8") as f:` |
| 5 | `open(p, "rb")` / `"wb"` | Modo binario crudo (`bytes`), sin `encoding` | `with open(img, "rb") as f:` |
| 6 | `for linea in f:` | Iteración perezosa línea a línea con memoria constante $O(1)$ | `for ln in f: procesar(ln.rstrip("\n"))` |
| 7 | `f.read(n)` | Lee todo el resto del flujo (o hasta `n` caracteres) | `texto = f.read()` |
| 8 | `f.readline(n)` | Lee una línea (o hasta `n` caracteres de la línea actual) | `encabezado = f.readline()` |
| 9 | `f.readlines()` | Carga todas las líneas restantes en una `list[str]` | `lineas = f.readlines()` |
| 10 | `f.write(s)` | Escribe la cadena `s` y devuelve el número de caracteres `int` | `n = f.write("Registro\n")` |
| 11 | `f.writelines(seq)` | Escribe cada cadena del iterable `seq` sin agregar `"\n"` | `f.writelines(["a\n", "b\n"])` |
| 12 | `f.tell()` / `f.seek(pos)` | Consulta o reposiciona (en bytes) el cursor del flujo | `f.seek(0)` |
| 13 | `Path.read_text` / `write_text` | Abre, lee o sobrescribe texto completo y cierra en un paso | `ruta.read_text(encoding="utf-8")` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Escritura (`"w"`), adición (`"a"`), caracteres UTF-8 y control explícito del cursor (`tell` y `seek`).**

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "bitacora.txt"

    # 1. Escritura inicial en modo "w" con codificación UTF-8 explícita
    with open(ruta, mode="w", encoding="utf-8", newline="\n") as archivo:
        lineas_iniciales = [
            "Inicio de bitácora del sistema\n",
            "Verificación de diéresis y eñe: agüita, año\n",
        ]
        archivo.writelines(lineas_iniciales)

    # 2. Adición al final en modo "a" sin truncar lo anterior
    with open(ruta, mode="a", encoding="utf-8", newline="\n") as archivo:
        caracteres = archivo.write("Cierre de verificación correcto\n")
        print("Caracteres agregados con write():", caracteres)

    # 3. Lectura y demostración del cursor de flujo
    with open(ruta, mode="r", encoding="utf-8") as archivo:
        contenido_1 = archivo.read()
        lectura_agotada = archivo.read()
        print("Posición tras agotar el flujo (bytes):", archivo.tell())
        print("Segunda lectura sin seek(0):", repr(lectura_agotada))

        archivo.seek(0)
        primera_linea = archivo.readline().rstrip("\n")
        print("Primera línea tras seek(0):", primera_linea)

    print("¿Archivo cerrado fuera de 'with'?:", archivo.closed)
    print("Total de líneas persistidas:", len(contenido_1.splitlines()))
```

Explicación paso a paso:

- Se emplea `pathlib.Path` sobre un directorio temporal aislado y `encoding="utf-8"` en las tres aperturas, preservando intactos los caracteres `"á"`, `"ó"`, `"é"`, `"ü"` y `"ñ"` (que ocupan dos bytes cada uno en UTF-8, razón por la que `tell()` reporta `114` bytes frente a `108` caracteres Unicode).
- Se demuestra experimentalmente por qué una segunda llamada a `archivo.read()` devuelve `''`: el cursor ya se encuentra al final del flujo, y basta invocar `archivo.seek(0)` para volver a leer desde el principio.
- Al salir del bloque `with`, `archivo.closed` confirma `True` de forma determinista.

Resultado esperado:

```text
Caracteres agregados con write(): 32
Posición tras agotar el flujo (bytes): 114
Segunda lectura sin seek(0): ''
Primera línea tras seek(0): Inicio de bitácora del sistema
¿Archivo cerrado fuera de 'with'?: True
Total de líneas persistidas: 3
```

### Intermedio

**Ejemplo 2 — Procesamiento perezoso línea a línea ($O(1)$ en RAM) y generación estructurada de reporte con `zip`.**

```python
import tempfile
from pathlib import Path


def persistir_personas(
    ruta_destino: Path,
    nombres: list[str],
    apellidos: list[str],
    edades: list[int],
) -> None:
    with open(ruta_destino, mode="w", encoding="utf-8") as salida:
        for nombre, apellido, edad in zip(nombres, apellidos, edades, strict=True):
            salida.write(f"{nombre.strip().title()}|{apellido.strip().title()}|{edad}\n")


def filtrar_mayores_en_streaming(ruta_origen: Path, edad_minima: int = 18) -> list[str]:
    seleccionados: list[str] = []
    with open(ruta_origen, mode="r", encoding="utf-8") as entrada:
        for numero_linea, linea in enumerate(entrada, start=1):
            texto = linea.strip()
            if not texto:
                continue
            nombre, apellido, edad_txt = texto.split("|")
            edad = int(edad_txt)
            if edad >= edad_minima:
                seleccionados.append(f"L{numero_linea}: {nombre} {apellido} ({edad} años)")
    return seleccionados


with tempfile.TemporaryDirectory() as tmp_dir:
    archivo_datos = Path(tmp_dir) / "personas.txt"
    persistir_personas(
        archivo_datos,
        nombres=["flavio", "joaquin", "fabian", "camila"],
        apellidos=["silva", "salazar", "silva", "dalto"],
        edades=[18, 7, 21, 24],
    )
    for registro in filtrar_mayores_en_streaming(archivo_datos, edad_minima=18):
        print(registro)
```

Explicación técnica:

- Refactorizando `problema_txt.py` (L81-95), la lógica se desacopla de `input()`, valida con `zip(..., strict=True)` que las tres listas tengan idéntica longitud y utiliza `salida.write(...)` en vez de pasar un `str` a `writelines(...)`.
- En `filtrar_mayores_en_streaming`, iterar directamente sobre `entrada` con `enumerate` procesa una única línea en memoria a la vez, patrón óptimo para archivos masivos de registros.

Resultado esperado:

```text
L1: Flavio Silva (18 años)
L3: Fabian Silva (21 años)
L4: Camila Dalto (24 años)
```

### Avanzado

**Ejemplo 3 — Escritura atómica resistente a fallos (*atomic write*) mediante archivo temporal y `os.replace`.**

```python
import os
import tempfile
from pathlib import Path


def escribir_texto_atomico(destino: Path, contenido: str) -> None:
    """Sobrescribe 'destino' de forma atómica evitando archivos truncados a medias."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    fd, ruta_temporal_str = tempfile.mkstemp(
        dir=destino.parent, prefix=f".{destino.name}.", suffix=".tmp"
    )
    ruta_temporal = Path(ruta_temporal_str)
    try:
        with os.fdopen(fd, mode="w", encoding="utf-8") as flujo_tmp:
            flujo_tmp.write(contenido)
            flujo_tmp.flush()
            os.fsync(flujo_tmp.fileno())
        os.replace(ruta_temporal, destino)
    except Exception:
        ruta_temporal.unlink(missing_ok=True)
        raise


with tempfile.TemporaryDirectory() as tmp_dir:
    config = Path(tmp_dir) / "estado_produccion.conf"
    config.write_text("version=1\nestado=estable\n", encoding="utf-8")

    try:
        # Simulamos cómo un reemplazo exitoso actualiza íntegramente el destino
        escribir_texto_atomico(config, "version=2\nestado=actualizado\n")
    except OSError as err:
        print("Error de E/S:", err)

    print(config.read_text(encoding="utf-8").strip())
```

Explicación de confiabilidad en producción:

- Si se abre directamente un archivo crítico de configuración con `open(destino, "w")` y el proceso sufre un corte eléctrico o una excepción antes de terminar de escribir, el archivo original habrá quedado destruido o incompleto (corrupto).
- Escribir primero en un archivo temporal dentro del **mismo directorio** (mismo sistema de archivos), forzar su volcado físico con `flush()` + `os.fsync()` y permutar el inodo final con `os.replace()` garantiza atomicidad a nivel del sistema operativo: cualquier lector observará siempre la versión antigua completa o la versión nueva completa, nunca un estado intermedio truncado.

Resultado esperado:

```text
version=2
estado=actualizado
```

## 6. Aplicaciones en el mundo real

- **Análisis e ingesta de bitácoras (*log parsing*):** recorrer en *streaming* archivos de acceso de servidores web (Nginx, Apache) o trazas de aplicaciones de varios gigabytes buscando patrones de error sin saturar la memoria del contenedor.
- **Generación de reportes, recibos y plantillas de texto:** exportar resúmenes contables, archivos Markdown, scripts SQL de migración o manifiestos de configuración codificados en UTF-8.
- **Persistencia local de estado y cachés en herramientas CLI:** leer y actualizar archivos de configuración en directorios de usuario (`~/.config/`) de forma atómica y segura.
- **Verificación de integridad binaria (*hashing*):** abrir archivos grandes en modo `"rb"` leyendo bloques fijos (`while bloque := f.read(65536):`) para calcular sumas SHA-256 sin cargar el archivo completo en RAM.

## 7. Uso en producción

- **Declarar `encoding="utf-8"` sin excepción en todo archivo de texto:** activar en pruebas e integración continua la variable de entorno `PYTHONWARNDEFAULTENCODING=1` (o `PYTHONUTF8=1`, **PEP 540** / **PEP 686**) permite detectar de inmediato cualquier llamada a `open()` o `Path.read_text()` que haya olvidado fijar la codificación.
- **Construir rutas relativas al módulo o por configuración, nunca literales locales:** si un módulo necesita cargar un archivo de recursos adjunto, debe resolverlo respecto a su propia ubicación con `Path(__file__).resolve().parent / "recursos" / "plantilla.txt"`, o bien recibir la ruta mediante variables de entorno o argumentos CLI.
- **Prevenir vulnerabilidades de recorrido de directorios (*Path Traversal*):** cuando el nombre de un archivo provenga de una petición externa del usuario, nunca debe concatenarse directamente; debe validarse con `ruta_candidata = (directorio_base / nombre_usuario).resolve()` comprobando `ruta_candidata.is_relative_to(directorio_base.resolve())` antes de llamar a `open()`.
- **Elegir el formato adecuado cuando los datos son estructurados:** almacenar registros con múltiples campos mediante separadores artesanales como `"----------"` (`problema_txt.py` L86-94) complica su lectura posterior. Para datos tabulares debe emplearse [CSV](archivos_csv.md) o Parquet, y para estructuras jerárquicas JSON (`json`) o TOML (`tomllib`).

## 8. Errores comunes y recomendaciones

1. **Abrir con `"w"` creyendo que agrega contenido o solo abre para consultar (pérdida inmediata de datos).**

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "notas.txt"
    ruta.write_text("Información valiosa previa\n", encoding="utf-8")

    # Incluso sin llamar a write(), abrir con "w" trunca el archivo a 0 bytes
    with open(ruta, mode="w", encoding="utf-8"):
        pass

    print("Tamaño tras abrir con 'w' sin escribir:", ruta.stat().st_size, "bytes")
```

Resultado esperado:

```text
Tamaño tras abrir con 'w' sin escribir: 0 bytes
```

Diagnóstico: el modo `"w"` trunca el archivo existente en el instante mismo de abrirlo. Recomendación: utilizar `"a"` para añadir al final, `"x"` cuando se desea fallar si el archivo ya existe y `"r"` para lectura.

2. **Intentar leer o escribir sobre el flujo fuera del bloque `with` (`ValueError`).**

```python
# ERROR INTENCIONAL: ValueError al operar sobre un archivo ya cerrado al salir de 'with'
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "ejemplo.txt"
    ruta.write_text("línea única\n", encoding="utf-8")

    with open(ruta, mode="r", encoding="utf-8") as f:
        pass

    contenido = f.read()
```

Diagnóstico: tal como se observa al descomentar la línea 48 de `archivos_txt.py`, operar sobre un flujo cerrado dispara `ValueError: I/O operation on closed file`. Solución: realizar toda lectura o transformación necesaria dentro del bloque indentado de `with` y guardar en variables los datos ya extraídos.

3. **Olvidar saltos de línea en `.writelines()` o pasarle un `str` suelto.**

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta = Path(tmp_dir) / "lista.txt"
    palabras = ["uno", "dos", "tres"]

    with open(ruta, mode="w", encoding="utf-8") as f:
        # Sin "\n", todas las cadenas quedan pegadas en una sola línea: "unodostres"
        f.writelines(f"{p}\n" for p in palabras)

    print(ruta.read_text(encoding="utf-8").splitlines())
```

Resultado esperado:

```text
['uno', 'dos', 'tres']
```

Recomendación: añadir explícitamente `"\n"` mediante una expresión generadora en `writelines(...)` o escribir `"\n".join(palabras) + "\n"` con `.write(...)`.

4. **Omitir `encoding="utf-8"` al intercambiar archivos entre sistemas operativos.** Leer en Windows (`cp1252`) un archivo UTF-8 sin declarar `encoding="utf-8"` corrompe los caracteres no ASCII o interrumpe la ejecución con `UnicodeDecodeError`.

## 9. Resumen

- El manejo de archivos en Python descansa sobre descriptores finitos del sistema operativo envueltos por las capas de búfer y codificación del módulo estándar `io`.
- El bloque `with open(ruta, mode=..., encoding="utf-8") as f:` constituye el estándar obligatorio para garantizar el volcado de búferes y el cierre determinista del archivo ante cualquier circunstancia.
- El modo `"r"` lee sin modificar, `"w"` sobrescribe truncando de inmediato el archivo previo, `"a"` añade al final, `"x"` protege contra colisiones de archivos existentes y `"rb"`/`"wb"` procesan `bytes` binarios puros.
- Todo flujo mantiene un cursor interno consultable con `tell()` y reubicable con `seek()`; para archivos extensos debe preferirse la iteración perezosa `for linea in f:` ($O(1)$ en memoria) frente a `.read()` o `.readlines()`.
- La clase `pathlib.Path` de la biblioteca estándar permite construir rutas multiplataforma limpias y seguras sin depender de cadenas codificadas para un único sistema operativo.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_TXT/archivos_txt.py` (L1-51) | `archivos_txt.py` | Apertura con `open()`, `.read()`, `.readlines()`, `.readline()`, `.readline(21)` y cierre manual con `.close()` | Se corrigió la causa real por la que `readlines()` devuelve `[]` tras `read()` (cursor en *EOF*, `tell`/`seek`) y el comportamiento exacto de `readline(size)` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_TXT/Leer_TXT_Optimamente.py` (L1-16) | `Leer_TXT_Optimamente.py` | Lectura con gestor de contexto `with open(..., encoding="UTF-8") as archivo:` | Se explicó el protocolo `__enter__`/`__exit__`, aclarando que `with` no suprime excepciones sino que garantiza el cierre determinista, y se fundamentó PEP 597 |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_TXT/Editar_TXT.py` (L1-15) | `Editar_TXT.py` | Permiso de escritura `"w"` y escritura de listas de cadenas con `.writelines([...])` | Se advirtió sobre el truncado instantáneo a 0 bytes del modo `"w"` y se introdujo el patrón de escritura atómica en producción |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_TXT/Agregar_TXT.py` (L1-23) | `Agregar_TXT.py` | Modo `"a"` (*append*), `.write()` y escritura iterativa con bucle `for` | Se contrastó `"a"` frente a `"w"` y `"x"`, desacoplando la persistencia respecto de la lectura por `input()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_TXT/Mi_Arcivo_TXT.txt` (L1-16) | `Mi_Arcivo_TXT.txt` | Archivo de prueba con caracteres UTF-8 (`"agüita"`, `"línea"`) generado con `"w"` y `"a"` | Empleado para ilustrar el impacto multiplataforma de UTF-8 frente a `cp1252` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/problema_txt.py` (L81-95) | `problema_txt.py` | Escritura combinada de listas `nombres`, `apellidos` y `edades` con `zip` y `range` | Se corrigió el uso de `archivo.writelines(f"...")` sobre un `str` individual explicando por qué debe emplearse `archivo.write(f"...")` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/nombre_apellido_edad.txt` (L1-31) | `nombre_apellido_edad.txt` | Salida textual de registros separados por guiones | Se contrastó con delimitadores estructurados y formatos tabulares estándar |

**Fundamento complementario:** se incorporaron cinco componentes fundamentales de la biblioteca estándar de Python para un dominio completo del tema: (1) la arquitectura interna en tres capas del módulo `io` (`FileIO`, búfer binario y `TextIOWrapper`); (2) los modos `"x"`, `"r+"` y binarios (`"rb"`/`"wb"`); (3) el estándar **PEP 597** sobre codificación explícita; (4) la gestión multiplataforma de rutas con `pathlib.Path`; y (5) el patrón de escritura atómica con `tempfile` y `os.replace` junto con la prevención de *Path Traversal*.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files> — Tutorial oficial de Python: lectura y escritura de archivos, modos, gestor `with` y métodos de objetos archivo.
- <https://docs.python.org/3/library/functions.html#open> — Biblioteca estándar (`open`): firma completa, tabla de modos de apertura, codificación y manejo de saltos de línea.
- <https://docs.python.org/3/library/io.html> — Biblioteca estándar (`io`): jerarquía de flujos crudos, binarios con búfer y flujos de texto (`TextIOWrapper`).
- <https://docs.python.org/3/library/pathlib.html> — Biblioteca estándar (`pathlib`): rutas del sistema de archivos orientadas a objetos (`Path`, `read_text`, `write_text`).
- <https://peps.python.org/pep-0597/> — PEP 597 (*Add optional EncodingWarning*): justificación técnica del uso explícito de `encoding="utf-8"` al abrir archivos de texto.
