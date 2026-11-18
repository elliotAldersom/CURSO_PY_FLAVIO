# Documentación Técnica de Métodos de Pandas

Bienvenido a la biblioteca exhaustiva de métodos, funciones y accesores de **Pandas 2.2.x**, estructurada según los estándares más rigurosos de ingeniería de software y ciencia de datos.

Cada documento es **completamente autónomo**, incluye la firma oficial de la API, análisis de mutabilidad y comportamiento en memoria, tabla exhaustiva de parámetros, tres niveles de ejemplos prácticos con salidas reales sobre datos deportivos y referencias canónicas.

---

## Índice Temático por Categorías

### 1. Ingesta y Persistencia
* [Índice de Lectura y Escritura](01_lectura_escritura/indice.md)
  * [`read_csv`](01_lectura_escritura/read_csv.md) — Ingesta de texto delimitado CSV/TSV.
  * [`read_excel`](01_lectura_escritura/read_excel.md) — Lectura de libros Microsoft Excel.
  * [`ExcelFile`](01_lectura_escritura/excel_file.md) — Inspección y lectura multioja eficiente.
  * [`to_csv`](01_lectura_escritura/to_csv.md) — Exportación a texto delimitado.
  * [`to_excel`](01_lectura_escritura/to_excel.md) — Exportación a hojas Excel.

### 2. Inspección y Exploración
* [Índice de Inspección y Exploración](02_inspeccion_exploracion/indice.md)
  * [`head`](02_inspeccion_exploracion/head.md) — Primeras filas.
  * [`tail`](02_inspeccion_exploracion/tail.md) — Últimas filas.
  * [`info`](02_inspeccion_exploracion/info.md) — Diagnóstico de tipos y memoria.
  * [`describe`](02_inspeccion_exploracion/describe.md) — Resumen estadístico descriptivo.
  * [`shape`](02_inspeccion_exploracion/shape.md) — Dimensionalidad `(filas, columnas)`.
  * [`dtypes`](02_inspeccion_exploracion/dtypes.md) — Tipos de datos por columna.
  * [`columns`](02_inspeccion_exploracion/columns.md) — Etiquetas de columnas.
  * [`sample`](02_inspeccion_exploracion/sample.md) — Muestreo aleatorio reproducible.
  * [`nunique`](02_inspeccion_exploracion/nunique.md) — Conteo de valores únicos.
  * [`value_counts`](02_inspeccion_exploracion/value_counts.md) — Frecuencias absolutas y relativas.
  * [`isna` / `isnull`](02_inspeccion_exploracion/isna.md) — Máscara booleana de valores faltantes.

### 3. Selección y Filtrado
* [Índice de Selección y Filtrado](03_seleccion_filtrado/indice.md)
  * [`filtrado_booleano`](03_seleccion_filtrado/filtrado_booleano.md) — Máscaras booleanas con `&`, `|`, `~`.
  * [`loc`](03_seleccion_filtrado/loc.md) — Indexación basada en etiquetas.
  * [`iloc`](03_seleccion_filtrado/iloc.md) — Indexación posicional entera.
  * [`query`](03_seleccion_filtrado/query.md) — Filtrado declarativo con strings y variables `@`.
  * [`isin`](03_seleccion_filtrado/isin.md) — Comprobación de pertenencia a conjuntos.
  * [`between`](03_seleccion_filtrado/between.md) — Pertenencia a intervalos continuos.
  * [`str.contains`](03_seleccion_filtrado/str_contains.md) — Búsqueda de subcadenas y Regex.

### 4. Ordenamiento e Índices
* [Índice de Ordenamiento e Índices](04_ordenamiento_indices/indice.md)
  * [`sort_values`](04_ordenamiento_indices/sort_values.md) — Ordenamiento multicriterio.
  * [`reset_index`](04_ordenamiento_indices/reset_index.md) — Restablecimiento de índices a enteros.
  * [`set_index`](04_ordenamiento_indices/set_index.md) — Promoción de columnas a índice.
  * [`nlargest`](04_ordenamiento_indices/nlargest.md) — Extracción de los $N$ mayores valores.
  * [`nsmallest`](04_ordenamiento_indices/nsmallest.md) — Extracción de los $N$ menores valores.
  * [`idxmax`](04_ordenamiento_indices/idxmax.md) — Etiqueta del valor máximo.
  * [`idxmin`](04_ordenamiento_indices/idxmin.md) — Etiqueta del valor mínimo.
  * [`rank`](04_ordenamiento_indices/rank.md) — Asignación de rangos y clasificaciones.

