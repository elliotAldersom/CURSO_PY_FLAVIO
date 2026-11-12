# Aritmética Decimal Exacta, Contextos de Precisión y Redondeo Financiero (`decimal`)

## 2. Introducción

En la mayoría de lenguajes de programación, el tipo numérico de coma flotante predeterminado (`float` en Python, estudiado en [tipos de datos](../../Basico/chapter-one/tipos_datos.md)) implementa el estándar de hardware **IEEE 754 de doble precisión en base 2** (*binary64*). Aunque ese diseño ofrece velocidad extraordinaria para cálculo físico, gráfico o estadístico, tiene una consecuencia matemática ineludible: fracciones cotidianas en base 10 como $0.1$, $0.2$ o $2.675$ carecen de representación finita en binario, produciendo resultados como `0.1 + 0.2 == 0.30000000000000004` o redondeos inesperados como `round(2.675, 2) == 2.67` (`redondeo.py` L3-7).

En contabilidad, facturación electrónica, banca, liquidación de impuestos y pasarelas de pago, acumular discrepancias de millonésimas o perder un céntimo entre el subtotal y las cuotas resulta inaceptable. Para resolverlo sin bibliotecas de terceros, la **biblioteca estándar de Python** incluye el [módulo](../chapter-three/modulos.md) `decimal`, implementación fiel de la especificación *General Decimal Arithmetic* de IBM (alineada con IEEE 754-2008 en base 10).

Sus ventajas centrales frente a `float` son cuatro:

1. **Representación exacta en base 10:** todo número escrito por personas en texto decimal (`Decimal("0.10")`) se almacena sin error de conversión binaria.
2. **Conservación de ceros finales significativos:** `Decimal("15.00")` distingue explícitamente una magnitud medida al céntimo (exponente `-2`) frente a `Decimal("15.0")` (exponente `-1`).
3. **Precisión configurable y aislada:** permite ajustar el número de cifras significativas desde unas pocas hasta cientos de dígitos dentro de bloques acotados (`localcontext()`).
4. **Ocho modos deterministas de redondeo y señales auditables:** permite elegir entre redondeo bancario (`ROUND_HALF_EVEN`), comercial (`ROUND_HALF_UP`, utilizado en `numero_decimal.py` L1 y `calculadora_simple.py` L1) o truncado, detectando operaciones inválidas mediante [excepciones](excepciones.md) dedicadas.

## 3. Fundamentos y conceptos

**Por qué `float` binario difiere de la aritmética humana en base 10.** Un `float` de 64 bits almacena un signo, 53 bits de mantisa significativa y un exponente en potencias de $2$. Así como $\frac{1}{3} = 0.3333\ldots_{10}$ es periódico infinito en base 10, la fracción $\frac{1}{10} = \frac{1}{2 \times 5}$ es periódica infinita en base 2 porque su denominador contiene el factor primo $5$:

$$\frac{1}{10} = 0.00011001100110011\ldots_2$$

Al truncar esa secuencia a 53 bits, el literal `0.1` en Python almacena en realidad el valor exacto:

`0.1000000000000000055511151231257827021181583404541015625`

Lo mismo explica el caso clásico de `redondeo.py` (L3-7): el literal `float` `2.675` se guarda internamente como `2.674999999999999822364316...`, ligeramente **menor** que el punto medio exacto $2.675$, por lo que `round(2.675, 2)` redondea hacia abajo a `2.67`. En cambio, la clase `Decimal` representa cada número mediante una terna exacta $(\text{signo}, \text{dígitos en base } 10, \text{exponente en base } 10)$, de modo que `Decimal("2.675")` equivale exactamente a $2675 \times 10^{-3}$.

**Regla fundamental de construcción: `str` o `int`, nunca `float` binario.** El origen del dato pasado al constructor `Decimal(...)` determina si se conserva o se pierde la exactitud:

- **Correcto:** construir desde `str` (`Decimal("0.10")`, `Decimal("19.99")`), desde `int` (`Decimal(100)`) o desde una tupla estructural (`Decimal((0, (2, 6, 7, 5), -3))`). Cuando el dato proviene de regiones donde el separador decimal es la coma (`"12,50"`), debe normalizarse previamente a punto (`texto.strip().replace(",", ".")`, como en `Ejm_Operadores_Aritméticos.py` L6-7) antes de invocar `Decimal(...)`.
- **Incorrecto:** escribir `Decimal(0.1)` pasando un literal `float`. Antes incluso de ejecutarse `Decimal(...)`, Python ya habrá evaluado `0.1` como `float` binario inexacto, y `Decimal` copiará fielmente sus 55 dígitos contaminados.

**Incompatibilidad deliberada entre `Decimal` y `float` (`TypeError`).** Python permite operar directamente `Decimal` con enteros `int` (`Decimal("19.99") * 3` produce `Decimal("59.97")`), pero prohíbe mezclar `Decimal` y `float` en [operadores](../../Basico/chapter-one/operadores.md) aritméticos (`+`, `-`, `*`, `/`, `**`), lanzando `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'`. Esta barrera protege los cálculos monetarios contra contaminaciones accidentales de precisión. En los archivos originales (`REPASO(02)_CLASS_ONE.py` L103, `Ejm_Operadores_Aritméticos.py` L59 y `calculadora_simple.py` L27), la expresión `v1 ** (1 / v2)` solo funciona porque `1` es `int` y `v2` es `Decimal`, de modo que `1 / v2` produce un `Decimal`; si se hubiese escrito `1.0 / v2`, fallaría con `TypeError`. Además, para raíces cuadradas, el propio objeto ofrece el método nativo `v1.sqrt()`, que calcula con precisión exacta de última unidad (*ulp*) en lugar de sufrir el redondeo intermedio de `1 / Decimal(3)`.

**Contextos de ejecución: `getcontext()` frente a `localcontext()`, y qué significa realmente `prec`.** Todas las operaciones aritméticas de `decimal` consultan un **contexto activo** por hilo de ejecución:

- `getcontext()` devuelve el contexto actual del hilo (por defecto `prec = 28` dígitos significativos y modo de redondeo `ROUND_HALF_EVEN`). Modificar `getcontext().prec` altera globalmente el comportamiento de cualquier otra biblioteca llamada después en el mismo hilo.
- `with localcontext() as ctx:` crea una copia temporal aislada del contexto y restaura automáticamente los parámetros previos al salir del bloque `with`, incluso si ocurre una excepción.
- **Distinción esencial:** `ctx.prec` define la cantidad total de **cifras significativas** (contando tanto la parte entera como la fraccionaria) durante resultados intermedios de operaciones aritméticas, **no** la cantidad de decimales fijos tras el punto. Si `ctx.prec = 2`, sumar `Decimal("123.45") + Decimal("0.01")` produce `Decimal('1.2E+2')` (`120`). Para fijar una escala decimal exacta (p. ej. 2 decimales para céntimos) se emplea siempre `.quantize(...)`.

**Escala fija con `.quantize()` y políticas de redondeo.** El método `valor.quantize(exp, rounding=...)` ajusta `valor` para que adopte exactamente el mismo exponente que el modelo `exp` (tanto `Decimal("0.01")` como `Decimal("0.00")`, usado en los cinco scripts originales, tienen exponente `-2` y producen idéntica escala de dos decimales):

- `ROUND_HALF_EVEN` (*redondeo al par más cercano* o *redondeo bancario*, predeterminado en `decimal` y en `round()` de Python): ante un empate exacto en `.xx5`, redondea hacia el dígito par (`2.645` -> `2.64`, `2.655` -> `2.66`). Minimiza el sesgo estadístico acumulado al sumar miles de partidas contables.
- `ROUND_HALF_UP` (*redondeo comercial clásico*, empleado en `redondeo.py` L6): ante un empate `.xx5`, se aleja siempre de cero (`2.645` -> `2.65`, `-2.645` -> `-2.65`). Es el exigido habitualmente en boletas y facturas minoristas.
- `ROUND_DOWN`: trunca hacia cero descartando dígitos sobrantes (`2.649` -> `2.64`, `-2.649` -> `-2.64`).
- `ROUND_FLOOR` y `ROUND_CEILING`: redondean hacia $-\infty$ y $+\infty$ respectivamente (útil en cálculo prudencial de comisiones o retenciones).

