# `numpy.arange`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.arange([start,] stop[, step,], dtype=None, *, like=None)
```

## 2. ¿Qué es?

Es una **función constructora de secuencias** análoga a `range` de Python pero que retorna un arreglo `ndarray` vectorizado con soporte de pasos flotantes.

## 3. ¿Para qué sirve?

Genera secuencias numéricas continuas o espaciadas uniformemente para índices y coordenadas.

## 4. ¿Cómo funciona?

1. Calcula la longitud requerida y llena el búfer contiguo en C en una sola operación de CPU.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `start` | número | Opcional | `0` | Valor inicial de la secuencia. |
| `stop` | número | Obligatorio | Posicional | Límite superior (excluido). |
| `step` | número | Opcional | `1` | Incremento entre elementos. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.arange(5))
```

**Salida real:**

```text
[0 1 2 3 4]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.arange(10, 30, 5))
```

**Salida real:**

```text
[10 15 20 25]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
pasos = np.arange(0, 1, 0.2)
print(np.round(pasos, 1))
```

**Salida real:**

```text
[0.  0.2 0.4 0.6 0.8]
```

## 8. Errores frecuentes y casos borde

1. Imprecisión flotante con `step` no entero: Usar `linspace` en su lugar.

## 9. Buenas prácticas y rendimiento

* Usar `arange` para enteros y `linspace` para números continuos con decimales.

## 10. Métodos relacionados

* `linspace` — Intervalos equiespaciados exactos.

## 11. Referencias oficiales

* **API Reference:** [`numpy.arange`](https://numpy.org/doc/stable/reference/generated/numpy.arange.html) (NumPy 2.x).
