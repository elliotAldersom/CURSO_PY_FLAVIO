# Documentación integral de Python y Programación Orientada a Objetos

## 1. ¿Qué es Python?

Python es un lenguaje de programación de alto nivel, de propósito general, interpretado, con tipado dinámico y fuertemente tipado. Fue concebido bajo una premisa fundamental: el código fuente se lee muchas más veces de las que se escribe, por lo que la legibilidad sintáctica y la expresividad conceptual deben primar sobre la brevedad críptica o la sobrecarga ceremonial.

Como lenguaje multiparadigma, Python no fuerza al desarrollador a adoptar una única filosofía de diseño: permite estructurar soluciones empleando programación procedural, programación orientada a objetos (POO) o elementos funcionales (funciones de orden superior, clausuras, comprensiones y generadores). Su sintaxis limpia utiliza la indentación obligatoria para delimitar bloques lógicos, eliminando llaves `{}` o palabras clave de apertura y cierre, lo que garantiza una uniformidad visual constante en proyectos individuales y colaborativos.

## 2. Historia de Python

Python fue concebido a finales de la década de 1980 por el programador neerlandés **Guido van Rossum** en el *Centrum Wiskunde & Informatica* (CWI) de Ámsterdam, Países Bajos. Su desarrollo formal comenzó en diciembre de 1989 como un proyecto personal durante las vacaciones de Navidad, buscando crear un sucesor del lenguaje educativo ABC que fuera capaz de gestionar excepciones e interactuar de forma nativa con el sistema operativo distribuido Amoeba. El nombre del lenguaje no proviene del reptil, sino del grupo humorístico británico *Monty Python*, del cual Van Rossum era ferviente seguidor.

Hitos y versiones fundamentales en su evolución:
- **Python 0.9.0 (febrero de 1991):** primera publicación pública en alt.sources. Incluía clases con herencia, manejo de excepciones, funciones y los tipos esenciales `str`, `list`, `dict`.
- **Python 1.0 (enero de 1994):** incorporó herramientas de programación funcional (`lambda`, `map`, `filter`, `reduce`). Van Rossum asumió formalmente el rol de *Benevolent Dictator For Life* (BDFL), título honorífico que conservó hasta julio de 2018 cuando delegó la gobernanza técnica en un Consejo Directivo colegiado (*Steering Council*).
- **Python 2.0 (octubre de 2000):** introdujo comprensiones de listas (PEP 202), un recolector de basura capaz de detectar ciclos cíclicos de referencias en CPython y la transición hacia un modelo de desarrollo de código abierto respaldado por la *Python Software Foundation* (PSF).
- **Python 3.0 (diciembre de 2008):** ruptura deliberada y controlada de retrocompatibilidad (*Python 3000* o *Py3k*) diseñada para subsanar defectos arquitectónicos históricos acumulados en la serie 2.x. Entre sus cambios esenciales destacan: distinción estricta entre texto Unicode (`str`) y datos binarios crudos (`bytes`), `print` convertido de sentencia a función integrada, división entera `/` que retorna `float` exacto frente a división truncada `//`, e iteradores perezosos en `range`, `zip` y vistas de diccionarios. La serie Python 2 finalizó oficialmente su ciclo de soporte (*End of Life*) el 1 de enero de 2020.
- **Python Moderno (versiones 3.8 a 3.14):** introducción de asignaciones de expresión (`:=` o walrus, PEP 572), coincidencia de patrones estructurales (`match`/`case`, PEP 634), tipado gradual estático avanzado (`typing`), soporte de zonas horarias IANA nativas (`zoneinfo`, PEP 615), mensajes de error y diagnósticos mejorados, y optimizaciones profundas de rendimiento en el intérprete CPython mediante el proyecto *Faster CPython*.

## 3. ¿Por qué existe Python?

Python surgió como respuesta directa a la brecha existente a finales de los años 80 entre dos familias extremas de lenguajes: por un lado, lenguajes compilados de bajo nivel para sistemas como C o C++, que ofrecían máximo rendimiento de máquina a costa de ciclos de desarrollo extensos, gestión manual de memoria y alta complejidad accidental; por otro lado, lenguajes de scripting o shells de sistemas operativos (como Bash o sh), idóneos para automatizar tareas inmediatas pero deficientes en estructuras de datos, manejo de errores y modularidad al escalar hacia aplicaciones complejas.

Guido van Rossum buscó un puente: un lenguaje que combinara la expresividad, rapidez de desarrollo y facilidad de lectura de un lenguaje de scripting con las capacidades modulares, estructuradas y robustas de un lenguaje de software profesional.

### Filosofía de diseño: El Zen de Python

La filosofía que guía las decisiones del lenguaje se encuentra condensada en el **PEP 20** (*The Zen of Python*), escrito por Tim Peters. Algunos de sus principios rectores más influyentes son:
- *Bello es mejor que feo:* la claridad y elegancia estética del código facilitan su razonamiento formal.
- *Explícito es mejor que implícito:* evitar comportamientos mágicos ocultos; el flujo de ejecución debe ser evidente al lector.
- *Simple es mejor que complejo; complejo es mejor que complicado:* priorizar la solución más directa; si una solución es intrínsecamente compleja por la naturaleza del dominio, debe modularizarse sin introducir enredos innecesarios.
- *La legibilidad cuenta:* la sintaxis debe asemejarse al pseudocódigo ejecutable, reduciendo la distancia cognitiva entre el algoritmo y su implementación.
- *Debería haber una —y preferiblemente solo una— manera obvia de hacerlo:* desalentar la multiplicidad caótica de formas sintácticas para resolver un mismo problema, fomentando modismos idiomáticos compartidos por toda la comunidad (*Pythonic code*).
- *Los errores nunca deberían dejarse pasar silenciosamente, a menos que hayan sido silenciados explícitamente:* favorecer el manejo estructurado de excepciones frente a códigos de retorno mágicos ignorados.

## 4. ¿Para qué se utiliza?

Gracias a su sintaxis accesible, potente biblioteca estándar (*batteries included*) y un ecosistema masivo de paquetes mantenidos por la comunidad científica y profesional (distribuidos mediante el repositorio oficial PyPI), Python es líder en diversas industrias:

1. **Desarrollo Backend y APIs web:** frameworks de grado empresarial como Django, FastAPI y Flask potencian plataformas transaccionales distribuidas, microservicios asíncronos y arquitecturas orientadas a eventos.
2. **Ciencia de datos y manipulación tabular:** librerías especializadas como NumPy (cálculo matricial optimizado en C/Fortran) y Pandas (estructuras de datos tabulares columnares) constituyen el estándar de facto en análisis exploratorio, minería de datos y procesamiento cuantitativo.
3. **Inteligencia Artificial y Machine Learning:** el ecosistema dominante de aprendizaje automático profundo (PyTorch, TensorFlow, Scikit-learn, Hugging Face Transformers) expone APIs nativas de Python como capa de abstracción orquestadora sobre motores subyacentes compilados en C++ y acelerados por GPU/TPU (CUDA).
4. **Automatización de infraestructura y scripting operativo:** scripting para administración de servidores Linux/Windows, herramientas de DevOps (Ansible, Terraform CDK, SaltStack) y extracción de información (*web scraping* con Beautiful Soup y Scrapy).
5. **Procesamiento de lenguaje natural (PLN):** librerías especializadas como NLTK, spaCy y TextBlob permiten análisis de sentimientos, tokenización léxica y clasificación textual.
6. **Visualización técnica de información:** motores gráficos como Matplotlib y Seaborn permiten representar distribuciones estadísticas, series temporales y modelos bivariados con calidad de publicación académica.
7. **Aplicaciones de escritorio e interfaces gráficas:** desarrollo multiplataforma mediante bibliotecas como Tkinter (incluida en la biblioteca estándar), PyQt y PySide.
8. **Investigación científica y bioinformática:** computación numérica avanzada (SciPy, SymPy, Biopython) utilizada en astrofísica, genómica, simulación física y modelos climáticos globales.

