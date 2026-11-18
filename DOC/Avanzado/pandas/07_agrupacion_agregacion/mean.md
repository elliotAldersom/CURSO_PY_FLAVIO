# `DataFrame.mean` y `Series.mean`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.mean(axis=0, skipna=True, numeric_only=False)
```

## 2. ¿Qué es?

Es un **método de reducción estadística** que calcula la media aritmética de los valores sobre un eje.

## 3. ¿Para qué sirve?

Calcula promedios representativos de variables continuas en análisis exploratorio y reportes de rendimiento.

* **Equivalencia en SQL:** `AVG(columna)`.

## 4. ¿Cómo funciona?

1. Suma vectorialmente los valores no nulos en C y divide entre el conteo efectivo de elementos válidos.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | Eje de reducción (`0` columnas, `1` filas). |
| `skipna` | `bool` | Opcional | `True` | Omite valores faltantes `NaN`. |
| `numeric_only` | `bool` | Opcional | `False` | Computa únicamente sobre tipos numéricos. |

## 6. Retorno

* Escalar (en Series) o `pandas.Series` (en DataFrame).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

minutos = pd.Series([90, 85, 90, 75])
print(minutos.mean())
```

**Salida real:**

```text
85.0
```

---

### Nivel 2: Intermedio

```python
import pandas as pd

df = pd.DataFrame({
    'posicion': ['DEL', 'DEL', 'DEF'],
    'kilometros': [10.5, 11.2, 9.8]
})
print(df.groupby('posicion')['kilometros'].mean().round(2))
```

**Salida real:**

```text
posicion
DEF      9.80
DEL     10.85
Name: kilometros, dtype: float64
```

---

### Nivel 3: Avanzado

```python
import pandas as pd

salarios = pd.Series([10000, 12000, 11000, 150000])
print(f'Media: {salarios.mean():.1f} | Mediana: {salarios.median():.1f}')
```

**Salida real:**

```text
Media: 45750.0 | Mediana: 11500.0
```

## 8. Errores frecuentes y casos borde

1. Columnas tipo string mezcladas sin `numeric_only=True`: En Pandas 2.x lanza `TypeError`.

## 9. Buenas prácticas y rendimiento

* Usar `numeric_only=True` en tablas heterogéneas.

## 10. Métodos relacionados

* `std` — Desviación estándar.
* `median` — Mediana robusta.

## 11. Referencias oficiales

* **API Reference:** [`DataFrame.mean` y `Series.mean`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.mean.html) (Pandas 2.2).
