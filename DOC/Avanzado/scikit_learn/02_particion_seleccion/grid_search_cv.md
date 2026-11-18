# Scikit-learn: GridSearchCV

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.model_selection.GridSearchCV(estimator, param_grid, *, scoring=None, n_jobs=None, refit=True, cv=None, verbose=0, pre_dispatch='2*n_jobs', error_score=np.nan, return_train_score=False)
```

## 2. ¿Qué es?

`GridSearchCV` es un optimizador exhaustivo de hiperparámetros que evalúa sistemáticamente todas las combinaciones posibles especificadas en una grilla mediante validación cruzada.

## 3. ¿Para qué sirve?

Automatiza la selección del mejor modelo predictivo optimizando una métrica de rendimiento objetivo sin intervención manual propensa a sesgos.

## 4. ¿Cómo funciona?

Construye el producto cartesiano de los parámetros dados en `param_grid`. Para cada combinación, entrena y evalúa el modelo a lo largo de $K$ particiones de cross-validation. Al finalizar, reentrena el mejor modelo sobre todo el conjunto si `refit=True`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `estimator` | `BaseEstimator` | Obligatorio | N/A | Modelo o Pipeline sobre el que optimizar parámetros. |
| `param_grid` | `dict[str, list]` | Obligatorio | N/A | Diccionario con listas de valores a explorar por parámetro. |
| `scoring` | `str` o `Callable` | Opcional | `None` | Métrica de evaluación (`'accuracy'`, `'f1'`, `'neg_mean_squared_error'`). |
| `n_jobs` | `int` | Opcional | `None` | Cantidad de núcleos de CPU para ejecución en paralelo (-1 usa todos). |
| `cv` | `int` | Opcional | `5` | Número de particiones de validación cruzada. |
| `refit` | `bool` | Opcional | `True` | Si es `True`, reentrena el mejor estimador sobre todo el dataset. |

## 6. Retorno

`GridSearchCV`. Instancia del estimador optimizado listo para inferencia directa.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

X = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([2.0, 4.0, 6.0, 8.0])

param_grid = {"alpha": [0.1, 1.0, 10.0]}
grid = GridSearchCV(Ridge(), param_grid, cv=2)
grid.fit(X, y)

print(f"Mejor parámetro encontrado: {grid.best_params_}")
print(f"Mejor score CV (R2): {float(grid.best_score_):.2f}")
```

**Salida real:**

```text
Mejor parámetro encontrado: {'alpha': 0.1}
Mejor score CV (R2): 0.99
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

X = np.array([[1, 2], [2, 3], [5, 6], [6, 7]])
y = np.array([0, 0, 1, 1])

# Exploración combinada de profundidad y criterio
grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid={"max_depth": [1, 2, 3], "criterion": ["gini", "entropy"]},
    cv=2,
    refit=True
)
grid.fit(X, y)

pred = grid.predict(np.array([[3, 4]]))
print(f"Predicción con el mejor estimador reentrenado: {int(pred[0])}")
```

**Salida real:**

```text
Predicción con el mejor estimador reentrenado: 0
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

X = np.array([[1], [2], [8], [9]])
y = np.array([0, 0, 1, 1])

grid = GridSearchCV(LogisticRegression(), {"C": [0.01, 1.0, 100.0]}, cv=2)
grid.fit(X, y)

# Inspección de la tabla completa de resultados
resultados = grid.cv_results_
print(f"Parámetros explorados en orden: {resultados['params']}")
```

**Salida real:**

```text
Parámetros explorados en orden: [{'C': 0.01}, {'C': 1.0}, {'C': 100.0}]
```

## 8. Errores frecuentes y casos borde

- **Explosión combinatoria (Maldición de la grilla):** Probar 5 parámetros con 5 valores cada uno en un modelo con $CV=5$ requiere entrenar $5^5 \times 5 = 15,625$ modelos, tardando horas o días. En espacios grandes, preferir `RandomizedSearchCV` o `HalvingGridSearchCV`.
- **Data Leakage al preprocesar fuera de `GridSearchCV`:** Si se escala la matriz antes del grid search, las particiones de validación cruzada sufren fuga de datos. La grilla debe envolver al `Pipeline` completo.

## 9. Buenas prácticas y rendimiento

- Usar `n_jobs=-1` para aprovechar todos los núcleos de CPU en paralelo.
- Envolverse siempre dentro de un `Pipeline` especificando los parámetros con la sintaxis de doble guion bajo: `paso__parametro` (ej. `'classifier__C': [0.1, 1.0]`).

## 10. Métodos relacionados

- [cross_val_score](cross_val_score.md)
- [train_test_split](train_test_split.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
