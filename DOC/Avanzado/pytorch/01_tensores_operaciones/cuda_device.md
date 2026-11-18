# PyTorch: Gestión de Dispositivos y Aceleración CUDA (to, is_available)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.cuda.is_available() -> bool
Tensor.to(*args, device=None, dtype=None, non_blocking=False, copy=False) -> Tensor
```

## 2. ¿Qué es?

Mecanismo de PyTorch para detectar hardware acelerador (NVIDIA CUDA, Apple MPS) y transferir tensores o módulos completos entre la memoria del sistema (CPU) y la memoria del acelerador (VRAM).

## 3. ¿Para qué sirve?

Permite escribir código agnóstico al dispositivo que se ejecuta automáticamente en GPU cuando está disponible o retrocede de manera transparente a CPU sin fallos.

## 4. ¿Cómo funciona?

`torch.cuda.is_available()` consulta los drivers del sistema. El método `.to(device)` asigna memoria en el dispositivo destino, transfiere los bytes por el bus PCIe y retorna una nueva referencia al tensor acelerado.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `device` | `torch.device` o `str` | Obligatorio | N/A | Dispositivo de destino (`'cpu'`, `'cuda'`, `'cuda:0'`, `'mps'`). |
| `non_blocking` | `bool` | Opcional | `False` | Si es `True` y la memoria está fija (*pinned*), ejecuta la transferencia asíncronamente en segundo plano. |

## 6. Retorno

`torch.Tensor` o `nn.Module`. El objeto transferido al dispositivo.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

# Detección determinista agnóstica de hardware
dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Dispositivo activo de ejecución: {dispositivo.type}")
```

**Salida real:**

```text
CUDA disponible: False
Dispositivo activo de ejecución: cpu
```

### Nivel 2: Intermedio

```python
import torch

dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
t = torch.tensor([1.0, 2.0, 3.0])

# Transferencia explícita con .to()
t_device = t.to(dispositivo)
print(f"Dispositivo del tensor: {t_device.device.type}")
```

**Salida real:**

```text
Dispositivo del tensor: cpu
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn

# Transferencia atómica de todos los pesos de un modelo a GPU/CPU
modelo = nn.Linear(5, 1)
dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
modelo.to(dispositivo)

primer_param = next(modelo.parameters())
print(f"Dispositivo de los pesos de la red: {primer_param.device.type}")
```

**Salida real:**

```text
Dispositivo de los pesos de la red: cpu
```

## 8. Errores frecuentes y casos borde

- **`RuntimeError: Expected all tensors to be on the same device`:** Intentar operar un tensor en CPU con uno en CUDA. Tanto los datos de entrada como el modelo deben residir en el mismo dispositivo (`X.to(device)` y `model.to(device)`).
- **Fuga de VRAM (CUDA Out of Memory):** Acumular pérdidas en una lista como `losses.append(loss)` mantiene el grafo de autograd completo en VRAM en cada época. Guardar siempre el escalar en CPU: `losses.append(loss.item())`.

## 9. Buenas prácticas y rendimiento

- Definir siempre al inicio del script `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`.
- Usar `loss.item()` para registrar métricas sin saturar la memoria VRAM.

## 10. Métodos relacionados

- [tensor_creation](tensor_creation.md)
- [nn_module](../03_modulos_redes/nn_module.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/cuda.html