## 5. Fortalezas y debilidades

Una evaluación objetiva de las capacidades operativas de Python permite comprender en qué escenarios destaca y en cuáles deben evaluarse alternativas arquitectónicas:

| N° | Fortalezas | Debilidades |
|---|---|---|
| 1 | **Legibilidad y mantenibilidad excepcional:** sintaxis limpia y uniforme que minimiza la deuda técnica y reduce drásticamente el costo de incorporación de nuevos ingenieros a proyectos existentes. | **Rendimiento de CPU puro inferior frente a compilados nativos:** como lenguaje interpretado dinámico con comprobaciones en tiempo de ejecución, es más lento que C, C++, Rust o Go en cálculos intensivos basados en bucles puros. |
| 2 | **Ecosistema inmenso y maduro:** miles de librerías especializadas y probadas en producción (PyPI) para prácticamente cualquier necesidad técnica, evitando reinventar componentes base. | **Consumo de memoria elevado:** cada valor en Python es un objeto en el montículo (*heap*), lo que introduce metadatos de tipo y conteo de referencias (un entero simple ocupa 28 bytes en CPython de 64 bits frente a 8 bytes en C). |
| 3 | **Tipado dinámico ágil con tipado gradual:** prototipado veloz con opción de aplicar análisis estático riguroso mediante type hints (PEP 484) y herramientas como `mypy` o `pyright` en sistemas a gran escala. | **Detección tardía de errores de tipo en tiempo de ejecución:** sin verificadores estáticos en el pipeline de integración continua, inconsistencias de tipo en rutas condicionales poco transitadas pueden detonar como `TypeError` o `AttributeError` en producción. |
| 4 | **Biblioteca estándar completa (*batteries included*):** soporte nativo para manipulación de archivos, formatos CSV/JSON, expresiones regulares, matemáticas decimales exactas, concurrencia, criptografía y redes sin dependencias externas. | **Limitación de concurrencia multihilo ligada a CPU por el GIL:** en la implementación canónica CPython, el *Global Interpreter Lock* restringe la ejecución de código bytecode Python puro a un único núcleo físico por proceso (requiere multiprocessing o extensiones C para paralelismo real de cómputo). |
| 5 | **Interoperabilidad nativa con bajo nivel:** capacidad transparente para invocar y enlazar extensiones escritas en C, C++ y Rust (mediante CFFI, ctypes o PyO3), permitiendo delegar cuellos de botella de cómputo a capas nativas. | **No apto para entornos con restricciones extremas de tiempo real:** la recolección automática de basura y la interpretación dinámica impiden garantías de latencia determinista a nivel de microsegundos requeridas en sistemas embebidos críticos o kernels. |

## 6. Cómo funciona Python

Para comprender técnicamente el comportamiento de un programa en Python, es imprescindible distinguir tres conceptos que con frecuencia se confunden en la literatura divulgativa:

- **Lenguaje Python:** es la especificación formal sintáctica y semántica del lenguaje (documentada en el *Python Language Reference* y enriquecida a través de los PEPs).
- **Implementación de Python:** es el software concreto que ejecuta programas escritos conforme a dicha especificación. La implementación canónica y de referencia mundial es **CPython**, escrita en lenguaje C estándar. Existen implementaciones alternativas con arquitecturas distintas, como **PyPy** (intérprete con compilador JIT que optimiza bucles en caliente), **Jython** (ejecución sobre la máquina virtual de Java JVM) e **IronPython** (ejecución sobre la plataforma .NET de Microsoft).
- **Intérprete:** es la herramienta o proceso ejecutable en ejecución que procesa y traduce las instrucciones.

```
+-------------------------------------------------------------------------+
| Código fuente (.py)                                                    |
+-------------------------------------------------------------------------+
                                     |
                                     v [Compilador interno de CPython]
+-------------------------------------------------------------------------+
| Bytecode intermedio (.pyc / memoria: LOAD_FAST, BINARY_OP, etc.)       |
+-------------------------------------------------------------------------+
                                     |
                                     v [Máquina Virtual de Python - PVM]
+-------------------------------------------------------------------------+
| Ejecución en bucle de evaluación sobre CPU / SO                        |
+-------------------------------------------------------------------------+
```

### El modelo de ejecución de CPython: de código a máquina

1. **Análisis léxico y sintáctico (Parsing):** el código fuente `.py` es tokenizado y transformado en un Árbol de Sintaxis Abstracta (*Abstract Syntax Tree* o AST). En esta etapa se detectan los errores de sintaxis (`SyntaxError`).
2. **Compilación a Bytecode:** el AST es compilado internamente a una secuencia de instrucciones compactas de bajo nivel denominadas **bytecode**. El bytecode no es código máquina nativo para la CPU de la computadora (x86-64 o ARM), sino un conjunto de instrucciones diseñado para una máquina de pila virtual. Para evitar recompilaciones innecesarias en ejecuciones posteriores de módulos importados, CPython almacena este bytecode en disco dentro del directorio especial `__pycache__/` con extensión `.pyc` etiquetada por versión (por ejemplo, `.cpython-313.pyc`).
3. **Máquina Virtual de Python (PVM):** el bucle de evaluación de CPython (tradicionalmente implementado en una gran estructura de control en C) toma las instrucciones de bytecode y las ejecuta de forma secuencial, interactuando con la memoria y las llamadas al sistema del sistema operativo anfitrión.

### Gestión de memoria y recolección de basura en CPython

A diferencia de lenguajes como C donde el programador reserva (`malloc`) y libera (`free`) punteros manualmente, CPython gestiona la memoria de manera totalmente autónoma mediante una arquitectura en capas:

- **Conteo de referencias (*Reference Counting*):** es el mecanismo primario e inmediato. Todo objeto en el montículo contiene un encabezado (`PyObject`) con un contador (`ob_refcnt`). Cada vez que una variable o estructura apunta al objeto, su contador se incrementa; cuando una referencia sale de ámbito o se elimina mediante la sentencia `del`, su contador se decrementa. En el instante exacto en que `ob_refcnt` llega a cero, la memoria del objeto es liberada de inmediato.
- **Recolector de basura generacional (*Cyclic Garbage Collector*):** el conteo de referencias tiene una limitación conocida: no puede detectar ciclos de referencias aislados (por ejemplo, dos objetos que se apuntan mutuamente `a.b = b; b.a = a`, pero que ya son inalcanzables desde el programa principal). Para resolverlo, CPython incluye un recolector de basura de soporte organizado en tres generaciones (G0, G1, G2) que inspecciona periódicamente los contenedores en busca de grafos de referencias circulares huérfanos.

## 7. Introducción a la programación orientada a objetos

Un **paradigma de programación** es un marco conceptual y metodológico que define cómo el desarrollador modela la realidad, estructura sus pensamientos y organiza las instrucciones computacionales.

En el paradigma **procedural o estructurado**, el software se compone de procedimientos o funciones que operan de forma externa sobre estructuras de datos pasivas (como variables, listas o diccionarios). Si bien es intuitivo para scripts pequeños, a medida que el sistema crece este modelo genera alta fricción: los datos quedan dispersos, cualquier función puede alterar variables globales y un cambio en la estructura de un dato obliga a refactorizar decenas de procedimientos desconectados.

La **Programación Orientada a Objetos (POO)** surge para resolver este problema mediante el principio de **cohesión**: en lugar de separar los datos de las operaciones que los procesan, los agrupa en entidades integradas denominadas **objetos**. Un objeto es una unidad autónoma de software que encapsula un estado interno (atributos) y un conjunto de comportamientos asociados (métodos).

