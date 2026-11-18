# Seaborn: countplot

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.13.x)
seaborn.countplot(data=None, *, x=None, y=None, hue=None, order=None, hue_order=None, orient=None, color=None, palette=None, saturation=0.75, fill=True, width=0.8, dodge='auto', gap=0, log_scale=None, native_scale=False, formatter=None, legend='auto', stat='count', ax=None, **kwargs)
```

## 2. ¿Qué es?

`seaborn.countplot` traza un gráfico de barras donde la altura (o longitud horizontal) de cada barra representa exclusivamente el conteo de frecuencias de una variable categórica.

## 3. ¿Para qué sirve?

Equivale a aplicar `value_counts()` de Pandas y graficar el resultado, proveyendo una visualización directa del balance de clases y cardinalidad de grupos sin especificar un eje Y numérico.

## 4. ¿Cómo funciona?

Agrupa internamente el vector de datos provisto en `x` (o `y`), computa la longitud de cada partición de índices y mapea las frecuencias a rectángulos.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `data` | `DataFrame` | Opcional | `None` | Estructura de datos tabular. |
| `x` | `str` | Opcional | `None` | Nombre de la columna para barras verticales (conteo en Y). |
| `y` | `str` | Opcional | `None` | Nombre de la columna para barras horizontales (conteo en X). |
| `hue` | `str` | Opcional | `None` | Variable para estratificar el conteo por un segundo nivel categórico. |
| `order` | `list[str]` | Opcional | `None` | Lista que especifica el orden de aparición de las barras. |
| `stat` | `'count'`, `'percent'` | Opcional | `'count'` | Representar frecuencia absoluta o porcentaje relativo. |
| `ax` | `matplotlib.axes.Axes` | Opcional | `None` | Eje destino. |

## 6. Retorno

`matplotlib.axes.Axes`. El eje con las barras de frecuencias generadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"tipo": ["A", "A", "B", "A", "C", "B", "A"]})
fig, ax = plt.subplots()
ret = sns.countplot(data=df, x="tipo", ax=ax)

print(f"Tipo retornado: {type(ret).__name__}")
print(f"Total barras: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Tipo retornado: Axes
Total barras: 3
```

### Nivel 2: Intermedio

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "ciudad": ["Bogotá", "Medellín", "Cali", "Bogotá", "Medellín", "Bogotá"],
    "canal": ["Web", "App", "Web", "App", "Web", "Web"]
})

fig, ax = plt.subplots()
sns.countplot(data=df, x="ciudad", hue="canal", palette="dark", ax=ax)
print(f"Barras de conteo estratificado: {len(ax.patches)}")
plt.close(fig)
```

**Salida real:**

```text
Barras de conteo estratificado: 6
```

### Nivel 3: Avanzado

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "nivel_severidad": ["Baja", "Baja", "Baja", "Media", "Media", "Crítica"]
})

fig, ax = plt.subplots()
# Ordenamiento explícito según severidad y barras horizontales
sns.countplot(data=df, y="nivel_severidad", order=["Baja", "Media", "Crítica"], color="coral", ax=ax)
ax.set_title("Distribución de Tickets por Severidad")

print(f"Etiquetas ordenadas: {[t.get_text() for t in ax.get_yticklabels()]}")
plt.close(fig)
```

**Salida real:**

```text
Etiquetas ordenadas: ['Baja', 'Media', 'Crítica']
```

## 8. Errores frecuentes y casos borde

- **Pasar ambos parámetros `x` e `y`:** Lanzará error porque `countplot` cuenta ocurrencias de UNA sola dimensión, la otra dimensión la computa él automáticamente.
- **Clases con cardinalidad excesiva:** Graficar una columna con 500 categorías generará un gráfico ilegible; filtrar previamente con `.value_counts().head(10)`.

## 9. Buenas prácticas y rendimiento

- Usar el eje horizontal (`y='categoria'`) cuando los nombres de las categorías sean largos para evitar rotaciones forzadas de texto.
- Utilizar el parámetro `order=df['categoria'].value_counts().index` para ordenar automáticamente de mayor a menor frecuencia.

## 10. Métodos relacionados

- [barplot](barplot.md)
- [histplot](../01_distribuciones/histplot.md)

## 11. Referencias oficiales

- https://seaborn.pydata.org/generated/seaborn.countplot.html
