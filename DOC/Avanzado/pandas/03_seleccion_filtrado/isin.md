# `DataFrame.isin` y `Series.isin`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.isin(values) -> pandas.DataFrame[bool]
```

## 2. ¿Qué es?

Es un **método de comprobación de pertenencia booleana** que verifica si cada elemento de una Serie o DataFrame está contenido en una lista, conjunto o diccionario de valores válidos.

## 3. ¿Para qué sirve?

Permite sustituir múltiples comparaciones or encadenadas (`col == 'A' | col == 'B' | col == 'C'`) por una instrucción limpia y vectorizada.

* **Equivalencia en SQL:** Equivale directamente a la cláusula `WHERE columna IN ('A', 'B', 'C')`.

## 4. ¿Cómo funciona?

1. **Búsqueda en conjunto hash:** Convierte la colección `values` en una estructura hash en C para búsquedas con complejidad promedio $O(1)$ por elemento.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `values` | `list`, `set`, `dict`, `Series` | Obligatorio | Posicional | Colección iterable de valores a contrastar. |

## 6. Retorno

* Máscara booleana (`Series[bool]` o `DataFrame[bool]`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Haaland", "Mbappé", "Saka"],
    "equipo": ["Real Madrid", "Man City", "Real Madrid", "Arsenal"]
})

equipos_objetivo = ["Real Madrid", "Arsenal"]
print(df[df["equipo"].isin(equipos_objetivo)])
```

**Salida real:**

```text
       jugador       equipo
0  Vinicius Jr  Real Madrid
2       Mbappé  Real Madrid
3         Saka      Arsenal
```

---

### Nivel 2: Intermedio

Negación lógica con operador `~` para exclusión de categorías:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Messi", "Ronaldo", "Suarez", "Neymar"],
    "liga": ["MLS", "Saudi Pro", "MLS", "Saudi Pro"]
})

# Excluir liga MLS
print(df[~df["liga"].isin(["MLS"])])
```

**Salida real:**

```text
   jugador       liga
1  Ronaldo  Saudi Pro
3   Neymar  Saudi Pro
```

---

### Nivel 3: Avanzado

Filtrado multidimensional mediante diccionario de condiciones por columna:

```python
import pandas as pd

df = pd.DataFrame({
    "equipo": ["Real Madrid", "Barcelona", "Real Madrid", "Arsenal"],
    "posicion": ["Delantero", "Mediocampista", "Defensa", "Delantero"]
})

criterios = {
    "equipo": ["Real Madrid"],
    "posicion": ["Delantero", "Defensa"]
}

# isin evalúa columna por columna; con all(axis=1) exigimos cumplir ambas
mascara = df.isin(criterios).all(axis=1)
print(df[mascara])
```

**Salida real:**

```text
        equipo   posicion
0  Real Madrid  Delantero
2  Real Madrid    Defensa
```

## 8. Errores frecuentes y casos borde

1. Pasar un único string no iterable en lugar de lista: `isin("Real Madrid")` buscará cada letra individual (`'R'`, `'e'`, `'a'`). **Solución:** Pasar `["Real Madrid"]`.

## 9. Buenas prácticas y rendimiento

* Pasar un `set` en lugar de una `list` si la colección contiene miles de elementos.

## 10. Métodos relacionados

* [between](between.md) — Pertenencia a rangos numéricos continuos.
* [filtrado_booleano](filtrado_booleano.md) — Filtros lógicos generales.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.isin](https://pandas.pydata.org/docs/reference/api/pandas.Series.isin.html) (Pandas 2.2).
