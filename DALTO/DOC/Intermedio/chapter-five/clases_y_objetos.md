# Clases, Objetos, Ciclo de Instanciación e Identidad en Memoria

## 2. Introducción

A medida que un sistema crece en volumen de datos y reglas de negocio, representarlo exclusivamente mediante [variables](../../Basico/chapter-one/variables.md) sueltas (`Clases_y_Objetos.py` L12-26) o colecciones paralelas ([listas](../../Basico/chapter-two/listas.md) y [diccionarios](../chapter-one/diccionarios.md) independientes) introduce fragilidad estructural: nada impide olvidar una clave, desincronizar índices entre estructuras o dispersar las validaciones por múltiples módulos.

La **Programación Orientada a Objetos (POO)** resuelve este acoplamiento agrupando **estado** (datos) y **comportamiento** (operaciones válidas sobre esos datos) dentro de unidades cohesivas denominadas **objetos**, construidas a partir de moldes formales llamados **clases** (`Clase_One.py` L1-30, `Clase_One_2.py` L1-35). Dominar sus cimientos en Python resulta indispensable por cuatro motivos técnicos:

1. **Cohesión y modelado de dominio:** cada entidad (`Estudiante`, `Celular`, `Stack`) concentra sus invariantes y transiciones en un único lugar auditable.
2. **Comprensión real del ciclo de creación:** distinguir entre el asignador `__new__` y el inicializador `__init__` evita errores de diseño y explica cómo Python materializa instancias en tiempo de ejecución.
3. **Modelo uniforme de objetos e identidad:** en Python todo valor es un objeto; diferenciar con rigor entre identidad (`is`, `id()`), igualdad de valor (`==`) y detalles específicos de **CPython** previene fallos sutiles con referencias compartidas.
4. **Arquitectura desacoplada y verificable:** separar las clases del dominio respecto de la captura interactiva por consola (`BUENAS_PRACTICAS.py` L95-193) permite reutilizar el mismo modelo en APIs web, procesos por lotes y pruebas automatizadas.

## 3. Fundamentos y conceptos

**Limitaciones del enfoque procedimental disperso frente a la cohesión en POO.** En `Clases_y_Objetos.py` (L12-26) se declaran doce variables independientes (`celular1_marca`, `celular2_marca`, ..., `celular3_camaraF`) para describir apenas tres dispositivos. Incluso reemplazando esas variables por diccionarios sueltos, el intérprete no garantiza que todos posean los mismos campos ni impide asociarles funciones incompatibles. Una **clase** establece un contrato explícito de estructura y comportamiento: define una sola vez qué [atributos y métodos](atributos_y_metodos.md) posee el concepto y permite fabricar tantas instancias independientes como requiera el programa (`Keyword_del.py` L7-34, `Clase_One.py` L134-175).

**Clase frente a objeto (instancia) y la metaclase `type`.** Conviene precisar la relación ontológica entre ambos términos en el modelo de datos de Python:

- **Clase (`class`):** es la definición estructural o plantilla que describe la familia de objetos y actúa como un nuevo [tipo de dato](../../Basico/chapter-one/tipos_datos.md) definido por el programador. En Python, las clases son a su vez objetos de primera clase en memoria: al evaluar un bloque `class Celular:`, el intérprete ejecuta su cuerpo en un espacio de nombres aislado y construye un objeto clase cuya clase (su **metaclase** predeterminada) es `type` (`isinstance(Celular, type) == True`).
- **Objeto o instancia:** es cada ejemplar concreto creado al invocar la clase (`cel = Celular()`). Cada instancia mantiene su propio estado particular y verifica `isinstance(cel, Celular) == True`.

**Convenciones estilísticas de PEP 8.** La guía oficial de estilo **PEP 8** establece identificadores en formato `CapWords` (también conocido como `PascalCase`, p. ej. `CellPhone`, `CuentaBancaria`, `AnalizadorLexico`) para los nombres de clases, reservando `snake_case` para instancias, [funciones](../chapter-two/funciones.md), métodos y atributos (`mi_personaje`, `subir_nivel`). En consecuencia, definiciones como `class personaje:` (`Clase_One.py` L134) deben corregirse a `class Personaje:`, y paréntesis vacíos como `class Celular():` (`Clases_y_Objetos.py` L59) se simplifican idiomáticamente a `class Celular:` cuando no se especifican superclases explícitas.

