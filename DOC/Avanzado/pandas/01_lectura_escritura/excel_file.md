# `pandas.ExcelFile` y `ExcelFile.sheet_names`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
class pandas.ExcelFile(
    path_or_buffer,
    engine=None,
    storage_options=None,
    engine_kwargs=None
)

# Propiedad de la clase:
ExcelFile.sheet_names -> list[str]
```

## 2. ¿Qué es?

Es una **clase contenedora** del módulo `pandas` que mantiene abierto el descriptor de un archivo Excel, permitiendo inspeccionar metadatos como los nombres de las hojas (`.sheet_names`) y analizar múltiples pestañas sin descomprimir ni reabrir el archivo repetidamente.

## 3. ¿Para qué sirve?

Optimiza la ingesta cuando un libro Excel contiene muchas hojas y se requiere validar su estructura antes de cargarlas, evitando la sobrecarga de `pd.read_excel()` que reabre y descomprime el paquete ZIP en cada llamada.

* **Equivalencia en SQL:** Equivale a consultar vistas de esquema del catálogo `INFORMATION_SCHEMA.TABLES`.

## 4. ¿Cómo funciona?

1. **Apertura persistente:** Carga una única vez la estructura XML del libro y mantiene la referencia en el motor (`openpyxl`).
2. **Propiedad `.sheet_names`:** Devuelve una lista de cadenas con los nombres de todas las hojas de cálculo disponibles en el orden exacto del libro.
3. **Método `.parse()`:** Permite extraer hojas individuales recibiendo exactamente los mismos argumentos que `read_excel`.
4. **Context Manager:** Implementa el protocolo `__enter__` y `__exit__` para garantizar el cierre determinista del descriptor de archivo.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `path_or_buffer` | `str`, `Path`, bytes | Obligatorio | Posicional | Ruta al archivo Excel o flujo en memoria. |
| `engine` | `str` | Opcional | `None` | Motor subyacente (`'openpyxl'`, `'calamine'`, etc.). |
| `storage_options` | `dict` | Opcional | `None` | Parámetros para almacenamiento remoto (S3, GCS). |

> [!NOTE] Diferencia entre parámetro y argumento
> El **parámetro** es la variable declarada en el constructor (`path_or_buffer`). El **argumento** es la referencia concreta pasada al instanciar (`path_or_buffer=ruta_archivo`).

## 6. Retorno

* **Constructor `ExcelFile(...)`:** Objeto de clase `pandas.ExcelFile`.
* **Propiedad `.sheet_names`:** `list[str]` con los nombres de las hojas.
* **Método `.parse(...)`:** `pandas.DataFrame` correspondiente a la hoja parseada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Inspección de nombres de hojas con `.sheet_names`:

```python
import io
import pandas as pd

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame({"a": [1]}).to_excel(writer, sheet_name="Defensa", index=False)
    pd.DataFrame({"b": [2]}).to_excel(writer, sheet_name="Ataque", index=False)
buffer.seek(0)

# Uso con gestor de contexto
with pd.ExcelFile(buffer, engine="openpyxl") as xls:
    hojas = xls.sheet_names
    print("Hojas disponibles:", hojas)
```

**Salida real:**

```text
Hojas disponibles: ['Defensa', 'Ataque']
```

---

### Nivel 2: Intermedio

Lectura selectiva con `.parse()` según condiciones del nombre de hoja:

```python
import io
import pandas as pd

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame({"jugador": ["Lautaro Martínez"], "goles": [24]}).to_excel(writer, sheet_name="2023_SerieA", index=False)
    pd.DataFrame({"jugador": ["Lautaro Martínez"], "goles": [27]}).to_excel(writer, sheet_name="2024_SerieA", index=False)
    pd.DataFrame({"datos": [0]}).to_excel(writer, sheet_name="Notas_Internas", index=False)
buffer.seek(0)

with pd.ExcelFile(buffer, engine="openpyxl") as xls:
    hojas_serie_a = [h for h in xls.sheet_names if "SerieA" in h]
    df_serie_a = pd.concat([xls.parse(h) for h in hojas_serie_a], ignore_index=True)

print(df_serie_a)
```

**Salida real:**

```text
            jugador  goles
0  Lautaro Martínez     24
1  Lautaro Martínez     27
```

---

### Nivel 3: Avanzado

Auditoría defensiva de esquemas multioja sin reabrir el archivo físico:

```python
import io
import pandas as pd

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    pd.DataFrame({"jugador": ["Kimmich"], "pases": [95]}).to_excel(writer, sheet_name="Mediocampo", index=False)
    pd.DataFrame({"jugador": ["Alisson"], "atajadas": [12]}).to_excel(writer, sheet_name="Porteria", index=False)
buffer.seek(0)

esquemas = {}
with pd.ExcelFile(buffer, engine="openpyxl") as xls:
    for hoja in xls.sheet_names:
        # Carga solo 0 filas para obtener la metadata de nombres de columna
        df_meta = xls.parse(hoja, nrows=0)
        esquemas[hoja] = list(df_meta.columns)

for hoja, columnas in esquemas.items():
    print(f"Hoja: {hoja} -> Columnas: {columnas}")
```

**Salida real:**

```text
Hoja: Mediocampo -> Columnas: ['jugador', 'pases']
Hoja: Porteria -> Columnas: ['jugador', 'atajadas']
```

## 8. Errores frecuentes y casos borde

1. **No cerrar el objeto `ExcelFile`:** Dejar el archivo abierto puede bloquear descriptores en sistemas Windows. **Solución:** Utilizar siempre la sentencia `with pd.ExcelFile(...) as xls:`.
2. **Reabrir el archivo con `read_excel` en bucles:** Ineficiencia severa que multiplica por $N$ el tiempo de ejecución.

## 9. Buenas prácticas y rendimiento

* **Reutilización del descriptor:** Si tenés que leer más de una pestaña del mismo `.xlsx`, `ExcelFile` es mandatorio en lugar de múltiples `pd.read_excel`.

## 10. Métodos relacionados

* [read_excel](read_excel.md) — Lectura directa de hojas individuales.
* [to_excel](to_excel.md) — Escritura y exportación a Excel.

## 11. Referencias oficiales

* **API Reference:** [pandas.ExcelFile](https://pandas.pydata.org/docs/reference/api/pandas.ExcelFile.html) (Pandas 2.2).
