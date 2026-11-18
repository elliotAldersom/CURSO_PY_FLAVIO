# `DataFrame.nsmallest` y `Series.nsmallest`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.nsmallest(n, columns, keep='first')
```

## 2. ¿Qué es?

Es un **método de selección por montículo** que retorna las `n` filas con los valores numéricos más bajos en las columnas indicadas.

## 3. ¿Para qué sirve?

Permite identificar los registros mínimos (p. ej. atletas con menor tiempo de carrera, jugadores con menor cantidad de tarjetas o menor salario) sin costo de ordenación total.

* **Equivalencia en SQL:** `SELECT * FROM tabla ORDER BY col ASC LIMIT n`.

## 4. ¿Cómo funciona?

1. **Max-Heap subyacente:** Mantiene un montículo acotado de tamaño `n` con complejidad algorítmica $O(N \log n)$.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `n` | `int` | Obligatorio | Posicional | Cantidad de filas mínimas a obtener. |
| `columns` | `str`, `list[str]` | Obligatorio | Posicional | Columnas numéricas a evaluar. |
| `keep` | `{'first', 'last', 'all'}` | Opcional | `'first'` | Criterio de resolución de empates. |

## 6. Retorno

* `pandas.DataFrame` (o `Series`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Carvajal", "Rudiger", "Camavinga"], "faltas": [28, 35, 18]})
print(df.nsmallest(1, "faltas"))
```

**Salida real:**

```text
     jugador  faltas
2  Camavinga      18
```

---

### Nivel 2: Intermedio

Evaluación de menor cantidad de minutos con desempate:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Guler", "Endrick", "Ceballos"],
    "minutos": [450, 450, 300],
    "edad": [19, 18, 27]
})

print(df.nsmallest(2, ["minutos", "edad"]))
```

**Salida real:**

```text
    jugador  minutos  edad
2  Ceballos      300    27
1   Endrick      450    18
```

---

### Nivel 3: Avanzado

Pipeline de control de fatiga (jugadores con menor descanso):

```python
import pandas as pd

df_descanso = pd.DataFrame({
    "jugador": ["Valverde", "Bellingham", "Rodri", "Kroos"],
    "dias_descanso": [2, 3, 2, 6]
})

alerta_sobrecarga = df_descanso.nsmallest(2, "dias_descanso", keep="all")
print("Atletas en zona de riesgo de sobrecarga:")
print(alerta_sobrecarga)
```

**Salida real:**

```text
Atletas en zona de riesgo de sobrecarga:
    jugador  dias_descanso
0  Valverde              2
2     Rodri              2
```

## 8. Errores frecuentes y casos borde

1. Columnas con nulos: Los `NaN` se omiten automáticamente del montículo.

## 9. Buenas prácticas y rendimiento

* Preferir frente a `sort_values(ascending=True).head(n)`.

## 10. Métodos relacionados

* [nlargest](nlargest.md) — Mayores valores.
* [idxmin](idxmin.md) — Índice del valor mínimo único.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.nsmallest](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nsmallest.html) (Pandas 2.2).