**Ciclo de vida de instanciación: `__new__` frente a `__init__`.** En `Clase_One.py` (L20-23) y `Clases_y_Objetos.py` (L103-105) se denomina coloquialmente "constructor" a `__init__`. En la especificación formal de Python, sin embargo, la creación de `obj = MiClase(*args, **kwargs)` consta de **dos etapas diferenciadas** orquestadas por `type.__call__`:

```text
MiClase(arg1, arg2)
   │
   ├──► 1. obj = MiClase.__new__(MiClase, arg1, arg2)
   │         └─► Reserva y retorna la nueva instancia vacía (constructor real)
   │
   └──► 2. Si isinstance(obj, MiClase):
             MiClase.__init__(obj, arg1, arg2)
               └─► Pobla el estado inicial sobre `self` y retorna obligatoriamente None
```

1. **`__new__(cls, ...)` (asignador / constructor real):** método estático especial heredado de `object` que aloja la instancia en memoria y la devuelve. Rara vez necesita redefinirse, salvo al subclasificar tipos inmutables (`int`, `str`, [tuplas](../chapter-one/tuplas.md)) o implementar patrones de control de instancias.
2. **`__init__(self, ...)` (inicializador):** recibe como primer argumento la instancia recién creada por `__new__` y configura sus atributos iniciales (`self.marca = marca`). Por contrato estricto del lenguaje, **`__init__` debe retornar `None`** (de forma implícita o mediante `return` vacío); devolver cualquier otro objeto provoca inmediatamente `TypeError: __init__() should return None`.

**El parámetro explícito `self`.** A diferencia de lenguajes que inyectan una palabra reservada implícita (`this`), Python opta por la transparencia explícita: todo método de instancia declara como primer parámetro la referencia al propio objeto sobre el cual se invoca, denominado universalmente `self` por convención de **PEP 8** (`Clase_One.py` L136-138, `Clases_y_Objetos.py` L108-111). Aunque `self` no es una palabra reservada gramatical, emplear otro nombre degrada severamente la legibilidad y es rechazado por analizadores estáticos. Cuando se escribe `mi_personaje.subir_nivel(10, 11, 20)`, Python traduce internamente la llamada a `Personaje.subir_nivel(mi_personaje, 10, 11, 20)`.

**Objetos en memoria, identidad abstracta (`is`, `id()`) y particularidades de CPython.** Al crear múltiples instancias (`celular1 = Celular()`, `celular2 = Celular()` en `Clases_y_Objetos.py` L69-76), cada llamada aloja un objeto distinto con su propio diccionario de estado (`__dict__`, explorado en `Crear_Clase.py` L89). Para inspeccionar referencias deben distinguirse tres conceptos:

- **Identidad abstracta en Python (`id()` e `is`):** la especificación del lenguaje define que todo objeto posee una **identidad** entera obtenible mediante `id(obj)`, garantizada como única y constante mientras el objeto permanezca vivo (una vez recolectado por el recolector de basura, otro objeto futuro podría reutilizar ese número). El [operador](../../Basico/chapter-one/operadores.md) `a is b` evalúa si ambas variables apuntan exactamente al **mismo objeto** (`id(a) == id(b)`), mientras que `a == b` consulta el método `__eq__` para comparar equivalencia de contenido (por defecto en clases de usuario sin `__eq__`, `object.__eq__` delega en identidad, aspecto profundizado en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md)).
- **Detalle de implementación en CPython frente a otros intérpretes:** en `Clases_y_Objetos.py` (L78-84) se observa la salida por defecto `<__main__.Celular object at 0x000001A11FF07230>`. Conviene precisar que hacer coincidir `id(obj)` con la **dirección virtual de memoria RAM** (mostrada en hexadecimal tras `at 0x...` por `object.__repr__`) es una **decisión interna de CPython**, no una regla universal del lenguaje Python: implementaciones alternativas como PyPy (con recolector de basura móvil que reubica objetos en RAM) o Jython asignan identificadores lógicos estables desvinculados de la dirección física.

**Desacoplamiento arquitectónico entre clases de dominio y entrada/salida (`BUENAS_PRACTICAS.py`).** En los primeros acercamientos (`One.py` L20-110, `Clases_y_Objetos.py` L143 y la primera versión de `Person` en `BUENAS_PRACTICAS.py` L3-84), el método `__init__` contiene llamadas a `input()` y `print()`. Este acoplamiento presenta tres defectos graves de ingeniería:

