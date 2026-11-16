# Procesamiento de Hojas de Cálculo Excel (`openpyxl` y `pandas`)

## 2. Introducción

En el ámbito empresarial, financiero y de análisis de datos, el formato **Microsoft Excel** (específicamente la especificación Office Open XML con extensión `.xlsx` y el formato heredado `.xls`) constituye uno de los estándares más difundidos para la distribución de reportes, tableros de control y tablas operativas.

A diferencia de los archivos planos delimitados como [archivos CSV](archivos_csv.md), un archivo `.xlsx` no es texto simple: es un paquete comprimido en formato ZIP que contiene múltiples documentos XML que describen celdas tipadas, hojas de cálculo independientes (*worksheets*), fórmulas matemáticas, formatos numéricos, estilos visuales y metadatos.

En el ecosistema Python, la interacción con hojas de cálculo se articula mediante dos herramientas fundamentales:

1. **`openpyxl`:** biblioteca especializada en la lectura, edición, formateo de celdas y manipulación integral de la estructura XML de libros Excel sin requerir tener instalado Microsoft Office.
2. **`pandas`:** biblioteca de alto nivel que utiliza motores subyacentes (como `openpyxl` o `calamine`) para ingerir y exportar estructuras bidimensionales `DataFrame` mediante `read_excel()` y `ExcelWriter`.

Dominar la gestión de archivos Excel en Python permite automatizar la ingesta masiva de reportes contables, consolidar múltiples hojas en una única estructura analítica y exportar resultados formateados profesionalmente.

## 3. Fundamentos y conceptos

**Estructura jerárquica de un archivo Excel.** El modelo de objetos de un archivo de hoja de cálculo se organiza en cuatro niveles anidados:

1. **Libro (*Workbook*):** representa el archivo físico completo (`.xlsx`), contenedor de todas las propiedades globales y colecciones de hojas.
2. **Hoja de cálculo (*Worksheet*):** superficie bidimensional de trabajo identificada por un nombre único (p. ej., `"Ventas_2025"`, `"Inventario"`).
3. **Fila (*Row*) y Columna (*Column*):** coordenadas de la cuadrícula; en Excel las columnas se identifican por letras (`A, B, C... Z, AA...`) y las filas por números base 1 (`1, 2, 3...`).
4. **Celda (*Cell*):** unidad mínima de almacenamiento que contiene un valor tipado (`string`, `number`, `boolean`, `datetime`), un formato visual y opcionalmente una fórmula de cálculo (`=SUMA(...)`).

**Motores de lectura y escritura en Python.** Para operar sobre archivos Excel, Python delega en bibliotecas externas especializadas:

| Motor | Formatos soportados | Ventajas principales | Rol en Pandas |
| :--- | :--- | :--- | :--- |
| **`openpyxl`** | `.xlsx`, `.xlsm`, `.xltx` | Estándar moderno, lectura/escritura, soporte de estilos y fórmulas. | Motor predeterminado de Pandas para `.xlsx`. |
| **`xlrd`** | `.xls` (formato binario legado) | Solo lectura de archivos antiguos de Excel 97-2003. | Motor exclusivo para `.xls`. |
| **`calamine`** | `.xlsx`, `.xls`, `.xlsb` | Motor escrito en Rust de lectura ultrarrápida para archivos gigantes. | Alternativa de alto rendimiento en Pandas 2.2+. |

**Cuándo utilizar Pandas frente a `openpyxl` directo:**
- **Utilizar `pandas` (`read_excel` / `to_excel`):** cuando el objetivo primordial es el **análisis numérico**, agregación, transformación de datos o limpieza de tablas completas que caben de forma tabular en un `DataFrame`.
- **Utilizar `openpyxl` nativo:** cuando se requiere preservar o aplicar **estilos visuales** (colores de fondo, bordes, fuentes tipográficas, anchos de columna), manipular fórmulas nativas sin evaluar o generar reportes ejecutivos con formatos corporativos rígidos.

## 4. Sintaxis y funcionamiento

Instalación de las dependencias requeridas en el entorno virtual:

```bash
pip install pandas openpyxl
```

Invocación típica de lectura con Pandas:

