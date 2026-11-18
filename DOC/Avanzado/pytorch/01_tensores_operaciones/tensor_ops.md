# PyTorch: Operaciones de Transformación Tensorial (reshape, view, cat, matmul)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
Tensor.view(*shape) -> Tensor
Tensor.reshape(*shape) -> Tensor
torch.cat(tensors, dim=0, *, out=None) -> Tensor
torch.matmul(input, other, *, out=None) -> Tensor
```

## 2. ¿Qué es?

Conjunto de operaciones esenciales para remodelar geometrías multidimensionales, concatenar batches y ejecutar multiplicaciones matriciales de alta velocidad.

## 3. ¿Para qué sirve?

Permiten adaptar las dimensiones de tensores para que coincidan con los requerimientos de entrada de capas densas (`view`/`reshape`), agrupar lotes (`cat`) y computar combinaciones lineales (`matmul`).

## 4. ¿Cómo funciona?

`view` altera exclusivamente los metadatos de tamaño y zancada (*stride*) sin copiar memoria pero exige contigüidad física. `reshape` devuelve una vista si es contigua o genera una copia si no lo es. `matmul` delega en librerías BLAS/cuBLAS de GPU altamente optimizadas.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `*shape` | `int...` | Obligatorio | N/A | Nuevas dimensiones geométricas deseadas (permite `-1` para inferencia automática). |
| `tensors` | `Sequence[Tensor]` | Obligatorio | N/A | Lista de tensores a unir. |
| `dim` | `int` | Opcional | `0` | Eje o dimensión sobre la cual concatenar. |
| `input, other` | `Tensor` | Obligatorio | N/A | Tensores a multiplicar matricialmente. |

## 6. Retorno

`torch.Tensor`. Tensor resultante de la operación.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

x = torch.arange(6)  # [0, 1, 2, 3, 4, 5]
# Remodelado a matriz 2x3 infiriendo columnas con -1
m = x.view(2, -1)

print(f"Shape original: {list(x.shape)}")
print(f"Shape remodelada: {list(m.shape)}")
print(f"Contenido:\n{m.tolist()}")
```

**Salida real:**

```text
Shape original: [6]
Shape remodelada: [2, 3]
Contenido:
[[0, 1, 2], [3, 4, 5]]
```

### Nivel 2: Intermedio

```python
import torch

t1 = torch.ones(2, 3)
t2 = torch.zeros(2, 3)

# Concatenación a lo largo del eje 0 (filas) y eje 1 (columnas)
cat_filas = torch.cat([t1, t2], dim=0)
cat_cols = torch.cat([t1, t2], dim=1)

print(f"Shape concatenando filas (dim=0): {list(cat_filas.shape)}")
print(f"Shape concatenando columnas (dim=1): {list(cat_cols.shape)}")
```

**Salida real:**

```text
Shape concatenando filas (dim=0): [4, 3]
Shape concatenando columnas (dim=1): [2, 6]
```

### Nivel 3: Avanzado

```python
import torch

# Multiplicación matricial (2x3) @ (3x2) -> (2x2)
A = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
B = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])

# Operador @ es azúcar sintáctico de torch.matmul
C = A @ B
print(f"Forma resultante: {list(C.shape)}")
print(f"Resultado:\n{C.tolist()}")
```

**Salida real:**

```text
Forma resultante: [2, 2]
Resultado:
[[4.0, 5.0], [10.0, 11.0]]
```

## 8. Errores frecuentes y casos borde

- **`RuntimeError: view size is not compatible with input tensor's size and stride`:** Ocurre al llamar `.view()` sobre un tensor que fue transpuesto (`.t()`) o permutado, perdiendo contigüidad en memoria. Solución: usar `.reshape()` o llamar `.contiguous().view()`.
- **Discrepancia de dimensiones en matmul:** Multiplicar matrices donde las columnas de $A$ no coinciden con las filas de $B$ lanza un error dimensional inmediato.

## 9. Buenas prácticas y rendimiento

- Usar el operador `@` en lugar de `torch.matmul` para código matemático más legible.
- Emplear `-1` en una de las dimensiones para que PyTorch deduzca automáticamente el tamaño según el volumen total de elementos.

## 10. Métodos relacionados

- [tensor_creation](tensor_creation.md)
- [cuda_device](cuda_device.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.reshape.html
