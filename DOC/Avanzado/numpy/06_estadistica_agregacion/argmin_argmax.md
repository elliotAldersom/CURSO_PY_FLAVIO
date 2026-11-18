# `numpy.argmin` y `numpy.argmax`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.argmin(a, axis=None, out=None, *, keepdims=False)
numpy.argmax(a, axis=None, out=None, *, keepdims=False)
```

## 2. ¿Qué es?

Son **funciones de localización de índices** que retornan la posición entera del valor mínimo o máximo a lo largo de un eje.

## 3. ¿Para qué sirve?

Identifican la clase con mayor probabilidad en redes de clasificación o el atleta con mejor marca.

## 4. ¿Cómo funciona?

1. Si `axis=None`, devuelve el índice lineal aplanado. Con `axis=0` o `1`, devuelve las posiciones a lo largo de ese eje.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `int` | Opcional | `None` | Eje de evaluación. |

## 6. Retorno

`int` o `numpy.ndarray[int]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([15, 31, 8, 22])
print('Posición del máximo:', np.argmax(arr))
```

**Salida real:**

```text
Posición del máximo: 1
```

---

### Nivel 2: Intermedio

```python
import numpy as np
probabilidades = np.array([
    [0.1, 0.7, 0.2],
    [0.8, 0.1, 0.1]
])
# Clase predicha para cada muestra (axis=1)
print('Clases predichas:', np.argmax(probabilidades, axis=1))
```

**Salida real:**

```text
Clases predichas: [1 0]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
m = np.array([[10, 50], [40, 20]])
idx_lin = np.argmax(m)
fila, col = np.unravel_index(idx_lin, m.shape)
print(f'Máximo en coordenadas: fila {fila}, col {col}')
```

**Salida real:**

```text
Máximo en coordenadas: fila 0, col 1
```

## 8. Errores frecuentes y casos borde

1. Si existen empates, devuelve únicamente el índice de la primera aparición.

## 9. Buenas prácticas y rendimiento

* Combinar con `np.unravel_index()` para traducir índices aplanados a coordenadas 2D.

## 10. Métodos relacionados

* `min_max` — Valores extremos.

## 11. Referencias oficiales

* **API Reference:** [`numpy.argmin` y `numpy.argmax`](https://numpy.org/doc/stable/reference/generated/numpy.argmax.html) (NumPy 2.x).
