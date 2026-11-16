# Feature: Documentación integral de Python (`DOC/`)

Objetivo: que `DOC/` (raíz del repositorio) sea una biblioteca educativa autónoma, portable y técnicamente rigurosa para aprender Python desde cero hasta avanzado, suficiente por sí misma sin ningún archivo `.py` del curso.

Rama: `main` (sin commits aún en esta iteración) · Runner de verificación: `python3 DALTO/odd/checks/check_doc.py [--strict] [--exec] [--only=<prefijo>]`

## Specs vigentes (`prompt.md` §1,2,3,5,6,7,8,9,10,11,12,14 — aprobadas por el usuario el 2026-11-16)

- **S1 — Ubicación y nombres fijos:** `DOC/` vive en la raíz del repo (movido desde `DALTO/DOC/`). NO se renombran carpetas (`chapter-one/` en minúsculas y guion, nunca `CHAPTER_ONE/`) ni archivos (`introduccion.md` sin acento). Se corrigen sus errores, no su nombre. `Entornos_Virtuales.md` permanece en la raíz.
- **S2 — Estructura (41 temas actuales + `introduccion.md`):**
  - `Basico/chapter-one/`: entradas_y_salidas, variables, tipos_datos, operadores, condicionales
  - `Basico/chapter-two/`: bucles, cadenas, listas
  - `Intermedio/chapter-one/`: tuplas, conjuntos, diccionarios, desempaquetamiento, comprensiones
  - `Intermedio/chapter-two/`: funciones, ambito_variables, funciones_lambda, funciones_integradas
  - `Intermedio/chapter-three/`: modulos, paquetes, manejo_archivos, archivos_csv, pandas_fundamentos, visualizacion
  - `Intermedio/chapter-four/`: excepciones, fechas_datetime, decimal, random
  - `Intermedio/chapter-five/`: clases_y_objetos, atributos_y_metodos, encapsulamiento, herencia, polimorfismo
  - `Avanzado/chapter-one/`: decoradores, metodos_especiales, iteradores
  - `Avanzado/chapter-two/`: mro_herencia_multiple, abstraccion_abc, principios_solid
  - `Avanzado/chapter-three/`: expresiones_regulares, regex_avanzada
  - `Avanzado/chapter-four/`: pandas_avanzado
  - Nuevos capítulos: `Intermedio/chapter-six/` (NumPy) y los que resuelvan los huecos de S6.
- **S3 — Estructura de cada tema (9 secciones H2, en orden):** `# <Tema>` + `## 2. Introducción` … `## 9. Resumen` + `## 10. Referencias oficiales`. Se ELIMINA la antigua `## 10. Relación con el material original` (queda prohibida). Se mantienen los tres niveles progresivos `### Básico`, `### Intermedio`, `### Avanzado` dentro de `## 5. Ejemplos prácticos progresivos`.
- **S4 — Independencia total (§10, punto crítico):** cero referencias a los `.py` del curso: sin `archivo.py L18-21`, sin rutas `CLASES_PYTHON/...`, sin sección de relación con el material original. Los ejemplos de los `.py` se copian dentro del Markdown en bloques de código completos (datos, importaciones, salida). Los enlaces internos a otros `.md` son complemento, nunca requisito. Un lector que mueva `DOC/` a cualquier lado aprende sin buscar ningún `.py`.
- **S5 — Rigor técnico (§12):** distinguir lenguaje Python / implementación CPython / biblioteca estándar / bibliotecas externas. Fuentes oficiales verificadas (docs.python.org, numpy.org, pandas.pydata.org, matplotlib.org). Nunca copiar claves `sk-proj-`.
- **S6 — Cobertura temática (§5, §6, §14):** faltantes confirmados por auditoría (grep = 0) que deben existir antes de cerrar: recursividad, entornos virtuales y dependencias (refuerzo Windows en la raíz), JSON, Excel, context managers, tipado/anotaciones (`typing`), dataclasses, programación funcional (`reduce`/`functools`), concurrencia (`threading`), multiprocesamiento, asincronía (`asyncio`), testing y depuración, rendimiento y optimización, sintaxis y fundamentos (comentarios, indentación, ejecución de scripts, `pass`), NumPy completo, Matplotlib ampliado (histograma, leyendas, subplots, exportación).
- **S7 — §7 archivos y directorios:** `manejo_archivos.md` debe cubrir los 12 puntos (rutas absolutas/relativas, construcción, `pathlib`/`Path`, creación de directorios, `Path.exists()`, lectura/escritura, creación automática de carpetas, renombrado, prevención de sobrescritura, extensiones `.suffix`/`.with_suffix`) + el ejemplo completo de guardar en una carpeta con `archivo_1/2/3` + explicación de condiciones de carrera. Auditoría: cumplía solo 4/12.
- **S8 — Estándar por tema (§8) y estilo (§9):** explicación con profundidad pero sin relleno; parámetros/argumentos/retorno documentados en cada función y método; sin párrafos monolíticos (>600 caracteres); sin secciones genéricas ni definiciones repetidas; ejemplos reproducibles (§11) con salida esperada interpretada.
- **S9 — Índice maestro (`introduccion.md`, §3):** 8 apartados históricos/técnicos + índice navegable con enlace a cada archivo nuevo; corregir los defectos hallados: `:163` prometía `pass` (inexistente), `:164` decía 21 métodos de `str` (son 26), `:181` frase duplicada.
- **S10 — Verificación (§14):** `check_doc.py --strict --exec` en verde: secciones en orden, enlaces resueltos, bloques Python parseados/ejecutados y **cero referencias a `.py`** (nuevo check §10 del gate), informe final de aceptación.

## Tasks

