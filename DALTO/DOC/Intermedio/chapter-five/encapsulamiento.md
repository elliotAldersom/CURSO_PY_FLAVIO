# Encapsulamiento, Convenciones de Visibilidad, *Name Mangling* y `@property`

## 2. Introducción

Cuando cualquier módulo externo puede alterar libremente los [atributos](atributos_y_metodos.md) internos de un [objeto](clases_y_objetos.md) —por ejemplo, asignando un saldo bancario negativo, vaciando directamente la lista subyacente de una pila (`Keyword_del.py` L28) o desincronizando dos campos dependientes—, la clase pierde la capacidad de garantizar la validez de su propio estado.

El **encapsulamiento** agrupa los datos junto con las operaciones que los gobiernan y establece una frontera clara entre la **interfaz pública estable** de una clase y sus **detalles internos de implementación** (`Encapsulamiento.py` L1-8). En Python, este pilar adopta un diseño idiomático propio que conviene dominar por cuatro motivos arquitectónicos:

1. **Protección de invariantes de dominio:** asegura que un objeto sea válido desde su inicialización en `__init__` y tras cada transición de estado posterior.
2. **Desacoplamiento evolutivo, no seguridad criptográfica:** permite cambiar la representación interna de una clase sin romper el código cliente que la consume.
3. **Comprensión exacta de `_atributo` frente a `__atributo`:** distingue la convención contractual protegida de **PEP 8** respecto de la transformación léxica (*name mangling*), evitando falsas expectativas de privacidad absoluta.
4. **Evolución transparente mediante `@property`:** sustituye los métodos verbosos `get_x()`/`set_x()` propios de otros lenguajes (`Encapsulamiento.py` L98-183) por descriptores que validan, calculan o protegen lecturas manteniendo intacta la sintaxis natural de acceso por punto.

## 3. Fundamentos y conceptos

**Encapsulamiento como contrato arquitectónico frente a control de acceso de seguridad.** Un malentendido frecuente consiste en equiparar el encapsulamiento con seguridad informática o cifrado de datos (`Clase_One_2.py` L12, L15). Ningún modificador de visibilidad —ni siquiera `private` en C++ o Java, salvable mediante reflexión, y mucho menos los guiones bajos en Python— protege secretos frente a código que corre dentro del mismo proceso de memoria. El propósito real del encapsulamiento es **arquitectónico**: reducir el acoplamiento entre módulos e impedir que consumidores externos dependan de estructuras internas volátiles o violen las reglas de consistencia (**invariantes**) de la entidad.

**La filosofía de "adultos responsables" (*consenting adults*) y los tres niveles de nombres en Python.** Python prescinde de palabras reservadas como `public`, `protected` o `private` y articula la visibilidad mediante tres convenciones léxicas documentadas en **PEP 8** (`Encapsulamiento.py` L18-64):

| Nivel en Python | Sintaxis | Comportamiento del intérprete | Propósito de diseño (**PEP 8**) |
|---|---|---|---|
| **Público** | `saldo`, `depositar()` | Acceso directo sin transformación | Contrato público estable garantizado para cualquier consumidor externo |
| **No público (protegido por convención)** | `_saldo`, `_recalcular()` | Sin restricción en ejecución (omitido en `from mod import *` a nivel de módulo) | Detalle interno de implementación; subclases pueden usarlo con cautela, clientes externos no deben tocarlo |
| **Desfigurado (*name mangling*)** | `__saldo`, `__auditar()` | Reescrito en compilación a `_NombreClase__identificador` | Evitar colisiones accidentales de nombres internos en jerarquías de [herencia](herencia.md) |

**Mecánica real del *name mangling* (`__identificador`).** Cuando el compilador de Python encuentra dentro del cuerpo de una clase `ClaseBase` cualquier identificador que comience con **al menos dos guiones bajos** y termine con **a lo sumo un guion bajo** (excluyendo así los [métodos especiales](../../Avanzado/chapter-one/metodos_especiales.md) como `__init__` o `__str__`), transforma automáticamente el nombre anteponiendo `_ClaseBase`:

- En `Keyword_del.py` (L9, L28), `self.__stack_list` se almacena realmente en `stack_object.__dict__` bajo la clave `'_Stack__stack_list'`.
- En `Encapsulamiento.py` (L39-51) y `REPASOS/Encapsulamiento.py` (L3-19), `self.__atributo_privado` y `def __hablar(self)` pasan a llamarse `_MiClase__atributo_privado` y `_MiClase__hablar`.

Esta transformación **no existe para crear "atributos muy privados" inaccesibles**, sino para resolver un problema concreto de herencia: si `ClaseBase` usa internamente `self.__cache` y una subclase escrita por otro equipo define también su propio `self.__cache` sin conocer los detalles internos del padre, el *name mangling* los separa en `_ClaseBase__cache` y `_Subclase__cache`, impidiendo que uno sobrescriba accidentalmente al otro. Para atributos internos ordinarios, **PEP 8** recomienda preferir **un solo guion bajo (`_nombre`)**, ya que el doble guion bajo entorpece innecesariamente la extensión legítima en subclases, la introspección y las pruebas unitarias.

**Por qué los métodos `get_x()` y `set_x()` al estilo Java no son idiomáticos en Python.** En `Encapsulamiento.py` (L98-183) y `REPASOS/Encapsulamiento.py` (L28-46) se escriben pares `get_nombre()` / `set_nombre()` y `get_edad()` / `set_edad()`. En lenguajes estáticos tradicionales esa práctica preventiva es obligatoria porque exponer un campo público `persona.edad` impide añadir validación en el futuro sin cambiar todas las llamadas existentes a `persona.getEdad()` y `persona.setEdad(...)`. En Python, escribir *getters* y *setters* manuales degrada la expresividad (`cuenta.set_saldo(cuenta.get_saldo() + 50)` frente a `cuenta.saldo += 50`) y resulta innecesario gracias al descriptor `@property`.

**Propiedades Pythonicas con `@property`, `@x.setter` y `@x.deleter`.** El [decorador](../../Avanzado/chapter-one/decoradores.md) integrado `@property` (`Decoradores_@Property.py` L32-82, `Decorador_Property.py` L6-65) convierte métodos en **descriptores de datos** que interceptan la lectura, asignación y borrado de un atributo conservando intacta la sintaxis de acceso por punto:

```text
Acceso cliente              Método interceptado en la clase
─────────────────────       ──────────────────────────────────────────
valor = obj.edad       ──►  @property        def edad(self) -> int
obj.edad = 25          ──►  @edad.setter     def edad(self, valor: int) -> None
del obj.edad           ──►  @edad.deleter    def edad(self) -> None
```

Este diseño aporta cuatro ventajas decisivas en ingeniería de software:

1. **Migración transparente sin ruptura de compatibilidad:** una clase comienza exponiendo un atributo público sencillo (`self.edad = edad`). Si meses después surge el requisito de validar que `edad >= 0`, se reemplaza por `@property` y `@edad.setter` respaldados por `self._edad`, **sin modificar ni una sola línea del código cliente existente**.
2. **Validación unificada desde `__init__`:** a diferencia de `Decorador_Property.py` (L2-4), donde `__init__` asigna directamente `self.__nombre = name` y `self.__edad = age` saltándose por completo las validaciones del *setter* (permitiendo crear `Person(12345, -90)`), asignar **`self.edad = edad` dentro de `__init__`** canaliza también la construcción inicial a través de `@edad.setter`, garantizando el invariante en todo momento.
3. **Propiedades de solo lectura y atributos calculados (*computed properties*):** declarar únicamente `@property` (omitiendo `@x.setter`, como `Mostrar_Estado` en `Abastraccion.py` L13-15) bloquea automáticamente cualquier intento de escritura externa con `AttributeError`, resultando ideal para métricas derivadas al vuelo (`subtotal`, `impuesto`, `esta_vencido`) que nunca quedan desactualizadas.
4. **Señalización rigurosa mediante excepciones, no `print()` ni `input()`:** en `Decorador_Property.py` (L35-65), `@Datos.setter` imprime mensajes en consola cuando el dato es inválido (dejando que el programa continúe silenciosamente creyendo que la asignación tuvo éxito) y `@Datos.deleter` bloquea la ejecución con `input()`. En código profesional, un *setter* rechaza entradas inválidas lanzando [excepciones](../chapter-four/excepciones.md) (`TypeError` o `ValueError`), y `@x.deleter` se aplica sobre la misma propiedad (evitando crear propiedades ficticias vacías como `Borrar_Datos` en `Decoradores_@Property.py` L53-62) para limpiar cachés o restablecer estados opcionales sin interacción de consola.

