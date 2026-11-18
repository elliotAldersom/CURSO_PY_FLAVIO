# `DataFrame.loc`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
# Indexador por etiquetas
DataFrame.loc[filas_etiquetas, columnas_etiquetas]
```

## 2. ¿Qué es?

Es un **indexador explícito por etiquetas** de `pandas.DataFrame` que permite seleccionar subconjuntos de filas y columnas basándose en sus nombres de índice o condiciones booleanas.

## 3. ¿Para qué sirve?

Resuelve de raíz la ambigüedad del acceso encadenado `df['col'][fila]`, garantizando accesos seguros en lectura y escritura sin advertencias de `SettingWithCopyWarning`.

* **Equivalencia en SQL:** Equivale a `SELECT col1, col2 WHERE condicion`.

## 4. ¿Cómo funciona?

1. **Inclusión estricta de extremos:** A diferencia del slicing posicional estándar de Python (`start:stop` excluye `stop`), **en `loc` el rango por etiquetas `inicio:fin` incluye ambos extremos**.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `filas_etiquetas` | etiqueta, lista, slice, booleanos | Obligatorio | Posicional | Etiquetas de filas a seleccionar. |
| `columnas_etiquetas` | etiqueta, lista, slice, booleanos | Opcional | Todas | Etiquetas de columnas a proyectar. |

## 6. Retorno

* Escalar (si se accede a una celda única), `Series` (una fila o columna) o `DataFrame` (múltiples filas y columnas).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame(
    {"goles": [25, 28], "asistencias": [15, 12]},
    index=["Messi", "Mbappé"]
)

print(df.loc["Messi", "goles"])
print("\nFila completa:")
print(df.loc["Mbappé"])
```

**Salida real:**

```text
25

Fila completa:
goles          28
asistencias    12
Name: Mbappé, dtype: int64
```

---

### Nivel 2: Intermedio

Slicing por etiquetas con inclusión de ambos extremos:

```python
import pandas as pd

df = pd.DataFrame(
    {"puntos": [95, 85, 81, 76]},
    index=["Real Madrid", "Barcelona", "Girona", "Atletico"]
)

# Ambos extremos incluidos
print(df.loc["Real Madrid":"Girona", ["puntos"]])
```

**Salida real:**

```text
             puntos
Real Madrid      95
Barcelona        85
Girona           81
```

---

### Nivel 3: Avanzado

Asignación segura en producción sobre subconjunto filtrado:

```python
import pandas as pd

df_salarios = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Guler", "Modric"],
    "categoria": ["Titular", "Suplente", "Veterano"],
    "bono": [0, 0, 0]
})

# Asignación segura con loc
df_salarios.loc[df_salarios["categoria"] == "Titular", "bono"] = 50000
print(df_salarios)
```

**Salida real:**

```text
       jugador categoria   bono
0  Vinicius Jr   Titular  50000
1        Guler  Suplente      0
2       Modric  Veterano      0
```

## 8. Errores frecuentes y casos borde

1. Intentar usar posiciones numéricas si el índice no es numérico: Lanza `KeyError`.

## 9. Buenas prácticas y rendimiento

* Usar siempre `loc` en lugar de indexación encadenada `df[filtro]['col'] = val`.

## 10. Métodos relacionados

* [iloc](iloc.md) — Indexación basada en posición entera.
* [query](query.md) — Selección condicional declarativa.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.loc](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html) (Pandas 2.2).
