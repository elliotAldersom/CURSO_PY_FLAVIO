# Fechas, Horas, Diferencias Temporales y Zonas Horarias (`datetime` y `zoneinfo`)

## 2. Introducción

Representar fechas y marcas de tiempo como simples [cadenas de texto](../../Basico/chapter-two/cadenas.md) (`"07/11/2025"`) o números enteros sueltos (`anyo_bi.py` L1-8) resulta frágil en cualquier aplicación real: los meses tienen longitudes variables (28, 29, 30 o 31 días), el calendario gregoriano aplica reglas compuestas para los años bisiestos, los formatos regionales invierten día y mes (`DD/MM/YYYY` frente a `MM/DD/YYYY`), y un mismo instante físico corresponde a horas civiles distintas según el huso horario y el horario de verano (*DST*, *Daylight Saving Time*).

Para resolver estos desafíos sin dependencias externas, la **biblioteca estándar de Python** provee tres [módulos](../chapter-three/modulos.md) complementarios e integrados de fábrica:

1. **`datetime`:** define los tipos inmutables fundamentales para fechas de calendario (`date`), horas del reloj (`time`), marcas combinadas (`datetime`), intervalos aritméticos (`timedelta`) y desplazamientos fijos respecto a UTC (`timezone`).
2. **`zoneinfo` (incorporado en Python 3.9 mediante PEP 615):** conecta directamente con la base de datos oficial de zonas horarias de la **IANA** (`America/Lima`, `America/Argentina/Buenos_Aires`, `Europe/Madrid`), aplicando reglas históricas y transiciones de horario de verano de forma automática.
3. **`calendar`:** suministra utilidades de calendario gregoriano, incluida la verificación exacta de años bisiestos (`calendar.isleap`).

Dominar la distinción entre objetos temporales ingenuos (*naive*) y conscientes de zona horaria (*timezone-aware*), así como el estándar internacional **ISO 8601**, es indispensable para evitar desfases silenciosos en bitácoras, facturación, vencimientos contractuales y sistemas distribuidos.

## 3. Fundamentos y conceptos

**Módulos de la biblioteca estándar y clases centrales de `datetime`.** El módulo estándar `datetime` (importado en `CLASE_ONE.py` L1001 y `FECHA_HORA.py` L2) contiene una clase homónima `datetime.datetime` —motivo por el cual resulta habitual importar sus clases de forma explícita mediante `from datetime import date, time, datetime, timedelta, timezone`—. Todos sus objetos son **inmutables** y *hashables* (aptos como claves de [diccionarios](../chapter-one/diccionarios.md) o elementos de [conjuntos](../chapter-one/conjuntos.md)):

- `date(year, month, day)`: representa una fecha idealizada del calendario gregoriano (año entre `1` y `9999`), sin componente horario. Valida automáticamente la existencia del día en ese mes y año, lanzando `ValueError` ante fechas imposibles como `date(2025, 2, 29)`.
- `time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)`: representa una hora del día aislada de cualquier fecha concreta (`00:00:00.000000` a `23:59:59.999999`).
- `datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)`: hereda de `date` y combina fecha completa y hora con resolución de microsegundos.
- `timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)`: modela la duración o diferencia exacta entre dos objetos `date` o `datetime`. Internamente normaliza cualquier combinación de argumentos únicamente a tres atributos enteros: `.days`, `.seconds` (entre `0` y `86399`) y `.microseconds` (entre `0` y `999999`); para obtener la duración completa expresada en segundos se utiliza el método `.total_seconds()`.
- `timezone`: subclase concreta de la interfaz abstracta `tzinfo` para desplazamientos fijos respecto al Tiempo Universal Coordinado, destacando el *singleton* `timezone.utc` (`UTC+00:00`).

**Objetos *naive* (ingenuos) frente a *timezone-aware* (conscientes de zona horaria).** Esta es la distinción conceptual más crítica del módulo `datetime`:

- Un objeto **naive** carece de referencia geográfica o desplazamiento temporal (`dt.tzinfo is None`). Es lo que devuelve `datetime.now()` sin argumentos (`CLASE_ONE.py` L1002, `FECHA_HORA.py` L3): toma la hora local del sistema operativo anfitrión pero descarta qué zona horaria utilizó. Un `datetime(2025, 7, 15, 10, 0)` *naive* es ambiguo: no permite saber si ocurrió en Lima, en Ciudad de México o en UTC.
- Un objeto **aware** posee un `tzinfo` válido con desplazamiento no nulo (`dt.tzinfo is not None` y `dt.utcoffset() is not None`), anclándolo de forma inequívoca a la línea de tiempo física universal.
- **Obsolescencia de `datetime.utcnow()` y `datetime.utcfromtimestamp()` en Python 3.12+:** históricamente, `datetime.utcnow()` devolvía la hora actual en UTC pero como un objeto *naive* (`tzinfo=None`), lo que provocaba errores graves cuando otras funciones asumían que un objeto *naive* estaba en hora local. Desde Python 3.12 ambos métodos están formalmente **obsoletos (*deprecated*)** y emiten `DeprecationWarning`; la forma canónica y vigente de obtener el instante actual en UTC es siempre `datetime.now(timezone.utc)`.
- Python impide mezclar ambos mundos: comparar (`<`, `>`) o restar (`-`) un `datetime` *naive* con uno *aware* lanza inmediatamente `TypeError` (véase [excepciones](excepciones.md)).

**Zonas horarias IANA con `zoneinfo.ZoneInfo` (PEP 615).** Un desplazamiento fijo como `timezone(timedelta(hours=-5))` solo expresa "-5 horas siempre", pero las jurisdicciones reales cambian sus reglas legales y adoptan o eliminan horarios de verano (*DST*). Desde Python 3.9, el módulo estándar `zoneinfo` permite instanciar `ZoneInfo("America/Lima")` o `ZoneInfo("Europe/Madrid")` consultando la base de datos IANA del sistema operativo (o el paquete oficial de respaldo `tzdata` en entornos Windows o contenedores mínimos). El método `dt_aware.astimezone(otra_zona)` convierte instantáneamente un instante entre cualesquiera zonas horarias preservando el mismo momento físico (`dt_utc == dt_lima == dt_madrid` evalúa a `True`).

Conviene notar además una sutileza de la aritmética en `datetime` (**PEP 495**): restar dos objetos *aware* que comparten exactamente la misma instancia `ZoneInfo` calcula la diferencia nominal de reloj de pared; para medir el **tiempo físico real transcurrido** a través de un salto de cambio de hora (*DST*), ambos extremos deben convertirse primero a `timezone.utc` y restarse allí.

**Estándar ISO 8601 frente a formateo y análisis personalizado (`strftime` y `strptime`).**

- **Intercambio entre sistemas (ISO 8601):** `.isoformat()` genera representaciones inequívocas ordenables lexicográficamente como `"2025-07-15T18:30:00+00:00"` (o `"2025-07-15"` en `date`), y `datetime.fromisoformat(cadena)` las reconstruye con alta eficiencia (soportando desde Python 3.11 el sufijo `"Z"` para UTC).
- **Presentación humana y formatos heredados:** `dt.strftime(formato)` (*string format time*, empleado en `CLASE_ONE.py` L1008 y `FECHA_HORA.py` L8 con `"%d/%m/%Y  %H:%M:%S"`) formatea un objeto temporal hacia `str` mediante directivas con `%`, mientras que el método de clase `datetime.strptime(texto, formato)` (*string parse time*) realiza el camino inverso validando y construyendo un `datetime` desde una cadena.

**Regla completa de años bisiestos y `calendar.isleap`.** En `anyo_bi.py` (L1-9) quedó inconcluso el algoritmo para determinar si un año es bisiesto (`if fecha % 4 == 0: v1 = fecha // 100`). En el calendario gregoriano, un año $a$ tiene 366 días (29 de febrero) si y solo si es divisible entre 4, **excepto** los años seculares divisibles entre 100, **salvo** que también sean divisibles entre 400:

