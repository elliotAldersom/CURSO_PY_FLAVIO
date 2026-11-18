# `DataFrame.sample`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.sample(
    n=None,
    frac=None,
    replace=False,
    weights=None,
    random_state=None,
    axis=None,
    ignore_index=False
)
```

## 2. ¿Qué es?

Es un **método de instancia** que extrae una muestra aleatoria de filas (o columnas) de un DataFrame o Series.

## 3. ¿Para qué sirve?

Permite auditar datos sin el sesgo del orden inicial (`head`) o final (`tail`), crear particiones de prueba para modelado y realizar remuestreo (*bootstrap*).

* **Equivalencia en SQL:** Equivale a `SELECT * FROM tabla ORDER BY RANDOM() LIMIT n`.

## 4. ¿Cómo funciona?

1. **Generador pseudoaleatorio:** Emplea internamente el generador de NumPy o una semilla (`random_state`) para seleccionar índices de forma equiprobable o ponderada (`weights`).

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `n` | `int` | Opcional | `None` | Número exacto de elementos a extraer. Mutuamente excluyente con `frac`. |
| `frac` | `float` | Opcional | `None` | Proporción de elementos a extraer (p. ej. `0.2` para el 20%). |
| `replace` | `bool` | Opcional | `False` | Muestreo con reemplazo (permite seleccionar la misma fila más de una vez). |
| `random_state` | `int`, generador | Opcional | `None` | Semilla determinista para garantizar reproducibilidad exacta. |
| `ignore_index` | `bool` | Opcional | `False` | Si es `True`, resetea el índice de salida de `0` a `n - 1`. |

## 6. Retorno

* **Tipo devuelto:** `pandas.DataFrame` (o `Series`).
* **Mutabilidad:** Inmutable; retorna una nueva estructura.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Extracción determinista de 2 registros con semilla:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Messi", "Ronaldo", "Mbappé", "Haaland"],
    "goles": [25, 22, 28, 31]
})

print(df.sample(n=2, random_state=42))
```

**Salida real:**

```text
   jugador  goles
1  Ronaldo     22
3  Haaland     31
```

---

### Nivel 2: Intermedio

Muestreo fraccional con reseteo de índice:

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": [f"Jugador_{i}" for i in range(10)],
    "equipo": ["Equipo_A"] * 10
})

muestra_50 = df.sample(frac=0.5, random_state=123, ignore_index=True)
print(f"Total muestra: {len(muestra_50)} filas.")
print(muestra_50.head(2))
```

**Salida real:**

```text
Total muestra: 5 filas.
     jugador    equipo
0  Jugador_4  Equipo_A
1  Jugador_8  Equipo_A
```

---

### Nivel 3: Avanzado

Particionamiento reproducible de conjuntos de entrenamiento y prueba sin librerías externas:

```python
import pandas as pd

df_atletas = pd.DataFrame({
    "id": range(100),
    "rendimiento": [i * 1.2 for i in range(100)]
})

# 80% entrenamiento, 20% prueba
df_train = df_atletas.sample(frac=0.8, random_state=42)
df_test = df_atletas.drop(df_train.index)

print(f"Entrenamiento: {df_train.shape[0]} filas | Prueba: {df_test.shape[0]} filas.")
assert len(set(df_train.index).intersection(set(df_test.index))) == 0
```

**Salida real:**

```text
Entrenamiento: 80 filas | Prueba: 20 filas.
```

## 8. Errores frecuentes y casos borde

1. Especificar simultáneamente `n` y `frac`: Lanza `ValueError: Please enter a value for `frac` OR `n`, not both`.

## 9. Buenas prácticas y rendimiento

* Fijar siempre `random_state` en scripts analíticos y pipelines para garantizar reproducibilidad en pruebas de regresión.

## 10. Métodos relacionados

* [head](head.md) — Selección inicial posicional.
* [tail](tail.md) — Selección final posicional.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.sample](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html) (Pandas 2.2).
