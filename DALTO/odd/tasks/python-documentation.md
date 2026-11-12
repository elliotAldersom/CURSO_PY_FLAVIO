# Feature: Documentación completa de Python y POO (`DALTO/DOC`)

Objetivo: construir en `DALTO/DOC/` una biblioteca académica y técnica unificada (41 archivos temáticos + `introduccion.md`), derivada de la auditoría exhaustiva de `DALTO/CLASES_PYTHON/` y `DALTO/CLASS_PY_POO/` (nombre en disco correspondiente a `DALTO/CLASES_PY_POO/` en `prompt.md`), con trazabilidad completa y rigor oficial.

## Specs vigentes (`prompt.md` + `inventario_y_estructura.md` aprobado)

- **S1 — Alcance y protección de fuentes:** `DALTO/CLASES_PYTHON/` (140 archivos) y `DALTO/CLASS_PY_POO/` (42 archivos) en modo estricto de solo lectura (integridad verificada por SHA-256). Carpetas hermanas (`INTERFAZ_GRAFICA/`, `CREAR_ARCHVO_CSV/`, etc.) fuera del alcance. Los 8 archivos previos de `DOC/Basico/` se inspeccionaron y se corrigen in situ sin eliminarlos.
- **S2 — Estructura unificada (41 temas + `introduccion.md`):**
  - `Basico/chapter-one/`: `entradas_y_salidas`, `variables`, `tipos_datos`, `operadores`, `condicionales`
  - `Basico/chapter-two/`: `bucles`, `cadenas`, `listas`
  - `Intermedio/chapter-one/`: `tuplas`, `conjuntos`, `diccionarios`, `desempaquetamiento`, `comprensiones`
  - `Intermedio/chapter-two/`: `funciones`, `ambito_variables`, `funciones_lambda`, `funciones_integradas`
  - `Intermedio/chapter-three/`: `modulos`, `paquetes`, `manejo_archivos`, `archivos_csv`, `pandas_fundamentos`, `visualizacion`
  - `Intermedio/chapter-four/`: `excepciones`, `fechas_datetime`, `decimal`, `random`
  - `Intermedio/chapter-five/`: `clases_y_objetos`, `atributos_y_metodos`, `encapsulamiento`, `herencia`, `polimorfismo`
  - `Avanzado/chapter-one/`: `decoradores`, `metodos_especiales`, `iteradores`
  - `Avanzado/chapter-two/`: `mro_herencia_multiple`, `abstraccion_abc`, `principios_solid`
  - `Avanzado/chapter-three/`: `expresiones_regulares`, `regex_avanzada`
  - `Avanzado/chapter-four/`: `pandas_avanzado`
- **S3 — Estructura obligatoria de cada tema (11 secciones):** `# <Nombre del tema>` seguido de `## 2. Introducción` a `## 11. Referencias oficiales`, con tablas `| N° | Elemento | Descripción | Ejemplo |` cuando corresponda y tres niveles progresivos (`### Básico`, `### Intermedio`, `### Avanzado`) en la sección 5.
- **S4 — Trazabilidad conjunta (sección 10):** tabla o bloques con `Directorio de origen` (`CLASES_PYTHON/` o `CLASS_PY_POO/`), ruta relativa verificada en disco, nombre del archivo, conceptos identificados y aspectos ampliados (o indicación explícita de `fundamento complementario`).
- **S5 — Rigor técnico y separación conceptual:** distinguir lenguaje Python, implementación CPython, biblioteca estándar (`builtins`, `csv`, `datetime`, `decimal`, `random`, `re`, `abc`, `sys`) y librerías externas (`pandas`, `matplotlib`, `seaborn`, `textblob`, `openai`). Nunca copiar claves `sk-proj-`. URLs oficiales verificadas.
- **S6 — `DOC/introduccion.md` (8 apartados):** 1. ¿Qué es Python? · 2. Historia de Python · 3. ¿Por qué existe Python? · 4. ¿Para qué se utiliza? · 5. Fortalezas y debilidades · 6. Cómo funciona Python · 7. Introducción a la programación orientada a objetos · 8. Índice general de documentación (enlazando los 41 temas reales).
- **S7 — Verificación final e informe de 12 puntos:** `check_doc.py --strict --exec`, verificación SHA-256 de directorios originales e informe final con los 12 puntos de la sección 9 de `prompt.md`.

## Tasks (ejecución secuencial capítulo por capítulo — Fase 5)

| ID | Capítulo / Unidad | Estado | Verificación |
|---|---|---|---|
| T1 | `DOC/Basico/chapter-one/` (revisión y ajuste de 5 archivos existentes) | [x] | `check_doc.py --exec --only=Basico/chapter-one` OK (5/5) |
| T2 | `DOC/Basico/chapter-two/` (revisión y ajuste de 3 archivos existentes) | [x] | `check_doc.py --exec --only=Basico` OK (8/8) |
| T3 | `DOC/Intermedio/chapter-one/` (5 archivos nuevos) | [x] | `check_doc.py --exec --only=Intermedio/chapter-one` OK (5/5) |
| T4 | `DOC/Intermedio/chapter-two/` (4 archivos nuevos) | [x] | `check_doc.py --exec --only=Intermedio/chapter-two` OK (4/4) |
| T5 | `DOC/Intermedio/chapter-three/` (6 archivos nuevos) | [x] | `check_doc.py --exec --only=Intermedio/chapter-three` OK (6/6) |
| T6 | `DOC/Intermedio/chapter-four/` (4 archivos nuevos) | [x] | `check_doc.py --exec --only=Intermedio/chapter-four` OK (4/4) |
| T7 | `DOC/Intermedio/chapter-five/` (5 archivos nuevos — POO base y pilares) | [x] | `check_doc.py --exec --only=Intermedio/chapter-five` OK (5/5) |
| T8 | `DOC/Avanzado/chapter-one/` (3 archivos nuevos — decoradores, dunders, iteradores) | [x] | `check_doc.py --exec --only=Avanzado/chapter-one` OK (3/3) |
| T9 | `DOC/Avanzado/chapter-two/` (3 archivos nuevos — MRO, ABC, SOLID) | [x] | `check_doc.py --exec --only=Avanzado/chapter-two` OK (3/3) |
| T10 | `DOC/Avanzado/chapter-three/` (2 archivos nuevos — regex) | [x] | `check_doc.py --exec --only=Avanzado/chapter-three` OK (2/2) |
| T11 | `DOC/Avanzado/chapter-four/` (1 archivo nuevo — `pandas_avanzado`) | [x] | `check_doc.py --exec --only=Avanzado/chapter-four` OK (1/1) |
| T12 | `DOC/introduccion.md` (8 secciones + índice navegable de 41 temas) | [x] | `check_doc.py --strict --exec` OK (41/41 enlazados) |
| T13 | Verificación global (`--strict --exec` + SHA-256) e informe final de 12 puntos | [x] | Quality gate 100% verde; diff SHA-256 vacío (196 archivos originales intactos) |
