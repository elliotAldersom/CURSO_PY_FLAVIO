# Proyecto: Documentación completa de Python y Programación Orientada a Objetos (POO)

## 1. Objetivo general

Quiero que analices exhaustivamente el contenido de los siguientes directorios:

- `DALTO/CLASES_PYTHON/`
- `DALTO/CLASES_PY_POO/`

Ambos directorios contienen material educativo relacionado con Python. Debes analizarlos conjuntamente, considerando que pueden complementarse, profundizar en determinados conceptos o abordar los mismos temas desde perspectivas diferentes.

Tu objetivo es identificar todos los conceptos, herramientas, módulos, librerías, funcionalidades, técnicas y principios de programación que se enseñan en ambos directorios.

A partir de ese análisis, debes construir una única documentación técnica y educativa dentro del directorio:

`DALTO/DOC/`

La documentación debe funcionar como un material de estudio independiente, organizado progresivamente desde nivel básico hasta avanzado.

**IMPORTANTE:**

- No analices únicamente `CLASES_PYTHON/`. Ambos directorios son fuentes obligatorias de información.
- No documentes únicamente los ejemplos mencionados explícitamente en esta solicitud.
- Descubre los temas a partir del contenido real de ambas carpetas, incluyendo conceptos implícitos en el código.
- No generes dos documentaciones separadas. Integra todo el conocimiento en una única estructura organizada.
- Si un tema aparece en ambas carpetas, combina la información sin duplicar innecesariamente su documentación.
- Si una carpeta profundiza en un concepto presentado en la otra, integra ambos niveles de conocimiento en el mismo tema cuando corresponda.

La prioridad es construir una biblioteca de aprendizaje completa, rigurosa y organizada, que permita estudiar cada tema desde sus fundamentos hasta su aplicación en proyectos reales.

---

## 2. Fase 1: Auditoría del contenido original

Antes de escribir cualquier documentación, analiza exhaustivamente ambos directorios.

### Directorios que debes analizar

```text
DALTO/
│
├── CLASES_PYTHON/
│   └── (Primera fuente de conocimiento)
│
├── CLASES_PY_POO/
│   └── (Segunda fuente de conocimiento)
│
└── DOC/
    └── (Destino de la documentación)
```

### Procedimiento de auditoría

1. Recorre todos los archivos y subdirectorios de `CLASES_PYTHON/`.
2. Recorre todos los archivos y subdirectorios de `CLASES_PY_POO/`.
3. Identifica los lenguajes, módulos, librerías, funciones, métodos, estructuras y conceptos utilizados.
4. Analiza el código fuente para comprender qué se está enseñando realmente.
5. Agrupa los conceptos relacionados en temas y subtemas.
6. Identifica dependencias entre temas para establecer un orden pedagógico correcto.
7. Detecta conceptos que necesitan conocimientos previos para ser comprendidos.
8. Identifica qué conceptos son propios del lenguaje Python y cuáles pertenecen a librerías o herramientas externas.
9. Registra los archivos originales relacionados con cada tema identificado.
10. Identifica los temas que aparecen en ambas carpetas.
11. Detecta conceptos que se complementan, amplían o profundizan entre ambas fuentes.
12. Identifica posibles diferencias, contradicciones o enfoques distintos en las explicaciones originales.

### Ejemplos de temas que debes identificar

Esta lista es orientativa y no limita el análisis:

**Fundamentos de Python:**

- Variables y constantes.
- Tipos de datos.
- Operadores.
- Condicionales.
- Bucles (`for`, `while`).
- Funciones.
- Parámetros y argumentos.
- Ámbito de las variables (scope).
- Estructuras de datos.
- Listas, tuplas, conjuntos y diccionarios.
- Comprensiones.
- Manejo de excepciones.
- Módulos e importaciones.
- `__init__.py`.
- Manejo de paquetes.
- Gestión de archivos.
- Importación y exportación de información.
- Rutas y módulos `pathlib` y `os`.
- Módulo `math`.
- Módulo `random`.
- Librería `NumPy`.
- Librería `Pandas`.
- Interfaces gráficas con `Tkinter`.
- Manejo de fechas.
- Iteradores y generadores.
- Decoradores.
- Context managers.
- Entornos virtuales.
- Instalación y administración de dependencias.

**Programación Orientada a Objetos (POO):**

