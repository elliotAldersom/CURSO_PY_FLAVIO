# PyTorch: Creación de Tensores (torch.tensor, zeros, randn)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.tensor(data, *, dtype=None, device=None, requires_grad=False, pin_memory=False)
torch.zeros(*size, *, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False)
torch.randn(*size, *, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False)
```

## 2. ¿Qué es?

Las funciones de creación de tensores instancian bloques de memoria homogéneos multidimensionales (`torch.Tensor`) a partir de colecciones de Python, arreglos de NumPy o generadores matemáticos (ceros, unos, distribuciones normales estándar).

## 3. ¿Para qué sirve?

Constituyen la base fundamental de entrada de cualquier canal de procesamiento o red neuronal, asignando el tipo de dato físico (`dtype`), el dispositivo de hardware (`device`) y las propiedades de autograd.

## 4. ¿Cómo funciona?

Asignan memoria contigua (en RAM o VRAM), configuran los pasos de zancada (*strides*) para indexación eficiente y retornan la estructura tensorial lista para cálculo vectorizado.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` / `*size` | `ArrayLike` o `int...` | Obligatorio | N/A | Datos a copiar o dimensiones geométricas `(d0, d1, ...)`. |
| `dtype` | `torch.dtype` | Opcional | `None` | Tipo físico de dato (`torch.float32`, `torch.int64`, etc.). |
| `device` | `torch.device` o `str` | Opcional | `'cpu'` | Dispositivo de hardware de asignación (`'cpu'`, `'cuda'`). |
| `requires_grad` | `bool` | Opcional | `False` | Si es `True`, activa el rastreo de operaciones para Autograd. |

## 6. Retorno

`torch.Tensor`. El tensor instanciado en el dispositivo indicado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

# Creación directa desde lista de Python
t = torch.tensor([1.0, 2.0, 3.0])
print(f"Tensor creado: {t.tolist()}")
print(f"Forma: {list(t.shape)}")
print(f"Tipo: {t.dtype}")
```

**Salida real:**

```text
Tensor creado: [1.0, 2.0, 3.0]
Forma: [3]
Tipo: torch.float32
```

### Nivel 2: Intermedio

```python
import torch

# Inicialización con ceros y distribución normal estándar
z = torch.zeros(2, 3, dtype=torch.float32)
r = torch.randn(2, 2, generator=torch.manual_seed(42))

print(f"Tensor de ceros shape: {list(z.shape)}")
print(f"Tensor aleatorio normal:\n{r.tolist()}")
```

**Salida real:**

```text
Tensor de ceros shape: [2, 3]
Tensor aleatorio normal:
[[0.3366904854774475, 0.12880949676036835], [0.23446239531040192, 0.2303255945444107]]
```

### Nivel 3: Avanzado

```python
import numpy as np
import torch

arr = np.array([10, 20, 30], dtype=np.int64)

# torch.from_numpy comparte el mismo búfer de memoria subyacente (Zero-Copy)
t_zero_copy = torch.from_numpy(arr)
arr[0] = 99  # Modificar numpy altera el tensor

print(f"Valor en tensor tras mutar array numpy: {t_zero_copy[0].item()}")
```

**Salida real:**

```text
Valor en tensor tras mutar array numpy: 99
```

## 8. Errores frecuentes y casos borde

- **Confundir `torch.Tensor` con `torch.tensor`:** `torch.Tensor()` con mayúscula es el constructor sin inicializar que asigna memoria con basura aleatoria. Usar SIEMPRE `torch.tensor()` con minúscula que copia datos con seguridad.
- **Pérdida de rendimiento por conversión innecesaria:** Pasar listas gigantes de Python elemento a elemento es lento; convertir a NumPy primero y usar `torch.from_numpy()`.

## 9. Buenas prácticas y rendimiento

- Usar `torch.from_numpy()` para evitar duplicar memoria RAM en datasets masivos.
- Fijar semillas deterministas con `torch.manual_seed(seed)` para reproducibilidad.

## 10. Métodos relacionados

- [tensor_ops](tensor_ops.md)
- [cuda_device](cuda_device.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.tensor.html
