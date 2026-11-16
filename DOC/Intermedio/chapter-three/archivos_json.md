# Serialización, Deserialización y Gestión de Datos JSON (`json`)

## 2. Introducción

En la ingeniería de software moderna, **JSON** (*JavaScript Object Notation*, formalizado en **RFC 8259** y **ECMA-404**) es el formato estándar de facto para el intercambio de información estructurada en la web, APIs REST, almacenamiento de configuraciones y persistencia ligera de datos entre sistemas heterogéneos.

La **biblioteca estándar de Python** incluye el módulo nativo `json`, el cual provee una interfaz robusta, determinista y de alto rendimiento para convertir estructuras de datos en memoria ([diccionarios](../chapter-one/diccionarios.md), [listas](../../Basico/chapter-two/listas.md), [cadenas](../../Basico/chapter-two/cadenas.md), números y booleanos) a su representación textual equivalente en JSON y viceversa.

Dominar la gestión de archivos JSON exige comprender con precisión la correspondencia biunívoca entre los tipos de datos de Python y JSON, la diferencia operativa entre flujos de texto en memoria (`dumps`/`loads`) y archivos en disco (`dump`/`load`), la extensión para serializar tipos complejos (como fechas, UUIDs o entidades de dominio) mediante `default` y `JSONEncoder`, y las prácticas de escritura atómica para prevenir la corrupción de datos ante cortes imprevistos del sistema.

## 3. Fundamentos y conceptos

**Serialización (*marshalling* / *encoding*) y Deserialización (*unmarshalling* / *decoding*).** El ciclo de vida de los datos articulado por el módulo `json` comprende dos transformaciones inversas:

1. **Serialización (Codificación):** traduce un grafo de objetos Python residentes en memoria a una secuencia de caracteres con formato JSON estándar.
2. **Deserialización (Decodificación):** analiza sintácticamente una cadena o archivo JSON y reconstruye las estructuras nativas equivalentes de Python.

**Tabla de correspondencia formal de tipos entre Python y JSON:**

| Tipo en Python | Tipo en JSON | Notas de serialización |
| :--- | :--- | :--- |
| `dict` | `object` | Las claves en JSON **deben ser siempre cadenas (`str`)**. Claves enteras en Python se convierten a cadenas al serializar. |
| `list`, `tuple` | `array` | Las tuplas de Python se convierten a arreglos JSON. Al deserializar, **ambos se reconstruyen siempre como `list`**. |
| `str` | `string` | Se codifica en UTF-8 con escape de caracteres especiales (`\n`, `\"`, `\\`). |
| `int`, `float` | `number` | JSON no distingue entre enteros y flotantes. Valores especiales `NaN`, `Infinity` y `-Infinity` violan el RFC 8259 estricto (aunque Python los admite por defecto mediante `allow_nan=True`). |
| `True` / `False` | `true` / `false` | Conversión booleana exacta en minúsculas. |
| `None` | `null` | Mapeo directo al valor nulo de JSON. |

> [!IMPORTANT]
> Tipos nativos de Python como `set`, `frozenset`, `bytes`, `complex`, `datetime` o instancias de clases personalizadas **no tienen equivalente directo en JSON** y disparan un `TypeError: Object of type ... is not JSON serializable` si se intentan serializar sin un codificador auxiliar.

**Flujos en memoria (`loads` / `dumps`) frente a flujos de archivos (`load` / `dump`).** La convención de la API del módulo `json` utiliza la letra final `s` (*string*) para distinguir el destino:

- `json.dumps(obj)`: serializa un objeto a un `str` en memoria.
- `json.loads(cadena_json)`: deserializa un `str` o `bytes` a un objeto Python.
- `json.dump(obj, fp)`: serializa el objeto escribiéndolo directamente en un archivo o flujo abierto en modo texto (`w`).
- `json.load(fp)`: lee un archivo o flujo abierto en modo texto (`r`) y deserializa su contenido.

