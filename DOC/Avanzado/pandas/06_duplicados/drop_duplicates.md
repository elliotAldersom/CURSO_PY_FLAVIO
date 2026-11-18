# `DataFrame.drop_duplicates`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.drop_duplicates(
    subset=None,
    *,
    keep='first',
    inplace=False,
    ignore_index=False
)
```

## 2. ¿Qué es?

Es un **método de instancia** perteneciente a la clase `pandas.DataFrame` (con variante análoga en `pandas.Series`). Se invoca directamente sobre un objeto `DataFrame` existente para identificar y descartar registros redundantes basándose en la totalidad de sus columnas o en un subconjunto específico de ellas.

## 3. ¿Para qué sirve?

Resuelve el problema de la duplicación de datos generada durante procesos de ingesta, concatenación de múltiples fuentes, reintentos de red o errores de registro transaccional. Garantiza la unicidad lógica de las entidades dentro del conjunto de datos antes de proceder al entrenamiento de modelos o cálculo de agregaciones.

* **Equivalencia en SQL:** Equivale a la cláusula `SELECT DISTINCT` o a filtrar mediante una función de ventana `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) = 1`.

## 4. ¿Cómo funciona?

Internamente, Pandas evalúa la duplicación delegando en una tabla hash escrita en C/Cython (`khash`).

1. **Construcción de claves hash:** Si se especifica `subset`, Pandas construye una tupla hash con los valores de las columnas indicadas fila por fila; si `subset=None`, computa el hash considerando cada fila completa.
2. **Evaluación de colisiones y orden:** El algoritmo recorre las filas secuencialmente preservando el orden de inserción:
   * Con `keep='first'`, la primera vez que se observa una clave hash se registra como válida; las apariciones posteriores con idéntica clave se marcan para eliminación.
   * Con `keep='last'`, el recorrido lógico retiene únicamente la última fila vista con esa clave hash.
   * Con `keep=False`, cualquier clave hash que aparezca dos o más veces en el conjunto de datos es marcada por completo para ser descartada (eliminando tanto la original como sus réplicas).
3. **Manejo de valores nulos:** A diferencia de SQL estándar donde `NULL = NULL` evalúa a desconocido, en el algoritmo de deduplicación de Pandas **dos valores `NaN`/`None`/`pd.NA` en la misma columna se consideran idénticos**, por lo que solo se conservará uno según el criterio de `keep`.
4. **Construcción del resultado:** Salvo que se indique `ignore_index=True`, el método preserva las etiquetas del `Index` original de las filas conservadas, lo que genera saltos en la numeración del índice.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `subset` | `str`, `list[str]`, `tuple` o `None` | Opcional | `None` | Nombre o lista de nombres de columnas a considerar para determinar si una fila está duplicada. Si es `None`, se evalúan todas las columnas del DataFrame. |
| `keep` | `{'first', 'last', False}` | Opcional | `'first'` | Determina qué duplicados se conservan: `'first'` conserva la primera aparición; `'last'` conserva la última aparición; `False` elimina todas las filas duplicadas. |
| `inplace` | `bool` | Opcional | `False` | Modifica el DataFrame directamente en memoria en lugar de retornar uno nuevo. **Obsolescencia:** En desuso (*deprecated*) a partir de Pandas 2.x hacia 3.0 bajo el modelo *Copy-on-Write*; debe evitarse en código nuevo. |
| `ignore_index` | `bool` | Opcional | `False` | Si es `True`, el DataFrame resultante se reindexa automáticamente desde `0` hasta `n - 1`. Si es `False`, se mantienen las etiquetas originales del índice. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es el identificador formal definido en la firma del método (por ejemplo, `subset` o `keep`). El **argumento** es el valor concreto que se le pasa al invocarlo en tiempo de ejecución (por ejemplo, `subset=["jugador", "equipo"]` o `keep="last"`).

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `None` si se usó el argumento obsoleto `inplace=True`).
* **Mutabilidad:** Con `inplace=False` (predeterminado), el método **no modifica el DataFrame original**, sino que devuelve una **nueva estructura DataFrame** con las filas duplicadas filtradas.

## 7. Ejemplos en tres niveles

El dominio unificado para todos los ejemplos corresponde al rendimiento de jugadores de fútbol en una liga profesional.

### Nivel 1: Básico (Uso mínimo predeterminado)

Deduplicación directa sobre todas las columnas conservando la primera ocurrencia:

```python
import pandas as pd

