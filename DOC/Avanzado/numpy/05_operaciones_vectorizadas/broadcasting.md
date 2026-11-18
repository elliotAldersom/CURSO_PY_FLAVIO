# Reglas de Broadcasting en NumPy

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
# Regla matemática de compatibilidad dimensional:
# Dos dimensiones son compatibles si son iguales o una de ellas es 1.
```

## 2. ¿Qué es?

Es el **mecanismo de difusión dimensional** que permite operar aritméticamente entre arreglos de diferentes formas sin duplicar físicamente los datos en memoria.

## 3. ¿Para qué sirve?

Permite sumar un vector a cada fila de una matriz o escalar una matriz por un escalar sin reservar memoria adicional.

## 4. ¿Cómo funciona?

1. Alinea las tuplas de dimensiones empezando por la derecha (*trailing dimensions*).
2. Si una dimensión es `1`, la estira virtualmente ajustando sus estrías a 0 bytes.

## 5. Parámetros

| Regla | Descripción |
| :--- | :--- |
| Alineación derecha | Compara `shape` desde el último eje hacia la izquierda. |
| Expansión virtual | Si una dimensión vale 1, se simula su repetición sin copiar datos en RAM. |

## 6. Retorno

`numpy.ndarray` con la forma máxima expandida.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
arr = np.array([1, 2, 3])
print(arr + 10)
```

**Salida real:**

```text
[11 12 13]
```

---

### Nivel 2: Intermedio

```python
import numpy as np
matriz = np.ones((2, 3))
vector = np.array([10, 20, 30])
print(matriz + vector)
```

**Salida real:**

```text
[[11. 21. 31.]
 [11. 21. 31.]]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
columna = np.array([[1], [2], [3]]) # 3x1
fila = np.array([10, 20])           # 1x2
print('Matriz resultante 3x2:\n', columna + fila)
```

**Salida real:**

```text
Matriz resultante 3x2:
 [[11 21]
 [12 22]
 [13 23]]
```

## 8. Errores frecuentes y casos borde

1. Intentar operar formas incompatibles (p. ej. `(2, 3)` con `(2,)`): Lanza `ValueError: operands could not be broadcast together`.

## 9. Buenas prácticas y rendimiento

* Emplear `None` o `np.newaxis` para añadir ejes unitarios y forzar compatibilidad.

## 10. Métodos relacionados

* `expand_dims` — Expansión explícita.

## 11. Referencias oficiales

* **API Reference:** [Reglas de Broadcasting en NumPy](https://numpy.org/doc/stable/user/basics.broadcasting.html) (NumPy 2.x).
