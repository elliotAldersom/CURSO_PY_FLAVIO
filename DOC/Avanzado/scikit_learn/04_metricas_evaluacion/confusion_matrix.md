# Scikit-learn: confusion_matrix

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.metrics.confusion_matrix(y_true, y_pred, *, labels=None, sample_weight=None, normalize=None)
```

## 2. ¿Qué es?

`confusion_matrix` evalúa la precisión de un clasificador construyendo una matriz cruzada donde las filas representan las clases reales y las columnas las clases predichas.

## 3. ¿Para qué sirve?

Permite desglosar el rendimiento más allá del accuracy global, identificando con precisión falsos positivos (error tipo I) y falsos negativos (error tipo II).

## 4. ¿Cómo funciona?

Tabula los pares `(y_true_i, y_pred_i)`. En problemas binarios, devuelve una matriz $2 \times 2$ estructurada como: `[[TN, FP], [FN, TP]]`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `y_true` | `ArrayLike` | Obligatorio | N/A | Vector con los valores verdaderos del conjunto de prueba. |
| `y_pred` | `ArrayLike` | Obligatorio | N/A | Vector con las etiquetas predichas por el estimador. |
| `labels` | `list` | Opcional | `None` | Lista de etiquetas para forzar el orden de indexación. |
| `normalize` | `'true'`, `'pred'`, `'all'`, `None` | Opcional | `None` | Normaliza las cuentas a proporciones sobre filas, columnas o total. |

## 6. Retorno

`numpy.ndarray`. Matriz bidimensional de confusión de tamaño $(n\_classes, n\_classes)$.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_true = [0, 0, 1, 1, 1]
y_pred = [0, 1, 0, 1, 1]

cm = confusion_matrix(y_true, y_pred)
print(f"Matriz de confusión:\n{cm}")
```

**Salida real:**

```text
Matriz de confusión:
[[1 1]
 [1 2]]
```

### Nivel 2: Intermedio

```python
from sklearn.metrics import confusion_matrix

y_real = [0, 0, 1, 1]
y_pred = [0, 1, 0, 1]

# Desempaquetado analítico canónico en clasificación binaria
tn, fp, fn, tp = confusion_matrix(y_real, y_pred).ravel()
print(f"Verdaderos Negativos (TN): {tn}")
print(f"Falsos Positivos (FP): {fp}")
print(f"Falsos Negativos (FN): {fn}")
print(f"Verdaderos Positivos (TP): {tp}")
```

**Salida real:**

```text
Verdaderos Negativos (TN): 1
Falsos Positivos (FP): 1
Falsos Negativos (FN): 1
Verdaderos Positivos (TP): 1
```

### Nivel 3: Avanzado

```python
from sklearn.metrics import confusion_matrix

y_real = [0, 0, 0, 1, 1, 1]
y_pred = [0, 0, 1, 1, 1, 1]

# Normalización por fila (normalize='true') para ver tasas de recall por clase
cm_norm = confusion_matrix(y_real, y_pred, normalize="true")
print(f"Tasa de acierto clase 0 (Especificidad): {float(cm_norm[0, 0]):.2f}")
print(f"Tasa de acierto clase 1 (Recall): {float(cm_norm[1, 1]):.2f}")
```

**Salida real:**

```text
Tasa de acierto clase 0 (Especificidad): 0.67
Tasa de acierto clase 1 (Recall): 1.00
```

## 8. Errores frecuentes y casos borde

- **Invertir el orden de argumentos:** Pasar `confusion_matrix(y_pred, y_true)` transpone la matriz, intercambiando falsos positivos con falsos negativos y viciando todo el diagnóstico. La regla fija es: **`y_true` primero, `y_pred` segundo**.
- **Confusión en la orientación:** En Scikit-learn, las filas son las clases REALES y las columnas las PREDICHAS.

## 9. Buenas prácticas y rendimiento

- Usar `.ravel()` para extraer limpiamente `tn, fp, fn, tp` en flujos de automatización binarios.
- Graficar la matriz resultante utilizando `ConfusionMatrixDisplay` o `sns.heatmap` para reportes técnicos claros.

## 10. Métodos relacionados

- [classification_report](classification_report.md)
- [logistic_regression](../03_estimadores_clasicos/logistic_regression.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