### Conceptos fundamentales

- **Clase:** es la plantilla, contrato o plano de diseño (*blueprint*) a partir del cual se construyen objetos. Define qué propiedades y métodos tendrán los elementos de esa categoría.
- **Objeto o Instancia:** es un ejemplar concreto creado en memoria en base a una clase. Cada objeto posee su propia identidad y sus propios valores de estado independientes.
- **Atributos:** variables vinculadas a un objeto o clase que representan sus características o datos internos.
- **Métodos:** funciones definidas dentro del cuerpo de una clase que describen las acciones que un objeto sabe realizar, recibiendo habitualmente una referencia explícita al propio objeto a través del parámetro `self`.

### Los cuatro pilares de la POO

1. **Abstracción:** capacidad de aislar las características esenciales de un concepto ignorando los detalles accesorios de implementación. Permite exponer una interfaz simple y expresiva hacia el exterior mientras la complejidad interna permanece oculta.
2. **Encapsulamiento:** mecanismo de agrupamiento y protección del estado interno de un objeto. Establece fronteras arquitectónicas para evitar modificaciones directas descontroladas desde el exterior, canalizando las mutaciones a través de métodos o propiedades validadas (`@property`).
3. **Herencia:** mecanismo que permite crear nuevas clases especializadas a partir de clases existentes, reutilizando y extendiendo comportamientos en una jerarquía coherente de tipo "es-un" (*is-a*).
4. **Polimorfismo:** capacidad de enviar un mismo mensaje o invocar un mismo método sobre objetos de clases diferentes y obtener respuestas particulares y coherentes en cada uno, garantizando un tratamiento uniforme a través de contratos compartidos o mediante la flexibilidad del tipado dinámico (*duck typing*).

### ¿Cuándo conviene utilizar POO?

La POO no debe imponerse por dogma en todos los problemas:
- **Es altamente recomendable:** en sistemas empresariales con dominios de negocio complejos, simulaciones de entidades interactivas, interfaces gráficas de usuario (donde botones, ventanas y formularios son naturalmente objetos jerárquicos), arquitecturas extensibles mediante plugins o adaptadores, y cuando se requiere proteger invariantes estrictos de estado.
- **Es innecesaria o contraproducente:** en scripts lineales de automatización corta, transformaciones de datos matemáticas puramente canalizadas (*data pipelines* funcionales) o tareas puntuales donde simples funciones puras ofrecen una solución más limpia, directa y verificable.

---

## 8. Índice general de documentación

La documentación técnica y educativa completa construida dentro de `DOC/` se encuentra organizada pedagógicamente en tres niveles de dificultad y catorce capítulos temáticos integrados:

```
DOC/
├── introduccion.md (este documento)
├── Basico/
│   ├── chapter-one/ (5 temas)
│   └── chapter-two/ (3 temas)
├── Intermedio/
│   ├── chapter-one/ (5 temas)
│   ├── chapter-two/ (5 temas)
│   ├── chapter-three/ (8 temas)
│   ├── chapter-four/ (4 temas)
│   ├── chapter-five/ (5 temas)
│   └── chapter-six/ (3 temas)
└── Avanzado/
    ├── chapter-one/ (4 temas)
    ├── chapter-two/ (3 temas)
    ├── chapter-three/ (2 temas)
    ├── chapter-four/ (1 tema)
    ├── chapter-five/ (2 temas)
    └── chapter-six/ (4 temas)
```

### Nivel básico

Orientado a la comprensión de los fundamentos conceptuales, la sintaxis esencial, el modelo de enlace nombre-objeto, las estructuras de control de flujo y las operaciones sobre secuencias elementales.

#### Chapter One: Fundamentos del lenguaje y control de flujo
- [Entradas y salidas en consola](Basico/chapter-one/entradas_y_salidas.md) — Flujos estándar E/S, `input()`, `print()`, formateo con f-strings y desacoplamiento de interfaz.
- [Variables y constantes en Python](Basico/chapter-one/variables.md) — Enlace de nombres en memoria, tipado dinámico, asignación aumentada `+=`, sentencia `del` y convenciones PEP 8.
- [Tipos de datos fundamentales en Python](Basico/chapter-one/tipos_datos.md) — Tipos primitivos (`int`, `float`, `str`, `bool`, `NoneType`), conversión de tipos e introspección con `type()` e `isinstance()`.
- [Operadores en Python](Basico/chapter-one/operadores.md) — Aritméticos, relacionales, lógicos, de pertenencia, tablas de verdad, precedencia formal y operadores de identidad (`is` vs `==`).
- [Estructuras condicionales en Python](Basico/chapter-one/condicionales.md) — Bloques `if`, `elif`, `else`, expresiones condicionales ternarias y coincidencia de patrones con `match`/`case`.

#### Chapter Two: Iteración y secuencias básicas
- [Bucles y estructuras de control iterativas en Python](Basico/chapter-two/bucles.md) — Bucles `while` y `for`, generador `range()`, sentencias de salto (`break`, `continue`, `pass`), y cláusulas `else` en bucles.
- [Cadenas de caracteres (strings) en Python](Basico/chapter-two/cadenas.md) — Inmutabilidad textual, indexación, rebanado (*slicing*), 21 métodos esenciales de `str`, y formateo con `.format()` y f-strings.
- [Listas en Python](Basico/chapter-two/listas.md) — Secuencias mutables, indexación positiva y negativa, métodos de mutación, y análisis de costo en la implementación CPython (`PyListObject`).

---

### Nivel intermedio

Orientado a la combinación de estructuras de datos avanzadas, abstracción procedimental, modularización del código, gestión de persistencia en disco, librerías del ecosistema de datos, tratamiento robusto de excepciones y los pilares de la programación orientada a objetos.

#### Chapter One: Estructuras de datos avanzadas y comprensiones
- [Tuplas en Python](Intermedio/chapter-one/tuplas.md) — Secuencias inmutables, empaquetado posicional por comas, tuplas unitarias, inmutabilidad estructural y optimización de memoria.
- [Conjuntos (sets) y frozensets en Python](Intermedio/chapter-one/conjuntos.md) — Colecciones desordenadas de elementos únicos, requerimiento de hashabilidad, `frozenset`, y operaciones algebraicas de conjuntos.
- [Diccionarios en Python](Intermedio/chapter-one/diccionarios.md) — Mapeos asociativos clave-valor, tablas hash, preservación del orden de inserción, vistas dinámicas y operadores de fusión `|` y `|=`.
- [Desempaquetamiento en Python](Intermedio/chapter-one/desempaquetamiento.md) — Asignación múltiple, intercambio atómico de variables, desempaquetamiento extendido con `*` (PEP 3132) y generalizaciones en llamadas (PEP 448).
- [Comprensiones en Python](Intermedio/chapter-one/comprensiones.md) — Comprensiones de listas, conjuntos y diccionarios, filtrado declarativo, y expresiones generadoras para evaluación perezosa en memoria.

