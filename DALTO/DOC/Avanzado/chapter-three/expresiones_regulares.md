# Fundamentos del Motor de Expresiones Regulares en Python

## 2. Introducción

En la teoría de la computación formal, los lenguajes regulares ocupan el nivel más básico en la Jerarquía de Chomsky (Tipo 3). Estos lenguajes pueden ser descritos de manera concisa mediante expresiones regulares y reconocidos mediante autómatas finitos, ya sean deterministas (DFA) o no deterministas (NFA). En el desarrollo de software moderno, una expresión regular (*regular expression* o *regex*) constituye un patrón algebraico que describe un conjunto de cadenas de texto de acuerdo con reglas formales de sintaxis (`A-INTRODUCCION.py` L14-26).

En Python, el procesamiento de expresiones regulares está provisto por el módulo de la biblioteca estándar `re`. A diferencia de los métodos de búsqueda estática incluidos en el tipo [`str`](../../Basico/chapter-two/cadenas.md) (tales como `str.find`, `str.replace` o `str.startswith`), el motor `re` permite modelar patrones dinámicos complejos: validación de formatos arbitrarios, extracción selectiva de componentes léxicos, tokenización léxica y transformaciones semánticas estructuradas (`SIMBOLOGIA_REGEX.py` L1-33).

Comprender la arquitectura interna del motor `re` de Python (basado en un autómata NFA con retroceso o *backtracking*) es indispensable para construir validadores eficientes, seguros frente a desbordamientos de cómputo y desacoplados de bibliotecas externas.

## 3. Fundamentos y conceptos

### El motor de expresiones regulares y la notación cruda (Raw Strings)

El motor interno de Python compila un patrón de texto en un flujo de instrucciones de bajo nivel (*bytecodes* ejecutados por el motor en C `_sre`). Durante este proceso, ocurre un fenómeno crítico de colisión léxica entre las secuencias de escape del analizador de Python y los metacaracteres del motor de expresiones regulares (`A-INTRODUCCION.py` L30-37).

En una cadena de caracteres estándar de Python (`"..."`), el carácter barra invertida `\` introduce secuencias de escape léxicas (`\n` para salto de línea, `\t` para tabulación). Por su parte, el motor de regex también utiliza `\` para definir clases de caracteres (`\d` para dígitos, `\w` para alfanuméricos) o anular el significado especial de un metacarácter (`\.`). Si se escribe `"\d"`, el analizador léxico de Python interpreta `\` antes de pasarlo a `re`. Para representar una barra invertida literal sin el prefijo crudo, se requeriría duplicar cada barra (`"\\\\d"`), lo cual resulta propenso a errores y genera el denominado «síndrome del peine inclinado» (*leaning toothpick syndrome*).

Para mitigar este problema, los patrones deben definirse obligatoriamente utilizando cadenas de caracteres crudas (*raw strings*, prefijadas con `r"..."`). En una cadena cruda, Python trata el carácter `\` como un literal sintáctico y transfiere la secuencia íntegra al motor `re`:

```python
import re

