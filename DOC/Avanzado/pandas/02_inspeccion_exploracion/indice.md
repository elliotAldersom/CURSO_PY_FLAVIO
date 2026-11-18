# Categoría 02: Inspección y Exploración

Métodos y atributos para diagnosticar, auditar y explorar conjuntos de datos tabulares.

| Método / Atributo | Tipo | Descripción | Enlace |
| :--- | :--- | :--- | :--- |
| `head` | Método | Retorna las primeras `n` filas según el orden físico de almacenamiento. | [head.md](head.md) |
| `tail` | Método | Retorna las últimas `n` filas del DataFrame. | [tail.md](tail.md) |
| `info` | Método | Resumen de tipos físicos, conteo de no nulos y consumo en memoria RAM. | [info.md](info.md) |
| `describe` | Método | Estadísticos descriptivos centrales de variables numéricas y categóricas. | [describe.md](describe.md) |
| `shape` | Atributo | Tupla `(filas, columnas)` con las dimensiones del DataFrame. | [shape.md](shape.md) |
| `dtypes` | Atributo | Serie con los tipos de datos de almacenamiento físico de cada columna. | [dtypes.md](dtypes.md) |
| `columns` | Atributo | Índice con las etiquetas y nombres de todas las columnas. | [columns.md](columns.md) |
| `sample` | Método | Extracción aleatoria de filas con o sin reemplazo y semilla determinista. | [sample.md](sample.md) |
| `nunique` | Método | Conteo de la cantidad de valores únicos distintos por columna o fila. | [nunique.md](nunique.md) |
| `value_counts` | Método | Tabla de distribución de frecuencias absolutas o relativas. | [value_counts.md](value_counts.md) |
| `isna` / `isnull` | Método | Máscara booleana que identifica celdas con valores faltantes. | [isna.md](isna.md) |