#### Chapter Two: Funciones, ámbito e introspección
- [Funciones en Python](Intermedio/chapter-two/funciones.md) — Declaración con `def`, argumentos posicionales y nominales, valores por defecto mutables, `*args`, `**kwargs`, parámetros posicionales y nominales estrictos, retornos y anotaciones de tipo.
- [Ámbito y ciclo de vida de variables en Python](Intermedio/chapter-two/ambito_variables.md) — Resolución de nombres bajo la regla LEGB, análisis en tiempo de compilación de variables locales, sentencias `global` y `nonlocal`, y corrección sobre el alcance en bucles.
- [Funciones lambda en Python](Intermedio/chapter-two/funciones_lambda.md) — Funciones anónimas de expresión única, paso como parámetros de orden superior (`sorted`, `filter`, `map`), clausuras y alternativas legibles.
- [Funciones integradas (built-in functions) en Python](Intermedio/chapter-two/funciones_integradas.md) — Catálogo central de funciones en el espacio `builtins` (`abs`, `round`, `enumerate`, `zip`, `all`, `any`, `isinstance`), e implicancias de seguridad en el uso de `eval()`.
- [Recursividad y gestión de la pila en Python](Intermedio/chapter-two/recursividad.md) — Caso base, caso inductivo, pila de llamadas (*call stack*), límites de recursión (`sys.getrecursionlimit`), y optimización mediante memoización con `@functools.lru_cache`.

#### Chapter Three: Módulos, persistencia, análisis y visualización de datos
- [Módulos en Python](Intermedio/chapter-three/modulos.md) — Modularización de código, sentencia `import`, resolución en `sys.modules` y `sys.path`, variables canónicas `__name__ == "__main__"` y módulos compilados en C.
- [Paquetes en Python](Intermedio/chapter-three/paquetes.md) — Organización jerárquica de proyectos, rol del archivo `__init__.py`, paquetes regulares vs paquetes de espacio de nombres (PEP 420), e importaciones relativas vs absolutas.
- [Manejo de archivos de texto en Python](Intermedio/chapter-three/manejo_archivos.md) — Manejadores de archivos nativos, modos de apertura, codificación obligatoria UTF-8, gestión segura con `with`, y punteros de lectura `seek()` y `tell()`.
- [Manejo de archivos CSV en Python](Intermedio/chapter-three/archivos_csv.md) — Procesamiento de datos tabulares mediante el módulo estándar `csv` (`reader`, `writer`, `DictReader`, `DictWriter`), delimitadores, y prevención de inyección en hojas de cálculo.
- [Fundamentos de Pandas en Python](Intermedio/chapter-three/pandas_fundamentos.md) — Biblioteca externa Pandas, estructuras `Series` y `DataFrame`, lectura con `read_csv()`, inspección, indexación con `.loc` e `.iloc`, y filtrado booleano vectorizado.
- [Visualización de datos con Matplotlib y Seaborn en Python](Intermedio/chapter-three/visualizacion.md) — Bibliotecas externas de graficación estadística: gráficos de líneas, barras, dispersión y cajas (*boxplot*), API orientada a objetos (`fig, ax`), y exportación headless a producción.
- [Gestión y serialización de datos JSON en Python](Intermedio/chapter-three/archivos_json.md) — Módulo estándar `json`, serialización `dumps`/`loads` en memoria, `dump`/`load` en disco, correspondencia de tipos, codificadores extensibles y persistencia atómica.
- [Procesamiento de hojas de cálculo Excel en Python](Intermedio/chapter-three/archivos_excel.md) — Bibliotecas `openpyxl` y `pandas`, lectura y escritura de archivos `.xlsx`, consolidación de múltiples hojas con `ExcelWriter`, estilos y fórmulas.

#### Chapter Four: Manejo de errores y utilidades del sistema
- [Manejo de excepciones en Python](Intermedio/chapter-four/excepciones.md) — Jerarquía formal de `BaseException` y `Exception`, bloques `try`/`except`/`else`/`finally`, encadenamiento explícito de errores (`raise ... from`), y diseño de excepciones de dominio.
- [Manejo de fechas y horas con datetime en Python](Intermedio/chapter-four/fechas_datetime.md) — Módulo estándar `datetime`, objetos `date`, `time`, `datetime`, aritmética temporal con `timedelta`, formateo `strftime`/`strptime`, y zonas horarias IANA con `zoneinfo`.
- [Aritmética de precisión fija con decimal en Python](Intermedio/chapter-four/decimal.md) — Módulo estándar `decimal`, representación decimal exacta en base 10 frente a limitaciones de `float` binario IEEE 754, contextos de cálculo y políticas de redondeo contable.
- [Generación pseudoaleatoria con random en Python](Intermedio/chapter-four/random.md) — Módulo estándar `random`, generador Mersenne Twister, semillas deterministas, muestreo con y sin reemplazo, y contraste de seguridad frente al módulo estándar `secrets`.

#### Chapter Five: Programación orientada a objetos (POO)
- [Clases y objetos en Python](Intermedio/chapter-five/clases_y_objetos.md) — Paradigma de POO, definición con `class`, instanciación en memoria, método constructor `__init__`, parámetro explícito `self`, y desacoplamiento de capas.
- [Atributos y métodos en Python](Intermedio/chapter-five/atributos_y_metodos.md) — Atributos de instancia frente a atributos de clase compartidos, resolución en diccionarios `__dict__`, métodos de instancia, métodos de clase (`@classmethod`), y métodos estáticos (`@staticmethod`).
- [Encapsulamiento en Python](Intermedio/chapter-five/encapsulamiento.md) — Protección de invariantes, convención protegida `_atributo`, ofuscación de nombres (*name mangling*) `__atributo`, y propiedades idiomáticas `@property` (`getter`, `setter`, `deleter`).
- [Herencia en Python](Intermedio/chapter-five/herencia.md) — Herencia simple, jerárquica y multinivel, delegación cooperativa con `super()`, comprobación de jerarquías con `isinstance()` e `issubclass()`, y diseño por composición y agregación.
- [Polimorfismo en Python](Intermedio/chapter-five/polimorfismo.md) — Despacho polimórfico, sobrescritura de métodos (*overriding*), tipado estructural (*duck typing*), particularidades de la sobrecarga de métodos en Python, y distinción entre tipo real y tipo declarado.

#### Chapter Six: Computación numérica y matricial con NumPy
- [Fundamentos de arreglos N-dimensionales con NumPy](Intermedio/chapter-six/numpy_fundamentos.md) — Estructura `ndarray`, tipos de datos (`dtypes`), diferencias de memoria frente a listas nativas y constructores analíticos (`linspace`, `arange`, `zeros`).
- [Operaciones vectorizadas, indexación avanzada y broadcasting en NumPy](Intermedio/chapter-six/numpy_operaciones.md) — Computación vectorizada con `ufuncs`, vistas en memoria frente a copias independientes, máscaras booleanas y reglas formales de difusión (*Broadcasting*).
- [Manipulación estructural, estadística y álgebra lineal en NumPy](Intermedio/chapter-six/numpy_avanzado.md) — Reorganización con `reshape`, agregaciones estadísticas con control de `axis`, álgebra lineal con `numpy.linalg` y persistencia binaria `.npz`.

---

### Nivel avanzado

Orientado a la metaprogramación, el modelo de datos interno de Python, los protocolos de iteración bajo demanda, la resolución de herencia múltiple compleja, el diseño de arquitecturas desacopladas según principios SOLID, el procesamiento léxico avanzado mediante expresiones regulares y el análisis de datos de alto rendimiento.

#### Chapter One: Metaprogramación, protocolos e iteradores
- [Decoradores en Python](Avanzado/chapter-one/decoradores.md) — Clausuras avanzadas, sintaxis `@decorador`, preservación de metadatos con `@functools.wraps`, decoradores con argumentos (fábricas), decoradores apilados y decoradores de clase.
- [Métodos especiales (dunder methods) en Python](Avanzado/chapter-one/metodos_especiales.md) — Modelo de datos de Python (*Python Data Model*), métodos `__str__` y `__repr__`, sobrecarga integral de operadores aritméticos y relacionales, manejo de `NotImplemented`, y métodos de contenedor.
- [Iteradores y generadores en Python](Avanzado/chapter-one/iteradores.md) — Protocolo de iteración formal (`__iter__`, `__next__`, `StopIteration`), diseño de iterables reutilizables desacoplados de sus cursores, funciones generadoras con `yield` y consumo en flujo continuo con `itertools`.
- [Gestores de contexto y gestión determinista de recursos en Python](Avanzado/chapter-one/context_managers.md) — Sentencia `with`, protocolo `__enter__` y `__exit__`, supresión controlada de excepciones, decorador `@contextlib.contextmanager` y `ExitStack`.

