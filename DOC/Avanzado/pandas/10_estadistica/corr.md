# `DataFrame.corr` y `Series.corr`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.corr(
    method='pearson',
    min_periods=1,
    numeric_only=False
) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es un **método estadístico bivariado** que calcula la matriz de correlación par a par entre todas las columnas numéricas de un DataFrame.

## 3. ¿Para qué sirve?

Mide la fuerza y dirección de la relación lineal o monótona entre variables continuas (p. ej. relación entre minutos jugados y goles, o distancia recorrida y fatiga), sirviendo para selección de variables en Machine Learning.

* **Equivalencia en SQL:** Función analítica `CORR(col1, col2)`.

## 4. ¿Cómo funciona?

1. **Métodos paramétricos y no paramétricos:**
   * `'pearson'`: Coeficiente de correlación lineal estándar (sensible a outliers).
   * `'spearman'`: Correlación de rangos no paramétrica para relaciones monótonas no lineales.
   * `'kendall'`: Correlación basada en pares concordantes y discordantes, ideal para datasets pequeños o ordinales.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `method` | `{'pearson', 'kendall', 'spearman'}`, `callable` | Opcional | `'pearson'` | Algoritmo estadístico de correlación. |
| `min_periods` | `int` | Opcional | `1` | Cantidad mínima de observaciones válidas por par para no retornar `NaN`. |
| `numeric_only` | `bool` | Opcional | `False` | Si es `True`, calcula únicamente sobre tipos numéricos omitiendo strings. |

## 6. Retorno

* `pandas.DataFrame` (matriz simétrica cuadrada con diagonal principal igual a `1.0`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Matriz de correlación lineal directa de Pearson:

```python
import pandas as pd

df = pd.DataFrame({
    "minutos": [1200, 1800, 2400],
    "goles": [5, 15, 25],
    "tarjetas": [4, 2, 1]
})

print(df.corr().round(2))
```

**Salida real:**

```text
          minutos  goles  tarjetas
minutos      1.00   1.00     -0.98
goles        1.00   1.00     -0.98
tarjetas    -0.98  -0.98      1.00
```

---

### Nivel 2: Intermedio

Correlación de rangos de Spearman para relaciones no lineales:

```python
import pandas as pd

df = pd.DataFrame({
    "esfuerzo": [1, 2, 3, 4, 5],
    "fatiga_exponencial": [2, 4, 8, 16, 32]
})

# Spearman evalúa monotonicidad perfecta (= 1.0) aunque la relación no sea una recta
print("Pearson:", round(df.corr(method="pearson").iloc[0, 1], 2))
print("Spearman:", round(df.corr(method="spearman").iloc[0, 1], 2))
```

**Salida real:**

```text
Pearson: 0.94
Spearman: 1.0
```

---

### Nivel 3: Avanzado

Detección automática de multicolinealidad para preprocesamiento en ML:

```python
import numpy as np
import pandas as pd

df_metricas = pd.DataFrame({
    "goles": [25, 20, 15, 10],
    "remates": [100, 80, 60, 40],       # Altamente correlacionada con goles
    "recuperaciones": [10, 40, 50, 70]
})

matriz_corr = df_metricas.corr().abs()
# Seleccionamos el triángulo superior sin la diagonal
superior = matriz_corr.where(np.triu(np.ones(matriz_corr.shape), k=1).astype(bool))

# Detectamos columnas con correlación > 0.95
colineales = [col for col in superior.columns if any(superior[col] > 0.95)]
print("Variables redundantes a descartar para evitar multicolinealidad:", colineales)
```

**Salida real:**

```text
Variables redundantes a descartar para evitar multicolinealidad: ['remates']
```

## 8. Errores frecuentes y casos borde

1. Columnas constantes: Si una columna tiene siempre el mismo valor (varianza cero), la correlación con cualquier otra variable será matemáticamente indefinida (`NaN`).

## 9. Buenas prácticas y rendimiento

* Pasar `numeric_only=True` para evitar advertencias de tipos mixtos en tablas con texto.

## 10. Métodos relacionados

* [std](../07_agrupacion_agregacion/std.md) — Desviación estándar individual.
* [describe](../02_inspeccion_exploracion/describe.md) — Estadísticos generales.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.corr](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html) (Pandas 2.2).
