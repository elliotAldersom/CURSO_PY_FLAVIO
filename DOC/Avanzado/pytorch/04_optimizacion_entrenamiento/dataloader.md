# PyTorch: Dataset y DataLoader

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.2.x)
torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=None, sampler=None, batch_sampler=None, num_workers=0, collate_fn=None, pin_memory=False, drop_last=False, timeout=0, worker_init_fn=None, multiprocessing_context=None, generator=None, *, prefetch_factor=None, persistent_workers=False, pin_memory_device='')
```

## 2. ¿Qué es?

`Dataset` y `DataLoader` son las abstracciones fundamentales para desacoplar el almacenamiento y lectura de datos del bucle de entrenamiento de la red.

## 3. ¿Para qué sirve?

Resuelven la ingesta eficiente de datos a gran escala: dividen en lotes (*mini-batches*), barajan aleatoriamente (*shuffling*), pre-cargan en paralelo usando múltiples núcleos de CPU y fijan memoria para transferencia ultrarrápida a GPU.

## 4. ¿Cómo funciona?

`Dataset` implementa `__len__()` y `__getitem__()` para indexación por muestra. `DataLoader` crea un iterador multiproceso que extrae muestras en lotes de tamaño `batch_size`, las ensambla con `collate_fn` y las entrega como tensores listos para cómputo.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `dataset` | `Dataset` | Obligatorio | N/A | Instancia que provee las muestras del conjunto de datos. |
| `batch_size` | `int` | Opcional | `1` | Cantidad de muestras agrupadas por cada lote. |
| `shuffle` | `bool` | Opcional | `False` | Si es `True`, baraja aleatoriamente los índices en cada época. |
| `num_workers` | `int` | Opcional | `0` | Cantidad de subprocesos paralelos para carga de datos en CPU. |
| `pin_memory` | `bool` | Opcional | `False` | Si es `True`, fija la memoria en RAM para transferencia PCIe directa a GPU. |
| `drop_last` | `bool` | Opcional | `False` | Descarta el último lote incompleto si el tamaño total no es múltiplo exacto de `batch_size`. |

## 6. Retorno

`DataLoader`. Iterador sobre lotes de datos empaquetados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import torch
from torch.utils.data import TensorDataset, DataLoader

# Creación de dataset a partir de tensores existentes
X = torch.arange(10).view(5, 2).float()
y = torch.tensor([0, 1, 0, 1, 0])

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=2, shuffle=False)

for batch_x, batch_y in loader:
    print(f"Batch X: {batch_x.tolist()} - Batch Y: {batch_y.tolist()}")
    break
```

**Salida real:**

```text
Batch X: [[0.0, 1.0], [2.0, 3.0]] - Batch Y: [0, 1]
```

### Nivel 2: Intermedio

```python
import torch
from torch.utils.data import Dataset, DataLoader

# Dataset personalizado para datos de negocio
class DatasetVentas(Dataset):
    def __init__(self, registros):
        self.datos = torch.tensor(registros, dtype=torch.float32)

    def __len__(self):
        return len(self.datos)

    def __getitem__(self, idx):
        return self.datos[idx]

ds = DatasetVentas([[100, 2], [150, 3], [200, 4]])
loader = DataLoader(ds, batch_size=2)
primer_lote = next(iter(loader))

print(f"Total registros: {len(ds)}")
print(f"Forma del lote extraído: {list(primer_lote.shape)}")
```

**Salida real:**

```text
Total registros: 3
Forma del lote extraído: [2, 2]
```

### Nivel 3: Avanzado

```python
import torch
from torch.utils.data import DataLoader, TensorDataset

X = torch.randn(10, 4)
y = torch.zeros(10)
loader = DataLoader(TensorDataset(X, y), batch_size=4, drop_last=True)

# 10 muestras con batch_size=4 y drop_last=True genera 2 lotes completos (descarta los últimos 2)
total_lotes = len(loader)
print(f"Total lotes completos procesados: {total_lotes}")
```

**Salida real:**

```text
Total lotes completos procesados: 2
```

## 8. Errores frecuentes y casos borde

- **`num_workers > 0` en entornos sin protección de `if __name__ == '__main__':`:** En Windows y sistemas basados en spawn, usar múltiples workers sin proteger el script principal causa un bucle infinito de creación de procesos.
- **Shuffle activo en validación/test:** El conjunto de prueba o validación no debe barajarse (`shuffle=False`) para garantizar evaluaciones deterministas comparables.

## 9. Buenas prácticas y rendimiento

- Usar `pin_memory=True` y `num_workers=4` cuando se entrena sobre GPU para evitar cuellos de botella en la transferencia PCIe.
- Activar `shuffle=True` estrictamente en el conjunto de entrenamiento para evitar sesgos por orden secuencial de datos.

## 10. Métodos relacionados

- [optimizer_step](optimizer_step.md)
- [loss_functions](loss_functions.md)

## 11. Referencias oficiales

- https://pytorch.org/docs/stable/data.html
