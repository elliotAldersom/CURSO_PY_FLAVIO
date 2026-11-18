# `DataFrame.tail`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.tail(n=5)
```

## 2. ¿Qué es?

Es un **método de instancia** de `pandas.DataFrame` (y `pandas.Series`) que extrae las últimas `n` filas del conjunto de datos.

## 3. ¿Para qué sirve?

Permite examinar el cierre del conjunto de datos para detectar filas de totales agregadas indebidamente al final del archivo, valores nulos terminales o validar el resultado tras operaciones de ordenamiento.

* **Equivalencia en SQL:** Equivale conceptualmente a `SELECT * FROM tabla ORDER BY id DESC LIMIT n`.

## 4. ¿Cómo funciona?

1. **Slicing negativo:** Equivale a `self.iloc[-n:]`.
2. **Argumentos negativos:** Si `n` es negativo, devuelve todas las filas desde la posición `abs(n)` hasta el final (excluyendo las primeras `abs(n)` filas).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `n` | `int` | Opcional | `5` | Cantidad de filas finales a retornar. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición formal `n`. El **argumento** es el entero suministrado (`n=3`).

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `pandas.Series`).
* **Mutabilidad:** Inmutable; genera un nuevo sub-DataFrame.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Visualización de las últimas 2 filas:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Courtois", "Rudiger", "Militao", "Carvajal"],
    "partidos": [10, 32, 28, 30]
})

print(df_liga.tail(2))
```

**Salida real:**

```text
    jugador  partidos
2   Militao        28
3  Carvajal        30
```

---

### Nivel 2: Intermedio

Omisión de las primeras filas con `n` negativo:

```python
import pandas as pd

df_tabla = pd.DataFrame({
    "equipo": ["Real Madrid", "Barcelona", "Girona", "Atletico Madrid"],
    "puntos": [95, 85, 81, 76]
})

# Excluye los primeros 2 equipos del inicio (n = -2)
print(df_tabla.tail(-2))
```

**Salida real:**

```text
            equipo  puntos
2           Girona      81
3  Atletico Madrid      76
```

---

### Nivel 3: Avanzado

Detección de filas de totales indebidas al final de un reporte contable/deportivo:

```python
import pandas as pd

df_reporte = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "TOTAL GENERAL"],
    "goles": [21, 28, 49]
})

# Detección defensiva de strings sospechosos en la última fila
ultima_fila = df_reporte.tail(1)
if ultima_fila["jugador"].str.contains("TOTAL").any():
    print("[ALERTA] Fila de total detectada al final. Se procede a sanear.")
    df_limpio = df_reporte.iloc[:-1]
    print(df_limpio)
```

**Salida real:**

```text
[ALERTA] Fila de total detectada al final. Se procede a sanear.
       jugador  goles
0  Vinicius Jr     21
1       Mbappé     28
```

## 8. Errores frecuentes y casos borde

1. **Preservación del índice original:** `tail()` mantiene los índices originales (p. ej. `[2, 3]`), no los resetea a `0`.

## 9. Buenas prácticas y rendimiento

* Utilizar `tail()` para verificar si un archivo CSV traía notas al pie o metadatos de cierre antes de ejecutar conversiones numéricas.

## 10. Métodos relacionados

* [head](head.md) — Inspecciona las primeras filas.
* [sample](sample.md) — Muestreo aleatorio.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.tail](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.tail.html) (Pandas 2.2).
