# `Series.between`

```python
# NO EJECUTAR (Firma oficial de la API en Pandas 2.2.x)
Series.between(left, right, inclusive='both') -> pandas.Series[bool]
```

## 2. ¿Qué es?

Es un **método de instancia de Series** que genera una máscara booleana evaluando si cada elemento numérico o temporal se encuentra dentro de un intervalo cerrado, abierto o semiabierto `[left, right]`.

## 3. ¿Para qué sirve?

Simplifica la sintaxis al evitar escribir `(df['goles'] >= 10) & (df['goles'] <= 25)`.

* **Equivalencia en SQL:** Equivale directamente a la cláusula `WHERE columna BETWEEN left AND right`.

## 4. ¿Cómo funciona?

1. **Comparación vectorizada:** Evalúa vectorialmente los límites inferior y superior con control fino sobre la inclusión de extremos mediante `inclusive`.

## 5. Parámetros

| Parámetro | Tipo aceptado | Obligatorio / Opcional | Valor por defecto | Descripción y restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `left` | escalar | Obligatorio | Posicional | Límite inferior del intervalo. |
| `right` | escalar | Obligatorio | Posicional | Límite superior del intervalo. |
| `inclusive` | `{'both', 'neither', 'left', 'right'}` | Opcional | `'both'` | Política de inclusión de los límites. |

## 6. Retorno

* `pandas.Series[bool]`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd

df = pd.DataFrame({
    "jugador": ["Bellingham", "Kroos", "Modric", "Guler"],
    "minutos": [2400, 2100, 1600, 750]
})

filtro_media = df["minutos"].between(1500, 2200)
print(df[filtro_media])
```

**Salida real:**

```text
  jugador  minutos
1   Kroos     2100
2  Modric     1600
```

---

### Nivel 2: Intermedio

Control de intervalos abiertos y semiabiertos:

```python
import pandas as pd

edades = pd.Series([18, 21, 25, 30, 35])
# Excluyendo ambos extremos (estrictamente entre 21 y 35)
print(edades[edades.between(21, 35, inclusive="neither")])
```

**Salida real:**

```text
2    25
3    30
dtype: int64
```

---

### Nivel 3: Avanzado

Filtrado de series temporales en ventanas dinámicas:

```python
import pandas as pd

df_partidos = pd.DataFrame({
    "fecha": pd.to_datetime(["2024-03-01", "2024-04-15", "2024-06-01"]),
    "rival": ["Valencia", "Barcelona", "Dortmund"]
})

en_primavera = df_partidos["fecha"].between("2024-03-21", "2024-05-31")
print(df_partidos[en_primavera])
```

**Salida real:**

```text
       fecha      rival
1 2024-04-15  Barcelona
```

## 8. Errores frecuentes y casos borde

1. Invertir los límites (`left > right`): Retorna una máscara donde todos los valores son `False`.

## 9. Buenas prácticas y rendimiento

* Altamente eficiente en series numéricas y temporales con índices contiguos.

## 10. Métodos relacionados

* [isin](isin.md) — Pertenencia a conjuntos discretos.
* [filtrado_booleano](filtrado_booleano.md) — Filtros lógicos manuales.

## 11. Referencias oficiales

* **API Reference:** [pandas.Series.between](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html) (Pandas 2.2).
