# `Worksheet.append`

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.x)
Worksheet.append(iterable)
```

## 2. ¿Qué es?

Es un **método de escritura secuencial** que adjunta una lista o tupla de valores como una nueva fila al final de los datos existentes.

## 3. ¿Para qué sirve?

Permite llenar tablas fila por fila de forma limpia y veloz sin calcular manualmente las coordenadas de filas.

## 4. ¿Cómo funciona?

1. Localiza la primera fila vacía (`max_row + 1`) y escribe secuencialmente cada elemento en las columnas sucesivas.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `iterable` | lista, tupla, dict | Obligatorio | Posicional | Valores a insertar en la fila. |

## 6. Retorno

`None`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['Jugador', 'Goles'])
ws.append(['Kylian Mbappé', 28])
print(f'Total de filas escritas: {ws.max_row}')
```

**Salida real:**

```text
Total de filas escritas: 2
```

---

### Nivel 2: Intermedio

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
datos = [['A', 1], ['B', 2], ['C', 3]]
for fila in datos:
    ws.append(fila)
print('Última fila:', ws.max_row)
```

**Salida real:**

```text
Última fila: 3
```

---

### Nivel 3: Avanzado

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
# Diccionario por columnas
ws.append({'A': 'Fecha', 'C': 'Total'})
print('Celda C1:', ws['C1'].value)
```

**Salida real:**

```text
Celda C1: Total
```

## 8. Errores frecuentes y casos borde

1. Pasar un escalar en lugar de una lista: Intentar `ws.append('texto')` iterará sobre cada letra individual.

## 9. Buenas prácticas y rendimiento

* Es el método más rápido y recomendado para generar reportes tabulares.

## 10. Métodos relacionados

* `cell_access` — Modificación puntual de celdas.

## 11. Referencias oficiales

* **API Reference:** [`Worksheet.append`](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.worksheet.html).
