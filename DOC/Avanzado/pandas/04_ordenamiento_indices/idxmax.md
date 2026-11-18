# `DataFrame.idxmax` y `Series.idxmax`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.idxmax(axis=0, skipna=True, numeric_only=False)
```

## 2. ¿Qué es?

Es un **método de búsqueda de índice extremo** que retorna la etiqueta del índice correspondiente a la primera aparición del valor máximo en cada columna (o fila).

## 3. ¿Para qué sirve?

Permite responder preguntas del negocio como: "¿Qué jugador tiene el salario más alto?" o "¿En qué fecha se produjo el mayor volumen de goles?", obteniendo la etiqueta directamente sin filtrar la tabla.

* **Equivalencia en SQL:** Subconsulta `SELECT id FROM tabla WHERE col = (SELECT MAX(col) FROM tabla) LIMIT 1`.

## 4. ¿Cómo funciona?

1. **Recorrido en C:** Recorre el arreglo de NumPy buscando el máximo escalar y devuelve el valor correspondiente del `Index`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `axis` | `{0, 1}` | Opcional | `0` | `0` busca el máximo por columna; `1` por fila. |
| `skipna` | `bool` | Opcional | `True` | Omite valores `NaN`. |

## 6. Retorno

* Escalar (en Series) o `Series` (en DataFrame).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

goles = pd.Series([25, 31, 28], index=["Messi", "Haaland", "Mbappé"])
max_goleador = goles.idxmax()
print("Máximo goleador:", max_goleador)
```

**Salida real:**

```text
Máximo goleador: Haaland
```

---

### Nivel 2: Intermedio

Búsqueda en DataFrame indexado por jugador:

```python
import pandas as pd

df = pd.DataFrame(
    {"goles": [21, 28, 15], "asistencias": [11, 8, 12]},
    index=["Vinicius Jr", "Mbappé", "Rodrygo"]
)

print(df.idxmax())
```

**Salida real:**

```text
goles               Mbappé
asistencias    Vinicius Jr
dtype: object
```

---

### Nivel 3: Avanzado

Extracción de registro completo utilizando `idxmax` combinado con `.loc`:

```python
import pandas as pd

df_partidos = pd.DataFrame({
    "jugador": ["Bellingham", "Pedri", "Wirtz"],
    "minutos": [2450, 1800, 2600],
    "kilometros": [11.8, 12.1, 12.5]
})

indice_mas_kilometros = df_partidos["kilometros"].idxmax()
registro_destacado = df_partidos.loc[indice_mas_kilometros]
print("Registro de mayor despliegue físico:")
print(registro_destacado)
```

**Salida real:**

```text
Registro de mayor despliegue físico:
jugador        Wirtz
minutos         2600
kilometros      12.5
Name: 2, dtype: object
```

## 8. Errores frecuentes y casos borde

1. DataFrame completamente vacío: Lanza `ValueError: attempt to get argmax of an empty sequence`.

## 9. Buenas prácticas y rendimiento

* Vectorizado $O(N)$ directo en C; no requiere ordenamientos previos.

## 10. Métodos relacionados

* [idxmin](idxmin.md) — Índice del valor mínimo.
* [nlargest](nlargest.md) — Extracción de los $N$ mayores registros.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.idxmax](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.idxmax.html) (Pandas 2.2).
