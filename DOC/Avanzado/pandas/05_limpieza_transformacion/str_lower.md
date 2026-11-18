# `Series.str.lower`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.str.lower() -> pandas.Series[str]
```

## 2. ¿Qué es?

Es un **método vectorizado de cadenas de texto** del accesor `.str` que convierte todos los caracteres alfabéticos de una Serie a minúsculas, respetando valores nulos.

## 3. ¿Para qué sirve?

Estandariza campos de texto (nombres, correos, categorías) antes de realizar agrupaciones, fusiones o comparaciones de igualdad.

* **Equivalencia en SQL:** Equivale a la función `LOWER(columna)`.

## 4. ¿Cómo funciona?

1. **Vectorización:** Invoca internamente `str.lower` de Python sobre cada elemento saltando de forma transparente los valores `NaN`.

## 5. Parámetros

* No recibe parámetros obligatorios ni opcionales.

## 6. Retorno

* `pandas.Series[str]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

equipos = pd.Series(["REAL MADRID", "FC Barcelona", "MANCHESTER CITY"])
print(equipos.str.lower())
```

**Salida real:**

```text
0       real madrid
1      fc barcelona
2    manchester city
dtype: object
```

---

### Nivel 2: Intermedio

Normalización defensiva tolerando valores nulos:

```python
import pandas as pd

jugadores = pd.Series(["VINICIUS JR", None, "RODRYGO GOES"])
print(jugadores.str.lower())
```

**Salida real:**

```text
0     vinicius jr
1            None
2    rodrygo goes
dtype: object
```

---

### Nivel 3: Avanzado

Pipeline de homogeneización antes de cruzar datos:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador_raw": ["  MESSI  ", "haaland ", " MBAPPÉ"]
})

df["jugador_limpio"] = df["jugador_raw"].str.strip().str.lower()
print(df)
```

**Salida real:**

```text
  jugador_raw jugador_limpio
0     MESSI            messi
1    haaland         haaland
2     MBAPPÉ          mbappé
```

## 8. Errores frecuentes y casos borde

1. Intentar aplicar `.lower()` directamente a la Serie sin el accesor `.str`: Lanza `AttributeError: 'Series' object has no attribute 'lower'`.

## 9. Buenas prácticas y rendimiento

* Con tipos PyArrow (`string[pyarrow]`), `str.lower()` se ejecuta en C++ multihilo ultra veloz.

## 10. Métodos relacionados

* [str_strip](str_strip.md) — Eliminación de espacios laterales.
* [str_title](str_title.md) — Capitalización tipo título.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.str.lower](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.lower.html) (Pandas 2.2).
