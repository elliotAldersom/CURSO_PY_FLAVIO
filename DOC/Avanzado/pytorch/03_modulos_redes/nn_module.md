# PyTorch: Clase torch.nn.Module

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
class torch.nn.Module(*args, **kwargs)
```

## 2. ¿Qué es?

`torch.nn.Module` es la clase base fundamental para todos los modelos de redes neuronales, capas especializadas y bloques arquitectónicos en PyTorch.

## 3. ¿Para qué sirve?

Provee la infraestructura orientada a objetos para encapsular parámetros aprendibles (`torch.nn.Parameter`), subcapas anidadas, transferencias entre dispositivos y ganchos de ejecución.

## 4. ¿Cómo funciona?

Al subclasificar `nn.Module`, se define la inicialización de capas en `__init__()` y la computación del paso hacia adelante en `forward()`. Al invocar la instancia como `modelo(x)`, PyTorch ejecuta internamente el método `__call__`, gestionando hooks antes y después de `forward()`.

## 5. Parámetros

| Método / Atributo Clave | Tipo | Descripción |
|---|---|---|
| `forward(*input)` | Método | Define la computación lógica que transforma las entradas en predicciones. |
| `parameters()` | Generador | Itera recursivamente sobre todos los pesos y sesgos entrenables del módulo. |
| `to(device)` | Método | Transfiere todas las capas y tensores internos a CPU o GPU de forma atómica. |
| `train(mode=True)` | Método | Pone el módulo en modo entrenamiento (afecta a Dropout y BatchNorm). |
| `eval()` | Método | Pone el módulo en modo evaluación e inferencia determinista. |

## 6. Retorno

`nn.Module`. Instancia de la red neuronal o capa personalizada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
import torch.nn as nn

class RedMinima(nn.Module):
    def __init__(self):
        super().__init__()
        self.capa = nn.Linear(2, 1)

    def forward(self, x):
        return self.capa(x)

red = RedMinima()
entrada = torch.tensor([[1.0, 2.0]])
salida = red(entrada)

print(f"Salida generada shape: {list(salida.shape)}")
print(f"Parámetros registrados: {len(list(red.parameters()))}")
```

**Salida real:**

```text
Salida generada shape: [1, 1]
Parámetros registrados: 2
```

### Nivel 2: Intermedio

```python
import torch
import torch.nn as nn

class PerceptronMulticapa(nn.Module):
    def __init__(self, n_in, n_oculta, n_out):
        super().__init__()
        self.oculta = nn.Linear(n_in, n_oculta)
        self.activacion = nn.ReLU()
        self.salida = nn.Linear(n_oculta, n_out)

    def forward(self, x):
        x = self.activacion(self.oculta(x))
        return self.salida(x)

mlp = PerceptronMulticapa(10, 16, 2)
x = torch.randn(4, 10)
y = mlp(x)

print(f"Batch procesado con éxito shape: {list(y.shape)}")
```

**Salida real:**

```text
Batch procesado con éxito shape: [4, 2]
```

### Nivel 3: Avanzado

```python
import torch.nn as nn

class BloqueResidual(nn.Module):
    def __init__(self, canales):
        super().__init__()
        self.fc = nn.Linear(canales, canales)
        self.relu = nn.ReLU()

    def forward(self, x):
        # Conexión residual (Skip Connection): F(x) + x
        return self.relu(self.fc(x)) + x

bloque = BloqueResidual(8)
print(f"Total parámetros en bloque residual: {sum(p.numel() for p in bloque.parameters())}")
```

**Salida real:**

```text
Total parámetros en bloque residual: 72
```

## 8. Errores frecuentes y casos borde

- **Invocar `modelo.forward(x)` directamente:** Debe llamarse SIEMPRE `modelo(x)`. Invocar directamente `forward()` ignora los hooks de PyTorch y puede causar que autograd o herramientas de perfilado fallen.
- **Olvidar llamar a `super().__init__()`:** Si no se invoca el constructor de la clase base en `__init__`, PyTorch no podrá registrar las capas ni los parámetros.

## 9. Buenas prácticas y rendimiento

- Usar `modelo.train()` y `modelo.eval()` estrictamente al alternar entre épocas de entrenamiento y validación.
- Modularizar arquitecturas complejas descomponiéndolas en submódulos reutilizables que hereden de `nn.Module`.

## 10. Métodos relacionados

- [linear_layer](linear_layer.md)
- [sequential](sequential.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.nn.Module.html