- Paradigmas de programación.
- Introducción a la programación orientada a objetos.
- Clases y objetos.
- Atributos y métodos.
- Atributos de instancia y de clase.
- Métodos de instancia.
- Métodos de clase (`@classmethod`).
- Métodos estáticos (`@staticmethod`).
- Constructor (`__init__`).
- Parámetro `self`.
- Encapsulamiento.
- Abstracción.
- Herencia.
- Polimorfismo.
- Sobrescritura de métodos (overriding).
- Sobrecarga y sus particularidades en Python.
- Herencia múltiple.
- MRO (Method Resolution Order).
- Clases abstractas.
- Módulo `abc`.
- Propiedades (`@property`).
- Métodos especiales (dunder methods).
- Composición y agregación.
- Relaciones entre objetos.
- Clases y objetos en memoria.
- Dataclasses.
- Protocolos y duck typing.
- Principios SOLID, cuando estén relacionados con el material.

Estos son ejemplos de referencia. Debes comprobar su presencia en el material original y documentar también los conceptos adicionales que descubras.

### 2.1. Distinción entre lenguaje, implementación y librerías

Mantén una separación conceptual correcta durante toda la documentación.

Por ejemplo:

- **Python:** es el lenguaje de programación.
- **CPython:** es una implementación del lenguaje Python.
- **NumPy:** es una librería externa del ecosistema Python.
- **Pandas:** es una librería externa para manipulación y análisis de datos.
- **Tkinter:** es una interfaz de Python para trabajar con Tcl/Tk.

No presentes las implementaciones, módulos de la biblioteca estándar y librerías externas como si fueran lo mismo.

Cuando un concepto pertenezca a una implementación específica, indícalo expresamente. No atribuyas comportamientos particulares de CPython a todas las implementaciones de Python.

### 2.2. Integración de conocimientos de ambas fuentes

Debes analizar la relación entre los dos directorios.

Aplica los siguientes criterios:

- Si un tema aparece solamente en `CLASES_PYTHON/`, documéntalo utilizando esa fuente.
- Si aparece solamente en `CLASES_PY_POO/`, documéntalo utilizando esa fuente.
- Si aparece en ambas carpetas, integra la información en un único documento.
- Si una carpeta presenta una explicación introductoria y la otra profundiza en el mismo concepto, combina ambas explicaciones siguiendo una progresión pedagógica.
- Si existen ejemplos diferentes para un mismo concepto, selecciona los más didácticos y complementarios.
- Si existen diferencias conceptuales o técnicas, investiga cuál es la explicación correcta utilizando documentación oficial.
- No elimines información importante simplemente porque el mismo tema aparece en ambas fuentes.

No asumas que todos los contenidos de `CLASES_PY_POO/` pertenecen necesariamente al nivel avanzado. La clasificación debe depender de la dificultad real del concepto.

### 2.3. Trazabilidad con el material original

Cada tema documentado debe mantener una relación identificable con el material que motivó su documentación.

Para ello, cada archivo temático debe incorporar una sección llamada:

**Relación con el material original**

Debe indicar:

- Directorio de origen: `CLASES_PYTHON/` o `CLASES_PY_POO/`.
- Ruta relativa del archivo original.
- Nombre del archivo.
- Conceptos identificados en ese archivo.
- Qué aspectos del material original se ampliaron o profundizaron.

Si un tema aparece en varios archivos o en ambas carpetas, registra todas las fuentes relacionadas.

Si el tema se incorpora como conocimiento previo necesario, pero no aparece explícitamente en ninguna de las dos fuentes, indícalo como fundamento complementario.

No inventes referencias a archivos originales.

### Resultado de esta fase

Establece un inventario de temas y determina:

- Qué temas deben documentarse.
- De cuál o cuáles carpetas provienen.
- A qué nivel pertenecen.
- En qué capítulo deben ubicarse.
- Qué conocimientos previos necesitan.
- Qué temas se relacionan entre sí.
- Qué conceptos se repiten entre ambas fuentes.
- Qué conceptos se complementan.
- Qué fundamentos adicionales deben incorporarse.

No comiences a redactar los archivos hasta tener una visión global del contenido de ambos directorios.

---

## 3. Fase 2: Organización de la documentación

La estructura de directorios debe seguir este formato:

```text
DALTO/
│
├── CLASES_PYTHON/
│   └── (Contenido original, no modificar)
│
├── CLASES_PY_POO/
│   └── (Contenido original, no modificar)
│
└── DOC/
    │
    ├── introduccion.md
    │
    ├── Basico/
    │   ├── chapter-one/
    │   │   ├── variables.md
    │   │   ├── tipos_datos.md
    │   │   └── operadores.md
    │   │
    │   └── chapter-two/
    │       ├── condicionales.md
    │       └── bucles.md
    │
    ├── Intermedio/
    │   ├── chapter-one/
    │   │   ├── funciones.md
    │   │   └── estructuras_datos.md
    │   │
    │   └── chapter-two/
    │       ├── clases_objetos.md
    │       ├── atributos_metodos.md
    │       └── encapsulamiento.md
    │
    └── Avanzado/
        ├── chapter-one/
        │   ├── herencia_multiple.md
        │   ├── polimorfismo.md
        │   └── metodos_especiales.md
        │
        └── chapter-two/
            └── ...
```

La estructura anterior es ilustrativa. Debes establecer los capítulos y archivos definitivos según el inventario obtenido durante la auditoría de ambas carpetas.

### Reglas de organización

- `Basico`, `Intermedio` y `Avanzado` representan la dificultad conceptual y los conocimientos necesarios.
- Cada capítulo debe agrupar temas relacionados.
- Los capítulos deben tener un orden lógico de aprendizaje.
- Cada tema debe tener su propio archivo `.md`.
- Los nombres de archivos deben ser descriptivos, preferentemente en `snake_case`.
- Evita duplicar documentación entre archivos.
- Cuando un tema dependa de otro, establece referencias mediante enlaces relativos de Markdown.
- No clasifiques una tecnología completa en un único nivel cuando sus conceptos puedan tener dificultades diferentes.
- Integra los contenidos de ambas carpetas en una única estructura, sin separarlos por su procedencia.

### 3.1. Criterios de clasificación por dificultad

**Básico:**

- Conceptos fundamentales.
- Sintaxis esencial.
- Operaciones elementales.
- Primeros ejemplos prácticos.
- Comprensión de los mecanismos básicos.

**Intermedio:**

- Combinación de conceptos.
- Resolución de problemas.
- Uso de herramientas y librerías.
- Organización del código.
- Aplicaciones prácticas más completas.
- Introducción a conceptos de POO cuando corresponda.

**Avanzado:**

- Funcionamiento interno.
- Abstracciones y mecanismos complejos.
- Optimización.
- Arquitectura.
- Rendimiento.
- Escalabilidad.
- Patrones de diseño.
- Aplicaciones profesionales complejas.

La clasificación debe considerar los conocimientos previos requeridos, no el nombre de la tecnología.

Ejemplo: NumPy puede contener operaciones básicas y avanzadas. De igual forma, POO no debe clasificarse íntegramente como avanzada: las clases, los objetos y sus atributos pueden estudiarse en nivel intermedio, mientras que la herencia múltiple, el MRO y determinados mecanismos internos pueden corresponder al nivel avanzado.

---

## 4. Fase 3: Estructura obligatoria de cada tema

Cada archivo de documentación debe seguir esta estructura:

### 1. Nombre del tema

Título claro y descriptivo.

### 2. Introducción

Explica:

- ¿Qué es?
- ¿Por qué existe?
- ¿Qué problema resuelve?
- ¿Para qué sirve?
- ¿En qué situaciones se utiliza?
- ¿Cuál es su importancia dentro de Python?

La explicación debe comenzar desde los fundamentos, suponiendo que el estudiante todavía no domina el vocabulario técnico.

### 3. Fundamentos y conceptos

Explica los conceptos fundamentales del tema.

Reglas:

- Utiliza terminología técnica cuando corresponda.
- Cada término técnico debe explicarse inmediatamente.
- No asumas que el estudiante conoce conceptos que todavía no se han documentado.
- Explica cómo funciona internamente cuando sea relevante.
- Diferencia conceptos que suelen confundirse.
- Explica el porqué de las decisiones de diseño del lenguaje cuando exista información oficial al respecto.
- Relaciona los fundamentos con otros temas cuando sea necesario.

### 4. Sintaxis y funcionamiento

Presenta la sintaxis correspondiente.

Explica sus componentes, parámetros, argumentos, valores de retorno y comportamiento.

Cuando corresponda, incluye tablas con las siguientes columnas:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|

### 5. Ejemplos prácticos progresivos

Todos los temas deben incluir tres niveles de ejemplos:

**Básico**

