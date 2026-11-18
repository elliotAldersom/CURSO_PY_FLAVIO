# `numpy.argsort`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.argsort(a, axis=-1, kind=None, order=None, *, stable=False)
```

## 2. ¿Qué es?

Es una **función de ordenamiento indirecto** que retorna los índices enteros que ordenarían el arreglo a lo largo del eje especificado.

## 3. ¿Para qué sirve?

Permite ordenar múltiples arreglos en paralelo basándose en el orden de uno solo (p. ej. ordenar nombres de atletas según sus tiempos).

## 4. ¿Cómo funciona?

1. Computa el ranking de índices sin mover los datos originales.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | arreglo | Obligatorio | Posicional | Arreglo a analizar. |

## 6. Retorno

`numpy.ndarray[int]` con los índices de orden.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([30, 10, 20])
indices = np.argsort(arr)
print('Índices de orden:', indices)
print('Arreglo ordenado mediante índices:', arr[indices])
```

**Salida real:**

```text
Índices de orden: [1 2 0]
Arreglo ordenado mediante índices: [10 20 30]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
# Ordenar nombres según tiempos de carrera
tiempos = np.array([10.2, 9.8, 10.5])
atletas = np.array(['Atleta_A', 'Atleta_B', 'Atleta_C'])
orden = np.argsort(tiempos)
print('Podio ordenado:', atletas[orden])
```

**Salida real:**

```text
Podio ordenado: ['Atleta_B' 'Atleta_A' 'Atleta_C']
```

---

### Nivel 3: Avanzado

```python
import numpy as np
# Índices descendentes (de mayor a menor)
goles = np.array([21, 28, 15])
top_indices = np.argsort(goles)[::-1]
print('Top goleadores ordenados:', top_indices)
```

**Salida real:**

```text
Top goleadores ordenados: [1 0 2]
```

## 8. Errores frecuentes y casos borde

1. Asumir que `argsort` ordena los valores directamente: Retorna exclusivamente los índices.

## 9. Buenas prácticas y rendimiento

* Técnica obligatoria para sincronizar ordenamientos de múltiples matrices paralelas.

## 10. Métodos relacionados

* `sort` — Ordenamiento directo.

## 11. Referencias oficiales

* **API Reference:** [`numpy.argsort`](https://numpy.org/doc/stable/reference/generated/numpy.argsort.html) (NumPy 2.x).