$$\text{bisiesto}(a) \iff (a \bmod 4 = 0 \land a \bmod 100 \neq 0) \lor (a \bmod 400 = 0)$$

Así, `2024` y `2000` son bisiestos, pero `1900` y `2100` no lo son. La biblioteca estándar encapsula esta regla exacta en `calendar.isleap(a)`.

## 4. Sintaxis y funcionamiento

Patrón recomendado para instanciar, convertir, operar y serializar marcas de tiempo conscientes de zona horaria:

```text
from datetime import date, time, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

instante_utc = datetime.now(timezone.utc)
instante_local = instante_utc.astimezone(ZoneInfo("<Continente>/<Ciudad>"))
vencimiento = instante_utc + timedelta(days=<n>, hours=<h>)
```

Referencia de clases, métodos y directivas principales de formato:

| N° | Elemento | Descripción | Ejemplo |
|---|---|---|---|
| 1 | `date(y, m, d)` | Fecha inmutable del calendario gregoriano | `d = date(2025, 11, 7)` |
| 2 | `time(H, M, S)` | Hora del día independiente de fecha | `t = time(14, 30, 0)` |
| 3 | `datetime.now(timezone.utc)` | Marca de tiempo actual *aware* en UTC (estándar vigente) | `ahora = datetime.now(timezone.utc)` |
| 4 | `ZoneInfo("Región/Ciudad")` | Zona horaria IANA oficial con reglas históricas y *DST* | `lima = ZoneInfo("America/Lima")` |
| 5 | `dt.astimezone(tz)` | Convierte un `datetime` *aware* hacia otra zona horaria | `dt_utc.astimezone(lima)` |
| 6 | `timedelta(days=..., hours=...)` | Duración exacta para sumar o restar fechas y horas | `plazo = timedelta(days=15)` |
| 7 | `td.total_seconds()` | Total completo del `timedelta` en segundos (`float`) | `seg = plazo.total_seconds()` |
| 8 | `dt.isoformat()` / `fromisoformat` | Serialización y lectura estándar **ISO 8601** | `datetime.fromisoformat(s)` |
| 9 | `dt.strftime(fmt)` | Formatea `date`/`time`/`datetime` a `str` según directivas | `dt.strftime("%d/%m/%Y %H:%M:%S")` |
| 10 | `datetime.strptime(s, fmt)` | Analiza `str` según `fmt` y construye un `datetime` | `datetime.strptime("07/11/2025", "%d/%m/%Y")` |
| 11 | `%Y`, `%m`, `%d`, `%H`, `%M`, `%S`, `%z` | Año 4 dígitos, mes `01-12`, día `01-31`, hora 24h, minuto, segundo, *offset* UTC | `"%Y-%m-%d %H:%M:%S%z"` |
| 12 | `d.weekday()` / `calendar.isleap(y)` | Día de la semana (`0`=lunes ... `6`=domingo) y año bisiesto | `calendar.isleap(2024)` |

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Construcción determinista, formateo/análisis (`strftime`/`strptime`), ISO 8601 y resolución completa de años bisiestos.**

```python
import calendar
from datetime import date, datetime, time


def es_bisiesto_gregoriano(anio: int) -> bool:
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


fecha_bisiesta = date(2024, 2, 29)
hora_apertura = time(9, 30, 15)
evento = datetime.combine(fecha_bisiesta, hora_apertura)

formato_legible = evento.strftime("%d/%m/%Y %H:%M:%S")
reconstruido = datetime.strptime(formato_legible, "%d/%m/%Y %H:%M:%S")
cadena_iso = evento.isoformat()

anios_prueba = [1900, 2000, 2024, 2025]
verificacion = {
    a: (es_bisiesto_gregoriano(a), calendar.isleap(a))
    for a in anios_prueba
}

print("Formato legible :", formato_legible)
print("ISO 8601        :", cadena_iso)
print("Ida y vuelta OK :", evento == reconstruido == datetime.fromisoformat(cadena_iso))
print("Años bisiestos  :", {a: par[0] for a, par in verificacion.items()})
print("Coincide stdlib :", all(p[0] == p[1] for p in verificacion.values()))
```

