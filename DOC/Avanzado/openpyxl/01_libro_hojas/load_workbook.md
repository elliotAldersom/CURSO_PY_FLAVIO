# `openpyxl.load_workbook`

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
openpyxl.load_workbook(filename, read_only=False, keep_vba=False, data_only=False, keep_links=True)
```

## 2. ¿Qué es?

Es la **función de apertura e ingesta** que parsea un archivo físico `.xlsx` existente en disco o buffer.

## 3. ¿Para qué sirve?

Permite leer plantillas existentes, modificar celdas específicas y extraer datos preservando formatos.

## 4. ¿Cómo funciona?

1. Descomprime el paquete ZIP OpenXML y construye las referencias de celdas en memoria.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `filename` | `str`, buffer | Obligatorio | Posicional | Ruta o descriptor del archivo `.xlsx`. |
| `data_only` | `bool` | Opcional | `False` | Si es `True`, lee los valores calculados de las fórmulas en lugar del texto `=SUM(...)`. |
| `read_only` | `bool` | Opcional | `False` | Modo streaming de lectura sin sobrecarga de memoria. |

## 6. Retorno

`openpyxl.workbook.Workbook`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import io, openpyxl
buf = io.BytesIO()
wb_orig = openpyxl.Workbook()
wb_orig.save(buf)
buf.seek(0)
wb = openpyxl.load_workbook(buf)
print('Cargado con éxito:', wb.sheetnames)
```

**Salida real:**

```text
Cargado con éxito: ['Sheet']
```

---

### Nivel 2: Intermedio

```python
import io, openpyxl
buf = io.BytesIO()
wb_orig = openpyxl.Workbook()
ws = wb_orig.active
ws['A1'] = 100
wb_orig.save(buf)
buf.seek(0)
wb = openpyxl.load_workbook(buf, data_only=True)
print('Valor en celda:', wb.active['A1'].value)
```

**Salida real:**

```text
Valor en celda: 100
```

---

### Nivel 3: Avanzado

```python
import io, openpyxl
buf = io.BytesIO()
openpyxl.Workbook().save(buf)
buf.seek(0)
wb = openpyxl.load_workbook(buf, read_only=True)
print('Modo sólo lectura activo:', wb.read_only)
wb.close()
```

**Salida real:**

```text
Modo sólo lectura activo: True
```

## 8. Errores frecuentes y casos borde

1. Fórmulas con `data_only=True`: Si el archivo no fue guardado por Excel tras calcular, devolverá `None`.

## 9. Buenas prácticas y rendimiento

* Usar `read_only=True` para archivos que superen los 50 MB.

## 10. Métodos relacionados

* `workbook` — Creación de libros nuevos.

## 11. Referencias oficiales

* **API Reference:** [`openpyxl.load_workbook`](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html).
