# PyTorch: torch.no_grad y torch.inference_mode

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.no_grad()
torch.inference_mode(mode=True)
```

## 2. ¿Qué es?

Gestores de contexto que desactivan temporalmente el cálculo y rastreo de gradientes en todas las operaciones contenidas dentro de su bloque de código.

## 3. ¿Para qué sirve?

Indispensables durante las fases de validación, evaluación y despliegue en producción: eliminan la sobrecarga computacional de construir grafos dinámicos y reducen drásticamente el consumo de memoria RAM y VRAM.

## 4. ¿Cómo funciona?

Modifican un estado global de hilo en C++ que instruye a los operadores a generar tensores planos sin atributos `grad_fn`. `torch.inference_mode()` (PyTorch 1.9+) es una versión aún más rápida que deshabilita además el versionado de tensores.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `mode` | `bool` | Opcional | `True` | Estado de activación del modo de inferencia. |

## 6. Retorno

`ContextManager`. Gestor de contexto para uso con la sentencia `with`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

x = torch.tensor([2.0], requires_grad=True)

with torch.no_grad():
    y = x * 3

print(f"¿y requiere gradiente?: {y.requires_grad}")
print(f"Nodo grad_fn en y: {y.grad_fn}")
```

**Salida real:**

```text
¿y requiere gradiente?: False
Nodo grad_fn en y: None
```

### Nivel 2: Intermedio

```python
import torch
import torch.nn as nn

red = nn.Linear(4, 2)
entradas = torch.randn(1, 4)

# Inferencia rápida sin consumo de memoria de gradientes
with torch.inference_mode():
    salida = red(entradas)

print(f"Salida de inferencia calculada shape: {list(salida.shape)}")
print(f"Requiere gradiente: {salida.requires_grad}")
```

**Salida real:**

```text
Salida de inferencia calculada shape: [1, 2]
Requiere gradiente: False
```

### Nivel 3: Avanzado

```python
import torch

# Uso como decorador de función
@torch.no_grad()
def predecir(tensor_entrada):
    return tensor_entrada * 10

v = torch.tensor([1.0], requires_grad=True)
res = predecir(v)

print(f"Resultado decorado: {res.item()}")
print(f"Requiere grad: {res.requires_grad}")
```

**Salida real:**

```text
Resultado decorado: 10.0
Requiere grad: False
```

## 8. Errores frecuentes y casos borde

- **Intentar llamar `.backward()` sobre tensores generados dentro de `no_grad`:** Como no se construyó ningún grafo, llamará a un `RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn`.
- **Mutar tensores producidos en `inference_mode`:** Los tensores creados bajo `inference_mode` no rastrean versiones y arrojan excepción si se intenta mutarlos posteriormente.

## 9. Buenas prácticas y rendimiento

- Usar siempre `torch.inference_mode()` en lugar de `torch.no_grad()` en PyTorch moderno para máxima velocidad de inferencia.
- Envolver todos los endpoints de predicción en APIs de producción dentro de este bloque de contexto.

## 10. Métodos relacionados

- [backward](backward.md)
- [grad](grad.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.no_grad.html
- https://pytorch.org/docs/stable/generated/torch.inference_mode.html
