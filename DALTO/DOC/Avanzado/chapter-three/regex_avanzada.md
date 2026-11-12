# Expresiones Regulares Avanzadas y Seguridad en Python

## 2. Introducción

En el diseño de sistemas de software de alta concurrencia, el uso superficial de expresiones regulares mediante funciones inmediatas y patrones simples resulta insuficiente y potencialmente peligroso. Conforme los requerimientos de procesamiento textual aumentan en complejidad, los desarrolladores deben dominar herramientas avanzadas: precompilación de patrones para optimizar el rendimiento de la CPU, consumo perezoso de memoria mediante generadores [iteradores](../../Avanzado/chapter-one/iteradores.md), agrupamiento semántico con nombres y retro-referencias, y aserciones de ancho cero (*lookaround assertions*) (`REGEX-Search.py` L1-22).

Asimismo, el motor de expresiones regulares de Python (`re`), al igual que la mayoría de los motores de lenguajes de alto nivel como Perl, Java o JavaScript, se basa en un autómata finito no determinista con retroceso recursivo (*backtracking NFA*). Esta característica arquitectónica implica que patrones diseñados de manera deficiente —en particular aquellos con cuantificadores anidados o solapados— exhiben una complejidad temporal exponencial $O(2^n)$. Cuando un atacante envía una carga maliciosa diseñada para forzar este comportamiento, el sistema sufre una denegación de servicio por expresión regular (**ReDoS**, *Regular Expression Denial of Service*) (`Z-Conejo_De_Indias.py` L3).

Esta guía profundiza en las capacidades avanzadas del módulo `re`, formaliza las aserciones de inspección sin consumo de caracteres y establece las directrices defensivas indispensables para neutralizar vulnerabilidades de retroceso catastrófico en entornos de producción, complementando los [fundamentos de expresiones regulares](expresiones_regulares.md).

## 3. Fundamentos y conceptos

### Precompilación de expresiones con `re.compile()`

Cuando se invoca una función como `re.search(patron, texto)`, Python debe realizar internamente tres pasos:
1. Analizar léxicamente la cadena del patrón.
2. Compilar el árbol sintáctico en *bytecodes* interpretables por el motor en C `_sre`.
3. Ejecutar el autómata contra el texto objetivo.

Aunque Python mantiene una caché interna pequeña (`re._cache`), en bucles intensivos o servicios web concurrentes depender de la compilación bajo demanda genera contención en bloqueos de sincronización y sobrecarga de procesamiento innecesaria. La función `re.compile(pattern, flags=0)` compila el patrón una sola vez y retorna una instancia inmutable y segura para múltiples hilos (*thread-safe*) de la clase `re.Pattern`:

```python
import re

# Compilación única a nivel de módulo o clase
PATRON_UUID = re.compile(r"^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$", re.IGNORECASE)

# Reutilización determinista sin recompilación
assert PATRON_UUID.match("c9a646d3-9c61-4cd7-9f51-7f631e81b660") is not None
```

### Procesamiento perezoso de memoria con `re.finditer()`

A diferencia de `re.findall()`, que evalúa exhaustivamente toda la cadena y materializa en memoria una lista completa con todas las coincidencias (`CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Z-Conejo_De_Indias.py` L30-34), `re.finditer()` retorna un iterador que produce objetos `re.Match` bajo demanda (*lazy evaluation*) (`Z-Conejo_De_Indias.py` L37-43).

En el procesamiento de archivos de registro masivos (de cientos de megabytes o gigabytes), `re.finditer()` permite procesar coincidencias una a una manteniendo un consumo constante de memoria $O(1)$ respecto al volumen de coincidencias halladas:

```python
import re

documento = "Evento 1: OK, Evento 2: ERROR, Evento 3: OK"
patron = re.compile(r"Evento\s+(\d+):\s+([A-Z]+)")

# finditer produce un generador de objetos Match sin instanciar listas masivas
for coincidencia in patron.finditer(documento):
    id_evento, estado = coincidencia.groups()
    assert id_evento in {"1", "2", "3"}
```

### Grupos de captura posicional vs grupos sin captura

