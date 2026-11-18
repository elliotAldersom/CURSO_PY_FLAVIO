# `DataFrame.isna` e `isnull`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.isna() -> pandas.DataFrame
DataFrame.isnull() -> pandas.DataFrame  # Alias idéntico
```

## 2. ¿Qué es?

Es un **método de diagnóstico booleano** que evalúa elemento por elemento si una celda contiene un valor nulo, faltante o no definido (`NaN`, `None`, `pd.NA`), retornando una máscara booleana de idéntica dimensión.

## 3. ¿Para qué sirve?

Constituye la base de la limpieza de datos para cuantificar la ausencia de información en auditorías y habilitar filtrados o imputaciones selectivas.

* **Equivalencia en SQL:** Equivale a la expresión `columna IS NULL`.

## 4. ¿Cómo funciona?

1. **Vectorización a nivel de C:** Evalúa las reglas de tipo flotante IEEE 754 (`val != val`) o tipos centinela de Pandas sin sobrecarga de bucles interpretados.

## 5. Parámetros

* No recibe parámetros obligatorios.

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `pandas.Series`) con valores booleanos (`True` si es nulo, `False` si es válido).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", None],
    "goles": [21, None]
})

print(df.isna())
```

**Salida real:**

```text
   jugador  goles
0    False  False
1     True   True
```

---

### Nivel 2: Intermedio

Conteo y porcentaje de valores nulos por columna:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Rodri", "Foden", "De Bruyne"],
    "asistencias": [8, None, 18],
    "lesion": [None, None, "Rodilla"]
})

print("Conteo absoluto de nulos:")
print(df.isna().sum())
print("\nPorcentaje de nulos:")
print((df.isna().mean() * 100).round(1))
```

**Salida real:**

```text
Conteo absoluto de nulos:
jugador        0
asistencias    1
lesion         2
dtype: int64

Porcentaje de nulos:
jugador         0.0
asistencias    33.3
lesion         66.7
dtype: float64
```

---

### Nivel 3: Avanzado

Filtrado defensivo para aislar registros que requieren imputación en ETL:

```python
import pandas as pd

df_atletas = pd.DataFrame({
    "jugador": ["Courtois", "Lunin", "Kepa"],
    "minutos": [1200, None, 1800]
})

# Aislamos las filas donde minutos es nulo
df_pendientes = df_atletas[df_atletas["minutos"].isna()]
print("Registros pendientes de validación médica:")
print(df_pendientes)
```

**Salida real:**

```text
Registros pendientes de validación médica:
  jugador  minutos
1   Lunin      NaN
```

## 8. Errores frecuentes y casos borde

1. Confundir cadenas vacías `""` o espacios `" "` con nulos: Pandas no las considera `NaN` salvo que se especifique en `read_csv(na_values=[""])`.

## 9. Buenas prácticas y rendimiento

* Encadenar `.isna().sum()` para auditar nulos en una sola instrucción vectorizada de alto rendimiento.

## 10. Métodos relacionados

* [dropna](../05_limpieza_transformacion/dropna.md) — Elimina filas o columnas con nulos.
* [fillna](../05_limpieza_transformacion/fillna.md) — Rellena o imputa valores nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.isna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html) (Pandas 2.2).