#### Chapter Two: Arquitectura avanzada y principios SOLID
- [MRO (Method Resolution Order) y herencia múltiple en Python](Avanzado/chapter-two/mro_herencia_multiple.md) — Herencia múltiple, resolución del problema del diamante, algoritmo formal de linealización C3, inspección con `.mro()`, contrato de llamadas cooperativas con `super()`, y diseño mediante mixins.
- [Abstracción y clases abstractas con el módulo abc en Python](Avanzado/chapter-two/abstraccion_abc.md) — Módulo estándar `abc`, clase base `ABC`, decorador `@abstractmethod`, combinación de descriptores con métodos abstractos, registro de subclases virtuales, y contraste frente a `typing.Protocol`.
- [Principios SOLID en Python](Avanzado/chapter-two/principios_solid.md) — Los cinco principios arquitectónicos de diseño orientado a objetos (SRP, OCP, LSP, ISP, DIP) explicados y refactorizados en Python con inyección de dependencias y modularidad para producción.

#### Chapter Three: Expresiones regulares
- [Expresiones regulares (Regex) en Python](Avanzado/chapter-three/expresiones_regulares.md) — Módulo estándar `re`, notación cruda `r"..."`, clases de caracteres, metacaracteres, cuantificadores codiciosos y perezosos, métodos de búsqueda y reemplazo (`search`, `match`, `findall`, `sub`), e inspección de objetos `Match`.
- [Expresiones regulares avanzadas en Python](Avanzado/chapter-three/regex_avanzada.md) — Precompilación con `re.compile()`, evaluación perezosa con `re.finditer()`, grupos de captura semánticos nombrados, aserciones de ancho cero (*lookaround*), banderas de compilación y prevención de vulnerabilidades ReDoS (*Catastrophic Backtracking*).

#### Chapter Four: Análisis de datos avanzado y métodos de Pandas
- [Pandas avanzado: manipulación, limpieza y escalabilidad en Python](Avanzado/chapter-four/pandas_avanzado.md) — Tratamiento riguroso de valores faltantes (`dropna`, `fillna`), deduplicación, optimización extrema de memoria con tipos categóricos (`category`), concatenación (`concat`), transformaciones con `DataFrame.map()` (reemplazo oficial de `applymap`), y procesamiento por lotes con `chunksize`.
- [DataFrame.drop_duplicates](Avanzado/pandas/06_duplicados/drop_duplicates.md) — Identificación y descarte de registros redundantes mediante hashing en C con control de ocurrencias (`keep`) e indexación.



##### Métodos y Referencia Técnica de Pandas
- [Excel File](Avanzado/pandas/01_lectura_escritura/excel_file.md)
- [Indice](Avanzado/pandas/01_lectura_escritura/indice.md)
- [Read Csv](Avanzado/pandas/01_lectura_escritura/read_csv.md)
- [Read Excel](Avanzado/pandas/01_lectura_escritura/read_excel.md)
- [To Csv](Avanzado/pandas/01_lectura_escritura/to_csv.md)
- [To Excel](Avanzado/pandas/01_lectura_escritura/to_excel.md)
- [Columns](Avanzado/pandas/02_inspeccion_exploracion/columns.md)
- [Describe](Avanzado/pandas/02_inspeccion_exploracion/describe.md)
- [Dtypes](Avanzado/pandas/02_inspeccion_exploracion/dtypes.md)
- [Head](Avanzado/pandas/02_inspeccion_exploracion/head.md)
- [Indice](Avanzado/pandas/02_inspeccion_exploracion/indice.md)
- [Info](Avanzado/pandas/02_inspeccion_exploracion/info.md)
- [Isna](Avanzado/pandas/02_inspeccion_exploracion/isna.md)
- [Nunique](Avanzado/pandas/02_inspeccion_exploracion/nunique.md)
- [Sample](Avanzado/pandas/02_inspeccion_exploracion/sample.md)
- [Shape](Avanzado/pandas/02_inspeccion_exploracion/shape.md)
- [Tail](Avanzado/pandas/02_inspeccion_exploracion/tail.md)
- [Value Counts](Avanzado/pandas/02_inspeccion_exploracion/value_counts.md)
- [Between](Avanzado/pandas/03_seleccion_filtrado/between.md)
- [Filtrado Booleano](Avanzado/pandas/03_seleccion_filtrado/filtrado_booleano.md)
- [Iloc](Avanzado/pandas/03_seleccion_filtrado/iloc.md)
- [Indice](Avanzado/pandas/03_seleccion_filtrado/indice.md)
- [Isin](Avanzado/pandas/03_seleccion_filtrado/isin.md)
- [Loc](Avanzado/pandas/03_seleccion_filtrado/loc.md)
- [Query](Avanzado/pandas/03_seleccion_filtrado/query.md)
- [Str Contains](Avanzado/pandas/03_seleccion_filtrado/str_contains.md)
- [Idxmax](Avanzado/pandas/04_ordenamiento_indices/idxmax.md)
- [Idxmin](Avanzado/pandas/04_ordenamiento_indices/idxmin.md)
- [Indice](Avanzado/pandas/04_ordenamiento_indices/indice.md)
- [Nlargest](Avanzado/pandas/04_ordenamiento_indices/nlargest.md)
- [Nsmallest](Avanzado/pandas/04_ordenamiento_indices/nsmallest.md)
- [Rank](Avanzado/pandas/04_ordenamiento_indices/rank.md)
- [Reset Index](Avanzado/pandas/04_ordenamiento_indices/reset_index.md)
- [Set Index](Avanzado/pandas/04_ordenamiento_indices/set_index.md)
- [Sort Values](Avanzado/pandas/04_ordenamiento_indices/sort_values.md)
- [Apply](Avanzado/pandas/05_limpieza_transformacion/apply.md)
- [Assign](Avanzado/pandas/05_limpieza_transformacion/assign.md)
- [Astype](Avanzado/pandas/05_limpieza_transformacion/astype.md)
- [Cut](Avanzado/pandas/05_limpieza_transformacion/cut.md)
- [Dropna](Avanzado/pandas/05_limpieza_transformacion/dropna.md)
- [Fillna](Avanzado/pandas/05_limpieza_transformacion/fillna.md)
- [Indice](Avanzado/pandas/05_limpieza_transformacion/indice.md)
- [Map](Avanzado/pandas/05_limpieza_transformacion/map.md)
- [Pipe](Avanzado/pandas/05_limpieza_transformacion/pipe.md)
- [Qcut](Avanzado/pandas/05_limpieza_transformacion/qcut.md)
- [Rename](Avanzado/pandas/05_limpieza_transformacion/rename.md)
- [Replace](Avanzado/pandas/05_limpieza_transformacion/replace.md)
- [Str Lower](Avanzado/pandas/05_limpieza_transformacion/str_lower.md)
- [Str Strip](Avanzado/pandas/05_limpieza_transformacion/str_strip.md)
- [Str Title](Avanzado/pandas/05_limpieza_transformacion/str_title.md)
- [To Numeric](Avanzado/pandas/05_limpieza_transformacion/to_numeric.md)
- [Duplicated](Avanzado/pandas/06_duplicados/duplicated.md)
- [Indice](Avanzado/pandas/06_duplicados/indice.md)
- [Agg](Avanzado/pandas/07_agrupacion_agregacion/agg.md)
- [Crosstab](Avanzado/pandas/07_agrupacion_agregacion/crosstab.md)
- [Cumsum](Avanzado/pandas/07_agrupacion_agregacion/cumsum.md)
- [Groupby](Avanzado/pandas/07_agrupacion_agregacion/groupby.md)
- [Indice](Avanzado/pandas/07_agrupacion_agregacion/indice.md)
- [Mean](Avanzado/pandas/07_agrupacion_agregacion/mean.md)
- [Median](Avanzado/pandas/07_agrupacion_agregacion/median.md)
- [Pivot Table](Avanzado/pandas/07_agrupacion_agregacion/pivot_table.md)
- [Quantile](Avanzado/pandas/07_agrupacion_agregacion/quantile.md)
- [Std](Avanzado/pandas/07_agrupacion_agregacion/std.md)
- [Sum](Avanzado/pandas/07_agrupacion_agregacion/sum.md)
- [Diff](Avanzado/pandas/08_fechas_series_tiempo/diff.md)
- [Dt Accessor](Avanzado/pandas/08_fechas_series_tiempo/dt_accessor.md)
- [Dt Day Names](Avanzado/pandas/08_fechas_series_tiempo/dt_day_names.md)
- [Dt Isocalendar](Avanzado/pandas/08_fechas_series_tiempo/dt_isocalendar.md)
- [Dt To Period](Avanzado/pandas/08_fechas_series_tiempo/dt_to_period.md)
- [Dt Year Month](Avanzado/pandas/08_fechas_series_tiempo/dt_year_month.md)
- [Indice](Avanzado/pandas/08_fechas_series_tiempo/indice.md)
- [Resample](Avanzado/pandas/08_fechas_series_tiempo/resample.md)
- [To Datetime](Avanzado/pandas/08_fechas_series_tiempo/to_datetime.md)
- [Concat](Avanzado/pandas/09_combinacion_reestructuracion/concat.md)
- [Indice](Avanzado/pandas/09_combinacion_reestructuracion/indice.md)
- [Melt](Avanzado/pandas/09_combinacion_reestructuracion/melt.md)
- [Merge](Avanzado/pandas/09_combinacion_reestructuracion/merge.md)
- [Corr](Avanzado/pandas/10_estadistica/corr.md)
- [Indice](Avanzado/pandas/10_estadistica/indice.md)
- [Fundamentos Pandas](Avanzado/pandas/fundamentos_pandas.md)
- [Indice](Avanzado/pandas/indice.md)

