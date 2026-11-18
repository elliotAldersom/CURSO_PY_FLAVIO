# `DataFrame.dtypes`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
# Atributo (propiedad)
DataFrame.dtypes -> pandas.Series
```

## 2. ¿Qué es?

Es un **atributo de propiedad** que devuelve una `Series` de Pandas con el tipo físico de almacenamiento (`dtype`) asignado a cada columna del DataFrame.

## 3. ¿Para qué sirve?

Permite certificar que las variables numéricas no hayan sido importadas erróneamente como texto (`object`), y que fechas y categorías cuenten con la representación óptima en memoria.

* **Equivalencia en SQL:** Consulta de tipos en el catálogo de columnas de base de datos.

## 4. ¿Cómo funciona?

1. **Inspección de metadatos:** Lee los metadatos de los arreglos columnares de NumPy o PyArrow subyacentes.

## 5. Parámetros

* No recibe parámetros (es una propiedad).

## 6. Retorno

* **Tipo devuelto:** `pandas.Series` indexada por los nombres de columna, con valores de tipo `numpy.dtype` o tipos de extensión de Pandas (`ArrowDtype`, `CategoricalDtype`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Bellingham", "Wirtz"],
    "goles": [19, 11],
    "promedio": [0.65, 0.42]
})
print(df.dtypes)
```

**Salida real:**

```text
jugador      object
goles         int64
promedio    float64
dtype: object
```

---

### Nivel 2: Intermedio

Filtrado de columnas de tipo numérico mediante `dtypes`:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Alisson"],
    "atajadas": [12],
    "altura": [1.93]
})

cols_numericas = df.dtypes[df.dtypes != "object"].index.tolist()
print("Columnas numéricas detectadas:", cols_numericas)
```

**Salida real:**

```text
Columnas numéricas detectadas: ['atajadas', 'altura']
```

---

### Nivel 3: Avanzado

Auditoría defensiva de tipos antes del entrenamiento de un modelo:

```python
import pandas as pd

def auditar_tipos_sin_objetos(df: pd.DataFrame):
    objetos = df.select_dtypes(include=["object"]).columns.tolist()
    if objetos:
        print(f"[ADVERTENCIA] Columnas sin tipado compacto detectadas: {objetos}")
    else:
        print("[OK] Todas las columnas están optimizadas numéricamente o con tipos flecha.")

df_prueba = pd.DataFrame({"id": [1, 2], "dato": ["A", "B"]})
auditar_tipos_sin_objetos(df_prueba)
```

**Salida real:**

```text
[ADVERTENCIA] Columnas sin tipado compacto detectadas: ['dato']
```

## 8. Errores frecuentes y casos borde

1. Confundir `type(df['col'])` (que devuelve `Series`) con `df['col'].dtype` (que devuelve el tipo interno de sus valores).

## 9. Buenas prácticas y rendimiento

* En Pandas 2.x+, convertir columnas `object` a `string` o `category` para reducir hasta un 70% el consumo de RAM.

## 10. Métodos relacionados

* [astype](../05_limpieza_transformacion/astype.md) — Conversión explícita de tipos.
* [info](info.md) — Resumen completo de tipos y nulos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.dtypes](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html) (Pandas 2.2).
