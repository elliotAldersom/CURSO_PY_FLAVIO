# Fundamentos de Manipulación de Hojas de Cálculo con OpenPyXL

## 2. Introducción

OpenPyXL es la biblioteca canónica de Python para la lectura, edición, formateo de celdas y generación de libros Microsoft Excel bajo el estándar Office Open XML (`.xlsx`, `.xlsm`). A diferencia de Pandas (orientado exclusivamente al análisis tabular numérico), OpenPyXL permite interactuar con la estructura XML interna del libro, manipulando estilos visuales, colores de celda, fuentes tipográficas, bordes, fórmulas nativas sin evaluar y múltiples hojas de cálculo independientes.

## 3. Fundamentos y conceptos

1. **Modelo jerárquico de objetos de Excel:**
   * **`Workbook`:** Representa el contenedor del archivo `.xlsx` completo.
   * **`Worksheet`:** Superficie bidimensional de cuadrícula identificada por un nombre único.
   * **`Cell`:** Unidad mínima que alberga un valor tipado, un estilo visual (`Font`, `PatternFill`, `Border`) y opcionalmente una fórmula de cálculo (`=SUM(...)`).
2. **Coordenadas y direccionamiento:**
   * Indexación alfanumérica estándar de Excel: `ws['A1']`.
   * Indexación numérica entera en base 1: `ws.cell(row=1, column=1)`.
3. **Modos de bajo consumo de memoria:**
   * `read_only=True`: Abre el archivo en flujo de lectura perezoso sin cargar el DOM completo en memoria.
   * `write_only=True`: Permite volcar millones de celdas en streaming constante sin desbordar la memoria RAM.

## 4. Sintaxis y funcionamiento

Instalación:

```bash
pip install openpyxl
```

Importación canónica:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
```

## 5. Ejemplos prácticos progresivos

### Básico

Creación y escritura básica en una hoja de cálculo:

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Goleadores"

ws["A1"] = "Jugador"
ws["B1"] = "Goles"
ws.append(["Vinicius Jr", 21])

print(f"Hoja activa: {ws.title} | Celda A1: {ws['A1'].value}")
```

**Salida real:**

```text
Hoja activa: Goleadores | Celda A1: Jugador
```

---

### Intermedio

Aplicación de formato y estilos corporativos a celdas:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill

wb = openpyxl.Workbook()
ws = wb.active

ws["A1"] = "Reporte Oficial"
ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")

print("Estilo aplicado exitosamente con color de fondo y fuente en negrita.")
```

**Salida real:**

```text
Estilo aplicado exitosamente con color de fondo y fuente en negrita.
```

---

### Avanzado

Generación de reporte financiero deportivo con fórmulas y dimensiones automáticas:

```python
import io
import openpyxl
from openpyxl.styles import Font

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Presupuesto"

ws.append(["Concepto", "Monto USD"])
ws.append(["Fichajes", 150000000])
ws.append(["Salarios", 80000000])
ws.append(["Total", "=SUM(B2:B3)"])

ws["A4"].font = Font(bold=True)
ws["B4"].font = Font(bold=True)
ws.column_dimensions["A"].width = 20
ws.column_dimensions["B"].width = 18

buffer = io.BytesIO()
wb.save(buffer)
print(f"Reporte generado en memoria. Tamaño: {len(buffer.getvalue())} bytes.")
```

**Salida real:**

```text
Reporte generado en memoria. Tamaño: 5240 bytes.
```

## 6. Aplicaciones en el mundo real

En el sector bancario, de auditoría contable y consultoría de gestión, los reportes ejecutivos deben entregarse obligatoriamente en formato `.xlsx` con plantillas visuales estrictas (paleta de colores de marca, celdas bloqueadas, fórmulas dinámicas y hojas protegidas). OpenPyXL permite automatizar la generación diaria de miles de estos informes contables sin intervención humana ni licencias de Microsoft Office.

## 7. Uso en producción

1. **Memoria en archivos grandes:** Cargar libros gigantescos con `openpyxl.load_workbook(filename)` carga todo el árbol XML en RAM, pudiendo consumir gigabytes de memoria. Para datasets masivos de solo lectura, pasar obligatoriamente `read_only=True`.
2. **Cierre de flujos:** Siempre cerrar el libro (`wb.close()`) o guardarlo en un buffer con gestores de contexto.
3. **Fórmulas no evaluadas:** OpenPyXL escribe fórmulas pero **no las calcula**. El valor de la celda será `None` hasta que el archivo sea abierto y calculado por Microsoft Excel o LibreOffice.

## 8. Errores comunes y recomendaciones

* **Error común: Índices base 0:** En OpenPyXL, las filas y columnas son **base 1** (`row=1, column=1`). Usar `row=0` lanza `ValueError: Row or column values must be at least 1`.
* **Error común: Confundir `.value` con el objeto `Cell`:** Imprimir `ws['A1']` devuelve `<Cell 'Sheet'.A1>`, no el texto. Debe leerse `ws['A1'].value`.

## 9. Resumen

OpenPyXL es la solución definitiva para manipular libros `.xlsx` preservando estilos visuales, múltiples hojas y fórmulas. Se complementa con Pandas para exportar datos con presentación ejecutiva corporativa.

## 10. Referencias oficiales

* [OpenPyXL Documentation](https://openpyxl.readthedocs.io/en/stable/).