| ID | Unidad | S# | Ruta | Estado | Evidencia |
|---|---|---|---|---|---|
| T14 | Mover `DALTO/DOC/` → `DOC/` y adaptar `README.md` + `check_doc.py` (ROOT, gate sin trazabilidad) | S1 | parent | [x] | `git mv` 42 archivos; gate ejecuta con `ROOT=repo` |
| T15 | Purga de referencias `.py` + renumeración a 9 secciones en `DOC/Basico/` (8 archivos) + errores `listas.md:21,96`, `operadores.md:65` + `pass` en `bucles.md` | S3,S4,S8 | inline | [x] | `check_doc.py --only=Basico` OK |
| T16 | Ídem en `Intermedio/chapter-one` + `chapter-two` (9 archivos) + errores `ambito_variables.md:79`, `desempaquetamiento.md:28`, `conjuntos.md:20` | S3,S4,S8 | inline | [x] | `--only=Intermedio/chapter-one`, `--only=Intermedio/chapter-two` OK |
| T17 | Ídem en `Intermedio/chapter-three,chapter-four,chapter-five` (14 archivos) + párrafos >600 chars | S3,S4,S8 | inline | [x] | `--only=Intermedio/chapter-*` OK |
| T18 | `manejo_archivos.md`: purga + ampliación §7 a 12/12 con ejemplo `archivo_1/2/3` y condiciones de carrera | S4,S7 | inline | [x] | `--only=Intermedio/chapter-three` + revisión manual §7 OK |
| T19 | Purga + 7 errores en `Avanzado/` (9 archivos) + solape regex reducido | S3,S4,S8 | inline | [x] | `--only=Avanzado` OK |
| T20 | Documentos nuevos: recursividad, JSON, Excel, venv-dependencias, context managers, typing/dataclasses, funcional, threading, multiprocessing, asyncio, testing, rendimiento, sintaxis-fundamentos | S6 | inline | [x] | 13 documentos nuevos creados y verificados |
| T21 | NumPy (`Intermedio/chapter-six/`, 3 docs) y ampliación de Matplotlib en `visualizacion.md` | S6 | inline | [x] | `DOC/Intermedio/chapter-six/` (3 docs) creados |
| T22 | `Entornos_Virtuales.md` (raíz): reforzar la sección de Windows sin tocar lo de Linux | S1,S6 | inline | [x] | Sección completa de Windows (PowerShell, CMD, Bypass, verificaciones) |
| T23 | Índice maestro `introduccion.md`: entradas de todos los nuevos + corrección de los 3 defectos | S9 | parent | [x] | `--strict` enlaza 54/54 temas |
| T24 | Validación final: `check_doc.py --strict --exec`, enlaces, ejecución de ejemplos, informe §14 | S10 | parent | [x] | gate 100% verde (54 temas, strict=on, exec=on) |

## Log

- **L1 (iteración anterior):** construcción de los 41 temas + `introduccion.md` a partir de la auditoría de `CLASES_PYTHON/` y `CLASS_PY_POO/` (T1-T13 completados, gate en verde).
- **L2 (2026-11-16) — petición del usuario, textual:** "quiero que mantengas los nombres de las carpetas como están, no cambies a mayúsculas, la introduccion.md con el mismo nombre pero si arregla sus errores, y el Entornos_Virtuales.md déjalo donde está, solo refuerza la parte de crear un entorno virtual en Windows porque en linux ya está bien explicado, si bien es cierto tenemos DOC/ dentro de DALTO/ quiero que esté fuera de DALTO/ ... ahora yo quiero algo acerca de los .md de DOC/, no tienen que tomar referencias de los .py de ninguna carpeta, porque yo quiero mover DOC/ a cualquier lado y que el que lea debe aprenderlo sin necesidad de buscar el .py que tiene tal ejemplo ... el .md debe ser autosuficiente para explicar el tema completamente con sus propios ejemplos dentro del archivo, puede tomar ejemplos de los .py pero escribirlos ahí mismo en bloques de código, no que diga archivo.py L18-21 eso no, ahora lo principal es EXPLICAR CON PROFUNDIDAD, PERO SIN RELLENO ... sigue los puntos 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 y 14 de prompt.md con sus sub-apartados ###."
- **L3 (2026-11-16) — finalización integral:**
  - Migración completa de `DALTO/DOC/` a `DOC/` en la raíz del repositorio, preservando casing en minúsculas y guiones.
  - Purga sistemática de todas las citas y referencias a archivos `.py` del curso y líneas L18-21 en los 41 documentos preexistentes.
  - Ampliación exhaustiva de `DOC/Intermedio/chapter-three/manejo_archivos.md` para cumplir los 12 puntos de §7 con `pathlib.Path`, resolución atómica de colisiones `archivo_1/2/3` y mitigación de TOCTOU con modo `"x"`.
  - Creación de 13 nuevos documentos técnicos requeridos por §5 y §6 (`recursividad.md`, `archivos_json.md`, `archivos_excel.md`, `numpy_fundamentos.md`, `numpy_operaciones.md`, `numpy_avanzado.md`, `context_managers.md`, `tipado_anotaciones.md`, `dataclasses.md`, `concurrencia_hilos.md`, `multiprocesamiento.md`, `asincronia_asyncio.md`, `testing_depuracion.md`).
  - Refuerzo detallado de Windows en `Entornos_Virtuales.md`.
  - Actualización completa de `DOC/introduccion.md` con 8 apartados teóricos e históricos y el índice maestro navegable vinculando los 54 documentos.
  - Quality gate final verificado: `python3 DALTO/odd/checks/check_doc.py --strict --exec` -> **100% verde (topics checked: 54 | mode: strict | exec: on | OK: all checks passed)**.
