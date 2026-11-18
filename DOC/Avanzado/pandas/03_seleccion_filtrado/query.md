# `DataFrame.query`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.query(expr, *, inplace=False, **kwargs)
```

## 2. ¿Qué es?

Es un **método declarativo de filtrado** que evalúa una expresión lógica en forma de string utilizando internamente el motor compilado `numexpr` o Python puro.

## 3. ¿Para qué sirve?

Mejora drásticamente la legibilidad del código al eliminar la repetición del nombre del DataFrame (`df[df['col'] > 5]`) y permitir referenciar variables del entorno local mediante el prefijo `@`.

* **Equivalencia en SQL:** Equivale casi literalmente a la cláusula `WHERE col > 10 AND estado = 'Activo'`.

## 4. ¿Cómo funciona?

1. **Parser sintáctico:** Analiza la expresión con el analizador gramatical de Python o `numexpr`, evitando instanciar series intermedias en memoria y optimizando la velocidad en tablas de millones de registros.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `expr` | `str` | Obligatorio | Posicional | Cadena de texto con la expresión booleana a evaluar. |
| `inplace` | `bool` | Opcional | `False` | Modifica en el lugar (en desuso en Pandas 2.x). |

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Rodrygo"],
    "goles": [21, 28, 15]
})

print(df.query("goles > 20"))
```

**Salida real:**

```text
       jugador  goles
0  Vinicius Jr     21
1       Mbappé     28
```

---

### Nivel 2: Intermedio

Referencia a variables locales del entorno de Python con el símbolo `@`:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Lautaro", "Thuram", "Barella"],
    "minutos": [2600, 2100, 2400]
})

umbral_minutos = 2200
print(df.query("minutos >= @umbral_minutos"))
```

**Salida real:**

```text
   jugador  minutos
0  Lautaro     2600
2  Barella     2400
```

---

### Nivel 3: Avanzado

Consultas complejas con operadores lógicos de texto y tratamiento de nombres de columnas con espacios:

```python
import pandas as pd

df = pd.DataFrame({
    "Nombre Jugador": ["Pedri", "Yamal", "Lewandowski"],
    "equipo": ["Barcelona", "Barcelona", "Barcelona"],
    "goles": [4, 8, 26]
})

# Columnas con espacios se encierran entre acentos graves `...`
resultado = df.query("`Nombre Jugador`.str.startswith('Y') or goles > 20")
print(resultado)
```

**Salida real:**

```text
  Nombre Jugador     equipo  goles
1          Yamal  Barcelona      8
2    Lewandowski  Barcelona     26
```

## 8. Errores frecuentes y casos borde

1. Columnas con espacios o palabras reservadas sin acentos graves (`` `col con espacio` ``): Lanza `SyntaxError`.

## 9. Buenas prácticas y rendimiento

* En DataFrames con más de 200.000 filas, `query()` con `numexpr` instalado es notablemente más veloz que la indexación booleana tradicional.

## 10. Métodos relacionados

* [filtrado_booleano](filtrado_booleano.md) — Filtrado booleano clásico con corchetes.
* [loc](loc.md) — Indexación basada en etiquetas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.query](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html) (Pandas 2.2).
