# `openpyxl.Workbook`

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
openpyxl.Workbook(write_only=False, iso_dates=False)
```

## 2. ¿Qué es?

Es la **clase constructora del libro** de Excel en OpenPyXL que crea una nueva instancia de documento `.xlsx` en memoria.

## 3. ¿Para qué sirve?

Inicializa un nuevo libro para generar reportes desde cero.

## 4. ¿Cómo funciona?

1. Construye el árbol de documentos XML en memoria con una hoja activa predeterminada.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `write_only` | `bool` | Opcional | `False` | Habilita modo streaming optimizado para escritura masiva. |

## 6. Retorno

`openpyxl.workbook.Workbook`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl
wb = openpyxl.Workbook()
print(wb.sheetnames)
```

**Salida real:**

```text
['Sheet']
```

---

### Nivel 2: Intermedio

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Ventas'
print(wb.sheetnames)
```

**Salida real:**

```text
['Ventas']
```

---

### Nivel 3: Avanzado

```python
import io, openpyxl
wb = openpyxl.Workbook()
buf = io.BytesIO()
wb.save(buf)
print('Bytes generados:', len(buf.getvalue()) > 0)
```

**Salida real:**

```text
Bytes generados: True
```

## 8. Errores frecuentes y casos borde

1. Guardar sin hojas: Un libro debe contener al menos una hoja visible.

## 9. Buenas prácticas y rendimiento

* Siempre cerrar con `wb.close()` tras guardar.

## 10. Métodos relacionados

* `load_workbook` — Apertura de archivos existentes.

## 11. Referencias oficiales

* **API Reference:** [`openpyxl.Workbook`](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.workbook.workbook.html).