Explicación paso a paso:

- Se utilizan fechas fijas deterministas en lugar del reloj variable del sistema (`datetime.now()` en `CLASE_ONE.py` L1002 y `FECHA_HORA.py` L3), combinando `date` y `time` con `datetime.combine`.
- Se verifica la equivalencia exacta entre el objeto original, el reconstruido con `strptime` usando `"%d/%m/%Y %H:%M:%S"` y el reconstruido desde ISO 8601 con `fromisoformat`.
- Se completa el ejercicio inconcluso de `anyo_bi.py` contrastando la expresión booleana gregoriana completa con `calendar.isleap()`, incluyendo los casos frontera `1900` (`False`) y `2000` (`True`).

Resultado esperado:

```text
Formato legible : 29/02/2024 09:30:15
ISO 8601        : 2024-02-29T09:30:15
Ida y vuelta OK : True
Años bisiestos  : {1900: False, 2000: True, 2024: True, 2025: False}
Coincide stdlib : True
```

### Intermedio

**Ejemplo 2 — Aritmética temporal con `timedelta`: plazos calendario, días hábiles y cálculo de ventanas SLA en segundos.**

```python
from datetime import date, timedelta


def sumar_dias_habiles(inicio: date, dias_habiles: int) -> date:
    if dias_habiles < 0:
        raise ValueError("La cantidad de días hábiles no puede ser negativa")
    actual = inicio
    restantes = dias_habiles
    un_dia = timedelta(days=1)
    while restantes > 0:
        actual += un_dia
        if actual.weekday() < 5:  # 0=lunes ... 4=viernes; 5=sábado, 6=domingo
            restantes -= 1
    return actual


emision = date(2025, 5, 9)  # Viernes 9 de mayo de 2025
vencimiento_calendario = emision + timedelta(days=10)
vencimiento_habil = sumar_dias_habiles(emision, dias_habiles=10)
ventana_sla = timedelta(hours=36, minutes=30)

print("Fecha de emisión               :", emision.isoformat())
print("Más 10 días calendario         :", vencimiento_calendario.isoformat())
print("Más 10 días hábiles            :", vencimiento_habil.isoformat())
print("Atributos internos (days, secs):", (ventana_sla.days, ventana_sla.seconds))
print("Segundos totales de SLA (36.5h):", int(ventana_sla.total_seconds()))
```

Explicación técnica:

- Sumar `timedelta(days=10)` avanza días naturales incluyendo fines de semana (`2025-05-19`), mientras que iterar consultando `actual.weekday() < 5` permite calcular plazos administrativos o bancarios en días hábiles (`2025-05-23`).
- Se observa una distinción crucial en `timedelta(hours=36, minutes=30)`: el atributo `ventana_sla.seconds` almacena únicamente la fracción sobrante del día (`45000` segundos = 12.5 horas, ya que las primeras 24 horas pasaron a `ventana_sla.days == 1`), mientras que `ventana_sla.total_seconds()` entrega la duración íntegra (`131400` segundos).

Resultado esperado:

```text
Fecha de emisión               : 2025-05-09
Más 10 días calendario         : 2025-05-19
Más 10 días hábiles            : 2025-05-23
Atributos internos (days, secs): (1, 45000)
Segundos totales de SLA (36.5h): 131400
```

### Avanzado

**Ejemplo 3 — Conversión global entre zonas horarias IANA (`zoneinfo.ZoneInfo`) y duración física real durante un cambio de horario de verano (*DST*).**

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

instante_utc = datetime(2025, 7, 15, 18, 30, 0, tzinfo=timezone.utc)
zona_lima = ZoneInfo("America/Lima")
zona_madrid = ZoneInfo("Europe/Madrid")

en_lima = instante_utc.astimezone(zona_lima)
en_madrid = instante_utc.astimezone(zona_madrid)

print("UTC           :", instante_utc.isoformat())
print("America/Lima  :", en_lima.isoformat(), f"({en_lima.tzname()})")
print("Europe/Madrid :", en_madrid.isoformat(), f"({en_madrid.tzname()})")
print("Mismo instante:", instante_utc == en_lima == en_madrid)

