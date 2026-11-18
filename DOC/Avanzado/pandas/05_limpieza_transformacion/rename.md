# `DataFrame.rename`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.rename(
    mapper=None,
    *,
    index=None,
    columns=None,
    axis=None,
    copy=None,
    inplace=False,
    level=None,
    errors='ignore'
)
```

## 2. ¿Qué es?

Es un **método de renombrado selectivo** que altera las etiquetas de columnas o índices pasando un diccionario de mapeo o una función.

## 3. ¿Para qué sirve?

Permite corregir nombres de columnas sin necesidad de redefinir la lista completa de columnas del DataFrame.

* **Equivalencia en SQL:** Cláusula `AS nuevo_nombre`.

## 4. ¿Cómo funciona?

1. **Mapeo por diccionario:** Reemplaza únicamente las claves presentes en el diccionario suministrado; las columnas no mencionadas permanecen intactas.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `columns` | `dict`, `callable` | Opcional | `None` | Diccionario `{nombre_antiguo: nombre_nuevo}` o función de transformación. |
| `index` | `dict`, `callable` | Opcional | `None` | Mapeo para etiquetas de filas. |
| `errors` | `{'ignore', 'raise'}` | Opcional | `'ignore'` | Si es `'raise'`, arroja `KeyError` si una columna mapeada no existe. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"j": ["Messi"], "g": [25]})
print(df.rename(columns={"j": "jugador", "g": "goles"}))
```

**Salida real:**

```text
  jugador  goles
0   Messi     25
```

---

### Nivel 2: Intermedio

Renombrado mediante función con validación de errores:

```python
import pandas as pd

df = pd.DataFrame({"Nombre": ["Pedri"], "Minutos Jugados": [1800]})
df_renombrado = df.rename(columns=lambda c: c.lower().replace(" ", "_"))
print(df_renombrado)
```

**Salida real:**

```text
  nombre  minutos_jugados
0  Pedri             1800
```

---

### Nivel 3: Avanzado

Validación contractual con `errors='raise'`:

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Rodri"], "goles": [8]})
try:
    df.rename(columns={"col_fantasma": "nueva_col"}, errors="raise")
except KeyError as err:
    print(f"[ERROR CAPTURADO] Intento de renombrar columna inexistente: {err}")
```

**Salida real:**

```text
[ERROR CAPTURADO] Intento de renombrar columna inexistente: "['col_fantasma'] not found in axis"
```

## 8. Errores frecuentes y casos borde

1. Confundir `df.rename(columns={...})` con `df.rename(mapper, axis=1)`. Ambas son válidas, pero `columns={...}` es más explícita y recomendada.

## 9. Buenas prácticas y rendimiento

* Usar diccionarios explícitos para garantizar claridad conceptual en revisiones de código.

## 10. Métodos relacionados

* [columns](../02_inspeccion_exploracion/columns.md) — Asignación masiva.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.rename](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html) (Pandas 2.2).
