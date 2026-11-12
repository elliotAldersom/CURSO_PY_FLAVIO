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

La documentación técnica y educativa completa construida dentro de `DALTO/DOC/` se encuentra organizada pedagógicamente en tres niveles de dificultad y doce capítulos temáticos integrados:

```
DALTO/DOC/
├── introduccion.md (este documento)
├── Basico/
│   ├── chapter-one/ (5 temas)
│   └── chapter-two/ (3 temas)
├── Intermedio/
│   ├── chapter-one/ (5 temas)
│   ├── chapter-two/ (4 temas)
│   ├── chapter-three/ (6 temas)
│   ├── chapter-four/ (4 temas)
│   └── chapter-five/ (5 temas)
└── Avanzado/
    ├── chapter-one/ (3 temas)
    ├── chapter-two/ (3 temas)
    ├── chapter-three/ (2 temas)
    └── chapter-four/ (1 tema)
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

#### Chapter Three: Módulos, persistencia, análisis y visualización de datos
- [Módulos en Python](Intermedio/chapter-three/modulos.md) — Modularización de código, sentencia `import`, resolución en `sys.modules` y `sys.path`, variables canónicas `__name__ == "__main__"` y módulos compilados en C.
- [Paquetes en Python](Intermedio/chapter-three/paquetes.md) — Organización jerárquica de proyectos, rol del archivo `__init__.py`, paquetes regulares vs paquetes de espacio de nombres (PEP 420), e importaciones relativas vs absolutas.
- [Manejo de archivos de texto en Python](Intermedio/chapter-three/manejo_archivos.md) — Manejadores de archivos nativos, modos de apertura, codificación obligatoria UTF-8, gestión segura con `with`, y punteros de lectura `seek()` y `tell()`.
- [Manejo de archivos CSV en Python](Intermedio/chapter-three/archivos_csv.md) — Procesamiento de datos tabulares mediante el módulo estándar `csv` (`reader`, `writer`, `DictReader`, `DictWriter`), delimitadores, y prevención de inyección en hojas de cálculo.
- [Fundamentos de Pandas en Python](Intermedio/chapter-three/pandas_fundamentos.md) — Biblioteca externa Pandas, estructuras `Series` y `DataFrame`, lectura con `read_csv()`, inspección, indexación con `.loc` e `.iloc`, y filtrado booleano vectorizado.
- [Visualización de datos con Matplotlib y Seaborn en Python](Intermedio/chapter-three/visualizacion.md) — Bibliotecas externas de graficación estadística: gráficos de líneas, barras, dispersión y cajas (*boxplot*), API orientada a objetos (`fig, ax`), y exportación headless a producción.

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

---

### Nivel avanzado

Orientado a la metaprogramación, el modelo de datos interno de Python, los protocolos de iteración bajo demanda, la resolución de herencia múltiple compleja, el diseño de arquitecturas desacopladas según principios SOLID, el procesamiento léxico avanzado mediante expresiones regulares y el análisis de datos de alto rendimiento.

#### Chapter One: Metaprogramación, protocolos e iteradores
- [Decoradores en Python](Avanzado/chapter-one/decoradores.md) — Clausuras avanzadas, sintaxis `@decorador`, preservación de metadatos con `@functools.wraps`, decoradores con argumentos (fábricas), decoradores apilados y decoradores de clase.
- [Métodos especiales (dunder methods) en Python](Avanzado/chapter-one/metodos_especiales.md) — Modelo de datos de Python (*Python Data Model*), métodos `__str__` y `__repr__`, sobrecarga integral de operadores aritméticos y relacionales, manejo de `NotImplemented`, y métodos de contenedor.
- [Iteradores y generadores en Python](Avanzado/chapter-one/iteradores.md) — Protocolo de iteración formal (`__iter__`, `__next__`, `StopIteration`), diseño de iterables reutilizables desacoplados de sus cursores, funciones generadoras con `yield` y consumo en flujo continuo con `itertools`.

#### Chapter Two: Arquitectura avanzada y principios SOLID
- [MRO (Method Resolution Order) y herencia múltiple en Python](Avanzado/chapter-two/mro_herencia_multiple.md) — Herencia múltiple, resolución del problema del diamante, algoritmo formal de linealización C3, inspección con `.mro()`, contrato de llamadas cooperativas con `super()`, y diseño mediante mixins.
- [Abstracción y clases abstractas con el módulo abc en Python](Avanzado/chapter-two/abstraccion_abc.md) — Módulo estándar `abc`, clase base `ABC`, decorador `@abstractmethod`, combinación de descriptores con métodos abstractos, registro de subclases virtuales, y contraste frente a `typing.Protocol`.
- [Principios SOLID en Python](Avanzado/chapter-two/principios_solid.md) — Los cinco principios arquitectónicos de diseño orientado a objetos (SRP, OCP, LSP, ISP, DIP) explicados y refactorizados en Python con inyección de dependencias y modularidad para producción.

#### Chapter Three: Expresiones regulares
- [Expresiones regulares (Regex) en Python](Avanzado/chapter-three/expresiones_regulares.md) — Módulo estándar `re`, notación cruda `r"..."`, clases de caracteres, metacaracteres, cuantificadores codiciosos y perezosos, métodos de búsqueda y reemplazo (`search`, `match`, `findall`, `sub`), e inspección de objetos `Match`.
- [Expresiones regulares avanzadas en Python](Avanzado/chapter-three/regex_avanzada.md) — Precompilación con `re.compile()`, evaluación perezosa con `re.finditer()`, grupos de captura semánticos nombrados, aserciones de ancho cero (*lookaround*), banderas de compilación y prevención de vulnerabilidades ReDoS (*Catastrophic Backtracking*).

#### Chapter Four: Análisis de datos avanzado
- [Pandas avanzado: manipulación, limpieza y escalabilidad en Python](Avanzado/chapter-four/pandas_avanzado.md) — Tratamiento riguroso de valores faltantes (`dropna`, `fillna`), deduplicación, optimización extrema de memoria con tipos categóricos (`category`), concatenación (`concat`), transformaciones con `DataFrame.map()` (reemplazo oficial de `applymap`), y procesamiento por lotes con `chunksize`.

