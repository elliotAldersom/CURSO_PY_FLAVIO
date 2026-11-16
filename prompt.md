# Proyecto: Documentación integral de Python — DOC/

## 1. Objetivo general

Convertir la carpeta `DOC/` en una biblioteca educativa completa, autónoma y técnicamente rigurosa para aprender Python desde cero hasta un nivel avanzado.

La documentación debe ser suficiente por sí misma para estudiar todos los temas incluidos, sin depender de archivos `.py`, notebooks, ejercicios externos u otros recursos para comprender las explicaciones.

La prioridad es la calidad pedagógica y técnica, no la cantidad de texto.

**Principio fundamental: explicar con profundidad, pero sin relleno.**

## 2. Estructura obligatoria
La estructura principal debe respetar exactamente estos niveles:

- `DOC/Basico/`
- `DOC/Intermedio/`
- `DOC/Avanzado/`

Cada nivel debe contener capítulos independientes con esta convención: 

- `cahpter_one/`
- `cahpter_two/`
- `cahpter_three/`
- Y los necesarios según el contenido.

Cada capítulo contendrá los documentos `.md` correspondientes a sus temas.

Además, debe existir:

- `DOC/introduccion.md`

Este documento tendrá dos funciones:

1. Introducir Python desde sus fundamentos históricos y técnicos.
2. Ser el índice maestro de toda la documentación.

No crear capítulos arbitrarios ni distribuir temas sin una justificación pedagógica. La organización debe seguir las dependencias conceptuales y la dificultad progresiva.

## 3. Documento introduccion.md

Debe explicar de manera clara y rigurosa:

- Historia y origen de Python.
- Qué es Python.
- Para qué se utiliza.
- Características y filosofía del lenguaje.
- Lenguaje de alto nivel.
- Tipado dinámico y tipado fuerte.
- Lenguaje interpretado.
- Bytecode y funcionamiento de CPython.
- Diferencias entre compilación e interpretación.
- Versiones y evolución de Python.
- Biblioteca estándar y bibliotecas externas.
- Ecosistema de Python.

No convertir esta introducción en un libro de historia. Cada apartado debe aportar fundamentos útiles para comprender el lenguaje.

Al finalizar, debe incluir un índice completo y navegable con enlaces relativos a:

- Nivel básico.
- Nivel intermedio.
- Nivel avanzado.
- Todos los capítulos.
- Todos los archivos Markdown.

Mantener este índice actualizado durante todo el proyecto.

## 4. Auditoría inicial

Antes de modificar documentos:

1. Examinar todos los archivos y carpetas de `DOC/`.
2. Identificar los temas existentes.
3. Evaluar su profundidad y exactitud.
4. Detectar explicaciones redundantes o innecesariamente extensas.
5. Identificar referencias externas que sustituyen ejemplos o explicaciones.
6. Detectar temas faltantes.
7. Evaluar la organización actual y proponer mejoras.

No eliminar contenido útil ni modificar masivamente la estructura sin aprobación.

## 5. Cobertura temática

La documentación no debe limitarse a los conceptos presentes en los archivos `.py` originales.

Debe cubrir todos los conocimientos necesarios para aprender Python de forma progresiva.

Incluir, entre otros:

**Nivel básico:**
- Sintaxis y fundamentos.
- Variables y constantes.
- Tipos de datos.
- Operadores.
- Cadenas de texto.
- Entrada y salida.
- Condicionales.
- Bucles.
- Listas, tuplas, conjuntos y diccionarios.
- Funciones básicas.
- Comprensiones introductorias.

**Nivel intermedio:**
- Funciones y argumentos.
- Parámetros posicionales y nominales.
- *args y **kwargs.
- Alcance de variables.
- Funciones lambda.
- Recursividad.
- Módulos y paquetes.
- Manejo de excepciones.
- Archivos y directorios.
- Programación orientada a objetos.
- Iteradores y generadores.
- Expresiones regulares.
- Entornos virtuales y dependencias.
- Gestión de datos JSON, CSV y Excel.

**Nivel avanzado:**
- POO avanzada.
- Herencia, polimorfismo y encapsulamiento.
- Decoradores.
- Generadores avanzados.
- Context managers.
- Tipado y anotaciones.
- Dataclasses.
- Programación funcional.
- Concurrencia.
- Multiprocesamiento.
- Asincronía y asyncio.
- Testing y depuración.
- Rendimiento y optimización.
- Arquitectura y buenas prácticas.

La lista es una referencia inicial. Agregar otros temas cuando sean necesarios para completar la formación.

## 6. Bibliotecas fundamentales

