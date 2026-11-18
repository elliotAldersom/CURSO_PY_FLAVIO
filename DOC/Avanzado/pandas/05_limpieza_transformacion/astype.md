# `DataFrame.astype` y `Series.astype`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.astype(dtype, copy=None, errors='raise')
```

## 2. ¿Qué es?

Es un **método de conversión de tipos de datos** (fundición / *casting*) que transforma la representación física de las columnas a un tipo compatible de NumPy, Pandas o PyArrow.

## 3. ¿Para qué sirve?

Optimiza memoria (p. ej. `int64` a `int16`, `object` a `category`) y prepara columnas para operaciones matemáticas o relacionales que exigen tipos homogéneos.

* **Equivalencia en SQL:** `CAST(columna AS tipo)`.

## 4. ¿Cómo funciona?

1. **Conversión en bloque:** Delega en el método `astype` del arreglo de NumPy o motor de extensión de Pandas, relocalizando memoria cuando es necesario.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `dtype` | tipo, `dict` | Obligatorio | Posicional | Tipo objetivo (o diccionario `{col: tipo}`). |
| `errors` | `{'raise', 'ignore'}` | Opcional | `'raise'` | Si es `'raise'`, lanza error ante conversiones inválidas. |

## 6. Retorno

* `pandas.DataFrame` o `Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

s = pd.Series(["10", "20", "30"])
s_int = s.astype("int32")
print(s_int)
print("Tipo:", s_int.dtype)
```

**Salida real:**

```text
0    10
1    20
2    30
dtype: int32
Tipo: int32
```

---

### Nivel 2: Intermedio

Conversión masiva mediante diccionario y optimización categórica:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Rodrygo"],
    "goles": ["21", "15"],
    "equipo": ["Real Madrid", "Real Madrid"]
})

df_optimizado = df.astype({
    "goles": "int16",
    "equipo": "category"
})
print(df_optimizado.dtypes)
```

**Salida real:**

```text
jugador      object
goles         int16
equipo     category
dtype: object
```

---

### Nivel 3: Avanzado

Auditoría de reducción real de memoria profunda (*deep memory*):

```python
import pandas as pd

equipos = pd.Series(["Real Madrid"] * 1000)
memoria_previa = equipos.memory_usage(deep=True)

equipos_cat = equipos.astype("category")
memoria_posterior = equipos_cat.memory_usage(deep=True)

reduccion_pct = round((1 - memoria_posterior / memoria_previa) * 100, 1)
print(f"Memoria previa: {memoria_previa} B | Posterior: {memoria_posterior} B | Ahorro: {reduccion_pct}%")
```

**Salida real:**

```text
Memoria previa: 75032 B | Posterior: 2064 B | Ahorro: 97.2%
```

## 8. Errores frecuentes y casos borde

1. Intentar convertir `'int64'` una columna con strings mezclados o nulos: Lanza `ValueError: invalid literal for int()`. **Solución:** Usar `pd.to_numeric(..., errors='coerce')`.

## 9. Buenas prácticas y rendimiento

* Convertir a `category` cualquier columna de texto repetitivo antes de agregaciones o merge.

## 10. Métodos relacionados

* [to_numeric](to_numeric.md) — Conversión segura con manejo de errores no numéricos.
* [dtypes](../02_inspeccion_exploracion/dtypes.md) — Inspección de tipos.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.astype](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html) (Pandas 2.2).
