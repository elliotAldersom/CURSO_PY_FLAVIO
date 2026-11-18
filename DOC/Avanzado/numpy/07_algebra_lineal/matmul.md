# `numpy.matmul` y operador `@`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.matmul(x1, x2, /, out=None, *, casting='same_kind', order='K', dtype=None)
```

## 2. ¿Qué es?

Es la **función canónica de multiplicación matricial** que implementa el producto de matrices para arreglos 2D y lotes tensoriales (*batch matrix multiplication*).

## 3. ¿Para qué sirve?

Núcleo de transformaciones lineales, capas densas de Deep Learning y proyecciones PCA.

## 4. ¿Cómo funciona?

1. Opera mediante librerías optimizadas BLAS (como OpenBLAS o Intel MKL). Permite usar el operador infijo `@` introducido en PEP 465.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `x1`, `x2` | arreglos | Obligatorio | Posicional | Matrices compatibles ($N \times K$ y $K \times M$). |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)
```

**Salida real:**

```text
[[19 22]
 [43 50]]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
x = np.array([1, 2])
# Transformación lineal A * x
print(A @ x)
```

**Salida real:**

```text
[ 5 11]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Batch matmul: lote de 2 matrices 2x2
lote_A = np.zeros((2, 2, 2))
lote_B = np.ones((2, 2, 2))
resultado = lote_A @ lote_B
print('Forma del lote:', resultado.shape)
```

**Salida real:**

```text
Forma del lote: (2, 2, 2)
```

## 8. Errores frecuentes y casos borde

1. Multiplicación escalar: `matmul` no admite escalares; usar `*` para escalado.

## 9. Buenas prácticas y rendimiento

* Usar el operador `@` por su claridad matemática y estricta conformidad con PEP 465.

## 10. Métodos relacionados

* `dot` — Producto punto general.

## 11. Referencias oficiales

* **API Reference:** [`numpy.matmul` y operador `@`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) (NumPy 2.x).
