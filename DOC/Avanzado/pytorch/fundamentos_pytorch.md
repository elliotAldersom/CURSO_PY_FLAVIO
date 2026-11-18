# Fundamentos de PyTorch: Computación Tensorial y Redes Neuronales Profundas en Python

PyTorch es el framework líder a nivel global para investigación y producción de Deep Learning e inteligencia artificial moderna, desarrollado por Meta AI y mantenido bajo la Linux Foundation.

## 2. Introducción

Antes de la adopción masiva de PyTorch, el ecosistema de Deep Learning dependía de frameworks con grafos computacionales estáticos (como TensorFlow 1.x), donde la arquitectura de la red debía compilarse rígidamente antes de ejecutar cualquier dato, complicando la depuración con herramientas estándar de Python.

Lanzado en 2016 por Adam Paszke, Soumith Chintala y Ronan Collobert, PyTorch transformó la industria mediante el paradigma de ejecución inmediata imperativa (**Eager Execution**) y diferenciación automática en tiempo real (**Define-by-Run**): el grafo se construye dinámicamente al paso que el código en Python se ejecuta, permitiendo depurar modelos con `breakpoint()`, estructuras de control nativas (`if`, `for`) y compatibilidad transparente con GPUs mediante CUDA.

## 3. Fundamentos y conceptos

La arquitectura de PyTorch se sostiene sobre cuatro pilares conceptuales innegociables:
1. **Tensores (`torch.Tensor`):** Estructura multidimensional similar a un `ndarray` de NumPy, pero con dos ventajas críticas: puede residir y acelerarse en hardware paralelo (GPUs NVIDIA vía CUDA, Apple Silicon vía MPS) y puede registrar su grafo de operaciones para cálculo de gradientes.
2. **Motor Autograd (`torch.autograd`):** Motor de cálculo diferencial automático que implementa la regla de la cadena reversa (Backpropagation). Rastrea cada operación ejecutada sobre tensores marcados con `requires_grad=True` y evalúa gradientes exactos con `.backward()`.
3. **Módulos Neuronales (`torch.nn.Module`):** Clase base para encapsular capas (pesos y sesgos), funciones de activación y la lógica de inferencia directa (`forward`).
4. **Optimización (`torch.optim`):** Algoritmos numéricos basados en gradiente descendente estocástico (SGD, Adam, AdamW) que actualizan los parámetros entrenables según la señal de pérdida.

## 4. Sintaxis y funcionamiento

El bucle de entrenamiento estándar en PyTorch sigue un ciclo canónico e inmutable de cinco pasos por cada batch:

```python
import torch
import torch.nn as nn
import torch.optim as optim

# NO EJECUTAR (Estructura de referencia de bucle de entrenamiento)
modelo = nn.Linear(in_features=10, out_features=1)
criterio = nn.MSELoss()
optimizador = optim.SGD(modelo.parameters(), lr=0.01)

# 1. Puesta a cero de gradientes del paso anterior
optimizador.zero_grad()
# 2. Paso hacia adelante (Forward pass)
predicciones = modelo(X_batch)
# 3. Cálculo de la función de pérdida
perdida = criterio(predicciones, y_batch)
# 4. Paso hacia atrás (Backward pass / cálculo de derivadas)
perdida.backward()
# 5. Actualización de pesos según la regla del optimizador
optimizador.step()
```

## 5. Ejemplos prácticos progresivos

### Básico

Creación de tensores numéricos, operaciones matriciales e inspección de memoria en CPU.

```python
import torch

# Tensores 2D equivalentes a matrices
A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

# Multiplicación matricial (matmul / @)
C = torch.matmul(A, B)

print(f"Tipo de objeto: {type(C).__name__}")
print(f"Forma del tensor (shape): {list(C.shape)}")
print(f"Tipo de dato físico (dtype): {C.dtype}")
print(f"Dispositivo asignado (device): {C.device}")
print(f"Matriz resultante:\n{C.tolist()}")
```

**Salida real:**

```text
Tipo de objeto: Tensor
Forma del tensor (shape): [2, 2]
Tipo de dato físico (dtype): torch.float32
Dispositivo asignado (device): cpu
Matriz resultante:
[[19.0, 22.0], [43.0, 50.0]]
```

### Intermedio

Diferenciación automática con Autograd para optimizar una función cuadrática $f(x) = x^2 - 4x + 4$.

