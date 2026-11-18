# Acceso y Modificación de Celdas (`Worksheet.cell` y `ws['A1']`)

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
Worksheet.cell(row, column, value=None) -> Cell
Worksheet['A1'] -> Cell
```

## 2. ¿Qué es?

Es el **mecanismo de direccionamiento celular** que permite leer o escribir valores tipados en coordenadas específicas de la cuadrícula.

## 3. ¿Para qué sirve?

Modifica valores en celdas fijas o mediante iteraciones numéricas por coordenadas.

## 4. ¿Cómo funciona?

1. Retorna un objeto `Cell` con propiedades `.value`, `.data_type` y `.coordinate`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `row` | `int` | Obligatorio | Posicional | Fila en base 1. |
| `column` | `int` | Obligatorio | Posicional | Columna en base 1. |

## 6. Retorno

`openpyxl.cell.cell.Cell`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = 'Lionel Messi'
print(ws['A1'].value)
```

**Salida real:**

```text
Lionel Messi
```

---

### Nivel 2: Intermedio

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
celda = ws.cell(row=2, column=3, value=25)
print(f'Coordenada: {celda.coordinate} | Valor: {celda.value}')
```

**Salida real:**

```text
Coordenada: C2 | Valor: 25
```

---

### Nivel 3: Avanzado

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
# Asignación numérica directa con tipo detectado
ws['B5'] = 4500.50
print('Tipo de dato detectado:', ws['B5'].data_type)
```

**Salida real:**

```text
Tipo de dato detectado: n
```

## 8. Errores frecuentes y casos borde

1. Usar `row=0` o `column=0`: Lanza `ValueError` (OpenPyXL es estrictamente base 1).

## 9. Buenas prácticas y rendimiento

* Usar `cell(row, col)` en bucles numéricos y `ws['A1']` para celdas fijas.

## 10. Métodos relacionados

* `append` — Escritura secuencial de filas.

## 11. Referencias oficiales

* **API Reference:** [Acceso y Modificación de Celdas (`Worksheet.cell` y `ws['A1']`)](https://openpyxl.readthedocs.io/en/stable/tutorial.html#accessing-cells).
