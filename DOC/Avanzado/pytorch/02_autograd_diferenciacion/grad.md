# PyTorch: Atributo Tensor.grad y requires_grad

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
Tensor.requires_grad: bool
Tensor.grad: Optional[Tensor]
```

## 2. ¿Qué es?

`requires_grad` es una bandera booleana que instruye a PyTorch a registrar todas las operaciones matemáticas aplicadas sobre ese tensor para rastreo en Autograd. `grad` es el atributo donde se almacenan las derivadas acumuladas tras invocar `.backward()`.

## 3. ¿Para qué sirve?

Permite controlar quirúrgicamente qué partes de una red neuronal deben actualizarse durante el entrenamiento y cuáles deben permanecer congeladas (técnica clave en Transfer Learning y Fine-Tuning).

## 4. ¿Cómo funciona?

Si un tensor tiene `requires_grad=True`, cada operación genera un nodo `grad_fn` en el grafo de computación dinámica. Al ejecutar `backward()`, el valor del gradiente se suma (`+=`) al tensor existente en `.grad`.

## 5. Parámetros

| Parámetro / Propiedad | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `requires_grad` | `bool` | Opcional | `False` | Activa el registro en el motor de diferenciación de Autograd. |
| `grad` | `Tensor` o `None` | Solo lectura | `None` | Tensor con las derivadas parciales acumuladas tras `backward()`. |

## 6. Retorno

`Tensor` o `None`. Tensor con las derivadas exactas calculadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

a = torch.tensor([2.0], requires_grad=True)
b = torch.tensor([3.0])

c = a + b
print(f"¿a requiere gradiente?: {a.requires_grad}")
print(f"¿c requiere gradiente?: {c.requires_grad}")
print(f"Nodo grad_fn asociado a c: {c.grad_fn.__class__.__name__}")
```

**Salida real:**

```text
¿a requiere gradiente?: True
¿c requiere gradiente?: True
Nodo grad_fn asociado a c: AddBackward0
```

### Nivel 2: Intermedio

```python
import torch

x = torch.tensor([4.0], requires_grad=True)
y = x**2

y.backward()
print(f"Gradiente primer backward (2*4): {x.grad.item()}")

# Sin zero_grad, el segundo backward ACUMULA sobre el anterior
y2 = x**2
y2.backward()
print(f"Gradiente acumulado tras segundo backward (8 + 8): {x.grad.item()}")
```

**Salida real:**

```text
Gradiente primer backward (2*4): 8.0
Gradiente acumulado tras segundo backward (8 + 8): 16.0
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn

# Congelación de capas (Freezing) para Transfer Learning
capa = nn.Linear(10, 2)
for param in capa.parameters():
    param.requires_grad = False

print(f"Parámetros congelados para entrenamiento: {all(not p.requires_grad for p in capa.parameters())}")
```

**Salida real:**

```text
Parámetros congelados para entrenamiento: True
```

## 8. Errores frecuentes y casos borde

- **Acumulación inadvertida de gradientes:** Debido a que `.grad` suma valores sucesivamente, no limpiar los gradientes entre épocas causa divergencia numérica inmediata.
- **Modificar un tensor in-place con `requires_grad=True`:** Modificar variables con operaciones como `x += 1` puede romper la copia requerida para calcular la derivada en el backward pass.

## 9. Buenas prácticas y rendimiento

- Congelar capas pre-entrenadas estableciendo `param.requires_grad = False` para acelerar el fine-tuning y prevenir olvido catastrófico.
- Usar `x.grad.zero_()` manualmente si no se utiliza un optimizador formal.

## 10. Métodos relacionados

- [backward](backward.md)
- [no_grad](no_grad.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/autograd.html
