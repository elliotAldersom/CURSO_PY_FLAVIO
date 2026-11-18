# `numpy.power`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.power(x1, x2, /, out=None, *, where=True, dtype=None)
```

## 2. ¿Qué es?

Es una **función universal (ufunc)** que eleva cada elemento del primer arreglo a la potencia indicada en el segundo arreglo o escalar.

## 3. ¿Para qué sirve?

Calcula potencias, cuadrados para cálculo de distancias euclidianas o funciones exponenciales discretas.

## 4. ¿Cómo funciona?

1. Ejecuta la exponenciación en C optimizada para potencias enteras o flotantes.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `x1` | arreglo | Obligatorio | Posicional | Base. |
| `x2` | arreglo, escalar | Obligatorio | Posicional | Exponente. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.power([2, 3, 4], 2))
```

**Salida real:**

```text
[ 4  9 16]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
bases = np.array([2, 3])
exponentes = np.array([3, 2])
print(np.power(bases, exponentes))
```

**Salida real:**

```text
[8 9]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Distancia euclidiana al cuadrado (x^2 + y^2)
x = np.array([3.0, 5.0])
y = np.array([4.0, 12.0])
dist_cuadrada = np.power(x, 2) + np.power(y, 2)
print('Distancias euclidianas:', np.sqrt(dist_cuadrada))
```

**Salida real:**

```text
Distancias euclidianas: [ 5. 13.]
```

## 8. Errores frecuentes y casos borde

1. Elevar enteros negativos a exponentes negativos lanza `ValueError: Integers to negative integer powers are not allowed`. Requiere castear a flotante.

## 9. Buenas prácticas y rendimiento

* Usar `**` como sintaxis idiomática directa.

## 10. Métodos relacionados

* `multiply` — Multiplicación simple.

## 11. Referencias oficiales

* **API Reference:** [`numpy.power`](https://numpy.org/doc/stable/reference/generated/numpy.power.html) (NumPy 2.x).
