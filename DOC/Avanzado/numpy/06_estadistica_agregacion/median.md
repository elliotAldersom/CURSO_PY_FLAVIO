# `numpy.median`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.median(a, axis=None, out=None, overwrite_input=False, keepdims=False)
```

## 2. ¿Qué es?

Es una **función de reducción robusta** que calcula el valor mediano a lo largo del eje especificado.

## 3. ¿Para qué sirve?

Provee una medida de centro insensible a valores atípicos extremos.

## 4. ¿Cómo funciona?

1. Ordena una copia de los datos y devuelve el valor central.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | arreglo | Obligatorio | Posicional | Arreglo a evaluar. |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.median([1, 2, 100]))
```

**Salida real:**

```text
2.0
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[1, 5], [3, 9]])
print('Mediana por columna:', np.median(m, axis=0))
```

**Salida real:**

```text
Mediana por columna: [2. 7.]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
datos = np.array([1.0, np.nan, 5.0])
print('Mediana con nanmedian:', np.nanmedian(datos))
```

**Salida real:**

```text
Mediana con nanmedian: 3.0
```

## 8. Errores frecuentes y casos borde

1. `NaN` en los datos contamina el resultado: Usar `np.nanmedian()`.

## 9. Buenas prácticas y rendimiento

* Preferir la mediana para métricas asimétricas como ingresos o tiempos de respuesta.

## 10. Métodos relacionados

* `mean` — Media aritmética.

## 11. Referencias oficiales

* **API Reference:** [`numpy.median`](https://numpy.org/doc/stable/reference/generated/numpy.median.html) (NumPy 2.x).
