# Procesamiento de Archivos CSV con la Biblioteca Estándar

## 2. Introducción

El formato **CSV** (*Comma-Separated Values*, valores separados por comas) es uno de los estándares más extendidos en la industria para el intercambio ligero de información tabular entre bases de datos relacionales, aplicaciones empresariales, sistemas heredados y hojas de cálculo (`Leer_CSV.py` L2-4).

Aunque a simple vista un archivo CSV parece una secuencia trivial de líneas de texto divididas por comas, intentar procesarlo manualmente con `linea.split(",")` produce errores graves en cuanto un texto real incluye comas internas, comillas dobles o saltos de línea dentro de una celda.

Python incluye en su **biblioteca estándar** el módulo `csv` (respaldado en CPython por la extensión en C `_csv`), cuyo dominio técnico aporta cuatro capacidades fundamentales:

1. **Análisis gramatical conforme a RFC 4180:** interpreta con exactitud delimitadores, campos entrecomillados (`Datos.csv` L1-7), comillas escapadas y saltos de línea embebidos sin dependencias externas.
2. **Lectura y escritura semántica por nombre de columna:** además de listas posicionales (`csv.reader` / `csv.writer`), provee `csv.DictReader` y `csv.DictWriter` para trabajar con [diccionarios](../chapter-one/diccionarios.md) resilientes ante cambios en el orden de las columnas.
3. **Procesamiento en *streaming* con memoria constante $O(1)$:** consume e inyecta registros uno a uno mediante [iteradores](../../Avanzado/chapter-one/iteradores.md), permitiendo transformar archivos de decenas de gigabytes donde cargar una tabla completa en RAM resultaría inviable.
4. **Exportación segura e interoperable:** configurar `newline=""`, `encoding="utf-8"`, dialectos regionales (`;`) y saneamiento frente a inyección de fórmulas garantiza archivos íntegros en cualquier sistema operativo y motor de hojas de cálculo.

## 3. Fundamentos y conceptos

**Anatomía del estándar RFC 4180 y el fracaso de `str.split(",")`.** Un documento CSV representa una única tabla bidimensional en texto plano sin metadatos nativos de tipos de datos:

- Cada registro suele ocupar una línea terminada en `CRLF` (`\r\n`) o `LF` (`\n`), con una primera fila opcional de encabezados (`"nombre","apellido","edad"` en `Datos.csv` L1).
- Los campos se separan mediante un carácter delimitador (por defecto `,`, aunque en configuraciones regionales de Europa y América Latina donde la coma es separador decimal es habitual `;`).
- Cualquier campo que contenga el delimitador, un salto de línea o comillas dobles **debe encerrarse entre comillas dobles (`"`)**, y toda comilla doble literal dentro del campo se escapa duplicándola (`""`).

Si una fila contiene `"Silva, Flavio"," Lima, Perú",18`, evaluar `linea.split(",")` la fragmentará erróneamente en `5` pedazos con comillas sueltas en lugar de `3` columnas. El autómata finito de `csv.reader` reconoce el estado de apertura y cierre de comillas y entrega exactamente `['Silva, Flavio', ' Lima, Perú', '18']`.

**Naturaleza de los datos leídos: todo campo ingresa como `str`.** A diferencia de formatos binarios tipados (como Parquet o bases SQL), un archivo CSV puro almacena únicamente texto. Al iterar sobre `csv.reader(archivo_csv)` (`Leer_CSV.py` L18-23), el objeto devuelto es un iterador perezoso donde cada fila es una `list[str]`. Incluso valores numéricos como `18` en `Datos.csv` o `18.0` en `archivo.csv` se leen inicialmente como cadenas `'18'` y `'18.0'`, por lo que el código de aplicación debe convertirlos explícitamente (`int()`, `float()`, `Decimal`) antes de realizar operaciones aritméticas.

**El requisito obligatorio `newline=""` al abrir el archivo.** En `Leer_CSV.py` (L13) se abrió el archivo únicamente con `open(ruta)`. Sin embargo, la documentación oficial de la biblioteca estándar de Python estipula que todo archivo pasado a objetos del módulo `csv` **debe abrirse siempre con `newline=""`** junto con [codificación explícita](manejo_archivos.md) `encoding="utf-8"`:

- **En escritura (`mode="w"` o `"a"`):** `csv.writer` escribe por defecto el terminador estándar `\r\n`. Si en Windows no se especifica `newline=""`, la capa `TextIOWrapper` traduce automáticamente cada `\n` a `\r\n`, transformando `\r\n` en `\r\r\n` e insertando **una fila en blanco vacía entre cada registro escrito**.
- **En lectura (`mode="r"`):** `newline=""` desactiva la división prematura de saltos de línea en `TextIOWrapper`, permitiendo que el analizador `csv` distinga correctamente entre un salto de línea que cierra un registro y un salto de línea incrustado legítimamente dentro de una celda entrecomillada.

**Lectores y escritores posicionales frente a basados en diccionarios.** El módulo `csv` ofrece dos pares complementarios de interfaces:

1. **Interfaz posicional (`csv.reader` y `csv.writer`):** representa cada fila como una secuencia indexada por posición (`fila[0]`, `fila[1]`). Tiene una sobrecarga mínima de CPU y memoria, idónea cuando el esquema es pequeño e invariable o el archivo carece de fila de encabezados.
2. **Interfaz por clave (`csv.DictReader` y `csv.DictWriter`):** utiliza la primera fila (o la secuencia `fieldnames` indicada) como claves de un `dict[str, str]` por cada registro (`fila["ingresos"]`). Desacopla el código de la posición física de las columnas: si el proveedor externo inserta una columna nueva en medio del archivo, `fila["ingresos"]` continúa apuntando al dato correcto sin romper índices numéricos fijos.

**Dialectos, delimitadores personalizados y espacios tras la coma.** El comportamiento léxico de `csv` se ajusta mediante parámetros clave:

- `delimiter`: carácter separador de campos (por ejemplo, `";"` o `"\t"` para archivos TSV).
- `quotechar`: carácter de encerramiento (por defecto `'"'`).
- `quoting`: política de entrecomillado al escribir (`csv.QUOTE_MINIMAL` por defecto, `csv.QUOTE_ALL` como en los textos de `Datos.csv`, `csv.QUOTE_NONNUMERIC` o `csv.QUOTE_NONE`).
- `skipinitialspace=True`: ignora los espacios inmediatamente posteriores al delimitador. Resuelve de raíz el inconveniente descrito en los comentarios de `Importando_con_pandas.py` (L35-44), donde escribir `"nombre", "apellido"` (con espacio tras la coma) hacía que el encabezado se interpretase literalmente como `' "apellido"'` con comillas incluidas.

**Criterio profesional de elección: módulo `csv` frente a `pandas.read_csv`.** En `Importando_con_pandas.py` (L2-5) se afirma que en entornos profesionales siempre conviene usar Pandas en lugar de `csv`. En ingeniería de producción la decisión real depende del caso de uso y del perfil de memoria:

| Criterio | `csv` (biblioteca estándar) | `pandas` (biblioteca externa) |
|---|---|---|
| Instalación y peso | Integrado en Python (0 dependencias) | Requiere instalar `pandas` y `numpy` |
| Consumo de RAM | Constante $O(1)$ en *streaming* fila a fila | Proporcional al archivo $O(N)$ en memoria columnar |
| Caso óptimo | Archivos gigantescos (multi-GB), microservicios ligeros, validación/migración fila por fila, respuesta HTTP en *streaming* | Análisis exploratorio, agregaciones grupales, cruces tabulares (*merge*), limpieza estadística y [visualización](visualizacion.md) |

**Seguridad en producción: inyección de fórmulas en hojas de cálculo (*CSV Injection*).** Cuando una aplicación web exporta a CSV textos ingresados por usuarios externos (nombres, comentarios, direcciones) y un operador administrativo abre ese archivo en Microsoft Excel, LibreOffice Calc o Google Sheets, cualquier celda cuyo primer carácter sea `=`, `+`, `-`, `@`, tabulación (`\t`) o retorno de carro (`\r`) es evaluada como una **fórmula activa**, pudiendo exfiltrar celdas o invocar comandos externos. Para reportes destinados a hojas de cálculo, debe anteponerse una comilla simple `'` (o neutralizar el prefijo peligroso) en las cadenas de texto que comiencen con dichos símbolos.

## 4. Sintaxis y funcionamiento

Patrones canónicos de lectura y escritura CSV con la biblioteca estándar:

```text
import csv

with open(ruta, mode="r", newline="", encoding="utf-8") as entrada:
    lector = csv.DictReader(entrada, delimiter=",")
    for fila in lector:
        <procesar_diccionario_fila>

with open(ruta, mode="w", newline="", encoding="utf-8") as salida:
    escritor = csv.DictWriter(salida, fieldnames=["col1", "col2"])
    escritor.writeheader()
    escritor.writerow({"col1": "valor1", "col2": 10})
```