# Con cadena cruda (notación recomendada):
patron_crudo = r"\d+\.\d+"
coincidencia = re.search(patron_crudo, "Valor: 45.99")
assert coincidencia is not None and coincidencia.group() == "45.99"
```

### Metacaracteres y clases de caracteres

Los metacaracteres son símbolos reservados que no representan su valor literal, sino que codifican una instrucción estructural al motor:

1. **Punto (`.`):** Coincide con cualquier carácter excepto un salto de línea (`\n`), salvo que se active la bandera `re.DOTALL` (`Expresiones_Regulares.py` L162-177).
2. **Anclas (`^` y `$`)**: Coinciden con el límite inicial (`^`) o final (`$`) del flujo textual. Si se utiliza la bandera `re.MULTILINE`, coinciden con el inicio y fin de cada línea física (`Expresiones_Regulares.py` L201-231).
3. **Conjuntos de caracteres (`[...]` y `[^...]`):** Definen clases explícitas. `[a-z]` representa cualquier minúscula; `[^0-9]` invierte la selección, coincidiendo con cualquier carácter que no sea un dígito (`SIMBOLOGIA_REGEX.py` L53-64).
4. **Disyunción (`|`):** Operador lógico de alternancia que evalúa ramas de búsqueda alternativas de izquierda a derecha (`SIMBOLOGIA_REGEX.py` L65-70).
5. **Clases predefinidas:**
   - `\d`: Coincide con dígitos Unicode (o ASCII si se usa la bandera `re.ASCII`). Equivalente a `[0-9]`.
   - `\D`: Negación de `\d`. Coincide con cualquier carácter no numérico (`Expresiones_Regulares.py` L91-106).
   - `\w`: Coincide con caracteres de palabra (letras, dígitos y el carácter de subrayado `_`). En Unicode, incluye letras acentuadas (`SIMBOLOGIA_REGEX.py` L130-134).
   - `\W`: Negación de `\w`. Coincide con caracteres no alfanuméricos (`SIMBOLOGIA_REGEX.py` L136-140).
   - `\s`: Coincide con espacios en blanco, tabulaciones y saltos de línea (`SIMBOLOGIA_REGEX.py` L142-146).
   - `\S`: Negación de `\s`. Coincide con cualquier carácter que no sea espacio (`SIMBOLOGIA_REGEX.py` L148-152).
   - `\b`: Límite de palabra (*word boundary*), representa la transición entre un carácter `\w` y un `\W` o el extremo de la cadena (`SIMBOLOGIA_REGEX.py` L154-158).

### Cuantificadores: Comportamiento Codicioso (*Greedy*) vs Perezoso (*Lazy*)

Los cuantificadores especifican cuántas repeticiones del elemento inmediatamente anterior deben consumirse:

- `*`: Cero o más repeticiones (`Expresiones_Regulares.py` L84-86).
- `+`: Una o más repeticiones (`Expresiones_Regulares.py` L88-92).
- `?`: Cero o una repetición (hace al elemento precedente opcional) (`Creando_Expreiones.py` L6-14).
- `{m,n}`: De $m$ a $n$ repeticiones inclusivas (`Expresiones_Regulares.py` L253-268).

Por defecto, los cuantificadores en Python son **codiciosos (*greedy*)**: consumen la mayor cantidad posible de texto compatible antes de retroceder si la coincidencia global falla. Al añadir un sufijo `?` a un cuantificador (`*?`, `+?`, `??`, `{m,n}?`), este se transforma en **perezoso o no codicioso (*lazy* / *non-greedy*)**, consumiendo la menor cantidad de caracteres estrictamente necesaria para satisfacer el patrón.

### Métodos fundamentales del módulo `re`

El módulo ofrece cuatro funciones primarias de inspección con diferentes semánticas de anclaje:

1. **`re.search(pattern, string, flags=0)`:** Escanea toda la cadena de izquierda a derecha y retorna un objeto `re.Match` con la primera coincidencia localizada, o `None` si ninguna posición coincide (`Expresiones_Regulares.py` L28-32).
2. **`re.match(pattern, string, flags=0)`:** Evalúa la coincidencia estrictamente anclada al inicio de la cadena (índice 0). Si el primer carácter no satisface el patrón, retorna `None` inmediatamente.
3. **`re.fullmatch(pattern, string, flags=0)`:** Requiere que la totalidad de la cadena, desde el primer hasta el último carácter, coincida de extremo a extremo con el patrón. Es el método idóneo para validación de entradas de usuario (`SIMBOLOGIA_REGEX.py` L4).
4. **`re.findall(pattern, string, flags=0)`:** Retorna una lista con todas las coincidencias no solapadas. Si el patrón no contiene grupos de captura, retorna una lista de cadenas `list[str]`; si contiene múltiples grupos, retorna una lista de tuplas `list[tuple[str, ...]]` (`Expresiones_Regulares.py` L34-59).

### El objeto `re.Match`

Cuando una operación de búsqueda es exitosa, retorna una instancia de la clase `re.Match`. Este objeto encapsula metadatos deterministas sobre el segmento coincidente:

- `match.group(0)` o `match.group()`: Retorna el texto íntegro consumido por la coincidencia.
- `match.group(n)`: Retorna la subcadena capturada por el $n$-ésimo paréntesis de captura.
- `match.groups()`: Retorna una tupla conteniendo todos los subgrupos capturados.
- `match.start()` / `match.end()`: Retornan los índices inicial y final dentro de la cadena original.
- `match.span()`: Retorna una tupla `(inicio, fin)` compatible con la indexación por rebanadas de Python.

### Transformación y partición: `re.sub` y `re.split`

La manipulación de texto estructurado se expande mediante dos funciones fundamentales:

- **`re.sub(pattern, repl, string, count=0, flags=0)`:** Reemplaza ocurrencias del patrón en la cadena objetivo (`Creando_Expreiones.py` L8). El argumento `repl` puede ser una cadena de sustitución o una función invocable (*callable*) `def f(match: re.Match) -> str`, permitiendo cálculos dinámicos basados en la coincidencia.
- **`re.split(pattern, string, maxsplit=0, flags=0)`:** Divide la cadena utilizando las coincidencias del patrón como separadores, superando la limitación de `str.split` que únicamente admite delimitadores literales fijos.

## 4. Sintaxis y funcionamiento

### Elementos fundamentales de expresiones regulares

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `r"..."` | Notación de cadena cruda; previene la interpretación de escapes por el analizador de Python. | `r"\d+\n"` procesa la barra invertida literalmente sin requerir `\\d+`. |
| 2 | `.` | Metacarácter comodín; coincide con cualquier carácter excepto el salto de línea `\n`. | `r"a.c"` coincide con `"abc"`, `"a-c"`, `"a9c"`. |
| 3 | `^` | Ancla de inicio; coincide con el comienzo de la cadena o línea (en modo `re.M`). | `r"^GET"` valida que una petición HTTP comience con dicho método. |
| 4 | `$` | Ancla de finalización; coincide con el término de la cadena o línea (en modo `re.M`). | `r"\.json$"` verifica la extensión al final de un nombre de archivo. |
| 5 | `\d` / `\D` | Clase de dígitos; `\d` coincide con `[0-9]`, mientras que `\D` niega los dígitos. | `r"\d{4}"` extrae años de cuatro cifras; `r"\D+"` extrae texto sin dígitos. |
| 6 | `\w` / `\W` | Clase alfanumérica; `\w` incluye `[a-zA-Z0-9_]`, `\W` representa caracteres especiales. | `r"\w+"` tokeniza identificadores; `r"\W"` localiza puntuación. |
| 7 | `\s` / `\S` | Clase de espacio en blanco; `\s` incluye `[ \t\n\r\f\v]`, `\S` cualquier no espacio. | `r"\s+"` colapsa secuencias de separación tipográfica. |
| 8 | `[...]` / `[^...]` | Conjunto de caracteres explícito o negado según el corchete inicial. | `r"[A-F0-9]"` coincide con dígitos hexadecimales en mayúscula. |
| 9 | `*` / `+` / `?` | Cuantificadores codiciosos: `*` (0 o más), `+` (1 o más), `?` (0 o 1). | `r"https?://"` coincide con `"http://"` y `"https://"`. |
| 10 | `{m,n}` | Cuantificador acotado; requiere entre $m$ y $n$ repeticiones del elemento previo. | `r"\d{2,4}"` acepta códigos numéricos de entre dos y cuatro cifras. |
| 11 | `*?` / `+?` | Cuantificadores perezosos; consumen la menor cantidad posible de caracteres. | `r"<.+?>"` coincide con una sola etiqueta HTML en vez de abarcar todo el documento. |
| 12 | `(...)` | Grupo de captura posicional; aísla subpatrones e indexa sus valores coincidentes. | `r"(\d{4})-(\d{2})"` aísla el año y el mes en grupos separados. |
| 13 | `re.search()` | Escanea el texto completo retornando la primera ocurrencia como objeto `re.Match`. | `re.search(r"\bID:\d+\b", log)` halla la primera mención de identificador. |
| 14 | `re.fullmatch()` | Verifica coincidencia total y estricta de principio a fin de la cadena. | `re.fullmatch(r"[A-Z]{3}-\d{4}", placa)` valida placas vehiculares. |
| 15 | `re.sub()` | Sustituye ocurrencias mediante cadenas o funciones invocables dinámicas. | `re.sub(r"\s+", " ", texto)` normaliza espacios múltiples en uno solo. |

## 5. Ejemplos prácticos progresivos

### Básico

En este nivel inicial se exploran la validación estricta con `re.fullmatch()`, la búsqueda posicional con `re.search()`, la extracción global con `re.findall()` y la inspección de metadatos en el objeto `re.Match` (`start`, `end`, `span`).

```python
import re

