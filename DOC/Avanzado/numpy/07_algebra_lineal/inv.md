# `numpy.linalg.inv`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.linalg.inv(a)
```

## 2. ¿Qué es?

Es una **función de álgebra lineal** que calcula la matriz inversa multiplicativa $A^{-1}$ tal que $A A^{-1} = I$.

## 3. ¿Para qué sirve?

Resuelve sistemas de ecuaciones lineales exactos $Ax = b \Rightarrow x = A^{-1}b$.

## 4. ¿Cómo funciona?

1. Emplea descomposición LU implementada en LAPACK.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | matriz cuadrada | Obligatorio | Posicional | Matriz invertible de tamaño $N \times N$. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.]])
A_inv = np.linalg.inv(A)
print(A_inv)
```

**Salida real:**

```text
[[-2.   1. ]
 [ 1.5 -0.5]]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.]])
A_inv = np.linalg.inv(A)
# Verificamos A @ A_inv == I
print(np.allclose(A @ A_inv, np.eye(2)))
```

**Salida real:**

```text
True
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Resolución de sistema: 2x + y = 8, x + 3y = 9
A = np.array([[2., 1.], [1., 3.]])
b = np.array([8., 9.])
x = np.linalg.inv(A) @ b
print('Solución (x, y):', x)
```

**Salida real:**

```text
Solución (x, y): [3. 2.]
```

## 8. Errores frecuentes y casos borde

1. Matriz singular (determinante cero): Lanza `numpy.linalg.LinAlgError: Singular matrix`.

## 9. Buenas prácticas y rendimiento

* Para resolver sistemas $Ax = b$, preferir `np.linalg.solve(A, b)` en vez de calcular la inversa explícita por precisión numérica.

## 10. Métodos relacionados

* `det` — Determinante.

## 11. Referencias oficiales

* **API Reference:** [`numpy.linalg.inv`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html) (NumPy 2.x).
