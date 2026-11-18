# `pandas.cut`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.cut(
    x,
    bins,
    right=True,
    labels=None,
    retbins=False,
    precision=3,
    include_lowest=False,
    duplicates='raise',
    ordered=True
)
```

## 2. ¿Qué es?

Es una **función de discretización uniforme** que segmenta y clasifica valores numéricos continuos en intervalos o contenedores discretos (*bins*) basados en rangos definidos o de ancho constante.

## 3. ¿Para qué sirve?

Convierte variables numéricas continuas (edad, salario, minutos) en variables categóricas ordenadas (p. ej. `['Joven', 'Adulto', 'Veterano']`).

* **Equivalencia en SQL:** `CASE WHEN edad < 21 THEN 'Joven' ... END`.

## 4. ¿Cómo funciona?

1. **Intervalos:** Divide la escala numérica en cortes cerrados por la derecha `(a, b]` por defecto (`right=True`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `x` | `Series`, arreglo | Obligatorio | Posicional | Arreglo numérico a discretizar. |
| `bins` | `int`, secuencia de escalares | Obligatorio | Posicional | Cantidad de tramos iguales o lista de puntos de corte exactos. |
| `labels` | `list[str]`, `False` | Opcional | `None` | Etiquetas categóricas para cada tramo. |

## 6. Retorno

* `pandas.Series[Categorical]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

edades = pd.Series([18, 24, 29, 35])
tramos = pd.cut(edades, bins=2)
print(tramos)
```

**Salida real:**

```text
0    (17.983, 26.5]
1    (17.983, 26.5]
2      (26.5, 35.0]
3      (26.5, 35.0]
dtype: category
Categories (2, interval[float64, right]): [(17.983, 26.5] < (26.5, 35.0]]
```

---

### Nivel 2: Intermedio

Discretización con cortes de negocio y etiquetas semánticas:

```python
import pandas as pd

minutos = pd.Series([450, 1200, 2400, 2800])
etiquetas = ["Baja Participación", "Rotación", "Titular Indiscutido"]
clasificacion = pd.cut(minutos, bins=[0, 1000, 2000, 3500], labels=etiquetas)
print(clasificacion)
```

**Salida real:**

```text
0     Baja Participación
1               Rotación
2    Titular Indiscutido
3    Titular Indiscutido
dtype: category
Categories (3, object): ['Baja Participación' < 'Rotación' < 'Titular Indiscutido']
```

---

### Nivel 3: Avanzado

Ingeniería de variables para segmentación de rendimiento de atletas:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Guler", "Bellingham", "Vinicius Jr"],
    "goles": [6, 19, 21]
})

df["nivel_goleador"] = pd.cut(
    df["goles"],
    bins=[-1, 10, 20, 50],
    labels=["Promesa", "Consagrado", "Bota de Oro"]
)
print(df)
```

**Salida real:**

```text
       jugador  goles nivel_goleador
0        Guler      6        Promesa
1   Bellingham     19     Consagrado
2  Vinicius Jr     21    Bota de Oro
```

## 8. Errores frecuentes y casos borde

1. Valores fuera del rango de `bins`: Se convierten automáticamente en `NaN`.

## 9. Buenas prácticas y rendimiento

* Utilizar `include_lowest=True` para no dejar fuera el valor mínimo.

## 10. Métodos relacionados

* [qcut](qcut.md) — Discretización basada en cuantiles con igual número de registros.

## 11. Referencias oficiales

* **API Reference:** [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html) (Pandas 2.2).