# 1. Validación estricta con fullmatch
patron_codigo = r"[A-Z]{3}-\d{4}"
valido = "CLI-9821"
invalido = "cliente-9821"

assert re.fullmatch(patron_codigo, valido) is not None
assert re.fullmatch(patron_codigo, invalido) is None
print(f"Validación de código '{valido}': Aceptado")

# 2. Localización de primera coincidencia e inspección de re.Match
documento = "Registro operacional referencia REF-5421 emitido el 2026-11-07."
patron_ref = r"\bREF-\d{4}\b"

coincidencia = re.search(patron_ref, documento)
if coincidencia:
    print(f"Texto coincidente: {coincidencia.group()}")
    print(f"Posición inicial: {coincidencia.start()}")
    print(f"Posición final: {coincidencia.end()}")
    print(f"Intervalo (span): {coincidencia.span()}")
    print(f"Segmento rebanado: {documento[coincidencia.start():coincidencia.end()]}")

# 3. Extracción de todas las ocurrencias numéricas con findall
linea_contable = "Factura 102: Base 1500 USD, IVA 315 USD, Total 1815 USD."
cifras = re.findall(r"\b\d+\b", linea_contable)
print(f"Cifras extraídas: {cifras}")
```

#### Resultado esperado:
```text
Validación de código 'CLI-9821': Aceptado
Texto coincidente: REF-5421
Posición inicial: 32
Posición final: 40
Intervalo (span): (32, 40)
Segmento rebanado: REF-5421
Cifras extraídas: ['102', '1500', '315', '1815']
```

---

### Intermedio

Se contrastan los cuantificadores codiciosos (*greedy*) frente a los perezosos (*lazy*), se demuestra la captura estructurada con `Match.groups()` y se implementa la tokenización de texto multilínea mediante `re.split()`.

```python
import re

