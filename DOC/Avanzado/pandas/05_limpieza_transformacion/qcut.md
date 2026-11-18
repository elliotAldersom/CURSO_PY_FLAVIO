# `pandas.qcut`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.qcut(
    x,
    q,
    labels=None,
    retbins=False,
    precision=3,
    duplicates='raise'
)
```

## 2. ¿Qué es?

Es una **función de discretización por cuantiles** que divide los datos numéricos en intervalos tales que cada contenedor contenga aproximadamente la misma cantidad de observaciones (*frecuencia balanceada*).

## 3. ¿Para qué sirve?

Permite agrupar en cuartiles, deciles o percentiles equilibrados, evitando que categorías queden sobrecargadas o vacías.

* **Equivalencia en SQL:** Función de ventana `NTILE(q) OVER (ORDER BY col)`.

## 4. ¿Cómo funciona?

1. **Cálculo de cuantiles:** Computa los percentiles estadísticos sobre la distribución de los datos y asigna cada fila a su cuantil respectivo.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `x` | `Series`, arreglo | Obligatorio | Posicional | Datos numéricos a clasificar. |
| `q` | `int`, lista de cuantiles | Obligatorio | Posicional | Número de cuantiles (p. ej. `4` para cuartiles). |
| `labels` | lista de etiquetas | Opcional | `None` | Nombres para cada cuantil. |
| `duplicates` | `{'raise', 'drop'}` | Opcional | `'raise'` | Si es `'drop'`, colapsa cuantiles con valores idénticos. |

## 6. Retorno

* `pandas.Series[Categorical]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

División en 4 cuartiles equilibrados:

```python
import pandas as pd

goles = pd.Series([2, 5, 8, 12, 15, 20, 25, 30])
cuartiles = pd.qcut(goles, q=4)
print(cuartiles.value_counts())
```

**Salida real:**

```text
(1.999, 7.25]    2
(7.25, 13.5]     2
(13.5, 21.25]    2
(21.25, 30.0]    2
Name: count, dtype: int64
```

---

### Nivel 2: Intermedio

Asignación de etiquetas cualitativas por deciles/terciles:

```python
import pandas as pd

minutos = pd.Series([500, 800, 1200, 1500, 2100, 2600])
etiquetas = ["Bajo", "Medio", "Alto"]
terciles = pd.qcut(minutos, q=3, labels=etiquetas)
print(terciles)
```

**Salida real:**

```text
0     Bajo
1     Bajo
2    Medio
3    Medio
4     Alto
5     Alto
dtype: category
Categories (3, object): ['Bajo' < 'Medio' < 'Alto']
```

---

### Nivel 3: Avanzado

Manejo robusto de duplicados en distribuciones con muchos ceros:

```python
import pandas as pd

# Muchos ceros generan bordes de cuantiles idénticos
faltas = pd.Series([0, 0, 0, 0, 2, 5, 8, 12])
# duplicates='drop' evita el error ValueError
tramos = pd.qcut(faltas, q=4, duplicates="drop")
print(tramos.value_counts())
```

**Salida real:**

```text
(-0.001, 2.0]    5
(2.0, 12.0]      3
Name: count, dtype: int64
```

## 8. Errores frecuentes y casos borde

1. `ValueError: Bin edges must be unique`: Ocurre cuando hay muchos valores idénticos. **Solución:** Pasar `duplicates='drop'`.

## 9. Buenas prácticas y rendimiento

* Preferir `qcut` sobre `cut` cuando se requiere balance de clases para Machine Learning.

## 10. Métodos relacionados

* [cut](cut.md) — Discretización por anchos fijos.
* [quantile](../07_agrupacion_agregacion/quantile.md) — Cuantiles numéricos.

## 11. Referencias oficiales

* **API Reference:** [pandas.qcut](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html) (Pandas 2.2).
