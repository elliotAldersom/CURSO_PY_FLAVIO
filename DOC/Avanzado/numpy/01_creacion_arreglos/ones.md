# `numpy.ones`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.ones(shape, dtype=None, order='C', *, like=None)
```

## 2. ¿Qué es?

Es una **función de inicialización contigua** que retorna un nuevo arreglo lleno de unos.

## 3. ¿Para qué sirve?

Crea máscaras multiplicativas, pesos neutros o matrices base para escalado.

## 4. ¿Cómo funciona?

1. Asigna memoria y escribe el valor `1` en cada posición según el `dtype`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `shape` | `int`, tupla | Obligatorio | Posicional | Dimensiones físicas. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.ones(4))
```

**Salida real:**

```text
[1. 1. 1. 1.]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.ones((2, 2), dtype=np.int16))
```

**Salida real:**

```text
[[1 1]
 [1 1]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
pesos = np.ones(5) * 2.5
print(pesos)
```

**Salida real:**

```text
[2.5 2.5 2.5 2.5 2.5]
```

## 8. Errores frecuentes y casos borde

1. Dimensiones erróneas por pasar enteros sueltos en vez de tupla: `np.ones(2, 3)` falla. Usar `np.ones((2, 3))`.

## 9. Buenas prácticas y rendimiento

* Pasar la dimensión como tupla `(filas, cols)`.

## 10. Métodos relacionados

* `zeros` — Ceros.
* `full` — Valores arbitrarios.

## 11. Referencias oficiales

* **API Reference:** [`numpy.ones`](https://numpy.org/doc/stable/reference/generated/numpy.ones.html) (NumPy 2.x).
