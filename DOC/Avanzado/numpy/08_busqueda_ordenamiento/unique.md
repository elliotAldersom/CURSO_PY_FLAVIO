# `numpy.unique`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.unique(ar, return_index=False, return_inverse=False, return_counts=False, axis=None, *, equal_nan=True)
```

## 2. ¿Qué es?

Es una **función de deduplicación y conteo** que encuentra y retorna los elementos únicos ordenados de un arreglo.

## 3. ¿Para qué sirve?

Identifica categorías únicas, calcula tablas de frecuencias y genera identificadores enteros para codificación.

## 4. ¿Cómo funciona?

1. Ordena los datos internamente y elimina duplicados consecutivos en C.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `return_counts` | `bool` | Opcional | `False` | Si es `True`, devuelve el conteo de frecuencia de cada elemento. |
| `return_inverse` | `bool` | Opcional | `False` | Devuelve los índices enteros para reconstruir el arreglo original (codificación de categorías). |

## 6. Retorno

`numpy.ndarray` o tupla de arreglos.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([3, 1, 2, 3, 1, 4])
print(np.unique(arr))
```

**Salida real:**

```text
[1 2 3 4]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
arr = np.array(['DEL', 'MED', 'DEL', 'DEF', 'DEL'])
valores, conteos = np.unique(arr, return_counts=True)
for v, c in zip(valores, conteos):
    print(f'{v}: {c}')
```

**Salida real:**

```text
DEF: 1
DEL: 3
MED: 1
```

---

### Nivel 3: Avanzado

```python
import numpy as np
categorias = np.array(['Madrid', 'Barca', 'Madrid', 'Arsenal'])
unicos, codigos = np.unique(categorias, return_inverse=True)
print('Categorías únicas:', unicos)
print('Códigos numéricos asignados:', codigos)
```

**Salida real:**

```text
Categorías únicas: ['Arsenal' 'Barca' 'Madrid']
Códigos numéricos asignados: [2 1 2 0]
```

## 8. Errores frecuentes y casos borde

1. Olvidar que por defecto aplana matrices multidimensionales si no se pasa `axis`.

## 9. Buenas prácticas y rendimiento

* Usar `return_inverse=True` para implementar un LabelEncoder nativo ultra veloz en NumPy sin Scikit-learn.

## 10. Métodos relacionados

* `where` — Búsqueda condicional.

## 11. Referencias oficiales

* **API Reference:** [`numpy.unique`](https://numpy.org/doc/stable/reference/generated/numpy.unique.html) (NumPy 2.x).
