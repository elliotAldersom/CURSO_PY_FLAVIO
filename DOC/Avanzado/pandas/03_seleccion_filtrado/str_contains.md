# `Series.str.contains`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.str.contains(
    pat,
    case=True,
    flags=0,
    na=None,
    regex=True
) -> pandas.Series[bool]
```

## 2. ¿Qué es?

Es un **método del accesor de strings (`.str`)** que evalúa si una cadena literal o un patrón de expresión regular (Regex) está contenido dentro de cada elemento de una Serie de texto.

## 3. ¿Para qué sirve?

Permite buscar subcadenas, clasificar registros textuales, filtrar categorías por coincidencias parciales e ignorar mayúsculas y minúsculas.

* **Equivalencia en SQL:** Equivale a la cláusula `WHERE columna LIKE '%patron%'` o `WHERE columna ~ 'regex'`.

## 4. ¿Cómo funciona?

1. **Motor léxico CPython:** Aplica internamente el motor de expresiones regulares `re.search` de forma vectorizada fila a fila, o una búsqueda de subcadenas rápida si `regex=False`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `pat` | `str` | Obligatorio | Posicional | Caracteres literales o patrón de expresión regular a buscar. |
| `case` | `bool` | Opcional | `True` | Si es `False`, la búsqueda es insensible a mayúsculas/minúsculas (*case-insensitive*). |
| `na` | escalar | Opcional | `None` | Valor a asignar cuando se encuentra un valor nulo (`NaN`). |
| `regex` | `bool` | Opcional | `True` | Si es `False`, trata `pat` como una cadena literal pura sin interpretar metacaracteres. |

## 6. Retorno

* `pandas.Series[bool]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Búsqueda insensible a mayúsculas:

```python
import pandas as pd

jugadores = pd.Series(["Kylian Mbappé", "LIONEL MESSI", "Erling Haaland"])
filtro_messi = jugadores.str.contains("messi", case=False)
print(jugadores[filtro_messi])
```

**Salida real:**

```text
1    LIONEL MESSI
dtype: object
```

---

### Nivel 2: Intermedio

Tratamiento defensivo de valores nulos con `na=False`:

```python
import pandas as pd

plantel = pd.Series(["Vinicius Jr", None, "Rodrygo Goes"])
# na=False evita que los NaN contaminen la máscara booleana con valores no evaluables
filtro = plantel.str.contains("Goes", na=False)
print(plantel[filtro])
```

**Salida real:**

```text
2    Rodrygo Goes
dtype: object
```

---

### Nivel 3: Avanzado

Búsqueda con patrones Regex complejos de nombres de clubes:

```python
import pandas as pd

equipos = pd.Series(["Real Madrid CF", "FC Barcelona", "Manchester City FC", "Arsenal FC"])
# Regex: detecta si empieza con 'FC ' o termina con ' FC'
filtro_fc = equipos.str.contains(r"(^FC\s|\sFC$)", regex=True)
print(equipos[filtro_fc])
```

**Salida real:**

```text
1          FC Barcelona
2    Manchester City FC
3            Arsenal FC
dtype: object
```

## 8. Errores frecuentes y casos borde

1. Buscar caracteres especiales como `(` o `[` con `regex=True` sin escaparlos: Lanza `re.error: missing ), unterminated subpattern`. **Solución:** Pasar `regex=False`.

## 9. Buenas prácticas y rendimiento

* Si la búsqueda es una subcadena fija y no una expresión regular, pasar `regex=False` es hasta 5 veces más rápido.

## 10. Métodos relacionados

* [str_lower](../05_limpieza_transformacion/str_lower.md) — Normalización a minúsculas.
* [query](query.md) — Consultas lógicas declarativas.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.str.contains](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html) (Pandas 2.2).