# El 30 de marzo de 2025 en Madrid, a las 02:00 el reloj adelanta a las 03:00 (CET -> CEST)
antes_salto = datetime(2025, 3, 30, 1, 30, tzinfo=zona_madrid)
despues_salto = datetime(2025, 3, 30, 3, 30, tzinfo=zona_madrid)

duracion_fisica = (
    despues_salto.astimezone(timezone.utc) - antes_salto.astimezone(timezone.utc)
)
print("Antes del salto  :", antes_salto.isoformat())
print("Después del salto:", despues_salto.isoformat())
print("Tiempo real (UTC):", duracion_fisica)
```

Explicación de sistemas distribuidos:

- Un único evento registrado canónicamente en UTC (`18:30:00+00:00`) se proyecta con `.astimezone(...)` hacia `America/Lima` (`13:30:00-05:00`, sin horario de verano) y `Europe/Madrid` (`20:30:00+02:00`, horario de verano europeo `CEST`). La comparación `==` evalúa `True` porque Python compara ambos operandos respecto a UTC.
- Durante la madrugada del 30 de marzo de 2025 en Madrid, entre la `01:30+01:00` y las `03:30+02:00` los relojes locales parecen distar dos horas, pero al proyectar ambos instantes a `timezone.utc` se comprueba que solo transcurrió **una hora física** (`1:00:00`).

Resultado esperado:

```text
UTC           : 2025-07-15T18:30:00+00:00
America/Lima  : 2025-07-15T13:30:00-05:00 (-05)
Europe/Madrid : 2025-07-15T20:30:00+02:00 (CEST)
Mismo instante: True
Antes del salto  : 2025-03-30T01:30:00+01:00
Después del salto: 2025-03-30T03:30:00+02:00
Tiempo real (UTC): 1:00:00
```

## 6. Aplicaciones en el mundo real

- **Auditoría, trazabilidad y bitácoras distribuidas:** sellar todos los eventos de microservicios, contenedores y colas de mensajería en UTC con formato ISO 8601 (`2025-11-07T04:15:00.123456+00:00`) para correlacionar incidentes ocurridos en centros de datos de distintos continentes.
- **Expiración de tokens de autenticación (JWT y sesiones):** fijar los campos `iat` (*issued at*) y `exp` (*expiration*) sumando `datetime.now(timezone.utc) + timedelta(minutes=15)`.
- **Facturación, suscripciones y agendas médicas o aéreas:** almacenar fechas de vuelos o videollamadas junto al identificador IANA (`America/Lima`, `America/Santiago`) para recalcular correctamente la hora local si la legislación de un país modifica sus fechas de cambio de hora antes del evento.
- **Series temporales e ingesta de archivos [CSV](../chapter-three/archivos_csv.md):** convertir columnas textuales con formatos heterogéneos (`DD/MM/YYYY`, `YYYY-MM-DD`) a objetos `date` o `datetime` tipados antes de agregarlos o graficarlos.

## 7. Uso en producción

- **Regla de oro "UTC en el núcleo, zona local en los bordes":** toda persistencia en bases de datos (`TIMESTAMP WITH TIME ZONE` en PostgreSQL), cachés y contratos de API debe almacenar y transmitir marcas *aware* en UTC (`datetime.now(timezone.utc)`); la conversión a `ZoneInfo(...)` se realiza exclusivamente en la capa de presentación (interfaz web, correo electrónico o reporte PDF) según la preferencia del usuario.
- **Medir latencias y tiempos de ejecución con `time.perf_counter()`, no con `datetime.now()`:** el reloj de sistema consultado por `datetime.now()` puede saltar hacia adelante o retroceder cuando el demonio NTP sincroniza la hora del servidor. Para cronometrar cuánto tarda una consulta o una función en producción debe usarse el reloj monotónico de alta resolución `time.perf_counter()` del módulo estándar `time`.
- **Inyectar el reloj en pruebas unitarias:** una función de dominio que invoca internamente `datetime.now(timezone.utc)` depende de la hora en que corre la prueba. Aceptar un parámetro opcional `ahora: datetime | None = None` (o inyectar un proveedor de reloj) permite probar cierres de mes, años bisiestos y expiraciones de forma 100 % determinista sin pausar los tests.
- **Garantizar la disponibilidad de datos IANA en contenedores mínimos y Windows:** en imágenes Docker ultra reducidas sin `/usr/share/zoneinfo` o en entornos Windows, incluir el paquete oficial `tzdata` (mantenido por el equipo núcleo de Python) asegura que `ZoneInfo` disponga siempre de las tablas IANA actualizadas.

## 8. Errores comunes y recomendaciones

1. **Mezclar objetos *naive* y *timezone-aware* en comparaciones o restas (`TypeError`).**

```python
# ERROR INTENCIONAL: TypeError al restar un datetime naive con uno timezone-aware
from datetime import datetime, timezone