1. Impide instanciar la clase desde orígenes no interactivos (bases de datos, archivos CSV/JSON, peticiones HTTP o suites de pruebas automatizadas).
2. Viola la separación entre la capa de presentación (interfaz de línea de comandos) y la capa de dominio.
3. Oculta defectos latentes en ramas interactivas difíciles de ejercitar automáticamente: por ejemplo, en `BUENAS_PRACTICAS.py` (L43) existe el error tipográfico `input(...).strip().tile()` (en lugar de `.title()`), que lanza `AttributeError` en tiempo de ejecución al llegar al cuarto campo.

La segunda versión de `BUENAS_PRACTICAS.py` (L95-193) y `Crear_Clase.py` (L1-9, L85-87) aplican el diseño correcto: la clase `Person` o `Roca` recibe únicamente datos ya capturados como parámetros de `__init__` (apoyándose opcionalmente en [desempaquetamiento](../chapter-one/desempaquetamiento.md) `Person(* datos)`), manteniendo el dominio puro y determinista.

## 4. Sintaxis y funcionamiento

Anatomía declarativa de una clase de dominio e instanciación explícita:

```text
class NombreEnPascalCase:
    """Docstring descriptivo de la responsabilidad e invariantes de la clase."""

    def __init__(self, param_obligatorio: str, param_opcional: int = 0) -> None:
        self.param_obligatorio = param_obligatorio
        self.param_opcional = param_opcional

    def metodo_comportamiento(self, factor: int) -> str:
        return f"{self.param_obligatorio}: {self.param_opcional * factor}"


instancia = NombreEnPascalCase("sensor-norte", param_opcional=5)
resultado = instancia.metodo_comportamiento(3)
```

Referencia de elementos nucleares en la definición y manipulación de clases e instancias:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `class NombreClase:` | Crea un nuevo objeto clase (instancia de `type`) en `PascalCase` | `class DispositivoMovil:` |
| 2 | `Clase(...)` | Ejecuta `__new__` (aloja instancia) seguido de `__init__` (inicializa estado) | `cel = DispositivoMovil("S25")` |
| 3 | `def __init__(self, ...):` | Inicializador de atributos de la instancia recién alojada; retorna `None` | `def __init__(self, marca: str) -> None:` |
| 4 | `self` | Primer parámetro explícito que referencia a la instancia receptora | `self.marca = marca` |
| 5 | `obj.atributo` | Acceso, creación o reasignación de atributos mediante notación de punto | `cel.marca` |
| 6 | `obj.metodo(...)` | Invocación de comportamiento enlazando automáticamente `obj` a `self` | `cel.llamar()` |
| 7 | `type(obj)` / `isinstance(obj, C)` | Obtiene la clase concreta del objeto o verifica pertenencia de tipo | `isinstance(cel, DispositivoMovil)` |
| 8 | `a is b` / `id(obj)` | Comprueba identidad exacta de referencia frente al identificador único | `cel_a is cel_b` |
| 9 | `obj.__dict__` | Diccionario interno que almacena los atributos propios de la instancia | `list(cel.__dict__.keys())` |
| 10 | `del obj.atributo` / `del var` | Elimina un atributo del diccionario del objeto o desenlaza un nombre | `del cel.temporal` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Transición de variables dispersas a una clase cohesiva con parámetros posicionales, por palabra clave y valores por defecto.**

```python
class DispositivoMovil:
    """Representa un teléfono móvil con estado y operaciones básicas."""

    def __init__(self, marca: str, modelo: str, camara: str = "50MP") -> None:
        self.marca = marca
        self.modelo = modelo
        self.camara = camara
        self.encendido = False

    def alternar_energia(self) -> str:
        self.encendido = not self.encendido
        estado = "encendido" if self.encendido else "apagado"
        return f"{self.marca} {self.modelo} ahora está {estado}"

    def ficha_tecnica(self) -> str:
        return f"{self.marca} {self.modelo} | Cámara: {self.camara}"


equipo_1 = DispositivoMovil("Samsung", "S25", "200MP")
equipo_2 = DispositivoMovil(marca="Xiaomi", modelo="14T")

print(equipo_1.ficha_tecnica())
print(equipo_2.ficha_tecnica())
print(equipo_1.alternar_energia())
print("Estado equipo_1:", equipo_1.encendido, "| Estado equipo_2:", equipo_2.encendido)
```