**Persistencia atómica y prevención de corrupción.** Modificar un archivo JSON directamente con `open(ruta, "w")` presenta un riesgo arquitectónico grave: si el proceso se interrumpe durante la escritura (corte eléctrico, fallo de disco, excepción no capturada), el archivo previo queda truncado o destruido a mitad de camino, dejando datos corruptos irrecuperables. En sistemas de producción, la persistencia de configuraciones JSON debe realizarse mediante **escritura atómica**: escribir primero en un archivo temporal en el mismo sistema de archivos y reemplazar el archivo destino mediante un renombrado atómico (`os.replace` o `Path.replace`).

## 4. Sintaxis y funcionamiento

Firma y parámetros esenciales de `json.dumps` y `json.dump`:

```python
# Firma conceptual en la biblioteca estándar:
# def dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
#           allow_nan=True, indent=None, separators=None, default=None, sort_keys=False) -> str

# Invocación con los parámetros principales configurados:
import json

salida_ejemplo = json.dumps(
    {"clave": "valor"},
    skipkeys=False,        # Si True, ignora claves de dict que no sean tipos básicos en vez de lanzar TypeError
    ensure_ascii=True,     # Si True (defecto), escapa caracteres no ASCII como \uXXXX; si False, escribe Unicode directo
    check_circular=True,   # Previene referencias circulares en objetos
    allow_nan=True,        # Permite NaN e Infinity violando el estándar estricto
    indent=2,              # Entero que define espacios de sangría para formato legible (pretty-print)
    separators=(", ", ": "),  # Tupla (item_sep, key_sep) para formateo o compactación
    default=str,           # Invocable auxiliar para convertir tipos no soportados
    sort_keys=True,        # Si True, ordena las claves de los diccionarios alfabéticamente
)
```

Firma de `json.loads` y `json.load`:

```python
# Firma conceptual en la biblioteca estándar:
# def loads(s, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None) -> Any

# Invocación con interceptores personalizados:
import json

datos_cargados = json.loads(
    '{"precio": 99.5}',
    object_hook=None,          # Función opcional llamada con cada dict decodificado para construir entidades de dominio
    parse_float=float,         # Invocable alternativo para flotantes (p. ej. decimal.Decimal para finanzas)
    parse_int=int,             # Invocable alternativo para enteros
    parse_constant=None,       # Invocable para constantes no estándar (-Infinity, Infinity, NaN)
)
```

## 5. Ejemplos prácticos progresivos

### Básico

**Ejemplo 1 — Serialización y deserialización elemental en memoria y preservación de UTF-8.**

```python
import json

# Estructura de datos en memoria con tipos mixtos
datos_usuario = {
    "id": 101,
    "nombre": "Flavio Estrada",
    "activo": True,
    "roles": ["administrador", "docente"],
    "calificaciones": {"python": 9.8, "sql": 10.0},
    "contacto_emergencia": None,
}

# 1. Serialización a cadena compacta
cadena_compacta = json.dumps(datos_usuario, separators=(",", ":"))

# 2. Serialización legible (pretty-print) con caracteres Unicode directos (sin \uXXXX)
cadena_legible = json.dumps(datos_usuario, indent=2, ensure_ascii=False)

# 3. Deserialización de vuelta a Python
objeto_reconstruido = json.loads(cadena_legible)

print("Longitud de cadena compacta :", len(cadena_compacta))
print("Equivalencia tras ida/vuelta:", objeto_reconstruido == datos_usuario)
print("Tipo reconstruido de roles  :", type(objeto_reconstruido["roles"]).__name__)
print("Primer rol recuperado       :", objeto_reconstruido["roles"][0])
```

Explicación paso a paso:

- `json.dumps(..., separators=(',', ':'))` elimina todos los espacios en blanco innecesarios, minimizando los bytes a transmitir por red.
- `ensure_ascii=False` asegura que caracteres acentuados como `ó` en "emergencia" no se codifiquen artificialmente como secuencias de escape `\u00f3`, reduciendo el tamaño y facilitando la lectura humana.
- `json.loads` analiza el texto JSON y reconstruye fielmente el diccionario, manteniendo `roles` como una lista mutable (`list`) y `contacto_emergencia` como `None`.

Resultado esperado:

```text
Longitud de cadena compacta : 138
Equivalencia tras ida/vuelta: True
Tipo reconstruido de roles  : list
Primer rol recuperado       : administrador
```

### Intermedio