#### Chapter Five: Tipado estático y modelado de datos
- [Sistema de tipos gradual y anotaciones de tipos en Python](Avanzado/chapter-five/tipado_anotaciones.md) — Tipado gradual (PEP 484), uniones modernas con `|`, contenedores genéricos, `Callable`, `TypeVar`, `Generic` y protocolos estructurales (PEP 544).
- [Clases de datos declarativas con dataclasses en Python](Avanzado/chapter-five/dataclasses.md) — Decorador `@dataclass`, campos tipados con `field()`, inmutabilidad con `frozen=True`, ordenamiento por valor y ganchos con `__post_init__`.

#### Chapter Six: Concurrencia, asincronía y calidad de software
- [Concurrencia con hilos y exclusión mutua en Python](Avanzado/chapter-six/concurrencia_hilos.md) — Modelo multihilo con `threading` y `ThreadPoolExecutor`, naturaleza del GIL en CPython, condiciones de carrera y sincronización con `Lock`.
- [Paralelismo real y cómputo intensivo con multiprocessing en Python](Avanzado/chapter-six/multiprocesamiento.md) — Evasión del GIL para tareas CPU-bound, métodos `spawn` vs `fork`, comunicación IPC con `Queue` y `ProcessPoolExecutor`.
- [Programación asíncrona cooperativa con asyncio en Python](Avanzado/chapter-six/asincronia_asyncio.md) — Bucle de eventos, corrutinas con `async def` y `await`, orquestación concurrente con `gather`, colas asíncronas y cancelación limpia de tareas.
- [Pruebas automatizadas y depuración en Python](Avanzado/chapter-six/testing_depuracion.md) — Frameworks `unittest` y `pytest`, dobles de prueba con `unittest.mock`, fixtures temporales seguras y depuración interactiva con `pdb` y `breakpoint()`.



##### Métodos y Referencia Técnica de NumPy
- [Arange](Avanzado/numpy/01_creacion_arreglos/arange.md)
- [Array](Avanzado/numpy/01_creacion_arreglos/array.md)
- [Eye](Avanzado/numpy/01_creacion_arreglos/eye.md)
- [Full](Avanzado/numpy/01_creacion_arreglos/full.md)
- [Indice](Avanzado/numpy/01_creacion_arreglos/indice.md)
- [Linspace](Avanzado/numpy/01_creacion_arreglos/linspace.md)
- [Ones](Avanzado/numpy/01_creacion_arreglos/ones.md)
- [Zeros](Avanzado/numpy/01_creacion_arreglos/zeros.md)
- [Add](Avanzado/numpy/05_operaciones_vectorizadas/add.md)
- [Broadcasting](Avanzado/numpy/05_operaciones_vectorizadas/broadcasting.md)
- [Indice](Avanzado/numpy/05_operaciones_vectorizadas/indice.md)
- [Multiply](Avanzado/numpy/05_operaciones_vectorizadas/multiply.md)
- [Power](Avanzado/numpy/05_operaciones_vectorizadas/power.md)
- [Argmin Argmax](Avanzado/numpy/06_estadistica_agregacion/argmin_argmax.md)
- [Indice](Avanzado/numpy/06_estadistica_agregacion/indice.md)
- [Mean](Avanzado/numpy/06_estadistica_agregacion/mean.md)
- [Median](Avanzado/numpy/06_estadistica_agregacion/median.md)
- [Min Max](Avanzado/numpy/06_estadistica_agregacion/min_max.md)
- [Std](Avanzado/numpy/06_estadistica_agregacion/std.md)
- [Sum](Avanzado/numpy/06_estadistica_agregacion/sum.md)
- [Det](Avanzado/numpy/07_algebra_lineal/det.md)
- [Dot](Avanzado/numpy/07_algebra_lineal/dot.md)
- [Indice](Avanzado/numpy/07_algebra_lineal/indice.md)
- [Inv](Avanzado/numpy/07_algebra_lineal/inv.md)
- [Matmul](Avanzado/numpy/07_algebra_lineal/matmul.md)
- [Argsort](Avanzado/numpy/08_busqueda_ordenamiento/argsort.md)
- [Indice](Avanzado/numpy/08_busqueda_ordenamiento/indice.md)
- [Select](Avanzado/numpy/08_busqueda_ordenamiento/select.md)
- [Sort](Avanzado/numpy/08_busqueda_ordenamiento/sort.md)
- [Unique](Avanzado/numpy/08_busqueda_ordenamiento/unique.md)
- [Where](Avanzado/numpy/08_busqueda_ordenamiento/where.md)
- [Fundamentos Numpy](Avanzado/numpy/fundamentos_numpy.md)
- [Indice](Avanzado/numpy/indice.md)

##### Métodos y Referencia Técnica de OpenPyXL

