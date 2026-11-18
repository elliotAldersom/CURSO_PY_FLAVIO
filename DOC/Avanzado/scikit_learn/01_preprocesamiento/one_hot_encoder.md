# Scikit-learn: OneHotEncoder

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.preprocessing.OneHotEncoder(*, categories='auto', drop=None, sparse_output=True, dtype=np.float64, handle_unknown='error', min_frequency=None, max_categories=None)
```

## 2. ¿Qué es?

`OneHotEncoder` codifica variables categóricas nominales en una matriz binaria dispersa o densa donde cada categoría única se representa mediante una columna booleana (0 o 1).

## 3. ¿Para qué sirve?

Permite alimentar algoritmos matemáticos que requieren exclusivamente entradas numéricas continuas sin imponer un orden jerárquico artificial (como ocurriría erróneamente con `LabelEncoder`).

## 4. ¿Cómo funciona?

Inspecciona los valores únicos de cada columna durante `fit()`. Durante `transform()`, mapea cada categoría a un vector unitario de ceros con un 1 en la posición correspondiente. Puede descartar la primera columna (`drop='first'`) para evitar multicolinealidad perfecta.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `categories` | `'auto'` o `list[list]` | Opcional | `'auto'` | Categorías esperadas por columna. |
| `drop` | `'first'`, `'if_binary'`, `None` | Opcional | `None` | Descarta una categoría por columna para modelos lineales. |
| `sparse_output` | `bool` | Opcional | `True` | Retorna matriz dispersa de SciPy si es `True`, o array NumPy denso si es `False`. |
| `handle_unknown` | `'error'`, `'ignore'`, `'infrequent_if_exist'` | Opcional | `'error'` | Qué hacer ante categorías inéditas durante `transform`. |

## 6. Retorno

`OneHotEncoder`. Instancia del transformador categórico.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sklearn.preprocessing import OneHotEncoder

datos = [["Perro"], ["Gato"], ["Perro"]]
enc = OneHotEncoder(sparse_output=False)
salida = enc.fit_transform(datos)

print(f"Categorías identificadas: {enc.categories_[0].tolist()}")
print(f"Matriz codificada: {salida.tolist()}")
```

**Salida real:**

```text
Categorías identificadas: ['Gato', 'Perro']
Matriz codificada: [[0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]
```

### Nivel 2: Intermedio

```python
from sklearn.preprocessing import OneHotEncoder

ciudades_train = [["Madrid"], ["Bogota"], ["Lima"]]
ciudades_test = [["Bogota"], ["Tokio"]]  # Tokio no existía en train

# handle_unknown='ignore' previene excepciones en producción llenando con ceros
enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
enc.fit(ciudades_train)
salida_test = enc.transform(ciudades_test)

print(f"Test transformado (Tokio con ceros): {salida_test.tolist()}")
```

**Salida real:**

```text
Test transformado (Tokio con ceros): [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
```

### Nivel 3: Avanzado

```python
from sklearn.preprocessing import OneHotEncoder

# Prevención de la trampa de variables ficticias (dummy variable trap)
datos = [["Hombre"], ["Mujer"], ["Hombre"]]
enc = OneHotEncoder(drop="first", sparse_output=False)
salida = enc.fit_transform(datos)

print(f"Nombres de columnas generadas: {enc.get_feature_names_out().tolist()}")
print(f"Salida con 1 columna descartada: {salida.tolist()}")
```

**Salida real:**

```text
Nombres de columnas generadas: ['x0_Mujer']
Salida con 1 columna descartada: [[0.0], [1.0], [0.0]]
```

## 8. Errores frecuentes y casos borde

- **Fallo por categorías inéditas en producción:** Si un usuario introduce una nueva categoría no vista en train, `handle_unknown='error'` arroja una excepción fatal. En APIs de producción, configurar `handle_unknown='ignore'`.
- **Explosión dimensional:** Aplicar One-Hot Encoding a columnas con 10,000 valores únicos (ej. códigos postales) satura la memoria. En alta cardinalidad, usar `TargetEncoder` o agrupamiento por frecuencia.

## 9. Buenas prácticas y rendimiento

- Usar `drop='first'` en modelos lineales para evitar colinealidad perfecta; en modelos basados en árboles (Random Forest), mantener `drop=None`.
- Consultar los nombres de las columnas resultantes mediante `enc.get_feature_names_out()`.

## 10. Métodos relacionados

- [standard_scaler](standard_scaler.md)
- [column_transformer](../05_pipelines/column_transformer.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
