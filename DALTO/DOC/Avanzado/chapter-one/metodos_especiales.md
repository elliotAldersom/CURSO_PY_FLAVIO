# Modelo de Datos de Python, Métodos Especiales (*Dunder*) y Sobrecarga de Operadores

## 2. Introducción

Una de las mayores fortalezas de diseño de Python reside en la uniformidad de su sintaxis: expresiones nativas como `len(coleccion)`, `str(objeto)`, `a + b`, `x == y`, `clave in registro` o `item[0]` funcionan de manera idéntica tanto sobre tipos integrados (`int`, `str`, `list`, `dict`) como sobre [clases](../../Intermedio/chapter-five/clases_y_objetos.md) de dominio creadas por el desarrollador. En lugar de obligar al consumidor a memorizar nombres ad hoc (`sumar_importes()`, `obtener_longitud()`, `es_igual_a()`), el lenguaje define un contrato unificado conocido como **Modelo de Datos de Python** (*Python Data Model*).

Este contrato se materializa a través de los **métodos especiales** —denominados coloquialmente métodos *dunder* (*double underscore*) por iniciar y finalizar con doble guion bajo, como `__init__`, `__repr__` o `__add__` (`Metodos_Especiales.py` L1-8)—. Comprender su mecánica interna resulta esencial por cuatro motivos técnicos:

1. **Despacho implícito sobre el tipo y ranuras de CPython (*type slots*):** explica cómo el intérprete invoca operaciones nativas a alta velocidad resolviendo los métodos en la clase (`type(x)`) y no en el diccionario de la instancia.
2. **Representación textual rigurosa y segura (`__str__` frente a `__repr__`):** separa la presentación legible para usuarios finales respecto del diagnóstico inequívoco para ingeniería, erradicando riesgos de ejecución arbitraria asociados a `eval()`.
3. **Sobrecarga algebraica correcta en Python 3:** aplica los métodos vigentes (`__truediv__`, `__floordiv__`, reflejados `__radd__`), la constante `NotImplemented` y la inmutabilidad de objetos de valor.
4. **Coherencia entre igualdad, ordenamiento y tablas hash:** coordina `__eq__`, `@functools.total_ordering` y el invariante de `__hash__` junto con los protocolos de contenedores e invocables (`__len__`, `__getitem__`, `__contains__`, `__call__`).

## 3. Fundamentos y conceptos

**El Modelo de Datos y la invocación implícita sobre el tipo (*CPython type slots*).** Los identificadores rodeados por doble guion bajo (`__nombre__`) pertenecen de forma exclusiva a la especificación del lenguaje —incluyendo también atributos especiales de [módulos](../../Intermedio/chapter-three/modulos.md) y [paquetes](../../Intermedio/chapter-three/paquetes.md) como `__name__` (`MÓDULOS.py` L116-119, `Saludar.py` L12, `saludo_name.py` L1-11) o `__path__` e `__init__.py` (`PAQUETE.py` L8, L23, L41-42)—; nunca deben inventarse nombres `__propio__` arbitrarios porque podrían colisionar con futuras versiones de Python. Asimismo, el programador rara vez invoca `obj.__str__()` o `obj.__len__()` directamente: invoca las [funciones integradas](../../Intermedio/chapter-two/funciones_integradas.md) `str(obj)` y `len(obj)` o los [operadores](../../Basico/chapter-one/operadores.md) `+`, `==`, `[]`.

Cuando el intérprete evalúa `len(x)` o `str(x)`, **no busca el método en `x.__dict__`**, sino directamente en el tipo del objeto (`type(x).__len__(x)`). En la implementación de referencia **CPython**, definir un método especial en una sentencia `class` rellena punteros a funciones en C denominados **ranuras de tipo** (*type slots*, como `tp_str`, `tp_repr`, `nb_add` o `sq_length` en la estructura `PyTypeObject`). Gracias a ello, el despacho evita búsquedas dinámicas repetidas por diccionario y alcanza un rendimiento cercano al de los tipos nativos escritos en C.

**Representación textual: `__str__` frente a `__repr__` y regla de respaldo.** En `Metodos_Especiales.py` (L18-38, L50-58), `One.py` (L42-46) y `Juego.py` (L72-73, L92-93) conviven dos métodos complementarios de conversión a texto:

| Método especial | Invocado por | Audiencia y propósito | Regla de respaldo (*fallback*) |
|---|---|---|---|
| `__repr__(self) -> str` | `repr(x)`, `f"{x!r}"`, colecciones (`print([x])`), consola interactiva y trazas | **Desarrolladores y registros técnicos:** representación inequívoca que identifique tipo y estado exacto (p. ej. `Personaje(nombre='Goku', fuerza=200)`) | Si falta, hereda `object.__repr__` (`<Clase object at 0x...>`) |
| `__str__(self) -> str` | `str(x)`, `print(x)`, `f"{x}"` | **Usuarios finales e interfaces:** resumen legible y conciso del valor de negocio | Si falta `__str__`, **Python delega automáticamente en `__repr__`** |

De esta asimetría se desprende una regla fundamental: si solo se implementa uno de los dos métodos, debe implementarse siempre **`__repr__`**, pues cubrirá tanto `repr(x)` como `str(x)`. Conviene además evitar representaciones ambiguas como la de `Juego.py` (L92-93), donde `__repr__` devuelve `'["Goku" , 12 , 13 , 14]'` imitando visualmente una lista estándar en lugar de indicar la clase `Guerrero`.

**Advertencia crítica de seguridad sobre `eval(repr(obj))`.** En `Metodos_Especiales.py` (L42-45, L59-72) se ejecuta `repre = repr(one)` seguido de `resultado = eval(repre)` sobre un `__repr__` escrito como `f'Persona("{self.nombre}",{self.edad})'` (L23). Es imprescindible establecer dos precisiones técnicas:

1. La expresión `obj == eval(repr(obj))` citada en la documentación clásica es únicamente una **heurística orientativa de formato** (sugiriendo que `repr` luzca como una llamada válida al constructor cuando sea razonable), **jamás un mecanismo de deserialización en producción**.
2. Invocar `eval()` sobre cadenas que incorporen datos externos no confiables abre una vulnerabilidad crítica de **ejecución remota o arbitraria de código** (*Arbitrary Code Execution*): si `self.nombre` contuviera comillas dobles e instrucciones maliciosas, `eval()` las ejecutaría con todos los privilegios del proceso. Para formatear atributos dentro de `__repr__` debe usarse siempre el conversor `!r` (`f"Persona({self.nombre!r}, {self.edad!r})"`) que escapa comillas de forma segura, y para persistir o reconstruir objetos deben emplearse formatos de datos puros (`json`, constructores explícitos `from_dict` o `ast.literal_eval` exclusivamente sobre literales).

**Sobrecarga de operadores aritméticos, corrección de Python 3 (`__truediv__`) y protocolo `NotImplemented`.** En `Metodos_Especiales.py` (L98-113), `One.py` (L48-67), `Juego.py` (L75-90, L95-170) y `Ejercicio_2.png` se sobrecargan `+` (`__add__`) y `-` (`__sub__`). Al consultar la tabla gráfica `Sobrecarga_Operadores.png` debe aplicarse una **corrección histórica obligatoria respecto de Python 2 frente a Python 3**:

- La lámina `Sobrecarga_Operadores.png` enumera `__div__(self, other)` para el operador `/` y `__idiv__(self, other)` para `/=`. **Ambos métodos fueron eliminados en Python 3**: declararlos en una clase actual es código muerto que no intercepta `/` (produciendo `TypeError`).
- Python 3 separa explícitamente la división real (`/` y `/=`) mediante **`__truediv__`** e **`__itruediv__`**, y la división entera hacia abajo (`//` y `//=`) mediante **`__floordiv__`** e **`__ifloordiv__`**.

Asimismo, la evaluación de un operador binario `a + b` sigue un protocolo cooperativo en tres pasos gobernado por el *singleton* integrado **`NotImplemented`** (que no debe confundirse con la excepción `NotImplementedError`):

```text
Expresión: a + b
  1. Python invoca type(a).__add__(a, b)
     ├─ Si reconoce el tipo de b ──► calcula y retorna un NUEVO objeto resultado
     └─ Si NO reconoce el tipo de b ──► DEBE hacer 'return NotImplemented'
  2. Si el paso 1 retornó NotImplemented (y type(a) is not type(b)):
     Python intenta el método reflejado type(b).__radd__(b, a)
  3. Si ambos retornan NotImplemented:
     El propio intérprete lanza TypeError con un mensaje estándar uniforme
```

