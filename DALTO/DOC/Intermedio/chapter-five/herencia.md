# Herencia, Delegación con `super()`, Introspección Jerárquica y Composición frente a Agregación

## 2. Introducción

Cuando distintas entidades de un dominio comparten atributos estructurales y reglas comunes —como `Empleado` y `Estudiante` respecto de `Persona` (`Herencia.py` L14-60), o excepciones específicas respecto de `Exception` (`Mi_Excepcion.py` L4)—, duplicar la misma lógica en clases inconexas multiplica el esfuerzo de mantenimiento y propicia divergencias ante cualquier corrección.

La **herencia** permite definir nuevas [clases](clases_y_objetos.md) especializadas (**subclases** o clases derivadas) a partir de clases existentes (**superclases** o clases base), reutilizando y refinando su contrato. Sin embargo, utilizar la herencia de forma indiscriminada produce jerarquías rígidas difíciles de evolucionar. Dominar este capítulo requiere equilibrar cuatro ejes fundamentales:

1. **Relación semántica "es-un" (*is-a*) y raíz implícita `object`:** comprender cómo Python 3 unifica todos los tipos bajo una única raíz común.
2. **Delegación limpia mediante `super()`:** inicializar estado heredado y **extender** métodos de la base (`EJERCICIO_DOS.py` L25-29) sin acoplarse a nombres rígidos de clases padre.
3. **Verificación jerárquica en ejecución:** diferenciar `isinstance()` e `issubclass()` respecto de comparaciones estrictas con `type()`.
4. **Composición y agregación ("tiene-un" / *has-a*):** distinguir ciclos de vida entre partes poseídas y colaboradores inyectados (`SRP.py` L94-96, `DIP.py` L32-73), aplicando el principio de ingeniería de **favorecer la composición sobre la herencia**.

## 3. Fundamentos y conceptos

**Relación "es-un" (*is-a*) y herencia implícita de `object` en Python 3.** Declarar `class Subclase(Superclase):` establece un vínculo taxonómico: toda instancia de `Subclase` **es también una** instancia legítima de `Superclase` (`Usar_Herencia.py` L1-20). En Python 3 todas las clases son de "nuevo estilo" (*new-style classes*) y heredan implícitamente de la raíz universal `object`:

```python
class Persona:        # Exactamente equivalente en Python 3 a: class Persona(object):
    pass
```

Gracias a esta raíz común (`issubclass(Persona, object) == True`), toda clase dispone de inmediato de los mecanismos base del modelo de datos (`__new__`, `__init__`, `__repr__`, `__eq__`, descriptores).

**Modalidades estructurales de herencia.** Según la topología de la jerarquía se distinguen cuatro configuraciones clásicas:

```text
Simple               Jerárquica                   Multinivel
Animal               Persona                      Exception
  └── Perro            ├── Empleado                 └── ErrorDominio
                       └── Estudiante                     └── CupoAgotadoError
```

- **Herencia simple:** una subclase deriva de una única superclase directa (`Estudiante(Persona)` en `EJERCICIO_DOS.py` L23).
- **Herencia jerárquica:** múltiples subclases hermanas especializan una misma superclase común (`Empleado(Persona)` y `Estudiante(Persona)` en `Herencia.py` L24-60).
- **Herencia multinivel:** cadena transitiva donde una subclase sirve a su vez como base de otra más específica (`Vehiculo -> Motorizado -> Camioneta`).
- **Herencia múltiple:** una clase combina dos o más bases directas (`Murcielago(Mamifero, Ave)` en `EJERCICIO_DOS_TWO.py` L30). Su algoritmo de linealización C3 y la resolución de diamantes se estudian en profundidad en [MRO y herencia múltiple](../../Avanzado/chapter-two/mro_herencia_multiple.md).

**Reutilización, sobrescritura y extensión mediante `super()`.** Una subclase puede interactuar con los [atributos y métodos](atributos_y_metodos.md) heredados de tres maneras complementarias:

1. **Heredar sin cambios:** si la subclase no redefine un método (p. ej. `dog.comer()` en `Usar_Herencia.py` L28), Python lo resuelve automáticamente en la superclase.
2. **Reemplazar (sobrescritura total):** definir un método con el mismo nombre sustituye la versión del padre (`saludar()` en `Herencia.py` L39, L58; `sonido()` en `Usar_Herencia.py` L18), habilitando el [polimorfismo](polimorfismo.md).
3. **Extender cooperativamente con `super()`:** con mucha frecuencia la subclase no desea descartar la lógica del padre, sino ejecutarla y añadir estado o comportamiento adicional. Así ocurre en `EJERCICIO_DOS.py` tanto en el inicializador (`super().__init__(nombre, edad)` seguido de `self.grado = grado`, L25-26) como en un método regular (`f"{super().Presentarse()}, y estoy en el grado {self.grado}."`, L29).

**Por qué `super().__init__(...)` supera a `Padre.__init__(self, ...)` (y el fallo latente de `Herencia.py` L86-93).** Invocar `super()` devuelve un objeto *proxy* que delega dinámicamente en la siguiente clase del **Orden de Resolución de Métodos (MRO)** de la instancia, evitando fijar manualmente el nombre de la clase base. Mezclar ambos estilos ocasiona defectos críticos: en `Herencia.py` (L86-93), `Estudiante` y `Empleado` usan internamente `super().__init__(nombre, edad, nacionalidad)`, mientras que `Estudiante_Trabajador(Estudiante, Empleado)` intenta llamarlos explícitamente por nombre (`Estudiante.__init__(self, ...)` en L88). Al ejecutarse, `super().__init__` dentro de `Estudiante` no salta a `Persona`, sino al siguiente elemento del MRO de `Estudiante_Trabajador`, que es `Empleado`, pasándole solo 3 argumentos cuando `Empleado.__init__` exige 6, disparando inmediatamente `TypeError: Empleado.__init__() missing 3 required positional arguments`. La solución cooperativa completa se desarrolla en [MRO y herencia múltiple](../../Avanzado/chapter-two/mro_herencia_multiple.md).

**Introspección de tipos y linaje: `isinstance()` e `issubclass()`.** Para consultar relaciones de herencia en tiempo de ejecución nunca debe emplearse `type(obj) is ClaseBase` si se desea admitir subclases, pues `type(obj)` devuelve únicamente la clase exacta de instanciación:

- `isinstance(obj, ClaseO_TuplaDeClases)`: retorna `True` si `obj` es ejemplar directo de la clase indicada o de **cualquier subclase** descendiente (`isinstance(dog, Animal) == True`). Conviene recordar una particularidad histórica del modelo de tipos de Python: **`bool` es subclase de `int`** (`issubclass(bool, int) == True`), por lo que `isinstance(True, int)` evalúa a `True`.
- `issubclass(Sub, Base)`: verifica entre objetos clase si `Sub` deriva directa o indirectamente de `Base` (considerándose toda clase subclase impropia de sí misma: `issubclass(Animal, Animal) == True`).

**Composición y agregación ("tiene-un" / *has-a*) frente a herencia.** Muchos diseños fallan cuando fuerzan herencia donde en realidad existe una relación de **colaboración o pertenencia ("tiene-un")**: un automóvil *no es* un tanque de combustible, sino que **tiene un** tanque (`SRP.py` L92-97); un corrector ortográfico *no es* un diccionario, sino que **utiliza un** verificador (`DIP.py` L64-70). Dentro de las asociaciones *tiene-un* la arquitectura orientada a objetos distingue dos grados según la **propiedad del ciclo de vida**:

| Relación | Vínculo conceptual | Creación y ciclo de vida del componente | Ejemplo en el repositorio |
|---|---|---|---|
| **Herencia** | *Es-un* (*is-a*) | Subclase especializa a la base en tiempo de compilación/definición | `Perro(Animal)` (`Usar_Herencia.py` L13) |
| **Composición** | *Parte-de* exclusivo (*owns-a*) | El contenedor **instancia internamente** al componente y gobierna su vida; si el contenedor desaparece, la parte también | `self.diccionario = Diccionario()` dentro de `__init__` (`DIP.py` L32-35) |
| **Agregación** | *Tiene-un* independiente (*uses-a*) | El componente se crea **fuera** y se inyecta al contenedor; sobrevive aunque el contenedor se destruya y puede compartirse o sustituirse | `Auto(tanque)` (`SRP.py` L94-125), `CorrectorOrtografico(verificador)` (`DIP.py` L64-73), `AnalizadorDeSentimientos(rangos)` (`Con_TextBlob.py` L14-35) |

**Por qué favorecer la composición/agregación sobre la herencia profunda.** El principio clásico del diseño orientado a objetos (*"Favor object composition over class inheritance"*) responde al **problema de la clase base frágil**: en jerarquías profundas, cualquier cambio menor en los atributos internos o métodos de la superclase puede quebrar inadvertidamente decenas de subclases acopladas a su implementación. La agregación mediante inyección de colaboradores permite cambiar comportamientos en tiempo de ejecución (p. ej. alternar entre `Diccionario` local y `ServicioOnline` en `DIP.py` L72-73), evita la explosión combinatoria de subclases y simplifica radicalmente las pruebas unitarias mediante dobles de prueba (*fakes* o *mocks*), fundamento directo de los [principios SOLID](../../Avanzado/chapter-two/principios_solid.md).

## 4. Sintaxis y funcionamiento

Esquema comparativo entre especialización por herencia (`super()`) y delegación por agregación:

```text
# 1. Herencia ("es-un"): Subclase especializa e invoca super()
class Base:
    def __init__(self, id_entidad: str) -> None:
        self.id_entidad = id_entidad

    def describir(self) -> str:
        return f"ID={self.id_entidad}"


class Derivada(Base):
    def __init__(self, id_entidad: str, nivel: int) -> None:
        super().__init__(id_entidad)
        self.nivel = nivel

    def describir(self) -> str:
        return f"{super().describir()} | Nivel={self.nivel}"


# 2. Agregación ("tiene-un"): Servicio delega en un colaborador externo
class ServicioProcesamiento:
    def __init__(self, politica_reintento: Politica) -> None:
        self._politica = politica_reintento
```

Referencia de elementos sintácticos e introspección de herencia:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `class Hija(Padre):` | Declara que `Hija` hereda atributos y métodos de `Padre` | `class Estudiante(Persona):` |
| 2 | `super().__init__(...)` | Inicializa la porción de estado correspondiente a la superclase | `super().__init__(nombre, edad)` |
| 3 | `super().metodo(...)` | Invoca la implementación heredada para extender su resultado | `base = super().Presentarse()` |
| 4 | `isinstance(obj, C)` | Comprueba si `obj` es instancia de `C` o de alguna subclase suya | `isinstance(est, Persona)` |
| 5 | `isinstance(o, (A, B))` | Comprueba pertenencia contra una tupla de múltiples clases | `isinstance(x, (int, float))` |
| 6 | `issubclass(Sub, Base)` | Evalúa si la clase `Sub` desciende de `Base` | `issubclass(Estudiante, Persona)` |
| 7 | `Clase.__bases__` | Tupla con las superclases directas declaradas en `Clase` | `Estudiante.__bases__` |
| 8 | `Clase.mro()` | Lista ordenada de búsqueda de clases hasta llegar a `object` | `[c.__name__ for c in Hija.mro()]` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Herencia simple y jerárquica con reutilización de `super().__init__`, extensión de métodos e introspección `isinstance`/`issubclass`.**

