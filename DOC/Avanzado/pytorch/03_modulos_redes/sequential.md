# PyTorch: Contenedor torch.nn.Sequential

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.nn.Sequential(*args: Module)
torch.nn.Sequential(arg: OrderedDict[str, Module])
```

## 2. ¿Qué es?

`nn.Sequential` es un contenedor que encadena secuencialmente una lista ordenada de módulos y funciones de activación, pasando la salida de cada capa como entrada directa a la siguiente.

## 3. ¿Para qué sirve?

Permite construir redes feed-forward y bloques densos compactos de manera limpia sin tener que declarar explícitamente cada llamada intermedia en el método `forward()`.

## 4. ¿Cómo funciona?

Almacena las capas en un diccionario ordenado interno. Al invocarse, itera a través de cada módulo en el orden de definición, alimentando secuencialmente el tensor de activaciones.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `*args` | `Module...` | Obligatorio | N/A | Secuencia posicional de módulos (`Linear`, `ReLU`, `Dropout`, etc.). |

## 6. Retorno

`nn.Sequential`. Instancia del contenedor secuencial ejecutable.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
import torch.nn as nn

# Construcción rápida de un clasificador binario
modelo = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid()
)

entrada = torch.randn(2, 4)
probabilidades = modelo(entrada)

print(f"Capas en el Sequential: {len(modelo)}")
print(f"Probabilidades de salida shape: {list(probabilidades.shape)}")
```

**Salida real:**

```text
Capas en el Sequential: 4
Probabilidades de salida shape: [2, 1]
```

### Nivel 2: Intermedio

```python
from collections import OrderedDict
import torch.nn as nn

# Construcción con nombres explícitos por capa mediante OrderedDict
red_nombrada = nn.Sequential(OrderedDict([
    ("capa_entrada", nn.Linear(10, 20)),
    ("activacion", nn.ReLU()),
    ("capa_salida", nn.Linear(20, 2))
]))

print(f"Capa accesible por nombre: {red_nombrada.capa_entrada}")
```

**Salida real:**

```text
Capa accesible por nombre: Linear(in_features=10, out_features=20, bias=True)
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn

# Integración de Sequential como submódulo dentro de una clase mayor
class EncoderPersonalizado(nn.Module):
    def __init__(self):
        super().__init__()
        self.bloque = nn.Sequential(
            nn.Linear(32, 16),
            nn.Dropout(0.2),
            nn.ReLU()
        )

    def forward(self, x):
        return self.bloque(x)

enc = EncoderPersonalizado()
x = torch.randn(5, 32)
print(f"Salida del encoder shape: {list(enc(x).shape)}")
```

**Salida real:**

```text
Salida del encoder shape: [5, 16]
```

## 8. Errores frecuentes y casos borde

- **Limitación en arquitecturas no secuenciales:** `nn.Sequential` solo soporta flujos estrictamente lineales con una sola entrada y una sola salida. No puede utilizarse para conexiones residuales (skip connections) ni arquitecturas con múltiples ramas o salidas múltiples.
- **Error de dimensión entre capas contiguas:** El `out_features` de la capa $N$ debe ser idéntico al `in_features` de la capa $N+1$.

## 9. Buenas prácticas y rendimiento

- Usar `nn.Sequential` para bloques compactos repetitivos dentro de redes neuronales más grandes.
- Utilizar `OrderedDict` cuando se desee acceder a capas individuales por nombre semántico.

## 10. Métodos relacionados

- [nn_module](nn_module.md)
- [linear_layer](linear_layer.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.nn.Sequential.html