- Ejemplos pequeños.
- Una sola idea por ejemplo.
- Explicación línea por línea.
- Resultado esperado.

**Intermedio**

- Combinación de varios conceptos.
- Casos de uso más realistas.
- Manejo de diferentes escenarios.
- Explicación de las decisiones tomadas.

**Avanzado**

- Aplicaciones más complejas.
- Buenas prácticas.
- Casos particulares.
- Consideraciones de rendimiento y mantenibilidad cuando corresponda.

No coloques código sin explicar qué hace y por qué funciona.

Los ejemplos deben ser coherentes con el nivel del apartado. No introduzcas conceptos avanzados sin explicar previamente los fundamentos necesarios.

### 6. Aplicaciones en el mundo real

Explica cómo se utiliza el tema en proyectos reales.

Cuando corresponda, incluye ejemplos de:

- Desarrollo de software.
- Automatización.
- Backend.
- Procesamiento de archivos.
- Análisis de datos.
- Ciencia de datos.
- Visualización de información.
- Aplicaciones de escritorio.
- Procesamiento de grandes volúmenes de información.

No fuerces aplicaciones que no tengan relación con el tema.

### 7. Uso en producción

Explica cómo se utiliza correctamente en proyectos profesionales.

Incluye cuando corresponda:

- Buenas prácticas.
- Errores frecuentes.
- Seguridad.
- Rendimiento.
- Escalabilidad.
- Mantenibilidad.
- Organización del código.
- Alternativas disponibles.
- Cuándo conviene y cuándo no conviene utilizar determinada herramienta.

Diferencia claramente entre un ejemplo educativo y una implementación apropiada para producción.

### 8. Errores comunes y recomendaciones

Identifica errores frecuentes de principiantes y desarrolladores.

Explica por qué ocurren, cómo diagnosticarlos y cómo evitarlos.

### 9. Resumen

Recapitula los conceptos fundamentales del tema.

### 10. Relación con el material original

Incluye las rutas relativas de todos los archivos de ambas carpetas donde se identificó el tema.

Explica brevemente qué conceptos del material original se desarrollaron y cuáles se ampliaron.

Si se trata de un fundamento complementario que no aparece explícitamente en las clases, indícalo.

### 11. Referencias oficiales

Incluye enlaces a documentación oficial de Python o de la librería correspondiente.

Prioriza:

- Documentación oficial de Python: https://docs.python.org/3/
- Documentación oficial de NumPy: https://numpy.org/doc/
- Documentación oficial de Pandas: https://pandas.pydata.org/docs/
- Documentación oficial de Tkinter: https://docs.python.org/3/library/tkinter.html

Para POO, utiliza también las secciones oficiales relacionadas con:

- Clases y objetos: https://docs.python.org/3/tutorial/classes.html
- Modelo de datos: https://docs.python.org/3/reference/datamodel.html
- Clases abstractas: https://docs.python.org/3/library/abc.html
- Dataclasses: https://docs.python.org/3/library/dataclasses.html

Utiliza documentación oficial específica para cada tema.

No inventes referencias, funciones, parámetros ni comportamientos.

---

## 5. Fase 4: Archivo introductorio `introduccion.md`

Dentro de `DALTO/DOC/` crea un archivo llamado:

`introduccion.md`

Este archivo será la puerta de entrada a toda la documentación.

Debe contener:

### 1. ¿Qué es Python?

- Concepto.
- Naturaleza del lenguaje.
- Características principales.

### 2. Historia de Python

- Origen.
- Guido van Rossum.
- Contexto de creación.
- Evolución del lenguaje.
- Versiones importantes.

### 3. ¿Por qué existe Python?

- Problemas que buscaba resolver.
- Filosofía de diseño.
- Legibilidad y simplicidad.
- Principios fundamentales de Python.

### 4. ¿Para qué se utiliza?

Explica sus principales campos de aplicación:

- Desarrollo backend.
- Automatización.
- Análisis de datos.
- Ciencia de datos.
- Inteligencia artificial.
- Machine Learning.
- Aplicaciones de escritorio.
- Scripting.
- Educación científica.

### 5. Fortalezas y debilidades

Incluye una comparación objetiva:

| N° | Fortalezas | Debilidades |
|---|---|---|
| 1 | Legibilidad | Rendimiento frente a lenguajes compilados en determinados escenarios |
| 2 | Ecosistema amplio | Consumo de memoria en determinados casos |
| 3 | Curva de aprendizaje accesible | Limitaciones de concurrencia en ciertos escenarios |