Explicación paso a paso:

- Se refactoriza `Clases_y_Objetos.py` (L12-26, L135-159) eliminando el `print()` lateral dentro de `__init__` y definiendo una clase en `PascalCase` con valores predeterminados (`camara: str = "50MP"`).
- `equipo_1` y `equipo_2` mantienen estados independientes: activar `equipo_1.alternar_energia()` modifica únicamente `equipo_1.encendido`, dejando intacto `equipo_2.encendido`.

Resultado esperado:

```text
Samsung S25 | Cámara: 200MP
Xiaomi 14T | Cámara: 50MP
Samsung S25 ahora está encendido
Estado equipo_1: True | Estado equipo_2: False
```

### Intermedio

**Ejemplo 2 — Interacción entre objetos independientes, referencias en memoria (`is` frente a alias) e inspección de `__dict__`.**

```python
class PersonajeJuego:
    """Entidad de combate desacoplada de la salida estándar."""

    def __init__(self, nombre: str, fuerza: int, defensa: int, vida: int) -> None:
        self.nombre = nombre
        self.fuerza = fuerza
        self.defensa = defensa
        self.vida = vida

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def calcular_danio(self, oponente: "PersonajeJuego") -> int:
        return max(0, self.fuerza - oponente.defensa)

    def atacar(self, oponente: "PersonajeJuego") -> str:
        danio = self.calcular_danio(oponente)
        oponente.vida = max(0, oponente.vida - danio)
        return (
            f"{self.nombre} inflige {danio} de daño a {oponente.nombre} "
            f"(vida restante: {oponente.vida})"
        )


heroe = PersonajeJuego("BitBoss", fuerza=18, defensa=10, vida=50)
clon_distinto = PersonajeJuego("BitBoss", fuerza=18, defensa=10, vida=50)
alias_heroe = heroe
enemigo = PersonajeJuego("Centinela", fuerza=12, defensa=6, vida=20)

print("¿Clase es instancia de type?:", isinstance(PersonajeJuego, type))
print("¿heroe es clon_distinto?    :", heroe is clon_distinto, "| id distintos:", id(heroe) != id(clon_distinto))
print("¿heroe es alias_heroe?      :", heroe is alias_heroe, "| id iguales  :", id(heroe) == id(alias_heroe))
print(heroe.atacar(enemigo))
print(heroe.atacar(enemigo))
print("¿Enemigo sigue vivo?:", enemigo.esta_vivo())
print("Atributos de enemigo:", enemigo.__dict__)
```

Explicación técnica:

- Se moderniza `Clase_One.py` (L134-205) corrigiendo dos detalles lógicos: el daño nunca resulta negativo (`max(0, ...)` evita curar accidentalmente al oponente si su defensa supera la fuerza atacante) y los métodos retornan cadenas descriptivas en lugar de acoplarse a `print()`.
- Aunque `heroe` y `clon_distinto` reciben idénticos argumentos de inicialización, alojan objetos distintos (`heroe is clon_distinto` es `False`); en cambio, `alias_heroe = heroe` copia la referencia al mismo objeto.

Resultado esperado:

```text
¿Clase es instancia de type?: True
¿heroe es clon_distinto?    : False | id distintos: True
¿heroe es alias_heroe?      : True | id iguales  : True
BitBoss inflige 12 de daño a Centinela (vida restante: 8)
BitBoss inflige 12 de daño a Centinela (vida restante: 0)
¿Enemigo sigue vivo?: False
Atributos de enemigo: {'nombre': 'Centinela', 'fuerza': 12, 'defensa': 6, 'vida': 0}
```

### Avanzado

**Ejemplo 3 — Verificación experimental del ciclo `__new__` -> `__init__` y arquitectura desacoplada con validación de dominio.**