Componentes principales del módulo estándar `csv`:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `newline=""` | Argumento obligatorio en `open()` para evitar filas vacías dobles y cortes erróneos | `open(p, "w", newline="", encoding="utf-8")` |
| 2 | `csv.reader(f)` | Iterador que entrega cada registro del archivo como `list[str]` | `for fila in csv.reader(f):` |
| 3 | `csv.writer(f)` | Escritor posicional de secuencias (`writerow`, `writerows`) | `w.writerow(["Ana", 25])` |
| 4 | `csv.DictReader(f)` | Iterador que entrega cada fila como `dict[str, str]` usando encabezados | `for r in csv.DictReader(f):` |
| 5 | `csv.DictWriter(f, fieldnames)` | Escritor basado en diccionarios; requiere `fieldnames` explícito | `dw.writeheader()` |
| 6 | `delimiter` | Carácter de separación entre celdas (por defecto `","`) | `csv.reader(f, delimiter=";")` |
| 7 | `skipinitialspace` | Si es `True`, descarta espacios inmediatamente posteriores al delimitador | `csv.reader(f, skipinitialspace=True)` |
| 8 | `quoting` | Controla cuándo rodear campos con `quotechar` al exportar | `quoting=csv.QUOTE_NONNUMERIC` |
| 9 | `extrasaction` | En `DictWriter`, define qué hacer con claves extra (`"raise"` o `"ignore"`) | `extrasaction="ignore"` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Comparación entre `str.split(",")` y `csv.reader` ante comas internas, comillas escapadas y espacios tras delimitador.**

```python
import csv
import io

CONTENIDO_CSV = (
    '"cliente", "ciudad", "concepto", "monto"\r\n'
    '"Silva, Flavio", "Lima, Perú", "Monitor 27"" IPS", 320.50\r\n'
    '"Dalto, Camila", "Buenos Aires", "Teclado mecánico", 95.00\r\n'
)

primera_fila_datos = CONTENIDO_CSV.splitlines()[1]
print("Partición ingenua con split(','):", len(primera_fila_datos.split(",")), "fragmentos")

flujo_memoria = io.StringIO(CONTENIDO_CSV)
lector = csv.reader(flujo_memoria, skipinitialspace=True)
encabezados = next(lector)
print("Encabezados limpios:", encabezados)

for cliente, ciudad, concepto, monto_txt in lector:
    monto = float(monto_txt)
    print(f"{cliente} | {ciudad} | {concepto} | USD {monto:.2f}")
```

Explicación paso a paso:

- `primera_fila_datos.split(",")` rompe erróneamente la fila en `6` fragmentos porque divide por las comas internas de `"Silva, Flavio"` y `"Lima, Perú"`.
- `csv.reader(..., skipinitialspace=True)` consume el encabezado con `next(lector)` eliminando los espacios tras cada coma, deshace el escape `""` en `'Monitor 27" IPS'` y entrega exactamente los `4` campos esperados por registro, convirtiendo `monto_txt` a `float`.

Resultado esperado:

```text
Partición ingenua con split(','): 6 fragmentos
Encabezados limpios: ['cliente', 'ciudad', 'concepto', 'monto']
Silva, Flavio | Lima, Perú | Monitor 27" IPS | USD 320.50
Dalto, Camila | Buenos Aires | Teclado mecánico | USD 95.00
```

### Intermedio

**Ejemplo 2 — Escritura y lectura tipada con `DictWriter` y `DictReader` empleando delimitador regional (`;`).**

```python
import csv
import tempfile
from pathlib import Path

INGRESOS = [
    {"fuente": "Trabajo fijo", "ingresos": 3000, "auditado": "si", "nota_interna": "nómina"},
    {"fuente": "Freelance", "ingresos": 800, "auditado": "si", "nota_interna": "proyecto web"},
    {"fuente": "Youtube regalías", "ingresos": 350, "auditado": "no", "nota_interna": "pendiente"},
    {"fuente": "Consultoría", "ingresos": 600, "auditado": "si", "nota_interna": "arquitectura"},
]

with tempfile.TemporaryDirectory() as tmp_dir:
    ruta_csv = Path(tmp_dir) / "ingresos_regional.csv"
    campos_publicos = ["fuente", "ingresos", "auditado"]

    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as salida:
        escritor = csv.DictWriter(
            salida,
            fieldnames=campos_publicos,
            delimiter=";",
            extrasaction="ignore",
        )
        escritor.writeheader()
        escritor.writerows(INGRESOS)

    total_auditado = 0
    with open(ruta_csv, mode="r", newline="", encoding="utf-8") as entrada:
        for fila in csv.DictReader(entrada, delimiter=";"):
            if fila["auditado"] == "si":
                total_auditado += int(fila["ingresos"])

    print("Primera línea física del archivo:", ruta_csv.read_text(encoding="utf-8").splitlines()[0])
    print(f"Total de ingresos auditados: {total_auditado} USD")
```

