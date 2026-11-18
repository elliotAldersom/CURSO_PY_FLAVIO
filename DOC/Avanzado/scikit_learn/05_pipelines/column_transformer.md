# Scikit-learn: ColumnTransformer

```python
# NO EJECUTAR (Firma oficial de la API en versión 1.4.x)
sklearn.compose.ColumnTransformer(transformers, *, remainder='drop', sparse_threshold=0.3, n_jobs=None, transformer_weights=None, verbose=False, verbose_feature_names_out=True)
```

## 2. ¿Qué es?

`ColumnTransformer` aplica transformadores heterogéneos independientes sobre subconjuntos específicos de columnas en una matriz o DataFrame (ej. imputar y escalar columnas numéricas, mientras se codifica con One-Hot columnas de texto).

## 3. ¿Para qué sirve?

Resuelve el preprocesamiento de datasets del mundo real que combinan variables continuas y categóricas, unificando sus salidas en una única matriz resultante.

## 4. ¿Cómo funciona?

Ejecuta en paralelo cada tupla de transformador sobre las columnas asignadas, concatena horizontalmente los resultados (`np.hstack` o `scipy.sparse.hstack`) y descarta o preserva las columnas no seleccionadas según `remainder`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `transformers` | `list[tuple[str, Transformer, list[str | int]]]` | Obligatorio | N/A | Lista de tuplas: `('nombre', transformador, columnas)`. |
| `remainder` | `'drop'`, `'passthrough'`, `Transformer` | Opcional | `'drop'` | Qué hacer con las columnas no especificadas en la lista. |
| `sparse_threshold` | `float` | Opcional | `0.3` | Umbral para devolver matriz dispersa si contiene muchos ceros. |
| `verbose_feature_names_out` | `bool` | Opcional | `True` | Prefija el nombre del transformador en los nombres de salida. |

## 6. Retorno

`ColumnTransformer`. Instancia compuesta del transformador multicanal.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df = pd.DataFrame({
    "edad": [25.0, 35.0, 45.0],
    "pais": ["España", "Colombia", "España"]
})

ct = ColumnTransformer(transformers=[
    ("num", StandardScaler(), ["edad"]),
    ("cat", OneHotEncoder(sparse_output=False), ["pais"])
])

salida = ct.fit_transform(df)
print(f"Columnas transformadas shape: {salida.shape}")
print(f"Nombres generados: {ct.get_feature_names_out().tolist()}")
```

**Salida real:**

```text
Columnas transformadas shape: (3, 3)
Nombres generados: ['num__edad', 'cat__pais_Colombia', 'cat__pais_España']
```

### Nivel 2: Intermedio

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    "id": [101, 102, 103],
    "salario": [3000.0, 4500.0, 5000.0]
})

# remainder='passthrough' conserva la columna id sin alterarla
ct = ColumnTransformer(
    transformers=[("scale", StandardScaler(), ["salario"])],
    remainder="passthrough"
)
resultado = ct.fit_transform(df)
print(f"Salida preservando columnas restantes shape: {resultado.shape}")
```

**Salida real:**

```text
Salida preservando columnas restantes shape: (3, 2)
```

### Nivel 3: Avanzado

```python
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df = pd.DataFrame({
    "score": [1.5, 2.5, 3.5],
    "categoria": ["A", "B", "A"],
    "calificacion": [80.0, 90.0, 85.0]
})

# Selección automática por tipo de datos (dtypes)
ct = ColumnTransformer(transformers=[
    ("num", StandardScaler(), make_column_selector(dtype_include="float64")),
    ("cat", OneHotEncoder(sparse_output=False), make_column_selector(dtype_include="object"))
])
salida = ct.fit_transform(df)

print(f"Columnas detectadas automáticamente y transformadas: {salida.shape[1]}")
```

**Salida real:**

```text
Columnas detectadas automáticamente y transformadas: 4
```

## 8. Errores frecuentes y casos borde

- **Columnas no especificadas desaparecen:** Por defecto `remainder='drop'`. Si no se especifica explícitamente `remainder='passthrough'`, todas las columnas que no se incluyan en `transformers` serán eliminadas.
- **Error de nombres en Pandas:** Si se pasan nombres de columnas como strings pero se introduce un array de NumPy sin nombres en `transform()`, fallará. Usar índices numéricos o mantener siempre DataFrames.

## 9. Buenas prácticas y rendimiento

- Usar `make_column_selector(dtype_include=...)` para aplicar reglas universales por tipo de dato en lugar de listar manualmente cientos de nombres de columnas.
- Combinar `ColumnTransformer` como primer paso dentro de un `Pipeline` maestro.

## 10. Métodos relacionados

- [pipeline](pipeline.md)
- [one_hot_encoder](../01_preprocesamiento/one_hot_encoder.md)

## 11. Referencias oficiales

- https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html
