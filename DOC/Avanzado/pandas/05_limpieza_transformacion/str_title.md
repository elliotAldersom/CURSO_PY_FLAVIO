# `Series.str.title`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.str.title() -> pandas.Series[str]
```

## 2. ¿Qué es?

Es un **método de formateo de texto** que capitaliza la primera letra de cada palabra de una Serie, convirtiendo las demás a minúsculas.

## 3. ¿Para qué sirve?

Formatea nombres propios de personas, clubes o estadios para reportes ejecutivos.

* **Equivalencia en SQL:** `INITCAP(columna)`.

## 4. ¿Cómo funciona?

1. Aplica la regla `title()` de Unicode sobre cada elemento de la Serie.

## 5. Parámetros

* No recibe parámetros.

## 6. Retorno

* `pandas.Series[str]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

nombres = pd.Series(["lionel messi", "erling haaland", "kylian mbappé"])
print(nombres.str.title())
```

**Salida real:**

```text
0     Lionel Messi
1   Erling Haaland
2    Kylian Mbappé
dtype: object
```

---

### Nivel 2: Intermedio

Corrección de mayúsculas sostenidas:

```python
import pandas as pd

clubes = pd.Series(["REAL MADRID", "ATLETICO DE MADRID"])
print(clubes.str.title())
```

**Salida real:**

```text
0           Real Madrid
1    Atletico De Madrid
dtype: object
```

---

### Nivel 3: Avanzado

Integración con canalización de limpieza de entidades:

```python
import pandas as pd

df = pd.DataFrame({"nombre_ingesta": ["fede VALVERDE", "luka MODRIC"]})
df["nombre_oficial"] = df["nombre_ingesta"].str.strip().str.title()
print(df)
```

**Salida real:**

```text
  nombre_ingesta  nombre_oficial
0  fede VALVERDE   Fede Valverde
1    luka MODRIC     Luka Modric
```

## 8. Errores frecuentes y casos borde

1. Palabras con apóstrofes: `"o'neill".title()` genera `"O'Neill"`, pero palabras como `"it's"` generan `"It'S"`.

## 9. Buenas prácticas y rendimiento

* Aplicar como paso final de presentación visual, no para claves de búsqueda.

## 10. Métodos relacionados

* [str_lower](str_lower.md) — Minúsculas para búsquedas.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.str.title](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.title.html) (Pandas 2.2).
