# `DataFrame.apply` y `Series.apply`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.apply(
    func,
    axis=0,
    raw=False,
    result_type=None,
    args=(),
    by_row='compat',
    **kwargs
)
```

## 2. ¿Qué es?

Es un **método de aplicación funcional** que ejecuta una función personalizada a lo largo de un eje del DataFrame (a cada columna con `axis=0`, o a cada fila con `axis=1`).

## 3. ¿Para qué sirve?

Permite aplicar lógica procedural compleja o cálculos arbitrarios que combinan múltiples columnas simultáneamente cuando no existe una alternativa vectorizada directa.

## 4. ¿Cómo funciona?

1. **Iteración interna en Python:** `apply` es fundamentalmente un bucle `for` optimizado internamente. **No es una operación vectorizada compilada en C**, por lo que tiene un sobrecosto notable frente a operadores nativos.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `func` | `callable` | Obligatorio | Posicional | Función a aplicar a cada fila o columna. |
| `axis` | `{0, 1}` | Opcional | `0` | `0` aplica a cada columna (como Serie); `1` aplica a cada fila (como Serie). |
| `raw` | `bool` | Opcional | `False` | Si es `True`, pasa arreglos `ndarray` de NumPy en lugar de Series (mucho más rápido). |

## 6. Retorno

* `pandas.Series` o `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Aplicación a nivel de columnas (`axis=0`):

```python
import pandas as pd

df = pd.DataFrame({"goles": [25, 31, 28], "asistencias": [15, 8, 12]})
rango = df.apply(lambda col: col.max() - col.min(), axis=0)
print(rango)
```

**Salida real:**

```text
goles          6
asistencias    7
dtype: int64
```

---

### Nivel 2: Intermedio

Cálculo por fila combinando múltiples columnas (`axis=1`):

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Messi", "Haaland"],
    "goles": [25, 31],
    "partidos": [28, 30]
})

def calcular_promedio(fila):
    return round(fila["goles"] / fila["partidos"], 2)

df["promedio_gol"] = df.apply(calcular_promedio, axis=1)
print(df)
```

**Salida real:**

```text
   jugador  goles  partidos  promedio_gol
0    Messi     25        28          0.89
1  Haaland     31        30          1.03
```

---

### Nivel 3: Avanzado

Contraste de rendimiento: `apply` frente a la alternativa nativa vectorizada:

```python
import pandas as pd

df = pd.DataFrame({"minutos": [2100, 2450], "goles": [21, 28]})

# Enfoque vectorizado (RECOMENDADO EN PRODUCCIÓN: 100x más rápido):
df["minutos_por_gol_vectorizado"] = (df["minutos"] / df["goles"]).round(1)

# Enfoque con apply (más lento):
df["minutos_por_gol_apply"] = df.apply(lambda f: round(f["minutos"] / f["goles"], 1), axis=1)

print(df[["minutos_por_gol_vectorizado", "minutos_por_gol_apply"]])
```

**Salida real:**

```text
   minutos_por_gol_vectorizado  minutos_por_gol_apply
0                        100.0                  100.0
1                         87.5                   87.5
```

## 8. Errores frecuentes y casos borde

1. Abuso de `axis=1` para operaciones aritméticas básicas (`df.apply(lambda r: r['a'] + r['b'], axis=1)`): Es un antipatrón masivo. Debe escribirse vectorizado: `df['a'] + df['b']`.

## 9. Buenas prácticas y rendimiento

* Usar `raw=True` si se utiliza `apply` para cálculos numéricos intensivos sin metadatos de índices.

## 10. Métodos relacionados

* [map](map.md) — Transformación celda por celda.
* [pipe](pipe.md) — Transformación de todo el DataFrame.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.apply](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) (Pandas 2.2).