**Ejemplo 2 — Lectura, escritura atómica y persistencia en disco con `pathlib.Path`.**

```python
import json
import os
import tempfile
from pathlib import Path


def guardar_json_atomico(ruta_destino: Path, contenido: dict) -> None:
    """Escribe un archivo JSON de forma atómica garantizando que nunca quede a medio escribir."""
    # 1. Asegurar la existencia del directorio contenedor
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    # 2. Crear un archivo temporal en el mismo directorio para permitir renombrado atómico en el mismo FS
    directorio = str(ruta_destino.parent)
    descriptor, ruta_temporal = tempfile.mkstemp(dir=directorio, prefix=".tmp_json_")

    try:
        with open(descriptor, mode="w", encoding="utf-8") as f:
            json.dump(contenido, f, indent=2, ensure_ascii=False, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())  # Forzar descarga física a disco antes de renombrar
        # 3. Reemplazo atómico garantizado por el sistema operativo
        os.replace(ruta_temporal, ruta_destino)
    except Exception:
        # En caso de error, limpiar el temporal sin alterar el archivo original
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        raise


def leer_json_seguro(ruta: Path) -> dict:
    """Lee y deserializa un archivo JSON validando codificación UTF-8."""
    if not ruta.is_file():
        raise FileNotFoundError(f"El archivo {ruta} no existe")
    with open(ruta, mode="r", encoding="utf-8") as f:
        return json.load(f)


# Demostración práctica
with tempfile.TemporaryDirectory() as temp_dir:
    archivo_config = Path(temp_dir) / "configuracion" / "sistema.json"
    configuracion_inicial = {
        "version": "2.4.0",
        "ambiente": "produccion",
        "timeout_segundos": 30,
        "puertos_habilitados": [8080, 8443],
    }

    guardar_json_atomico(archivo_config, configuracion_inicial)
    datos_leidos = leer_json_seguro(archivo_config)

    print("Archivo creado en disco  :", archivo_config.exists())
    print("Versión leída            :", datos_leidos["version"])
    print("Puertos cargados         :", datos_leidos["puertos_habilitados"])
    print("Verificación de igualdad :", datos_leidos == configuracion_inicial)
```

Explicación técnica:

- Se utiliza `tempfile.mkstemp` en el mismo directorio (`ruta_destino.parent`) para asegurar que el archivo temporal y el archivo final residan en la misma partición del sistema de archivos, condición obligatoria para que `os.replace()` ejecute una operación atómica de puntero sin copias físicas intermedias.
- `os.fsync(f.fileno())` fuerza la sincronización de los búferes del sistema operativo hacia el medio de almacenamiento magnético o de estado sólido antes del renombrado.
- La lectura se ejecuta especificando explícitamente `encoding="utf-8"`, evitando fallos de codificación en entornos donde la configuración regional del sistema no coincida con el estándar.

Resultado esperado:

```text
Archivo creado en disco  : True
Versión leída            : 2.4.0
Puertos cargados         : [8080, 8443]
Verificación de igualdad : True
```

### Avanzado

**Ejemplo 3 — Serializador extensible con `default` y deserializador de dominio con `object_hook` y precisión decimal (`decimal.Decimal`).**

