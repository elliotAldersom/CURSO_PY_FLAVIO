# `DataFrame.head`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.head(n=5)
```

## 2. ¿Qué es?

Es un **método de instancia** de `pandas.DataFrame` (y `pandas.Series`) que retorna las primeras `n` filas de la estructura tabular según su orden físico de almacenamiento.

## 3. ¿Para qué sirve?

Permite realizar un diagnóstico visual preliminar inmediato para verificar si los encabezados, tipos de datos y primeros registros fueron cargados correctamente tras la ingesta.

* **Equivalencia en SQL:** Equivale a la cláusula `SELECT * FROM tabla LIMIT n`.

## 4. ¿Cómo funciona?

1. **Slicing posicional:** Opera internamente mediante un corte de índice posicional `self.iloc[:n]`.
2. **Eficiencia en memoria:** En Pandas con *Copy-on-Write* (v2.x+), devuelve una vista referencial de sólo lectura de los primeros bloques de memoria sin duplicar los arreglos subyacentes.
3. **Manejo de valores negativos:** Si `n` es negativo (p. ej. `n = -2`), devuelve todas las filas del DataFrame **excepto** las últimas `abs(n)` filas.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `n` | `int` | Opcional | `5` | Número de filas a devolver. Admite valores negativos para excluir filas finales. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la variable declarada `n`. El **argumento** es el valor numérico pasado al llamarlo (por ejemplo `n=3`).

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `pandas.Series`).
* **Mutabilidad:** No muta el objeto original; devuelve un nuevo sub-DataFrame con las filas seleccionadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Visualización de las primeras 2 filas:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé", "Erling Haaland"],
    "goles": [25, 22, 28, 31]
})

print(df_liga.head(2))
```

**Salida real:**

```text
             jugador  goles
0       Lionel Messi     25
1  Cristiano Ronaldo     22
```

---

### Nivel 2: Intermedio

Exclusión de registros finales usando argumento negativo:

```python
import pandas as pd

df_plantilla = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Rodrygo", "Bellingham", "Valverde"],
    "minutos": [2100, 1950, 2400, 2600]
})

# Retorna todas las filas excepto la última (n = -1)
print(df_plantilla.head(-1))
```

**Salida real:**

```text
       jugador  minutos
0  Vinicius Jr     2100
1      Rodrygo     1950
2   Bellingham     2400
```

---

### Nivel 3: Avanzado

Auditoría defensiva al inicio de una función de ingesta:

```python
import pandas as pd

def validar_ingesta_primeros_registros(df: pd.DataFrame, n_filas: int = 3) -> pd.DataFrame:
    if df.empty:
        raise ValueError("El DataFrame ingresado está vacío.")
    muestra = df.head(n_filas)
    print(f"[AUDITORÍA] Diagnóstico de ingesta (primeras {len(muestra)} filas):")
    print(muestra)
    return df

df_partido = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Lamine Yamal"],
    "equipo": ["Barcelona", "Barcelona", "Barcelona"]
})

validar_ingesta_primeros_registros(df_partido, 2)
```

**Salida real:**

```text
[AUDITORÍA] Diagnóstico de ingesta (primeras 2 filas):
  jugador     equipo
0   Pedri  Barcelona
1    Gavi  Barcelona
```

## 8. Errores frecuentes y casos borde

1. **`n=0`:** No arroja error; retorna un DataFrame vacío preservando los nombres de columna y el índice.
2. **`n > len(df)`:** No falla; retorna la totalidad de las filas disponibles sin rellenar con nulos.

## 9. Buenas prácticas y rendimiento

* **Nunca usar bucles para inspeccionar:** `head()` está vectorizado a nivel de corte posicional $O(1)$.
* **Evitar imprimir todo el DataFrame:** En terminales o logs masivos, `df.head()` evita bloquear la salida con millones de líneas.

## 10. Métodos relacionados

* [tail](tail.md) — Inspecciona las últimas `n` filas del DataFrame.
* [sample](sample.md) — Extrae una muestra aleatoria en lugar de las primeras filas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.head](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html) (Pandas 2.2).
