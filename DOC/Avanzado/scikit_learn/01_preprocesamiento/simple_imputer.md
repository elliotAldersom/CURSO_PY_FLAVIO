# Scikit-learn: SimpleImputer

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.impute.SimpleImputer(*, missing_values=np.nan, strategy='mean', fill_value=None, copy=True, add_indicator=False, keep_empty_features=False)
```

## 2. ¿Qué es?

`SimpleImputer` es un transformador univariado que reemplaza valores faltantes (`NaN` o marcadores personalizados) utilizando estadísticas agregadas descriptivas.

## 3. ¿Para qué sirve?

Permite rescatar registros con datos incompletos sin tener que descartar filas completas (`dropna`), garantizando que la matriz final esté libre de valores nulos.

## 4. ¿Cómo funciona?

Calcula durante `fit()` el estadístico seleccionado (media, mediana o moda) a lo largo de cada columna. Durante `transform()`, localiza las posiciones de los nulos y asigna el valor precalculado.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `missing_values` | `int`, `float`, `str`, `np.nan`, `None` | Opcional | `np.nan` | Marcador que identifica el valor ausente. |
| `strategy` | `'mean'`, `'median'`, `'most_frequent'`, `'constant'` | Opcional | `'mean'` | Estrategia de sustitución estadística. |
| `fill_value` | `str` o `numerical` | Opcional | `None` | Valor constante a inyectar si `strategy='constant'`. |
| `add_indicator` | `bool` | Opcional | `False` | Si es `True`, agrega columnas binarias adicionales indicando dónde había un nulo. |

## 6. Retorno

`SimpleImputer`. Instancia del transformador de imputación.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[1.0, 2.0], [np.nan, 3.0], [7.0, 6.0]])
imp = SimpleImputer(strategy="mean")
X_imputed = imp.fit_transform(X)

print(f"Estadísticos calculados (medias): {imp.statistics_.tolist()}")
print(f"Matriz imputada: {X_imputed.tolist()}")
```

**Salida real:**

```text
Estadísticos calculados (medias): [4.0, 3.6666666666666665]
Matriz imputada: [[1.0, 2.0], [4.0, 3.0], [7.0, 6.0]]
```

### Nivel 2: Intermedio

```python
import numpy as np
from sklearn.impute import SimpleImputer

# Imputación de variables categóricas con la moda (most_frequent)
datos = np.array([["A"], ["B"], ["A"], [np.nan]], dtype=object)
imp = SimpleImputer(strategy="most_frequent")
resultado = imp.fit_transform(datos)

print(f"Moda aprendida: {imp.statistics_[0]}")
print(f"Resultado imputado: {[r[0] for r in resultado.tolist()]}")
```

**Salida real:**

```text
Moda aprendida: A
Resultado imputado: ['A', 'B', 'A', 'A']
```

### Nivel 3: Avanzado

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[10.0], [np.nan], [30.0]])
# add_indicator=True preserva la señal del patrón de ausencia
imp = SimpleImputer(strategy="median", add_indicator=True)
res = imp.fit_transform(X)

print(f"Matriz con indicador de ausencia: {res.tolist()}")
```

**Salida real:**

```text
Matriz con indicador de ausencia: [[10.0, 0.0], [20.0, 1.0], [30.0, 0.0]]
```

## 8. Errores frecuentes y casos borde

- **Imputar con la media en datos altamente asimétricos:** La presencia de outliers sesga drásticamente la media muestral, imputando valores irreales; usar `strategy='median'` en variables con colas pesadas.
- **Fuga de datos:** Ajustar el imputador con `fit` sobre todo el dataset antes de la partición de prueba contamina las medias.

## 9. Buenas prácticas y rendimiento

- Activar `add_indicator=True` cuando la ausencia de un dato no sea completamente aleatoria (Missing Not at Random), permitiendo al modelo aprender del patrón de fallo.
- Usar `strategy='most_frequent'` o `'constant'` para características categóricas.

## 10. Métodos relacionados

- [standard_scaler](standard_scaler.md)
- [column_transformer](../05_pipelines/column_transformer.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html