### 5. Limpieza y Transformación
* [Índice de Limpieza y Transformación](05_limpieza_transformacion/indice.md)
  * [`str.lower`](05_limpieza_transformacion/str_lower.md) — Cadenas en minúsculas.
  * [`str.strip`](05_limpieza_transformacion/str_strip.md) — Remoción de espacios laterales.
  * [`str.title`](05_limpieza_transformacion/str_title.md) — Capitalización de títulos.
  * [`rename`](05_limpieza_transformacion/rename.md) — Renombrado selectivo de columnas.
  * [`astype`](05_limpieza_transformacion/astype.md) — Fundición física de tipos de datos.
  * [`to_numeric`](05_limpieza_transformacion/to_numeric.md) — Coerción segura a números.
  * [`fillna`](05_limpieza_transformacion/fillna.md) — Imputación de nulos.
  * [`dropna`](05_limpieza_transformacion/dropna.md) — Eliminación de filas con nulos.
  * [`replace`](05_limpieza_transformacion/replace.md) — Sustitución exacta o por Regex.
  * [`map`](05_limpieza_transformacion/map.md) — Transformación elemento a elemento.
  * [`apply`](05_limpieza_transformacion/apply.md) — Aplicación funcional por filas/columnas.
  * [`assign`](05_limpieza_transformacion/assign.md) — Asignación funcional encadenada.
  * [`pipe`](05_limpieza_transformacion/pipe.md) — Orquestación de pipelines completos.
  * [`cut`](05_limpieza_transformacion/cut.md) — Discretización en contenedores fijos.
  * [`qcut`](05_limpieza_transformacion/qcut.md) — Discretización por cuantiles equilibrados.

### 6. Duplicados
* [Índice de Duplicados](06_duplicados/indice.md)
  * [`duplicated`](06_duplicados/duplicated.md) — Diagnóstico de registros redundantes.
  * [`drop_duplicates`](06_duplicados/drop_duplicates.md) — Eliminación de filas duplicadas con hashing en C.

### 7. Agrupación y Agregación
* [Índice de Agrupación y Agregación](07_agrupacion_agregacion/indice.md)
  * [`groupby`](07_agrupacion_agregacion/groupby.md) — Paradigma Split-Apply-Combine.
  * [`agg`](07_agrupacion_agregacion/agg.md) — Agregación multifunción con Named Aggregations.
  * [`pivot_table`](07_agrupacion_agregacion/pivot_table.md) — Tablas dinámicas bidimensionales.
  * [`crosstab`](07_agrupacion_agregacion/crosstab.md) — Tabulación cruzada de contingencia.
  * [`cumsum`](07_agrupacion_agregacion/cumsum.md) — Suma acumulada progresiva.
  * [`sum`](07_agrupacion_agregacion/sum.md) — Sumatoria de reducción.
  * [`mean`](07_agrupacion_agregacion/mean.md) — Media aritmética.
  * [`median`](07_agrupacion_agregacion/median.md) — Mediana robusta.
  * [`std`](07_agrupacion_agregacion/std.md) — Desviación estándar.
  * [`quantile`](07_agrupacion_agregacion/quantile.md) — Cálculo de cuantiles y percentiles.

### 8. Fechas y Series de Tiempo
* [Índice de Fechas y Series de Tiempo](08_fechas_series_tiempo/indice.md)
  * [`to_datetime`](08_fechas_series_tiempo/to_datetime.md) — Parsing a DatetimeIndex.
  * [`dt_accessor`](08_fechas_series_tiempo/dt_accessor.md) — Introducción al accesor temporal `.dt`.
  * [`dt.year` / `dt.month`](08_fechas_series_tiempo/dt_year_month.md) — Extracción de año y mes.
  * [`dt.day_name`](08_fechas_series_tiempo/dt_day_names.md) — Nombre del día y orden semanal.
  * [`dt.isocalendar`](08_fechas_series_tiempo/dt_isocalendar.md) — Estándar internacional ISO 8601.
  * [`dt.to_period`](08_fechas_series_tiempo/dt_to_period.md) — Intervalos temporales regulares.
  * [`resample`](08_fechas_series_tiempo/resample.md) — Remuestreo por frecuencia fija.
  * [`diff`](08_fechas_series_tiempo/diff.md) — Diferencias finitas y deltas.

### 9. Combinación y Reestructuración
* [Índice de Combinación y Reestructuración](09_combinacion_reestructuracion/indice.md)
  * [`merge`](09_combinacion_reestructuracion/merge.md) — Uniones relacionales tipo SQL.
  * [`concat`](09_combinacion_reestructuracion/concat.md) — Concatenación por filas o columnas.
  * [`melt`](09_combinacion_reestructuracion/melt.md) — De formato ancho a formato largo (*tidy*).

### 10. Estadística
* [Índice de Estadística](10_estadistica/indice.md)
  * [`corr`](10_estadistica/corr.md) — Matriz de correlación bivariada (Pearson, Spearman, Kendall).