Los paréntesis en una expresión regular cumplen dos funciones potencialmente disyuntivas:
1. **Agrupación lógica:** Delimitar el ámbito de un operador (como `|` o cuantificadores `+`, `*`).
2. **Captura:** Asignar memoria para indexar y extraer el fragmento coincidente (`REGEX-Search.py` L14-16).

Cuando solo se requiere agrupación lógica sin necesidad de recuperar el valor capturado, reservar memoria de captura introduce una penalización de procesamiento. La sintaxis `(?:...)` define un **grupo sin captura (*non-capturing group*)** (`REGEX-Search.py` L231, `SIMBOLOGIA_REGEX.py` L190-194). Esto optimiza el consumo de memoria del motor y previene que `re.findall()` retorne tuplas innecesarias en lugar de coincidencias directas.

### Grupos con nombre y retro-referencias (*Backreferences*)

Para evitar acoplar el código a índices numéricos posicionales frágiles (`group(1)`, `group(2)`), Python permite asignar nombres semánticos a los grupos mediante la sintaxis `(?P<nombre>...)` (`SIMBOLOGIA_REGEX.py` L196-200). Los valores capturados pueden extraerse como diccionario con `match.groupdict()` o accederse nominalmente con `match.group("nombre")`.

Asimismo, las **retro-referencias** permiten verificar simetría y congruencia dentro del mismo texto:
- **Dentro del patrón sintáctico:** `(?P=nombre)` exige que el texto en la posición actual coincida de forma idéntica con lo ya capturado por el grupo nombrado (por ejemplo, asegurar comillas simétricas de apertura y cierre: `(?P<quote>["'])(.*?)(?P=quote)`).
- **En cadenas de sustitución con `re.sub`:** `\g<nombre>` o `\g<id>` inserta el grupo capturado en el texto resultante (`Analisis_expresiones.py` L42-57).

### Banderas de compilación (*Compilation Flags*)

Las banderas modifican el comportamiento interno del analizador léxico y del motor autómata:

1. **`re.IGNORECASE` (`re.I`):** Realiza comparaciones insensibles a mayúsculas y minúsculas respetando las tablas Unicode o ASCII (`SIMBOLOGIA_REGEX.py` L202-206).
2. **`re.MULTILINE` (`re.M`):** Altera las anclas `^` y `$` para que coincidan al inicio y al final de cada línea física (tras cada `\n`), en lugar de coincidir únicamente al inicio y fin del texto global (`SIMBOLOGIA_REGEX.py` L208-212).
3. **`re.DOTALL` (`re.S`):** Fuerza a que el comodín punto `.` coincida con absolutamente cualquier carácter, incluyendo saltos de línea `\n` (`SIMBOLOGIA_REGEX.py` L214-217).
4. **`re.VERBOSE` (`re.X`):** Permite escribir expresiones regulares legibles y mantenibles en múltiples líneas, ignorando espacios en blanco no escapados y permitiendo comentarios con `#` dentro del propio patrón.
5. **Composición con operadores bit a bit:** Múltiples banderas se combinan mediante el operador OR binario: `flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE`.

### Aserciones de ancho cero (*Lookaround Assertions*)

Las aserciones de búsqueda anticipada (*lookahead*) y retrospectiva (*lookbehind*) son condiciones de ancho cero (*zero-width*): evalúan si un subpatrón coincide o no coincide en una posición determinada **sin consumir caracteres** ni avanzar el cursor de coincidencia del motor (`SIMBOLOGIA_REGEX.py` L26-27, L178-188):

1. **Búsqueda anticipada positiva (*Positive Lookahead*) `(?=...)`:** La coincidencia es válida únicamente si el subpatrón coincide inmediatamente a la derecha, pero dichos caracteres permanecen disponibles para los siguientes componentes del patrón.
2. **Búsqueda anticipada negativa (*Negative Lookahead*) `(?!...)`:** La coincidencia es válida únicamente si el subpatrón **no** coincide a la derecha.
3. **Búsqueda retrospectiva positiva (*Positive Lookbehind*) `(?<=...)`:** La coincidencia es válida únicamente si el subpatrón coincide inmediatamente a la izquierda. En Python, el motor `re` exige que el subpatrón dentro de un lookbehind tenga una **longitud fija** en tiempo de compilación (no admite cuantificadores variables como `+` o `*`).
4. **Búsqueda retrospectiva negativa (*Negative Lookbehind*) `(?<!...)`:** La coincidencia es válida únicamente si el subpatrón **no** precede a la izquierda.

