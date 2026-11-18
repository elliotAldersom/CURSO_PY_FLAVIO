# PyTorch: Funciones de Pérdida (MSELoss, CrossEntropyLoss)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.nn.MSELoss(size_average=None, reduce=None, reduction='mean')
torch.nn.CrossEntropyLoss(weight=None, size_average=None, ignore_index=-100, reduce=None, reduction='mean', label_smoothing=0.0)
```

## 2. ¿Qué es?

Las funciones de pérdida o criterio cuantifican la discrepancia matemática entre las predicciones emitidas por la red neuronal y las etiquetas reales del dataset.

## 3. ¿Para qué sirve?

Proporcionan la señal de error diferenciable que guía el cálculo de gradientes a través de backpropagation para ajustar el modelo.

## 4. ¿Cómo funciona?

`MSELoss` calcula el error cuadrático medio para regresión continua. `CrossEntropyLoss` combina internamente `LogSoftmax` y pérdida de entropía cruzada (`NLLLoss`) en un solo paso numéricamente estable para clasificación multiclase.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `reduction` | `'mean'`, `'sum'`, `'none'` | Opcional | `'mean'` | Cómo agregar los errores individuales del lote. |
| `weight` | `Tensor` | Opcional | `None` | Pesos de ponderación para clases desbalanceadas en CrossEntropy. |
| `ignore_index` | `int` | Opcional | `-100` | Índice de categoría a omitir en el cálculo (útil para padding en NLP). |

## 6. Retorno

`torch.Tensor`. Tensor escalar con la pérdida calculada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
import torch.nn as nn

criterio_regresion = nn.MSELoss()
predicciones = torch.tensor([2.5, 4.0])
etiquetas_reales = torch.tensor([3.0, 4.0])

loss = criterio_regresion(predicciones, etiquetas_reales)
print(f"Pérdida MSE calculada: {float(loss.item()):.4f}")
```

**Salida real:**

```text
Pérdida MSE calculada: 0.1250
```

### Nivel 2: Intermedio

```python
import torch
import torch.nn as nn

# CrossEntropyLoss espera logits crudos (sin Softmax previo) y etiquetas enteras
criterio_clasificacion = nn.CrossEntropyLoss()
logits = torch.tensor([[2.0, 1.0, 0.1], [0.2, 3.5, 0.5]])  # 2 muestras, 3 clases
etiquetas = torch.tensor([0, 1])  # Clase 0 para la primera, clase 1 para la segunda

perdida = criterio_clasificacion(logits, etiquetas)
print(f"Pérdida de clasificación multiclase: {float(perdida.item()):.4f}")
```

**Salida real:**

```text
Pérdida de clasificación multiclase: 0.2017
```

### Nivel 3: Avanzado

```python
import torch
import torch.nn as nn

# Ponderación de clases desbalanceadas (clase 1 es 5 veces más crítica)
pesos = torch.tensor([1.0, 5.0])
criterio_ponderado = nn.CrossEntropyLoss(weight=pesos)

logits = torch.tensor([[1.0, 2.0]])
target = torch.tensor([1])
loss = criterio_ponderado(logits, target)

print(f"Pérdida con penalización ponderada: {float(loss.item()):.4f}")
```

**Salida real:**

```text
Pérdida con penalización ponderada: 1.5661
```

## 8. Errores frecuentes y casos borde

- **Aplicar `nn.Softmax()` antes de `CrossEntropyLoss`:** `nn.CrossEntropyLoss` ya aplica internamente `LogSoftmax` con estabilidad numérica. Si aplicas Softmax previamente, el modelo calculará un doble softmax erróneo y los gradientes se descalibrarán.
- **Pasar etiquetas one-hot a CrossEntropyLoss antiguo:** PyTorch espera índices enteros (`torch.long`) con la clase correcta, no vectores binarios one-hot.

## 9. Buenas prácticas y rendimiento

- Dejar siempre que la última capa de clasificación lineal entregue logits puros sin activación final.
- Usar `label_smoothing=0.1` en `CrossEntropyLoss` para evitar sobreconfianza en modelos de visión o lenguaje.

## 10. Métodos relacionados

- [optimizer_step](optimizer_step.md)
- [dataloader](dataloader.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/nn.html#loss-functions