Si `__add__` lanza manualmente `raise TypeError` ante un operando desconocido en lugar de retornar `NotImplemented`, **bloquea el paso 2** e impide que el operando derecho resuelva la operación mediante `__radd__` o `__rmul__` (por ejemplo, al evaluar `2 * vector` donde `int.__mul__(2, vector)` retorna `NotImplemented` cediendo el turno a `Vector.__rmul__(vector, 2)`). Finalmente, los operadores aritméticos sobre objetos de valor deben ser **funciones puras sin efectos secundarios**: nunca deben mutar `self` ni ejecutar `print()` en consola como ocurre en `Metodos_Especiales.py` (L103), `One.py` (L59) y `Juego.py` (L89, L168), y deben respetar una semántica intuitiva (evitando que `g1 - g2` retorne una tupla de cadenas de combate como en `Juego.py` L95-170, acción que corresponde a un método explícito `combatir_contra(otro)`).

**Comparaciones ricas (`__eq__`, `@functools.total_ordering`) y el contrato de `__hash__`.** Los operadores relacionales se implementan mediante `__eq__` (`==`), `__ne__` (`!=`, que en Python 3 delega automáticamente negando `__eq__`), `__lt__` (`<`), `__le__` (`<=`), `__gt__` (`>`) y `__ge__` (`>=`). Para no escribir seis métodos repetitivos, el [decorador](decoradores.md) estándar `@functools.total_ordering` genera todos los comparadores de orden a partir de `__eq__` y uno solo de ellos (habitualmente `__lt__`).

Aquí rige una regla crucial del Modelo de Datos sobre **hashabilidad**: las tablas hash (`set`, `frozenset` y claves de `dict`) exigen el invariante matemático `a == b  ==>  hash(a) == hash(b)`. Por ello, **en cuanto una clase define `__eq__` sin definir `__hash__`, Python asigna automáticamente `__hash__ = None`**, bloqueando su uso en conjuntos o como clave de diccionario con `TypeError: unhashable type`. Si la clase es **mutable**, debe permanecer no *hashable*; si representa un **objeto de valor inmutable**, puede restablecer su hashabilidad definiendo `__hash__` a partir de una tupla con los mismos campos inmutables empleados en `__eq__`.

**Protocolos de contenedor e instancias invocables (`__len__`, `__getitem__`, `__contains__`, `__call__`).** Tal como resume la sección inferior de `Sobrecarga_Operadores.png`, implementar `__len__` habilita `len(obj)` (y el valor de verdad implícito `bool(obj)` si no existe `__bool__`), `__getitem__` habilita la indexación `obj[clave]` o rebanadas (`slice`), `__contains__` optimiza el operador `in`, y `__call__` permite invocar una instancia como si fuera una función (`instancia(arg)`), base de objetos de estrategia con estado y decoradores basados en clases.

## 4. Sintaxis y funcionamiento

Plantilla idiomática de un objeto de valor inmutable con representación segura, aritmética cooperativa, orden total y soporte hash:

```text
from functools import total_ordering

@total_ordering
class Monto:
    def __init__(self, centavos: int, moneda: str = "PEN") -> None:
        self._centavos = int(centavos)
        self._moneda = moneda.upper()

    def __repr__(self) -> str:
        return f"Monto(centavos={self._centavos!r}, moneda={self._moneda!r})"

    def __str__(self) -> str:
        return f"{self._centavos / 100:.2f} {self._moneda}"

    def __add__(self, otro: object) -> "Monto":
        if not isinstance(otro, Monto):
            return NotImplemented
        if self._moneda != otro._moneda:
            raise ValueError("Monedas incompatibles")
        return Monto(self._centavos + otro._centavos, self._moneda)

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Monto):
            return NotImplemented
        return (self._centavos, self._moneda) == (otro._centavos, otro._moneda)

    def __lt__(self, otro: object) -> bool:
        if not isinstance(otro, Monto) or self._moneda != otro._moneda:
            return NotImplemented
        return self._centavos < otro._centavos

    def __hash__(self) -> int:
        return hash((self._centavos, self._moneda))
```