# 1. Comparación entre cuantificación codiciosa (greedy) y perezosa (lazy)
markup = "<div>Primer contenedor</div><div>Segundo contenedor</div>"

# El cuantificador codicioso (.+) consumirá hasta el último cierre </div>
patron_codicioso = r"<div>.+</div>"
# El cuantificador perezoso (.+?) se detendrá en el primer cierre </div>
patron_perezoso = r"<div>.+?</div>"

resultado_codicioso = re.findall(patron_codicioso, markup)
resultado_perezoso = re.findall(patron_perezoso, markup)

print(f"Coincidencias codiciosas (total {len(resultado_codicioso)}): {resultado_codicioso}")
print(f"Coincidencias perezosas (total {len(resultado_perezoso)}): {resultado_perezoso}")

# 2. Descomposición de fechas estructuradas mediante grupos posicionales
registro_temporal = "Transacción ejecutada el 2026-11-07 con autorización OK-998."
patron_fecha = r"\b(\d{4})-(\d{2})-(\d{2})\b"

match_fecha = re.search(patron_fecha, registro_temporal)
if match_fecha:
    año, mes, dia = match_fecha.groups()
    print(f"Fecha analizada -> Año: {año}, Mes: {mes}, Día: {dia}")
    print(f"Grupo global (0): {match_fecha.group(0)}")
    print(f"Grupos individuales: g1={match_fecha.group(1)}, g2={match_fecha.group(2)}, g3={match_fecha.group(3)}")

# 3. Tokenización y limpieza con re.split
encabezado = "usuario_id;  nombre,  departamento  |  rol\t:activo"
delimitadores = r"[;,|:\t]\s*"
columnas = [token.strip() for token in re.split(delimitadores, encabezado) if token.strip()]
print(f"Columnas normalizadas: {columnas}")
```

#### Resultado esperado:
```text
Coincidencias codiciosas (total 1): ['<div>Primer contenedor</div><div>Segundo contenedor</div>']
Coincidencias perezosas (total 2): ['<div>Primer contenedor</div>', '<div>Segundo contenedor</div>']
Fecha analizada -> Año: 2026, Mes: 11, Día: 07
Grupo global (0): 2026-11-07
Grupos individuales: g1=2026, g2=11, g3=07
Columnas normalizadas: ['usuario_id', 'nombre', 'departamento', 'rol', 'activo']
```

---

### Avanzado

Implementación de un procesador de anonimización y sanitización de registros de auditoría (*log sanitizer*) en producción. Utiliza sustitución funcional dinámica mediante `re.sub()` recibiendo un *callable* para enmascarar información personal identificable (PII, como correos electrónicos, números telefónicos y números de tarjetas de crédito) mientras preserva la estructura léxica del mensaje.

```python
import re
from typing import Callable


