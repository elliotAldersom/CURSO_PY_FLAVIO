# Scikit-learn: train_test_split

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.model_selection.train_test_split(*arrays, test_size=None, train_size=None, random_state=None, shuffle=True, stratify=None)
```

## 2. ¿Qué es?

`train_test_split` particiona aleatoriamente matrices o DataFrames en subconjuntos disjuntos de entrenamiento (train) y prueba (test).

## 3. ¿Para qué sirve?

Es la función fundamental de validación estadística para evaluar la capacidad de generalización de un modelo y prevenir el sobreajuste (overfitting).

## 4. ¿Cómo funciona?

Genera una permutación de índices aleatoria y divide las colecciones manteniendo la correspondencia biunívoca fila a fila. Si `stratify` se especifica, utiliza muestreo estratificado para garantizar idénticas proporciones de clases en ambos bloques.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `*arrays` | `Sequence[ArrayLike]` | Obligatorio | N/A | Matrices con idéntica primera dimensión (ej. `X, y`). |
| `test_size` | `float` o `int` | Opcional | `None` (0.25) | Proporción decimal (ej. 0.2) o conteo absoluto de filas de test. |
| `train_size` | `float` o `int` | Opcional | `None` | Proporción de filas de train (complementaria a `test_size`). |
| `random_state` | `int` | Opcional | `None` | Semilla del generador pseudoaleatorio para reproducibilidad. |
| `shuffle` | `bool` | Opcional | `True` | Si es `True`, mezcla los datos antes de dividir. |
| `stratify` | `ArrayLike` | Opcional | `None` | Vector objetivo para preservar las proporciones de clases. |

## 6. Retorno

`list`. Lista empaquetada con las particiones resultantes `[X_train, X_test, y_train, y_test]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.model_selection import train_test_split

X = np.arange(10).reshape((5, 2))
y = np.array([0, 1, 0, 1, 0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
print(f"Filas en X_train: {len(X_train)}")
print(f"Filas en X_test: {len(X_test)}")
```

**Salida real:**

```text
Filas en X_train: 3
Filas en X_test: 2
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.model_selection import train_test_split

# Datos fuertemente desbalanceados (90% clase 0, 10% clase 1)
y = np.array([0]*90 + [1]*10)
X = np.ones((100, 2))

# stratify=y garantiza que tanto train como test tengan exactamente 10% de clase 1
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print(f"Proporción de clase 1 en Train: {float(np.mean(y_tr)):.2f}")
print(f"Proporción de clase 1 en Test: {float(np.mean(y_te)):.2f}")
```

**Salida real:**

```text
Proporción de clase 1 en Train: 0.10
Proporción de clase 1 en Test: 0.10
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.model_selection import train_test_split

# Partición secuencial en series temporales (shuffle=False)
tiempo = np.arange(100)
senial = np.sin(tiempo)

t_tr, t_te, s_tr, s_te = train_test_split(tiempo, senial, test_size=0.2, shuffle=False)
print(f"Último índice de entrenamiento: {t_tr[-1]}")
print(f"Primer índice de prueba (estrictamente futuro): {t_te[0]}")
```

**Salida real:**

```text
Último índice de entrenamiento: 79
Primer índice de prueba (estrictamente futuro): 80
```

## 8. Errores frecuentes y casos borde

- **Hacer shuffle en datos temporales o de series de tiempo:** Mezclar aleatoriamente el orden temporal permite que el modelo use el futuro para predecir el pasado, destruyendo la validez experimental. Usar `shuffle=False` o `TimeSeriesSplit`.
- **Olvidar `stratify=y` en clasificación desbalanceada:** Puede ocasionar que el conjunto de prueba no reciba ningún ejemplo de la clase minoritaria.

## 9. Buenas prácticas y rendimiento

- Fijar siempre `random_state` en código de laboratorio e investigación para garantizar reproducibilidad exacta.
- Emplear proporciones estándar: 80/20 o 70/30 para datasets medianos, o 95/5 en conjuntos masivos con millones de registros.

## 10. Métodos relacionados

- [cross_val_score](cross_val_score.md)
- [grid_search_cv](grid_search_cv.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
