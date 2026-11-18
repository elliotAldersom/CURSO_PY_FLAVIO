# `pandas.concat`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
pandas.concat(
    objs,
    *,
    axis=0,
    join='outer',
    ignore_index=False,
    keys=None,
    levels=None,
    names=None,
    verify_integrity=False,
    sort=False,
    copy=None
) -> pandas.DataFrame
```

## 2. ¿Qué es?

Es una **función constructora de ensamblaje** que une múltiples objetos Series o DataFrames a lo largo de un eje específico (verticalmente apilando filas con `axis=0`, u horizontalmente pegando columnas con `axis=1`).

## 3. ¿Para qué sirve?

Permite consolidar archivos mensuales en una sola tabla continua o yuxtaponer columnas de fuentes distintas alineadas por índice.

* **Equivalencia en SQL:** `UNION ALL` (con `axis=0`) o `FULL OUTER JOIN` sobre índices (con `axis=1`).

## 4. ¿Cómo funciona?

1. **Alineación por índice:** Con `axis=0`, apila filas alineando columnas por nombre. Con `axis=1`, concatena columnas alineando filas por el `Index`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `objs` | lista de DataFrames o Series | Obligatorio | Posicional | Secuencia de estructuras a combinar. |
| `axis` | `{0, 1}` | Opcional | `0` | `0` apila filas; `1` concatena columnas. |
| `join` | `{'inner', 'outer'}` | Opcional | `'outer'` | Intersección (`'inner'`) o unión (`'outer'`) del eje opuesto. |
| `ignore_index` | `bool` | Opcional | `False` | Si es `True`, genera un índice continuo `0..n-1`. |
| `verify_integrity` | `bool` | Opcional | `False` | Verifica que no se generen índices duplicados. |

## 6. Retorno

* `pandas.DataFrame` o `Series`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

Apilado vertical de dos lotes mensuales:

```python
import pandas as pd

lote_1 = pd.DataFrame({"jugador": ["Pedri"], "goles": [2]})
lote_2 = pd.DataFrame({"jugador": ["Gavi"], "goles": [1]})

df_total = pd.concat([lote_1, lote_2], ignore_index=True)
print(df_total)
```

**Salida real:**

```text
  jugador  goles
0   Pedri      2
1    Gavi      1
```

---

### Nivel 2: Intermedio

Concatenación horizontal (`axis=1`) con intersección estricta (`join='inner'`):

```python
import pandas as pd

df_ataque = pd.DataFrame({"goles": [21, 28]}, index=["Vinicius Jr", "Mbappé"])
df_defensa = pd.DataFrame({"recuperaciones": [45]}, index=["Vinicius Jr"])

# Solo incluye filas presentes en ambos DataFrames
print(pd.concat([df_ataque, df_defensa], axis=1, join="inner"))
```

**Salida real:**

```text
             goles  recuperaciones
Vinicius Jr     21              45
```

---

### Nivel 3: Avanzado

Concatenación con claves jerárquicas (`keys`) para auditoría de lotes:

```python
import pandas as pd

df_t1 = pd.DataFrame({"goles": [15]}, index=["Haaland"])
df_t2 = pd.DataFrame({"goles": [16]}, index=["Haaland"])

df_historico = pd.concat([df_t1, df_t2], keys=["Temporada_2023", "Temporada_2024"])
print(df_historico)
print("\nConsulta de la Temporada 2024:")
print(df_historico.loc["Temporada_2024"])
```

**Salida real:**

```text
                        goles
Temporada_2023 Haaland     15
Temporada_2024 Haaland     16

Consulta de la Temporada 2024:
         goles
Haaland     16
```

## 8. Errores frecuentes y casos borde

1. Concatenar dentro de un bucle `for` (`df = pd.concat([df, nueva_fila])`): Es un antipatrón cuadrático $O(N^2)$. **Solución:** Acumular DataFrames en una lista de Python y hacer un único `pd.concat(lista)` al final.

## 9. Buenas prácticas y rendimiento

* Siempre acumular en listas y concatenar en una sola operación masiva.

## 10. Métodos relacionados

* [merge](merge.md) — Uniones relacionales tipo SQL.

## 11. Referencias oficiales

* **API Reference:** [pandas.concat](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) (Pandas 2.2).
