# Scikit-learn: mean_squared_error

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.metrics.mean_squared_error(y_true, y_pred, *, sample_weight=None, multioutput='uniform_average', squared='deprecated')
```

## 2. ¿Qué es?

`mean_squared_error` calcula el Error Cuadrático Medio (MSE) entre las observaciones continuas reales y las predicciones emitidas por un modelo de regresión.

## 3. ¿Para qué sirve?

Es la función de pérdida y métrica estándar para optimizar y evaluar modelos continuos, penalizando de forma cuadrática y severa los errores grandes respecto a los pequeños.

## 4. ¿Cómo funciona?

Computa el promedio aritmético de las diferencias al cuadrado: $MSE = \frac{1}{n}\sum_{i=1}^{n} (y_i - \hat{y}_i)^2$. A partir de Scikit-learn 1.4+, para calcular la raíz cuadrada (RMSE) se utiliza `root_mean_squared_error()`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `y_true` | `ArrayLike` | Obligatorio | N/A | Valores cuantitativos reales. |
| `y_pred` | `ArrayLike` | Obligatorio | N/A | Valores cuantitativos predichos. |
| `multioutput` | `'raw_values'`, `'uniform_average'` | Opcional | `'uniform_average'` | Ponderación en regresiones multidimensionales. |

## 6. Retorno

`float` o `numpy.ndarray`. Valor en punto flotante no negativo del error calculado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.metrics import mean_squared_error

y_true = [3.0, -0.5, 2.0, 7.0]
y_pred = [2.5, 0.0, 2.0, 8.0]

mse = mean_squared_error(y_true, y_pred)
print(f"Error Cuadrático Medio (MSE): {float(mse):.4f}")
```

**Salida real:**

```text
Error Cuadrático Medio (MSE): 0.3750
```

### Nivel 2: Intermedio

```python
import math
from sklearn.metrics import mean_squared_error

y_real = [100.0, 200.0, 300.0]
y_est = [110.0, 190.0, 310.0]

# Cálculo explícito de RMSE (Root Mean Squared Error) en las mismas unidades que Y
mse = mean_squared_error(y_real, y_est)
rmse = math.sqrt(mse)

print(f"MSE (unidades cuadradas): {float(mse):.1f}")
print(f"RMSE (unidades reales): {float(rmse):.2f}")
```

**Salida real:**

```text
MSE (unidades cuadradas): 100.0
RMSE (unidades reales): 10.00
```

### Nivel 3: Avanzado

```python
from sklearn.metrics import mean_squared_error

y_real = [10, 20, 30]
# Predicción con un error atípico extremo en el último elemento
y_est_normal = [12, 18, 32]  # Diferencias: 2, -2, 2
y_est_outlier = [10, 20, 40] # Diferencias: 0, 0, 10

print(f"MSE errores uniformes pequeños: {mean_squared_error(y_real, y_est_normal):.2f}")
print(f"MSE con un solo outlier: {mean_squared_error(y_real, y_est_outlier):.2f}")
```

**Salida real:**

```text
MSE errores uniformes pequeños: 4.00
MSE con un solo outlier: 33.33
```

## 8. Errores frecuentes y casos borde

- **Sensibilidad extrema a outliers:** Debido al término al cuadrado, un único error grande eleva drásticamente el MSE. Si se busca una métrica robusta ante valores atípicos, usar `mean_absolute_error` (MAE).
- **Parámetro `squared` en desuso:** En versiones modernas de Scikit-learn, el parámetro `squared=False` ha sido deprecado en favor de la función nativa `root_mean_squared_error`.

## 9. Buenas prácticas y rendimiento

- Reportar siempre el RMSE (o MAE) junto al $R^2$; el MSE está en unidades al cuadrado, dificultando la interpretación intuitiva de negocio.
- En modelos de optimización, el MSE es suave y diferenciable en todo punto, lo que lo hace ideal para algoritmos basados en gradiente.

## 10. Métodos relacionados

- [linear_regression](../03_estimadores_clasicos/linear_regression.md)
- [cross_val_score](../02_particion_seleccion/cross_val_score.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