```python
traza_ciclo: list[str] = []


class SesionAuditada:
    """Demuestra el orden exacto de ejecución entre __new__ e __init__."""

    def __new__(cls, usuario: str) -> "SesionAuditada":
        traza_ciclo.append(f"1.__new__ recibe cls={cls.__name__}")
        instancia = super().__new__(cls)
        traza_ciclo.append(f"2.__new__ aloja instancia vacía={ list(instancia.__dict__.keys()) }")
        return instancia

    def __init__(self, usuario: str) -> None:
        traza_ciclo.append("3.__init__ configura self")
        self.usuario = usuario


class EstudianteRegistrado:
    """Modelo de dominio puro (sin input/print) con validación de invariantes."""

    SUFIJOS_CICLO = {
        1: "ro", 2: "do", 3: "ro", 4: "to", 5: "to",
        6: "to", 7: "mo", 8: "vo", 9: "no", 10: "mo",
    }

    def __init__(self, nombre: str, edad: int, ciclo: int) -> None:
        nombre_limpio = nombre.strip().title()
        if len(nombre_limpio) < 3 or not nombre_limpio.replace(" ", "").isalpha():
            raise ValueError(f"Nombre inválido: {nombre!r}")
        if edad < 2:
            raise ValueError(f"Edad fuera de rango: {edad}")
        if ciclo not in self.SUFIJOS_CICLO:
            raise ValueError(f"El ciclo {ciclo} debe estar entre 1 y 10")

        self.nombre = nombre_limpio
        self.edad = edad
        self.grado = f"{ciclo}{self.SUFIJOS_CICLO[ciclo]}"

    def describir_actividad(self, estudiando: bool = True) -> str:
        accion = "está estudiando" if estudiando else "está en receso"
        return f"Estudiante {self.nombre} ({self.grado} ciclo, {self.edad} años) {accion}"


sesion = SesionAuditada("operador_01")
for paso in traza_ciclo:
    print(paso)
print("Atributos tras __init__:", sesion.__dict__)

# Instanciación determinista desde registros estructurados (sin input())
filas_crudas = [("  ana lucia ", 19, 3), ("carlos", 21, 8)]
estudiantes = [EstudianteRegistrado(*fila) for fila in filas_crudas]
for est in estudiantes:
    print(est.describir_actividad())
```

Explicación de arquitectura:

- `SesionAuditada` evidencia que `__new__` recibe la clase `cls`, solicita memoria a `object.__new__` devolviendo un objeto cuyo `__dict__` aún está vacío `[]`, y solo entonces Python invoca `__init__` pasando ese mismo objeto como `self`.
- `EstudianteRegistrado` transforma la lógica interactiva de `One.py` (L18-115) y `BUENAS_PRACTICAS.py` (L95-193) en una entidad verificable: normaliza cadenas con `.strip().title()` (corrigiendo el `.tile()` de `BUENAS_PRACTICAS.py` L43), valida invariantes lanzando [excepciones](../chapter-four/excepciones.md) semánticas y permite instanciar lotes completos mediante desempaquetamiento `*fila`.

Resultado esperado:

```text
1.__new__ recibe cls=SesionAuditada
2.__new__ aloja instancia vacía=[]
3.__init__ configura self
Atributos tras __init__: {'usuario': 'operador_01'}
Estudiante Ana Lucia (3ro ciclo, 19 años) está estudiando
Estudiante Carlos (8vo ciclo, 21 años) está estudiando
```

## 6. Aplicaciones en el mundo real

- **Entidades de dominio en comercio electrónico y banca:** clases como `Pedido`, `LineaFactura` o `Poliza` agrupan estado monetario y reglas de transición (borrador -> pagado -> despachado), impidiendo modificaciones incoherentes desde capas externas.
- **Modelos ORM (*Object-Relational Mapping*):** bibliotecas como SQLAlchemy o el ORM de Django representan tablas relacionales mediante clases y filas individuales mediante instancias en memoria.
- **Estructuras de datos y contenedores especializados:** encapsulación de colas con prioridad, cachés LRU, grafos o pilas LIFO (como la clase `Stack` en `Keyword_del.py` L7-20) con operaciones atómicas controladas.
- **Clientes de infraestructura con estado de conexión:** sesiones HTTP reutilizables (`requests.Session`), cursores de base de datos o clientes de mensajería que conservan credenciales, *pools* de sockets y contadores de reintentos.

## 7. Uso en producción