```python
import pandas as pd

# Lectura básica de una hoja específica
dataframe = pd.read_excel(
    "reporte.xlsx",
    sheet_name="Ventas",       # Nombre o índice (base 0) de la hoja; None carga todas las hojas en un dict
    header=0,                  # Fila utilizada como nombres de columna (base 0)
    usecols=["ID", "Importe"], # Subconjunto de columnas a cargar (por nombre o letras 'A:D')
    dtype={"ID": str},         # Especificación defensiva de tipos de datos
    engine="openpyxl",         # Motor explícito de lectura
)
```

Patrón de escritura múltiple en un mismo libro con `pd.ExcelWriter`:

```python
import pandas as pd

df_clientes = pd.DataFrame({"id": [1, 2], "nombre": ["Ana", "Luis"]})
df_ventas = pd.DataFrame({"id": [1, 2], "total": [150.0, 320.0]})

# Context manager que consolida múltiples DataFrames en distintas hojas de un solo archivo
with pd.ExcelWriter("consolidado.xlsx", engine="openpyxl") as escritor:
    df_clientes.to_excel(escritor, sheet_name="Clientes", index=False)
    df_ventas.to_excel(escritor, sheet_name="Ventas", index=False)
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Creación, escritura y lectura directa con `openpyxl`.**

```python
import tempfile
from pathlib import Path
from openpyxl import Workbook, load_workbook

with tempfile.TemporaryDirectory() as temp_dir:
    ruta_archivo = Path(temp_dir) / "inventario_basico.xlsx"

    # 1. Creación de un libro nuevo en memoria
    wb = Workbook()
    hoja_activa = wb.active
    hoja_activa.title = "Productos"

    # 2. Inserción de encabezados y registros
    hoja_activa.append(["Codigo", "Descripcion", "Stock", "PrecioUnitario"])
    hoja_activa.append(["P001", "Monitor 27 pulgadas", 15, 249.99])
    hoja_activa.append(["P002", "Teclado mecanico", 42, 85.50])
    hoja_activa.append(["P003", "Raton ergonomico", 30, 45.00])

    # Guardar en disco
    wb.save(ruta_archivo)

    # 3. Lectura e inspección celda a celda
    wb_leido = load_workbook(ruta_archivo, data_only=True)
    hoja_leida = wb_leido["Productos"]

    filas_recuperadas = []
    for fila in hoja_leida.iter_rows(values_only=True):
        filas_recuperadas.append(fila)

print("Hojas en el libro   :", wb_leido.sheetnames)
print("Encabezados leídos  :", filas_recuperadas[0])
print("Primer registro     :", filas_recuperadas[1])
print("Total filas leídas  :", len(filas_recuperadas))
```

Explicación paso a paso:

- `Workbook()` inicializa un libro de trabajo en memoria con una hoja predeterminada accesible vía `wb.active`.
- `hoja.append(secuencia)` añade registros de manera secuencial en la siguiente fila disponible, infiriendo automáticamente los tipos numéricos y textuales.
- `load_workbook(..., data_only=True)` abre el archivo para lectura; el parámetro `data_only=True` garantiza que, en celdas con fórmulas, se lean los valores calculados en lugar del texto crudo de la fórmula.
- `hoja.iter_rows(values_only=True)` es un generador eficiente que devuelve únicamente los valores de cada celda como tuplas nativas de Python.

Resultado esperado:

```text
Hojas en el libro   : ['Productos']
Encabezados leídos  : ('Codigo', 'Descripcion', 'Stock', 'PrecioUnitario')
Primer registro     : ('P001', 'Monitor 27 pulgadas', 15, 249.99)
Total filas leídas  : 4
```

### Intermedio

**Ejemplo 2 — Procesamiento analítico con Pandas: lectura selectiva, agregación y escritura multilínea con `ExcelWriter`.**

```python
import tempfile
from pathlib import Path
import pandas as pd

