# `numpy.std`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True)
```

## 2. ¿Qué es?

Es una **función de dispersión estadística** que calcula la desviación estándar sobre un eje.

## 3. ¿Para qué sirve?

Mide la variabilidad de las mediciones respecto a la media.

## 4. ¿Cómo funciona?

1. **Por defecto `ddof=0` (poblacional):** A diferencia de Pandas (que usa `ddof=1` muestral), en NumPy el divisor es $N$ por defecto.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `ddof` | `int` | Opcional | `0` | Grados de libertad delta (`0` poblacional, `1` muestral). |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(round(np.std([10, 20, 30]), 2))
```

**Salida real:**

```text
8.16
```

---

### Nivel 2: Intermedio

```python
import numpy as np
datos = [10, 20, 30]
print('NumPy default (ddof=0):', round(np.std(datos), 2))
print('Muestral (ddof=1):', round(np.std(datos, ddof=1), 2))
```

**Salida real:**

```text
NumPy default (ddof=0): 8.16
Muestral (ddof=1): 10.0
```

---

### Nivel 3: Avanzado

```python
import numpy as np
m = np.array([[10, 12], [20, 22]])
print('Desvío por columna:', np.std(m, axis=0))
```

**Salida real:**

```text
Desvío por columna: [5. 5.]
```

## 8. Errores frecuentes y casos borde

1. Olvidar que NumPy usa `ddof=0` y no coincide directamente con `df.std()` de Pandas sin pasar `ddof=1`.

## 9. Buenas prácticas y rendimiento

* Fijar explícitamente `ddof=1` si se comparan cálculos con Pandas o estadística muestral.

## 10. Métodos relacionados

* `mean` — Media.

## 11. Referencias oficiales

* **API Reference:** [`numpy.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html) (NumPy 2.x).
