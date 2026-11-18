# `DataFrame.cumsum` y `Series.cumsum`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.cumsum(axis=None, skipna=True)
```

## 2. ¿Qué es?

Es un **método de agregación acumulativa** que calcula la suma acumulada de valores a lo largo de un eje.

## 3. ¿Para qué sirve?

Genera series cronológicas progresivas (p. ej. puntos acumulados en la temporada partido tras partido).

* **Equivalencia en SQL:** `SUM(col) OVER (ORDER BY fecha ROWS UNBOUNDED PRECEDING)`.

## 4. ¿Cómo funciona?

1. **Suma prefija vectorizada:** Ejecuta una suma prefija acumulada vectorizada en C, saltando nulos con `skipna=True`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | Eje de acumulación. |
| `skipna` | `bool` | Opcional | `True` | Omite valores faltantes. |

## 6. Retorno

* `pandas.Series` o `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles_por_partido = pd.Series([2, 1, 0, 3])
print(goles_por_partido.cumsum())
```

**Salida real:**

```text
0    2
1    3
2    3
3    6
dtype: int64
```

---

### Nivel 2: Intermedio

Acumulación cronológica agrupada por jugador con `groupby`:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Vinicius Jr", "Mbappé", "Mbappé"],
    "fecha": ["Fecha 1", "Fecha 2", "Fecha 1", "Fecha 2"],
    "goles": [1, 2, 2, 1]
})

df["goles_acumulados"] = df.groupby("jugador")["goles"].cumsum()
print(df)
```

**Salida real:**

```text
       jugador    fecha  goles  goles_acumulados
0  Vinicius Jr  Fecha 1      1                 1
1  Vinicius Jr  Fecha 2      2                 3
2       Mbappé  Fecha 1      2                 2
3       Mbappé  Fecha 2      1                 3
```

---

### Nivel 3: Avanzado

Evolución de puntos acumulados en la liga:

```python
import pandas as pd

df_puntos = pd.DataFrame({"partido": range(1, 4), "puntos_fecha": [3, 1, 3]})
df_puntos["tabla_acumulada"] = df_puntos["puntos_fecha"].cumsum()
print(df_puntos)
```

**Salida real:**

```text
   partido  puntos_fecha  tabla_acumulada
0        1             3                3
1        2             1                4
2        3             3                7
```

## 8. Errores frecuentes y casos borde

1. Calcular `cumsum` sin haber ordenado previamente por fecha: Genera una curva temporal incorrecta.

## 9. Buenas prácticas y rendimiento

* Ordenar siempre por tiempo antes de invocar `cumsum()`.

## 10. Métodos relacionados

* [sum](sum.md) — Suma escalar total.
* [diff](../08_fechas_series_tiempo/diff.md) — Diferenciación inversa.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.cumsum](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.cumsum.html) (Pandas 2.2).
