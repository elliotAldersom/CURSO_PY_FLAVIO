# `Series.str.strip`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.str.strip(to_strip=None) -> pandas.Series[str]
```

## 2. ¿Qué es?

Es un **método vectorizado de cadenas** que remueve espacios en blanco (o caracteres específicos indicados en `to_strip`) al principio y al final de cada texto.

## 3. ¿Para qué sirve?

Elimina espacios residuales invisibles introducidos en formularios manuales o CSVs mal formateados que impiden cruces relacionales exactos.

* **Equivalencia en SQL:** `TRIM(columna)`.

## 4. ¿Cómo funciona?

1. Elimina `\s`, tabulaciones `	` o saltos de línea `
` laterales de forma vectorizada.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `to_strip` | `str` | Opcional | `None` | Caracteres específicos a remover. Si es `None`, remueve cualquier espacio en blanco. |

## 6. Retorno

* `pandas.Series[str]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

s = pd.Series(["  Vinicius Jr  ", "Rodrygo  ", "  Bellingham"])
print(s.str.strip())
```

**Salida real:**

```text
0    Vinicius Jr
1        Rodrygo
2     Bellingham
dtype: object
```

---

### Nivel 2: Intermedio

Eliminación de caracteres especiales o puntuación marginal:

```python
import pandas as pd

codigos = pd.Series(["#JUG_01#", "#JUG_02", "JUG_03#"])
print(codigos.str.strip("#"))
```

**Salida real:**

```text
0    JUG_01
1    JUG_02
2    JUG_03
dtype: object
```

---

### Nivel 3: Avanzado

Limpieza masiva de todas las columnas de texto de un DataFrame:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["  Pedri  ", "  Gavi  "],
    "club": ["  Barcelona  ", "  Barcelona  "],
    "goles": [4, 2]
})

cols_texto = df.select_dtypes(include="object").columns
df[cols_texto] = df[cols_texto].apply(lambda col: col.str.strip())
print(df)
```

**Salida real:**

```text
  jugador       club  goles
0   Pedri  Barcelona      4
1    Gavi  Barcelona      2
```

## 8. Errores frecuentes y casos borde

1. Creer que elimina espacios internos: `"Real   Madrid".str.strip()` conserva los espacios centrales.

## 9. Buenas prácticas y rendimiento

* Aplicar siempre tras cargar CSVs con delimitadores irregulares.

## 10. Métodos relacionados

* [str_lower](str_lower.md) — Minúsculas.
* [replace](replace.md) — Reemplazo general de valores.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.str.strip](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.strip.html) (Pandas 2.2).