**Señales (*signals*) y trampas (*traps*) del contexto.** El módulo modela condiciones excepcionales como señales (`InvalidOperation`, `DivisionByZero`, `Overflow`, `Inexact`, `Rounded`, `FloatOperation`). Cuando una señal tiene activada su trampa en `ctx.traps[Senal] = True`, lanza inmediatamente la excepción correspondiente (todas subclases de `ArithmeticError` o `ValueError`); por ejemplo, `Decimal("abc")` o `Decimal("0") / Decimal("0")` lanzan `decimal.InvalidOperation`, y `Decimal("1") / Decimal("0")` lanza `decimal.DivisionByZero`. Activar `ctx.traps[FloatOperation] = True` en sistemas financieros estrictos hace que incluso `Decimal(0.1)` o `Decimal("0.1") < 0.2` fallen de inmediato.

## 4. Sintaxis y funcionamiento

Patrón seguro para operaciones monetarias y cambios aislados de contexto:

```text
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext

CENTAVO = Decimal("0.01")
monto = (Decimal("<cantidad_str>") * Decimal("<precio_str>")).quantize(
    CENTAVO, rounding=ROUND_HALF_UP
)
```

Referencia de constructores, métodos, constantes de redondeo y señales:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `Decimal("0.10")` | Construcción exacta en base 10 desde `str` (conserva escala `-2`) | `precio = Decimal("19.99")` |
| 2 | `Decimal(entero)` | Construcción exacta desde `int` | `iva = Decimal(18) / Decimal(100)` |
| 3 | `d.quantize(exp, rounding=...)` | Ajusta `d` a la escala decimal de `exp` con la regla indicada | `d.quantize(Decimal("0.01"))` |
| 4 | `ROUND_HALF_EVEN` | Empates al dígito par más cercano (predeterminado bancario) | `rounding=ROUND_HALF_EVEN` |
| 5 | `ROUND_HALF_UP` | Empates alejándose de cero (redondeo comercial tradicional) | `rounding=ROUND_HALF_UP` |
| 6 | `ROUND_DOWN` / `ROUND_CEILING` | Truncado hacia `0` / redondeo hacia $+\infty$ | `rounding=ROUND_DOWN` |
| 7 | `d.sqrt()` | Raíz cuadrada decimal con precisión completa del contexto | `Decimal(2).sqrt()` |
| 8 | `getcontext()` | Consulta el contexto decimal activo del hilo actual | `prec = getcontext().prec` |
| 9 | `with localcontext() as ctx:` | Modifica precisión, redondeo o trampas de forma aislada y reversible | `ctx.prec = 50` |
| 10 | `InvalidOperation` / `DivisionByZero` | Excepciones lanzadas ante entradas inválidas o división entre `0` | `except InvalidOperation:` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Contraste entre `float` binario (IEEE 754) y `Decimal`, y comparación de políticas de redondeo con `.quantize()`.**

```python
from decimal import (
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_HALF_EVEN,
    ROUND_HALF_UP,
    Decimal,
)

suma_float = 0.1 + 0.2
suma_decimal = Decimal("0.1") + Decimal("0.2")
print("float   0.1 + 0.2 :", repr(suma_float), "| ¿== 0.3?:", suma_float == 0.3)
print("Decimal 0.1 + 0.2 :", suma_decimal, "| ¿== Decimal('0.3')?:", suma_decimal == Decimal("0.3"))

# Caso de redondeo.py (L3-7): 2.675 en float frente a Decimal
print("round(2.675, 2) en float           :", round(2.675, 2))
print(
    "Decimal('2.675') con ROUND_HALF_UP :",
    Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
)

centavo = Decimal("0.01")
for muestra in (Decimal("2.645"), Decimal("2.655")):
    print(
        f"Valor {muestra} -> "
        f"HALF_EVEN={muestra.quantize(centavo, rounding=ROUND_HALF_EVEN)} | "
        f"HALF_UP={muestra.quantize(centavo, rounding=ROUND_HALF_UP)} | "
        f"DOWN={muestra.quantize(centavo, rounding=ROUND_DOWN)} | "
        f"CEILING={muestra.quantize(centavo, rounding=ROUND_CEILING)}"
    )
```