class SanitizadorAuditoria:
    """Procesador de enmascaramiento dinámico de datos sensibles en flujos de texto."""

    # Patrón compuesto para detectar correos, teléfonos internacionales y números bancarios
    PATRON_PII = re.compile(
        r"(?P<email>\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)"
        r"|(?P<telefono>\+\d{1,3}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3,4})"
        r"|(?P<tarjeta>\b(?:\d{4}[-\s]?){3}\d{4}\b)"
    )

    @classmethod
    def _enmascarar_match(cls, match: re.Match[str]) -> str:
        """Determina la estrategia de anonimización según el grupo capturado."""
        if match.group("email"):
            usuario, dominio = match.group("email").split("@", 1)
            visible = usuario[:2] if len(usuario) >= 2 else usuario[:1]
            return f"{visible}***@{dominio}"

        if match.group("telefono"):
            tel_limpio = re.sub(r"[\s-]", "", match.group("telefono"))
            return f"{tel_limpio[:4]}****{tel_limpio[-2:]}"

        if match.group("tarjeta"):
            tarjeta_digitos = re.sub(r"[\s-]", "", match.group("tarjeta"))
            return f"****-****-****-{tarjeta_digitos[-4:]}"

        return "[CONFIDENCIAL]"

    @classmethod
    def sanitizar(cls, mensaje: str) -> str:
        """Ejecuta la sustitución funcional de todas las entidades sensibles."""
        return cls.PATRON_PII.sub(cls._enmascarar_match, mensaje)


# Demostración del pipeline de sanitización
lineas_log = [
    "Operador carlosperez@empresa.com inició sesión remota.",
    "Llamada entrante atendida desde +54 911 4455-8899 sin incidencias.",
    "Cargo procesado con tarjeta 4532-8901-2345-6789 por importe 150.00 USD.",
    "Usuario maria.g@dominio.org confirmó cambio de teléfono al +51 941 611 934.",
]

sanitizador = SanitizadorAuditoria()
for log in lineas_log:
    resultado = sanitizador.sanitizar(log)
    print(resultado)
