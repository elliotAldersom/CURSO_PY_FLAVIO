# `numpy.array`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0, like=None)
```

## 2. ¿Qué es?

Es la **función constructora fundamental** de NumPy que transforma secuencias de Python (listas, tuplas) en arreglos homogéneos contiguos `ndarray`.

## 3. ¿Para qué sirve?

Convierte estructuras lentas de Python en arreglos optimizados para álgebra y computación vectorial.

## 4. ¿Cómo funciona?

1. Reserva memoria física contigua en C, infiere el tipo común si no se especifica y copia los valores al nuevo búfer.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `object` | secuencia | Obligatorio | Posicional | Datos a convertir. |
| `dtype` | tipo | Opcional | `None` | Tipo de dato físico explícito (`np.int32`, `np.float64`). |
| `copy` | `bool` | Opcional | `True` | Fuerza copia independiente. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([1, 2, 3])
print(arr)
```

**Salida real:**

```text
[1 2 3]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
matriz = np.array([[1, 2], [3, 4]], dtype=np.float32)
print(matriz)
print('Forma:', matriz.shape)
```

**Salida real:**

```text
[[1. 2.]
 [3. 4.]]
Forma: (2, 2)
```

---

### Nivel 3: Avanzado

```python
import numpy as np
datos = np.array([100, 200, 300], dtype=np.int16)
print('Bytes totales:', datos.nbytes)
```

**Salida real:**

```text
Bytes totales: 6
```

## 8. Errores frecuentes y casos borde

1. Listas irregulares (jagged arrays): `np.array([[1, 2], [3]])` genera error o arreglo de objetos en NumPy 2.x.

## 9. Buenas prácticas y rendimiento

* Especificar siempre `dtype` para evitar consumos de memoria innecesarios.

## 10. Métodos relacionados

* `arange` — Secuencias numéricas.
* `zeros` — Arreglos vacíos inicializados a cero.

## 11. Referencias oficiales

* **API Reference:** [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html) (NumPy 2.x).
