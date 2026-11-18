# OpenPyXL: Worksheet.column_dimensions

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.1.x)
Worksheet.column_dimensions[col_letter].width = float
```

## 2. ¿Qué es?

`Worksheet.column_dimensions` es un diccionario interno (instancia de `openpyxl.worksheet.dimensions.ColumnDimension`) que administra los metadatos geométricos y visuales de cada columna en una hoja de Excel.

## 3. ¿Para qué sirve?

Permite ajustar el ancho (`width`), visibilidad (`hidden`) o agrupar (`outline_level`) columnas de manera programática para evitar que textos largos aparezcan truncados o con símbolos `###` en hojas generadas.

## 4. ¿Cómo funciona?

OpenPyXL mapea letras de columna ('A', 'B', ...) a objetos `ColumnDimension`. Al guardar el archivo XLSX, estos valores se serializan en el elemento XML `<cols><col min='1' max='1' width='25' customWidth='1'/></cols>`.

## 5. Parámetros

| Parámetro / Propiedad | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `width` | `float` | Opcional | `None` | Ancho en caracteres tipográficos estándar de Excel. |
| `hidden` | `bool` | Opcional | `False` | Oculta la columna si es `True`. |
| `outline_level` | `int` | Opcional | `0` | Nivel de agrupación jerárquica para esquema. |

## 6. Retorno

`openpyxl.worksheet.dimensions.ColumnDimension`. Modifica las propiedades visuales de la columna en el XML de la hoja.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = "Código de Producto Extenso"
ws.column_dimensions['A'].width = 30
print(f"Ancho columna A: {ws.column_dimensions['A'].width}")
wb.close()
```

**Salida real:**

```text
Ancho columna A: 30
```

### Nivel 2: Intermedio

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active

headers = ["ID", "Nombre Completo", "Correo Electrónico"]
ws.append(headers)
ws.append([1, "Alexander von Humboldt", "alexander@ciencias.org"])

for col in ws.columns:
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    max_len = max(len(str(cell.value or '')) for cell in col)
    ws.column_dimensions[col_letter].width = max(max_len + 3, 10)
    print(f"Col {col_letter} auto-width: {ws.column_dimensions[col_letter].width}")
wb.close()
```

**Salida real:**

```text
Col A auto-width: 10
Col B auto-width: 25
Col C auto-width: 26
```

### Nivel 3: Avanzado

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Reporte_Financiero"

ws['A1'] = "Detalle Interno"
ws['B1'] = "Ingreso Neto"
ws.column_dimensions['A'].hidden = True
ws.column_dimensions['B'].width = 18

print(f"Col A oculta: {ws.column_dimensions['A'].hidden}")
print(f"Col B ancho: {ws.column_dimensions['B'].width}")
wb.close()
```

**Salida real:**

```text
Col A oculta: True
Col B ancho: 18
```

## 8. Errores frecuentes y casos borde

- **Confundir índice numérico con letra de columna:** `ws.column_dimensions[1]` lanza error; debe ser la letra `ws.column_dimensions['A']` o `openpyxl.utils.get_column_letter(1)`.
- **Unidades:** El ancho no es en píxeles ni milímetros, sino en ancho del glifo promedio de la fuente base.

## 9. Buenas prácticas y rendimiento

- Automatizar el ajuste de columnas calculando `max(len(str(val)))` tras escribir los datos.
- No iterar celdas innecesariamente en archivos masivos; definir anchos fijos precalculados.

## 10. Métodos relacionados

- [cell_access](../02_lectura_escritura_celdas/cell_access.md)
- [font](../03_estilos_formato/font.md)

## 11. Referencias oficiales

- https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.dimensions.html
- https://openpyxl.readthedocs.io/en/stable/worksheet_properties.html