- **Constructores puros, rápidos y libres de efectos secundarios de E/S:** en sistemas productivos, `__init__` solo debe validar argumentos y asignar referencias en memoria. Nunca debe solicitar entradas por terminal (`input()`), escribir en consola (`print()`), ni abrir conexiones bloqueantes de red o disco difíciles de simular en pruebas unitarias.
- **Fallo temprano (*fail-fast*) para garantizar invariantes de creación:** si los argumentos suministrados son inválidos, `__init__` debe lanzar `ValueError` o `TypeError` antes de completar la construcción; un objeto jamás debe quedar vivo en memoria en un estado parcialmente inicializado o inválido.
- **Anotaciones de tipos estáticas en firmas y atributos:** declarar tipos explícitos en `__init__` y métodos públicos permite que herramientas como `mypy` o `pyright` detecten errores de invocación o atributos mal escritos (como `.tile()` en lugar de `.title()`) antes de desplegar el software.
- **Implementación explícita de representaciones legibles:** definir `__repr__` en las clases de negocio sustituye la salida cruda `<__main__.Clase object at 0x...>` por diagnósticos útiles en registros de auditoría y trazas de depuración (desarrollado en [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md)).

## 8. Errores comunes y recomendaciones

1. **Retornar un valor distinto de `None` desde `__init__`.**

```python
class ConfiguracionInvalida:
    def __init__(self, puerto: int):
        self.puerto = puerto
        return self  # Inválido: __init__ solo inicializa, no retorna la instancia


try:
    ConfiguracionInvalida(8080)
except TypeError as err:
    print(f"{type(err).__name__}: {err}")
```

Resultado esperado:

```text
TypeError: __init__() should return None, not 'ConfiguracionInvalida'
```

Diagnóstico: la responsabilidad de crear y devolver la instancia corresponde exclusivamente a `__new__`; `__init__` opera por mutación sobre `self` y debe finalizar sin valor de retorno (o con `return None`).

2. **Omitir `self` al declarar métodos o al referenciar atributos dentro de la clase.**

```python
# ERROR INTENCIONAL: omisión de self en la firma del método de instancia
class ContadorDefectuoso:
    def __init__(self) -> None:
        self.total = 0

    def incrementar() -> None:
        pass


c = ContadorDefectuoso()
c.incrementar()  # TypeError: ContadorDefectuoso.incrementar() takes 0 positional arguments but 1 was given
```

Diagnóstico: al invocar `c.incrementar()`, Python inyecta automáticamente `c` como primer argumento posicional. Análogamente, escribir `total = 0` sin el prefijo `self.` dentro de un método solo crea una variable local efímera ([ámbito de variables](../chapter-two/ambito_variables.md)) que desaparece al retornar el método, sin actualizar el atributo del objeto.

3. **Confundir igualdad de estado (`==`) con identidad de objeto (`is`) en clases personalizadas.**

```python
class Coordenada:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


p1 = Coordenada(10, 20)
p2 = Coordenada(10, 20)

print("p1 is p2:", p1 is p2)
print("p1 == p2 (sin __eq__ definido):", p1 == p2)
```

Resultado esperado:

```text
p1 is p2: False
p1 == p2 (sin __eq__ definido): False
```

Diagnóstico: mientras una clase de usuario no redefina `__eq__`, hereda `object.__eq__`, el cual compara por identidad (`p1 is p2`), retornando `False` para dos instancias distintas aunque sus atributos sean idénticos. Recomendación: usar `is` únicamente para comprobar identidad exacta de referencia o *singletons* como `None` (`x is None`), e implementar `__eq__` (o usar `@dataclass`) cuando dos entidades deban compararse por valor.

4. **Acoplar lectura interactiva (`input()`) y escritura (`print()`) dentro de `__init__`.** Como demuestra la primera mitad de `BUENAS_PRACTICAS.py` (L3-84, incluido el defecto `.strip().tile()` en L43) frente a su refactorización posterior (L95-193), incrustar bucles de consola en el inicializador impide instanciar la clase programáticamente y oculta errores de ejecución tras flujos manuales.

## 9. Resumen

