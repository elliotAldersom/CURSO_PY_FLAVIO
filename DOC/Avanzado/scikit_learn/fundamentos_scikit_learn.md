# Fundamentos de Scikit-learn: Arquitectura de Estimadores y Machine Learning en Python

Scikit-learn es la biblioteca canónica de Python para aprendizaje automático clásico (Machine Learning supervisado y no supervisado), preprocesamiento y evaluación estadística.

## 2. Introducción

Originada en 2007 como un proyecto Google Summer of Code desarrollado por David Cournapeau y continuada por investigadores de INRIA (Francia), Scikit-learn democratizó la aplicación industrial de algoritmos de minería de datos y Machine Learning.

Su éxito universal radica en una arquitectura de software extraordinariamente coherente y minimalista: toda la biblioteca opera sobre contratos de interfaz uniformes (`fit`, `transform`, `predict`), interoperabilidad total con NumPy y SciPy, y una rigurosa separación entre fases de ajuste, inferencia y validación.

## 3. Fundamentos y conceptos

La arquitectura de Scikit-learn se estructura en cuatro contratos de interfaz de diseño:
1. **Estimadores (Estimators):** Cualquier objeto capaz de aprender patrones a partir de datos. Implementan el método `.fit(X, y=None)`. Todos los hiperparámetros se definen exclusivamente en el constructor `__init__`, nunca dentro de `fit`.
2. **Transformadores (Transformers):** Estimadores que transforman o filtran matrices de características (preprocesamiento, escalado, imputación, reducción de dimensionalidad). Implementan `.transform(X)` y el método optimizado `.fit_transform(X)`.
3. **Predictores (Predictors):** Estimadores capaces de realizar predicciones sobre nuevas observaciones no observadas. Implementan `.predict(X)` y, en clasificadores probabilísticos, `.predict_proba(X)`.
4. **Modelos Compuestos (Pipelines y ColumnTransformers):** Contenedores que encadenan secuencialmente múltiples transformadores culminando en un predictor final, previniendo fugas de información (*Data Leakage*).

## 4. Sintaxis y funcionamiento

El ciclo de vida canónico de cualquier flujo de Machine Learning con Scikit-learn consta de cinco pasos:
1. Partición de datos en entrenamiento y prueba (`train_test_split`).
2. Ajuste de transformadores con datos de entrenamiento (`scaler.fit(X_train)`).
3. Transformación de ambos conjuntos (`scaler.transform(X_train)`, `scaler.transform(X_test)`).
4. Ajuste del predictor (`model.fit(X_train_scaled, y_train)`).
5. Evaluación con métricas en el conjunto de prueba (`metrics.accuracy_score(y_test, y_pred)`).

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

# NO EJECUTAR (Estructura de referencia de flujo canónico)
X = np.array([[1.0, 2.0], [2.0, 3.0], [5.0, 6.0], [6.0, 7.0]])
y = np.array([0, 0, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

clf = LogisticRegression()
clf.fit(X_train_s, y_train)
preds = clf.predict(X_test_s)
acc = accuracy_score(y_test, preds)
```

## 5. Ejemplos prácticos progresivos

### Básico

Ajuste e inferencia con un estimador de regresión lineal simple sobre matrices de NumPy.

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Datos de entrada: matriz 2D para X, vector 1D para y
X = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([3.0, 5.0, 7.0, 9.0])  # y = 2x + 1

modelo = LinearRegression()
modelo.fit(X, y)

nuevos_puntos = np.array([[5.0], [6.0]])
predicciones = modelo.predict(nuevos_puntos)

print(f"Coeficiente angular (pendiente): {float(modelo.coef_[0]):.1f}")
print(f"Intercepto: {float(modelo.intercept_):.1f}")
print(f"Predicciones: {[round(p, 1) for p in predicciones.tolist()]}")
```

**Salida real:**

```text
Coeficiente angular (pendiente): 2.0
Intercepto: 1.0
Predicciones: [11.0, 13.0]
```

### Intermedio

Construcción de un clasificador supervisado con partición estratificada y matriz de confusión.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

X, y = make_classification(n_samples=100, n_features=4, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

rf = RandomForestClassifier(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"Forma matriz de confusión: {cm.shape}")
print(f"Precisión global de aciertos: {int(np.trace(cm))}/{len(y_test)}")
```

**Salida real:**

```text
Forma matriz de confusión: (2, 2)
Precisión global de aciertos: 28/30
```

### Avanzado

Encadenamiento de preprocesamiento, escalado y clasificador en un `Pipeline` con validación cruzada.

```python
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

X = np.array([[1, 2], [2, 3], [3, 4], [8, 9], [9, 10], [10, 11]])
y = np.array([0, 0, 0, 1, 1, 1])

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(random_state=42))
])

scores = cross_val_score(pipe, X, y, cv=2)
print(f"Puntajes CV por partición: {[round(s, 2) for s in scores.tolist()]}")
print(f"Rendimiento medio: {float(scores.mean()):.2f}")
```

**Salida real:**

```text
Puntajes CV por partición: [1.0, 1.0]
Rendimiento medio: 1.00
```

## 6. Aplicaciones en el mundo real

- **Sistemas de scoring crediticio:** Modelos de Regresión Logística y Random Forest para estimar la probabilidad de incumplimiento de pago (default) en entidades financieras.
- **Detección de fraude y anomalías:** Modelos de Isolation Forest o One-Class SVM sobre transacciones bancarias en tiempo real.
- **Segmentación de clientes:** Algoritmos de agrupamiento como K-Means sobre historiales de compra y navegación de usuarios en e-commerce.

## 7. Uso en producción

- **Data Leakage (Fuga de información):** Ajustar transformadores (`fit` o `fit_transform`) sobre el dataset completo antes de separar `train` y `test` contamina el conjunto de evaluación con información del futuro. La regla inquebrantable es: **`fit` solo en Train, `transform` en Test y Producción**.
- **Serialización segura:** Guardar modelos entrenados usando `joblib` (`joblib.dump(pipe, 'model.joblib')`). Advertencia: los archivos `.joblib` ejecutan código arbitrario al deserializarse; solo cargar modelos de fuentes confiables.
- **Persistencia de versiones:** Garantizar que la versión de Scikit-learn, NumPy y Python en el entorno de inferencia (FastAPI, Docker) sea exactamente idéntica a la del entorno de entrenamiento.

## 8. Errores comunes y recomendaciones

- **Llamar `fit_transform` sobre datos de prueba o producción:** Provoca que el modelo evalúe datos transformados con estadísticas diferentes a las aprendidas durante el entrenamiento.
- **Pasar vectores 1D a métodos que esperan matrices 2D:** Scikit-learn exige que la matriz de características $X$ sea bidimensional (`(n_samples, n_features)`). Si se tiene una sola característica, remodelar con `x.reshape(-1, 1)`.
- **No fijar `random_state`:** Ignorar `random_state` produce resultados no reproducibles entre ejecuciones experimentales.

## 9. Resumen

Scikit-learn establece el estándar industrial para Machine Learning tabular gracias a sus contratos `fit`, `transform` y `predict`. El empleo estricto de `Pipeline` asegura código modular, previene fugas de datos y facilita la serialización y despliegue continuo de modelos predictivos en arquitecturas de backend.

## 10. Referencias oficiales

- Documentación oficial de Scikit-learn: https://scikit-learn.org/stable/
- Guía de usuario (Scikit-learn User Guide): https://scikit-learn.org/stable/user_guide.html
- Glosario de términos y convenciones de la API: https://scikit-learn.org/stable/glossary.html