No presentes opiniones como hechos absolutos.

### 6. Cómo funciona Python

Explica de manera introductoria:

- Interpretación y ejecución.
- Bytecode.
- Máquina virtual de Python (cuando corresponda a CPython).
- Gestión de memoria.
- Recolección de basura.
- Diferencias entre Python y CPython.
- Diferencia entre lenguaje, implementación e intérprete.

### 7. Introducción a la programación orientada a objetos

Explica:

- Qué es un paradigma de programación.
- Qué es la programación orientada a objetos.
- Por qué surge este paradigma.
- Qué problemas busca resolver.
- Diferencias generales frente a la programación procedural.
- Qué son las clases y los objetos.
- Qué son los atributos y los métodos.
- Introducción a los cuatro pilares de POO: abstracción, encapsulamiento, herencia y polimorfismo.
- Cuándo conviene utilizar POO.

No desarrolles aquí toda la teoría de POO. Proporciona una introducción que permita comprender los capítulos especializados.

### 8. Índice general de documentación

Este apartado es fundamental.

Debe contener un índice navegable con enlaces relativos a TODOS los archivos `.md` creados dentro de `Basico/`, `Intermedio/` y `Avanzado/`.

Organiza el índice por nivel y capítulo.

Ejemplo:

```markdown
# Índice

## Nivel básico

### Chapter One
- [Variables](Basico/chapter-one/variables.md)
- [Tipos de datos](Basico/chapter-one/tipos_datos.md)

## Nivel intermedio

### Chapter One
- [Funciones](Intermedio/chapter-one/funciones.md)
- [Clases y objetos](Intermedio/chapter-one/clases_objetos.md)

## Nivel avanzado

### Chapter One
- [Decoradores](Avanzado/chapter-one/decoradores.md)
```

Los enlaces deben apuntar a archivos reales. No incluyas enlaces inexistentes.

---

## 6. Fuentes y rigor técnico

La documentación debe ser técnicamente correcta y verificable.

Prioridades:

1. Documentación oficial de Python.
2. Documentación oficial de las librerías.
3. PEP (Python Enhancement Proposals), cuando sean relevantes.
4. Otras fuentes técnicas confiables únicamente cuando la documentación oficial no sea suficiente.

Reglas:

- Verifica que las funciones y características documentadas existan en la versión correspondiente.
- Distingue entre funcionalidades del lenguaje y funcionalidades de librerías externas.
- Indica cuándo una funcionalidad depende de una versión específica.
- No confundas CPython con el lenguaje Python.
- No confundas módulos de la biblioteca estándar con paquetes externos.
- No inventes comportamientos para completar una explicación.
- No copies documentación oficial literalmente: explica los conceptos con tus propias palabras y cita la fuente.
- Prioriza ejemplos compatibles con versiones actuales y estables de Python.
- Cuando existan diferencias entre implementaciones de Python, indícalas.
- Cuando una afirmación dependa de una versión concreta, identifica esa versión.
- Si el material original contiene errores conceptuales, corrígelos utilizando fuentes oficiales y explica la corrección cuando sea relevante.

---

## 7. Reglas de ejecución y protección del contenido original

Estas reglas son obligatorias:

1. `CLASES_PYTHON/` y `CLASES_PY_POO/` son exclusivamente de lectura.
2. No modifiques, elimines, renombres ni muevas archivos originales de ninguno de los dos directorios.
3. No sobrescribas archivos existentes dentro de `DOC/` sin inspeccionar primero su contenido.
4. No elimines documentación existente.
5. No generes temas sin relación con el contenido analizado, salvo los fundamentos adicionales necesarios para comprenderlo.
6. Evita generar archivos innecesarios o documentación duplicada.
7. Mantén una nomenclatura consistente.
8. Utiliza Markdown correctamente.
9. Los ejemplos de código deben ser ejecutables siempre que sea posible.
10. Comprueba los enlaces internos antes de finalizar.
11. No inventes relaciones entre temas y archivos originales.
12. Mantén la trazabilidad entre cada documento y ambas fuentes originales.
13. No clasifiques tecnologías completas en un único nivel cuando sus conceptos puedan tener dificultades diferentes.
14. No atribuyas características de CPython a todas las implementaciones de Python.
15. No sacrifiques la precisión técnica para reducir la cantidad de texto.
16. No separes artificialmente los temas según el directorio del que provienen: la documentación final debe seguir una estructura pedagógica unificada.
17. Conserva la procedencia de cada concepto aunque se integren contenidos de ambas carpetas.

