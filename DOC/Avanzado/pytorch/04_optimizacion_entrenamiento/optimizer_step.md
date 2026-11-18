# PyTorch: Optimizadores (torch.optim.SGD, Adam, zero_grad, step)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
optimizer.zero_grad(set_to_none=True)
optimizer.step(closure=None)
```

## 2. ¿Qué es?

Los optimizadores de `torch.optim` implementan algoritmos de descenso de gradiente (como SGD con momentum, Adam, AdamW) que actualizan los parámetros entrenables de un modelo en función de los gradientes calculados.

## 3. ¿Para qué sirve?

Resuelven la convergencia numérica del entrenamiento: ajustan los pesos en la dirección que minimiza la función de pérdida sin requerir la actualización manual de miles de tensores.

## 4. ¿Cómo funciona?

`zero_grad()` limpia los gradientes acumulados en `.grad`. `step()` itera sobre la lista de parámetros registrados y aplica la regla de actualización del optimizador (ej. $w = w - \eta \cdot \nabla w$ en SGD).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `params` | `Iterable[Tensor]` | Obligatorio | N/A | Generador de tensores aprendibles (`modelo.parameters()`). |
| `lr` | `float` | Obligatorio | N/A | Tasa de aprendizaje (Learning Rate $\eta$). |
| `weight_decay` | `float` | Opcional | `0.0` | Regularización L2 sobre los pesos para prevenir sobreajuste. |
| `set_to_none` | `bool` | Opcional | `True` | En `zero_grad()`, asigna `None` en lugar de llenar con ceros para ahorrar memoria y tiempo. |

## 6. Retorno

`None`. Muta directamente los tensores de parámetros in-place.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
import torch.optim as optim

w = torch.tensor([5.0], requires_grad=True)
opt = optim.SGD([w], lr=0.1)

# Simulación de pérdida: L = w^2 -> dL/dw = 2*w = 10.0
loss = w**2
loss.backward()

# Actualización: w = 5.0 - 0.1 * 10.0 = 4.0
opt.step()
opt.zero_grad()

print(f"Nuevo valor del peso tras step: {float(w.item()):.2f}")
print(f"Gradiente reiniciado: {w.grad}")
```

**Salida real:**

```text
Nuevo valor del peso tras step: 4.00
Gradiente reiniciado: None
```

### Nivel 2: Intermedio

```python
import torch
import torch.nn as nn
import torch.optim as optim

red = nn.Linear(2, 1)
# Optimizador Adam con regularización L2 (weight_decay)
optimizador = optim.Adam(red.parameters(), lr=0.001, weight_decay=1e-4)

print(f"Optimizador inicializado: {optimizador.__class__.__name__}")
print(f"Tasa de aprendizaje (lr): {optimizador.param_groups[0]['lr']}")
```

**Salida real:**

```text
Optimizador inicializado: Adam
Tasa de aprendizaje (lr): 0.001
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Learning Rate diferenciado por grupos de capas
capa_base = nn.Linear(10, 5)
cabecera = nn.Linear(5, 1)

opt = optim.AdamW([
    {"params": capa_base.parameters(), "lr": 1e-4},
    {"params": cabecera.parameters(), "lr": 1e-3}
])

print(f"Grupos de parámetros configurados: {len(opt.param_groups)}")
print(f"LR de la base: {opt.param_groups[0]['lr']}")
print(f"LR de la cabecera: {opt.param_groups[1]['lr']}")
```

**Salida real:**

```text
Grupos de parámetros configurados: 2
LR de la base: 0.0001
LR de la cabecera: 0.001
```

## 8. Errores frecuentes y casos borde

- **Invertir el orden de `step()` y `zero_grad()`:** Si llamas `zero_grad()` antes de `step()`, los gradientes se eliminan antes de actualizar los pesos y el modelo no aprenderá absolutamente nada.
- **No pasar `modelo.parameters()`:** Olvidar registrar los parámetros en el constructor del optimizador provoca que `step()` no modifique ningún tensor.

## 9. Buenas prácticas y rendimiento

- Usar `optimizer.zero_grad(set_to_none=True)` en lugar de ceros para mejorar el rendimiento de memoria en GPU.
- Preferir `AdamW` sobre `Adam` estándar en modelos Transformer y redes profundas modernas.

## 10. Métodos relacionados

- [loss_functions](loss_functions.md)
- [dataloader](dataloader.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/optim.html
