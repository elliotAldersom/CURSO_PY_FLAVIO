# `DataFrame.nlargest` y `Series.nlargest`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.nlargest(n, columns, keep='first')
```

## 2. ¿Qué es?

Es un **método de selección optimizado** que devuelve las `n` filas con los mayores valores numéricos en una o varias columnas indicadas.

## 3. ¿Para qué sirve?

Obtiene rankings top (p. ej. los 5 máximos goleadores) de manera significativamente más rápida que ordenar el DataFrame completo con `sort_values().head(n)`.

* **Equivalencia en SQL:** `SELECT * FROM tabla ORDER BY col DESC LIMIT n`.

## 4. ¿Cómo funciona?

1. **Montículo binario (Min-Heap):** Utiliza internamente un algoritmo de montículo $O(N \log n)$, evitando el costo de un ordenamiento completo $O(N \log N)$ de toda la tabla.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `n` | `int` | Obligatorio | Posicional | Cantidad de filas superiores a extraer. |
| `columns` | `str`, `list[str]` | Obligatorio | Posicional | Columna(s) numéricas a evaluar. |
| `keep` | `{'first', 'last', 'all'}` | Opcional | `'first'` | Manejo de valores empatados. |

## 6. Retorno

* `pandas.DataFrame` (o `Series`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Haaland", "Kane", "Mbappé", "Lautaro"], "goles": [31, 36, 28, 27]})
print(df.nlargest(2, "goles"))
```

**Salida real:**

```text
   jugador  goles
1     Kane     36
0  Haaland     31
```

---

### Nivel 2: Intermedio

Desempate multicriterio evaluando goles y asistencias:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Palmer"],
    "goles": [21, 28, 21],
    "asistencias": [11, 8, 12]
})

print(df.nlargest(2, ["goles", "asistencias"]))
```

**Salida real:**

```text
       jugador  goles  asistencias
1       Mbappé     28            8
2       Palmer     21           12
```

---

### Nivel 3: Avanzado

Top N con preservación de todos los empates (`keep='all'`):

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Fermin"],
    "asistencias": [8, 8, 4]
})

# keep='all' devuelve todos los registros que comparten el valor de corte
print(df.nlargest(1, "asistencias", keep="all"))
```

**Salida real:**

```text
  jugador  asistencias
0   Pedri            8
1    Gavi            8
```

## 8. Errores frecuentes y casos borde

1. Columnas no numéricas: Lanza `TypeError: Column ... has invalid dtype`.

## 9. Buenas prácticas y rendimiento

* Si $n \ll N$ (ej. top 10 sobre 1.000.000 filas), `nlargest` es hasta 10 veces más rápido que `sort_values`.

## 10. Métodos relacionados

* [nsmallest](nsmallest.md) — Extracción de los $N$ menores valores.
* [sort_values](sort_values.md) — Reorganización completa.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.nlargest](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nlargest.html) (Pandas 2.2).
