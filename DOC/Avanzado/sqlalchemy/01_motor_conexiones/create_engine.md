# SQLAlchemy: create_engine

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.create_engine(url, **kwargs)
```

## 2. ¿Qué es?

`create_engine` es la función factoría central que instancia el objeto `Engine`, el cual representa la conectividad física, el pool de conexiones y el dialecto de comunicación con la base de datos.

## 3. ¿Para qué sirve?

Actúa como el corazón de bajo nivel de toda la arquitectura de SQLAlchemy, coordinando la autenticación, la serialización de tipos y el reciclaje eficiente de sockets de red.

## 4. ¿Cómo funciona?

Interpreta la cadena de conexión URL (`driver://usuario:password@host/db`). No abre una conexión de inmediato (evaluación perezosa o lazy connect); inicializa el `Pool` y aguarda a que se solicite la primera operación para establecer el handshake de red.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `url` | `str` o `URL` | Obligatorio | N/A | Cadena URI de conexión (ej. `'sqlite:///:memory:'`, `'postgresql+psycopg://...'`). |
| `echo` | `bool` | Opcional | `False` | Si es `True`, registra todas las sentencias SQL emitidas en el logger de Python. |
| `pool_size` | `int` | Opcional | `5` | Número de conexiones persistentes mantenidas en el pool. |
| `max_overflow` | `int` | Opcional | `10` | Conexiones adicionales temporales permitidas por encima de `pool_size`. |
| `pool_pre_ping` | `bool` | Opcional | `False` | Prueba la vitalidad de la conexión emitiendo un ping antes de entregarla del pool. |

## 6. Retorno

`sqlalchemy.engine.Engine`. Instancia del motor de base de datos.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")
print(f"Tipo de objeto: {type(engine).__name__}")
print(f"Dialecto activo: {engine.dialect.name}")
print(f"Driver utilizado: {engine.driver}")
engine.dispose()
```

**Salida real:**

```text
Tipo de objeto: Engine
Dialecto activo: sqlite
Driver utilizado: pysqlite
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine

# Configuración de producción para alta concurrencia
engine = create_engine(
    "sqlite:///:memory:",
    echo=False,
    pool_pre_ping=True
)

print(f"Pool class: {engine.pool.__class__.__name__}")
engine.dispose()
```

**Salida real:**

```text
Pool class: StaticPool
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Construcción segura de URL sin concatenar credenciales en texto plano
db_url = URL.create(
    drivername="sqlite",
    database=":memory:"
)

engine = create_engine(db_url)
print(f"URL compilada de forma segura: {engine.url}")
engine.dispose()
```

**Salida real:**

```text
URL compilada de forma segura: sqlite:///:memory:
```

## 8. Errores frecuentes y casos borde

- **Crear múltiples instancias de `Engine` para la misma base de datos:** El motor debe ser un objeto singleton por aplicación. Instanciar un `Engine` en cada petición agota las conexiones del servidor de base de datos rápidamente.
- **Omitir `pool_pre_ping=True` en producción:** En arquitecturas en la nube (AWS RDS, GCP Cloud SQL), los balanceadores matan conexiones inactivas tras unos minutos; sin `pool_pre_ping`, la aplicación arrojará excepciones de conexión rota.

## 9. Buenas prácticas y rendimiento

- Instanciar el `engine` una única vez a nivel de módulo en la capa de infraestructura del proyecto.
- Utilizar siempre `URL.create()` para parametrizar contraseñas complejas que contengan caracteres especiales (como `@`, `:`, `/`).

## 10. Métodos relacionados

- [connection_execute](connection_execute.md)
- [session](../03_sesion_transacciones/session.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/core/engines.html
