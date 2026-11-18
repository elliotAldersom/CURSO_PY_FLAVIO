# `numpy.dot`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.dot(a, b, out=None)
```

## 2. ¿Qué es?

Es una **función algebraica** que calcula el producto punto entre dos vectores o el producto matricial en 2D.

## 3. ¿Para qué sirve?

Calcula proyecciones vectoriales, productos internos y combinaciones lineales.

## 4. ¿Cómo funciona?

1. Para vectores 1D calcula el producto escalar $\sum a_i b_i$; para matrices 2D es equivalente a la multiplicación de matrices.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a`, `b` | arreglos | Obligatorio | Posicional | Vectores o matrices a multiplicar. |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print(np.dot(v1, v2))
```

**Salida real:**

```text
32
```

---

### Nivel 2: Intermedio

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[2, 0], [1, 2]])
print(np.dot(A, B))
```

**Salida real:**

```text
[[ 4  4]
 [10  8]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Similitud coseno entre dos vectores normalizados
u = np.array([1.0, 0.0])
v = np.array([0.7071, 0.7071])
similitud = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
print('Coseno:', round(similitud, 4))
```

**Salida real:**

```text
Coseno: 0.7071
```

## 8. Errores frecuentes y casos borde

1. Dimensiones interiores no coincidentes: Lanza `ValueError`.

## 9. Buenas prácticas y rendimiento

* Para multiplicación matricial moderna en 2D+, preferir el operador `@` o `np.matmul`.

## 10. Métodos relacionados

* `matmul` — Multiplicación matricial tensorial.

## 11. Referencias oficiales

* **API Reference:** [`numpy.dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html) (NumPy 2.x).
