# SQLAlchemy: Clase Session y sessionmaker

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.orm.Session(bind=None, *, autoflush=True, expire_on_commit=True, **kw)
sqlalchemy.orm.sessionmaker(bind=None, class_=Session, **kw)
```

## 2. ¿Qué es?

`Session` es el mediador principal entre los objetos en memoria de Python y la persistencia relacional en base de datos, implementando los patrones *Unit of Work* e *Identity Map*.

## 3. ¿Para qué sirve?

Garantiza la consistencia transaccional: asegura que un mismo registro de la base de datos esté representado por exactamente una única instancia de objeto en memoria, evitando lecturas sucias y conflictos de estado.

## 4. ¿Cómo funciona?

Rastrea las operaciones sobre entidades (`add`, `delete`). Cuando se requiere sincronizar o se invoca `commit()`, calcula automáticamente el conjunto mínimo de sentencias SQL (`INSERT`, `UPDATE`, `DELETE`) necesarias y las ejecuta ordenadamente en la base de datos.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `bind` | `Engine` o `Connection` | Opcional | `None` | Motor o conexión sobre el cual opera la sesión. |
| `autoflush` | `bool` | Opcional | `True` | Emite automáticamente las mutaciones a la base de datos antes de ejecutar consultas. |
| `expire_on_commit` | `bool` | Opcional | `True` | Expira los atributos de los objetos tras el commit para forzar recarga en la siguiente lectura. |

## 6. Retorno

`Session`. Instancia de sesión lista para transaccionar.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///:memory:")

# Uso canónico como gestor de contexto
with Session(engine) as session:
    print(f"Sesión activa: {session.is_active}")
    print(f"Autoflush activado: {session.autoflush}")

engine.dispose()
```

**Salida real:**

```text
Sesión activa: True
Autoflush activado: True
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///:memory:")

# sessionmaker es la factoría reutilizable estándar para inyección de dependencias
FabricaSesiones = sessionmaker(bind=engine, expire_on_commit=False)

with FabricaSesiones() as session:
    print(f"Sesión generada por factory: {type(session).__name__}")
    print(f"Expire on commit: {session.expire_on_commit}")

engine.dispose()
```

**Salida real:**

```text
Sesión generada por factory: Session
Expire on commit: False
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    u1 = Usuario(id=1, nombre="Alexander")
    session.add(u1)
    session.commit()

    # Identity Map: dos consultas por ID retornan LA MISMA instancia en memoria
    u_a = session.get(Usuario, 1)
    u_b = session.get(Usuario, 1)
    print(f"¿Son exactamente el mismo objeto en memoria?: {u_a is u_b}")

engine.dispose()
```

**Salida real:**

```text
¿Son exactamente el mismo objeto en memoria?: True
```

## 8. Errores frecuentes y casos borde

- **`expire_on_commit=True` en FastAPI:** Tras llamar `commit()`, acceder a un atributo del modelo fuera de la sesión lanza un `DetachedInstanceError`. Configurar `sessionmaker(..., expire_on_commit=False)` en APIs web.
- **Compartir una sesión entre múltiples hilos concurrentes:** La `Session` de SQLAlchemy NO es segura para subprocesos múltiples (*not thread-safe*). Usar una sesión independiente por hilo o petición HTTP.

## 9. Buenas prácticas y rendimiento

- Utilizar siempre la sesión dentro de un bloque `with Session(engine) as session:` para garantizar que la conexión se devuelva al pool al terminar.
- Configurar `expire_on_commit=False` cuando se retornen objetos del ORM directamente a clientes o vistas fuera del alcance de la sesión.

## 10. Métodos relacionados

- [session_commit_rollback](session_commit_rollback.md)
- [create_engine](../01_motor_conexiones/create_engine.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/session_basics.html