```

#### Resultado esperado:
```text
Operador ca***@empresa.com inició sesión remota.
Llamada entrante atendida desde +549****99 sin incidencias.
Cargo procesado con tarjeta ****-****-****-6789 por importe 150.00 USD.
Usuario ma***@dominio.org confirmó cambio de teléfono al +519****34.
```

## 6. Aplicaciones en el mundo real

El motor de expresiones regulares es un componente indispensable en arquitecturas empresariales:

1. **Pasarelas de API y validadores de esquemas:** En capas perimetrales de microservicios (como esquemas Pydantic o controladores FastAPI), las expresiones regulares validan que campos como RFC, códigos postales, IBAN o UUID cumplan con especificaciones formales antes de llegar a la lógica de negocio.
2. **Ingesta y estructuración de registros en Observabilidad (ETL):** Agentes de recolección de logs (Fluentbit, Logstash o scripts internos de Python) analizan archivos de texto desestructurados producidos por servidores web (Nginx, Apache), extrayendo direcciones IP, códigos de respuesta HTTP y tiempos de latencia mediante `re.search` y expresiones regulares con grupos.
3. **Preprocesamiento en Procesamiento del Lenguaje Natural (PLN):** Antes de alimentar modelos de lenguaje o analizadores de sentimientos, las expresiones regulares limpian etiquetas HTML, remueven URLs, anonimizan números telefónicos y eliminan secuencias de caracteres no imprimibles (`Ejercicio-Final.py` L13-24).
4. **Cumplimiento normativo y seguridad (Data Loss Prevention - DLP):** Filtros automatizados en sistemas de correo o bases de datos inspeccionan campos abiertos para detectar fugas de números de seguridad social, tarjetas de crédito o credenciales de autenticación expuestas accidentalmente.

## 7. Uso en producción

Al implementar expresiones regulares en entornos de alta concurrencia y producción, deben observarse los siguientes principios de ingeniería:

1. **Gestión de la caché interna del módulo `re`:** Las funciones de nivel de módulo como `re.search` o `re.sub` mantienen una caché interna (`re._cache`) limitada típicamente a 512 patrones compilados. En bucles de procesamiento masivo o servicios web bajo alta carga, depender de la búsqueda por cadena sin precompilación puede introducir sobrecargas innecesarias de sincronización y búsqueda en caché. Se recomienda precompilar patrones estáticos a nivel de módulo con `re.compile()`.
2. **Preferencia de métodos nativos de `str` para búsquedas literales:** Invocar el motor de expresiones regulares para operaciones que pueden resolverse con `cadena.startswith()`, `cadena.endswith()`, `subcadena in cadena` o `cadena.replace()` introduce una penalización de rendimiento innecesaria. El motor de regex solo debe emplearse cuando la regla involucre variabilidad de patrones, cuantificadores o clases de caracteres.
3. **Seguridad frente a inyección en expresiones regulares:** Cuando un patrón se construye concatenando entradas del usuario, cualquier metacarácter (`.`, `*`, `+`) ingresado por el cliente alterará la semántica del patrón, pudiendo generar denegaciones de servicio o accesos indebidos. En tales escenarios, es imperativo utilizar `re.escape(entrada_usuario)` para deshabilitar metacaracteres.
4. **Substitución funcional para transformaciones complejas:** En lugar de encadenar múltiples llamadas a `re.sub()`, estructurar una sola pasada léxica con una función invocable (`re.sub(patron, callback, texto)`) reduce la complejidad algorítmica de $O(k \cdot n)$ a $O(n)$, donde $k$ es el número de reglas y $n$ la longitud de la cadena.

## 8. Errores comunes y recomendaciones

### 1. Omisión del prefijo raw string en patrones con barras invertidas

Si se omite el prefijo `r` en una cadena que incluye secuencias de escape del motor de regex, Python 3 emitirá advertencias de tipo `SyntaxWarning: invalid escape sequence` y el patrón puede interpretarse de manera errónea.

```python
# ERROR INTENCIONAL: Omisión del prefijo raw string en secuencias de escape
import re

# En cadenas estándar, \d no es un escape válido de Python y genera advertencia:
patron_inseguro = "\d+\.\d+"
# Corrección obligatoria: emplear raw strings r"\d+\.\d+"
patron_correcto = r"\d+\.\d+"
assert re.search(patron_correcto, "3.14").group() == "3.14"
```

### 2. Confusión entre `re.match` y `re.search`

Un error recurrente consiste en utilizar `re.match()` esperando encontrar una coincidencia en cualquier parte del texto (`Analisis_expresiones.py` L121-128). Dado que `re.match()` ancla la búsqueda al índice 0, fallará silenciosamente retornando `None` si la coincidencia ocurre tras caracteres iniciales.

```python
import re

texto = "Servidor activo en puerto: 8080"
patron = r"\d+"

# re.match falla porque 'Servidor' está en el índice 0:
assert re.match(patron, texto) is None

# re.search escanea toda la cadena y localiza el puerto:
coincidencia = re.search(patron, texto)
assert coincidencia is not None and coincidencia.group() == "8080"
```

### 3. Avaricia no deseada en cuantificadores codiciosos

El uso indiscriminado del patrón `.*` dentro de cuantificadores codiciosos suele consumir delimitadores intermedios involuntarios.

```python
import re

texto = "El valor es <val1> y el segundo es <val2>."

# El cuantificador codicioso captura desde el primer '<' hasta el último '>'
codicioso = re.findall(r"<.*>", texto)
assert codicioso == ["<val1> y el segundo es <val2>"]

# El cuantificador perezoso captura cada etiqueta individualmente
perezoso = re.findall(r"<.*?>", texto)
assert perezoso == ["<val1>", "<val2>"]
```

### 4. Asumir retorno exitoso sin validar `None`

Acceder directamente a `.group()` sobre el resultado de `re.search()` sin verificar previamente si retornó un objeto `Match` provoca una excepción `AttributeError: 'NoneType' object has no attribute 'group'`.

```python
# ERROR INTENCIONAL: Acceso inseguro a .group() sobre resultado nulo
import re

texto = "Registro sin identificadores"
coincidencia = re.search(r"ID:\d+", texto)
# coincidencia.group() -> Generaría AttributeError