Explicación técnica:

- Inspirado en los datos de `grafico_barras.csv`, `DictWriter` exporta únicamente `campos_publicos` ignorando limpiamente `"nota_interna"` gracias a `extrasaction="ignore"` y empleando `";"` como delimitador.
- `DictReader` reconstruye cada fila como diccionario permitiendo consultar `fila["auditado"]` y `int(fila["ingresos"])` por nombre semántico en lugar de índices numéricos propensos a errores.

Resultado esperado:

```text
Primera línea física del archivo: fuente;ingresos;auditado
Total de ingresos auditados: 4400 USD
```

### Avanzado

**Ejemplo 3 — Tubería ETL en *streaming* ($O(1)$ en RAM) con validación de filas defectuosas y protección contra *CSV Formula Injection*.**

```python
import csv
import tempfile
from pathlib import Path

PREFIJOS_FORMULA = ("=", "+", "-", "@", "\t", "\r")


def sanear_celda_hoja_calculo(valor: str) -> str:
    """Neutraliza prefijos ejecutables en Excel/Calc anteponiendo un apóstrofo."""
    texto = valor.strip()
    if texto.startswith(PREFIJOS_FORMULA):
        return f"'{texto}"
    return texto


def transformar_csv_seguro(origen: Path, destino: Path) -> tuple[int, int]:
    aceptados = 0
    rechazados = 0
    with (
        open(origen, mode="r", newline="", encoding="utf-8") as f_in,
        open(destino, mode="w", newline="", encoding="utf-8") as f_out,
    ):
        lector = csv.DictReader(f_in)
        escritor = csv.DictWriter(f_out, fieldnames=["usuario", "comentario", "edad"])
        escritor.writeheader()

        for fila in lector:
            try:
                edad = int(fila["edad"])
                if edad <= 0:
                    raise ValueError("edad no positiva")
            except (TypeError, ValueError):
                rechazados += 1
                continue

            escritor.writerow(
                {
                    "usuario": sanear_celda_hoja_calculo(fila["usuario"] or ""),
                    "comentario": sanear_celda_hoja_calculo(fila["comentario"] or ""),
                    "edad": edad,
                }
            )
            aceptados += 1
    return aceptados, rechazados


with tempfile.TemporaryDirectory() as tmp_dir:
    ruta_cruda = Path(tmp_dir) / "entrada_usuarios.csv"
    ruta_limpia = Path(tmp_dir) / "salida_segura.csv"

    ruta_cruda.write_text(
        "usuario,comentario,edad\n"
        'flavio,"Registro normal, verificado",18\n'
        'atacante,"=HYPERLINK(""http://malicioso.ejemplo"",""Click"")",25\n'
        "incompleto,edad invalida,abc\n",
        encoding="utf-8",
    )

    ok, err = transformar_csv_seguro(ruta_cruda, ruta_limpia)
    print(f"Filas aceptadas: {ok} | Filas rechazadas: {err}")
    with open(ruta_limpia, mode="r", newline="", encoding="utf-8") as verificacion:
        for registro in csv.DictReader(verificacion):
            print(registro)
```

Explicación de arquitectura y seguridad:

- Abrir origen y destino simultáneamente en un único bloque `with (...)` procesa una fila a la vez sin almacenar listas intermedias en memoria: el mismo código funciona igual para `3` filas que para `30` millones de filas.
- Los registros con tipos inválidos (`"abc"`) se contabilizan y descartan sin abortar el lote completo, mientras que la fórmula `"=HYPERLINK(...)"` queda neutralizada como texto literal `"'=HYPERLINK(...)"`.

Resultado esperado:

```text
Filas aceptadas: 2 | Filas rechazadas: 1
{'usuario': 'flavio', 'comentario': 'Registro normal, verificado', 'edad': '18'}
{'usuario': 'atacante', 'comentario': '\'=HYPERLINK("http://malicioso.ejemplo","Click")', 'edad': '25'}
```

