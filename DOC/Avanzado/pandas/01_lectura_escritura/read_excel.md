# `pandas.read_excel`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.read_excel(
    io,
    sheet_name=0,
    *,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_format=None,
    thousands=None,
    decimal='.',
    comment=None,
    skipfooter=0,
    storage_options=None,
    dtype_backend=_NoDefault.no_default
)
```

## 2. ¿Qué es?

Es una **función constructora** del módulo `pandas` que analiza hojas de cálculo de Microsoft Excel (`.xlsx`, `.xls`, `.xlsm`, `.xlsb`, `.ods`) utilizando motores subyacentes como `openpyxl` o `calamine` y las convierte en un `DataFrame` o diccionario de DataFrames.

## 3. ¿Para qué sirve?

Permite integrar planillas empresariales y reportes contables directamente en entornos analíticos de Python, soportando selección de hojas por índice o nombre, lectura multioja y extracción de rangos celulares.

* **Equivalencia en SQL:** Equivale a una ingesta ETL desde hojas de cálculo o una carga externa `OPENROWSET('Microsoft.ACE.OLEDB.12.0', ...)`.

## 4. ¿Cómo funciona?

1. **Descompresión y análisis XML:** Un archivo `.xlsx` es un contenedor ZIP de archivos XML. Pandas delega la lectura en un motor (predeterminadamente `openpyxl`).
2. **Resolución de `sheet_name`:** Si se pasa un entero (`0`), lee la primera hoja; si se pasa un string (`"Ventas"`), busca la hoja con ese nombre exacto; si se pasa `None`, carga **todas** las hojas en un `dict[str, DataFrame]`.
3. **Conversión columnar:** Transfiere celdas tipadas de Excel (enteros, flotantes, fechas nativas) a columnas de NumPy/Pandas.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `io` | `str`, `Path`, bytes | Obligatorio | Posicional | Ruta al archivo Excel, URL o flujo de bytes. |
| `sheet_name` | `str`, `int`, `list`, `None` | Opcional | `0` | Hoja o lista de hojas a cargar. Si es `None`, devuelve un diccionario de DataFrames. |
| `header` | `int`, `list[int]`, `None` | Opcional | `0` | Fila base cero utilizada como encabezados de columna. |
| `usecols` | `str`, `list`, `callable` | Opcional | `None` | Columnas a leer, admitiendo rango de letras de Excel (p. ej. `'A:C'`) o nombres de columna. |
| `dtype` | `dict`, tipo | Opcional | `None` | Diccionario de tipos de datos para forzar en columnas específicas. |
| `engine` | `{'openpyxl', 'calamine', 'odf', 'pyxlsb', 'xlrd'}` | Opcional | `None` | Motor explícito de lectura. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición del argumento esperado en la firma (`sheet_name`, `engine`). El **argumento** es el valor específico utilizado al invocarla (`sheet_name="Jugadores"`, `engine="openpyxl"`).

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` o `dict[str, pandas.DataFrame]` (si se especifican múltiples hojas o `sheet_name=None`).
* **Mutabilidad:** Retorna **nuevas estructuras** en memoria.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Lectura directa de una hoja de cálculo desde un archivo de muestra:

```python
import io
import pandas as pd

# Creación de archivo Excel en memoria para garantizar reproducibilidad
buffer = io.BytesIO()
df_muestra = pd.DataFrame({
    "jugador": ["Lionel Messi", "Cristiano Ronaldo"],
    "goles": [830, 890]
})
df_muestra.to_excel(buffer, index=False, engine="openpyxl")
buffer.seek(0)

# Lectura con read_excel
df_leido = pd.read_excel(buffer, engine="openpyxl")
print(df_leido)
```

**Salida real:**

```text
             jugador  goles
0       Lionel Messi    830
1  Cristiano Ronaldo    890
```

---

### Nivel 2: Intermedio

Lectura con selección de columnas por letras de Excel y nombres tipados:

```python
import io
import pandas as pd

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame({
        "id": [1, 2, 3],
        "jugador": ["Kylian Mbappé", "Erling Haaland", "Vinicius Jr"],
        "minutos": [2450, 2600, 2100]
    }).to_excel(writer, sheet_name="Estadisticas", index=False)
buffer.seek(0)

df_intermedio = pd.read_excel(
    buffer,
    sheet_name="Estadisticas",
    usecols=["jugador", "minutos"],
    dtype={"jugador": "string", "minutos": "int32"},
    engine="openpyxl"
)
print(df_intermedio)
```

**Salida real:**

```text
          jugador  minutos
0   Kylian Mbappé     2450
1  Erling Haaland     2600
2     Vinicius Jr     2100
```

---

### Nivel 3: Avanzado

Carga masiva multioja simultánea con consolidación funcional:

```python
import io
import pandas as pd

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame({"jugador": ["Pedri"], "equipo": ["Barcelona"]}).to_excel(writer, sheet_name="Liga_Espana", index=False)
    pd.DataFrame({"jugador": ["Rodri"], "equipo": ["Man City"]}).to_excel(writer, sheet_name="Premier_League", index=False)
buffer.seek(0)

# sheet_name=None retorna un dict: {nombre_hoja: DataFrame}
hojas_dict = pd.read_excel(buffer, sheet_name=None, engine="openpyxl")

# Consolidamos asignando el origen de la hoja
df_consolidado = pd.concat(
    [df.assign(liga=nombre) for nombre, df in hojas_dict.items()],
    ignore_index=True
)
print(df_consolidado)
```

**Salida real:**

```text
  jugador     equipo            liga
0   Pedri  Barcelona     Liga_Espana
1   Rodri   Man City  Premier_League
```

## 8. Errores frecuentes y casos borde

1. **`ValueError: Worksheet named ... not found`:** El nombre de la hoja no coincide exactamente con el texto de la pestaña (incluyendo espacios invisibles al inicio o final).
2. **Columnas de códigos numéricos convertidas a float:** Códigos postales o identificadores como `"0123"` se interpretan como enteros perdiendo el cero a la izquierda. **Solución:** pasar `dtype={'codigo': str}`.

## 9. Buenas prácticas y rendimiento

* **Rendimiento con Calamine:** Para archivos Excel gigantescos, instalar `python-calamine` y pasar `engine='calamine'` acelera la ingesta entre 3x y 10x respecto a `openpyxl`.
* **Evitar Excel para Big Data:** Excel tiene un límite físico de 1.048.576 filas y sobrecosto XML. En producción masiva debe preferirse Parquet o CSV.

## 10. Métodos relacionados

* [read_csv](read_csv.md) — Lectura de archivos planos delimitados.
* [to_excel](to_excel.md) — Exportación de DataFrames a libros Excel.
* [excel_file](excel_file.md) — Inspección de metadatos y lectura múltiple eficiente sin reabrir el archivo.

## 11. Referencias oficiales

* **API Reference:** [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) (Pandas 2.2).
* **Guía de usuario:** [Reading Excel Files](https://pandas.pydata.org/docs/user_guide/io.html#excel-files).