```python
class Persona:
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = nombre
        self.edad = edad

    def presentarse(self) -> str:
        return f"{self.nombre} ({self.edad} años)"


class Estudiante(Persona):
    def __init__(self, nombre: str, edad: int, grado: str) -> None:
        super().__init__(nombre, edad)
        self.grado = grado

    def presentarse(self) -> str:
        return f"{super().presentarse()} — Estudiante de {self.grado}"


class Docente(Persona):
    def __init__(self, nombre: str, edad: int, especialidad: str) -> None:
        super().__init__(nombre, edad)
        self.especialidad = especialidad

    def presentarse(self) -> str:
        return f"{super().presentarse()} — Docente de {self.especialidad}"


alumno = Estudiante("Flavio", 19, "3er ciclo")
profesor = Docente("Elena", 38, "Arquitectura de Software")

print(alumno.presentarse())
print(profesor.presentarse())
print("isinstance(alumno, Persona) :", isinstance(alumno, Persona))
print("type(alumno) is Persona     :", type(alumno) is Persona)
print("issubclass(Docente, object) :", issubclass(Docente, object))
print("MRO de Estudiante           :", [cls.__name__ for cls in Estudiante.mro()])
```

Explicación paso a paso:

- Integrando `Herencia.py` (L14-76) y `EJERCICIO_DOS.py` (L15-40), `Estudiante` y `Docente` reutilizan la inicialización común de `Persona` y extienden `presentarse()` apoyándose en `super().presentarse()` en lugar de duplicar el formateo de `nombre` y `edad`.
- Se verifica la diferencia esencial entre `isinstance(alumno, Persona)` (`True`, respeta la relación *es-un*) y `type(alumno) is Persona` (`False`, porque el tipo concreto es `Estudiante`).

Resultado esperado:

```text
Flavio (19 años) — Estudiante de 3er ciclo
Elena (38 años) — Docente de Arquitectura de Software
isinstance(alumno, Persona) : True
type(alumno) is Persona     : False
issubclass(Docente, object) : True
MRO de Estudiante           : ['Estudiante', 'Persona', 'object']
```

### Intermedio

**Ejemplo 2 — Herencia multinivel con plantilla de validación común en transferencias financieras.**

```python
class OperacionBancaria:
    COMISION_FIJA = 0.0

    def __init__(self, referencia: str, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto de la operación debe ser positivo")
        self.referencia = referencia
        self.monto = round(monto, 2)

    def costo_total(self) -> float:
        return round(self.monto + self.COMISION_FIJA, 2)

    def resumen(self) -> str:
        return f"[{self.referencia}] Base={self.monto:.2f} | Total={self.costo_total():.2f}"


class TransferenciaInterbancaria(OperacionBancaria):
    COMISION_FIJA = 3.50

    def __init__(self, referencia: str, monto: float, banco_destino: str) -> None:
        super().__init__(referencia, monto)
        self.banco_destino = banco_destino

    def resumen(self) -> str:
        return f"{super().resumen()} -> Destino: {self.banco_destino}"


class TransferenciaInternacionalSwift(TransferenciaInterbancaria):
    TASA_SWIFT = 0.02

    def __init__(
        self, referencia: str, monto: float, banco_destino: str, codigo_swift: str
    ) -> None:
        super().__init__(referencia, monto, banco_destino)
        self.codigo_swift = codigo_swift

    def costo_total(self) -> float:
        subtotal = super().costo_total()
        recargo_swift = self.monto * self.TASA_SWIFT
        return round(subtotal + recargo_swift, 2)

    def resumen(self) -> str:
        return f"{super().resumen()} (SWIFT: {self.codigo_swift})"


op_local = TransferenciaInterbancaria("TX-101", 200.0, "Banco Sur")
op_intl = TransferenciaInternacionalSwift("TX-202", 500.0, "EuroBank", "EUBKDEFF")

print(op_local.resumen())
print(op_intl.resumen())
print("Cadena MRO multinivel:", [c.__name__ for c in TransferenciaInternacionalSwift.mro()])
```

Explicación técnica:

- En la cadena de tres niveles (`OperacionBancaria -> TransferenciaInterbancaria -> TransferenciaInternacionalSwift`), cada eslabón añade únicamente su delta de estado y cálculo: `TransferenciaInternacionalSwift.costo_total()` invoca `super().costo_total()` (que ya suma `monto + 3.50`) y le agrega el `2%` internacional (`10.00`), totalizando `513.50`.

Resultado esperado:

```text
[TX-101] Base=200.00 | Total=203.50 -> Destino: Banco Sur
[TX-202] Base=500.00 | Total=513.50 -> Destino: EuroBank (SWIFT: EUBKDEFF)
Cadena MRO multinivel: ['TransferenciaInternacionalSwift', 'TransferenciaInterbancaria', 'OperacionBancaria', 'object']
```

### Avanzado

**Ejemplo 3 — Contraste práctico entre composición (propiedad exclusiva) y agregación (colaborador intercambiable) en un vehículo autónomo.**

```python
class UnidadTelemetriaInterna:
    """Componente poseído en composición exclusiva por cada Vehiculo."""

    def __init__(self, chasis: str) -> None:
        self.chasis = chasis
        self.eventos: list[str] = []

    def registrar(self, evento: str) -> None:
        self.eventos.append(f"{self.chasis}:{evento}")


class BateriaExtraible:
    """Colaborador independiente inyectado por agregación."""

    def __init__(self, codigo: str, carga_kwh: float) -> None:
        self.codigo = codigo
        self._carga_kwh = carga_kwh

    @property
    def carga_kwh(self) -> float:
        return self._carga_kwh

    def consumir(self, kwh: float) -> bool:
        if kwh > self._carga_kwh:
            return False
        self._carga_kwh = round(self._carga_kwh - kwh, 2)
        return True


class VehiculoElectrico:
    CONSUMO_POR_KM = 0.20

    def __init__(self, chasis: str, bateria: BateriaExtraible) -> None:
        self.posicion_km = 0.0
        # Composición: nace y muere con el vehículo
        self._telemetria = UnidadTelemetriaInterna(chasis)
        # Agregación: inyectada desde fuera e intercambiable en caliente
        self.bateria = bateria

    def recorrer(self, distancia_km: float) -> str:
        energia_requerida = round(distancia_km * self.CONSUMO_POR_KM, 2)
        if not self.bateria.consumir(energia_requerida):
            self._telemetria.registrar("ENERGIA_INSUFICIENTE")
            return f"Energía insuficiente en {self.bateria.codigo} ({self.bateria.carga_kwh} kWh)"
        self.posicion_km += distancia_km
        self._telemetria.registrar(f"AVANCE_{distancia_km}KM")
        return (
            f"Posición: {self.posicion_km} km | "
            f"Batería {self.bateria.codigo}: {self.bateria.carga_kwh} kWh"
        )

    def intercambiar_bateria(self, nueva_bateria: BateriaExtraible) -> None:
        self.bateria = nueva_bateria
        self._telemetria.registrar(f"CAMBIO_BATERIA_{nueva_bateria.codigo}")

    @property
    def bitacora(self) -> tuple[str, ...]:
        return tuple(self._telemetria.eventos)


bat_1 = BateriaExtraible("BAT-A1", carga_kwh=8.0)
bat_2 = BateriaExtraible("BAT-B2", carga_kwh=15.0)

furgon = VehiculoElectrico("VIN-900", bateria=bat_1)
print(furgon.recorrer(30.0))
print(furgon.recorrer(20.0))

# Intercambio dinámico de batería en estación sin recrear el vehículo
furgon.intercambiar_bateria(bat_2)
print(furgon.recorrer(20.0))
print("Bitácora interna:", furgon.bitacora)

# Aunque el furgón deje de referenciar bat_1, bat_1 sigue existiendo independientemente
print("Carga remanente en bat_1 independiente:", bat_1.carga_kwh, "kWh")
```

Explicación de arquitectura:

- Evolucionando `SRP.py` (L61-140) y `DIP.py` (L32-73), `VehiculoElectrico` combina ambos patrones: contiene en **composición** su `UnidadTelemetriaInterna` privada (atada al chasis del vehículo) y recibe por **agregación** una `BateriaExtraible` que puede reemplazarse en tiempo de ejecución (`intercambiar_bateria`) y continúa viva fuera del vehículo para recargarse en estación.

Resultado esperado:

```text
Posición: 30.0 km | Batería BAT-A1: 2.0 kWh
Energía insuficiente en BAT-A1 (2.0 kWh)
Posición: 50.0 km | Batería BAT-B2: 11.0 kWh
Bitácora interna: ('VIN-900:AVANCE_30.0KM', 'VIN-900:ENERGIA_INSUFICIENTE', 'VIN-900:CAMBIO_BATERIA_BAT-B2', 'VIN-900:AVANCE_20.0KM')
Carga remanente en bat_1 independiente: 2.0 kWh
```

## 6. Aplicaciones en el mundo real

- **Jerarquías de excepciones de dominio y biblioteca estándar:** como muestra `Mi_Excepcion.py` (L4) y profundiza [manejo de excepciones](../chapter-four/excepciones.md), toda excepción personalizada hereda de `Exception` para integrarse selectivamente con bloques `except`.
- **Vistas basadas en clases y modelos base en frameworks web:** en Django o SQLAlchemy, los modelos heredan de `models.Model` o `DeclarativeBase` para adquirir mapeo relacional, mientras inyectan servicios de negocio por agregación.
- **Sistemas de conectores y estrategias intercambiables:** clientes de almacenamiento, pasarelas de pago o verificadores de texto (`DIP.py` L64-73, `Con_TextBlob.py` L12-35) que reciben por constructor el adaptador concreto a utilizar según el entorno (producción, preproducción o pruebas en memoria).
- **Interfaces gráficas y árboles de componentes (UI):** widgets que especializan controles base por herencia superficial, pero ensamblan pantallas completas mediante composición de paneles, botones y diseños.

## 7. Uso en producción

- **Limitar la profundidad de las jerarquías de herencia (máximo 2 o 3 niveles):** cadenas más hondas obligan al lector a saltar entre múltiples archivos para rastrear qué atributos existen en `self` y aumentan el riesgo de colisiones de estado.
- **Aplicar la prueba estricta de sustituibilidad antes de heredar:** solo se debe heredar de `Base` cuando toda instancia de `Subclase` pueda comportarse válidamente allí donde se espere un `Base` sin lanzar errores sorpresivos ni anular garantías del padre (Principio de Sustitución de Liskov, detallado en [principios SOLID](../../Avanzado/chapter-two/principios_solid.md)).
- **No heredar de contenedores mutables nativos (`list`, `dict`) solo para reutilizar almacenamiento:** los métodos en C de `list` y `dict` no siempre invocan otros métodos Python sobrescritos (p. ej. `dict.update` puede omitir un `__setitem__` personalizado). Cuando se requiere envolver una colección, se prefiere composición (`self._datos = {}`) o `collections.UserDict` / `collections.UserList`.
- **Inyectar dependencias externas por constructor (agregación):** nunca instanciar clientes de red, relojes del sistema o bases de datos de forma rígida dentro de `__init__` (`DIP.py` L34); recibirlos como parámetros permite sustituirlos limpiamente en pruebas automatizadas.

## 8. Errores comunes y recomendaciones

1. **Olvidar llamar a `super().__init__(...)` al redefinir `__init__` en la subclase.**

```python
class DispositivoRed:
    def __init__(self, direccion_ip: str) -> None:
        self.direccion_ip = direccion_ip


class RouterWifi(DispositivoRed):
    def __init__(self, direccion_ip: str, ssid: str) -> None:
        # Error: al redefinir __init__ sin llamar a super().__init__, direccion_ip nunca se crea
        self.ssid = ssid


router = RouterWifi("192.168.1.1", "Oficina-5G")
try:
    print(router.direccion_ip)
except AttributeError as err:
    print(f"{type(err).__name__}: {err}")
```

Resultado esperado:

```text
AttributeError: 'RouterWifi' object has no attribute 'direccion_ip'
```

Diagnóstico: a diferencia de otros lenguajes que insertan automáticamente una llamada al constructor sin argumentos de la clase base, en Python redefinir `__init__` **reemplaza por completo** al `__init__` heredado. Si no se invoca explícitamente `super().__init__(...)`, los atributos de la superclase jamás se inicializan.

