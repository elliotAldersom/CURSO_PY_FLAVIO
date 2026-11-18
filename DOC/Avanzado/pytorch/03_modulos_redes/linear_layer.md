# PyTorch: Capa Densa torch.nn.Linear

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.nn.Linear(in_features, out_features, bias=True, device=None, dtype=None)
```

## 2. ¿Qué es?

`nn.Linear` aplica una transformación afín lineal sobre los datos de entrada según la fórmula $y = xA^T + b$.

## 3. ¿Para qué sirve?

Es la capa densamente conectada (Fully Connected / Dense Layer) estándar en arquitecturas de perceptrón multicapa, cabezas de clasificación en Transformers y bloques lineales de proyección.

## 4. ¿Cómo funciona?

Inicializa internamente una matriz de pesos aprendibles `weight` de dimensiones `(out_features, in_features)` mediante la inicialización uniforme de Kaiming He, y opcionalmente un vector de sesgo `bias` de tamaño `(out_features)`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `in_features` | `int` | Obligatorio | N/A | Dimensión de cada muestra de entrada. |
| `out_features` | `int` | Obligatorio | N/A | Dimensión proyectada de cada muestra de salida. |
| `bias` | `bool` | Opcional | `True` | Si es `False`, la capa no aprenderá el sesgo aditivo $b$. |
| `dtype` | `torch.dtype` | Opcional | `None` | Tipo de dato numérico de los pesos. |

## 6. Retorno

`torch.Tensor`. Tensor proyectado de dimensiones `(*, out_features)` preservando dimensiones de batch precedentes.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
import torch.nn as nn

capa = nn.Linear(in_features=3, out_features=2)
x = torch.tensor([[1.0, 2.0, 3.0]])
salida = capa(x)

print(f"Forma de los pesos (weight): {list(capa.weight.shape)}")
print(f"Forma del sesgo (bias): {list(capa.bias.shape)}")
print(f"Salida generada shape: {list(salida.shape)}")
```

**Salida real:**

```text
Forma de los pesos (weight): [2, 3]
Forma del sesgo (bias): [2]
Salida generada shape: [1, 2]
```

### Nivel 2: Intermedio

```python
import torch
import torch.nn as nn

# Capa lineal sin sesgo (bias=False) para proyecciones normalizadas
capa_sin_bias = nn.Linear(4, 2, bias=False)
x = torch.randn(5, 4)  # Batch de 5 muestras de tamaño 4
salida = capa_sin_bias(x)

print(f"Sesgo es None: {capa_sin_bias.bias is None}")
print(f"Salida del batch: {list(salida.shape)}")
```

**Salida real:**

```text
Sesgo es None: True
Salida del batch: [5, 2]
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn

# Operación sobre secuencias 3D (Batch, Longitud_Secuencia, Embed_Dim)
capa_secuencia = nn.Linear(64, 128)
tokens = torch.randn(16, 50, 64)  # 16 oraciones, 50 palabras cada una
proyeccion = capa_secuencia(tokens)

print(f"Dimensiones de batch y secuencia preservadas: {list(proyeccion.shape)}")
```

**Salida real:**

```text
Dimensiones de batch y secuencia preservadas: [16, 50, 128]
```

## 8. Errores frecuentes y casos borde

- **Discrepancia en `in_features`:** Si la última dimensión del tensor de entrada no coincide exactamente con `in_features`, lanza un `RuntimeError: mat1 and mat2 shapes cannot be multiplied`.
- **Aplanar tensores antes de Linear:** Al recibir mapas de características de capas convolucionales (4D), se debe aplanar el tensor con `torch.flatten(x, 1)` antes de pasarlo a `nn.Linear`.

## 9. Buenas prácticas y rendimiento

- Configurar `bias=False` si la capa está seguida inmediatamente por una normalización (`BatchNorm1d` o `LayerNorm`), ya que el sesgo es redundante y se anula matemáticamente.
- Mantener consistencia en dimensiones de embedding en arquitecturas Transformer.

## 10. Métodos relacionados

- [nn_module](nn_module.md)
- [sequential](sequential.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.nn.Linear.html