```python
import torch

# Variable entrenable con seguimiento de gradiente activado
x = torch.tensor([5.0], requires_grad=True)

# Evaluación de la función
y = x**2 - 4*x + 4

# Cálculo automático de la derivada dy/dx mediante backpropagation
y.backward()

print(f"Valor de f(5.0): {float(y.item()):.2f}")
print(f"Derivada evaluada f'(5.0) = 2x - 4: {float(x.grad.item()):.2f}")
```

**Salida real:**

```text
Valor de f(5.0): 9.00
Derivada evaluada f'(5.0) = 2x - 4: 6.00
```

### Avanzado

Entrenamiento completo de un regresor lineal utilizando `nn.Module`, `optim.Adam` y control de gradientes.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Modelo de regresión lineal como nn.Module
class RegresorSimple(nn.Module):
    def __init__(self):
        super().__init__()
        self.lineal = nn.Linear(1, 1)

    def forward(self, x):
        return self.lineal(x)

# Datos sintéticos: y = 3x + 2
X = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
y = torch.tensor([[5.0], [8.0], [11.0], [14.0]])

torch.manual_seed(42)
red = RegresorSimple()
criterio = nn.MSELoss()
opt = optim.Adam(red.parameters(), lr=0.1)

# Bucle de optimización de 100 épocas
for epoca in range(100):
    opt.zero_grad()
    salida = red(X)
    loss = criterio(salida, y)
    loss.backward()
    opt.step()

# Evaluación con inference_mode para no consumir memoria de gradientes
with torch.inference_mode():
    pred = red(torch.tensor([[5.0]]))
    print(f"Predicción para x=5.0: {float(pred.item()):.2f}")
    print(f"Pérdida final alcanzada: {float(loss.item()):.4f}")
```

**Salida real:**

```text
Predicción para x=5.0: 16.79
Pérdida final alcanzada: 0.0528
```

## 6. Aplicaciones en el mundo real

- **Modelos de Lenguaje Grande (LLMs) y Procesamiento de Lenguaje Natural (NLP):** Arquitecturas Transformer como LLaMA, GPT o BERT están entrenadas y optimizadas nativamente sobre PyTorch.
- **Visión por Computadora (Computer Vision):** Modelos de detección de objetos en tiempo real (YOLO), segmentación médica y redes generativas (Diffusion Models).
- **Vehículos Autónomos y Robótica:** Inferencia de control en tiempo real sobre hardware embebido con optimizaciones `torch.compile` y TensorRT.

## 7. Uso en producción

- **torch.compile (PyTorch 2.0+):** En producción, compilar el modelo con `modelo_compilado = torch.compile(modelo)` fusiona kernels CUDA a bajo nivel, acelerando la inferencia entre un 30% y un 100% sin modificar código.
- **Modo Inferencia Explicito:** En servidores de producción (FastAPI, TorchServe), envolver SIEMPRE la inferencia en `with torch.inference_mode():`. Esto desactiva el rastreo de autograd, reduciendo drásticamente el consumo de memoria VRAM y la latencia.
- **Exportación a ONNX y TorchScript:** Para despliegue en entornos no Python (C++, iOS, Android), serializar modelos a formato ONNX (`torch.onnx.export`) o TorchScript (`torch.jit.trace`).

## 8. Errores comunes y recomendaciones

- **Olvidar `optimizer.zero_grad()`:** En PyTorch, los gradientes se ACUMULAN por defecto (`+=`). Si no se llama `zero_grad()` en cada iteración del bucle, los gradientes de batches anteriores se sumarán, provocando que los pesos diverjan o exploten numéricamente.
- **No poner el modelo en `eval()`:** Olvidar `modelo.eval()` durante la prueba o inferencia mantiene capas como `Dropout` y `BatchNorm` activadas en modo estocástico, produciendo predicciones erráticas e inconsistentes.
- **Mezclar tensores de CPU y GPU:** Operar un tensor que reside en CPU con uno en GPU arroja de inmediato un `RuntimeError: Expected all tensors to be on the same device`.

## 9. Resumen

PyTorch combina la agilidad del código nativo de Python con la potencia de la computación masiva en GPU y la diferenciación automática exacta. Dominar la mecánica de tensores, el ciclo de vida de `autograd` y la abstracción declarativa de `nn.Module` permite transicionar con solvencia técnica desde prototipos científicos hasta sistemas de Deep Learning desplegados en clústeres de producción.

## 10. Referencias oficiales

- Documentación oficial de PyTorch: https://pytorch.org/docs/stable/index.html
- Tutoriales oficiales de PyTorch: https://pytorch.org/tutorials/
- Referencia de la API de tensores de PyTorch: https://pytorch.org/docs/stable/tensors.html
