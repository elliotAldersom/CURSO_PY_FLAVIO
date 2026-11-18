# `DataFrame.info`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.info(
    verbose=None,
    buf=None,
    max_cols=None,
    memory_usage=None,
    show_counts=None
)
```

## 2. ¿Qué es?

Es un **método de diagnóstico de instancia** que imprime un resumen exhaustivo de la estructura interna del DataFrame: índice, cantidad de columnas, conteo de valores no nulos por columna, tipos de datos físicos (`dtypes`) y consumo aproximado o exacto de memoria RAM.

## 3. ¿Para qué sirve?

Es la primera herramienta de auditoría técnica que debe ejecutarse tras cargar cualquier dataset para detectar de inmediato valores faltantes, tipos `object` indeseados y cuellos de botella de memoria.

* **Equivalencia en SQL:** Equivale al comando `DESCRIBE tabla` o `\d+ tabla` en PostgreSQL.

## 4. ¿Cómo funciona?

1. **Inspección de bloques:** Analiza la colección de columnas (`BlockManager` de Pandas) evaluando el tipo `dtype` de cada una.
2. **Cálculo de valores no nulos:** Cuenta cuántos elementos distintos de `NaN`/`None` existen fila a fila.
3. **Cálculo de memoria:** Con `memory_usage="deep"`, recorre los punteros en memoria de los strings para medir el tamaño real en bytes del montículo de Python.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `verbose` | `bool` | Opcional | `None` | Si es `True`, lista cada columna individual con su conteo y tipo. |
| `buf` | flujo de texto | Opcional | `sys.stdout` | Destino donde escribir la salida (archivo, buffer, stdout). |
| `memory_usage` | `bool`, `'deep'` | Opcional | `None` | Si es `'deep'`, calcula el consumo de memoria real inspeccionando objetos en C. |
| `show_counts` | `bool` | Opcional | `None` | Fuerza mostrar el conteo de elementos no nulos. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición formal (`memory_usage`). El **argumento** es el valor pasado (`memory_usage="deep"`).

## 6. Retorno

* **Tipo devuelto:** `None` (su objetivo principal es la impresión o escritura en buffer).
* **Mutabilidad:** No altera el DataFrame.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Diagnóstico estándar en consola:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "jugador": ["Lionel Messi", "Kylian Mbappé"],
    "goles": [25, 28],
    "salario": [20.5, 30.0]
})

df_liga.info()
```

**Salida real:**

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 3 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   jugador  2 non-null      object 
 1   goles    2 non-null      int64  
 2   salario  2 non-null      float64
dtypes: float64(1), int64(1), object(1)
memory usage: 180.0 bytes
```

---

### Nivel 2: Intermedio

Captura de la salida de `info()` en un buffer de memoria con cálculo profundo de RAM:

```python
import io
import pandas as pd

df_jugadores = pd.DataFrame({
    "jugador": ["Erling Haaland" * 100],
    "asistencias": [10]
})

buffer = io.StringIO()
df_jugadores.info(buf=buffer, memory_usage="deep")
resumen = buffer.getvalue()
print("Salida capturada en buffer:")
print(resumen.splitlines()[0])
print(resumen.splitlines()[-1])
```

**Salida real:**

```text
Salida capturada en buffer:
<class 'pandas.core.frame.DataFrame'>
memory usage: 1.5 KB
```

---

### Nivel 3: Avanzado

Pipeline de auditoría automatizado para pipelines CI/CD:

```python
import io
import pandas as pd

def auditar_calidad_dataframe(df: pd.DataFrame) -> bool:
    buf = io.StringIO()
    df.info(buf=buf, show_counts=True)
    salida = buf.getvalue()
    
    # Validamos que no existan columnas con 0 elementos no nulos
    tiene_columnas_vacias = " 0 non-null " in salida
    print(f"[AUDITORÍA] Dataset auditado con éxito. Columnas vacías: {tiene_columnas_vacias}")
    return not tiene_columnas_vacias

df_muestra = pd.DataFrame({"jugador": ["Rodri"], "goles": [8]})
auditar_calidad_dataframe(df_muestra)
```

**Salida real:**

```text
[AUDITORÍA] Dataset auditado con éxito. Columnas vacías: False
```

## 8. Errores frecuentes y casos borde

1. **Asumir que retorna un string:** Intentar hacer `texto = df.info()` devuelve `None`. **Solución:** Pasar `buf=io.StringIO()`.
2. **Subestimación de memoria sin `'deep'`:** En columnas de strings, el reporte por defecto solo mide los punteros de 8 bytes, ignorando los megabytes de texto real en el heap.

## 9. Buenas prácticas y rendimiento

* Pasar siempre `memory_usage="deep"` cuando se evalúa la optimización de memoria.

## 10. Métodos relacionados

* [describe](describe.md) — Estadísticos descriptivos numéricos.
* [dtypes](dtypes.md) — Atributo con la serie de tipos por columna.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.info](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html) (Pandas 2.2).