with tempfile.TemporaryDirectory() as temp_dir:
    ruta_origen = Path(temp_dir) / "operaciones.xlsx"
    ruta_resumen = Path(temp_dir) / "informe_gerencial.xlsx"

    # Preparar datos sintéticos
    datos_ventas = {
        "Region": ["Norte", "Sur", "Norte", "Este", "Sur", "Este"],
        "Vendedor": ["Carlos", "Elena", "Carlos", "Marcos", "Elena", "Marcos"],
        "Unidades": [120, 85, 95, 140, 110, 60],
        "MontoTotal": [12000.0, 8500.0, 9500.0, 14000.0, 11000.0, 6000.0],
    }
    df_inicial = pd.DataFrame(datos_ventas)
    df_inicial.to_excel(ruta_origen, sheet_name="Transacciones", index=False)

    # 1. Ingesta selectiva con Pandas
    df_transacciones = pd.read_excel(
        ruta_origen,
        sheet_name="Transacciones",
        usecols=["Region", "Vendedor", "Unidades", "MontoTotal"],
    )

    # 2. Agregaciones analíticas (Group By)
    resumen_region = (
        df_transacciones.groupby("Region", as_index=False)
        .agg(TotalUnidades=("Unidades", "sum"), VentasTotales=("MontoTotal", "sum"))
        .sort_values(by="VentasTotales", ascending=False)
    )

    resumen_vendedor = (
        df_transacciones.groupby("Vendedor", as_index=False)
        .agg(PromedioVenta=("MontoTotal", "mean"), Operaciones=("Unidades", "count"))
    )

    # 3. Exportación consolidada en múltiples hojas
    with pd.ExcelWriter(ruta_resumen, engine="openpyxl") as writer:
        df_transacciones.to_excel(writer, sheet_name="Detalle", index=False)
        resumen_region.to_excel(writer, sheet_name="Por_Region", index=False)
        resumen_vendedor.to_excel(writer, sheet_name="Por_Vendedor", index=False)

    # Inspección de las hojas generadas con pd.ExcelFile
    libro_inspeccion = pd.ExcelFile(ruta_resumen)
    hojas_generadas = libro_inspeccion.sheet_names

print("Hojas creadas en el informe final:", hojas_generadas)
print("Resumen regional de ventas:\n", resumen_region.to_string(index=False))
```

Explicación técnica:

- Se utiliza `pd.read_excel` para transformar la hoja binaria directamente en un `DataFrame` estructurado.
- Se aplican agrupaciones multidimensionales con `.groupby()` y agregaciones explícitas con `.agg()`, obteniendo totales y promedios por dimensión geográfica y por comercial.
- El bloque `with pd.ExcelWriter(...) as writer:` gestiona el ciclo de vida del libro, canalizando múltiples `DataFrame.to_excel()` sin sobrescribir las hojas previas y asegurando el cierre ordenado del archivo.

Resultado esperado:

```text
Hojas creadas en el informe final: ['Detalle', 'Por_Region', 'Por_Vendedor']
Resumen regional de ventas:
 Region  TotalUnidades  VentasTotales
  Norte            215        21500.0
   Este            200        20000.0
    Sur            195        19500.0
```

### Avanzado

**Ejemplo 3 — Generación de reportes ejecutivos con estilos tipográficos, anchos automáticos y fórmulas con `openpyxl`.**

```python
import tempfile
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