### Retroceso catastrófico y vulnerabilidad ReDoS (*Catastrophic Backtracking*)

El retroceso (*backtracking*) es el mecanismo por el cual un motor NFA retrocede en su árbol de decisiones cuando una rama de coincidencia falla, explorando permutaciones alternativas.

El problema surge ante la presencia de **ambigüedad combinatoria**: cuando coexisten cuantificadores anidados sobre expresiones que pueden coincidir con los mismos caracteres. Un caso clásico es el patrón:

$$\text{Patrón vulnerable: } \wedge(a+)+ \$$$

Si este patrón se evalúa sobre una cadena de $n$ letras `'a'` seguida de un carácter que rompe la coincidencia final (como `"aaaaaaaaaa!"`), el motor intentará particionar la secuencia de `'a'` entre el cuantificador interno y el externo de todas las formas posibles antes de declarar el fallo:

$$\text{Número de permutaciones} = 2^{n-1}$$

Para $n = 30$, el motor ejecutará más de 500 millones de pasos de retroceso, consumiendo el 100% de un núcleo de CPU y bloqueando el hilo de ejecución por minutos u horas. En un servidor web, unas pocas peticiones con este patrón provocan una **Denegación de Servicio por Expresión Regular (ReDoS)**.

## 4. Sintaxis y funcionamiento

### Elementos avanzados y aserciones del motor `re`

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `re.compile(patron, flags)` | Precompila una expresión regular en un objeto `re.Pattern` reutilizable y eficiente. | `PATRON = re.compile(r"^\d{5}$")` optimiza validaciones repetitivas. |
| 2 | `re.finditer(patron, texto)` | Generador que produce objetos `re.Match` bajo demanda sin materializar listas en memoria. | `for m in patron.finditer(log): ...` procesa flujos masivos en $O(1)$ de memoria. |
| 3 | `(?:...)` | Grupo sin captura; agrupa subexpresiones sin reservar índices posicionales ni memoria. | `r"(?:https?\|ftp)://\S+"` agrupa protocolos sin capturarlos individualmente. |
| 4 | `(?P<nombre>...)` | Grupo de captura con nombre semántico accesible mediante clave o `groupdict()`. | `r"(?P<año>\d{4})-(?P<mes>\d{2})"` aísla campos temporales legibles. |
| 5 | `(?P=nombre)` | Retro-referencia en patrón; exige coincidencia exacta con lo capturado por el grupo nombrado. | `r"(?P<q>['\"]).*?(?P=q)"` garantiza apertura y cierre con la misma comilla. |
| 6 | `\g<nombre>` | Retro-referencia en sustitución; inserta el contenido del grupo en `re.sub()`. | `re.sub(r"(?P<v>\d+)", r"[\g<v>]", s)` envuelve números entre corchetes. |
| 7 | `(?=...)` | Búsqueda anticipada positiva (*Positive Lookahead*); valida lo que sigue sin consumirlo. | `r"\d+(?=px)"` extrae la cifra únicamente si está seguida de la unidad `"px"`. |
| 8 | `(?!...)` | Búsqueda anticipada negativa (*Negative Lookahead*); prohíbe que el subpatrón continúe a la derecha. | `r"\bfoo(?!bar)\b"` encuentra `"foo"` salvo si forma `"foobar"`. |
| 9 | `(?<=...)` | Búsqueda retrospectiva positiva (*Positive Lookbehind*); exige prefijo de longitud fija previo. | `r"(?<=\$)\d+(\.\d{2})?"` extrae importes precedidos por el signo monetario `$`. |
| 10 | `(?<!...)` | Búsqueda retrospectiva negativa (*Negative Lookbehind*); prohíbe prefijo de longitud fija previo. | `r"(?<!\\)@"` coincide con arrobas que no hayan sido escapadas con `\`. |
| 11 | `re.VERBOSE` / `re.X` | Bandera que permite estructurar patrones multilínea con espacios y comentarios explicativos. | Permite documentar cada subsección de expresiones regulares complejas. |
| 12 | `(a+)+$` *(Antipatrón)* | Cuantificación anidada ambigua; causa explosión combinatoria exponencial $O(2^n)$ (ReDoS). | Debe refactorizarse mediante clases mutuamente excluyentes como `^a+$`. |

## 5. Ejemplos prácticos progresivos

### Básico

Se implementa la precompilación de patrones con `re.compile()`, captura semántica mediante grupos nombrados `(?P<name>...)`, consumo perezoso de memoria con `re.finditer()` y exportación directa a estructuras de datos con `match.groupdict()`.

```python
import re

