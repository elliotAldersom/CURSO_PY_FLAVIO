# `numpy.multiply`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.multiply(x1, x2, /, out=None, *, where=True, casting='same_kind', order='K', dtype=None)
```

## 2. ¿Qué es?

Es una **función universal (ufunc)** que calcula el producto de Hadamard (multiplicación elemento por elemento) entre dos arreglos.

## 3. ¿Para qué sirve?

Escala tensores, aplica máscaras numéricas o calcula ponderaciones sin bucles.

## 4. ¿Cómo funciona?

1. Multiplica las celdas en las mismas coordenadas. **No debe confundirse con la multiplicación matricial algebraica (`matmul` o `@`)**.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `x1`, `x2` | arreglos | Obligatorio | Posicional | Factores a multiplicar. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.multiply([2, 3], [4, 5]))
```

**Salida real:**

```text
[ 8 15]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[1, 2], [3, 4]])
print(m * 2)
```

**Salida real:**

```text
[[2 4]
 [6 8]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
precios = np.array([100.0, 50.0])
descuentos = np.array([0.9, 0.8])
print('Precios finales:', np.multiply(precios, descuentos))
```

**Salida real:**

```text
Precios finales: [90. 40.]
```

## 8. Errores frecuentes y casos borde

1. Confundir `*` (producto elemento a elemento) con `@` (multiplicación matricial).

## 9. Buenas prácticas y rendimiento

* Usar `*` en la mayoría de los casos; usar `np.multiply` cuando se requiera `out`.

## 10. Métodos relacionados

* `matmul` — Multiplicación matricial de álgebra lineal.

## 11. Referencias oficiales

* **API Reference:** [`numpy.multiply`](https://numpy.org/doc/stable/reference/generated/numpy.multiply.html) (NumPy 2.x).