Catálogo de referencia de métodos especiales esenciales en Python 3:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `__init__(self, ...)` | Inicializa el estado de la instancia recién creada por `__new__` | `p = Personaje("Goku", 200)` |
| 2 | `__repr__(self)` | Representación técnica inequívoca para depuración (`!r` obligatorio en campos) | `repr(p)` -> `"Personaje('Goku', 200)"` |
| 3 | `__str__(self)` | Representación legible para usuario final; si se omite, cae en `__repr__` | `print(p)` -> `"Goku (Fuerza: 200)"` |
| 4 | `__add__` / `__radd__` / `__iadd__` | Suma directa (`a + b`), reflejada (`b + a`) y compuesta (`a += b`) | `fusion = goku + vegeta` |
| 5 | `__sub__` / `__mul__` / `__rmul__` | Resta (`-`), producto (`*`) y producto escalar reflejado (`2 * v`) | `doble = 2 * vector` |
| 6 | `__truediv__` / `__floordiv__` | División real (`/`) y división entera (`//`) en **Python 3** (sustituyen a `__div__`) | `mitad = vector / 2` |
| 7 | `NotImplemented` | Constante retornada cuando el tipo del operando no está soportado | `return NotImplemented` |
| 8 | `__eq__` / `__lt__` + `@total_ordering` | Igualdad estructural (`==`) y ordenamiento completo (`<`, `<=`, `>`, `>=`) | `sorted(versiones)` |
| 9 | `__hash__(self)` | Entero hash consistente con `__eq__` en objetos estrictamente inmutables | `{v1, v2}` / `{v1: "estable"}` |
| 10 | `__len__` / `__getitem__` / `__contains__` | Protocolo de colección: `len(c)`, indexación `c[i]` y pertenencia `x in c` | `if "arma" in inventario:` |
| 11 | `__call__(self, ...)` | Convierte una instancia en un objeto invocable con sintaxis de función | `filtro(registro)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Distinción práctica entre `__str__` y `__repr__` seguro con `!r`, formateo en colecciones y regla de respaldo.**

```python
class Personaje:
    def __init__(self, nombre: str, fuerza: int, velocidad: int) -> None:
        self.nombre = nombre
        self.fuerza = int(fuerza)
        self.velocidad = int(velocidad)

    def __repr__(self) -> str:
        # El conversor !r escapa comillas y preserva el tipo exacto de cada argumento
        return (
            f"Personaje(nombre={self.nombre!r}, "
            f"fuerza={self.fuerza!r}, velocidad={self.velocidad!r})"
        )

    def __str__(self) -> str:
        return f"{self.nombre} [Fuerza={self.fuerza}, Velocidad={self.velocidad}]"