- [Indice](Avanzado/openpyxl/01_libro_hojas/indice.md)
- [Load Workbook](Avanzado/openpyxl/01_libro_hojas/load_workbook.md)
- [Workbook](Avanzado/openpyxl/01_libro_hojas/workbook.md)
- [Append](Avanzado/openpyxl/02_lectura_escritura_celdas/append.md)
- [Cell Access](Avanzado/openpyxl/02_lectura_escritura_celdas/cell_access.md)
- [Indice](Avanzado/openpyxl/02_lectura_escritura_celdas/indice.md)
- [Font](Avanzado/openpyxl/03_estilos_formato/font.md)
- [Indice](Avanzado/openpyxl/03_estilos_formato/indice.md)
- [Pattern Fill](Avanzado/openpyxl/03_estilos_formato/pattern_fill.md)
- [Column Dimensions](Avanzado/openpyxl/04_formulas_dimensiones/column_dimensions.md)
- [Formulas Nativas](Avanzado/openpyxl/04_formulas_dimensiones/formulas_nativas.md)
- [Indice](Avanzado/openpyxl/04_formulas_dimensiones/indice.md)
- [Fundamentos Openpyxl](Avanzado/openpyxl/fundamentos_openpyxl.md)
- [Indice](Avanzado/openpyxl/indice.md)

##### Métodos y Referencia Técnica de Matplotlib

- [Figure](Avanzado/matplotlib/01_figura_ejes/figure.md)
- [Indice](Avanzado/matplotlib/01_figura_ejes/indice.md)
- [Set Title Labels](Avanzado/matplotlib/01_figura_ejes/set_title_labels.md)
- [Subplots](Avanzado/matplotlib/01_figura_ejes/subplots.md)
- [Bar](Avanzado/matplotlib/02_graficos_basicos/bar.md)
- [Hist](Avanzado/matplotlib/02_graficos_basicos/hist.md)
- [Indice](Avanzado/matplotlib/02_graficos_basicos/indice.md)
- [Plot](Avanzado/matplotlib/02_graficos_basicos/plot.md)
- [Scatter](Avanzado/matplotlib/02_graficos_basicos/scatter.md)
- [Grid](Avanzado/matplotlib/03_personalizacion_estilos/grid.md)
- [Indice](Avanzado/matplotlib/03_personalizacion_estilos/indice.md)
- [Legend](Avanzado/matplotlib/03_personalizacion_estilos/legend.md)
- [Set Lim](Avanzado/matplotlib/03_personalizacion_estilos/set_lim.md)
- [Indice](Avanzado/matplotlib/04_exportacion_composicion/indice.md)
- [Savefig](Avanzado/matplotlib/04_exportacion_composicion/savefig.md)
- [Tight Layout](Avanzado/matplotlib/04_exportacion_composicion/tight_layout.md)
- [Fundamentos Matplotlib](Avanzado/matplotlib/fundamentos_matplotlib.md)
- [Indice](Avanzado/matplotlib/indice.md)

##### Métodos y Referencia Técnica de Seaborn

- [Ecdfplot](Avanzado/seaborn/01_distribuciones/ecdfplot.md)
- [Histplot](Avanzado/seaborn/01_distribuciones/histplot.md)
- [Indice](Avanzado/seaborn/01_distribuciones/indice.md)
- [Kdeplot](Avanzado/seaborn/01_distribuciones/kdeplot.md)
- [Barplot](Avanzado/seaborn/02_categoricos/barplot.md)
- [Boxplot](Avanzado/seaborn/02_categoricos/boxplot.md)
- [Countplot](Avanzado/seaborn/02_categoricos/countplot.md)
- [Indice](Avanzado/seaborn/02_categoricos/indice.md)
- [Violinplot](Avanzado/seaborn/02_categoricos/violinplot.md)
- [Indice](Avanzado/seaborn/03_relacionales/indice.md)
- [Lineplot](Avanzado/seaborn/03_relacionales/lineplot.md)
- [Scatterplot](Avanzado/seaborn/03_relacionales/scatterplot.md)
- [Heatmap](Avanzado/seaborn/04_matrices_multivariados/heatmap.md)
- [Indice](Avanzado/seaborn/04_matrices_multivariados/indice.md)
- [Pairplot](Avanzado/seaborn/04_matrices_multivariados/pairplot.md)
- [Fundamentos Seaborn](Avanzado/seaborn/fundamentos_seaborn.md)
- [Indice](Avanzado/seaborn/indice.md)

##### Métodos y Referencia Técnica de Scikit-learn

- [Indice](Avanzado/scikit_learn/01_preprocesamiento/indice.md)
- [One Hot Encoder](Avanzado/scikit_learn/01_preprocesamiento/one_hot_encoder.md)
- [Simple Imputer](Avanzado/scikit_learn/01_preprocesamiento/simple_imputer.md)
- [Standard Scaler](Avanzado/scikit_learn/01_preprocesamiento/standard_scaler.md)
- [Cross Val Score](Avanzado/scikit_learn/02_particion_seleccion/cross_val_score.md)
- [Grid Search Cv](Avanzado/scikit_learn/02_particion_seleccion/grid_search_cv.md)
- [Indice](Avanzado/scikit_learn/02_particion_seleccion/indice.md)
- [Train Test Split](Avanzado/scikit_learn/02_particion_seleccion/train_test_split.md)
- [Decision Tree](Avanzado/scikit_learn/03_estimadores_clasicos/decision_tree.md)
- [Indice](Avanzado/scikit_learn/03_estimadores_clasicos/indice.md)
- [Kmeans](Avanzado/scikit_learn/03_estimadores_clasicos/kmeans.md)
- [Linear Regression](Avanzado/scikit_learn/03_estimadores_clasicos/linear_regression.md)
- [Logistic Regression](Avanzado/scikit_learn/03_estimadores_clasicos/logistic_regression.md)
- [Random Forest](Avanzado/scikit_learn/03_estimadores_clasicos/random_forest.md)
- [Classification Report](Avanzado/scikit_learn/04_metricas_evaluacion/classification_report.md)
- [Confusion Matrix](Avanzado/scikit_learn/04_metricas_evaluacion/confusion_matrix.md)
- [Indice](Avanzado/scikit_learn/04_metricas_evaluacion/indice.md)
- [Mean Squared Error](Avanzado/scikit_learn/04_metricas_evaluacion/mean_squared_error.md)
- [Column Transformer](Avanzado/scikit_learn/05_pipelines/column_transformer.md)
- [Indice](Avanzado/scikit_learn/05_pipelines/indice.md)
- [Pipeline](Avanzado/scikit_learn/05_pipelines/pipeline.md)
- [Fundamentos Scikit Learn](Avanzado/scikit_learn/fundamentos_scikit_learn.md)
- [Indice](Avanzado/scikit_learn/indice.md)

##### Métodos y Referencia Técnica de FastAPI

- [Apirouter](Avanzado/fastapi/01_aplicacion_enrutamiento/apirouter.md)
- [Endpoints](Avanzado/fastapi/01_aplicacion_enrutamiento/endpoints.md)
- [Fastapi App](Avanzado/fastapi/01_aplicacion_enrutamiento/fastapi_app.md)
- [Indice](Avanzado/fastapi/01_aplicacion_enrutamiento/indice.md)
- [Indice](Avanzado/fastapi/02_parametros_validacion/indice.md)
- [Path Params](Avanzado/fastapi/02_parametros_validacion/path_params.md)
- [Query Params](Avanzado/fastapi/02_parametros_validacion/query_params.md)
- [Request Body](Avanzado/fastapi/02_parametros_validacion/request_body.md)
- [Depends](Avanzado/fastapi/03_inyeccion_dependencias/depends.md)
- [Indice](Avanzado/fastapi/03_inyeccion_dependencias/indice.md)
- [Security](Avanzado/fastapi/03_inyeccion_dependencias/security.md)
- [Http Exception](Avanzado/fastapi/04_respuestas_errores/http_exception.md)
- [Indice](Avanzado/fastapi/04_respuestas_errores/indice.md)
- [Response Model](Avanzado/fastapi/04_respuestas_errores/response_model.md)
- [Fundamentos Fastapi](Avanzado/fastapi/fundamentos_fastapi.md)
- [Indice](Avanzado/fastapi/indice.md)