```python
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
import json
import uuid


@dataclass(frozen=True)
class Transaccion:
    id_transaccion: uuid.UUID
    marca_tiempo: datetime
    importe: Decimal
    concepto: str


def serializador_personalizado(obj: object) -> object:
    """Transforma tipos no estándar de Python a representaciones compatibles con JSON."""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        # En sistemas financieros el importe se serializa como cadena para preservar precisión exacta
        return str(obj)
    if isinstance(obj, Transaccion):
        payload = asdict(obj)
        payload["__tipo__"] = "Transaccion"
        return payload
    raise TypeError(f"El objeto de tipo {type(obj).__name__} no es serializable en JSON")


def decodificador_transaccion(d: dict) -> object:
    """Reconstruye entidades de dominio Transaccion al encontrar la marca __tipo__."""
    if d.get("__tipo__") == "Transaccion":
        return Transaccion(
            id_transaccion=uuid.UUID(d["id_transaccion"]),
            marca_tiempo=datetime.fromisoformat(d["marca_tiempo"]),
            importe=Decimal(d["importe"]),
            concepto=d["concepto"],
        )
    return d


# 1. Creación de la entidad original
registro = Transaccion(
    id_transaccion=uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890"),
    marca_tiempo=datetime(2025, 5, 10, 14, 30, tzinfo=timezone.utc),
    importe=Decimal("1549.99"),
    concepto="Licencia Anual Cloud",
)

# 2. Serialización con default y ordenamiento
json_serializado = json.dumps(
    registro,
    default=serializador_personalizado,
    indent=2,
    sort_keys=True,
)

# 3. Deserialización recuperando la entidad Transaccion con object_hook
registro_reconstruido: Transaccion = json.loads(
    json_serializado,
    object_hook=decodificador_transaccion,
)

print("JSON resultante:\n" + json_serializado)
print("Tipo reconstruido   :", type(registro_reconstruido).__name__)
print("Importe como Decimal:", type(registro_reconstruido.importe).__name__, registro_reconstruido.importe)
print("Fecha como datetime :", type(registro_reconstruido.marca_tiempo).__name__, registro_reconstruido.marca_tiempo)
print("Equivalencia total  :", registro == registro_reconstruido)
```

Explicación de ingeniería:

- El argumento `default=serializador_personalizado` intercepta cualquier objeto que el serializador nativo no reconozca. Transforma instancias `UUID` a cadenas canónicas, marcas temporales `datetime` al estándar internacional ISO 8601 (`YYYY-MM-DDTHH:MM:SS+00:00`) y números de precisión fija [decimal.Decimal](../chapter-four/decimal.md) a cadenas para evitar la pérdida de centavos inherente a los flotantes binarios IEEE 754 de JSON.
- Al deserializar, el parámetro `object_hook` inspecciona cada diccionario devuelto por el parser sintáctico. Al detectar la etiqueta semántica `'__tipo__': 'Transaccion'`, rehidrata automáticamente la instancia inmutable de la clase `Transaccion`, convirtiendo la carga textual cruda en una entidad de dominio fuertemente tipada.

Resultado esperado:

```text
JSON resultante:
{
  "__tipo__": "Transaccion",
  "concepto": "Licencia Anual Cloud",
  "id_transaccion": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "importe": "1549.99",
  "marca_tiempo": "2025-05-10T14:30:00+00:00"
}
Tipo reconstruido   : Transaccion
Importe como Decimal: Decimal 1549.99
Fecha como datetime : datetime 2025-05-10 14:30:00+00:00
Equivalencia total  : True
```

## 6. Aplicaciones en el mundo real

- **APIs Web y Microservicios:** carga y envío de cargas útiles (*payloads*) en solicitudes y respuestas HTTP REST con frameworks como FastAPI, Flask o Django REST Framework.
- **Archivos de configuración de infraestructura:** definición de manifiestos, archivos de configuración de despliegue (`package.json`, `launch.json`, políticas IAM de AWS).
- **Bases de datos de documentos y almacenamiento semiestructurado:** indexación y consulta en motores NoSQL como MongoDB, CouchDB, o columnas tipo `JSONB` en PostgreSQL.
- **Persistencia de telemetría y registros estructurados (*Structured Logging*):** exportación de eventos de aplicación en formato JSON por línea (*JSON Lines* o `.jsonl`) para ingesta en plataformas de análisis como Elasticsearch, Grafana Loki o Datadog.
- **Intercambio entre lenguajes y microservicios políglotas:** mediación de datos sin pérdida de fidelidad semántica entre componentes construidos en Python, Go, Rust, Java y JavaScript.

## 7. Uso en producción

