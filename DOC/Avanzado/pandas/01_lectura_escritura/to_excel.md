# `DataFrame.to_excel`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.to_excel(
    excel_writer,
    sheet_name='Sheet1',
    na_rep='',
    float_format=None,
    columns=None,
    header=True,
    index=True,
    index_label=None,
    startrow=0,
    startcol=0,
    engine=None,
    merge_cells=True,
    inf_rep='inf',
    freeze_panes=None,
    storage_options=None
)
```

## 2. ¿Qué es?

Es un **método de instancia** de `pandas.DataFrame` que exporta el contenido tabular a un libro de Microsoft Excel (`.xlsx` o `.xls`) utilizando motores como `openpyxl`.

## 3. ¿Para qué sirve?

Permite generar reportes corporativos y entregables para usuarios de negocio que requieren visualizar, formatear o compartir planillas en Microsoft Office sin interactuar con código.

* **Equivalencia en SQL:** Generación automatizada de reportes exportables a hojas de cálculo.

## 4. ¿Cómo funciona?

1. **Estructura XML:** Escribe una celda a la vez en las tablas internas del archivo OpenXML `.xlsx`.
2. **Coordenadas de inserción:** Permite desplazar la tabla dentro de la hoja especificando `startrow` y `startcol`.
3. **Escritura única vs compuesta:** Si se pasa una ruta de archivo, crea el archivo y lo cierra; si se pasa una instancia de `pandas.ExcelWriter`, permite añadir múltiples DataFrames en distintas pestañas o rangos antes de persistir.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `excel_writer` | `str`, `Path`, `ExcelWriter` | Obligatorio | Posicional | Ruta al archivo `.xlsx` o instancia activa de `ExcelWriter`. |
| `sheet_name` | `str` | Opcional | `'Sheet1'` | Nombre asignado a la pestaña de la hoja de cálculo. |
| `na_rep` | `str` | Opcional | `''` | Texto representativo para valores faltantes. |
| `index` | `bool` | Opcional | `True` | Escribe el índice de filas como primera columna. |
| `startrow` / `startcol` | `int` | Opcional | `0` | Fila o columna de inicio base cero dentro de la hoja. |
| `engine` | `str` | Opcional | `None` | Motor de escritura (`'openpyxl'`). |
| `freeze_panes` | `tuple[int, int]` | Opcional | `None` | Tupla `(fila, columna)` para inmovilizar paneles en Excel. |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la definición formal (`sheet_name`, `freeze_panes`). El **argumento** es el valor suministrado (`sheet_name="Goleadores"`, `freeze_panes=(1, 0)`).

## 6. Retorno

* **Tipo devuelto:** `None`.
* **Mutabilidad:** Crea o modifica el archivo externo en disco/buffer; no muta el DataFrame.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Exportación directa a un archivo Excel:

```python
import io
import pandas as pd

df_plantilla = pd.DataFrame({
    "jugador": ["Luka Modric", "Toni Kroos"],
    "asistencias": [8, 10]
})

buffer = io.BytesIO()
df_plantilla.to_excel(buffer, index=False, engine="openpyxl")
print(f"Exportación exitosa. Tamaño: {len(buffer.getvalue())} bytes.")
```

**Salida real:**

```text
Exportación exitosa. Tamaño: 5020 bytes.
```

---

### Nivel 2: Intermedio

Exportación desplazada con paneles inmovilizados:

```python
import io
import pandas as pd

df_equipo = pd.DataFrame({
    "jugador": ["Fede Valverde", "Eduardo Camavinga"],
    "kilometros": [11.5, 10.8]
})

buffer = io.BytesIO()
df_equipo.to_excel(
    buffer,
    sheet_name="Metricas",
    startrow=2,
    startcol=1,
    freeze_panes=(3, 0),
    index=False,
    engine="openpyxl"
)
print("Archivo generado con paneles inmovilizados y desplazamiento.")
```

**Salida real:**

```text
Archivo generado con paneles inmovilizados y desplazamiento.
```

---

### Nivel 3: Avanzado

Consolidación multioja en un único archivo mediante `ExcelWriter`:

```python
import io
import pandas as pd

df_delanteros = pd.DataFrame({"jugador": ["Vinicius Jr", "Rodrygo"], "goles": [21, 15]})
df_defensas = pd.DataFrame({"jugador": ["Rudiger", "Militao"], "despejes": [85, 60]})

buffer_final = io.BytesIO()
with pd.ExcelWriter(buffer_final, engine="openpyxl") as writer:
    df_delanteros.to_excel(writer, sheet_name="Delanteros", index=False)
    df_defensas.to_excel(writer, sheet_name="Defensas", index=False)

print(f"Libro consolidado con múltiples hojas generado exitosamente.")
```

**Salida real:**

```text
Libro consolidado con múltiples hojas generado exitosamente.
```

## 8. Errores frecuentes y casos borde

1. **Olvidar instalar `openpyxl`:** Lanza `ModuleNotFoundError: No module named 'openpyxl'`.
2. **Sobrescritura involuntaria:** Escribir dos veces a la misma ruta sin `ExcelWriter(mode='a')` destruye las hojas anteriores.

## 9. Buenas prácticas y rendimiento

* **Evitar exportar índices innecesarios:** Usar siempre `index=False` para generar tablas limpias.
* **Escritura agrupada:** Siempre que se generen varias hojas, utilizar la sentencia `with pd.ExcelWriter(...) as writer:`.

## 10. Métodos relacionados

* [read_excel](read_excel.md) — Carga de libros Excel.
* [to_csv](to_csv.md) — Exportación más ligera a CSV.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.to_excel](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html) (Pandas 2.2).