Incluir una sección de bibliotecas externas con capítulos propios y una progresión adecuada.

### NumPy
- Arrays y creación de arreglos.
- Dimensiones y formas.
- Indexación y slicing.
- Tipos de datos.
- Operaciones matemáticas.
- Operaciones vectorizadas.
- Broadcasting.
- Funciones estadísticas.
- Manipulación de arrays.

### Pandas
- Series y DataFrame.
- Importación y exportación.
- Lectura de CSV y Excel.
- Inspección de datos.
- Selección e indexación.
- Filtrado booleano.
- Ordenamiento.
- Tipos de datos y conversiones.
- Valores nulos.
- Duplicados.
- Transformaciones.
- Agrupaciones y agregaciones.
- Concatenación y combinación.
- Análisis exploratorio de datos.

### Matplotlib
- Figuras y ejes.
- Gráficos de líneas.
- Barras.
- Histogramas.
- Dispersión.
- Gráficos estadísticos.
- Etiquetas y leyendas.
- Personalización.
- Subplots.
- Exportación de gráficos.

Distinguir siempre entre características del lenguaje Python, biblioteca estándar y bibliotecas externas.

## 7. Tema obligatorio: archivos y directorios

Incluir un documento específico dedicado a la gestión de rutas, archivos y directorios.

Debe explicar:

- Rutas absolutas y relativas.
- Construcción de rutas.
- Módulo `pathlib`.
- Clase `Path`.
- Creación de directorios.
- Comprobación de existencia.
- Lectura y escritura de archivos.
- Creación automática de carpetas.
- Renombrado de archivos.
- Prevención de sobrescritura.
- Manejo de extensiones.

Debe incluir un ejemplo práctico completo que resuelva este escenario:

El programa necesita guardar un archivo dentro de una carpeta determinada.

1. Comprueba si el directorio existe.
2. Si no existe, lo crea automáticamente, incluyendo directorios intermedios cuando sea necesario.
3. Construye la ruta del archivo.
4. Comprueba si el archivo ya existe.
5. Si existe, genera otro nombre disponible: `archivo_1`, `archivo_2`, `archivo_3`, etc.
6. Guarda el archivo sin sobrescribir los anteriores.

Explicar cada operación y sus métodos correspondientes.

También explicar cómo evitar condiciones de carrera cuando se necesita garantizar que un archivo no sea sobrescrito.

## 8. Estándar de documentación de cada tema

Cada archivo `.md` debe explicar lo necesario para comprender el tema.

Utilizar una estructura flexible según el contenido:

1. **¿Qué es?** Definición clara y precisa.
2. **¿Para qué sirve?** Problema que resuelve y cuándo utilizarlo.
3. **¿Cómo funciona?** Comportamiento y fundamentos.
4. **Sintaxis:** estructura y forma de utilización.
5. **Parámetros y argumentos:** qué recibe, cuáles son opcionales, valores predeterminados y restricciones.
6. **Retorno:** qué devuelve y de qué tipo, o si no retorna un valor útil.
7. **Ejemplos:** código completo y reproducible.
8. **Resultado:** salida esperada e interpretación.
9. **Errores frecuentes y buenas prácticas:** cuando sean relevantes.

No forzar todos los apartados si el concepto no los necesita.

### Documentación de funciones y métodos

Cuando se documente una función o método, explicar específicamente:

- Nombre.
- Qué es y qué hace.
- Objeto sobre el que se invoca, cuando corresponda.
- Sintaxis.
- Parámetros.
- Argumentos aceptados.
- Parámetros obligatorios y opcionales.
- Valores predeterminados.
- Tipo de retorno.
- Qué representa el valor retornado.
- Si modifica el objeto original o genera uno nuevo.
- Ejemplo completo.

Diferenciar claramente parámetros de argumentos.

No confundir funciones, métodos, atributos, propiedades y clases.

Para atributos y propiedades explicar qué información proporcionan y cómo se consultan.

Para operadores explicar sus operandos, comportamiento y resultados.

## 9. Estilo pedagógico y extensión

La documentación debe ser directa, didáctica y técnicamente profunda.

Evitar:

- Párrafos excesivamente largos.
- Repeticiones de una misma definición.
- Introducciones genéricas que no aporten conocimiento.
- Secciones de relleno.
- Explicaciones excesivamente académicas cuando una explicación sencilla y precisa sea suficiente.
- Tablas que sustituyan explicaciones necesarias.
- Jerga técnica sin explicar.
- Ejemplos innecesariamente complejos.

Priorizar:

- Explicaciones claras.
- Fundamentos antes de atajos.
- Ejemplos progresivos.
- Comparaciones cuando ayuden a distinguir conceptos.
- Código comentado cuando sea necesario.
- Tablas para organizar información técnica.
- Explicación de por qué ocurre un comportamiento, no solamente qué sucede.

No reducir la profundidad para conseguir documentos cortos. La extensión debe depender de la complejidad real del tema.

## 10. Independencia de los documentos

Cada Markdown debe ser autosuficiente.

Está prohibido sustituir ejemplos o explicaciones por referencias como:

`aprendiendo_pandas.py`, líneas 18-27.

Todos los ejemplos deben escribirse directamente en el documento.

Cada ejemplo debe contener los datos, importaciones, variables y estructuras necesarios para ejecutarse.

Se permiten enlaces internos a otros documentos como material complementario, pero nunca como requisito para comprender el documento actual.

No utilizar la sección de relación con los archivos originales como sustituto de contenido educativo.

## 11. Ejemplos y reproducibilidad

Los ejemplos deben:

- Ser completos.
- Ser ejecutables.
- Utilizar nombres descriptivos.
- Incluir las importaciones necesarias.
- Mostrar los resultados esperados cuando sea pertinente.
- Explicar las operaciones importantes.
- Mantener una dificultad progresiva.

Cuando se utilicen bibliotecas externas, indicar su instalación y dependencias relevantes.

No presentar pseudocódigo como si fuera código ejecutable.

## 12. Fuentes técnicas

Priorizar documentación oficial:

- Python Documentation.
- NumPy Documentation.
- Pandas Documentation.
- Matplotlib Documentation.

Verificar parámetros, retornos, versiones y comportamientos.

Distinguir entre comportamiento documentado, recomendaciones y decisiones de implementación.

## 13. Metodología de trabajo

Trabajar por etapas y solicitar aprobación antes de avanzar:

**Etapa 1:** Auditoría de la carpeta DOC/.

**Etapa 2:** Diagnóstico de los documentos existentes.

**Etapa 3:** Diseño de la estructura definitiva y ruta de aprendizaje.

**Etapa 4:** Definición del índice maestro `introducción.md`.

**Etapa 5:** Corrección y ampliación de los documentos existentes.

**Etapa 6:** Creación de los documentos correspondientes a temas faltantes.

**Etapa 7:** Incorporación y desarrollo de NumPy, Pandas y Matplotlib.

**Etapa 8:** Validación técnica, pedagógica y de enlaces internos.

Trabajar documento por documento, mostrando los cambios y esperando aprobación cuando corresponda.

## 14. Criterios de aceptación final

La documentación estará completa cuando:

- Respete la estructura de carpetas establecida.
- Tenga una introducción y un índice maestro actualizado.
- Cubra los fundamentos y temas avanzados necesarios.
- Incluya NumPy, Pandas y Matplotlib.
- Explique CSV y Excel.
- Incluya gestión de archivos y directorios.
- Cada documento sea autónomo.
- Los ejemplos estén escritos directamente en los Markdown.
- Las funciones y métodos tengan documentados sus parámetros y retornos.
- No exista relleno ni repetición innecesaria.
- Los ejemplos sean reproducibles.
- Las explicaciones sean técnicamente correctas.

## 15. Ejecución efectiva del proyecto

Tu responsabilidad no consiste únicamente en analizar, recomendar o proponer cambios. Debes trabajar directamente sobre los archivos de la carpeta `DOC/` utilizando las herramientas de edición disponibles.

El objetivo es entregar documentación real y funcional, no solamente un plan de trabajo.

Reglas:

- Después de la auditoría y de obtener mi aprobación del plan, comienza a ejecutar las modificaciones.
- Crea las carpetas y archivos Markdown necesarios.
- Edita los documentos existentes cuando sea necesario.
- Conserva el contenido útil y mejora lo que esté incompleto.
- Actualiza los enlaces internos y el índice maestro.
- Verifica que los ejemplos de código sean ejecutables.
- No declares terminado un documento si todavía depende de explicaciones externas.
- No te limites a mostrarme bloques de código o contenido que yo tenga que copiar manualmente: escribe los cambios directamente en los archivos.
- Informa qué archivos creaste, modificaste o reorganizaste.
- Si alguna operación no puede realizarse con las herramientas disponibles, indícalo claramente.

Trabaja por etapas, solicita mi aprobación cuando corresponda y continúa con la ejecución una vez autorizada cada etapa.

**Resultado final: una biblioteca de estudio de Python que pueda utilizarse como material principal de aprendizaje desde cero hasta avanzado, sin depender de los archivos originales del curso para entender sus contenidos.**