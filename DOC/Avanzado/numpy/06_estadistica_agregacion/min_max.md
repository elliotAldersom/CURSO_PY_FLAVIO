# `numpy.min` y `numpy.max`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.min(a, axis=None, out=None, keepdims=False, initial=<no_default>, where=True)
numpy.max(a, axis=None, out=None, keepdims=False, initial=<no_default>, where=True)
```

## 2. ¿Qué es?

Son **funciones de reducción extrema** que retornan el valor mínimo o máximo a lo largo de un eje.

## 3. ¿Para qué sirve?

Encuentran extremos de rendimiento, cotas numéricas y límites de normalización Min-Max.

## 4. ¿Cómo funciona?

1. Recorren el búfer contiguo en tiempo $O(N)$ devolviendo el escalar o submatriz extrema.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `int`, tupla | Opcional | `None` | Eje de búsqueda. |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([15, 28, 6, 31])
print(np.min(arr), np.max(arr))
```

**Salida real:**

```text
6 31
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[10, 25], [30, 5]])
print('Mínimo por columna:', np.min(m, axis=0))
print('Máximo por fila:', np.max(m, axis=1))
```

**Salida real:**

```text
Mínimo por columna: [10  5]
Máximo por fila: [25 30]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Escalado Min-Max a rango [0, 1]
datos = np.array([10.0, 20.0, 30.0])
normalizado = (datos - np.min(datos)) / (np.max(datos) - np.min(datos))
print('Normalizado:', normalizado)
```

**Salida real:**

```text
Normalizado: [0.  0.5 1. ]
```

## 8. Errores frecuentes y casos borde

1. Conjunto vacío: Lanza `ValueError`.

## 9. Buenas prácticas y rendimiento

* Usar `np.nanmin` y `np.nanmax` si existen valores nulos.

## 10. Métodos relacionados

* `argmin_argmax` — Índices de los extremos.

## 11. Referencias oficiales

* **API Reference:** [`numpy.min` y `numpy.max`](https://numpy.org/doc/stable/reference/generated/numpy.min.html) (NumPy 2.x).
