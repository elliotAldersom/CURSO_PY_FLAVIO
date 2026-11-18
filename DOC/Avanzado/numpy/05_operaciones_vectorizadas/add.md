# `numpy.add`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.add(x1, x2, /, out=None, *, where=True, casting='same_kind', order='K', dtype=None)
```

## 2. ¿Qué es?

Es una **función universal (ufunc)** que ejecuta la suma aritmética elemento a elemento entre dos arreglos compatibles.

## 3. ¿Para qué sirve?

Suma tensores a nivel de instrucciones SIMD de la CPU con soporte de parámetro `out` para evitar asignaciones de memoria.

## 4. ¿Cómo funciona?

1. Opera a nivel compilado en C. Si se pasa `out=arr`, escribe el resultado directamente sobre el búfer existente sin reservar nueva memoria.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `x1`, `x2` | arreglos | Obligatorio | Posicional | Arreglos a sumar. |
| `out` | arreglo | Opcional | `None` | Búfer destino donde almacenar el resultado in-place. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.add(a, b))
```

**Salida real:**

```text
[5 7 9]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
a = np.ones(3)
b = np.full(3, 5.0)
np.add(a, b, out=a)
print('Suma in-place en búfer a:', a)
```

**Salida real:**

```text
Suma in-place en búfer a: [6. 6. 6.]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
x = np.array([10, 20, 30])
y = np.array([1, 2, 3])
res = np.zeros(3)
np.add(x, y, out=res, where=[True, False, True])
print('Suma condicionada con where:', res)
```

**Salida real:**

```text
Suma condicionada con where: [11.  0. 33.]
```

## 8. Errores frecuentes y casos borde

1. Desbordamiento de enteros (overflow): En tipos `int8`, `127 + 1` se convierte en `-128`.

## 9. Buenas prácticas y rendimiento

* Usar el operador `+` como alias, salvo que se requiera el parámetro `out` para optimizar memoria en producción.

## 10. Métodos relacionados

* `multiply` — Multiplicación vectorizada.

## 11. Referencias oficiales

* **API Reference:** [`numpy.add`](https://numpy.org/doc/stable/reference/generated/numpy.add.html) (NumPy 2.x).