## 6. Aplicaciones en el mundo real

- **Intercambio bancario, contable y tributario:** conciliación de extractos de pagos, nóminas y libros electrónicos donde las entidades regulatorias exigen esquemas CSV estrictos con delimitadores y codificaciones específicas.
- **Descargas masivas en *streaming* desde aplicaciones web:** endpoints de FastAPI o Django (`StreamingHttpResponse`) que generan archivos CSV al vuelo con `io.StringIO` y `csv.writer` a medida que iteran un cursor de base de datos, evitando agotar la RAM del servidor.
- **Migración e ingesta hacia almacenes de datos (*Data Warehouses*):** preprocesamiento ligero, limpieza de encabezados y validación de tipos antes de ejecutar cargas masivas (`COPY` en PostgreSQL o carga hacia BigQuery/Snowflake).
- **Integración con sensores e instrumentación científica:** lectura secuencial de series de telemetría exportadas por equipos industriales o de laboratorio.

## 7. Uso en producción

- **Especificar siempre la dupla `newline=""` y `encoding="utf-8"` (o `"utf-8-sig"` para Excel en Windows):** cuando el consumidor directo del archivo será Microsoft Excel abriéndolo con doble clic en Windows, exportar con `encoding="utf-8-sig"` escribe la marca de orden de bytes (*UTF-8 BOM*, `\xef\xbb\xbf`), indicando inequívocamente a Excel que decodifique tildes y eñes como UTF-8; al leer archivos provenientes de Excel con `utf-8-sig`, Python descarta el BOM automáticamente sin contaminar el nombre de la primera columna.
- **Validar encabezados antes de iterar millones de filas:** comprobar al inicio que `set(campos_requeridos).issubset(lector.fieldnames or [])` permite fallar rápido (*fail-fast*) con un mensaje descriptivo si el archivo subido carece de una columna obligatoria.
- **Manejar filas cortas o largas en `DictReader`:** si una fila corrupta tiene más valores que encabezados, `DictReader` agrupa el excedente bajo la clave `restkey` (por defecto `None`); si tiene menos valores, rellena los faltantes con `restval` (por defecto `None`). Comprobar `if None in fila:` detecta inmediatamente filas con columnas desalineadas.
- **Migrar a formatos columnares tipados para analítica interna:** usar CSV en fronteras de interoperabilidad externa, pero preferir Apache Parquet o SQLite/PostgreSQL para almacenamiento analítico interno, ya que conservan tipos exactos, comprimen datos y evitan reanalizar texto en cada lectura.

## 8. Errores comunes y recomendaciones

1. **Intentar indexar directamente el objeto `csv.reader` o agotarlo dos veces.**

```python
# ERROR INTENCIONAL: TypeError al intentar indexar un iterador csv.reader como si fuese una lista
import csv
import io

lector = csv.reader(io.StringIO("a,b\n1,2\n"))
primera = lector[0]
```

Diagnóstico: como observaba intuitivamente `Leer_CSV.py` (L19), `csv.reader` no devuelve una lista en memoria sino un **iterador** de un solo recorrido: no soporta indexación `lector[0]` (`TypeError: '_csv.reader' object is not subscriptable`) y, una vez recorrido con `for`, un segundo bucle sobre el mismo `lector` producirá cero elementos. Solución: extraer la primera fila con `next(lector)` e iterar con `for`, o convertir a `list(lector)` únicamente si el archivo es pequeño.

2. **Operar aritméticamente con valores leídos de CSV sin convertir su tipo (`str` en lugar de `int`/`float`).**

```python
import csv
import io

flujo = io.StringIO("producto,cantidad\nteclado,3\nmonitor,2\n")
lector = csv.DictReader(flujo)
cantidades_texto = [fila["cantidad"] for fila in lector]

print("Concatenación accidental de str:", cantidades_texto[0] + cantidades_texto[1])
print("Suma numérica tras conversión:", int(cantidades_texto[0]) + int(cantidades_texto[1]))
```

Resultado esperado:

```text
Concatenación accidental de str: 32
Suma numérica tras conversión: 5
```

Diagnóstico: como toda celda en CSV llega como `str`, sumar `fila["cantidad"]` sin conversión concatena cadenas (`"3" + "2" == "32"`) o falla al comparar magnitudes (`"9" > "10"` es `True` lexicográficamente). Solución: convertir explícitamente cada campo numérico al leerlo.