Explicación paso a paso:

- Se verifica que `0.1 + 0.2` en `float` no es exactamente igual a `0.3`, mientras que `Decimal("0.1") + Decimal("0.2")` produce exactamente `Decimal('0.3')`.
- Se explica experimentalmente el comentario de `redondeo.py` (L3-7): `Decimal("2.675")` redondeado con `ROUND_HALF_UP` produce `2.68`, frente al `2.67` devuelto por `round(2.675, 2)` en binario.
- Sobre los empates exactos `2.645` y `2.655` se aprecia cómo `ROUND_HALF_EVEN` converge siempre al centésimo par (`2.64` y `2.66`), mientras que `ROUND_HALF_UP` sube ambos (`2.65` y `2.66`).

Resultado esperado:

```text
float   0.1 + 0.2 : 0.30000000000000004 | ¿== 0.3?: False
Decimal 0.1 + 0.2 : 0.3 | ¿== Decimal('0.3')?: True
round(2.675, 2) en float           : 2.67
Decimal('2.675') con ROUND_HALF_UP : 2.68
Valor 2.645 -> HALF_EVEN=2.64 | HALF_UP=2.65 | DOWN=2.64 | CEILING=2.65
Valor 2.655 -> HALF_EVEN=2.66 | HALF_UP=2.66 | DOWN=2.65 | CEILING=2.66
```

### Intermedio

**Ejemplo 2 — Liquidación de factura con impuestos y prorrateo exacto en cuotas sin descuadre de céntimos.**

```python
from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")


def liquidar_factura(
    lineas: list[tuple[str, int, str]],
    tasa_impuesto: str = "0.18",
    numero_cuotas: int = 3,
) -> dict[str, Decimal | list[Decimal]]:
    if numero_cuotas <= 0:
        raise ValueError("El número de cuotas debe ser mayor que cero")

    subtotal = sum(
        (
            (Decimal(cantidad) * Decimal(precio_str)).quantize(
                CENTAVO, rounding=ROUND_HALF_EVEN
            )
            for _, cantidad, precio_str in lineas
        ),
        start=Decimal("0.00"),
    )
    impuesto = (subtotal * Decimal(tasa_impuesto)).quantize(
        CENTAVO, rounding=ROUND_HALF_UP
    )
    total = subtotal + impuesto

    cuota_base = (total / Decimal(numero_cuotas)).quantize(
        CENTAVO, rounding=ROUND_DOWN
    )
    cuotas = [cuota_base] * numero_cuotas
    residuo = total - sum(cuotas, start=Decimal("0.00"))
    cuotas[0] += residuo

    return {
        "subtotal": subtotal,
        "impuesto": impuesto,
        "total": total,
        "cuotas": cuotas,
    }


conceptos = [
    ("Licencia anual", 3, "19.99"),
    ("Soporte técnico", 2, "14.55"),
]
factura = liquidar_factura(conceptos, tasa_impuesto="0.18", numero_cuotas=3)
lista_cuotas = factura["cuotas"]
assert isinstance(lista_cuotas, list)

print("Subtotal :", factura["subtotal"])
print("IGV (18%):", factura["impuesto"])
print("Total    :", factura["total"])
print("Cuotas   :", [str(c) for c in lista_cuotas])
print(
    "Suma de cuotas == Total:",
    sum(lista_cuotas, start=Decimal("0.00")) == factura["total"],
)
```

Explicación técnica:

- Al dividir un total de `105.10` en `3` partes iguales ($105.10 / 3 = 35.0333\ldots$), redondear cada cuota de manera aislada a `35.03` sumaría `105.09`, dejando desaparecer `0.01` en el libro mayor.
- Truncar la cuota base con `ROUND_DOWN` (`35.03`), calcular el residuo exacto (`105.10 - 105.09 = 0.01`) y adjudicarlo a la primera cuota (`35.04`) garantiza la invariante contable fundamental: la suma de las partes coincide al céntimo con el total facturado.

Resultado esperado:

```text
Subtotal : 89.07
IGV (18%): 16.03
Total    : 105.10
Cuotas   : ['35.04', '35.03', '35.03']
Suma de cuotas == Total: True
```

### Avanzado

**Ejemplo 3 — Contextos aislados con `localcontext()`, alta precisión científica decimal y control de trampas (`DivisionByZero`, `FloatOperation`).**

```python
from decimal import (
    Decimal,
    DivisionByZero,
    FloatOperation,
    getcontext,
    localcontext,
)

print("Precisión global antes:", getcontext().prec)

with localcontext() as ctx:
    ctx.prec = 50
    raiz_dos = Decimal(2).sqrt()
    un_septimo = Decimal(1) / Decimal(7)

print("sqrt(2) (50 cifras):", str(raiz_dos)[:32] + "...")
print("1 / 7   (50 cifras):", str(un_septimo)[:32] + "...")
print("Precisión global después:", getcontext().prec)

# Desactivar temporalmente la trampa DivisionByZero produce Infinity IEEE 754
with localcontext() as ctx:
    ctx.traps[DivisionByZero] = False
    limite = Decimal("1") / Decimal("0")
    print("1 / 0 sin trampa activa :", limite)

# Activar FloatOperation bloquea cualquier ingreso accidental de float binario
with localcontext() as ctx:
    ctx.traps[FloatOperation] = True
    try:
        _ = Decimal(0.1)
    except FloatOperation as err:
        print("Trampa preventiva activada:", type(err).__name__)
```

Explicación avanzada:

- Dentro del primer `with localcontext() as ctx:`, elevar `ctx.prec = 50` permite calcular `Decimal(2).sqrt()` (sustituyendo la aproximación `v1 ** (1 / v2)` de `calculadora_simple.py` L27) con 50 cifras significativas exactas, dejando intacto el valor global `getcontext().prec == 28` al salir del bloque.
- El tercer bloque ilustra una salvaguarda de nivel bancario: activar `ctx.traps[FloatOperation] = True` impide en tiempo de ejecución que cualquier desarrollador introduzca por descuido un `float` binario en el motor contable.

Resultado esperado:

```text
Precisión global antes: 28
sqrt(2) (50 cifras): 1.414213562373095048801688724209...
1 / 7   (50 cifras): 0.142857142857142857142857142857...
Precisión global después: 28
1 / 0 sin trampa activa : Infinity
Trampa preventiva activada: FloatOperation
```

## 6. Aplicaciones en el mundo real

- **Sistemas contables, ERP y facturación electrónica:** cálculo exacto de bases imponibles, descuentos escalonados, retenciones tributarias (IGV, IVA, ISR) y conciliación bancaria sin diferencias de redondeo.
- **Pasarelas de pago, billeteras digitales y casas de cambio (*fintech*):** conversión multidivisa con tasas de 6 u 8 decimales intermedios (`Decimal("3.748520")`) antes de cuantizar el importe liquidado a la unidad mínima de la moneda destino (`0.01` para USD/PEN/EUR o `1` para JPY/CLP).
- **Contratos de comercio electrónico y carritos de compra:** valoración de cupones porcentuales y reparto proporcional entre múltiples artículos manteniendo cuadrada la suma total cobrada.
- **Auditoría regulatoria y tarifas de servicios públicos:** facturación de consumo eléctrico, agua o telecomunicaciones donde los pliegos tarifarios fijan por ley el número de decimales y el modo de redondeo aplicable.

## 7. Uso en producción

