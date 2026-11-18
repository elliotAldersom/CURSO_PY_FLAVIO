# `openpyxl.styles.PatternFill`

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
PatternFill(fill_type=None, start_color=None, end_color=None)
```

## 2. ¿Qué es?

Es una **clase de relleno de celdas** que define colores de fondo sólidos o patrones gráficos en hojas de cálculo.

## 3. ¿Para qué sirve?

Permite colorear encabezados corporativos y aplicar semaforización condicional (verde, amarillo, rojo).

## 4. ¿Cómo funciona?

1. Aplica la definición de relleno `<fill>` en la tabla de estilos XML.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `fill_type` | `str` | Opcional | `None` | Tipo de relleno (habitualmente `'solid'`). |
| `start_color` | `str` | Opcional | `None` | Código RGB hexadecimal del color de fondo. |

## 6. Retorno

`openpyxl.styles.fills.PatternFill`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl
from openpyxl.styles import PatternFill
wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = 'Aprobado'
ws['A1'].fill = PatternFill(start_color='C6EFCE', fill_type='solid')
print('Relleno aplicado:', ws['A1'].fill.fill_type)
```

**Salida real:**

```text
Relleno aplicado: solid
```

---

### Nivel 2: Intermedio

```python
import openpyxl
from openpyxl.styles import PatternFill
wb = openpyxl.Workbook()
ws = wb.active
azul_corp = PatternFill(start_color='1F497D', fill_type='solid')
ws['A1'] = 'Header'
ws['A1'].fill = azul_corp
print('Color hexadecimal:', ws['A1'].fill.start_color.rgb)
```

**Salida real:**

```text
Color hexadecimal: 001F497D
```

---

### Nivel 3: Avanzado

```python
import openpyxl
from openpyxl.styles import PatternFill
wb = openpyxl.Workbook()
ws = wb.active
# Semaforización de rendimiento
fill_verde = PatternFill('solid', start_color='00FF00')
fill_rojo = PatternFill('solid', start_color='FF0000')
ws['A1'] = 95; ws['A1'].fill = fill_verde
ws['A2'] = 40; ws['A2'].fill = fill_rojo
print('Semaforización completada.')
```

**Salida real:**

```text
Semaforización completada.
```

## 8. Errores frecuentes y casos borde

1. Olvidar `fill_type='solid'`: Si se pasa el color sin `fill_type='solid'`, el fondo permanece blanco transparente.

## 9. Buenas prácticas y rendimiento

* Especificar siempre `fill_type='solid'` para fondos uniformes.

## 10. Métodos relacionados

* `font` — Estilo de texto.

## 11. Referencias oficiales

* **API Reference:** [`openpyxl.styles.PatternFill`](https://openpyxl.readthedocs.io/en/stable/styles.html).