---

## 8. Fase 5: Desarrollo progresivo y control de calidad

No generes toda la documentación de una sola vez sin verificar su calidad.

Trabaja por etapas:

1. Completa la auditoría de `CLASES_PYTHON/`.
2. Completa la auditoría de `CLASES_PY_POO/`.
3. Establece el inventario conjunto de temas y su clasificación.
4. Identifica duplicaciones, complementos y diferencias entre ambas fuentes.
5. Define la estructura definitiva de directorios y capítulos.
6. Crea la documentación de un capítulo.
7. Revisa los archivos generados y comprueba su calidad técnica y pedagógica.
8. Corrige errores, duplicaciones y referencias incorrectas.
9. Continúa con el siguiente capítulo.

Cada capítulo debe considerarse terminado únicamente cuando:

- Todos sus temas estén documentados.
- Los fundamentos sean correctos.
- Los ejemplos sean coherentes y estén explicados.
- Las referencias oficiales estén verificadas.
- La trazabilidad con el material original esté presente.
- Los enlaces internos funcionen.
- No existan duplicaciones innecesarias.
- La integración de ambas fuentes sea coherente.

No avances sacrificando calidad para terminar más rápido.

Si el entorno permite trabajar de manera interactiva, presenta primero el inventario y la estructura propuesta para revisión antes de comenzar la generación masiva.

Si no es posible solicitar aprobación durante la ejecución, sigue las etapas de forma autónoma y registra las decisiones tomadas.

---

## 9. Verificación final

Antes de considerar terminado el trabajo:

- Comprueba que todos los archivos de `CLASES_PYTHON/` hayan sido analizados.
- Comprueba que todos los archivos de `CLASES_PY_POO/` hayan sido analizados.
- Comprueba que los temas identificados estén documentados.
- Comprueba que cada tema tenga su estructura obligatoria.
- Comprueba que los niveles estén correctamente asignados.
- Comprueba que los capítulos tengan una secuencia pedagógica coherente.
- Comprueba que las referencias oficiales existan.
- Comprueba que los enlaces relativos funcionen.
- Comprueba que `introduccion.md` incluya todos los temas documentados.
- Comprueba que cada tema tenga trazabilidad con el material original o esté identificado como fundamento complementario.
- Comprueba que no se haya modificado ningún archivo original.
- Comprueba que no se hayan confundido funcionalidades del lenguaje, implementaciones y librerías.
- Comprueba que no existan contradicciones entre documentos.
- Comprueba que los temas repetidos entre ambas carpetas se hayan integrado correctamente.
- Comprueba que no se haya perdido información relevante al combinar las dos fuentes.

Al terminar, proporciona un informe con:

1. Cantidad de archivos originales analizados en `CLASES_PYTHON/`.
2. Cantidad de archivos originales analizados en `CLASES_PY_POO/`.
3. Temas identificados en cada fuente.
4. Temas compartidos entre ambas fuentes.
5. Cantidad total de temas documentados.
6. Distribución de temas por nivel.
7. Capítulos creados.
8. Archivos generados.
9. Temas que no pudieron documentarse y el motivo.
10. Problemas o inconsistencias encontrados.
11. Referencias oficiales utilizadas.
12. Confirmación de que ambos directorios originales permanecen intactos.

---

## 10. Criterio de calidad

Quiero una documentación con calidad de material académico y técnico, no un conjunto de apuntes superficiales.

El estudiante debe poder abrir cualquier archivo, estudiar el tema desde cero, comprender sus fundamentos, practicar con ejemplos progresivos y entender cómo aplicar ese conocimiento en proyectos reales.

La documentación debe mantener una separación rigurosa entre los fundamentos del lenguaje Python, sus implementaciones, las herramientas de su ecosistema y los principios de programación orientada a objetos.

También debe permitir identificar de dónde proviene cada concepto dentro de los dos directorios originales.

**La prioridad es la comprensión profunda, la precisión técnica, la trazabilidad, la integración de ambas fuentes y la progresión pedagógica. No la cantidad de archivos generados.**
*OJO: EL DIRECTORIO ES: `DALTO/` Y DENTRO ESTÁ `DOC/` que es donde estará los documentos.*