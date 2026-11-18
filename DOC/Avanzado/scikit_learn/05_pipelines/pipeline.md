# Scikit-learn: Pipeline

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.pipeline.Pipeline(steps, *, memory=None, verbose=False)
```

## 2. ¿Qué es?

`Pipeline` ensambla una secuencia de transformadores culminando en un estimador final, exponiendo una interfaz unificada que ejecuta todas las transformaciones de forma atómica.

## 3. ¿Para qué sirve?

Es el estándar supremo de arquitectura en Scikit-learn: previene de forma matemática la fuga de datos (*Data Leakage*), simplifica el código de inferencia y permite serializar el flujo completo en un único artefacto.

## 4. ¿Cómo funciona?

Al invocar `.fit(X, y)`, ejecuta recursivamente `.fit_transform()` en cada transformador intermedio pasando la salida al siguiente, y finalmente invoca `.fit()` sobre el estimador terminal. En `.predict(X)`, ejecuta exclusivamente `.transform()` en los pasos intermedios y `.predict()` al final.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `steps` | `list[tuple[str, BaseEstimator]]` | Obligatorio | N/A | Lista de tuplas `('nombre', transformador/estimador)`. |
| `memory` | `str` o `object` | Opcional | `None` | Ruta de directorio para almacenar en caché transformaciones intermedias (vía joblib). |
| `verbose` | `bool` | Opcional | `False` | Muestra el tiempo transcurrido por cada paso al ajustar. |

## 6. Retorno

`Pipeline`. Instancia compuesta que implementa `fit`, `predict` y `score`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X = np.array([[1.0], [2.0], [8.0], [9.0]])
y = np.array([0, 0, 1, 1])

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(random_state=42))
])

pipe.fit(X, y)
pred = pipe.predict(np.array([[7.5]]))

print(f"Pasos del pipeline: {[name for name, _ in pipe.steps]}")
print(f"Predicción atómica generada: {int(pred[0])}")
```

**Salida real:**

```text
Pasos del pipeline: ['scaler', 'classifier']
Predicción atómica generada: 1
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

X = np.array([[1.0], [np.nan], [3.0], [4.0]])
y = np.array([2.0, 4.0, 6.0, 8.0])

# make_pipeline asigna nombres automáticos en minúscula
pipe = make_pipeline(SimpleImputer(strategy="mean"), StandardScaler(), Ridge(alpha=1.0))
pipe.fit(X, y)

print(f"R2 score en evaluación: {float(pipe.score(X, y)):.2f}")
```

**Salida real:**

```text
R2 score en evaluación: 0.94
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

pipe = Pipeline([("scale", StandardScaler()), ("reg", Ridge())])

# Optimización conjunta con sintaxis paso__parametro
param_grid = {"reg__alpha": [0.1, 1.0, 10.0]}
grid = GridSearchCV(pipe, param_grid, cv=2)
grid.fit(X, y)

print(f"Mejor parámetro del pipeline: {grid.best_params_}")
```

**Salida real:**

```text
Mejor parámetro del pipeline: {'reg__alpha': 0.1}
```

## 8. Errores frecuentes y casos borde

- **Todos los pasos intermedios DEBEN ser transformadores:** Si un paso intermedio no implementa `.transform()`, lanzará un `TypeError`. Solo el último paso puede ser un predictor puro.
- **Fugas de datos por ajustar transformadores afuera:** Nunca hacer `scaler.fit(X)` fuera del pipeline; el pipeline garantiza que el escalado se ajuste solo sobre el pliegue de entrenamiento en cada split de CV.

## 9. Buenas prácticas y rendimiento

- Serializar el objeto `Pipeline` completo con `joblib.dump(pipe, 'pipeline.joblib')` para servir modelos en APIs sin preocuparse por replicar el preprocesamiento manualmente en producción.
- Usar `make_pipeline` para escribir flujos concisos sin declarar nombres de tuplas.

## 10. Métodos relacionados

- [column_transformer](column_transformer.md)
- [grid_search_cv](../02_particion_seleccion/grid_search_cv.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
