# `DataFrame.duplicated` y `Series.duplicated`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.duplicated(subset=None, keep='first') -> pandas.Series[bool]
```

## 2. ¿Qué es?

Es un **método de diagnóstico de redundancia** que evalúa fila por fila si un registro está repetido en el DataFrame o Serie, retornando una máscara booleana (`True` si es duplicado, `False` si es único o la primera aparición).

## 3. ¿Para qué sirve?

A diferencia de `drop_duplicates` (que elimina directamente las filas), `duplicated` permite auditar, inspeccionar y cuantificar los registros repetidos antes de tomar decisiones de descarte.

* **Equivalencia en SQL:** `ROW_NUMBER() OVER (...) > 1`.

## 4. ¿Cómo funciona?

1. **Tabla hash en C:** Mantiene una tabla hash con las tuplas observadas según `subset` y evalúa según `keep`:
   * `'first'`: Marca como `True` todas las apariciones posteriores a la primera.
   * `'last'`: Marca como `True` todas las apariciones anteriores a la última.
   * `False`: Marca como `True` **todas** las filas que formen parte de un grupo duplicado.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `subset` | `str`, `list[str]` | Opcional | `None` | Columnas a evaluar. Si es `None`, evalúa todas las columnas. |
| `keep` | `{'first', 'last', False}` | Opcional | `'first'` | Criterio para definir cuáles filas se marcan como duplicadas. |

## 6. Retorno

* `pandas.Series[bool]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Messi", "Ronaldo", "Messi"], "equipo": ["Inter", "Al Nassr", "Inter"]})
print(df.duplicated())
```

**Salida real:**

```text
0    False
1    False
2     True
dtype: bool
```

---

### Nivel 2: Intermedio

Aislamiento de todos los registros redundantes para auditoría manual (`keep=False`):

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Vinicius Jr"],
    "fecha": ["2024-05-01", "2024-05-01", "2024-05-02"]
})

# keep=False identifica todas las filas involucradas en duplicidades
filas_en_conflicto = df[df.duplicated(subset=["jugador"], keep=False)]
print(filas_en_conflicto)
```

**Salida real:**

```text
       jugador       fecha
0  Vinicius Jr  2024-05-01
2  Vinicius Jr  2024-05-02
```

---

### Nivel 3: Avanzado

Aserción defensiva de clave primaria en pipelines de datos:

```python
import pandas as pd

def validar_clave_primaria_sin_duplicados(df: pd.DataFrame, col_id: str):
    duplicados = df.duplicated(subset=[col_id]).sum()
    if duplicados > 0:
        raise ValueError(f"Falla de integridad: Se detectaron {duplicados} IDs duplicados en '{col_id}'.")
    print(f"[OK] Integridad de clave primaria '{col_id}' validada con éxito.")

df_prueba = pd.DataFrame({"id_jugador": [101, 102, 103]})
validar_clave_primaria_sin_duplicados(df_prueba, "id_jugador")
```

**Salida real:**

```text
[OK] Integridad de clave primaria 'id_jugador' validada con éxito.
```

## 8. Errores frecuentes y casos borde

1. Evaluar nulos: Dos filas con `NaN` en las columnas evaluadas se consideran duplicadas entre sí a partir de la segunda aparición.

## 9. Buenas prácticas y rendimiento

* Usar `.duplicated().sum()` para verificar de inmediato si una tabla tiene filas redundantes.

## 10. Métodos relacionados

* [drop_duplicates](drop_duplicates.md) — Elimina físicamente las filas duplicadas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.duplicated](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html) (Pandas 2.2).