2. **Mezclar `super().__init__` con llamadas directas `ClasePadre.__init__(self, ...)` en diamantes de herencia (`Herencia.py` L86-93).**

```python
class PersonaBase:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre


class EmpleadoSub(PersonaBase):
    def __init__(self, nombre: str, salario: float) -> None:
        super().__init__(nombre)
        self.salario = salario


class EstudianteSub(PersonaBase):
    def __init__(self, nombre: str, carrera: str) -> None:
        super().__init__(nombre)
        self.carrera = carrera


class EstudianteTrabajadorRoto(EstudianteSub, EmpleadoSub):
    def __init__(self, nombre: str, salario: float, carrera: str) -> None:
        # Reproduce exactamente el fallo de Herencia.py L88-89:
        EstudianteSub.__init__(self, nombre, carrera)
        EmpleadoSub.__init__(self, nombre, salario)


try:
    EstudianteTrabajadorRoto("Pepe", 1500.0, "Mecatrónica")
except TypeError as err:
    print(f"{type(err).__name__}: {err}")
```

Resultado esperado:

```text
TypeError: EmpleadoSub.__init__() missing 1 required positional argument: 'salario'
```

Diagnóstico: dentro de `EstudianteSub.__init__`, `super().__init__(nombre)` avanza al siguiente elemento del MRO de `EstudianteTrabajadorRoto`, que es `EmpleadoSub` (no `PersonaBase`), pasándole únicamente `nombre` sin `salario`. Recomendación: para herencia simple basta `super().__init__(...)` uniforme; para herencia múltiple en diamante debe diseñarse inicialización cooperativa, tratada en [MRO y herencia múltiple](../../Avanzado/chapter-two/mro_herencia_multiple.md).

3. **Ignorar que `bool` hereda de `int` al validar tipos numéricos con `isinstance(x, int)`.**

```python
def duplicar_entero_ingenuo(valor: object) -> int:
    if not isinstance(valor, int):
        raise TypeError("Se esperaba un entero")
    return valor * 2


def duplicar_entero_estricto(valor: object) -> int:
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError("Se esperaba un int genuino, no un bool")
    return valor * 2


print("Ingenuo con True :", duplicar_entero_ingenuo(True))
try:
    duplicar_entero_estricto(True)
except TypeError as err:
    print("Estricto con True:", err)
```

Resultado esperado:

```text
Ingenuo con True : 2
Estricto con True: Se esperaba un int genuino, no un bool
```

Diagnóstico: dado que `issubclass(bool, int)` es `True` (`True == 1` y `False == 0`), `isinstance(True, int)` devuelve `True`. Cuando una función numérica debe rechazar valores booleanos procedentes de JSON o formularios, debe descartar `isinstance(valor, bool)` en primer lugar.

## 9. Resumen

