# `DataFrame.columns`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
# Atributo (propiedad)
DataFrame.columns -> pandas.Index
```

## 2. ¿Qué es?

Es un **atributo de propiedad** que contiene y expone el objeto `pandas.Index` representativo de las etiquetas de las columnas del DataFrame.

## 3. ¿Para qué sirve?

Permite iterar sobre las columnas, renombrarlas masivamente por asignación directa, filtrar listas de nombres y validar contratos de esquemas en ingestas automatizadas.

## 4. ¿Cómo funciona?

1. **Estructura Index inmutable:** Es un contenedor unidimensional indexable similar a una tupla optimizada con soporte para operaciones vectorizadas de strings (`df.columns.str`).

## 5. Parámetros

* No recibe parámetros. Permite asignación directa (`df.columns = [...]`).

## 6. Retorno

* **Tipo devuelto:** `pandas.Index`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"jugador": ["Rodri"], "equipo": ["Man City"]})
print(df.columns.tolist())
```

**Salida real:**

```text
['jugador', 'equipo']
```

---

### Nivel 2: Intermedio

Normalización masiva de nombres de columnas con métodos vectorizados de strings:

```python
import pandas as pd

df = pd.DataFrame({"  Nombre Jugador ": ["Musiala"], "GOLES 2024": [12]})
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())
```

**Salida real:**

```text
['nombre_jugador', 'goles_2024']
```

---

### Nivel 3: Avanzado

Validación defensiva de columnas obligatorias en pipeline de producción:

```python
import pandas as pd

COLUMNAS_REQUERIDAS = {"jugador", "equipo", "minutos"}

def validar_contrato_esquema(df: pd.DataFrame):
    faltantes = COLUMNAS_REQUERIDAS - set(df.columns)
    if faltantes:
        raise KeyError(f"Esquema inválido. Faltan columnas: {faltantes}")
    print("[VALIDACIÓN] Esquema contractual verificado exitosamente.")

df_valido = pd.DataFrame({"jugador": ["Pedri"], "equipo": ["Barca"], "minutos": [1800]})
validar_contrato_esquema(df_valido)
```

**Salida real:**

```text
[VALIDACIÓN] Esquema contractual verificado exitosamente.
```

## 8. Errores frecuentes y casos borde

1. Intentar modificar un elemento individual con `df.columns[0] = 'nuevo'`. Lanza `TypeError: Index does not support mutable operations`. **Solución:** Usar `df.rename(columns={...})` o reasignar la lista completa.

## 9. Buenas prácticas y rendimiento

* Estandarizar nombres en minúsculas y sin espacios (`snake_case`) al inicio del pipeline.

## 10. Métodos relacionados

* [rename](../05_limpieza_transformacion/rename.md) — Renombrado selectivo de columnas.
* [shape](shape.md) — Dimensionalidad del DataFrame.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.columns](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.columns.html) (Pandas 2.2).
