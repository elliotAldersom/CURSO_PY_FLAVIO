# `numpy.sum`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.sum(a, axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True)
```

## 2. ¿Qué es?

Es una **función de reducción estadística** que suma todos los elementos de un arreglo a lo largo del eje o ejes especificados.

## 3. ¿Para qué sirve?

Calcula totales globales o sumatorias por filas o columnas en matrices.

## 4. ¿Cómo funciona?

1. Si `axis=None`, colapsa todo el arreglo devolviendo un escalar. Si `axis=0`, suma colapsando filas (da una suma por columna); si `axis=1`, suma colapsando columnas (suma por fila).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | arreglo | Obligatorio | Posicional | Arreglo a sumar. |
| `axis` | `int`, tupla | Opcional | `None` | Eje de reducción. |
| `keepdims` | `bool` | Opcional | `False` | Preserva las dimensiones con longitud 1 para broadcasting. |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([10, 20, 30])
print(np.sum(arr))
```

**Salida real:**

```text
60
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[1, 2], [3, 4]])
print('Suma por columnas (axis=0):', np.sum(m, axis=0))
print('Suma por filas (axis=1):', np.sum(m, axis=1))
```

**Salida real:**

```text
Suma por columnas (axis=0): [4 6]
Suma por filas (axis=1): [3 7]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
m = np.array([[1, 2], [3, 4]])
suma_con_dims = np.sum(m, axis=1, keepdims=True)
print('Forma preservada:', suma_con_dims.shape)
print('Normalización por fila:\n', m / suma_con_dims)
```

**Salida real:**

```text
Forma preservada: (2, 1)
Normalización por fila:
 [[0.33333333 0.66666667]
 [0.42857143 0.57142857]]
```

## 8. Errores frecuentes y casos borde

1. Desbordamiento de tipo en sumas masivas de `int32`: Especificar `dtype=np.int64`.

## 9. Buenas prácticas y rendimiento

* Usar `keepdims=True` para permitir dividir inmediatamente la matriz original por su suma.

## 10. Métodos relacionados

* `mean` — Promedio aritmético.

## 11. Referencias oficiales

* **API Reference:** [`numpy.sum`](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) (NumPy 2.x).
