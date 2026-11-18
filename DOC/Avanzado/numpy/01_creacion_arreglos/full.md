# `numpy.full`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.full(shape, fill_value, dtype=None, order='C', *, like=None)
```

## 2. ¿Qué es?

Es una **función constructora** que crea un arreglo de dimensiones dadas relleno con un valor constante especificado.

## 3. ¿Para qué sirve?

Inicializa arreglos con valores centinela o constantes de negocio.

## 4. ¿Cómo funciona?

1. Reserva memoria y llena el búfer con `fill_value` adaptado a `dtype`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `shape` | `int`, tupla | Obligatorio | Posicional | Dimensiones del arreglo. |
| `fill_value` | escalar | Obligatorio | Posicional | Valor de relleno constante. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.full(3, 7))
```

**Salida real:**

```text
[7 7 7]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.full((2, 2), 99.5, dtype=np.float32))
```

**Salida real:**

```text
[[99.5 99.5]
 [99.5 99.5]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
mascara = np.full((3, 3), False, dtype=bool)
print(mascara)
```

**Salida real:**

```text
[[False False False]
 [False False False]
 [False False False]]
```

## 8. Errores frecuentes y casos borde

1. Desbordamiento de tipo si `fill_value` supera el rango de `dtype`.

## 9. Buenas prácticas y rendimiento

* Usar para inicializar con `np.nan` matrices flotantes.

## 10. Métodos relacionados

* `zeros` — Ceros.
* `ones` — Unos.

## 11. Referencias oficiales

* **API Reference:** [`numpy.full`](https://numpy.org/doc/stable/reference/generated/numpy.full.html) (NumPy 2.x).