marca_naive = datetime(2025, 7, 15, 12, 0, 0)
marca_utc = datetime(2025, 7, 15, 12, 0, 0, tzinfo=timezone.utc)

diferencia = marca_utc - marca_naive
```

Diagnóstico: Python rechaza `marca_utc - marca_naive` con `TypeError: can't subtract offset-naive and offset-aware datetimes` para evitar suposiciones silenciosas sobre el huso horario del operando *naive*. Recomendación: construir siempre marcas de tiempo con `tzinfo=timezone.utc` o `ZoneInfo(...)` desde su origen.

2. **Confundir directivas en `strftime` / `strptime` (`%m` mes frente a `%M` minutos) o leer `.seconds` en lugar de `.total_seconds()`.**

```python
from datetime import datetime, timedelta

muestra = datetime(2025, 11, 7, 14, 5, 9)
print("Directiva errónea (%M es minuto):", muestra.strftime("%d/%M/%Y"))
print("Directiva correcta (%m es mes)  :", muestra.strftime("%d/%m/%Y"))

dos_dias = timedelta(days=2, seconds=30)
print("td.seconds (solo resto del día) :", dos_dias.seconds)
print("td.total_seconds() (completo)   :", int(dos_dias.total_seconds()))
```

Resultado esperado:

```text
Directiva errónea (%M es minuto): 07/05/2025
Directiva correcta (%m es mes)  : 07/11/2025
td.seconds (solo resto del día) : 30
td.total_seconds() (completo)   : 172830
```

Diagnóstico: `%m` en minúscula representa el mes (`01`-`12`) y `%M` en mayúscula los minutos (`00`-`59`); usar `%M` en una fecha produce fechas numéricamente plausibles pero falsas (`07/05/2025` en vez de `07/11/2025`). Del mismo modo, `dos_dias.seconds` vale `30` (descartando los 2 días almacenados en `.days`), por lo que cualquier cálculo de segundos totales debe usar `.total_seconds()`.

3. **Construir fechas inexistentes sin validar rangos de calendario (`ValueError`).**

```python
# ERROR INTENCIONAL: ValueError al instanciar el 29 de febrero en un año no bisiesto
from datetime import date

fecha_invalida = date(2025, 2, 29)
```

Diagnóstico: `2025` no es bisiesto, por lo que `date(2025, 2, 29)` lanza `ValueError: day is out of range for month`. Recomendación: al sumar meses o años a fechas cercanas a fin de mes (p. ej., un año después del `2024-02-29`), no basta con ejecutar `fecha.replace(year=fecha.year + 1)` sin controlar `ValueError` o ajustar al último día válido del mes mediante `calendar.monthrange(anio, mes)`.

4. **Seguir invocando `datetime.utcnow()` en Python 3.12 o superior.** Aunque el nombre sugiere UTC, retorna un `datetime` *naive* sin `tzinfo` y emite `DeprecationWarning`. Debe reemplazarse en todo código moderno por `datetime.now(timezone.utc)`.

## 9. Resumen

