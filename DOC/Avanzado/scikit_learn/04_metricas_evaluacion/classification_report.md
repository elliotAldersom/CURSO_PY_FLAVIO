# Scikit-learn: classification_report

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.metrics.classification_report(y_true, y_pred, *, labels=None, target_names=None, sample_weight=None, digits=2, output_dict=False, zero_division='warn')
```

## 2. ¿Qué es?

`classification_report` construye un informe textual detallado con las principales métricas de evaluación de clasificación (Precision, Recall, F1-Score y Support) para cada clase individual y sus promedios macro y ponderados.

## 3. ¿Para qué sirve?

Resuelve el problema de evaluar modelos sobre datasets desbalanceados donde el `accuracy` global resulta engañoso e insuficiente para diagnosticar la calidad del modelo.

## 4. ¿Cómo funciona?

Computa para cada clase: Precision ($TP / (TP + FP)$), Recall ($TP / (TP + FN)$) y la media armónica F1 ($2 \times \frac{P \times R}{P + R}$). Calcula además el promedio macro (sin ponderar) y weighted (ponderado por el número de instancias de cada clase).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `y_true` | `ArrayLike` | Obligatorio | N/A | Etiquetas reales observadas. |
| `y_pred` | `ArrayLike` | Obligatorio | N/A | Etiquetas estimadas por el modelo. |
| `target_names` | `list[str]` | Opcional | `None` | Nombres semánticos legibles para cada clase. |
| `output_dict` | `bool` | Opcional | `False` | Si es `True`, retorna un diccionario de Python en lugar de una cadena formateada. |
| `zero_division` | `'warn'`, `0`, `1` | Opcional | `'warn'` | Valor a retornar ante divisiones por cero cuando una clase nunca fue predicha. |

## 6. Retorno

`str` o `dict`. Reporte formateado en tabla legible o diccionario con los valores numéricos.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sklearn.metrics import classification_report

y_true = [0, 1, 2, 2, 0]
y_pred = [0, 0, 2, 2, 0]

reporte = classification_report(y_true, y_pred)
print(reporte.strip())
```

**Salida real:**

```text
precision    recall  f1-score   support

           0       0.67      1.00      0.80         2
           1       0.00      0.00      0.00         1
           2       1.00      1.00      1.00         2

    accuracy                           0.80         5
   macro avg       0.56      0.67      0.60         5
weighted avg       0.67      0.80      0.72         5
```

### Nivel 2: Intermedio

```python
from sklearn.metrics import classification_report

y_true = [0, 1, 1, 0, 1]
y_pred = [0, 1, 1, 0, 0]

# Personalización con nombres explícitos y control de divisiones por cero
rep = classification_report(y_true, y_pred, target_names=["Negativo", "Positivo"], zero_division=0)
print(rep.strip())
```

**Salida real:**

```text
precision    recall  f1-score   support

    Negativo       0.67      1.00      0.80         2
    Positivo       1.00      0.67      0.80         3

    accuracy                           0.80         5
   macro avg       0.83      0.83      0.80         5
weighted avg       0.87      0.80      0.80         5
```

### Nivel 3: Avanzado

```python
from sklearn.metrics import classification_report

y_true = [0, 1, 0, 1]
y_pred = [0, 1, 0, 0]

# Retorno programático como diccionario para logging y monitoreo en MLflow
metricas = classification_report(y_true, y_pred, output_dict=True)
print(f"Accuracy global: {metricas['accuracy']:.2f}")
print(f"F1 macro average: {metricas['macro avg']['f1-score']:.2f}")
```

**Salida real:**

```text
Accuracy global: 0.75
F1 macro average: 0.73
```

## 8. Errores frecuentes y casos borde

- **Confundir Macro Avg con Weighted Avg:** En clases muy desbalanceadas, `macro avg` da el mismo peso a una clase de 10 muestras que a una de 10,000; `weighted avg` pondera por el soporte. Analizar siempre ambas.
- **`zero_division`:** Si el modelo nunca predice una clase, Precision divide por cero; usar `zero_division=0` en pipelines automatizados.

## 9. Buenas prácticas y rendimiento

- Usar `output_dict=True` cuando se integran métricas en dashboards o herramientas de observabilidad como Prometheus o MLflow.
- En detección de fraudes y enfermedades críticas, priorizar siempre el `Recall` de la clase positiva.

## 10. Métodos relacionados

- [confusion_matrix](confusion_matrix.md)
- [logistic_regression](../03_estimadores_clasicos/logistic_regression.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
