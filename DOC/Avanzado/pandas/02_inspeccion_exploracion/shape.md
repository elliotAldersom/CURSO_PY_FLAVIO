# `DataFrame.shape`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
# Atributo (propiedad sin paréntesis)
DataFrame.shape -> tuple[int, int]
```

## 2. ¿Qué es?

Es un **atributo de propiedad** (no un método ejecutable) que devuelve una tupla de Python con la dimensionalidad física del DataFrame: `(cantidad_filas, cantidad_columnas)`.

## 3. ¿Para qué sirve?

Permite conocer instantáneamente el tamaño del conjunto de datos y realizar desempaquetamiento de variables para validaciones defensivas de integridad dimensional.

* **Equivalencia en SQL:** Equivale a consultar `COUNT(*)` y el conteo de columnas en el esquema.

## 4. ¿Cómo funciona?

1. **Metadatos $O(1)$:** No itera sobre los datos. Consulta directamente la longitud del `Index` de filas y del `Index` de columnas (`len(self.index), len(self.columns)`), con complejidad de tiempo $O(1)$.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| *No posee* | N/A | N/A | N/A | Es una propiedad inmutable de sólo lectura; no recibe parámetros ni paréntesis. |

> [!NOTE] Diferencia entre propiedad y método
> Una **propiedad** se accede sin paréntesis (`df.shape`). Intentar invocarla como `df.shape()` lanzará un error de tipo `TypeError: 'tuple' object is not callable`.

## 6. Retorno

* **Tipo devuelto:** `tuple[int, int]` (en `Series` devuelve `tuple[int,]`).
* **Mutabilidad:** Inmutable.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Consulta directa de dimensiones:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Pedri", "Gavi", "Yamal"],
    "equipo": ["Barcelona", "Barcelona", "Barcelona"]
})

print(df_liga.shape)
```

**Salida real:**

```text
(3, 2)
```

---

### Nivel 2: Intermedio

Desempaquetamiento directo en variables de flujo:

```python
import pandas as pd

df_partidos = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Rodrygo"],
    "goles": [21, 15],
    "asistencias": [11, 8]
})

filas, columnas = df_partidos.shape
print(f"El dataset contiene {filas} jugadores evaluados en {columnas} métricas.")
```

**Salida real:**

```text
El dataset contiene 2 jugadores evaluados en 3 métricas.
```

---

### Nivel 3: Avanzado

Validación defensiva de aserción post-filtrado en pipelines de ETL:

```python
import pandas as pd

def verificar_integridad_columnar(df_original: pd.DataFrame, df_procesado: pd.DataFrame):
    _, cols_orig = df_original.shape
    _, cols_proc = df_procesado.shape
    assert cols_orig == cols_proc, f"Error: Se perdieron columnas ({cols_orig} -> {cols_proc})"
    print(f"[OK] Integridad columnar garantizada: {cols_proc} columnas preservadas.")

df_raw = pd.DataFrame({"jugador": ["Kimmich"], "pases": [90]})
df_clean = df_raw.copy()
verificar_integridad_columnar(df_raw, df_clean)
```

**Salida real:**

```text
[OK] Integridad columnar garantizada: 1 columnas preservadas.
```

## 8. Errores frecuentes y casos borde

1. **`TypeError: 'tuple' object is not callable`:** Ocurre al escribir por equivocación `df.shape()`.

## 9. Buenas prácticas y rendimiento

* Preferir `len(df)` si sólo se requiere la cantidad de filas, ya que es marginalmente más rápido que `df.shape[0]`.

## 10. Métodos relacionados

* [columns](columns.md) — Nombres de las columnas.
* [dtypes](dtypes.md) — Tipos de datos de cada columna.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.shape](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html) (Pandas 2.2).
