# `DataFrame.melt`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.melt(
    id_vars=None,
    value_vars=None,
    var_name=None,
    value_name='value',
    col_level=None,
    ignore_index=True
) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es un **método de desanulación y normalización** que transforma un DataFrame de formato ancho (*wide format*) a formato largo (*long/tidy format*), desempacando columnas en filas.

## 3. ¿Para qué sirve?

Convierte tablas donde los nombres de columnas son variables (p. ej. `'Enero'`, `'Febrero'`, `'Marzo'`) en tablas normalizadas con una columna identificadora y otra con el valor, facilitando el análisis en Seaborn o PowerBI.

* **Equivalencia en SQL:** Operador `UNPIVOT`.

## 4. ¿Cómo funciona?

1. **Despivotado:** Mantiene fijas las columnas indicadas en `id_vars` y transfiere todas las columnas de `value_vars` a dos nuevas columnas: `var_name` (con los encabezados) y `value_name` (con las celdas).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `id_vars` | `str`, lista | Opcional | `None` | Columnas a preservar como identificadores. |
| `value_vars` | `str`, lista | Opcional | `None` | Columnas a desanular. Si es `None`, desanula todas las que no estén en `id_vars`. |
| `var_name` | `str` | Opcional | `None` | Nombre para la nueva columna de variables desanuladas. |
| `value_name` | `str` | Opcional | `'value'` | Nombre para la nueva columna de valores numéricos. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Desanulación de meses a formato vertical:

```python
import pandas as pd

df_ancho = pd.DataFrame({
    "jugador": ["Haaland"],
    "Goles_Ene": [4],
    "Goles_Feb": [5]
})

print(df_ancho.melt(id_vars=["jugador"]))
```

**Salida real:**

```text
   jugador   variable  value
0  Haaland  Goles_Ene      4
1  Haaland  Goles_Feb      5
```

---

### Nivel 2: Intermedio

Personalización de nombres semánticos de columnas generadas:

```python
import pandas as pd

df_rendimiento = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé"],
    "Liga": [21, 28],
    "Champions": [6, 8]
})

df_tidy = df_rendimiento.melt(
    id_vars="jugador",
    value_vars=["Liga", "Champions"],
    var_name="torneo",
    value_name="goles"
)
print(df_tidy)
```

**Salida real:**

```text
       jugador     torneo  goles
0  Vinicius Jr       Liga     21
1       Mbappé       Liga     28
2  Vinicius Jr  Champions      6
3       Mbappé  Champions      8
```

---

### Nivel 3: Avanzado

Preparación de datasets estructurados para modelos estadísticos en Seaborn:

```python
import pandas as pd

df_telemetria = pd.DataFrame({
    "atleta": ["Atleta_1", "Atleta_2"],
    "fase_inicial": [140, 138],
    "fase_media": [165, 170],
    "fase_final": [180, 182]
})

df_curva = df_telemetria.melt(
    id_vars="atleta",
    var_name="etapa_prueba",
    value_name="bpm"
)
print(df_curva)
```

**Salida real:**

```text
     atleta  etapa_prueba  bpm
0  Atleta_1  fase_inicial  140
1  Atleta_2  fase_inicial  138
2  Atleta_1    fase_media  165
3  Atleta_2    fase_media  170
4  Atleta_1    fase_final  180
5  Atleta_2    fase_final  182
```

## 8. Errores frecuentes y casos borde

1. No definir `id_vars`: Desanula el DataFrame entero convirtiendo todo en dos únicas columnas.

## 9. Buenas prácticas y rendimiento

* Emplear `melt` para normalizar datasets a la arquitectura *Tidy Data* de Hadley Wickham antes de modelar o graficar.

## 10. Métodos relacionados

* [pivot_table](../07_agrupacion_agregacion/pivot_table.md) — Operación inversa de agregación y pivote.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.melt](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html) (Pandas 2.2).