# 1. Precompilación del patrón con grupos nombrados semánticos
PATRON_METRICA = re.compile(
    r"^TIMESTAMP:(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+"
    r"HOST:(?P<host>[a-zA-Z0-9.-]+)\s+"
    r"METRICA:(?P<metrica>[a-z_]+)\s+"
    r"VALOR:(?P<valor>\d+(?:\.\d+)?)$"
)

# 2. Flujo de datos multilínea simulado
flujo_telemetria = (
    "TIMESTAMP:2026-11-07T14:30:00 HOST:srv-prod-01 METRICA:cpu_usage VALOR:78.5\n"
    "TIMESTAMP:2026-11-07T14:30:01 HOST:srv-prod-02 METRICA:mem_free VALOR:1024\n"
    "TIMESTAMP:2026-11-07T14:30:02 HOST:srv-prod-01 METRICA:disk_io VALOR:0.92"
)

# 3. Procesamiento bajo demanda con finditer sin instanciar listas globales
registros_parseados: list[dict[str, str]] = []
for linea in flujo_telemetria.splitlines():
    coincidencia = PATRON_METRICA.match(linea)
    if coincidencia:
        datos = coincidencia.groupdict()
        registros_parseados.append(datos)
        print(f"Métrica procesada: host={datos['host']}, métrica={datos['metrica']}, valor={datos['valor']}")

assert len(registros_parseados) == 3
print(f"Total de registros estructurados exitosamente: {len(registros_parseados)}")
```

#### Resultado esperado:
```text
Métrica procesada: host=srv-prod-01, métrica=cpu_usage, valor=78.5
Métrica procesada: host=srv-prod-02, métrica=mem_free, valor=1024
Métrica procesada: host=srv-prod-01, métrica=disk_io, valor=0.92
Total de registros estructurados exitosamente: 3
```

---

### Intermedio

Se aplican aserciones de ancho cero (*lookaround assertions*) para validar políticas de seguridad de contraseñas de alta complejidad y extraer importes monetarios delimitados por contexto sin consumir los símbolos delimitadores. Se utiliza `re.VERBOSE` para documentar la arquitectura del patrón.

```python
import re

# 1. Validador de contraseñas de alta seguridad utilizando múltiples Lookaheads positivos
# Requisitos: al menos 1 mayúscula, 1 minúscula, 1 número, 1 carácter especial, longitud >= 10
PATRON_PASSWORD = re.compile(
    r"""
    ^                       # Ancla de inicio
    (?=.*[A-Z])             # Lookahead positivo: contiene al menos una letra mayúscula
    (?=.*[a-z])             # Lookahead positivo: contiene al menos una letra minúscula
    (?=.*\d)                # Lookahead positivo: contiene al menos un dígito numérico
    (?=.*[!@#$%^&*()_+\-=\[\]{}]) # Lookahead positivo: contiene al menos un símbolo especial
    (?!.*(.)\1{2,})         # Lookahead negativo: prohíbe caracteres idénticos repetidos 3+ veces consecutivas
    .{10,}                  # Longitud mínima de 10 caracteres
    $                       # Ancla de fin
    """,
    re.VERBOSE,
)

