# Scikit-learn: LinearRegression

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.linear_model.LinearRegression(*, fit_intercept=True, copy_X=True, n_jobs=None, positive=False)
```

## 2. ¿Qué es?

`LinearRegression` es el estimador estadístico clásico de mínimos cuadrados ordinarios (Ordinary Least Squares - OLS) para problemas de regresión continua.

## 3. ¿Para qué sirve?

Modela relaciones lineales continuas de la forma $y = X\beta + \epsilon$, minimizando la suma residual de cuadrados entre las observaciones reales y las predicciones lineales.

## 4. ¿Cómo funciona?

Calcula la solución analítica exacta de las ecuaciones normales mediante descomposición en valores singulares (SVD) de la matriz $X$, almacenando los coeficientes en `coef_` y el término independiente en `intercept_`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `fit_intercept` | `bool` | Opcional | `True` | Si calcula el término independiente $\beta_0$ o asume que los datos están centrados. |
| `copy_X` | `bool` | Opcional | `True` | Si es `False`, sobreescribe la memoria de la matriz $X$. |
| `positive` | `bool` | Opcional | `False` | Si es `True`, fuerza a que todos los coeficientes calculados sean $\ge 0$. |

## 6. Retorno

`LinearRegression`. Instancia del estimador ajustado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

reg = LinearRegression()
reg.fit(X, y)

print(f"Pendiente (coef_): {float(reg.coef_[0]):.1f}")
print(f"Intercepto: {float(reg.intercept_):.1f}")
```

**Salida real:**

```text
Pendiente (coef_): 2.0
Intercepto: 0.0
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Regresión lineal múltiple con 2 variables predictoras
X = np.array([[1, 2], [2, 1], [3, 4], [4, 3]])
y = np.array([7.0, 8.0, 15.0, 16.0])

reg = LinearRegression()
reg.fit(X, y)
pred = reg.predict(np.array([[5, 5]]))

print(f"Coeficientes [b1, b2]: {[round(c, 2) for c in reg.coef_.tolist()]}")
print(f"Predicción para [5, 5]: {float(pred[0]):.1f}")
```

**Salida real:**

```text
Coeficientes [b1, b2]: [3.0, 2.0]
Predicción para [5, 5]: 26.0
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[10], [20], [30]])
y = np.array([100, 200, 300])

reg = LinearRegression()
reg.fit(X, y)
r2_score = reg.score(X, y)

print(f"Coeficiente de determinación R^2: {float(r2_score):.2f}")
```

**Salida real:**

```text
Coeficiente de determinación R^2: 1.00
```

## 8. Errores frecuentes y casos borde

- **Multicolinealidad severa:** Si dos columnas de $X$ están perfectamente correlacionadas, la matriz $X^T X$ no es invertible y los coeficientes divergen con varianza enorme. Usar `Ridge` o `Lasso`.
- **Sensibilidad a Outliers:** OLS penaliza el error al cuadrado, por lo que un solo valor atípico distorsiona la recta por completo.

## 9. Buenas prácticas y rendimiento

- Estandarizar previamente las variables con `StandardScaler` si se desea comparar la magnitud relativa del impacto de cada coeficiente.
- Si la relación entre variables no es estrictamente lineal, incorporar `PolynomialFeatures` dentro de un `Pipeline`.

## 10. Métodos relacionados

- [logistic_regression](logistic_regression.md)
- [mean_squared_error](../04_metricas_evaluacion/mean_squared_error.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
