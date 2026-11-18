# `numpy.sort`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.sort(a, axis=-1, kind=None, order=None, *, stable=False)
```

## 2. ¿Qué es?

Es una **función de ordenamiento** que devuelve una copia ordenada de un arreglo a lo largo del eje especificado.

## 3. ¿Para qué sirve?

Ordena datos numéricos, fechas o vectores multidimensionales en memoria rápida de C.

## 4. ¿Cómo funciona?

1. Por defecto ordena sobre el último eje (`axis=-1`) usando `quicksort` o `introsort`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | arreglo | Obligatorio | Posicional | Arreglo a ordenar. |
| `axis` | `int`, `None` | Opcional | `-1` | Eje a lo largo del cual ordenar. Si es `None`, aplana y ordena todo. |
| `stable` | `bool` | Opcional | `False` | Preserva el orden relativo de elementos idénticos. |

## 6. Retorno

`numpy.ndarray` ordenado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([3, 1, 4, 1, 5])
print(np.sort(arr))
```

**Salida real:**

```text
[1 1 3 4 5]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[5, 2], [1, 4]])
print('Orden por filas (axis=1):\n', np.sort(m, axis=1))
print('Orden por columnas (axis=0):\n', np.sort(m, axis=0))
```

**Salida real:**

```text
Orden por filas (axis=1):
 [[2 5]
 [1 4]]
Orden por columnas (axis=0):
 [[1 2]
 [5 4]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
arr = np.array([10, 5, 20])
# Orden inverso (descendente)
print('Descendente:', np.sort(arr)[::-1])
```

**Salida real:**

```text
Descendente: [20 10  5]
```

## 8. Errores frecuentes y casos borde

1. Confundir `np.sort(arr)` (devuelve una copia) con `arr.sort()` (muta in-place el arreglo).

## 9. Buenas prácticas y rendimiento

* Usar `arr.sort()` si se quiere ahorrar memoria y no se necesita el arreglo original.

## 10. Métodos relacionados

* `argsort` — Retorna los índices del ordenamiento.

## 11. Referencias oficiales

* **API Reference:** [`numpy.sort`](https://numpy.org/doc/stable/reference/generated/numpy.sort.html) (NumPy 2.x).
