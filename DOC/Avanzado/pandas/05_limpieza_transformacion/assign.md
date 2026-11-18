# `DataFrame.assign`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.assign(**kwargs) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es un **método de asignación funcional** que crea y adjunta nuevas columnas a un DataFrame retornando una nueva copia, ideal para tuberías encadenadas de transformación.

## 3. ¿Para qué sirve?

Evita la mutación de estado imperativo (`df['nueva'] = ...`) y permite encadenar transformaciones fluidas con sintaxis funcional.

* **Equivalencia en SQL:** Generar campos calculados en la lista `SELECT ..., col1 / col2 AS nueva_col`.

## 4. ¿Cómo funciona?

1. **Evaluación de callables:** Acepta funciones lambda donde el argumento representa el DataFrame en el estado exacto de la canalización previa.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `**kwargs` | expresiones, `callables` | Obligatorio | Clave=Valor | Columnas a calcular y agregar. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Kane"], "goles": [36], "partidos": [32]})
print(df.assign(promedio=df["goles"] / df["partidos"]))
```

**Salida real:**

```text
  jugador  goles  partidos  promedio
0    Kane     36        32     1.125
```

---

### Nivel 2: Intermedio

Uso de lambdas para encadenar cálculos dependientes:

```python
import pandas as pd

df = pd.DataFrame({"goles": [25, 20]})
df_resultado = (
    df.assign(goles_duplicados=lambda d: d["goles"] * 2)
      .assign(puntos_estimados=lambda d: d["goles_duplicados"] + 5)
)
print(df_resultado)
```

**Salida real:**

```text
   goles  goles_duplicados  puntos_estimados
0     25                50                55
1     20                40                45
```

---

### Nivel 3: Avanzado

Tubería de ingeniería de características sin variables temporales:

```python
import pandas as pd

df_atletas = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé"],
    "minutos": [2100, 2450],
    "goles": [21, 28]
})

df_metricas = (
    df_atletas
    .assign(min_por_gol=lambda d: (d["minutos"] / d["goles"]).round(1))
    .assign(categoria=lambda d: ["Elite" if m < 110 else "Estándar" for m in d["min_por_gol"]])
    .sort_values(by="min_por_gol")
)
print(df_metricas)
```

**Salida real:**

```text
       jugador  minutos  goles  min_por_gol categoria
1       Mbappé     2450     28         87.5     Elite
0  Vinicius Jr     2100     21        100.0     Elite
```

## 8. Errores frecuentes y casos borde

1. No usar lambda al referenciar una columna calculada en la misma cadena: Intentar usar `df['nueva']` fallará porque aún no existe en el DataFrame inicial.

## 9. Buenas prácticas y rendimiento

* Usar siempre lambdas en `assign()` para garantizar encadenamiento desacoplado.

## 10. Métodos relacionados

* [pipe](pipe.md) — Canalización de funciones de alto nivel.
* [apply](apply.md) — Transformación por filas o columnas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.assign](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html) (Pandas 2.2).