# Creación de DataFrame con una fila exactamente duplicada (filas 0 y 3)
datos = {
    "jugador": ["Lionel Messi", "Kylian Mbappé", "Erling Haaland", "Lionel Messi"],
    "equipo": ["Inter Miami", "Real Madrid", "Manchester City", "Inter Miami"],
    "goles": [25, 28, 31, 25],
    "minutos_jugados": [2100, 2450, 2600, 2100],
}
df_partidos = pd.DataFrame(datos)

# Eliminación de duplicados exactos
df_sin_duplicados = df_partidos.drop_duplicates()

print("Original:")
print(df_partidos)
print("\nResultado básico:")
print(df_sin_duplicados)
```

**Salida real:**

```text
Original:
          jugador           equipo  goles  minutos_jugados
0    Lionel Messi      Inter Miami     25             2100
1   Kylian Mbappé      Real Madrid     28             2450
2  Erling Haaland  Manchester City     31             2600
3    Lionel Messi      Inter Miami     25             2100

Resultado básico:
          jugador           equipo  goles  minutos_jugados
0    Lionel Messi      Inter Miami     25             2100
1   Kylian Mbappé      Real Madrid     28             2450
2  Erling Haaland  Manchester City     31             2600
```

---

### Nivel 2: Intermedio (Subconjunto de columnas, valores nulos y reindexación)

Deduplicación basada únicamente en la clave de negocio (`jugador`), reteniendo el registro más reciente (`keep='last'`) y reseteando el índice continuo (`ignore_index=True`):

```python
import pandas as pd

# Registro cronológico donde un jugador tiene múltiples mediciones y registros nulos
datos_rendimiento = {
    "jugador": ["Vinicius Jr", "Bukayo Saka", "Vinicius Jr", "Rodri", "Bukayo Saka"],
    "equipo": ["Real Madrid", "Arsenal", "Real Madrid", "Manchester City", "Arsenal"],
    "goles": [15, None, 21, 8, 16],
    "fecha_registro": ["2024-01-15", "2024-01-15", "2024-05-20", "2024-05-20", "2024-05-20"],
}
df_rendimiento = pd.DataFrame(datos_rendimiento)

# Deduplicamos por jugador conservando el último registro temporal y limpiando el índice
df_ultimo_estado = df_rendimiento.drop_duplicates(
    subset=["jugador"],
    keep="last",
    ignore_index=True
)

print(df_ultimo_estado)
```

**Salida real:**

```text
       jugador           equipo  goles fecha_registro
0        Rodri  Manchester City    8.0     2024-05-20
1  Vinicius Jr      Real Madrid   21.0     2024-05-20
2  Bukayo Saka          Arsenal   16.0     2024-05-20
```

---

### Nivel 3: Avanzado (Canalización de producción con validación y auditoría)

En pipelines de datos profesionales, `drop_duplicates` no se ejecuta a ciegas. Se combina con ordenamiento determinista previo (`sort_values`), validación de cardinalidad antes y después, y encadenamiento funcional mediante `.pipe()`:

```python
import pandas as pd

def deduplicar_estricto(df: pd.DataFrame, clave: list[str], orden_col: str) -> pd.DataFrame:
    """
    Ordena descendentemente por una columna temporal/métrica y deduplica
    registrando la cantidad exacta de registros eliminados.
    """
    total_inicial = len(df)
    
    df_procesado = (
        df.sort_values(by=orden_col, ascending=False)
        .drop_duplicates(subset=clave, keep="first", ignore_index=True)
    )
    
    eliminados = total_inicial - len(df_procesado)
    print(f"[AUDITORÍA] Registros iniciales: {total_inicial} | Duplicados eliminados: {eliminados}")
    return df_procesado