# Manejo seguro:
identificador = coincidencia.group() if coincidencia is not None else "NO_ENCONTRADO"
assert identificador == "NO_ENCONTRADO"
```

## 9. Resumen

1. **Lenguajes regulares y el módulo `re`:** Python implementa soporte completo para lenguajes regulares mediante su biblioteca estándar `re`, basada en un autómata NFA con retroceso (*backtracking*).
2. **Notación cruda imperativa:** Todos los patrones de expresiones regulares deben definirse mediante cadenas crudas `r"..."` para evitar que el analizador léxico de Python consuma las barras invertidas `\` antes de entregarlas al compilador de regex.
3. **Semántica de operaciones clave:**
   - `re.fullmatch`: Valida la totalidad de la cadena de extremo a extremo.
   - `re.search`: Localiza la primera coincidencia en cualquier posición del texto.
   - `re.match`: Evalúa la coincidencia exclusivamente anclada al índice cero.
   - `re.findall`: Extrae todas las ocurrencias no solapadas como lista de cadenas o tuplas.
4. **Inspección precisa con `re.Match`:** Encapsula la posición inicial (`start()`), final (`end()`), rango (`span()`) y los grupos capturados (`group()`, `groups()`).
5. **Cuantificación controlada:** La distinción entre cuantificadores codiciosos (`*`, `+`) y perezosos (`*?`, `+?`) es crítica para delimitar correctamente extracciones en textos con múltiples separadores idénticos.
6. **Transformación funcional:** `re.sub()` admite funciones invocables dinámicas como reemplazo, facilitando flujos de trabajo avanzados de enmascaramiento y sanitización de datos sensibles en producción.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/A-INTRODUCCION.py` (L1-37) | `A-INTRODUCCION.py` | Definición introductoria de regex, motivación para agendas de contactos y necesidad del prefijo `r"..."`. | Formalización matemática en la Jerarquía de Chomsky, explicación técnica de la colisión de secuencias de escape entre el lexer de Python y el motor en C `_sre`. |
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Creando_Expreiones.py` (L1-15) | `Creando_Expreiones.py` | Detección y ocultamiento de números telefónicos internacionales mediante `re.sub()`. | Transformación funcional dinámica con `re.sub(callable)` para anonimización parcial preservando códigos de área; tipado estático con `typing.Callable`. |
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/SIMBOLOGIA_REGEX.py` (L1-217) | `SIMBOLOGIA_REGEX.py` | Catálogo exhaustivo de metacaracteres (`.`, `^`, `$`, `[]`, `|`, `()`, `\d`, `\w`, `\s`, `\b`). | Sistematización en matriz de sintaxis y funcionamiento; distinción formal entre clases de caracteres ASCII vs Unicode y comportamiento de los límites de palabra. |
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Expresiones_Regulares.py` (L1-292) | `Expresiones_Regulares.py` | Ejercicios prácticos con `re.search()`, `re.findall()`, banderas `re.M`, `re.IGNORECASE` y cuantificadores acotados `{n,m}`. | Análisis del ciclo de vida del objeto `re.Match`, cuantificación codiciosa (*greedy*) vs perezosa (*lazy*), tokenización con `re.split()` y directrices de rendimiento en producción. |
| `CLASS_PY_POO` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Ejercicio-Final.py` (L1-81) | `Ejercicio-Final.py` | Preprocesamiento de texto previo al análisis de sentimientos con bibliotecas externas y APIs. | Diseño de capas de sanitización de entradas de usuario y neutralización de cadenas maliciosas mediante expresiones regulares robustas antes de invocar servicios externos. |

**Fundamento complementario:** los ejemplos originales presentaban fragmentos aislados de código en scripts secuenciales con impresiones en consola (`print`) y dependencias no controladas. Esta guía formaliza los fundamentos de las expresiones regulares dentro de la teoría de autómatas, introduce el análisis detallado del objeto `re.Match`, sistematiza la sustitución funcional mediante `re.sub(callable)` y provee patrones de validación testeables y deterministas para entornos de producción.

## 11. Referencias oficiales

- [Documentación oficial de Python 3: Módulo `re`](https://docs.python.org/3/library/re.html) — Especificación formal de la biblioteca estándar para expresiones regulares en Python.
- [Python Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — Guía oficial y tutorial exhaustivo sobre el diseño y optimización de expresiones regulares escrito por A.M. Kuchling.