with tempfile.TemporaryDirectory() as temp_dir:
    ruta_reporte = Path(temp_dir) / "reporte_financiero_estilizado.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Balance"

    # Datos base
    encabezados = ["Rubro", "Presupuesto", "Ejecutado", "Diferencia"]
    registros = [
        ["Infraestructura Cloud", 15000, 14200],
        ["Licenciamiento Software", 8000, 8350],
        ["Servicios Profesionales", 12000, 11500],
        ["Capacitacion Tecnica", 5000, 4800],
    ]

    # Estilos profesionales
    fuente_titulo = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    relleno_encabezado = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    alineacion_centrada = Alignment(horizontal="center", vertical="center")
    borde_fino = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    # 1. Escribir y estilizar encabezados (Fila 1)
    ws.append(encabezados)
    for col_idx in range(1, len(encabezados) + 1):
        celda = ws.cell(row=1, column=col_idx)
        celda.font = fuente_titulo
        celda.fill = relleno_encabezado
        celda.alignment = alineacion_centrada

    # 2. Escribir registros e incorporar fórmulas dinámicas
    for fila_idx, (rubro, pres, ejec) in enumerate(registros, start=2):
        formula_dif = f"=B{fila_idx}-C{fila_idx}"
        ws.append([rubro, pres, ejec, formula_dif])

        for col_idx in range(1, len(encabezados) + 1):
            c = ws.cell(row=fila_idx, column=col_idx)
            c.border = borde_fino
            if col_idx in (2, 3, 4):
                c.number_format = '"$"#,##0.00'

    # 3. Fila de totales con fórmulas SUM
    fila_total = len(registros) + 2
    ws.cell(row=fila_total, column=1, value="TOTAL GENERAL").font = Font(bold=True)
    for col_idx, letra in enumerate(["B", "C", "D"], start=2):
        celda_tot = ws.cell(row=fila_total, column=col_idx)
        celda_tot.value = f"=SUM({letra}2:{letra}{fila_total - 1})"
        celda_tot.font = Font(bold=True)
        celda_tot.number_format = '"$"#,##0.00'

    # 4. Ajuste automático del ancho de columnas según el contenido
    for col in ws.columns:
        longitud_max = max(len(str(celda.value or "")) for celda in col)
        col_letra = get_column_letter(col[0].column)
        ws.column_dimensions[col_letra].width = max(longitud_max + 4, 12)

    wb.save(ruta_reporte)

    # Verificación de fórmulas y propiedades
    wb_verificacion = load_workbook(ruta_reporte, data_only=False)
    ws_verif = wb_verificacion["Balance"]
    formula_leida = ws_verif[f"D2"].value
    formula_total = ws_verif[f"B{fila_total}"].value

print("Reporte con estilos guardado correctamente.")
print("Fórmula en celda Diferencia Fila 2:", formula_leida)
print("Fórmula en celda Total Presupuesto :", formula_total)
```

Explicación de ingeniería:

- Se aplican formatos numéricos estandarizados (`number_format = '"$"#,##0.00'`), lo que permite que el usuario final interactúe con valores numéricos reales en Excel en lugar de cadenas de texto formateadas rígidamente.
- Se inyectan fórmulas nativas de Excel (`=B2-C2`, `=SUM(...)`), preservando la capacidad interactiva de la hoja cuando sea abierta por usuarios finales o auditores financieros.
- El bucle de ajuste dinámico calcula la longitud máxima de texto por columna y establece `ws.column_dimensions[letra].width`, evitando el clásico defecto donde los números aparecen truncados con signos de número (`###`) al abrir el reporte.

Resultado esperado:

```text
Reporte con estilos guardado correctamente.
Fórmula en celda Diferencia Fila 2: =B2-C2
Fórmula en celda Total Presupuesto : =SUM(B2:B5)
```

## 6. Aplicaciones en el mundo real

- **Automatización de reportes contables y financieros:** generación desatendida de balances generales, liquidaciones salariales y conciliaciones bancarias programadas en servicios nocturnos.
- **Ingesta de datos en pipelines de Business Intelligence (BI):** lectura e integración de hojas enviadas por sucursales operativas en almacenes de datos analíticos (*Data Warehouses*).
- **Herramientas de migración y auditoría de sistemas legados:** reconciliación entre exportaciones masivas de sistemas ERP (SAP, Oracle) y bases de datos relacionales modernas.
- **Exportación de tableros de control enriquecidos:** provisión de reportes descargables en portales web y aplicaciones SaaS para usuarios finales no técnicos.

## 7. Uso en producción

- **Elegir el motor adecuado según el tamaño del archivo:** para archivos masivos superiores a 50 megabytes, `openpyxl` puede consumir cantidades excesivas de memoria RAM. En entornos críticos de producción, utilizar `openpyxl` en modo lectura optimizada (`load_workbook(ruta, read_only=True)`) o adoptar el motor ultrarrápido `calamine` (`pd.read_excel(ruta, engine="calamine")`).
- **Definir explícitamente los tipos de datos (`dtype`):** columnas identificadoras como códigos postales, RUT/DNI o IDs de cliente con ceros a la izquierda (p. ej. `"00123"`) son interpretadas por defecto como enteros por Excel, mutilando los ceros iniciales (`123`). Suministrar `dtype={"codigo": str}` preserva la integridad del dato.
- **Cerrar siempre los manejadores de archivos con `ExcelWriter`:** emplear siempre la sentencia `with pd.ExcelWriter(...) as writer:` para asegurar que el archivo temporal ZIP se cierre, sincronice y guarde correctamente incluso si se lanzan excepciones durante el proceso.
- **Separar capas de cálculo de capas de presentación:** nunca usar Excel como base de datos transaccional; utilizarlo como vehículo de ingesta inicial o artefacto de salida final, procesando las reglas de negocio complejas en Python o SQL.

