# `pandas.to_numeric`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.to_numeric(
    arg,
    errors='raise',
    downcast=None,
    dtype_backend=_NoDefault.no_default
)
```

## 2. ¿Qué es?

Es una **función constructora utilitaria** de Pandas que parsea secuencias escalares o Series de texto o tipos mixtos convirtiéndolas a números flotantes o enteros, con manejo seguro de valores corruptos.

## 3. ¿Para qué sirve?

Resuelve la limpieza de columnas donde valores numéricos válidos vienen mezclados con caracteres extraños (`'12.5'`, `'SIN_DATO'`, `'N/A'`) mediante el argumento `errors='coerce'`.

## 4. ¿Cómo funciona?

1. **Coerción:** Si `errors='coerce'`, cualquier valor que falle la conversión a número se reemplaza automáticamente por `NaN`. Con `downcast`, comprime el tipo resultante al entero o flotante más pequeño posible (`int8`, `float32`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `arg` | `Series`, lista, escalar | Obligatorio | Posicional | Objeto a transformar a número. |
| `errors` | `{'raise', 'coerce', 'ignore'}` | Opcional | `'raise'` | `'coerce'` reemplaza errores por `NaN`. |
| `downcast` | `{'integer', 'signed', 'unsigned', 'float'}` | Opcional | `None` | Comprime al subtipo más pequeño posible. |

## 6. Retorno

* `pandas.Series` numérico o escalar.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

s = pd.Series(["10", "25", "30.5"])
print(pd.to_numeric(s))
```

**Salida real:**

```text
0    10.0
1    25.0
2    30.5
dtype: float64
```

---

### Nivel 2: Intermedio

Coerción defensiva de texto inválido a `NaN`:

```python
import pandas as pd

goles_corruptos = pd.Series(["15", "N/A", "22", "DESCONOCIDO"])
goles_limpios = pd.to_numeric(goles_corruptos, errors="coerce")
print(goles_limpios)
```

**Salida real:**

```text
0    15.0
1     NaN
2    22.0
3     NaN
dtype: float64
```

---

### Nivel 3: Avanzado

Conversión con downcasting automático de memoria para microservicios:

```python
import pandas as pd

edades = pd.Series(["18", "21", "25", "32"])
edades_comprimidas = pd.to_numeric(edades, downcast="integer")
print("Tipo final optimizado:", edades_comprimidas.dtype)
```

**Salida real:**

```text
Tipo final optimizado: int8
```

## 8. Errores frecuentes y casos borde

1. Usar `errors='ignore'` (obsoleto): Deja los datos en `object` silenciosamente. Preferir siempre `'coerce'`.

## 9. Buenas prácticas y rendimiento

* Siempre utilizar `to_numeric(..., errors='coerce')` tras ingesta de fuentes externas no verificadas.

## 10. Métodos relacionados

* [astype](astype.md) — Conversión general.
* [fillna](fillna.md) — Relleno de los `NaN` generados tras coerción.

## 11. Referencias oficiales

* **API Reference:** [pandas.to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html) (Pandas 2.2).