## 4. Sintaxis y funcionamiento

Patrón canónico de propiedad validada con atributo de respaldo `_atributo` y propiedad calculada de solo lectura:

```text
class Cuenta:
    def __init__(self, titular: str, saldo_inicial: float) -> None:
        self.titular = titular          # Público directo (sin reglas especiales)
        self.saldo = saldo_inicial      # Invoca automáticamente @saldo.setter

    @property
    def saldo(self) -> float:
        return self._saldo              # Lee el atributo interno de respaldo

    @saldo.setter
    def saldo(self, nuevo_saldo: float) -> None:
        if nuevo_saldo < 0:
            raise ValueError("El saldo no puede ser negativo")
        self._saldo = float(nuevo_saldo)

    @property
    def tiene_fondos(self) -> bool:     # Solo lectura (sin @tiene_fondos.setter)
        return self._saldo > 0.0
```

Referencia de convenciones y elementos de encapsulamiento en Python:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `self.publico` | Atributo parte de la interfaz pública documentada | `self.moneda = "PEN"` |
| 2 | `self._interno` | Convención **PEP 8** de atributo protegido/interno de la clase | `self._saldo = 0.0` |
| 3 | `self.__colision` | *Name mangling*: renombrado internamente a `_Clase__colision` | `self.__token_local = x` |
| 4 | `@property` | Define el descriptor de lectura (`getter`) accedido sin paréntesis | `@property def saldo(self):` |
| 5 | `@prop.setter` | Define la validación/asignación al ejecutar `obj.prop = valor` | `@saldo.setter def saldo(self, v):` |
| 6 | `@prop.deleter` | Define la acción ejecutada ante la sentencia `del obj.prop` | `@cache.deleter def cache(self):` |
| 7 | Propiedad sin *setter* | Atributo de solo lectura o calculado dinámicamente | `@property def area(self):` |
| 8 | `self.prop = v` en `__init__` | Reutiliza la lógica de validación de `@prop.setter` al instanciar | `self.edad = edad_inicial` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Convención protegida (`_`), inspección real del *name mangling* (`__`) y encapsulamiento de operaciones en una pila LIFO.**

```python
class PilaAcotada:
    """Estructura LIFO que protege su capacidad máxima e invariantes."""

    def __init__(self, capacidad: int) -> None:
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")
        self._capacidad = capacidad
        self.__elementos: list[int] = []

    def apilar(self, valor: int) -> None:
        if len(self.__elementos) >= self._capacidad:
            raise OverflowError("La pila alcanzó su capacidad máxima")
        self.__elementos.append(valor)

    def desapilar(self) -> int:
        if not self.__elementos:
            raise IndexError("No se puede desapilar de una pila vacía")
        return self.__elementos.pop()

    def tamano(self) -> int:
        return len(self.__elementos)


pila = PilaAcotada(capacidad=2)
pila.apilar(10)
pila.apilar(20)

print("Claves reales en pila.__dict__:", list(pila.__dict__.keys()))
print("¿Existe atributo literal '__elementos'?:", hasattr(pila, "__elementos"))
print("Tamaño actual:", pila.tamano(), "| Desapilado:", pila.desapilar())
```

Explicación paso a paso:

- Evolucionando la clase `Stack` de `Keyword_del.py` (L7-34) y `Encapsulamiento.py` (L36-52), se comprueba que `self._capacidad` conserva su nombre intacto en `__dict__`, mientras que `self.__elementos` fue renombrado por el compilador a `'_PilaAcotada__elementos'` (`hasattr(pila, "__elementos")` es `False`).
- Los métodos públicos `apilar`, `desapilar` y `tamano` protegen el invariante `0 <= len <= capacidad` lanzando excepciones estándar (`OverflowError`, `IndexError`) ante operaciones ilegales.

