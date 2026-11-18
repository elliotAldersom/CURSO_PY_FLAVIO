# `DataFrame.diff` y `Series.diff`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.diff(periods=1, axis=0)
```

## 2. ¿Qué es?

Es un **método de cálculo de diferencias finitas** que resta cada elemento de la fila actual respecto al elemento situado `periods` posiciones antes.

## 3. ¿Para qué sirve?

Calcula variaciones incrementales o tasas de cambio discretas (p. ej. goles anotados respecto a la jornada anterior, aumento de puntos).

* **Equivalencia en SQL:** `columna - LAG(columna, periods) OVER (ORDER BY ...)`. 

## 4. ¿Cómo funciona?

1. Desplaza vectorialmente el arreglo en `periods` posiciones y ejecuta la resta elemento a elemento en memoria compilada.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `periods` | `int` | Opcional | `1` | Desfase temporal o posicional para la resta. |
| `axis` | `{0, 1}` | Opcional | `0` | Eje de diferenciación. |

## 6. Retorno

* `pandas.Series` o `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

puntos = pd.Series([10, 13, 14, 17])
print(puntos.diff().tolist())
```

**Salida real:**

```text
[nan, 3.0, 1.0, 3.0]
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

s = pd.Series([10, 15, 22])
print(s.diff(periods=-1).tolist())
```

**Salida real:**

```text
[-5.0, -7.0, nan]
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

df = pd.DataFrame({
    'jugador': ['Vinicius Jr', 'Vinicius Jr'],
    'km': [10.5, 22.0]
})
df['km_partido'] = df.groupby('jugador')['km'].diff().fillna(df['km'])
print(df)
```

**Salida real:**

```text
       jugador    km  km_partido
0  Vinicius Jr  10.5        10.5
1  Vinicius Jr  22.0        11.5
```

## 8. Errores frecuentes y casos borde

1. No ordenar previamente la serie temporal: Genera deltas incoherentes.

## 9. Buenas prácticas y rendimiento

* Asegurarse de ordenar por fecha antes de aplicar `diff()`.

## 10. Métodos relacionados

* `cumsum` — Operación inversa.
* `resample` — Remuestreo.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.diff` y `Series.diff`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.diff.html) (Pandas 2.2).
