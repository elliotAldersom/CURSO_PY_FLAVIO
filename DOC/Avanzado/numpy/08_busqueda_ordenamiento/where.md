# `numpy.where`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.where(condition, [x, y, /])
```

## 2. ¿Qué es?

Es una **función condicional vectorizada** que opera como un selector ternario `x if condition else y` elemento por elemento, o devuelve las coordenadas donde `condition` es `True`.

## 3. ¿Para qué sirve?

Reemplaza condicionales anidados e imputa valores de forma vectorizada sin bucles.

## 4. ¿Cómo funciona?

1. Si se proporcionan `x` e `y`, devuelve un arreglo eligiendo valores según `condition`. Si sólo se pasa `condition`, retorna una tupla de arreglos de índices.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `condition` | arreglo booleano | Obligatorio | Posicional | Condición a evaluar. |
| `x`, `y` | valores, arreglos | Opcional | `None` | Valor si es `True` (`x`) o si es `False` (`y`). |

## 6. Retorno

`numpy.ndarray` o `tuple[ndarray, ...]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([10, -5, 20, -2])
# Si es menor a 0 reemplazar por 0, sino conservar
print(np.where(arr < 0, 0, arr))
```

**Salida real:**

```text
[10  0 20  0]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
arr = np.array([10, 20, 30, 40])
# Obtener los índices de los elementos mayores a 25
indices = np.where(arr > 25)
print('Índices coincidentes:', indices[0])
```

**Salida real:**

```text
Índices coincidentes: [2 3]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
goles = np.array([25, 12, 19])
categorias = np.where(goles >= 20, 'Goleador', 'Normal')
print(categorias)
```

**Salida real:**

```text
['Goleador' 'Normal' 'Normal']
```

## 8. Errores frecuentes y casos borde

1. Olvidar que sin `x` e `y`, `where` devuelve una tupla de arreglos con los índices coincidentes.

## 9. Buenas prácticas y rendimiento

* Herramienta estándar para binarización de etiquetas (0 y 1) en Machine Learning.

## 10. Métodos relacionados

* `select` — Condiciones múltiples.

## 11. Referencias oficiales

* **API Reference:** [`numpy.where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html) (NumPy 2.x).