- Una **clase** es un objeto molde (instancia de la metaclase `type`, nombrada en `PascalCase` según **PEP 8**) que agrupa atributos y métodos; un **objeto** o **instancia** es cada ejemplar independiente creado a partir de ella.
- La instanciación ejecuta dos pasos ordenados: `__new__(cls, ...)` aloja y retorna la instancia vacía, y `__init__(self, ...)` inicializa su estado sobre `self` retornando obligatoriamente `None`.
- El parámetro `self` explicita la instancia receptora en los métodos: `obj.metodo(arg)` equivale a `Clase.metodo(obj, arg)`.
- En Python, `id(obj)` e `is` evalúan **identidad abstracta** de objeto; el hecho de que `id(obj)` y `<... at 0x...>` reflejen la dirección virtual en RAM es un detalle específico de **CPython**.
- Las clases de dominio deben mantenerse libres de llamadas a `input()` y `print()`, recibiendo datos ya capturados y señalizando violaciones de invariantes mediante excepciones.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clase_One.py` (L1-205) | `Clase_One.py` | Introducción conceptual a los cuatro pilares, declaración de `class personaje:`, uso de `self`, `__init__` e interacción entre `mi_personaje` y `mi_enemigo` | Se adoptó `PascalCase` (**PEP 8**), se corrigió el cálculo de daño negativo y se desacoplaron los métodos respecto de `print()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clase_One_2.py` (L1-40) | `Clase_One_2.py` | Definición conceptual de POO, contraste entre clases (plantillas) y objetos (instancias), escalabilidad y reutilización | Se formalizó el rol de las clases como objetos de primera clase construidos por la metaclase `type` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/CLASE_PRIMERA/Clases_y_Objetos.py` (L1-159) | `Clases_y_Objetos.py` | Variables sueltas repetitivas (L12-26), `class Celular():`, salida `<__main__.Celular object at 0x...>` (L80) y `class CellPhone:` con valores por defecto en `__init__` | Se diferenció la identidad abstracta de Python (`id()`, `is`) respecto de la dirección de memoria RAM propia de **CPython**, y se eliminó el `print()` dentro de `__init__` (L143) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_ONE/EJERCICIOS/One.py` (L1-157) | `One.py` | `class Estudiante:` con captura en `__init__`, métodos `estudiar()`/`descansar()` y funciones externas tipadas con `user : Estudiante` (L121, L143) | Se transformó la captura interactiva en un modelo de dominio determinista con validación de invariantes mediante `ValueError` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/BUENAS_PRACTICAS.py` (L1-200) | `BUENAS_PRACTICAS.py` | Contraste explícito entre pedir datos con `input()` dentro de `Person.__init__` (L3-84) y extraer `Pedir_Datos()` pasando `*Pedir_Datos()` (L95-193) | Se documentó el error en tiempo de ejecución `.strip().tile()` (`AttributeError` en L43) como evidencia práctica del riesgo de acoplar E/S dentro de `__init__` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Crear_Clase.py` (L1-98) | `Crear_Clase.py` | Clase `Roca` desacoplada de `Pedir_Datos()` e inspección del espacio de nombres de instancia mediante `roca_One.__dict__.items()` (L89-93) | Se explicó el papel estructural de `__dict__` en el almacenamiento dinámico de atributos por instancia |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L7-34) | `Keyword_del.py` | Definición temprana de `class Stack:` con estado interno y métodos `push`/`pop` | Se integró como ejemplo transversal de cohesión entre estructura de datos y operaciones válidas |

**Fundamento complementario:** se incorporaron tres piezas esenciales de la especificación del lenguaje ausentes en los apuntes iniciales: (1) la arquitectura de instanciación en dos fases (`__new__` como asignador frente a `__init__` como inicializador obligado a retornar `None`); (2) la naturaleza de las clases como instancias de la metaclase `type`; y (3) la distinción rigurosa entre la semántica abstracta de `id()`/`is` en el lenguaje Python y la representación por dirección de memoria en **CPython**, junto con el comportamiento predeterminado de `object.__eq__`.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/classes.html> — Tutorial oficial de Python (*Classes*): objetos clase, objetos instancia, objetos método e instanciación.
- <https://docs.python.org/3/reference/datamodel.html#objects-values-and-types> — Referencia del modelo de datos (*Objects, values and types*): identidad (`id()`, `is`), tipo (`type()`) y valor de todo objeto en Python.
- <https://docs.python.org/3/reference/datamodel.html#basic-customization> — Referencia del modelo de datos (*Basic customization*): contrato formal de `object.__new__`, `object.__init__` y `object.__repr__`.
- <https://peps.python.org/pep-0008/#class-names> — PEP 8 (*Style Guide for Python Code — Class Names & Function and Method Arguments*): convención `CapWords` (`PascalCase`) y uso de `self`.
