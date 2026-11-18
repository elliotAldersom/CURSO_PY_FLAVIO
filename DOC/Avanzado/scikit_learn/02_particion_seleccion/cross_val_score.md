# Scikit-learn: cross_val_score

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.model_selection.cross_val_score(estimator, X, y=None, *, groups=None, scoring=None, cv=None, n_jobs=None, verbose=0, fit_params=None, params=None, pre_dispatch='2*n_jobs')
```

## 2. ¿Qué es?

`cross_val_score` evalúa el rendimiento de un estimador dividiendo los datos en $K$ particiones mutuamente excluyentes (K-Fold Cross Validation), retornando un array con las puntuaciones métricas de cada iteración.

## 3. ¿Para qué sirve?

Provee una estimación insesgada y robusta del error de generalización, reduciendo la variabilidad inherente a una única partición fija de entrenamiento/prueba.

## 4. ¿Cómo funciona?

Itera $K$ veces: en cada ciclo reserva un pliegue como conjunto de prueba y entrena el estimador con los $K-1$ restantes, evaluando la métrica elegida (`scoring`) y calculando la media y varianza del desempeño.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `estimator` | `BaseEstimator` | Obligatorio | N/A | Modelo o Pipeline a evaluar. |
| `X` | `ArrayLike` | Obligatorio | N/A | Matriz de características. |
| `y` | `ArrayLike` | Opcional | `None` | Vector objetivo para modelos supervisados. |
| `scoring` | `str` o `Callable` | Opcional | `None` | Métrica de evaluación (`'accuracy'`, `'roc_auc'`, `'r2'`). |
| `cv` | `int` o `CrossValidator` | Opcional | `5` | Número de particiones (K-Folds). |
| `n_jobs` | `int` | Opcional | `None` | Procesos paralelos en CPU (-1 para todos). |

## 6. Retorno

`numpy.ndarray`. Array de números en punto flotante con las puntuaciones de cada pliegue.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y = np.array([2.0, 4.0, 6.0, 8.0, 10.0, 12.0])

scores = cross_val_score(LinearRegression(), X, y, cv=3)
print(f"Puntuaciones R2 por fold: {[round(s, 2) for s in scores.tolist()]}")
print(f"Rendimiento medio: {float(scores.mean()):.2f}")
```

**Salida real:**

```text
Puntuaciones R2 por fold: [1.0, 1.0, 1.0]
Rendimiento medio: 1.00
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = np.array([[1, 2], [2, 3], [3, 4], [8, 9], [9, 10], [10, 11]])
y = np.array([0, 0, 0, 1, 1, 1])

# Evaluación con métrica F1 explícita
scores = cross_val_score(RandomForestClassifier(n_estimators=5, random_state=42), X, y, cv=2, scoring="f1")
print(f"Puntuaciones F1 por fold: {[round(s, 2) for s in scores.tolist()]}")
```

**Salida real:**

```text
Puntuaciones F1 por fold: [1.0, 1.0]
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

X = np.array([[1], [2], [3], [10], [11], [12]])
y = np.array([0, 0, 0, 1, 1, 1])

# Validación cruzada rigurosa con Pipeline (StandardScaler fitteado en cada fold)
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
scores = cross_val_score(pipe, X, y, cv=3)

print(f"Media de precisión con escalado seguro: {float(scores.mean()):.2f}")
print(f"Desviación estándar de los folds: {float(scores.std()):.2f}")
```

**Salida real:**

```text
Media de precisión con escalado seguro: 1.00
Desviación estándar de los folds: 0.00
```

## 8. Errores frecuentes y casos borde

- **Métricas negativas en Scikit-learn:** Para funciones de costo o error (como MSE), Scikit-learn invierte el signo (`'neg_mean_squared_error'`) para que mayor siempre signifique mejor. Recordar multiplicar por $-1$ al reportar el error positivo.
- **`cross_val_score` no retorna el modelo entrenado:** Solo computa números estadísticos. Si se necesita el modelo para inferencia, se debe invocar `fit()` sobre los datos finales.

## 9. Buenas prácticas y rendimiento

- Reportar siempre la media Y la desviación estándar de la métrica (`media ± std`) para reflejar la estabilidad del modelo frente a diferentes particiones.
- En problemas de clasificación desbalanceada, usar `scoring='f1_macro'` o `'roc_auc'` en lugar del `accuracy` por defecto.

## 10. Métodos relacionados

- [train_test_split](train_test_split.md)
- [grid_search_cv](grid_search_cv.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html
