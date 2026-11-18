# PyTorch: Tensor.backward y Propagación hacia Atrás

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
Tensor.backward(gradient=None, retain_graph=None, create_graph=False, inputs=None)
```

## 2. ¿Qué es?

`backward()` es el método principal que dispara la propagación hacia atrás (Backpropagation), computando automáticamente la derivada de la variable escalar respecto a todas las hojas del grafo con `requires_grad=True`.

## 3. ¿Para qué sirve?

Resuelve el cálculo exacto de gradientes para optimizar redes neuronales profundas sin derivar manualmente expresiones matemáticas analíticas complejas.

## 4. ¿Cómo funciona?

Aplica la regla de la cadena multivariada en sentido inverso a través del grafo acíclico dirigido (DAG) de funciones registrado durante el forward pass. Almacena las derivadas calculadas en el atributo `.grad` de cada tensor hoja.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `gradient` | `Tensor` | Opcional | `None` | Vector de pesos externos si el tensor no es escalar (Jacobian-Vector product). |
| `retain_graph` | `bool` | Opcional | `None` | Si es `True`, conserva el grafo en memoria para llamadas subsiguientes a `backward()`. |
| `create_graph` | `bool` | Opcional | `False` | Si es `True`, construye un grafo de las derivadas para calcular derivadas de orden superior. |

## 6. Retorno

`None`. Muta los tensores hoja rellenando su atributo `.grad`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch

x = torch.tensor([3.0], requires_grad=True)
y = 2 * x**3

# dy/dx = 6 * x^2 -> en x=3: 6 * 9 = 54
y.backward()
print(f"Gradiente acumulado en x.grad: {float(x.grad.item()):.1f}")
```

**Salida real:**

```text
Gradiente acumulado en x.grad: 54.0
```

### Nivel 2: Intermedio

```python
import torch

w = torch.tensor([2.0], requires_grad=True)
b = torch.tensor([1.0], requires_grad=True)
x = torch.tensor([4.0])

# Modelo lineal simple: y = w*x + b
y = w * x + b
loss = (y - 12.0)**2  # y=9, (9-12)^2 = 9

loss.backward()
print(f"dLoss/dw: {float(w.grad.item()):.1f}")
print(f"dLoss/db: {float(b.grad.item()):.1f}")
```

**Salida real:**

```text
dLoss/dw: -24.0
dLoss/db: -6.0
```

### Nivel 3: Avanzado

```python
import torch

# backward() sobre tensor no escalar requiere argumento gradient
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x * 2

v = torch.tensor([1.0, 1.0])
y.backward(v)

print(f"Gradiente vectorial calculado: {x.grad.tolist()}")
```

**Salida real:**

```text
Gradiente vectorial calculado: [2.0, 2.0]
```

## 8. Errores frecuentes y casos borde

- **`RuntimeError: Trying to backward through the graph a second time`:** Por defecto PyTorch libera los buffers del grafo computacional tras el primer `backward()` para ahorrar memoria. Si se requiere llamar `backward()` nuevamente, pasar `retain_graph=True`.
- **Llamar `backward()` en tensor no escalar sin vector de gradiente:** `loss.backward()` falla si `loss` tiene más de 1 elemento a menos que se agregue con `.mean()` o `.sum()`.

## 9. Buenas prácticas y rendimiento

- Asegurarse de que la función de costo produzca un único valor escalar (ej. `loss = criterio(pred, y).mean()`) antes de llamar a `backward()`.
- No olvidar poner a cero los gradientes antes de cada iteración con `optimizer.zero_grad()`.

## 10. Métodos relacionados

- [grad](grad.md)
- [no_grad](no_grad.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/generated/torch.Tensor.backward.html
