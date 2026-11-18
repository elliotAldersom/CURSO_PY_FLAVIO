# OpenPyXL: Escritura de Fórmulas Nativas

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.1.x)
Cell.value = '=SUM(A1:A10)'
```

## 2. ¿Qué es?

La asignación de fórmulas nativas consiste en inyectar expresiones en formato fórmula estándar de Excel en el atributo `.value` de una celda con el prefijo `=`. Las fórmulas deben escribirse en su nombre estándar en inglés.

## 3. ¿Para qué sirve?

Permite delegar cálculos matemáticos, financieros o estadísticos a la aplicación de hoja de cálculo consumidora (Excel, LibreOffice Calc) sin precalcularlos estáticamente en Python.

## 4. ¿Cómo funciona?

OpenPyXL no ejecuta el motor de cálculo de Excel; simplemente almacena la fórmula como cadena dentro del tag XML `<f>SUM(A1:A10)</f>`. Al abrirse el archivo en Excel, la suite evalúa la fórmula y genera el valor en caché.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `value` | `str` | Obligatorio | N/A | Cadena que comienza con `=` que contiene nombres de funciones en inglés y sintaxis válida de Excel. |

## 6. Retorno

`None`. La celda almacena la expresión XML de la fórmula.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active

ws['A1'] = 150
ws['A2'] = 350
ws['A3'] = "=SUM(A1:A2)"

print(f"Fórmula asignada a A3: {ws['A3'].value}")
wb.close()
```

**Salida real:**

```text
Fórmula asignada a A3: =SUM(A1:A2)
```

### Nivel 2: Intermedio

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active

ws.append(["Producto", "Precio", "Unidades", "Total"])
ws.append(["Monitor 4K", 400, 2, "=B2*C2"])
ws.append(["Teclado Mecánico", 120, 3, "=B3*C3"])
ws.append(["TOTAL GENERAL", "", "", "=SUM(D2:D3)"])

for row in ws.iter_rows(min_row=2, max_col=4, values_only=True):
    print(row)
wb.close()
```

**Salida real:**

```text
('Monitor 4K', 400, 2, '=B2*C2')
('Teclado Mecánico', 120, 3, '=B3*C3')
('TOTAL GENERAL', '', '', '=SUM(D2:D3)')
```

### Nivel 3: Avanzado

```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active

# Fórmulas condicionales avanzadas
ws['A1'] = 85
ws['A2'] = '=IF(A1>=70, "APROBADO", "REPROBADO")'
ws['A3'] = '=AVERAGE(A1, 95, 100)'

print(f"Condicional: {ws['A2'].value}")
print(f"Promedio: {ws['A3'].value}")
wb.close()
```

**Salida real:**

```text
Condicional: =IF(A1>=70, "APROBADO", "REPROBADO")
Promedio: =AVERAGE(A1, 95, 100)
```

## 8. Errores frecuentes y casos borde

- **Escribir fórmulas en español:** `=SUMA(A1:A10)` generará error `#NAME?` en Excel; las fórmulas en OpenPyXL deben estar SIEMPRE en inglés (`=SUM(...)`).
- **Lectura de valores de fórmulas:** Si lees un archivo generado con `data_only=True` inmediatamente sin haber sido guardado previamente por Excel, el valor será `None` porque OpenPyXL no incluye un evaluador de fórmulas.

## 9. Buenas prácticas y rendimiento

- Usar siempre nombres en inglés (`SUM`, `AVERAGE`, `VLOOKUP`, `IF`, `COUNTIF`).
- Si necesitas evaluar fórmulas desde Python sin abrir Excel, usa librerías complementarias como `pycel` o `formulas`.

## 10. Métodos relacionados

- [cell_access](../02_lectura_escritura_celdas/cell_access.md)
- [load_workbook](../01_libro_hojas/load_workbook.md)

## 11. Referencias oficiales

- https://openpyxl.readthedocs.io/en/stable/usage.html#using-formulae
- https://openpyxl.readthedocs.io/en/stable/api/openpyxl.cell.cell.html