3. **Omitir `newline=""` al escribir archivos CSV en Windows.** Produce líneas vacías intercaladas (`\r\r\n`) que alteran el conteo de registros en lectores estrictos.

4. **Dejar espacios tras las comas en CSV generados manualmente (`"a", "b"`).** Según RFC 4180, los espacios fuera de las comillas forman parte del campo y desactivan el reconocimiento de la comilla inicial salvo que el lector configure `skipinitialspace=True`. Al generar CSV debe escribirse `"a","b"` sin espacios superfluos tras el delimitador.

## 9. Resumen

- El módulo `csv` pertenece a la **biblioteca estándar de Python** e implementa el análisis y generación de datos tabulares conforme a **RFC 4180**, resolviendo comas internas, comillas escapadas (`""`) y saltos de línea embebidos donde `str.split(",")` fracasa.
- Todo archivo abierto para `csv` debe incluir `newline=""` y `encoding="utf-8"` (o `"utf-8-sig"` al interactuar con Excel en Windows).
- `csv.reader` y `csv.writer` operan sobre secuencias posicionales, mientras que `csv.DictReader` y `csv.DictWriter` vinculan cada celda al nombre de su columna mediante diccionarios.
- Todos los campos leídos por `csv` son inicialmente cadenas `str` y requieren conversión explícita de tipos antes de cálculos numéricos o comparaciones de orden.
- Para tuberías en *streaming* con memoria constante $O(1)$ y sin dependencias externas se prefiere `csv`; para transformaciones vectorizadas y analítica en memoria se emplea [Pandas](pandas_fundamentos.md). En exportaciones abiertas en hojas de cálculo debe mitigarse siempre la inyección de fórmulas.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Leer_CSV.py` (L1-23) | `Leer_CSV.py` | Importación de `csv`, apertura con `with open(...)` e iteración fila por fila con `csv.reader` | Se incorporaron los parámetros críticos `newline=""` y `encoding="utf-8"`, se explicó que `csv.reader` es un iterador perezoso y se añadieron `writer`, `DictReader` y `DictWriter` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Datos.csv` (L1-7) | `Datos.csv` | Encabezados y cadenas entre comillas dobles combinados con enteros sin comillas | Se conectó con las reglas gramaticales de RFC 4180, `quoting` y la lectura inicial como `str` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_CSV/Importando_con_pandas.py` (L2-10, L35-44) | `Importando_con_pandas.py` | Comparación preliminar con `csv` y problema de espacios intermedios entre comas y comillas | Se estableció una matriz rigurosa de decisión entre `csv` ($O(1)$ en RAM) y `pandas` ($O(N)$ columnar), mostrando cómo `skipinitialspace=True` resuelve los espacios tras comas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/EJERCICIOS_ARCHVOS/archivo.csv` (L1-4) | `archivo.csv` | Tabla simple sin comillas con edades decimales (`18.0`, `21.0`, `40.0`) | Utilizado para recalcar la necesidad de conversión explícita (`float`/`int`) al leer con `csv` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/ARCHIVOS_PROBLEMAS_GRAFICOS/grafico_barras.csv` (L1-6) | `grafico_barras.csv` | Registros categóricos y montos con tildes (`"Youtube regalías"`) | Reproducido y ampliado con `DictWriter`, `DictReader` y delimitadores regionales (`;`) |

**Fundamento complementario:** se incorporaron cinco pilares técnicos indispensables para trabajo profesional con archivos CSV: (1) la especificación formal **RFC 4180** frente a particiones ingenuas de cadenas; (2) el motivo técnico de `newline=""` en `TextIOWrapper`; (3) la lectura y escritura estructurada con `DictReader` y `DictWriter`; (4) el manejo de BOM (`utf-8-sig`) y delimitadores regionales (`;`); y (5) la prevención de *CSV Formula Injection* en exportaciones de producción.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/csv.html> — Biblioteca estándar (`csv`): referencia completa de `reader`, `writer`, `DictReader`, `DictWriter`, dialectos, constantes `QUOTE_*` y uso de `newline=""`.
- <https://docs.python.org/3/library/functions.html#open> — Biblioteca estándar (`open`): interacción entre `newline=""`, `encoding="utf-8"` y `encoding="utf-8-sig"`.
- <https://www.rfc-editor.org/rfc/rfc4180> — RFC 4180 (*Common Format and MIME Type for Comma-Separated Values (CSV) Files*): especificación estándar del formato CSV.