- Los módulos `datetime`, `zoneinfo` y `calendar` forman parte de la **biblioteca estándar de Python** y cubren representación, aritmética, formateo y zonas horarias sin requerir instalaciones de terceros en sistemas POSIX.
- Las clases `date`, `time`, `datetime` y `timedelta` son inmutables; en `timedelta`, la duración total en segundos se consulta siempre mediante `.total_seconds()`.
- Un `datetime` *naive* (`tzinfo is None`) carece de anclaje universal, mientras que uno *aware* incorpora `timezone.utc` o `ZoneInfo("Continente/Ciudad")` (**PEP 615**); en Python 3.12+ debe usarse `datetime.now(timezone.utc)` en sustitución del obsoleto `datetime.utcnow()`.
- El formato **ISO 8601** (`isoformat()` / `fromisoformat()`) constituye el estándar para persistencia y APIs, reservándose `strftime()` y `strptime()` para formatos regionales de visualización o lectura de fuentes heredadas.

## 10. Relación con el material original

| Directorio de origen | Ruta relativa | Archivo | Conceptos identificados | Aspectos ampliados o profundizados |
|---|---|---|---|---|
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/CLASS_ONE/CLASE_ONE.py` (L999-1009) | `CLASE_ONE.py` | Importación de `datetime`, obtención de fecha/hora local con `datetime.datetime.now()`, inspección con `type()` y formateo con `.strftime("%d/%m/%Y  %H:%M:%S")` | Se explicó por qué `datetime.now()` sin argumentos produce un objeto *naive*, incorporando `timezone.utc`, `strptime`, ISO 8601 y el resto de clases del módulo (`date`, `time`, `timedelta`) |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/FECHA_HORA.py` (L1-9) | `FECHA_HORA.py` | Práctica aislada de `datetime.datetime.now()` y formato `"%d/%m/%Y  %H:%M:%S"` | Se transformó el uso dependiente del reloj del sistema en ejemplos deterministas verificables y orientados a sistemas en producción |
| `CLASES_PYTHON/` | `CLASES_PYTHON/CLASE_ONE/COSAS_GENERALES/anyo_bi.py` (L1-9) | `anyo_bi.py` | Boceto incompleto de comprobación de año bisiesto mediante operadores `% 4` y `// 100` | Se completó la regla gregoriana exacta (`% 4`, `% 100`, `% 400`), se contrastó con `calendar.isleap()` de la biblioteca estándar y con la validación intrínseca de `datetime.date` |

**Fundamento complementario:** dado que el material original abordó únicamente `datetime.now()` y `strftime()`, se incorporaron los pilares indispensables de la biblioteca estándar moderna de Python: (1) la distinción rigurosa entre objetos *naive* y *timezone-aware* junto con la obsolescencia de `datetime.utcnow()` en Python 3.12+; (2) la aritmética temporal con `timedelta` y `.total_seconds()`; (3) la serialización **ISO 8601** (`isoformat` / `fromisoformat`) y el análisis con `strptime`; (4) la gestión oficial de zonas horarias IANA y cambios de horario de verano (*DST*) mediante `zoneinfo.ZoneInfo` (**PEP 615**); y (5) el contraste con `time.perf_counter()` para mediciones monotónicas en producción.

## 11. Referencias oficiales

- <https://docs.python.org/3/library/datetime.html> — Biblioteca estándar (`datetime`): tipos `date`, `time`, `datetime`, `timedelta`, `timezone`, distinción *naive* frente a *aware* y tabla completa de directivas `strftime`/`strptime`.
- <https://docs.python.org/3/library/zoneinfo.html> — Biblioteca estándar (`zoneinfo`): soporte nativo de zonas horarias IANA (`ZoneInfo`) y consideraciones sobre transiciones *DST*.
- <https://docs.python.org/3/library/calendar.html> — Biblioteca estándar (`calendar`): funciones de calendario gregoriano como `isleap()` y `monthrange()`.
- <https://peps.python.org/pep-0615/> — PEP 615 (*Support for the IANA Time Zone Database in the Standard Library*): diseño e incorporación del módulo `zoneinfo` en Python 3.9.