Resultado esperado:

```text
Claves reales en pila.__dict__: ['_capacidad', '_PilaAcotada__elementos']
¿Existe atributo literal '__elementos'?: False
Tamaño actual: 2 | Desapilado: 20
```

### Intermedio

**Ejemplo 2 — Propiedades validadas desde `__init__`, propiedades calculadas de solo lectura y limpieza controlada con `@deleter`.**

```python
class ProductoCatalogo:
    def __init__(self, nombre: str, precio_base: float, descuento: float = 0.0) -> None:
        self.nombre = nombre            # Pasa por @nombre.setter
        self.precio_base = precio_base  # Pasa por @precio_base.setter
        self.descuento = descuento      # Pasa por @descuento.setter
        self._nota_interna: str | None = "Revisión inicial aprobada"

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        limpio = valor.strip()
        if len(limpio) < 2:
            raise ValueError("El nombre del producto requiere al menos 2 caracteres")
        self._nombre = limpio

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El precio base debe ser estrictamente positivo")
        self._precio_base = round(float(valor), 2)

    @property
    def descuento(self) -> float:
        return self._descuento

    @descuento.setter
    def descuento(self, valor: float) -> None:
        if not (0.0 <= valor <= 0.80):
            raise ValueError("El descuento debe estar en el rango [0.0, 0.80]")
        self._descuento = float(valor)

    @property
    def precio_final(self) -> float:
        """Propiedad calculada de solo lectura: siempre consistente."""
        return round(self._precio_base * (1.0 - self._descuento), 2)

    @property
    def nota_interna(self) -> str:
        return self._nota_interna if self._nota_interna is not None else "(sin nota)"

    @nota_interna.deleter
    def nota_interna(self) -> None:
        self._nota_interna = None


monitor = ProductoCatalogo("  Monitor 27 UHD  ", precio_base=1200.0, descuento=0.15)
print(f"{monitor.nombre} -> Base: {monitor.precio_base} | Final: {monitor.precio_final}")

monitor.descuento = 0.25
print("Final tras nuevo descuento:", monitor.precio_final)

try:
    monitor.precio_final = 500.0
except AttributeError as err:
    print("Escritura bloqueada en solo lectura:", type(err).__name__)

del monitor.nota_interna
print("Estado tras del monitor.nota_interna:", monitor.nota_interna)
```

Explicación técnica:

- Se refinan `Decoradores_@Property.py` (L32-82) y `Decorador_Property.py` (L1-86): `__init__` asigna sobre las propiedades (`self.nombre = nombre`) activando las validaciones desde el nacimiento del objeto; `precio_final` calcula el importe en tiempo real e impide sobrescrituras directas; y `@nota_interna.deleter` restablece limpiamente el estado a `None` en lugar de eliminar el atributo dejando el objeto roto ante futuras lecturas.

Resultado esperado:

```text
Monitor 27 UHD -> Base: 1200.0 | Final: 1020.0
Final tras nuevo descuento: 900.0
Escritura bloqueada en solo lectura: AttributeError
Estado tras del monitor.nota_interna: (sin nota)
```

### Avanzado

**Ejemplo 3 — Prevención real de colisiones en subclases mediante *name mangling* y caché perezosa (*lazy caching*) invalidada por `@setter` / `@deleter`.**