pruebas_credenciales = [
    ("PasswordSeguro2026!", True),
    ("debil", False),              # Longitud insuficiente y sin mayúsculas
    ("SinSimbolosNumericosNiNada", False), # Carece de dígitos y símbolos
    ("PasswordAAA123!", False),    # Rechazado por Lookahead negativo (secuencia repetida 'AAA')
    ("Arq_S0lid#2026", True),
]

for clave, esperado in pruebas_credenciales:
    valida = bool(PATRON_PASSWORD.match(clave))
    assert valida == esperado
    estado = "Válida" if valida else "Rechazada"
    print(f"Clave evaluada: {clave:<28} -> {estado}")

# 2. Extracción de valores monetarios con Lookbehind positivo y Lookahead negativo
# Extrae cantidades en dólares ($) que NO terminen en céntimos fraccionados '.00'
texto_financiero = "Costos: $150.00 de apertura, $45.50 de mantenimiento y $1200 de amortización."
patron_importes = re.compile(r"(?<=\$)\d+(?:\.\d{2})?(?<!\.00)")

importes = patron_importes.findall(texto_financiero)
print(f"Importes significativos extraídos (sin base '.00'): {importes}")
```

#### Resultado esperado:
```text
Clave evaluada: PasswordSeguro2026!          -> Válida
Clave evaluada: debil                        -> Rechazada
Clave evaluada: SinSimbolosNumericosNiNada   -> Rechazada
Clave evaluada: PasswordAAA123!              -> Rechazada
Clave evaluada: Arq_S0lid#2026               -> Válida
Importes significativos extraídos (sin base '.00'): ['45.50', '1200']
```

---

### Avanzado

Auditoría y mitigación de vulnerabilidades de **Retroceso Catastrófico (ReDoS)**. Se demuestra la diferencia de rendimiento entre un analizador sintáctico ambiguo con cuantificadores anidados y su correspondiente refactorización lineal determinista utilizando clases mutuamente excluyentes y límites estrictos de procesamiento.

```python
import re
import time


class AnalizadorSintacticoDefensivo:
    """Demostración de refactorización de patrones vulnerables a ReDoS a autómatas lineales."""

    # PATRÓN VULNERABLE: Cuantificadores anidados sobre caracteres solapados.
    # Ante cadenas no coincidentes de tipo "a" * n + "!", explora 2^(n-1) ramas.
    PATRON_VULNERABLE = re.compile(r"^([a-zA-Z0-9]+)+$")

    # PATRÓN DEFENSIVO: Cuantificador único atómico no ambiguo delimitado.
    # Ejecución lineal O(n) garantizada independientemente de si la cadena coincide o falla.
    PATRON_DEFENSIVO = re.compile(r"^[a-zA-Z0-9]+$")

    @classmethod
    def validar_seguro(cls, cadena: str, max_longitud: int = 1000) -> bool:
        """Aplica defensa en profundidad: validación previa de longitud + patrón lineal."""
        if len(cadena) > max_longitud:
            return False
        return bool(cls.PATRON_DEFENSIVO.match(cadena))


# 1. Validación de equivalencia funcional en casos afirmativos
texto_valido = "AlfanumericoSeguro2026"
assert AnalizadorSintacticoDefensivo.PATRON_VULNERABLE.match(texto_valido) is not None
assert AnalizadorSintacticoDefensivo.validar_seguro(texto_valido) is True
print("Equivalencia funcional en casos válidos: Verificada")

# 2. Simulación de carga hostil diseñada para provocar retroceso catastrófico
longitud_ataque = 22
carga_maliciosa = ("a" * longitud_ataque) + "!"

# Medición del patrón vulnerable con retroceso exponencial
inicio_vulnerable = time.perf_counter()
AnalizadorSintacticoDefensivo.PATRON_VULNERABLE.match(carga_maliciosa)
duracion_vulnerable_ms = (time.perf_counter() - inicio_vulnerable) * 1000

# Medición del patrón defensivo lineal
inicio_defensivo = time.perf_counter()
AnalizadorSintacticoDefensivo.validar_seguro(carga_maliciosa)
duracion_defensivo_ms = (time.perf_counter() - inicio_defensivo) * 1000

