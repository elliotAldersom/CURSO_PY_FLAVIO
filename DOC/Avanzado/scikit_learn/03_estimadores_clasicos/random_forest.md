# Scikit-learn: RandomForestClassifier

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.ensemble.RandomForestClassifier(n_estimators=100, *, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='sqrt', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None)
```

## 2. ¿Qué es?

`RandomForestClassifier` es un meta-estimador de ensamble que entrena múltiples árboles de decisión independientes sobre submuestras aleatorias (Bagging) y promedia sus votos para emitir la predicción final.

## 3. ¿Para qué sirve?

Es uno de los algoritmos más robustos y exitosos de la industria para datos tabulares: reduce drásticamente la varianza y el sobreajuste de los árboles individuales sin incrementar el sesgo.

## 4. ¿Cómo funciona?

Aplica dos fuentes de aleatoriedad: (1) Muestreo Bootstrap de filas para cada árbol y (2) Selección aleatoria de un subconjunto de características (`max_features='sqrt'`) en cada nodo de división. La predicción final es la moda mayoritaria de los árboles.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `n_estimators` | `int` | Opcional | `100` | Cantidad de árboles individuales a entrenar en el ensamble. |
| `max_depth` | `int` | Opcional | `None` | Profundidad máxima permitida para cada árbol individual. |
| `max_features` | `'sqrt'`, `'log2'`, `float`, `None` | Opcional | `'sqrt'` | Número de características evaluadas en cada división. |
| `bootstrap` | `bool` | Opcional | `True` | Si entrena cada árbol sobre muestras bootstrap con reemplazo. |
| `n_jobs` | `int` | Opcional | `None` | Núcleos de CPU para entrenamiento en paralelo (-1 usa todos). |
| `random_state` | `int` | Opcional | `None` | Semilla para garantizar reproducibilidad exacta. |

## 6. Retorno

`RandomForestClassifier`. Instancia del ensamble ajustado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

X = np.array([[1, 2], [2, 3], [8, 9], [9, 10]])
y = np.array([0, 0, 1, 1])

rf = RandomForestClassifier(n_estimators=10, random_state=42)
rf.fit(X, y)

pred = rf.predict(np.array([[5, 6]]))
print(f"Predicción del ensamble: {int(pred[0])}")
print(f"Cantidad de árboles internos: {len(rf.estimators_)}")
```

**Salida real:**

```text
Predicción del ensamble: 1
Cantidad de árboles internos: 10
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

X = np.array([[1, 100], [2, 105], [8, 500], [9, 520]])
y = np.array([0, 0, 1, 1])

rf = RandomForestClassifier(n_estimators=20, random_state=42)
rf.fit(X, y)

# Extracción de la importancia relativa de cada variable (Feature Importance)
importancias = rf.feature_importances_
print(f"Importancias normalizadas (suman 1): {[round(i, 2) for i in importancias.tolist()]}")
print(f"Suma total de importancias: {float(np.sum(importancias)):.1f}")
```

**Salida real:**

```text
Importancias normalizadas (suman 1): [0.49, 0.51]
Suma total de importancias: 1.0
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# oob_score=True evalúa el modelo sin necesidad de partición de validación externa
rf = RandomForestClassifier(n_estimators=50, oob_score=True, random_state=42)
rf.fit(X, y)

print(f"Puntuación Out-Of-Bag (OOB): {float(rf.oob_score_):.2f}")
```

**Salida real:**

```text
Puntuación Out-Of-Bag (OOB): 1.00
```

## 8. Errores frecuentes y casos borde

- **Consumo de memoria en inferencia:** Guardar ensambles con miles de árboles de profundidad ilimitada puede generar archivos `.joblib` de varios gigabytes. Controlar siempre con `n_estimators=100` y `max_depth=12`.
- **Extrapolación de tendencias:** Los modelos basados en árboles NO pueden extrapolar valores continuos fuera del rango de entrenamiento observado.

## 9. Buenas prácticas y rendimiento

- Usar `n_jobs=-1` para acelerar el entrenamiento distribuyendo árboles en todos los núcleos disponibles.
- Utilizar `rf.feature_importances_` para descartar variables irrelevantes en fases de reducción de dimensionalidad.

## 10. Métodos relacionados

- [decision_tree](decision_tree.md)
- [grid_search_cv](../02_particion_seleccion/grid_search_cv.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