```python
class MotorBase:
    def __init__(self) -> None:
        # __registro se convierte en _MotorBase__registro (protegido frente a subclases)
        self.__registro = "estado-interno-motor-base"

    def leer_estado_base(self) -> str:
        return self.__registro


class MotorAnalitico(MotorBase):
    def __init__(self, muestras: list[float]) -> None:
        super().__init__()
        # __registro aquí se convierte en _MotorAnalitico__registro (no pisa al padre)
        self.__registro = "estado-interno-subclase"
        self.muestras = muestras

    @property
    def muestras(self) -> tuple[float, ...]:
        # Retorna tupla inmutable para evitar mutación externa por referencia
        return tuple(self._muestras)

    @muestras.setter
    def muestras(self, nuevas: list[float]) -> None:
        if not nuevas:
            raise ValueError("Se requiere al menos una muestra")
        self._muestras = [float(x) for x in nuevas]
        self._promedio_cache: float | None = None
        self._calculos_ejecutados = getattr(self, "_calculos_ejecutados", 0)

    @property
    def promedio(self) -> float:
        if self._promedio_cache is None:
            self._calculos_ejecutados += 1
            self._promedio_cache = sum(self._muestras) / len(self._muestras)
        return self._promedio_cache

    @promedio.deleter
    def promedio(self) -> None:
        self._promedio_cache = None

    def leer_estado_subclase(self) -> str:
        return self.__registro


motor = MotorAnalitico([10.0, 20.0, 30.0])
print("Padre intacto   :", motor.leer_estado_base())
print("Subclase propia :", motor.leer_estado_subclase())
print("Promedio (1ª vez):", motor.promedio, "| Cálculos:", motor._calculos_ejecutados)
print("Promedio (caché) :", motor.promedio, "| Cálculos:", motor._calculos_ejecutados)

motor.muestras = [50.0, 70.0]
print("Promedio tras actualizar muestras:", motor.promedio, "| Cálculos:", motor._calculos_ejecutados)
```

Explicación de arquitectura:

- Se demuestra el **verdadero caso de uso del doble guion bajo**: tanto `MotorBase` como `MotorAnalitico` declaran `self.__registro`, pero coexisten sin colisión como `_MotorBase__registro` y `_MotorAnalitico__registro`.
- Además, se cierra una fuga clásica de encapsulamiento: si `@property def muestras` devolviera directamente la lista interna `self._muestras`, un cliente podría ejecutar `motor.muestras.append(999)` eludiendo el *setter* y dejando obsoleto `_promedio_cache`. Retornar una copia inmutable `tuple(self._muestras)` blinda el estado interno.

Resultado esperado:

```text
Padre intacto   : estado-interno-motor-base
Subclase propia : estado-interno-subclase
Promedio (1ª vez): 20.0 | Cálculos: 1
Promedio (caché) : 20.0 | Cálculos: 1
Promedio tras actualizar muestras: 60.0 | Cálculos: 2
```

## 6. Aplicaciones en el mundo real

- **Modelos financieros y contables:** cuentas, carteras y órdenes de compra exponen saldos de solo lectura que únicamente pueden variar mediante métodos transaccionales auditados (`acreditar()`, `debitar()`), impidiendo asignaciones arbitrarias.
- **Configuración de clientes SDK y conexiones:** propiedades que normalizan URLs, validan rangos de *timeouts* y reconstruyen automáticamente cabeceras de autenticación cuando se rota un *token*.
- **Cálculo diferido (*lazy evaluation*) con caché transparente:** modelos científicos o de procesamiento de documentos que postergan un cálculo costoso hasta la primera lectura de `documento.resumen` y reutilizan el resultado en lecturas sucesivas.
- **Evolución de bibliotecas públicas sin romper versiones (*backward compatibility*):** transformación de antiguos atributos obsoletos en `@property` que emiten un `DeprecationWarning` y redirigen internamente al nuevo esquema de datos.

## 7. Uso en producción

- **Empezar con atributos públicos simples; introducir `@property` solo cuando exista lógica real:** en Python nunca se escriben `@property` y `@setter` triviales que únicamente leen y asignan `self._x = x` sin validación ni transformación (`Decoradores_@Property.py` L37-51). Ese código repetitivo añade sobrecarga de llamada a función sin aportar valor, dado que `@property` puede añadirse en el futuro sin romper a los clientes.
- **Evitar cálculos costosos o llamadas de red ocultas detrás de `@property`:** dado que `obj.atributo` parece sintácticamente una lectura barata en memoria, una propiedad nunca debe disparar consultas SQL pesadas, peticiones HTTP ni operaciones de disco inesperadas; esas acciones deben exponerse como métodos explícitos con verbo (`cargar_historial()`, `sincronizar_remoto()`).
- **Proteger colecciones internas contra mutación por alias (*defensive copying*):** cuando una propiedad expone una colección interna, debe retornar una vista inmutable (`tuple`, `frozenset`, `MappingProxyType`) o una copia superficial para impedir que el llamador mute el contenedor a espaldas de la clase.
- **Preferir `_atributo` sobre `__atributo` como estándar cotidiano:** reservar `__atributo` estrictamente para clases base o *mixins* destinados a ser heredados por terceros donde las colisiones accidentales de nombres sean un riesgo real.

