# `numpy.eye`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.eye(N, M=None, k=0, dtype=float, order='C', *, like=None)
```

## 2. ¿Qué es?

Es una **función constructora matricial** que retorna una matriz identidad 2D con unos en la diagonal y ceros en el resto.

## 3. ¿Para qué sirve?

Base del álgebra lineal, cálculo de matrices inversas y proyecciones lineales.

## 4. ¿Cómo funciona?

1. Llena con `1` los índices donde fila == columna + k.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `N` | `int` | Obligatorio | Posicional | Filas de la matriz. |
| `M` | `int` | Opcional | `None` | Columnas (si es `None`, es matriz cuadrada $N \times N$). |
| `k` | `int` | Opcional | `0` | Índice de la diagonal (0 principal, positivo arriba, negativo abajo). |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.eye(3))
```

**Salida real:**

```text
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.eye(3, k=1, dtype=int))
```

**Salida real:**

```text
[[0 1 0]
 [0 0 1]
 [0 0 0]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
I = np.eye(2)
A = np.array([[5, 2], [3, 4]])
print('A @ I == A:', np.array_equal(A @ I, A))
```

**Salida real:**

```text
A @ I == A: True
```

## 8. Errores frecuentes y casos borde

1. Confundir `np.eye` con `np.identity` (`identity` sólo crea cuadradas).

## 9. Buenas prácticas y rendimiento

* Usar `k` para matrices de adyacencia o diferencias finitas.

## 10. Métodos relacionados

* `array` — Arreglos generales.

## 11. Referencias oficiales

* **API Reference:** [`numpy.eye`](https://numpy.org/doc/stable/reference/generated/numpy.eye.html) (NumPy 2.x).