- **Elegir `Decimal` frente a `float` según el dominio del problema:** `Decimal` es obligatorio para **dinero, tasas contractuales y contabilidad**, donde las reglas están escritas en base 10; en cambio, para **aprendizaje automático, simulación física, geometría 3D o álgebra lineal masiva** ([Pandas](../chapter-three/pandas_fundamentos.md), NumPy), debe utilizarse `float64`/`float32` vectorizado en hardware, ya que `Decimal` es entre 3 y 15 veces más lento que `float` nativo (aunque CPython incluye la aceleración en C `libmpdec`).
- **Mapear hacia `NUMERIC(p, s)` / `DECIMAL(p, s)` en bases de datos y hacia `str` en JSON:** en SQL nunca deben almacenarse montos monetarios en columnas `REAL` o `DOUBLE PRECISION`, sino en `NUMERIC(19, 4)` o `NUMERIC(12, 2)` (que los adaptadores como `psycopg` convierten directamente a `decimal.Decimal`). Al serializar hacia JSON —formato cuyas implementaciones cliente suelen parsear números como `float` IEEE 754—, los importes monetarios se transmiten como cadenas (`"105.10"`) o en unidades enteras mínimas (céntimos: `10510`).
- **Redondear al final de cada etapa reglamentaria, no en cada suboperación arbitraria:** en cálculos financieros (interés compuesto, tipo de cambio), las operaciones intermedias se ejecutan con la precisión amplia del contexto (28 dígitos) y solo se invoca `.quantize(...)` en los puntos donde la norma contable exige asentar un importe redondeado.
- **Usar siempre `localcontext()` en lugar de mutar `getcontext()`:** modificar `getcontext().prec` o `getcontext().rounding` a nivel de módulo genera efectos colaterales difíciles de depurar sobre otras partes de la aplicación que compartan el mismo hilo.

## 8. Errores comunes y recomendaciones

1. **Instanciar `Decimal(0.1)` pasando un `float` en vez de una cadena `Decimal("0.1")`.**

```python
from decimal import Decimal

desde_float = Decimal(0.1)
desde_str = Decimal("0.1")

print("Decimal(0.1)  :", desde_float)
print("Decimal('0.1'):", desde_str)
print("¿Son iguales? :", desde_float == desde_str)
```

Resultado esperado:

```text
Decimal(0.1)  : 0.1000000000000000055511151231257827021181583404541015625
Decimal('0.1'): 0.1
¿Son iguales? : False
```

Diagnóstico: pasar un `float` traslada a `Decimal` la aproximación binaria previa. Recomendación: pasar siempre literales `str` (`Decimal("0.1")`) o `int`.

2. **Mezclar `Decimal` con `float` en una expresión aritmética (`TypeError`).**

```python
# ERROR INTENCIONAL: TypeError al multiplicar directamente un objeto Decimal por un float
from decimal import Decimal

precio = Decimal("100.00")
con_impuesto = precio * 1.18
```

Diagnóstico: Python lanza `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'`. Solución: representar ambos operandos como `Decimal` (`precio * Decimal("1.18")`) o enteros.

3. **Reducir `ctx.prec = 2` creyendo que fija dos posiciones decimales.**

```python
from decimal import Decimal, localcontext

with localcontext() as ctx:
    ctx.prec = 2
    erroneo = Decimal("123.45") + Decimal("0.01")

correcto = (Decimal("123.45") + Decimal("0.01")).quantize(Decimal("0.01"))
print("Con ctx.prec = 2          :", erroneo)
print("Con .quantize(Decimal('0.01')):", correcto)
```

Resultado esperado:

```text
Con ctx.prec = 2          : 1.2E+2
Con .quantize(Decimal('0.01')): 123.46
```

Diagnóstico: `prec = 2` recorta el resultado total a **dos cifras significativas** (`1.2E+2` = `120`), amputando unidades y centavos. Recomendación: mantener `prec` alto (p. ej. el valor por defecto `28`) y fijar los decimales exclusivamente con `.quantize(Decimal("0.01"))`.

4. **Pasar texto con coma decimal o no numérico sin capturar `decimal.InvalidOperation`.**

```python
# ERROR INTENCIONAL: InvalidOperation al construir Decimal con coma sin normalizar
from decimal import Decimal

monto_invalido = Decimal("12,50")
```

Diagnóstico: a diferencia de `int()` o `float()` que lanzan `ValueError`, el constructor `Decimal` señala errores de sintaxis numérica lanzando `decimal.InvalidOperation` (subclase de `ArithmeticError`). En calculadoras o formularios como `calculadora_simple.py` (L8-9), debe normalizarse el separador si procede (`Ejm_Operadores_Aritméticos.py` L6-7) y envolver la conversión y la división en un bloque `try` que capture `(InvalidOperation, DivisionByZero)`.

## 9. Resumen