## 8. Errores comunes y recomendaciones

1. **Provocar recursión infinita (`RecursionError`) al asignar sobre el mismo nombre de la propiedad dentro de su `@setter` o `@property`.**

```python
class TermostatoRecursivo:
    def __init__(self, grados: float) -> None:
        self.grados = grados

    @property
    def grados(self) -> float:
        return self.grados  # Error: vuelve a invocar @property grados indefinidamente

    @grados.setter
    def grados(self, valor: float) -> None:
        self.grados = valor  # Error: vuelve a invocar @grados.setter indefinidamente


try:
    TermostatoRecursivo(22.0)
except RecursionError as err:
    print(f"{type(err).__name__}: recursión infinita detectada en setter")
```

Resultado esperado:

```text
RecursionError: recursión infinita detectada en setter
```

Diagnóstico: el nombre público de la propiedad (`grados`) pertenece al descriptor alojado en la clase; dentro del *getter* y del *setter* debe emplearse obligatoriamente un atributo de respaldo con nombre distinto (`self._grados`).

2. **Retornar la referencia directa a una lista mutable interna desde `@property`.**

```python
class PermisosUsuario:
    def __init__(self) -> None:
        self._roles: list[str] = ["lector"]

    @property
    def roles_inseguros(self) -> list[str]:
        return self._roles  # Fuga de referencia mutable

    @property
    def roles_seguros(self) -> tuple[str, ...]:
        return tuple(self._roles)


u = PermisosUsuario()
u.roles_inseguros.append("administrador_total")  # Muta el estado interno sin pasar por validación
print("Estado vulnerado por alias mutable:", u.roles_seguros)
```

Resultado esperado:

```text
Estado vulnerado por alias mutable: ('lector', 'administrador_total')
```

Diagnóstico: aunque no exista `@roles_inseguros.setter`, devolver el objeto `list` interno entrega al exterior una referencia con capacidad de mutación *in situ* (`.append()`, `.clear()`). Recomendación: devolver una `tuple` inmutable y ofrecer métodos de dominio validados (`asignar_rol(rol)`).

3. **Imprimir advertencias con `print()` en un `@setter` en lugar de lanzar excepciones, o omitir el `@setter` en `__init__`.**

```python
# ERROR INTENCIONAL: antipatrón de validación silenciosa (Decorador_Property.py L2-4, L35-52)
class UsuarioSilencioso:
    def __init__(self, edad: int) -> None:
        self.__edad = edad  # Omite el setter: acepta UsuarioSilencioso(-50)

    @property
    def edad(self) -> int:
        return self.__edad

    @edad.setter
    def edad(self, valor: int) -> None:
        if valor < 0:
            print("Edad inválida")  # El llamador programático nunca detecta el fallo
        else:
            self.__edad = valor
```

Diagnóstico: en un servicio automatizado nadie lee mensajes sueltos en `stdout`; si una asignación viola una regla de negocio, debe interrumpir el flujo lanzando `ValueError` o `TypeError`, e `__init__` debe invocar `self.edad = edad` para aplicar exactamente el mismo filtro.

## 9. Resumen