## 8. Errores comunes y recomendaciones

1. **Pérdida de ceros a la izquierda en identificadores o códigos (`DNI`, `CBU`, `SKU`).**

```python
import pandas as pd
import io

# ERROR: sin dtype, Pandas interpreta "0045" como entero 45
# Solución: especificar dtype como string:
# df = pd.read_excel("datos.xlsx", dtype={"codigo_postal": str})
```

Diagnóstico: el motor de inferencia intenta convertir cadenas con dígitos a números enteros, eliminando ceros precedentes significativos. Recomendación: declarar taxativamente `dtype={columna: str}` al momento de invocar `pd.read_excel()`.

2. **Leer fórmulas vacías o valores no calculados con `openpyxl` (`None`).**

```python
# Ojo con data_only=True en archivos recién generados por script sin abrir en Excel:
# Si el archivo fue escrito con openpyxl conteniendo fórmulas pero nunca fue abierto
# ni guardado en la aplicación Excel, los valores calculados en caché NO existen
# y load_workbook(ruta, data_only=True) devolverá None en dichas celdas.
```

Diagnóstico: Excel calcula y almacena en caché el resultado de las fórmulas únicamente cuando el usuario abre y guarda el archivo en la aplicación de escritorio. Un archivo generado programáticamente con fórmulas contiene solo el texto de la fórmula. Recomendación: si se requiere evaluar fórmulas programáticamente desde Python sin abrir la aplicación gráfica, utilizar bibliotecas de evaluación de fórmulas como `formulas` o `pycel`.

3. **Sobrescribir accidentalmente hojas de cálculo previas al usar `to_excel` sin `ExcelWriter`.**

```python
# ERROR: cada to_excel destruye el archivo previo y deja una sola hoja
# df1.to_excel("reporte.xlsx", sheet_name="Hoja1")
# df2.to_excel("reporte.xlsx", sheet_name="Hoja2")  # Elimina Hoja1
```

Diagnóstico: invocar `df.to_excel("archivo.xlsx")` crea un archivo nuevo desde cero, destruyendo cualquier contenido preexistente. Recomendación: utilizar `with pd.ExcelWriter("reporte.xlsx", engine="openpyxl") as writer:` y escribir todas las hojas dentro del mismo contexto.

## 9. Resumen

- Los archivos **Excel** (`.xlsx`) son paquetes estructurados comprimidos en ZIP que combinan datos, metadatos, formatos visuales y fórmulas.
- La biblioteca **`openpyxl`** provee control total sobre el modelo de objetos de celdas, bordes, rellenos y fórmulas, siendo el motor por defecto en Python.
- **`pandas`** proporciona abstracciones de alto nivel mediante `pd.read_excel` y `DataFrame.to_excel`, permitiendo análisis tabular y agregaciones complejas con máxima productividad.
- La clase **`pd.ExcelWriter`** permite escribir múltiples `DataFrame` en hojas separadas dentro de un mismo libro sin sobrescribir información.
- En arquitecturas de producción deben controlarse rigurosamente los tipos de datos con `dtype`, usar `read_only=True` para archivos gigantes y gestionar estilos y fórmulas de forma desacoplada.

## 10. Referencias oficiales

- <https://openpyxl.readthedocs.io/en/stable/> — Documentación oficial de `openpyxl`: tutoriales, estilos, fórmulas y optimización de memoria.
- <https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html> — Referencia de API de Pandas para la función `pandas.read_excel`.
- <https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html> — Referencia de API de Pandas para la clase `pandas.ExcelWriter`.
- <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html> — Referencia de API de Pandas para exportar DataFrames a hojas Excel.