- El módulo `decimal` pertenece a la **biblioteca estándar de Python** y proporciona aritmética exacta en base 10 libre de los errores de representación binaria de `float` (IEEE 754 *binary64*).
- Las instancias de `Decimal` deben crearse a partir de `str` (`Decimal("19.99")`) o `int`, nunca desde literales `float` (`Decimal(19.99)`), y no admiten operaciones aritméticas directas mezcladas con `float` (`TypeError`).
- La propiedad `prec` del contexto controla el total de **cifras significativas** de las operaciones, no el número de decimales; para fijar posiciones decimales y aplicar políticas explícitas (`ROUND_HALF_EVEN`, `ROUND_HALF_UP`, `ROUND_DOWN`, `ROUND_CEILING`) se emplea `.quantize(Decimal("0.01"), rounding=...)`.
- Cualquier cambio temporal de precisión, redondeo o trampas (`FloatOperation`, `DivisionByZero`) debe encapsularse dentro del gestor de contexto `with localcontext() as ctx:`.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/numero_decimal.py` (L1-10) | `numero_decimal.py` | Importación de `Decimal` y `ROUND_HALF_UP`, suma desde cadenas y `.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)` | Se fundamentó matemáticamente por qué debe pasarse `str` en lugar de `float` y la equivalencia de escala entre `Decimal("0.00")` y `Decimal("0.01")` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/redondeo.py` (L1-20) | `redondeo.py` | Redondeo de `"2.675"` a `2.68` con `ROUND_HALF_UP` y suma redondeada a dos decimales | Se explicó por qué `round(2.675, 2)` en `float` binario produce `2.67` y se contrastó `ROUND_HALF_UP` frente al redondeo bancario `ROUND_HALF_EVEN`, `ROUND_DOWN` y `ROUND_CEILING` |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/REPASO(02)_CLASS_ONE.py` (L1, L59-118) | `REPASO(02)_CLASS_ONE.py` | Operaciones `+`, `-`, `*`, `/`, `**`, `**(1/numero_2)`, `//` y `%` sobre objetos `Decimal` | Se precisó el rol de `.sqrt()` frente a exponentes fraccionarios y por qué `1 / numero_2` funciona con `int` pero fallaría con `1.0` (`TypeError`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJEMPLOS (CLASS_ONE)/Ejm_Operadores_Aritméticos.py` (L1-75) | `Ejm_Operadores_Aritméticos.py` | Normalización previa de coma a punto con `.replace(",", ".")` antes de instanciar `Decimal` | Se integró con el manejo defensivo de señales `InvalidOperation` ante entradas mal formadas |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/EJERCICIOS_DE_CLASE_ONE.PY/calculadora_simple.py` (L1-30) | `calculadora_simple.py` | Calculadora ramificada por operador empleando `Decimal` y `ROUND_HALF_UP` | Se amplió hacia facturación real con prorrateo de céntimos sin descuadre y captura de `DivisionByZero` e `InvalidOperation` |

**Fundamento complementario:** se añadieron cuatro bloques conceptuales clave de la biblioteca estándar de Python para completar el dominio profesional del módulo: (1) el análisis interno de coma flotante binaria IEEE 754 de 53 bits frente a la representación decimal exacta; (2) la gestión de contextos globales y aislados (`getcontext()` frente a `localcontext()`) aclarando la diferencia entre cifras significativas (`prec`) y escala decimal (`quantize`); (3) el sistema de señales y trampas (`InvalidOperation`, `DivisionByZero`, `FloatOperation`); y (4) los criterios de arquitectura para elegir entre `Decimal` (finanzas/SQL `NUMERIC`) y `float` vectorizado (cómputo científico).

## 11. Referencias oficiales

- <https://docs.python.org/3/library/decimal.html> — Biblioteca estándar (`decimal`): especificación completa de `Decimal`, `Context`, `getcontext()`, `localcontext()`, modos de redondeo, `.quantize()` y señales/trampas.
- <https://docs.python.org/3/tutorial/floatingpoint.html> — Tutorial oficial de Python (*Floating-Point Arithmetic: Issues and Limitations*): explicación detallada de las fracciones binarias IEEE 754 y por qué `0.1 + 0.2 != 0.3`.
