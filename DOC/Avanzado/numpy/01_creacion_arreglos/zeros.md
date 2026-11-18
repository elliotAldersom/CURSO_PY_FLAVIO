# `numpy.zeros`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.zeros(shape, dtype=float, order='C', *, like=None)
```

## 2. ¿Qué es?

Es una **función de inicialización contigua** que retorna un arreglo de dimensiones dadas lleno exclusivamente de ceros.

## 3. ¿Para qué sirve?

Preasigna búferes de memoria para acumulación matricial sin costo de realocación.

## 4. ¿Cómo funciona?

1. Reserva memoria limpia inicializada a cero en C.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `shape` | `int`, tupla | Obligatorio | Posicional | Dimensiones del arreglo. |
| `dtype` | tipo | Opcional | `float64` | Tipo físico de las celdas. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.zeros(3))
```

**Salida real:**

```text
[0. 0. 0.]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.zeros((2, 3), dtype=np.int32))
```

**Salida real:**

```text
[[0 0 0]
 [0 0 0]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
tensor = np.zeros((2, 2, 2), dtype=np.uint8)
print('Dimensiones:', tensor.shape)
```

**Salida real:**

```text
Dimensiones: (2, 2, 2)
```

## 8. Errores frecuentes y casos borde

1. Olvidar que el tipo por defecto es `float64`.

## 9. Buenas prácticas y rendimiento

* Preasignar memoria con `zeros` antes de llenar datos en bucles intensivos.

## 10. Métodos relacionados

* `ones` — Inicialización a unos.
* `full` — Valor arbitrario.

## 11. Referencias oficiales

* **API Reference:** [`numpy.zeros`](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html) (NumPy 2.x).