print(f"Carga hostil (longitud {len(carga_maliciosa)} caracteres)")
print(f"Patrón lineal defensivo : {duracion_defensivo_ms:.4f} ms")
print(f"Patrón con backtracking  : {duracion_vulnerable_ms:.4f} ms")

# El patrón lineal debe ejecutarse de forma prácticamente instantánea (< 1 ms)
assert duracion_defensivo_ms < 5.0
# Se verifica que el patrón defensivo neutraliza el ataque rechazando la cadena
assert AnalizadorSintacticoDefensivo.validar_seguro(carga_maliciosa) is False
print("Estado de mitigación ReDoS: Protección activa y determinista.")
```

#### Resultado esperado:
```text
Equivalencia funcional en casos válidos: Verificada
Carga hostil (longitud 23 caracteres)
Patrón lineal defensivo : 0.0030 ms
Patrón con backtracking  : 15.2410 ms
Estado de mitigación ReDoS: Protección activa y determinista.
```

> [!NOTE]
> La duración en milisegundos puede presentar variaciones menores según la carga del procesador donde se ejecute la prueba, manteniéndose siempre la diferencia de órdenes de magnitud entre la evaluación lineal inmediata y la explosión combinatoria del retroceso.

## 6. Aplicaciones en el mundo real

Las técnicas avanzadas de expresiones regulares sustentan componentes centrales de la infraestructura de software:

1. **Firewalls de aplicaciones web (WAF) y filtrado de inyecciones:** Reglas de inspección profunda de paquetes analizan encabezados HTTP y cadenas de consulta buscando patrones de inyección SQL (`UNION SELECT`, `' OR '1'='1`) o Cross-Site Scripting (XSS). Dichas reglas utilizan aserciones negativas de ancho cero para ignorar parámetros legítimos sin consumir el cuerpo de la petición.
2. **Autenticación y cumplimiento de políticas de credenciales:** En servicios de identidad (OAuth2, IAM, Cognito), la verificación de contraseñas complejas se ejecuta en una sola pasada de CPU mediante múltiples búsquedas anticipadas positivas (`(?=.*[A-Z])(?=.*\d)...`), evitando encadenar múltiples llamadas condicionales.
3. **Analizadores sintácticos léxicos (Tokenizers y Lexers):** Motores de procesamiento de código y compiladores (incluyendo herramientas como Pygments, analizadores de Markdown o linters estáticos) emplean patrones precompilados con grupos nombrados y `re.finditer()` para clasificar palabras reservadas, literales y comentarios sin duplicar memoria.
4. **Validación robusta de interfaces de usuario:** En aplicaciones interactivas y sistemas de terminal, la unificación de validaciones léxicas en expresiones regulares con aserciones previene entradas corruptas de forma limpia y extensible (`Juego.py` L184-203).

## 7. Uso en producción

Al desplegar expresiones regulares avanzadas en sistemas distribuidos y servicios web de producción, deben implementarse las siguientes medidas de ingeniería:

1. **Inmutabilidad y seguridad multihilo de `re.Pattern`:** Las instancias compiladas mediante `re.compile()` son completamente inmutables y reentrantes. En servidores web asíncronos o multi-hilo (FastAPI, Gunicorn con Uvicorn o Celery), los patrones deben compilarse una sola vez a nivel de módulo o como constantes de clase, nunca dentro de funciones de controlador o bucles de eventos.
2. **Defensa en profundidad contra ReDoS:**
   - **Validación de longitud previa (*Guard Clauses*):** Antes de aplicar cualquier expresión regular sobre entradas no confiables provenientes de clientes externos, verifique que `len(texto) <= LIMITE_MAXIMO` (por ejemplo, 255 o 1024 caracteres). Esto acota la profundidad máxima de cualquier posible retroceso.
   - **Eliminación de cuantificadores anidados:** Audite patrones asegurándose de que subpatrones cuantificados como `(A+)+` o `(A|B)+` no compartan caracteres comunes entre `A` y `B`.
   - **Herramientas de análisis estático:** Incorpore analizadores estáticos de vulnerabilidades ReDoS en el pipeline de CI/CD para detectar patrones con complejidad superlineal antes del despliegue.
3. **Documentación estructural con `re.VERBOSE`:** Toda expresión regular que exceda los 25 caracteres o incorpore aserciones lookaround debe definirse obligatoriamente con la bandera `re.VERBOSE`. Los comentarios integrados preservan la mantenibilidad del código cuando otros ingenieros deban extender las reglas de negocio.
4. **Uso de `re.finditer` para flujos masivos:** En pipelines ETL o procesamiento de archivos que superen los 10 MB, evite estrictamente `re.findall()`. Utilice generadores basados en `re.finditer()` para mantener constante la huella de memoria.

## 8. Errores comunes y recomendaciones

### 1. Cuantificadores anidados susceptibles a Catastrophic Backtracking (ReDoS)

El error más destructivo en la ingeniería de expresiones regulares consiste en anidar cuantificadores sobre subgrupos abiertos.

```python
# ERROR INTENCIONAL: Cuantificadores anidados susceptibles a Catastrophic Backtracking (ReDoS)
import re

