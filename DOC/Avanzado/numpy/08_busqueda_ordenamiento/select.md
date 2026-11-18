# `numpy.select`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.select(condlist, choicelist, default=0)
```

## 2. ¿Qué es?

Es una **función condicional multicriterio** que evalúa una lista de condiciones en orden y asigna el valor correspondiente de una lista de opciones.

## 3. ¿Para qué sirve?

Implementa sentencias `CASE WHEN ... THEN` complejas de forma completamente vectorizada.

## 4. ¿Cómo funciona?

1. Evalúa las condiciones secuencialmente; el primer `True` determina el valor asignado.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `condlist` | lista de arreglos bool | Obligatorio | Posicional | Condiciones lógicas a contrastar. |
| `choicelist` | lista de arreglos/valores | Obligatorio | Posicional | Valores asignados para cada condición. |
| `default` | escalar | Opcional | `0` | Valor por defecto si ninguna condición es `True`. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
edades = np.array([16, 22, 35, 70])
condiciones = [edades < 18, edades < 65]
opciones = ['Menor', 'Adulto']
print(np.select(condiciones, opciones, default='Jubilado'))
```

**Salida real:**

```text
['Menor' 'Adulto' 'Adulto' 'Jubilado']
```

---

### Nivel 2: Intermedio

```python
import numpy as np
puntos = np.array([95, 82, 70, 50])
cond = [puntos >= 90, puntos >= 80, puntos >= 70]
opc = ['Oro', 'Plata', 'Bronce']
print(np.select(cond, opc, default='Sin premio'))
```

**Salida real:**

```text
['Oro' 'Plata' 'Bronce' 'Sin premio']
```

---

### Nivel 3: Avanzado

```python
import numpy as np
minutos = np.array([2500, 1800, 450])
c = [minutos > 2000, minutos > 1000]
v = [1.2, 1.0] # Multiplicadores salariales
print('Factor salarial:', np.select(c, v, default=0.8))
```

**Salida real:**

```text
Factor salarial: [1.2 1.  0.8]
```

## 8. Errores frecuentes y casos borde

1. Longitudes distintas en `condlist` y `choicelist`: Lanza `ValueError`.

## 9. Buenas prácticas y rendimiento

* Es infinitamente más rápido y legible que anidar múltiples `np.where()`.

## 10. Métodos relacionados

* `where` — Condición binaria simple.

## 11. Referencias oficiales

* **API Reference:** [`numpy.select`](https://numpy.org/doc/stable/reference/generated/numpy.select.html) (NumPy 2.x).
