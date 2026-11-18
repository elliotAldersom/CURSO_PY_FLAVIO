# Filtrado Booleano en Pandas

```python
# NO EJECUTAR (Firma sintáctica en Pandas 2.2.x)
# Indexación con máscara booleana
DataFrame[mascara_booleana]
```

## 2. ¿Qué es?

Es una **técnica de indexación vectorizada** central en Pandas donde una expresión condicional genera una `Series` de valores booleanos (`True` o `False`), la cual se utiliza como filtro dentro de corchetes para extraer únicamente las filas que satisfacen la condición.

## 3. ¿Para qué sirve?

Permite segmentar datos tabulares basándose en reglas lógicas complejas (comparaciones numéricas, pertenencia, rangos) de forma declarativa y de alta velocidad.

* **Equivalencia en SQL:** Equivale directamente a la cláusula `WHERE condicion_1 AND / OR condicion_2`.

## 4. ¿Cómo funciona?

1. **Evaluación vectorizada a nivel C:** Al evaluar `df['goles'] > 20`, NumPy/Pandas compara elemento a elemento en memoria compilada sin bucles Python.
2. **Operadores bitwise obligatorios:** Debido a la precedencia y sobrecarga de operadores en Python, se deben usar obligatoriamente `&` (AND), `|` (OR) y `~` (NOT), **encerrando cada condición individual entre paréntesis obligatorios** `(cond1) & (cond2)`. El uso de `and`, `or` o `not` lanza un error `ValueError`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `mascara_booleana` | `Series[bool]`, arreglo booleano | Obligatorio | Posicional | Secuencia booleana de la misma longitud que el DataFrame. |

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame`.
* **Mutabilidad:** Inmutable; retorna un nuevo DataFrame con las filas filtradas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Filtro simple de goleadores:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Haaland", "Mbappé", "Foden", "Rodri"],
    "goles": [31, 28, 19, 8]
})

df_top = df[df["goles"] >= 20]
print(df_top)
```

**Salida real:**

```text
   jugador  goles
0  Haaland     31
1   Mbappé     28
```

---

### Nivel 2: Intermedio

Filtro compuesto con operadores `&` y `~` con paréntesis:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Rodrygo", "Guler", "Bellingham"],
    "equipo": ["Real Madrid", "Real Madrid", "Real Madrid", "Real Madrid"],
    "goles": [21, 15, 6, 19],
    "lesionado": [False, False, True, False]
})

# Goles >= 15 Y NO lesionado
filtro = (df["goles"] >= 15) & (~df["lesionado"])
print(df[filtro])
```

**Salida real:**

```text
       jugador       equipo  goles  lesionado
0  Vinicius Jr  Real Madrid     21      False
1      Rodrygo  Real Madrid     15      False
3   Bellingham  Real Madrid     19      False
```

---

### Nivel 3: Avanzado

Segmentación dinámica con funciones lambda en método `.loc`:

```python
import pandas as pd

df_atletas = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Yamal", "Lewandowski"],
    "minutos": [1200, 800, 2100, 2600],
    "goles": [4, 2, 8, 26]
})

# Encadenamiento con lambda dentro de loc
df_eficientes = df_atletas.loc[lambda d: (d["minutos"] > 1000) & (d["goles"] > 5), ["jugador", "goles"]]
print(df_eficientes)
```

**Salida real:**

```text
       jugador  goles
2        Yamal      8
3  Lewandowski     26
```

## 8. Errores frecuentes y casos borde

1. **`ValueError: The truth value of a Series is ambiguous`:** Ocurre al escribir `if df['goles'] > 10:` o usar la palabra clave `and` en lugar de `&`.
2. **Olvidar los paréntesis:** Escribir `df['a'] > 5 & df['b'] < 3` falla porque `&` tiene mayor precedencia que `<` o `>`.

## 9. Buenas prácticas y rendimiento

* Encapsular condiciones complejas en variables booleanas intermedias legibles antes de filtrar (`mascara_activos = ...`).

## 10. Métodos relacionados

* [query](query.md) — Filtrado declarativo mediante strings.
* [loc](loc.md) — Indexación basada en etiquetas y condiciones booleanas.

## 11. Referencias oficiales

* **Guía de usuario:** [Boolean Indexing in Pandas](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing).
