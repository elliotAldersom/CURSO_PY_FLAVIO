# `openpyxl.styles.Font`

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
Font(name=None, sz=None, b=None, i=None, color=None, underline=None, strike=None)
```

## 2. ¿Qué es?

Es una **clase de estilo tipográfico** que define la familia de fuente, tamaño, negrita, cursiva y color del texto en celdas de Excel.

## 3. ¿Para qué sirve?

Permite jerarquizar títulos, encabezados y advertencias visuales en planillas.

## 4. ¿Cómo funciona?

1. Modifica la etiqueta XML `<font>` de los estilos del libro.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | Opcional | `'Calibri'` | Familia tipográfica (`'Arial'`, `'Calibri'`). |
| `size` / `sz` | `float` | Opcional | `11` | Tamaño de la fuente en puntos. |
| `bold` / `b` | `bool` | Opcional | `False` | Texto en negrita. |
| `color` | `str`, `Color` | Opcional | `'000000'` | Código hexadecimal RGB sin el `#` (p. ej. `'FF0000'`). |

## 6. Retorno

`openpyxl.styles.fonts.Font`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl
from openpyxl.styles import Font
wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = 'Encabezado'
ws['A1'].font = Font(name='Arial', size=12, bold=True)
print('Negrita activa:', ws['A1'].font.bold)
```

**Salida real:**

```text
Negrita activa: True
```

---

### Nivel 2: Intermedio

```python
import openpyxl
from openpyxl.styles import Font
wb = openpyxl.Workbook()
ws = wb.active
ws['B2'] = 'Alerta'
ws['B2'].font = Font(color='FF0000', italic=True)
print('Color asignado:', ws['B2'].font.color.rgb)
```

**Salida real:**

```text
Color asignado: 00FF0000
```

---

### Nivel 3: Avanzado

```python
import openpyxl
from openpyxl.styles import Font
wb = openpyxl.Workbook()
ws = wb.active
fuente_titulo = Font(size=16, bold=True)
for col in ['A1', 'B1', 'C1']:
    ws[col] = 'Col'
    ws[col].font = fuente_titulo
print('Estilo reutilizado en múltiples celdas.')
```

**Salida real:**

```text
Estilo reutilizado en múltiples celdas.
```

## 8. Errores frecuentes y casos borde

1. Incluir el símbolo `#` en el código de color: `'#FF0000'` genera color erróneo. Usar `'FF0000'`.

## 9. Buenas prácticas y rendimiento

* Crear instancias reutilizables de `Font` para no duplicar objetos en memoria.

## 10. Métodos relacionados

* `pattern_fill` — Fondo de celda.

## 11. Referencias oficiales

* **API Reference:** [`openpyxl.styles.Font`](https://openpyxl.readthedocs.io/en/stable/styles.html).