##### Métodos y Referencia Técnica de PyTorch

- [Cuda Device](Avanzado/pytorch/01_tensores_operaciones/cuda_device.md)
- [Indice](Avanzado/pytorch/01_tensores_operaciones/indice.md)
- [Tensor Creation](Avanzado/pytorch/01_tensores_operaciones/tensor_creation.md)
- [Tensor Ops](Avanzado/pytorch/01_tensores_operaciones/tensor_ops.md)
- [Backward](Avanzado/pytorch/02_autograd_diferenciacion/backward.md)
- [Grad](Avanzado/pytorch/02_autograd_diferenciacion/grad.md)
- [Indice](Avanzado/pytorch/02_autograd_diferenciacion/indice.md)
- [No Grad](Avanzado/pytorch/02_autograd_diferenciacion/no_grad.md)
- [Indice](Avanzado/pytorch/03_modulos_redes/indice.md)
- [Linear Layer](Avanzado/pytorch/03_modulos_redes/linear_layer.md)
- [Nn Module](Avanzado/pytorch/03_modulos_redes/nn_module.md)
- [Sequential](Avanzado/pytorch/03_modulos_redes/sequential.md)
- [Dataloader](Avanzado/pytorch/04_optimizacion_entrenamiento/dataloader.md)
- [Indice](Avanzado/pytorch/04_optimizacion_entrenamiento/indice.md)
- [Loss Functions](Avanzado/pytorch/04_optimizacion_entrenamiento/loss_functions.md)
- [Optimizer Step](Avanzado/pytorch/04_optimizacion_entrenamiento/optimizer_step.md)
- [Fundamentos Pytorch](Avanzado/pytorch/fundamentos_pytorch.md)
- [Indice](Avanzado/pytorch/indice.md)

##### Métodos y Referencia Técnica de SQLAlchemy 2.0

- [Connection Execute](Avanzado/sqlalchemy/01_motor_conexiones/connection_execute.md)
- [Create Engine](Avanzado/sqlalchemy/01_motor_conexiones/create_engine.md)
- [Indice](Avanzado/sqlalchemy/01_motor_conexiones/indice.md)
- [Declarative Base](Avanzado/sqlalchemy/02_declarative_orm/declarative_base.md)
- [Indice](Avanzado/sqlalchemy/02_declarative_orm/indice.md)
- [Mapped Column](Avanzado/sqlalchemy/02_declarative_orm/mapped_column.md)
- [Relationship](Avanzado/sqlalchemy/02_declarative_orm/relationship.md)
- [Indice](Avanzado/sqlalchemy/03_sesion_transacciones/indice.md)
- [Session](Avanzado/sqlalchemy/03_sesion_transacciones/session.md)
- [Session Commit Rollback](Avanzado/sqlalchemy/03_sesion_transacciones/session_commit_rollback.md)
- [Indice](Avanzado/sqlalchemy/04_consultas_crud/indice.md)
- [Insert Update Delete](Avanzado/sqlalchemy/04_consultas_crud/insert_update_delete.md)
- [Scalars All](Avanzado/sqlalchemy/04_consultas_crud/scalars_all.md)
- [Select Where](Avanzado/sqlalchemy/04_consultas_crud/select_where.md)
- [Fundamentos Sqlalchemy](Avanzado/sqlalchemy/fundamentos_sqlalchemy.md)
- [Indice](Avanzado/sqlalchemy/indice.md)

---

## 9. Ruta pedagógica escalonada: De los fundamentos a Machine Learning y Backend

En la ingeniería de software y la ciencia de datos profesional existe un principio innegociable: **los atajos son una ilusión y saltarse los fundamentos técnicos genera deuda técnica irreparable**. Intentar programar redes neuronales en PyTorch o construir microservicios en FastAPI sin dominar la memoria contigua, la vectorización o el bucle de eventos conduce inevitablemente a código ineficiente, frágil y opaco.

Para maximizar el aprendizaje sin lagunas conceptuales, el estudio del nivel avanzado debe seguir estrictamente esta ruta escalonada en cuatro niveles:

```text
[ Nivel 0: Dominio del Núcleo de Python ]
   │  - POO estricta, Decoradores, Metodología Dunder, Context Managers
   │  - Tipado gradual (typing), Dataclasses, Concurrencia (threading/asyncio)
   ▼
[ Nivel 1: Cómputo Matricial y Vectorial (NumPy) ]
   │  - Arreglos contiguos en memoria C (ndarray), tipos físicos homogéneos
   │  - Broadcasting, álgebra lineal, operaciones sin bucles de Python
   ▼
[ Nivel 2: Ingeniería y Manipulación Tabular (Pandas y OpenPyXL) ]
   │  - Series y DataFrames, alineación automática por índice
   │  - Limpieza defensiva de nulos, agregaciones grupales, I/O con CSV/Excel
   ▼
[ Nivel 3: Análisis Exploratorio Visual (Matplotlib y Seaborn) ]
   │  - Diagnóstico visual de distribuciones, outliers y correlaciones
   │  - Gráficos con la API orientada a objetos (fig, ax) listos para producción
   ▼
[ Nivel 4: Especialización Técnica ]
   ├───────────────────────────────────────────┬───────────────────────────────────────────┐
   │                                           │                                           │
   ▼ RUTA MACHINE LEARNING & DEEP LEARNING     ▼ RUTA BACKEND & ARQUITECTURA DISTRIBUIDA   │
   1. Scikit-learn (ML Clásico y Pipelines)    1. Tipado Gradual y Modelado Pydantic       │
   2. XGBoost / LightGBM (Gradient Boosting)   2. Persistencia y ORM con SQLAlchemy 2.0    │
   3. PyTorch (Tensores GPU, Redes Profundas)  3. Microservicios Asíncronos con FastAPI     │
   4. Hugging Face (NLP, LLMs y Fine-Tuning)   4. Testing Riguroso (pytest) y Docker       │
```

### Justificación técnica del orden escalonado

1. **¿Por qué NumPy antes que Pandas?**
   Pandas está construido directamente sobre NumPy. Si no comprendés cómo funciona un arreglo `ndarray`, qué es una vista en memoria frente a una copia o cómo opera el *broadcasting*, serás incapaz de razonar sobre el consumo de memoria de un `DataFrame` o resolver advertencias críticas como `SettingWithCopyWarning`.
2. **¿Por qué Pandas antes que Scikit-learn?**
   En problemas de negocio reales, el 80% del tiempo de un proyecto de Machine Learning se invierte en la ingesta, limpieza, imputación de nulos, codificación de variables y deduplicación. Scikit-learn espera datos numéricos y limpios; pasarle datos sin dominar Pandas conduce a fallos continuos de preprocesamiento.
3. **¿Por qué Scikit-learn antes que PyTorch?**
   Scikit-learn enseña la disciplina del aprendizaje automático: división no contaminada de datos (`train_test_split`), validación cruzada (*cross-validation*), métricas de evaluación rigurosas (precisión, sensibilidad, ROC-AUC) y la abstracción universal de producción `fit()`/`predict()`. Saltar directamente a Deep Learning sin entender el sobreajuste (*overfitting*), la regularización o el balance de clases en modelos lineales o de árboles genera redes complejas que aprenden ruido.
4. **¿Por qué Concurrencia y Tipado antes que FastAPI?**
   FastAPI no es una caja negra: es una arquitectura asíncrona sobre Starlette y Pydantic. Quien no domina corrutinas (`async`/`await`), gestores de contexto asíncronos y anotaciones de tipo avanzadas (`Union`, `TypeVar`, `Annotated`) termina bloqueando el bucle de eventos del servidor con operaciones síncronas que colapsan la latencia del sistema.


