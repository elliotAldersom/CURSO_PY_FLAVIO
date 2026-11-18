# `DataFrame.set_index`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
DataFrame.set_index(
    keys,
    *,
    drop=True,
    append=False,
    inplace=False,
    verify_integrity=False
)
```

## 2. ¿Qué es?

Es un **método de configuración estructural** que promueve una o varias columnas del DataFrame para convertirlas en el nuevo `Index` (o MultiIndex) de filas.

## 3. ¿Para qué sirve?

Habilita búsquedas optimizadas mediante `.loc` por claves de negocio (p. ej. `id_jugador` o `codigo_partido`) y alinea datos automáticamente al operar entre tablas.

## 4. ¿Cómo funciona?

1. **Construcción de Index:** Extrae las columnas indicadas y las transfiere a la propiedad `self.index`. Si `verify_integrity=True`, audita que no existan duplicados lanzando excepción en caso de colisión.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `keys` | columna, lista de columnas | Obligatorio | Posicional | Columnas a transformar en índice. |
| `drop` | `bool` | Opcional | `True` | Si es `True`, elimina las columnas del cuerpo de datos tras moverlas al índice. |
| `verify_integrity` | `bool` | Opcional | `False` | Audita que no existan etiquetas duplicadas en el nuevo índice. |

## 6. Retorno

* `pandas.DataFrame`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({"id": [101, 102], "jugador": ["Bellingham", "Wirtz"], "goles": [19, 11]})
df_indexado = df.set_index("id")
print(df_indexado)
```

**Salida real:**

```text
        jugador  goles
id                    
101  Bellingham     19
102       Wirtz     11
```

---

### Nivel 2: Intermedio

Verificación de unicidad con `verify_integrity=True`:

```python
import pandas as pd

df_atletas = pd.DataFrame({"dni": ["A1", "A2"], "jugador": ["Pedri", "Gavi"]})
df_seguro = df_atletas.set_index("dni", verify_integrity=True)
print("Índice único verificado:")
print(df_seguro)
```

**Salida real:**

```text
Índice único verificado:
    jugador
dni        
A1    Pedri
A2     Gavi
```

---

### Nivel 3: Avanzado

Construcción de MultiIndex jerárquico para consultas compuestas:

```python
import pandas as pd

df_liga = pd.DataFrame({
    "liga": ["Espana", "Espana", "Inglaterra"],
    "equipo": ["Real Madrid", "Barcelona", "Man City"],
    "puntos": [95, 85, 91]
})

df_multi = df_liga.set_index(["liga", "equipo"])
print(df_multi)
print("\nAcceso jerárquico a Real Madrid:")
print(df_multi.loc[("Espana", "Real Madrid")])
```

**Salida real:**

```text
                    puntos
liga       equipo         
Espana     Real Madrid      95
           Barcelona        85
Inglaterra Man City         91

Acceso jerárquico a Real Madrid:
puntos    95
Name: (Espana, Real Madrid), dtype: int64
```

## 8. Errores frecuentes y casos borde

1. Duplicados con `verify_integrity=True`: Lanza `ValueError: Index has duplicate keys`.

## 9. Buenas prácticas y rendimiento

* Conservar como índice identificadores únicos naturales para acelerar cruces posteriores.

## 10. Métodos relacionados

* [reset_index](reset_index.md) — Operación inversa.
* [loc](../03_seleccion_filtrado/loc.md) — Búsqueda rápida por etiqueta de índice.

## 11. Referencias oficiales

* **API Reference:** [pandas.DataFrame.set_index](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html) (Pandas 2.2).
