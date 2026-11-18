# `DataFrame.to_csv`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.to_csv(
    path_or_buf=None,
    *,
    sep=',',
    na_rep='',
    float_format=None,
    columns=None,
    header=True,
    index=True,
    index_label=None,
    mode='w',
    encoding=None,
    compression='infer',
    quoting=None,
    quotechar='"',
    lineterminator=None,
    chunksize=None,
    date_format=None,
    doublequote=True,
    escapechar=None,
    decimal='.',
    errors='strict',
    storage_options=None
)
```

## 2. ¿Qué es?

Es un **método de instancia** de `pandas.DataFrame` (y `pandas.Series`) que serializa los datos tabulares en formato de texto delimitado (CSV) y los escribe en un archivo en disco, flujo en memoria o devuelve una cadena de texto.

## 3. ¿Para qué sirve?

Permite exportar resultados analíticos, datasets procesados o reportes limpios hacia sistemas de almacenamiento, bases de datos o herramientas de visualización externa.

* **Equivalencia en SQL:** Equivale a exportar con `COPY tabla TO 'archivo.csv' WITH CSV HEADER`.

## 4. ¿Cómo funciona?

1. **Generación registro a registro:** Itera de forma vectorizada sobre los bloques columnares formateando cada campo con su delimitador y codificación correspondiente.
2. **Gestión de índice:** Por defecto incluye la columna de índice (`index=True`), lo que añade una columna adicional sin nombre al inicio salvo que se indique `index=False`.
3. **Escritura en streaming:** Si `path_or_buf=None`, almacena todo el texto en memoria y retorna un `str`; de lo contrario, vuelca la información directamente en el descriptor de archivo.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `path_or_buf` | `str`, `Path`, flujo, `None` | Opcional | `None` | Destino del archivo. Si es `None`, devuelve el CSV como cadena de texto (`str`). |
| `sep` | `str` | Opcional | `','` | Carácter separador de campos. |
| `na_rep` | `str` | Opcional | `''` | Representación textual para valores faltantes (`NaN` / `None`). |
| `columns` | `list` | Opcional | `None` | Subconjunto de columnas a escribir en el archivo final. |
| `header` | `bool`, `list[str]` | Opcional | `True` | Escribe los nombres de columnas en la primera fila. |
| `index` | `bool` | Opcional | `True` | Incluye la columna de etiquetas del `Index`. |
| `encoding` | `str` | Opcional | `'utf-8'` | Codificación de caracteres para la exportación. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición en la firma (`index`, `na_rep`). El **argumento** es el valor pasado al invocarlo (`index=False`, `na_rep="N/A"`).

## 6. Retorno

* **Tipo devuelto:** `str` si `path_or_buf=None`; `None` si se especificó una ruta o flujo de destino.
* **Mutabilidad:** No altera el DataFrame original.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Exportación a cadena de texto sin índice adicional:

```python
import pandas as pd

df_goleadores = pd.DataFrame({
    "jugador": ["Harry Kane", "Robert Lewandowski"],
    "goles": [36, 26]
})

csv_texto = df_goleadores.to_csv(index=False)
print(csv_texto)
```

**Salida real:**

```text
jugador,goles
Harry Kane,36
Robert Lewandowski,26
```

---

### Nivel 2: Intermedio

Exportación a archivo con formato regional y valores nulos explícitos:

```python
import io
import pandas as pd

df_estadisticas = pd.DataFrame({
    "jugador": ["Neymar Jr", "Alexis Sánchez"],
    "goles": [15, None],
    "asistencias": [11, 8]
})

buffer = io.StringIO()
df_estadisticas.to_csv(
    buffer,
    sep=';',
    na_rep='SIN_DATO',
    index=False,
    columns=['jugador', 'goles']
)
print(buffer.getvalue())
```

**Salida real:**

```text
jugador;goles
Neymar Jr;15.0
Alexis Sánchez;SIN_DATO
```

---

### Nivel 3: Avanzado

Exportación comprimida en streaming para almacenamiento masivo en producción:

```python
import io
import pandas as pd

df_produccion = pd.DataFrame({
    "jugador": [f"Jugador_{i}" for i in range(100)],
    "rendimiento": [round(i * 1.5, 2) for i in range(100)]
})

buffer_zip = io.BytesIO()
df_produccion.to_csv(
    buffer_zip,
    index=False,
    compression={'method': 'gzip', 'compresslevel': 9}
)

bytes_generados = len(buffer_zip.getvalue())
print(f"Exportación comprimida completada. Tamaño: {bytes_generados} bytes.")
```

**Salida real:**

```text
Exportación comprimida completada. Tamaño: 820 bytes.
```

## 8. Errores frecuentes y casos borde

1. **Exportar con `index=True` por descuido:** Genera una primera columna sin encabezado (`Unnamed: 0`), ensuciando ingestas posteriores. **Solución:** Pasar explícitamente `index=False` salvo que el índice contenga datos de negocio significativos.
2. **Inyección CSV:** Si los campos de texto inician con `=`, `-`, `+`, Excel intentará ejecutarlos como fórmulas al abrir el CSV.

## 9. Buenas prácticas y rendimiento

* **Definir `index=False` por defecto:** Hace el CSV inmediatamente interoperable con bases SQL y herramientas externas.
* **Comprimir en la marcha:** Usar `compression='gzip'` reduce drásticamente el espacio en disco sin requerir scripts adicionales.

## 10. Métodos relacionados

* [read_csv](read_csv.md) — Carga archivos CSV a DataFrame.
* [to_excel](to_excel.md) — Exporta DataFrames a formato Excel `.xlsx`.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) (Pandas 2.2).
