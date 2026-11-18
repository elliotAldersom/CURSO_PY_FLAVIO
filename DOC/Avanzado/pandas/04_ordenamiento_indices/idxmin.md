# `DataFrame.idxmin` y `Series.idxmin`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.idxmin(axis=0, skipna=True, numeric_only=False)
```

## 2. ¿Qué es?

Es un **método de búsqueda de índice extremo** que retorna la etiqueta del índice correspondiente al valor mínimo de una Serie o columna de DataFrame.

## 3. ¿Para qué sirve?

Identifica la clave de la fila con menor valor numérico (menor cantidad de faltas, menor tiempo de reacción, menor costo salarial).

## 4. ¿Cómo funciona?

1. **Búsqueda posicional C:** Localiza la posición del elemento mínimo con `argmin` y mapea la etiqueta del `Index`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | `0` busca por columna; `1` por fila. |
| `skipna` | `bool` | Opcional | `True` | Ignora valores nulos. |

## 6. Retorno

* Escalar o `pandas.Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

faltas = pd.Series([12, 4, 18], index=["Rudiger", "Kroos", "Carvajal"])
print("Jugador más limpio:", faltas.idxmin())
```

**Salida real:**

```text
Jugador más limpio: Kroos
```

---

### Nivel 2: Intermedio

Evaluación por fila (`axis=1`) para comparar métricas:

```python
import pandas as pd

df_tiempos = pd.DataFrame(
    {"carrera_1": [10.2, 10.5], "carrera_2": [9.9, 10.8]},
    index=["Atleta_A", "Atleta_B"]
)

print(df_tiempos.idxmin(axis=1))
```

**Salida real:**

```text
Atleta_A    carrera_2
Atleta_B    carrera_1
dtype: object
```

---

### Nivel 3: Avanzado

Aislamiento de mejor registro por posición en escuadra deportiva:

```python
import pandas as pd

df_porteros = pd.DataFrame({
    "jugador": ["Courtois", "Lunin", "Kepa"],
    "goles_concedidos_por_partido": [0.65, 0.80, 1.10]
})

idx_mejor = df_porteros["goles_concedidos_por_partido"].idxmin()
print("Portero más seguro del plantel:")
print(df_porteros.loc[idx_mejor, "jugador"])
```

**Salida real:**

```text
Portero más seguro del plantel:
Courtois
```

## 8. Errores frecuentes y casos borde

1. Series que contienen únicamente valores `NaN`: Devuelve `NaN` si `skipna=True`.

## 9. Buenas prácticas y rendimiento

* $O(N)$ en memoria sin copias adicionales.

## 10. Métodos relacionados

* [idxmax](idxmax.md) — Índice del valor máximo.
* [nsmallest](nsmallest.md) — Extracción de los $N$ menores.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.idxmin](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.idxmin.html) (Pandas 2.2).
