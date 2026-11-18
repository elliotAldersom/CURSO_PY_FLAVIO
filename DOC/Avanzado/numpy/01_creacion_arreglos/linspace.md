# `numpy.linspace`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0)
```

## 2. ¿Qué es?

Es una **función constructora lineal** que devuelve números espaciados uniformemente durante un intervalo numérico especificado.

## 3. ¿Para qué sirve?

Genera muestras exactas para gráficos, coordenadas matemáticas y funciones continuas.

## 4. ¿Cómo funciona?

1. Divide el intervalo exacto $[start, stop]$ en $num - 1$ pasos matemáticos deterministas.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `start` | número | Obligatorio | Posicional | Punto inicial. |
| `stop` | número | Obligatorio | Posicional | Punto final. |
| `num` | `int` | Opcional | `50` | Cantidad de muestras a generar. |

## 6. Retorno

`numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.linspace(0, 10, num=5))
```

**Salida real:**

```text
[ 0.   2.5  5.   7.5 10. ]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
print(np.linspace(0, 1, num=4, endpoint=False))
```

**Salida real:**

```text
[0.   0.25 0.5  0.75]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
muestras, paso = np.linspace(0, 100, num=5, retstep=True)
print('Paso calculado:', paso)
```

**Salida real:**

```text
Paso calculado: 25.0
```

## 8. Errores frecuentes y casos borde

1. Olvidar que por defecto `endpoint=True` incluye el valor final.

## 9. Buenas prácticas y rendimiento

* Es la herramienta estándar para muestrear funciones matemáticas en Matplotlib.

## 10. Métodos relacionados

* `arange` — Secuencias por tamaño de paso.

## 11. Referencias oficiales

* **API Reference:** [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html) (NumPy 2.x).