- El **encapsulamiento** resguarda los invariantes de dominio y desacopla la interfaz pública de una clase respecto de su representación interna; no constituye un mecanismo criptográfico de seguridad.
- Python articula la visibilidad mediante tres niveles: **público** (`nombre`), **no público / protegido por convención PEP 8** (`_nombre`) y **desfiguración de nombres o *name mangling*** (`__nombre` -> `_Clase__nombre`), diseñado específicamente para evitar colisiones accidentales en subclases.
- Escribir métodos `get_x()` y `set_x()` explícitos resulta ajeno al diseño idiomático de Python porque rompe la compatibilidad con el acceso natural a atributos.
- Los descriptores **`@property`**, **`@x.setter`** y **`@x.deleter`** permiten incorporar validaciones, propiedades calculadas de solo lectura y gestión de caché de forma transparente, almacenando el valor subyacente en `self._x` para evitar `RecursionError`.
- Para blindar completamente una entidad, `__init__` debe asignar a través de las propiedades validadas y los *getters* nunca deben exponer referencias crudas a colecciones mutables internas.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/Keyword_del.py` (L7-34) | `Keyword_del.py` | Atributo `self.__stack_list = []` en `class Stack`, operaciones `push`/`pop` y acceso externo `stack_object._Stack__stack_list` (L28) | Se explicó por qué el acceso por nombre desfigurado rompe el encapsulamiento y cómo validar desbordamientos y pila vacía |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Encapsulamiento.py` (L1-195) | `Encapsulamiento.py` | Niveles `_atributo_privado` y `__atributo_privado`, método `__hablar` y definición de `get_nombre`/`set_nombre` | Se corrigió la noción de "muy muy privado", precisando el propósito real del *name mangling* frente a colisiones en herencia y por qué se prefiere `@property` sobre `get_`/`set_` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Decoradores_@Property.py` (L1-84) | `Decoradores_@Property.py` | Uso de `@property`, `@nombre.setter`, `@edad.setter` y `@Borrar_Datos.deleter` | Se explicó por qué no deben escribirse propiedades triviales sin lógica y cómo asociar `@deleter` a la misma propiedad en lugar de crear `Borrar_Datos` vacío |
| `CLASS_PY_POO/` | `CLASS_PY_POO/CLASE_THREE/Clase_Tercera/Abastraccion.py` (L9-40) | `Abastraccion.py` | Estado interno `self.__estado = "apagado"` expuesto en modo lectura mediante `@property def Mostrar_Estado(self):` | Se formalizó el patrón de propiedades de solo lectura y atributos calculados sin *setter* |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Encapsulamiento.py` (L1-46) | `Encapsulamiento.py` | Métodos `get_presentar_name`, `get_presentar_age` y `set_cambiar_age` con impresiones laterales | Se desacopló la mutación de estado respecto de `print()` |
| `CLASS_PY_POO/` | `CLASS_PY_POO/REPASOS/Decorador_Property.py` (L1-86) | `Decorador_Property.py` | Propiedad compuesta `Datos` (evitando exponer `_Person__nombre` de `__dict__`), validación en `@Datos.setter` y `del xd.Datos` | Se sustituyeron los `print()` en `@Datos.setter` e `input()` en `@Datos.deleter` por excepciones de dominio y limpieza determinista, canalizando `__init__` por los *setters* |

**Fundamento complementario:** se añadieron cuatro conceptos esenciales de ingeniería en Python: (1) la distinción conceptual entre ocultamiento de información arquitectónico y control de acceso de seguridad; (2) el origen de `RecursionError` al omitir el prefijo `_` en el atributo de respaldo dentro de `@property`/`@setter`; (3) la protección frente a fugas de alias mutables retornando tuplas inmutables; y (4) la invalidación transparente de cachés perezosas mediante descriptores.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/functions.html#property> — Biblioteca estándar (`property`): firma completa, decoradores `@property`, `.setter` y `.deleter`, y propiedades de solo lectura.
- <https://docs.python.org/3/tutorial/classes.html#private-variables> — Tutorial oficial de Python (*Private Variables*): convención `_spam`, reglas exactas de *name mangling* (`__spam` -> `_ClassName__spam`) y prevención de colisiones en subclases.
- <https://docs.python.org/3/reference/expressions.html#atom-identifiers> — Referencia del lenguaje (*Private name mangling*): especificación léxica de transformación en tiempo de compilación.
- <https://peps.python.org/pep-0008/#designing-for-inheritance> — PEP 8 (*Designing for Inheritance*): guía oficial sobre atributos públicos frente a no públicos (`_` vs `__`) y filosofía Pythonica frente a *getters*/*setters* innecesarios.