- **Especificar siempre `encoding="utf-8"`:** nunca omitir el parámetro de codificación al abrir archivos (`open(ruta, "r", encoding="utf-8")`), pues en sistemas Windows la codificación predeterminada suele ser `cp1252`, lo que produce fallos `UnicodeDecodeError` ante cualquier carácter no anglosajón.
- **Implementar persistencia atómica en archivos críticos:** configuraciones o catálogos modificados dinámicamente deben escribirse primero en un temporal del mismo directorio y luego reemplazarse con `os.replace` para evitar truncamiento por caídas de proceso.
- **Protegerse contra deserialización de entradas masivas no confiables:** `json.loads` materializa todo el documento en memoria RAM antes de retornar; analizar archivos de varios gigabytes de una sola vez puede desencadenar errores de falta de memoria (*OOM*). En tales escenarios debe utilizarse lectura por lotes o el formato JSON Lines (`.jsonl`), donde cada línea es un objeto JSON independiente procesable en streaming.
- **Evitar flotantes binarios en montos monetarios:** serializar importes financieros siempre como cadenas (`"1549.99"`) o enteros de centavos (`154999`) y reconstruirlos con `decimal.Decimal` para garantizar precisión contable.

## 8. Errores comunes y recomendaciones

1. **Intentar serializar tipos no compatibles directamente (`TypeError`).**

```python
from datetime import datetime
import json

evento = {"nombre": "Despliegue", "fecha": datetime.now()}

# ERROR: TypeError: Object of type datetime is not JSON serializable
# json.dumps(evento)
```

Diagnóstico: JSON no tiene tipo nativo para fechas ni binarios. Recomendación: suministrar un formateador mediante `default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)`.

2. **Asumir que las claves numéricas de un diccionario se conservan como enteros tras la deserialización.**

```python
import json

inventario = {1: "teclado", 2: "ratón"}
json_texto = json.dumps(inventario)
recuperado = json.loads(json_texto)

print("Tipo de clave recuperada:", type(list(recuperado.keys())[0]))
# Imprime: <class 'str'>
# inventario[1] funciona, pero recuperado[1] lanza KeyError; debe usarse recuperado["1"]
```

Diagnóstico: el estándar ECMA-404 exige taxativamente que todas las claves de un objeto JSON sean cadenas de caracteres. Durante `dumps`, Python convierte silenciosamente las claves `1` y `2` a `"1"` y `"2"`. Recomendación: si se necesitan claves enteras tras deserializar, transformarlas explícitamente (`{int(k): v for k, v in recuperado.items()}`).

3. **Sobrescribir archivos JSON directamente con `open(..., "w")` perdiendo el contenido ante un fallo intermedio.**

Diagnóstico: abrir en modo `"w"` trunca el archivo a longitud cero antes de comenzar a escribir; si ocurre una excepción antes de que termine `dump()`, el archivo original se pierde irremediablemente. Recomendación: utilizar el patrón de reemplazo atómico mediante `mkstemp` y `os.replace` demostrado en la sección de ejemplos.

## 9. Resumen

- El formato **JSON** (**RFC 8259**) es el estándar universal para el intercambio de datos estructurados, gobernado en Python por el módulo integrado `json`.
- La función `dumps` y su contraparte `loads` operan sobre cadenas en memoria, mientras que `dump` y `load` procesan flujos de archivos abiertos en modo texto con codificación explícita `utf-8`.
- El mapeo de tipos traduce diccionarios a objetos, listas y tuplas a arreglos, enteros y flotantes a números, booleanos a `true`/`false`, y `None` a `null`.
- Tipos complejos (`datetime`, `UUID`, `Decimal`, clases de usuario) se serializan mediante el parámetro `default` y se reconstruyen de forma fuertemente tipada mediante `object_hook`.
- Para prevenir la corrupción catastrófica de configuraciones en producción, la persistencia en disco debe implementarse de forma atómica escribiendo en archivos temporales y ejecutando un reemplazo atómico a nivel de sistema de archivos.

## 10. Referencias oficiales

- <https://docs.python.org/3/library/json.html> — Biblioteca estándar (`json`): especificación de codificadores, decodificadores y funciones de conveniencia `dump`, `dumps`, `load` y `loads`.
- <https://datatracker.ietf.org/doc/html/rfc8259> — RFC 8259 (*The JavaScript Object Notation (JSON) Data Interchange Format*): estándar internacional de especificación sintáctica de JSON.
- <https://docs.python.org/3/library/os.html#os.replace> — Biblioteca estándar (`os.replace`): semántica de renombrado atómico en sistemas POSIX y Windows.
- <https://docs.python.org/3/library/decimal.html> — Biblioteca estándar (`decimal`): aritmética de punto fijo y flotante de precisión exacta para valores numéricos en JSON.