# Antipatrón vulnerable a degradación exponencial extrema O(2^n):
patron_catastrofico = re.compile(r"^(a+)+$")

# Corrección obligatoria: colapsar a un único cuantificador sobre clase atómica
patron_seguro = re.compile(r"^a+$")
assert patron_seguro.match("aaaaaaaaaa") is not None
```

### 2. Uso de patrones de longitud variable dentro de Lookbehind

El motor de expresiones regulares de Python exige que las aserciones retrospectivas (*lookbehind*) tengan una longitud fija predeterminada en tiempo de compilación (`SIMBOLOGIA_REGEX.py` L26). Si se incluye un cuantificador variable (`+`, `*`, `{1,5}`), el compilador lanza un error inmediato.

```python
# ERROR INTENCIONAL: Lookbehind con cuantificador de longitud variable
import re

# patron_invalido = re.compile(r"(?<=\d+)px")
# Arroja: re.error: look-behind requires fixed-width pattern

# Corrección: emplear longitud fija o estructurar mediante grupos con lookahead
patron_fijo = re.compile(r"(?<=\d{3})px")
assert patron_fijo.search("100px") is not None
```

### 3. Fuga de memoria por materialización de listas con `re.findall()`

En flujos continuos o archivos de gran escala, invocar `re.findall()` materializa todas las cadenas coincidentes en una lista en memoria, lo que puede provocar excepciones `MemoryError` o matar el proceso por el recolector OOM (*Out Of Memory*) del sistema operativo.

```python
import re

registro_extenso = "ID:100;ID:101;ID:102;" * 1000

# Ineficiente en producción (materializa lista de 3000 elementos):
lista_completa = re.findall(r"ID:(\d+)", registro_extenso)
assert len(lista_completa) == 3000

# Eficiente y escalable: consumo como iterador perezoso
iterador = re.finditer(r"ID:(\d+)", registro_extenso)
primer_id = next(iterador).group(1)
assert primer_id == "100"
```

### 4. Fragmentación de validaciones con múltiples búsquedas secuenciales

En código heredado es común encontrar validaciones estructuradas mediante múltiples llamadas a `re.search()` aplicadas a la misma variable (`Juego.py` L193-194). Esto incrementa el costo de ejecución linealmente y dispersa las reglas de validación.

```python
import re

nombre_usuario = "Guerrero2026"

# Fragmentado y redundante:
contiene_digito = re.search(r"\d", nombre_usuario) is not None
contiene_letra = re.search(r"[a-zA-Z]", nombre_usuario) is not None
valido_fragmentado = contiene_digito and contiene_letra

# Óptimo: unificado en un único patrón precompilado con aserciones anticipadas
PATRON_UNIFICADO = re.compile(r"^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z0-9]+$")
valido_unificado = bool(PATRON_UNIFICADO.match(nombre_usuario))

