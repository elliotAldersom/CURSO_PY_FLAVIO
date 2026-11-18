# Scikit-learn: StandardScaler

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.preprocessing.StandardScaler(*, copy=True, with_mean=True, with_std=True)
```

## 2. ¿Qué es?

`StandardScaler` es un transformador que estandariza las características numéricas restando la media muestral y dividiendo por la desviación estándar, logrando que cada variable tenga media 0 y varianza unitaria.

## 3. ¿Para qué sirve?

Fundamental para algoritmos sensibles a la escala métrica de las variables, como Regresión Logística (regularizada con L1/L2), SVMs, K-Means y redes neuronales.

## 4. ¿Cómo funciona?

Calcula durante `fit(X)` los vectores de medias $\mu$ y desviaciones $\sigma$. Durante `transform(X)`, computa $z = (x - \mu) / \sigma$. Guarda los estadísticos aprendidos en los atributos `mean_` y `scale_`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `with_mean` | `bool` | Opcional | `True` | Si es `True`, centra los datos restando la media (incompatible con matrices sparse a menos que sea False). |
| `with_std` | `bool` | Opcional | `True` | Si es `True`, escala los datos a varianza unitaria. |
| `copy` | `bool` | Opcional | `True` | Si es `False`, realiza el escalado in-place sobre la matriz original. |

## 6. Retorno

`StandardScaler`. Instancia del transformador con estadísticos calculados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0, -1.0], [2.0, 0.0], [0.0, 1.0]])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Medias aprendidas: {scaler.mean_.tolist()}")
print(f"Medias del resultado escalado: {[round(m, 2) for m in X_scaled.mean(axis=0).tolist()]}")
```

**Salida real:**

```text
Medias aprendidas: [1.0, 0.0]
Medias del resultado escalado: [0.0, 0.0]
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X_train = np.array([[10.0], [20.0], [30.0]])
X_test = np.array([[15.0], [40.0]])

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
# Aplicación estricta de transform sobre test sin refittear
X_test_s = scaler.transform(X_test)

print(f"Desviación estándar de train: {float(scaler.scale_[0]):.2f}")
print(f"Test transformado con estadísticas de train: {[round(v[0], 2) for v in X_test_s.tolist()]}")
```

**Salida real:**

```text
Desviación estándar de train: 8.16
Test transformado con estadísticas de train: [-0.61, 2.45]
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

# Reversión de estandarización con inverse_transform
scaler = StandardScaler()
original = np.array([[500.0], [1000.0], [1500.0]])
escalado = scaler.fit_transform(original)
reconstruido = scaler.inverse_transform(escalado)

print(f"Reconstrucción idéntica: {np.allclose(original, reconstruido)}")
```

**Salida real:**

```text
Reconstrucción idéntica: True
```

## 8. Errores frecuentes y casos borde

- **Aplicar `fit` o `fit_transform` sobre datos de prueba:** Rompe la validez del modelo al introducir Data Leakage. Test debe transformarse ÚNICAMENTE con `transform()`.
- **Sensibilidad a Outliers extremos:** La presencia de valores atípicos severos distorsiona la media y comprime la varianza de los datos normales. En tales casos, preferir `RobustScaler`.

## 9. Buenas prácticas y rendimiento

- Integrar siempre el escalador dentro de un `Pipeline` para automatizar la aplicación de `fit` en train y `transform` en validación.
- No aplicar estandarización a columnas categóricas codificadas con One-Hot Encoding.

## 10. Métodos relacionados

- [one_hot_encoder](one_hot_encoder.md)
- [simple_imputer](simple_imputer.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
