# Scikit-learn: DecisionTreeClassifier

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.tree.DecisionTreeClassifier(*, criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0)
```

## 2. ¿Qué es?

`DecisionTreeClassifier` es un modelo no paramétrico supervisado que particiona el espacio de características mediante reglas ortogonales recursivas de decisión jerárquica (árboles binarios).

## 3. ¿Para qué sirve?

Permite modelar relaciones no lineales complejas sin requerir escalado de datos, ofreciendo interpretabilidad visual total a través de reglas lógicas del tipo `IF-THEN`.

## 4. ¿Cómo funciona?

Aplica el algoritmo CART (Classification and Regression Trees), evaluando en cada nodo todas las divisiones binarias posibles y seleccionando aquella que maximiza la reducción de impureza de Gini o Entropía de Shannon.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `criterion` | `'gini'`, `'entropy'`, `'log_loss'` | Opcional | `'gini'` | Métrica para cuantificar la impureza de cada nodo. |
| `max_depth` | `int` | Opcional | `None` | Profundidad máxima del árbol (clave para controlar sobreajuste). |
| `min_samples_split` | `int` o `float` | Opcional | `2` | Cantidad mínima de muestras necesarias para dividir un nodo interno. |
| `min_samples_leaf` | `int` o `float` | Opcional | `1` | Cantidad mínima de muestras que debe contener cada hoja terminal. |
| `random_state` | `int` | Opcional | `None` | Semilla para garantizar reproducibilidad en empates de corte. |

## 6. Retorno

`DecisionTreeClassifier`. Instancia del estimador ajustado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier

X = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
y = np.array([0, 0, 1, 1])  # Función XOR no lineal

tree = DecisionTreeClassifier(random_state=42)
tree.fit(X, y)

print(f"Profundidad alcanzada: {tree.get_depth()}")
print(f"Hojas terminales: {tree.get_n_leaves()}")
print(f"Predicción exacta de XOR: {tree.predict(X).tolist()}")
```

**Salida real:**

```text
Profundidad alcanzada: 2
Hojas terminales: 4
Predicción exacta de XOR: [0, 0, 1, 1]
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier

X = np.array([[10], [20], [30], [40], [50]])
y = np.array([0, 0, 0, 1, 1])

# Poda previa (pre-pruning) para evitar sobreajuste
tree = DecisionTreeClassifier(max_depth=1, min_samples_leaf=2, random_state=42)
tree.fit(X, y)

print(f"Punto de corte aprendido en el nodo raíz: {float(tree.tree_.threshold[0]):.1f}")
```

**Salida real:**

```text
Punto de corte aprendido en el nodo raíz: 35.0
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

X = np.array([[25, 50000], [45, 120000], [35, 80000], [22, 25000]])
y = np.array([0, 1, 1, 0])

tree = DecisionTreeClassifier(max_depth=2, random_state=42)
tree.fit(X, y)

# Extracción de reglas de negocio en texto plano
reglas = export_text(tree, feature_names=["Edad", "Salario"])
print(f"Reglas generadas:\n{reglas.strip()}")
```

**Salida real:**

```text
Reglas generadas:
|--- Salario <= 65000.00
|   |--- class: 0
|--- Salario >  65000.00
|   |--- class: 1
```

## 8. Errores frecuentes y casos borde

- **Sobreajuste severo (Overfitting):** Con `max_depth=None`, el árbol crece hasta memorizar cada fila del dataset, generando hojas con 1 sola muestra y generalizando de forma pésima. Limitar siempre `max_depth`.
- **Inestabilidad por varianza:** Pequeñas variaciones en los datos de entrenamiento pueden alterar por completo toda la estructura del árbol. En producción, preferir ensambles (`RandomForestClassifier`).

## 9. Buenas prácticas y rendimiento

- Configurar siempre `max_depth` (ej. entre 3 y 8) y `min_samples_leaf` para forzar generalización.
- No es necesario escalar las variables con `StandardScaler`; los árboles son invariantes a transformaciones monótonas de escala.

## 10. Métodos relacionados

- [random_forest](random_forest.md)
- [classification_report](../04_metricas_evaluacion/classification_report.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
