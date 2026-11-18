# `DataFrame.pipe` y `Series.pipe`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.pipe(func, *args, **kwargs)
```

## 2. ¿Qué es?

Es un **método de orquestación y canalización funcional** que permite encadenar funciones de usuario que reciben y devuelven un DataFrame o Serie completo.

## 3. ¿Para qué sirve?

Elimina el anidamiento ilegible de llamadas a funciones `f(g(h(df)))`, permitiendo escribir una canalización fluida y limpia de izquierda a derecha: `df.pipe(h).pipe(g).pipe(f)`.

## 4. ¿Cómo funciona?

1. **Invocación transparente:** Invoca `func(self, *args, **kwargs)` pasando el propio DataFrame como primer argumento por defecto.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `func` | `callable` | Obligatorio | Posicional | Función a la cual inyectar el DataFrame. |
| `*args` / `**kwargs` | argumentos varios | Opcional | N/A | Parámetros adicionales para `func`. |

## 6. Retorno

* Lo que devuelva `func` (típicamente `pandas.DataFrame`).

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

def filtrar_goleadores(df, umbral):
    return df[df["goles"] >= umbral]

df = pd.DataFrame({"jugador": ["Haaland", "Rodri"], "goles": [31, 8]})
print(df.pipe(filtrar_goleadores, umbral=20))
```

**Salida real:**

```text
   jugador  goles
0  Haaland     31
```

---

### Nivel 2: Intermedio

Canalización modular de múltiples funciones de limpieza:

```python
import pandas as pd

def limpiar_nombres(df):
    df = df.copy()
    df["jugador"] = df["jugador"].str.strip().str.title()
    return df

def agregar_estado(df):
    return df.assign(activo=True)

df_raw = pd.DataFrame({"jugador": ["  messi ", " ronaldo "]})
df_clean = df_raw.pipe(limpiar_nombres).pipe(agregar_estado)
print(df_clean)
```

**Salida real:**

```text
   jugador  activo
0    Messi    True
1  Ronaldo    True
```

---

### Nivel 3: Avanzado

Pipeline completo de producción con logging y auditoría intercalada:

```python
import pandas as pd

def auditar_conteo(df, etapa):
    print(f"[PIPELINE - {etapa}] Filas activas: {len(df)}")
    return df

def filtrar_activos(df):
    return df[df["minutos"] > 500]

df_liga = pd.DataFrame({
    "jugador": ["Vinicius Jr", "Mbappé", "Canterano"],
    "minutos": [2100, 2450, 90]
})

df_final = (
    df_liga
    .pipe(auditar_conteo, etapa="Ingesta")
    .pipe(filtrar_activos)
    .pipe(auditar_conteo, etapa="Post-Filtrado")
)
```

**Salida real:**

```text
[PIPELINE - Ingesta] Filas activas: 3
[PIPELINE - Post-Filtrado] Filas activas: 2
```

## 8. Errores frecuentes y casos borde

1. Pasar funciones que mutan el DataFrame original en lugar de devolver uno nuevo: Rompe la pureza funcional de la tubería.

## 9. Buenas prácticas y rendimiento

* Utilizar `pipe` para estructurar pipelines ETL legibles y testeables por partes.

## 10. Métodos relacionados

* [assign](assign.md) — Asignación funcional de columnas.
* [apply](apply.md) — Aplicación por filas o columnas.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.pipe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pipe.html) (Pandas 2.2).
