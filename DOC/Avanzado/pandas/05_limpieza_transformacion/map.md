# `Series.map` y `DataFrame.map`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.map(arg, na_action=None) -> pandas.Series
DataFrame.map(func, na_action=None, **kwargs) -> pandas.DataFrame
```

## 2. ¿Qué es?

En `Series`, es un **método de transformación elemento a elemento** basado en diccionarios, Series o funciones. En `DataFrame` (a partir de Pandas 2.1+), es el reemplazo oficial y moderno del obsoleto `applymap`.

## 3. ¿Para qué sirve?

Transforma y recodifica valores individuales celda por celda de forma declarativa.

* **Equivalencia en SQL:** Sentencias `JOIN` con tablas de catálogo o expresiones `CASE`.

## 4. ¿Cómo funciona?

1. **Mapeo por lookup:** Si se le pasa un diccionario, mapea cada valor a su clave. **Importante:** Cualquier valor que no figure en el diccionario se convierte automáticamente en `NaN`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `arg` / `func` | `dict`, `Series`, `callable` | Obligatorio | Posicional | Regla de transformación celda por celda. |
| `na_action` | `{None, 'ignore'}` | Opcional | `None` | Si es `'ignore'`, no aplica la función a celdas nulas. |

## 6. Retorno

* `pandas.Series` o `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Mapeo de diccionario sobre Serie:

```python
import pandas as pd

codigos_pais = pd.Series(["ARG", "BRA", "FRA"])
paises = codigos_pais.map({"ARG": "Argentina", "BRA": "Brasil", "FRA": "Francia"})
print(paises)
```

**Salida real:**

```text
0    Argentina
1       Brasil
2      Francia
dtype: object
```

---

### Nivel 2: Intermedio

Transformación en DataFrame completo con `DataFrame.map` (reemplazo de `applymap`):

```python
import pandas as pd

df_metricas = pd.DataFrame({
    "velocidad_kmh": [32.456, 34.123],
    "distancia_km": [11.891, 10.452]
})

# Redondeo elemento a elemento en todo el DataFrame
print(df_metricas.map(lambda x: round(x, 1)))
```

**Salida real:**

```text
   velocidad_kmh  distancia_km
0           32.5          11.9
1           34.1          10.5
```

---

### Nivel 3: Avanzado

Formateo avanzado respetando nulos con `na_action='ignore'`:

```python
import pandas as pd

salarios = pd.Series([25000000, None, 18500000])
salarios_fmt = salarios.map(lambda s: f"$ {s:,.0f} USD", na_action="ignore")
print(salarios_fmt)
```

**Salida real:**

```text
0    $ 25,000,000 USD
1                 NaN
2    $ 18,500,000 USD
dtype: object
```

## 8. Errores frecuentes y casos borde

1. Usar un diccionario y olvidar que los valores no encontrados se vuelven `NaN`. Si se quiere conservar el original, usar `.replace()`.

## 9. Buenas prácticas y rendimiento

* Usar `DataFrame.map` en Pandas 2.x/3.0; nunca invocar el método deprecado `applymap`.

## 10. Métodos relacionados

* [replace](replace.md) — Reemplazo selectivo que preserva no mapeados.
* [apply](apply.md) — Aplicación a nivel de filas o columnas.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.map](https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html) (Pandas 2.2).
