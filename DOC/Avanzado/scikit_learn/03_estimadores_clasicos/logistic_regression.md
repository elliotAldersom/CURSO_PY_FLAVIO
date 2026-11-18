# Scikit-learn: LogisticRegression

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.linear_model.LogisticRegression(penalty='l2', *, dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='lbfgs', max_iter=100, multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None)
```

## 2. ¿Qué es?

`LogisticRegression` es el clasificador lineal estándar para modelar probabilidades de clases categóricas mediante la función sigmoide logística.

## 3. ¿Para qué sirve?

Fundamental para tareas de clasificación binaria y multiclase (scoring de riesgo, diagnóstico clínico, detección de spam), proveyendo probabilidades calibradas e interpretabilidad analítica directa.

## 4. ¿Cómo funciona?

Aplica la función sigmoide $\sigma(z) = \frac{1}{1 + e^{-z}}$ sobre la combinación lineal $z = Xw + b$, optimizando la pérdida de entropía cruzada binaria (Log-Loss) mediante algoritmos cuasi-Newton como `lbfgs`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `C` | `float` | Opcional | `1.0` | Inverso de la fuerza de regularización (valores más chicos implican regularización más fuerte). |
| `penalty` | `'l1'`, `'l2'`, `'elasticnet'`, `None` | Opcional | `'l2'` | Norma de penalización para evitar sobreajuste. |
| `solver` | `'lbfgs'`, `'liblinear'`, `'saga'`, `'newton-cg'` | Opcional | `'lbfgs'` | Algoritmo numérico de optimización. |
| `class_weight` | `'balanced'`, `dict`, `None` | Opcional | `None` | Ponderación de pesos para clases desbalanceadas. |
| `max_iter` | `int` | Opcional | `100` | Número máximo de iteraciones de convergencia del solver. |

## 6. Retorno

`LogisticRegression`. Instancia del clasificador ajustado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = np.array([[1.0], [2.0], [8.0], [9.0]])
y = np.array([0, 0, 1, 1])

clf = LogisticRegression(random_state=42)
clf.fit(X, y)

pred = clf.predict(np.array([[7.0]]))
print(f"Clase predicha para x=7.0: {int(pred[0])}")
```

**Salida real:**

```text
Clase predicha para x=7.0: 1
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = np.array([[1.0], [2.0], [8.0], [9.0]])
y = np.array([0, 0, 1, 1])

clf = LogisticRegression(random_state=42)
clf.fit(X, y)

# Extracción de probabilidades calibradas continuas con predict_proba
probabilidades = clf.predict_proba(np.array([[5.0]]))
print(f"Probabilidad de pertenecer a clase 0: {float(probabilidades[0, 0]):.2f}")
print(f"Probabilidad de pertenecer a clase 1: {float(probabilidades[0, 1]):.2f}")
```

**Salida real:**

```text
Probabilidad de pertenecer a clase 0: 0.50
Probabilidad de pertenecer a clase 1: 0.50
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

# Manejo de desbalance extremo de clases con class_weight='balanced'
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # 80% clase 0, 20% clase 1

clf = LogisticRegression(class_weight="balanced", random_state=42)
clf.fit(X, y)

print(f"Clases registradas: {clf.classes_.tolist()}")
print(f"Pesos de clases calculados internamente con balanceo")
```

**Salida real:**

```text
Clases registradas: [0, 1]
Pesos de clases calculados internamente con balanceo
```

## 8. Errores frecuentes y casos borde

- **`ConvergenceWarning: lbfgs failed to converge`:** Ocurre cuando los datos no están escalados o `max_iter` es insuficiente. Solución: escalar siempre con `StandardScaler` e incrementar `max_iter=500`.
- **Separación perfecta de clases:** Si una variable separa las clases sin ningún error, los coeficientes tienden a infinito si no hay regularización activa (`C=np.inf`).

## 9. Buenas prácticas y rendimiento

- Escalar SIEMPRE las variables antes de entrenar Regresión Logística; la regularización L2 penaliza los pesos según la escala de los datos.
- Usar `class_weight='balanced'` siempre que la clase positiva sea minoritaria.

## 10. Métodos relacionados

- [linear_regression](linear_regression.md)
- [confusion_matrix](../04_metricas_evaluacion/confusion_matrix.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