- En Python 3 todas las clases heredan implícitamente de `object`; la herencia modela relaciones taxonómicas **"es-un"** (*is-a*) en esquemas simples, jerárquicos o multinivel.
- Redefinir un método en la subclase permite reemplazar o extender el comportamiento base; usar **`super().__init__(...)`** y **`super().metodo(...)`** reutiliza limpiamente la lógica superior siguiendo el MRO sin acoplarse a nombres literales de clases padre.
- Las funciones integradas **`isinstance()`** e **`issubclass()`** verifican pertenencia respetando toda la cadena de herencia (recordando que `bool` es subclase de `int`).
- Las relaciones **"tiene-un"** (*has-a*) se dividen en **composición** (el contenedor crea y posee en exclusiva el ciclo de vida de la parte) y **agregación** (el colaborador se inyecta desde fuera con ciclo de vida independiente).
- En arquitecturas de producción se prioriza la **composición y agregación sobre la herencia profunda** para reducir el acoplamiento, intercambiar colaboradores dinámicamente y facilitar pruebas unitarias aisladas.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/CLASE_SEGUNDA/Herencia.py` (L1-105) | `Herencia.py` | Superclase `Persona`, herencia jerárquica en `Empleado(Persona)` y `Estudiante(Persona)` con `super().__init__`, y clase `Estudiante_Trabajador` (L86-93) | Se diagnosticó el `TypeError` real que ocurre en L93 al mezclar `super().__init__` con `Estudiante.__init__(self, ...)` y se enlazó su solución con MRO |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/EJERCICIOS/EJERCICIO_DOS.py` (L1-40) | `EJERCICIO_DOS.py` | Extensión de estado y de método mediante `super().__init__` y `super().Presentarse()`, llamada `Persona.Presentarse(user_one)` y `Estudiante.mro()` | Se formalizó la diferencia entre sobrescritura total y extensión cooperativa con `super()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_TWO/EJERCICIOS/EJERCICIO_DOS_TWO.py` (L1-39) | `EJERCICIO_DOS_TWO.py` | Jerarquía `Animal` -> `Mamifero`, `Ave` -> `Murcielago(Mamifero, Ave)` e inspección con `Murcielago.mro()` | Se contextualizó dentro de la taxonomía de tipos de herencia conectándolo con el estudio dedicado a linealización C3 y MRO |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Usar_Herencia.py` (L1-29) | `Usar_Herencia.py` | `Animal` y `Perro(Animal)` heredando `comer()` intacto y sobrescribiendo `sonido()` | Se integró con la verificación en tiempo de ejecución mediante `isinstance()` frente a `type()` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_FOUR/CLASE_CUARTA/EXCEPCIONES/Mi_Excepcion.py` (L1-16) | `Mi_Excepcion.py` | Especialización `class MiExcepcion(Exception):` sobre la jerarquía nativa de errores | Se conectó con la herencia multinivel de excepciones de dominio |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/CLASE_CUARTA/SRP.py` (L60-140) | `SRP.py` | Refactorización de `Auto` recibiendo una instancia externa `TanqueDeCombustible` (`Auto(tanque)`) | Se clasificó formalmente como **agregación** (*tiene-un* con ciclo de vida independiente) |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/CLASE_CUARTA/DIP.py` (L26-73) | `DIP.py` | Paso de instanciación interna rígida `self.diccionario = Diccionario()` (L34) a inyección externa `CorrectorOrtografico(verificador)` (L65) | Se utilizó para contrastar rigurosamente **composición** frente a **agregación** e inversión de dependencias |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_FOUR/EJERCICIO_FINAL/Con_TextBlob.py` (L3-36) | `Con_TextBlob.py` | `AnalizadorDeSentimientos(rangos)` recibiendo objetos `Sentimiento` asociados a intervalos | Se destacó como ejemplo práctico de agregación de objetos de valor configurables desde el exterior |

**Fundamento complementario:** se incorporaron cuatro pilares arquitectónicos esenciales: (1) la herencia implícita universal desde `object` en Python 3; (2) el contraste formal entre **composición** (posesión exclusiva de ciclo de vida) y **agregación** (colaboración independiente) junto al principio *"favorecer composición sobre herencia"*; (3) la semántica exacta de `isinstance()` e `issubclass()`, incluyendo el caso borde `issubclass(bool, int)`; y (4) las precauciones al subclasificar tipos mutables en C como `dict` o `list`.

## 11. Referencias oficiales

- <https://docs.python.org/3/tutorial/classes.html#inheritance> — Tutorial oficial de Python (*Inheritance*): sintaxis de clases derivadas, resolución de atributos, sobrescritura e introspección con `isinstance` e `issubclass`.
- <https://docs.python.org/3/library/functions.html#super> — Biblioteca estándar (`super`): funcionamiento del objeto *proxy* de delegación y relación con el MRO.
- <https://docs.python.org/3/library/functions.html#isinstance> — Biblioteca estándar (`isinstance` e `issubclass`): evaluación de pertenencia jerárquica y tuplas de clases.
- <https://docs.python.org/3/library/collections.html#collections.UserDict> — Biblioteca estándar (`UserDict` / `UserList`): envoltorios diseñados para subclasificación segura frente a tipos nativos en C.
