# `numpy.linalg.det`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.linalg.det(a)
```

## 2. ¿Qué es?

Es una **función algebraica** que calcula el determinante escalar de una matriz cuadrada.

## 3. ¿Para qué sirve?

Determina si una matriz es invertible (si $\det(A) \neq 0$) y cuantifica el factor de escala de transformaciones espaciales.

## 4. ¿Cómo funciona?

1. Computa el determinante a partir de la factorización LU en LAPACK.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | matriz cuadrada | Obligatorio | Posicional | Matriz $N \times N$. |

## 6. Retorno

`float` escalar.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
print(round(np.linalg.det(A), 2))
```

**Salida real:**

```text
-2.0
```

---

### Nivel 2: Intermedio

```python
import numpy as np
# Matriz singular (filas dependientes)
S = np.array([[1, 2], [2, 4]])
print('Determinante singular:', np.linalg.det(S))
```

**Salida real:**

```text
Determinante singular: 0.0
```

---

### Nivel 3: Avanzado

```python
import numpy as np
def es_invertible(matriz):
    return not np.isclose(np.linalg.det(matriz), 0.0)

print('¿Es A invertible?:', es_invertible(np.array([[2, 1], [1, 2]])))
```

**Salida real:**

```text
¿Es A invertible?: True
```

## 8. Errores frecuentes y casos borde

1. Matrices casi singulares pueden dar números muy pequeños cercanos a cero por imprecisión flotante.

## 9. Buenas prácticas y rendimiento

* Comprobar si `np.isclose(det, 0.0)` antes de intentar invertir matrices.

## 10. Métodos relacionados

* `inv` — Matriz inversa.

## 11. Referencias oficiales

* **API Reference:** [`numpy.linalg.det`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html) (NumPy 2.x).