assert valido_fragmentado == valido_unificado is True
```

## 9. Resumen

1. **Precompilación con `re.compile()`:** Almacena el árbol sintáctico compilado del autómata en un objeto `re.Pattern` inmutable y seguro para múltiples hilos, eliminando la sobrecarga de recompilación y sincronización en producción.
2. **Iteración perezosa con `re.finditer()`:** Sustituye ventajosamente a `re.findall()` en el análisis de flujos masivos de datos, generando objetos `re.Match` bajo demanda y garantizando una huella de memoria $O(1)$.
3. **Optimización con grupos sin captura `(?:...)`:** Permite aplicar cuantificadores y disyunciones lógicas sin incurrir en la sobrecarga de reservar índices de captura posicionales.
4. **Semántica y trazabilidad con grupos nombrados `(?P<name>...)`:** Proporciona contratos explícitos de extracción mediante diccionarios (`groupdict()`) y permite validar simetría léxica mediante retro-referencias `(?P=name)`.
5. **Inspección de ancho cero (*Lookaround Assertions*):** Permite verificar precondiciones y postcondiciones contextuales (`(?=...)`, `(?!...)`, `(?<=...)`, `(?<!...)`) sin consumir caracteres de la cadena principal.
6. **Seguridad contra ReDoS (*Catastrophic Backtracking*):** La erradicación de cuantificadores anidados sobre clases solapadas, la delimitación estricta de longitudes de entrada y el diseño de autómatas deterministas son requisitos indispensables para proteger la disponibilidad del sistema.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/REGEX-Search.py` (L1-235) | `REGEX-Search.py` | Métodos del objeto `Match`, cuantificadores acotados, validación de correos y nombres compuestos con grupos no captores `(?:...)`. | Precompilación con `re.compile()`, reutilización de `Pattern` en alta concurrencia, uso de banderas combinadas y aserciones lookaround. |
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Analisis_expresiones.py` (L1-142) | `Analisis_expresiones.py` | Sustitución múltiple con `re.sub()`, diferenciación entre `re.match()` y `re.search()`, validación de URLs y correos electrónicos. | Sustitución avanzada con retro-referencias con nombre `\g<name>`, uso de `re.VERBOSE` para expresiones autodocumentadas y aserciones lookbehind. |
| `CLASES_PYTHON` | `CLASES_PYTHON/CLASE_ZEXTRAS/CLASE_QUINTA/EXPRESIONES_REGULARES/Z-Conejo_De_Indias.py` (L1-43) | `Z-Conejo_De_Indias.py` | Modificador `(?s)` (`re.DOTALL`), patrón con cuantificadores anidados `(^.+(M|m)+.+$)` y consumo eficiente con `re.finditer()`. | Análisis formal de vulnerabilidades ReDoS por retroceso catastrófico originadas en cuantificadores anidados, y gestión de memoria mediante iteradores perezosos. |
| `CLASS_PY_POO` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L184-285) | `Juego.py` | Validaciones secuenciales de nombres de personajes mediante múltiples llamadas a `re.search(r"\d", name)` y `re.search(r"[A-Za-z]", name)`. | Refactorización hacia validadores atómicos unificados con aserciones anticipadas positivas (`(?=.*\d)(?=.*[a-zA-Z])`) y desacoplamiento de la consola interactiva. |

**Fundamento complementario:** los ejemplos originales exploraban casos particulares de validación mediante scripts interactivos dependientes de `input()` y construcciones empíricas de expresiones regulares. Esta guía complementa el material original analizando la arquitectura interna del motor autómata, sistematizando las aserciones de ancho cero (*lookaround*), abordando formalmente el problema de seguridad del retroceso catastrófico (ReDoS) con mediciones de latencia y proveyendo patrones de producción inmutables, testeables y eficientes.

## 11. Referencias oficiales

- [Documentación oficial de Python 3: Módulo `re`](https://docs.python.org/3/library/re.html) — Especificación completa de la API del módulo `re`, clases `Pattern` y `Match`, y sintaxis formal de expresiones regulares.
- [Python Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — Guía detallada sobre técnicas avanzadas de compilación, grupos de captura, aserciones lookaround y optimización del motor de búsqueda.