class PuntoCoordenada:
    """Define únicamente __repr__; str() delegará automáticamente en él."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"PuntoCoordenada(x={self.x!r}, y={self.y!r})"


heroe = Personaje('Goku "Saiyajin"', fuerza=200, velocidad=12)
punto = PuntoCoordenada(4, -7)

print("Salida __str__ :", heroe)
print("Salida __repr__:", repr(heroe))
print("En una lista   :", [heroe])
print("Respaldo str() :", str(punto), "| repr():", repr(punto))
```

Explicación paso a paso:

- Refinando `Metodos_Especiales.py` (L18-24) y `One.py` (L42-46), usar `self.nombre!r` dentro de `__repr__` escapa limpiamente las comillas internas de `'Goku "Saiyajin"'` sin romper la sintaxis ni recurrir a `eval()`.
- Al imprimir una lista `[heroe]`, Python invoca `__repr__` sobre sus elementos internos para evitar ambigüedades; por su parte, `PuntoCoordenada` demuestra que implementar `__repr__` cubre también `str(punto)`.

Resultado esperado:

```text
Salida __str__ : Goku "Saiyajin" [Fuerza=200, Velocidad=12]
Salida __repr__: Personaje(nombre='Goku "Saiyajin"', fuerza=200, velocidad=12)
En una lista   : [Personaje(nombre='Goku "Saiyajin"', fuerza=200, velocidad=12)]
Respaldo str() : PuntoCoordenada(x=4, y=-7) | repr(): PuntoCoordenada(x=4, y=-7)
```

### Intermedio

**Ejemplo 2 — Sobrecarga algebraica inmutable (`__add__`, `__sub__`, `__mul__`, `__rmul__`, `__truediv__`, `__floordiv__`) y cooperación mediante `NotImplemented`.**

```python
class Vector2D:
    """Objeto de valor inmutable que modela desplazamientos bidimensionales."""

    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"Vector2D({self._x!r}, {self._y!r})"

    def __add__(self, otro: object) -> "Vector2D":
        if not isinstance(otro, Vector2D):
            return NotImplemented
        return Vector2D(self._x + otro._x, self._y + otro._y)

    def __sub__(self, otro: object) -> "Vector2D":
        if not isinstance(otro, Vector2D):
            return NotImplemented
        return Vector2D(self._x - otro._x, self._y - otro._y)

    def __mul__(self, escalar: object) -> "Vector2D":
        if not isinstance(escalar, (int, float)):
            return NotImplemented
        return Vector2D(self._x * escalar, self._y * escalar)

    def __rmul__(self, escalar: object) -> "Vector2D":
        # Permite 3 * v cuando int.__mul__(3, v) retorna NotImplemented
        return self.__mul__(escalar)

    def __truediv__(self, divisor: object) -> "Vector2D":
        if not isinstance(divisor, (int, float)):
            return NotImplemented
        if divisor == 0:
            raise ZeroDivisionError("No se puede dividir un Vector2D entre cero")
        return Vector2D(self._x / divisor, self._y / divisor)

    def __floordiv__(self, divisor: object) -> "Vector2D":
        if not isinstance(divisor, (int, float)):
            return NotImplemented
        if divisor == 0:
            raise ZeroDivisionError("No se puede dividir un Vector2D entre cero")
        return Vector2D(self._x // divisor, self._y // divisor)


v1 = Vector2D(9, 15)
v2 = Vector2D(3, 5)

print("Suma (v1 + v2)           :", v1 + v2)
print("Resta (v1 - v2)          :", v1 - v2)
print("Escalar reflejado (3 * v2):", 3 * v2)
print("División real (v1 / 2)   :", v1 / 2)
print("División entera (v1 // 2):", v1 // 2)
print("Operandos originales intactos:", v1, "|", v2)

try:
    _ = v1 + "texto_incompatible"
except TypeError as err:
    print("Fallo limpio por NotImplemented:", type(err).__name__)
```

Explicación técnica:

- Ningún operador muta `v1` ni `v2` ni imprime mensajes laterales: cada expresión construye un nuevo `Vector2D` puro.
- Al evaluar `3 * v2`, `int.__mul__(3, v2)` retorna `NotImplemented` y Python delega automáticamente en `Vector2D.__rmul__(v2, 3)`. Además, `__truediv__` (`/`) y `__floordiv__` (`//`) muestran los métodos reales vigentes en Python 3 frente a los obsoletos `__div__` / `__idiv__` de `Sobrecarga_Operadores.png`.

Resultado esperado:

```text
Suma (v1 + v2)           : Vector2D(12.0, 20.0)
Resta (v1 - v2)          : Vector2D(6.0, 10.0)
Escalar reflejado (3 * v2): Vector2D(9.0, 15.0)
División real (v1 / 2)   : Vector2D(4.5, 7.5)
División entera (v1 // 2): Vector2D(4.0, 7.0)
Operandos originales intactos: Vector2D(9.0, 15.0) | Vector2D(3.0, 5.0)
Fallo limpio por NotImplemented: TypeError
```

### Avanzado

**Ejemplo 3 — Ordenamiento total (`@functools.total_ordering`), invariante `__eq__`/`__hash__` en objetos inmutables y contenedor invocable (`__len__`, `__getitem__`, `__contains__`, `__call__`).**

```python
from functools import total_ordering


@total_ordering
class VersionSemantica:
    """Versión inmutable comparable y apta como clave en set y dict."""

    def __init__(self, mayor: int, menor: int, parche: int) -> None:
        self._partes = (int(mayor), int(menor), int(parche))

    def __repr__(self) -> str:
        return f"VersionSemantica{self._partes!r}"

    def __str__(self) -> str:
        return f"{self._partes[0]}.{self._partes[1]}.{self._partes[2]}"

    @property
    def mayor(self) -> int:
        return self._partes[0]

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, VersionSemantica):
            return NotImplemented
        return self._partes == otro._partes

    def __lt__(self, otro: object) -> bool:
        if not isinstance(otro, VersionSemantica):
            return NotImplemented
        return self._partes < otro._partes

    def __hash__(self) -> int:
        return hash(self._partes)


class CatalogoLanzamientos:
    """Contenedor ordenable e invocable para filtrar versiones compatibles."""

    def __init__(self, versiones: list[VersionSemantica]) -> None:
        self._versiones = sorted(set(versiones))

    def __len__(self) -> int:
        return len(self._versiones)

    def __getitem__(self, indice: int) -> VersionSemantica:
        return self._versiones[indice]

    def __contains__(self, candidata: object) -> bool:
        return candidata in self._versiones

    def __call__(self, rama_mayor: int) -> list[str]:
        return [str(v) for v in self._versiones if v.mayor == rama_mayor]


v_a = VersionSemantica(2, 1, 0)
v_b = VersionSemantica(2, 1, 0)  # Duplicado lógico de v_a
v_c = VersionSemantica(1, 9, 4)
v_d = VersionSemantica(2, 0, 3)

catalogo = CatalogoLanzamientos([v_a, v_b, v_c, v_d])

print("Igualdad y hash consistente:", v_a == v_b, "|", hash(v_a) == hash(v_b))
print("Cantidad única (deduplicada por set):", len(catalogo))
print("Ordenadas (menor a mayor):", [str(catalogo[i]) for i in range(len(catalogo))])
print("¿Existe 1.9.4 en catálogo?:", VersionSemantica(1, 9, 4) in catalogo)
print("Filtro invocable rama 2.x :", catalogo(rama_mayor=2))
```

Explicación de arquitectura:

- `VersionSemantica` almacena su estado en una tupla privada inmutable `_partes` y define tanto `__eq__` como `__hash__`, lo que permite deduplicar instancias equivalentes con `set(versiones)` y ordenarlas mediante `@total_ordering` implementando solo `__eq__` y `__lt__`.
- `CatalogoLanzamientos` integra cuatro protocolos del Modelo de Datos: cardinalidad (`len`), acceso indexado (`catalogo[i]`), verificación de pertenencia (`in`) y consulta funcional parametrizada (`catalogo(rama_mayor=2)`) mediante `__call__`.

Resultado esperado:

```text
Igualdad y hash consistente: True | True
Cantidad única (deduplicada por set): 3
Ordenadas (menor a mayor): ['1.9.4', '2.0.3', '2.1.0']
¿Existe 1.9.4 en catálogo?: True
Filtro invocable rama 2.x : ['2.0.3', '2.1.0']
```

## 6. Aplicaciones en el mundo real

- **Manipulación de rutas del sistema de archivos (`pathlib.Path`):** la biblioteca estándar sobrecarga `__truediv__` (`/`) para unir segmentos de directorios de manera multiplataforma (`Path("/var") / "log" / "app.log"`).
- **Aritmética temporal y monetaria exacta:** `datetime.date`, `datetime.timedelta` y `decimal.Decimal` implementan `__add__`, `__sub__` y comparaciones ricas para operar fechas e importes financieros sin errores de coma flotante.
- **Computación científica y análisis tabular:** `numpy.ndarray` y `pandas.Series` redefinen los operadores aritméticos y relacionales para ejecutar operaciones vectorizadas en C sobre millones de datos simultáneamente.
- **Constructores declarativos de consultas ORM:** bibliotecas como SQLAlchemy y Django Q sobrecargan `__eq__`, `__and__` (`&`) y `__or__` (`|`) sobre descriptores de columnas para construir árboles de expresiones SQL parametrizadas sin concatenar cadenas.
- **Inferencia en aprendizaje automático:** marcos como PyTorch definen `__call__` en `nn.Module` para ejecutar ganchos (*hooks*) de preprocesamiento y postprocesamiento alrededor del método `forward()` al invocar `modelo(entrada)`.

## 7. Uso en producción

- **No reinventar clases de datos manuales cuando baste `@dataclass`:** si una entidad solo requiere `__init__`, `__repr__`, `__eq__`, ordenamiento y hashabilidad estándar sobre sus campos, `@dataclass(frozen=True, order=True)` los sintetiza automáticamente sin errores humanos.
- **Retornar siempre `NotImplemented` en operadores binarios y comparaciones ante tipos ajenos:** permite que subclases o tipos externos cooperen mediante métodos reflejados (`__radd__`, `__eq__` simétrico) sin acoplar las clases entre sí.
- **Mantener los métodos especiales libres de E/S y con complejidad predecible:** ni `__repr__`, ni `__eq__`, ni `__add__` deben imprimir por pantalla, abrir archivos ni realizar peticiones de red, dado que depuradores y marcos de registro invocan `repr()` automáticamente ante cualquier excepción.
- **Sobrecargar operadores únicamente cuando exista una analogía algebraica clara:** sumar vectores, importes o intervalos de tiempo mejora la legibilidad; usar `-` para simular una batalla devolviendo texto (`Juego.py` L95-170) oscurece el significado del código frente a un método con nombre de dominio explícito.

## 8. Errores comunes y recomendaciones

1. **Definir `__div__` (eliminado en Python 3) o lanzar `TypeError` directamente bloqueando operadores reflejados.**

```python
# ERROR INTENCIONAL: uso de __div__ obsoleto de Python 2 (Sobrecarga_Operadores.png) y bloqueo de __rmul__
class EscalaAntigua:
    def __init__(self, valor: float) -> None:
        self.valor = valor

    def __div__(self, otro: float) -> "EscalaAntigua":
        # En Python 3 este método jamás es invocado por el operador '/'
        return EscalaAntigua(self.valor / otro)

    def __add__(self, otro: object) -> "EscalaAntigua":
        if not isinstance(otro, EscalaAntigua):
            raise TypeError("Tipo inválido")  # Impide que Python intente otro.__radd__(self)
        return EscalaAntigua(self.valor + otro.valor)


# EscalaAntigua(10.0) / 2 lanza TypeError: unsupported operand type(s) for /: 'EscalaAntigua' and 'int'
```

Diagnóstico: en Python 3 el operador `/` invoca exclusivamente `__truediv__` (y `//` invoca `__floordiv__`). Asimismo, ante tipos desconocidos debe escribirse `return NotImplemented` en lugar de `raise TypeError`.

2. **Reconstruir objetos con `eval(repr(obj))` o interpolar cadenas sin `!r` en `__repr__`.**

```python
# ERROR INTENCIONAL: vulnerabilidad de ejecución arbitraria de código al usar eval() sobre repr()
class UsuarioInseguro:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def __repr__(self) -> str:
        # Interpolación sin !r: comillas en self.nombre rompen la expresión y permiten inyección
        return f'UsuarioInseguro("{self.nombre}")'


# Si nombre proviene de una entrada externa maliciosa, eval(repr(u)) ejecuta código arbitrario
```

Diagnóstico: a raíz del ejemplo en `Metodos_Especiales.py` (L23, L44), debe recordarse que `eval()` compila y ejecuta cualquier expresión Python arbitraria. En `__repr__` debe usarse siempre `{self.nombre!r}`, y para deserializar datos deben emplearse formatos declarativos seguros como `json.loads()`.

3. **Perder la capacidad de usar instancias en `set` o `dict` tras definir `__eq__`, o implementar `__hash__` sobre atributos mutables.**

```python
# ERROR INTENCIONAL: definir __eq__ desactiva __hash__ automáticamente; mutar claves corrompe dict/set
class EtiquetaMutable:
    def __init__(self, codigo: str) -> None:
        self.codigo = codigo

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, EtiquetaMutable):
            return NotImplemented
        return self.codigo == otro.codigo


# {EtiquetaMutable("A")} lanza TypeError: unhashable type: 'EtiquetaMutable'
```

Diagnóstico: Python establece `EtiquetaMutable.__hash__ = None` como medida de protección porque si un objeto cambiara su `codigo` estando ya dentro de un `set`, su cubeta (*bucket*) hash quedaría desincronizada y el elemento se volvería ilocalizable. Solo las clases cuyos campos comparados sean estrictamente inmutables deben definir `__hash__`.

## 9. Resumen

- El **Modelo de Datos de Python** conecta las clases definidas por el usuario con los operadores y funciones nativas mediante métodos especiales `__dunder__`, resueltos por el intérprete sobre el **tipo** del objeto (`type(x)`) mediante ranuras rápidas en CPython (*type slots*).
- **`__repr__`** proporciona una representación técnica inequívoca para desarrolladores (formateando sus campos con `!r` y actuando como respaldo automático si falta `__str__`), mientras que **`__str__`** ofrece una vista legible para usuarios finales; nunca debe usarse `eval(repr(x))` sobre datos no confiables.
- En **Python 3**, la división `/` corresponde a **`__truediv__`** y `//` a **`__floordiv__`** (habiendo desaparecido `__div__` e `__idiv__` de Python 2), y todo operador binario o relacional debe retornar la constante **`NotImplemented`** ante tipos desconocidos para permitir métodos reflejados (`__radd__`, `__rmul__`).
- Los operadores aritméticos deben comportarse como **operaciones puras** que retornen nuevas instancias sin mutar sus operandos ni imprimir en consola.
- Definir **`__eq__`** anula automáticamente **`__hash__` (`None`)**; únicamente los objetos de valor inmutables deben restaurar `__hash__`, pudiendo completar todos sus comparadores de orden mediante **`@functools.total_ordering`**.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Metodos_Especiales.py` (L1-113) | `Metodos_Especiales.py` | Definición de métodos dunder (`__init__`, `__str__`, `__repr__`), uso de `eval(repr(one))` (L42-45) y sobrecarga de `+` con `__add__` sumando edades de `Persona` | Se incorporó la advertencia de seguridad contra ejecución arbitraria en `eval()`, el uso de `!r` en `__repr__`, la eliminación de `print()` dentro de `__add__` y el protocolo `NotImplemented` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/One.py` (L1-68) | `One.py` | Clase `Personaje` con `__str__`, `__repr__` y fusión encadenada `Goku + Vegeta + Broly` mediante `__add__` | Se preservó la semántica inmutable retornando instancias nuevas sin efectos secundarios de consola y validando tipos de operandos |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio/Juego.py` (L33-173, L495, L589) | `Juego.py` | Clase `Guerrero` con `__str__`, `__repr__` en formato lista, fusión con `__add__` (`g1 + g2`) y batalla con `__sub__` (`g1 - g2`) | Se analizó por qué `__repr__` debe identificar la clase y por qué sobrecargar `-` para retornar una tupla de texto de combate rompe la intuición algebraica |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Ejercicio_2.png` | `Ejercicio_2.png` | Captura de ejecución del menú interactivo de creación y fusión de personajes del ejercicio práctico | Se trasladó la lógica de dominio a ejemplos deterministas autoejecutables desacoplados de `input()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Sobrecarga_Operadores.png` | `Sobrecarga_Operadores.png` | Tabla de operadores aritméticos (`__add__`, `__sub__`, `__mul__`, `__div__`, `__mod__`, `__pow__`), comparación, asignación (`__iadd__`...`__idiv__`) y otros (`__str__`, `__len__`, `__getitem__`) | Se corrigieron explícitamente `__div__` e `__idiv__` (exclusivos de Python 2 y eliminados en Python 3), sustituyéndolos por `__truediv__`/`__itruediv__` y `__floordiv__`/`__ifloordiv__` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/MODULOS_IMPORT/saludo_name.py` (L1-11) | `saludo_name.py` | Módulo auxiliar base cuya variante instrumentada en `PAQUETE/Saludar.py` (L12) y `MÓDULOS.py` (L116-119) inspecciona el atributo especial `__name__` | Se contextualizó `__name__` (`"__main__"` frente al nombre calificado del módulo) dentro de la convención reservada de nombres dunder del lenguaje |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/MÓDULOS.py` (L115-119) | `MÓDULOS.py` | Lectura de `Saludar.__name__` y `__name__` en el guion principal | Se integró con las guardas de ejecución `if __name__ == "__main__":` vistas en `Decoradores_Clases.py` (L57) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_THREE/CLASE_TERCERA/PAQUETE.py` (L6-24, L40-42) | `PAQUETE.py` | Reconocimiento de paquetes mediante `__init__.py` e inspección de rutas de búsqueda en `PAQUETE.__path__` | Se distinguió entre atributos especiales del sistema de importación (`__name__`, `__path__`) y métodos especiales del Modelo de Datos en clases |

**Fundamento complementario:** se añadieron cinco piezas centrales del Modelo de Datos de Python 3: (1) la resolución implícita sobre `type(x)` y las ranuras en C (`tp_str`, `nb_add`) de CPython; (2) el despacho cooperativo mediante `NotImplemented` y operadores reflejados (`__radd__`, `__rmul__`); (3) `@functools.total_ordering` para comparaciones ricas sin código repetitivo; (4) la relación estricta entre `__eq__`, inmutabilidad y `__hash__`; y (5) los protocolos `__contains__` y `__call__`.

## 11. Referencias oficiales

- <https://docs.python.org/3/reference/datamodel.html> — Referencia del lenguaje (*Data model*): especificación completa de `__repr__`, `__str__`, `__hash__`, emulación de tipos numéricos, contenedores, objetos invocables y búsqueda de métodos especiales sobre el tipo.
- <https://docs.python.org/3/library/functools.html#functools.total_ordering> — Biblioteca estándar (`functools.total_ordering`): generación automática de métodos de ordenamiento rico.
- <https://docs.python.org/3/library/functions.html#repr> — Funciones integradas (`repr`, `str`, `hash`, `len`): contratos y reglas de respaldo del intérprete.
- <https://docs.python.org/3/library/operator.html> — Módulo estándar `operator`: correspondencia funcional exacta de todos los operadores de Python 3 (`truediv`, `floordiv`, `add`, `getitem`).
