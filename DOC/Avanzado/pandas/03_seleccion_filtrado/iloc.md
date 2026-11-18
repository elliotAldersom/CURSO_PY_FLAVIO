# `DataFrame.iloc`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
# Indexador posicional entero
DataFrame.iloc[filas_posiciones, columnas_posiciones]
```

## 2. ¿Qué es?

Es un **indexador posicional** basado estrictamente en coordenadas enteras (`0` a `n - 1`), análogo al indexado clásico de matrices y listas en Python.

## 3. ¿Para qué sirve?

Permite acceder a filas y columnas conociendo su posición física sin importar cómo estén nombradas las etiquetas del índice o las columnas.

## 4. ¿Cómo funciona?

1. **Exclusión estándar de extremos:** Cumple con la semántica habitual de Python: `iloc[0:2]` toma los índices `0` y `1`, excluyendo el índice `2`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `filas_posiciones` | entero, lista de enteros, slice | Obligatorio | Posicional | Coordenadas enteras de filas (0 a $N-1$). |
| `columnas_posiciones` | entero, lista de enteros, slice | Opcional | Todas | Coordenadas enteras de columnas. |

## 6. Retorno

* Escalar, `Series` o `DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Haaland", "Kane"], "goles": [31, 36]})
# Primera fila, todas las columnas
print(df.iloc[0])
```

**Salida real:**

```text
jugador    Haaland
goles           31
Name: 0, dtype: object
```

---

### Nivel 2: Intermedio

Extracción de cuadrícula matricial con slices e índices negativos:

```python
import pandas as pd

df = pd.DataFrame({
    "col_0": [10, 20, 30],
    "col_1": [40, 50, 60],
    "col_2": [70, 80, 90]
})

# Filas 0 y 1, última columna
print(df.iloc[0:2, -1])
```

**Salida real:**

```text
0    70
1    80
Name: col_2, dtype: int64
```

---

### Nivel 3: Avanzado

División determinista de matrices de características y etiquetas para Machine Learning:

```python
import pandas as pd

df_dataset = pd.DataFrame({
    "minutos": [90, 85, 90],
    "kilometros": [11.2, 10.5, 12.0],
    "goles": [1, 0, 2]  # Target
})

# X: todas las columnas excepto la última; y: solo la última columna
X = df_dataset.iloc[:, :-1]
y = df_dataset.iloc[:, -1]

print("Matriz de características X:")
print(X)
print("\nVector objetivo y:")
print(y)
```

**Salida real:**

```text
Matriz de características X:
   minutos  kilometros
0       90        11.2
1       85        10.5
2       90        12.0

Vector objetivo y:
0    1
1    0
2    2
Name: goles, dtype: int64
```

## 8. Errores frecuentes y casos borde

1. Intentar pasar etiquetas de texto a `iloc`: Lanza `TypeError: Cannot index by location index with a non-integer key`.

## 9. Buenas prácticas y rendimiento

* Utilizar `iloc` para cortes posicionales de alto rendimiento en bucles científicos.

## 10. Métodos relacionados

* [loc](loc.md) — Indexación basada en etiquetas.
* [head](../02_inspeccion_exploracion/head.md) — Primeras filas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.iloc](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html) (Pandas 2.2).