# Ingesta con duplicidades parciales
telemetria_partido = pd.DataFrame({
    "jugador": ["Jude Bellingham", "Florian Wirtz", "Jude Bellingham", "Pedri", "Florian Wirtz"],
    "equipo": ["Real Madrid", "Bayer Leverkusen", "Real Madrid", "Barcelona", "Bayer Leverkusen"],
    "minutos_jugados": [85, 90, 45, 90, 90],
    "kilometros_recorridos": [11.2, 12.1, 5.8, 11.8, 12.0],
})

# Ejecución dentro de pipeline analítico
df_consolidado = telemetria_partido.pipe(
    deduplicar_estricto,
    clave=["jugador", "equipo"],
    orden_col="minutos_jugados"
)

print("\nResultado consolidado (mayor minutaje retenido):")
print(df_consolidado)
```

**Salida real:**

```text
[AUDITORÍA] Registros iniciales: 5 | Duplicados eliminados: 2

Resultado consolidado (mayor minutaje retenido):
           jugador            equipo  minutos_jugados  kilometros_recorridos
0    Florian Wirtz  Bayer Leverkusen               90                   12.1
1            Pedri         Barcelona               90                   11.8
2  Jude Bellingham       Real Madrid               85                   11.2
```

## 8. Errores frecuentes y casos borde

1. **Olvidar ordenar antes de deduplicar con `keep='first'`:**
   * **Causa:** `drop_duplicates` depende ciegamente del orden físico actual de las filas. Si el DataFrame no está ordenado explícitamente por fecha o valor numérico antes de ejecutarlo, el registro retenido será arbitrario o dependiente de la base de datos de origen.
   * **Solución:** Ejecutar siempre `df.sort_values(...)` antes de `drop_duplicates`.

2. **Suposición errónea sobre valores nulos (`NaN`):**
   * **Comportamiento:** En Python nativo, `float("nan") == float("nan")` es `False`. Sin embargo, `drop_duplicates` agrupa los `NaN` en una única clave compartida. Si tres filas tienen `NaN` en la columna analizada por `subset`, solo una sobrevivirá.

3. **Uso de `inplace=True` y advertencias de *Copy-on-Write*:**
   * **Riesgo:** Ejecutar `df.drop_duplicates(inplace=True)` sobre un sub-DataFrame obtenido por filtrado genera inconsistencias internas y está formalmente desaconsejado en Pandas 2.x/3.0.
   * **Solución:** Reasignar explícitamente: `df = df.drop_duplicates(...)`.

4. **Descoordinación del índice numérico tras la eliminación:**
   * **Problema:** Si se conservan las filas 0, 2 y 5, intentar acceder con `df.loc[1]` lanzará un `KeyError`.
   * **Solución:** Emplear el parámetro nativo `ignore_index=True` o encadenar `.reset_index(drop=True)`.

## 9. Buenas prácticas y rendimiento

* **Vectorización y tabla Hash en C:** `drop_duplicates` está altamente optimizado en C. Jamás reemplaces este método por bucles `for` manuales o comparaciones con `apply()`, los cuales degradan el rendimiento a $O(N^2)$ en memoria Python.
* **Reducir `subset` a los tipos más compactos:** Si el DataFrame contiene decenas de columnas, pasar `subset=["id_jugador"]` es órdenes de magnitud más rápido que evaluar todas las columnas, ya que solo computa hashes sobre una única serie entera o categórica.
* **Optimización previa con tipos `category`:** Si la columna de deduplicación contiene cadenas de texto repetidas, convertirla a `category` previo al descarte reduce el cálculo a enteros subyacentes, acelerando el proceso en grandes volúmenes.

## 10. Métodos relacionados

* `DataFrame.duplicated` — Retorna una máscara booleana indicando cuáles filas son duplicadas sin eliminarlas.
* `DataFrame.sort_values` — Ordena las filas según criterios específicos antes de deduplicar.
* `DataFrame.reset_index` — Reconstruye el índice secuencial en caso de no usar `ignore_index=True`.

## 11. Referencias oficiales

* **Documentación oficial de la API:** [pandas.DataFrame.drop_duplicates](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html) (Consultado para Pandas 2.2).
* **Guía de usuario:** [Essential Basic Functionality - Duplicates](https://pandas.pydata.org/docs/user_guide/indexing.html#duplicate-data).
