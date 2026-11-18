# Fundamentos de SQLAlchemy 2.0: Arquitectura de Persistencia Relacional y ORM Tipado en Python

SQLAlchemy es el toolkit SQL y Object Relational Mapper (ORM) canónico del ecosistema Python para persistencia relacional empresarial, desarrollado y mantenido por Mike Bayer.

## 2. Introducción

Antes de la llegada de SQLAlchemy 2.0 (lanzado en 2023), coexistían dos filosofías divergentes en la biblioteca: el estilo imperativo heredado de SQLAlchemy 1.x (con métodos fluidos como `session.query(Usuario).filter(...)`) y la nueva filosofía declarativa tipada alineada con PEP 484.

SQLAlchemy 2.0 unificó la arquitectura desterrando el antiguo `Query` y adoptando un modelo homogéneo centrado en constructores de sentencias SQL puras (`select()`, `insert()`, `update()`, `delete()`), anotaciones de tipo nativas (`Mapped[...]`, `mapped_column()`) y compatibilidad total con controladores asíncronos (`AsyncEngine`, `AsyncSession` con `asyncpg` y `aiosqlite`).

## 3. Fundamentos y conceptos

La arquitectura de SQLAlchemy se divide limpiamente en dos capas ortogonales:
1. **SQLAlchemy Core (Capa de Infraestructura y Metadatos):**
   - El Motor (`Engine`): Fábrica de conexiones a bajo nivel que administra el pool de conexiones (`QueuePool`) y la traducción al dialecto SQL específico (PostgreSQL, MySQL, SQLite, Oracle).
   - Lenguaje de Expresión SQL: Representación abstracta programática e independiente del motor para construir sentencias SQL complejas sin concatenar cadenas de texto vulnerables a inyección SQL.
2. **SQLAlchemy ORM (Capa de Mapeo Objeto-Relacional):**
   - Base Declarativa (`DeclarativeBase`): Superclase de la cual heredan las entidades del dominio de negocio.
   - Sesión (`Session`): Implementación del patrón *Unit of Work* e *Identity Map*, encargada de rastrear mutaciones de objetos en memoria y sincronizarlas de forma atómica y transaccional con la base de datos (`flush()` y `commit()`).

## 4. Sintaxis y funcionamiento

El patrón idiomático innegociable de SQLAlchemy 2.0 se fundamenta en la sentencia contextual `select()` y `session.scalars()`:

```python
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Usuario(nombre="Alexander"))
    session.commit()

    # Consulta canónica 2.0
    sentencia = select(Usuario).where(Usuario.nombre == "Alexander")
    usuario_encontrado = session.scalars(sentencia).one()
```

## 5. Ejemplos prácticos progresivos

### Básico

Conexión directa mediante Core y ejecución de SQL parametrizado seguro contra inyecciones.

```python
from sqlalchemy import create_engine, text

# Motor en memoria SQLite
motor = create_engine("sqlite:///:memory:")

with motor.connect() as conexion:
    conexion.execute(text("CREATE TABLE auditoria (id INT, evento TEXT)"))
    conexion.execute(
        text("INSERT INTO auditoria (id, evento) VALUES (:id, :evento)"),
        [{"id": 1, "evento": "LOGIN"}, {"id": 2, "evento": "LOGOUT"}]
    )
    conexion.commit()

    resultado = conexion.execute(text("SELECT id, evento FROM auditoria ORDER BY id"))
    filas = resultado.fetchall()

print(f"Filas recuperadas con Core: {filas}")
motor.dispose()
```

**Salida real:**

```text
Filas recuperadas con Core: [(1, 'LOGIN'), (2, 'LOGOUT')]
```

### Intermedio

Modelado ORM completo con `DeclarativeBase`, anotaciones tipadas `Mapped` e inserción transaccional.

```python
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40))
    precio: Mapped[float]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([
        Producto(nombre="Teclado", precio=120.0),
        Producto(nombre="Mouse", precio=45.0)
    ])
    session.commit()

    # Filtrado canónico con select y where
    stmt = select(Producto).where(Producto.precio > 50.0)
    resultado = session.scalars(stmt).all()

    print(f"Total productos filtrados: {len(resultado)}")
    print(f"Producto caro: {resultado[0].nombre} - ${resultado[0].precio}")
engine.dispose()
```

**Salida real:**

```text
Total productos filtrados: 1
Producto caro: Teclado - $120.0
```

### Avanzado

Relación uno a muchos (1:N) con clave foránea, `relationship` bidireccional y carga ansiosa (*Joined Eager Loading*).

```python
from typing import List
from sqlalchemy import create_engine, select, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, joinedload

class Base(DeclarativeBase):
    pass

class Autor(Base):
    __tablename__ = "autores"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    libros: Mapped[List["Libro"]] = relationship(back_populates="autor")

class Libro(Base):
    __tablename__ = "libros"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"))
    autor: Mapped["Autor"] = relationship(back_populates="libros")

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    autor = Autor(nombre="Gabriel García Márquez")
    autor.libros.append(Libro(titulo="Cien años de soledad"))
    session.add(autor)
    session.commit()

    # Consulta con joinedload para evitar el problema de N+1 consultas
    stmt = select(Autor).options(joinedload(Autor.libros)).where(Autor.nombre.like("%Márquez%"))
    autor_db = session.scalars(stmt).unique().one()

    print(f"Autor recuperado: {autor_db.nombre}")
    print(f"Libros asociados cargados sin N+1: {[l.titulo for l in autor_db.libros]}")
engine.dispose()
```

**Salida real:**

```text
Autor recuperado: Gabriel García Márquez
Libros asociados cargados sin N+1: ['Cien años de soledad']
```

## 6. Aplicaciones en el mundo real

- **Capa de Persistencia en Microservicios FastAPI:** Integración nativa asíncrona para backend REST y GraphQL con validación de modelos Pydantic y pooling de conexiones.
- **Sistemas Transaccionales Financieros:** Gestión estricta de aislamiento ACID mediante transacciones atómicas con control de concurrencia optimista o pesimista (`with_for_update()`).
- **Migraciones de Esquema de Base de Datos:** Base fundamental sobre la cual opera **Alembic** para versionar, generar y aplicar migraciones DDL automáticas en producción.

## 7. Uso en producción

- **Dimensionamiento del Connection Pool:** En producción con PostgreSQL, configurar explícitamente `create_engine(..., pool_size=20, max_overflow=10, pool_pre_ping=True)`. El parámetro `pool_pre_ping=True` comprueba la vitalidad de la conexión antes de entregarla, evitando caídas por conexiones muertas cerradas por el firewall.
- **Prevención de N+1 Queries:** Nunca iterar relaciones perezosas (*lazy loading*) en bucles dentro de serializadores de APIs. Configurar siempre carga explícita mediante `joinedload()` o `selectinload()`.
- **Modo Asíncrono con AsyncSession:** En aplicaciones asíncronas con FastAPI, usar `create_async_engine()` con drivers como `asyncpg` para no bloquear el bucle de eventos.

## 8. Errores comunes y recomendaciones

- **Usar la API obsoleta 1.x:** `session.query(Usuario).filter(...)` está deprecada en SQLAlchemy 2.0. El estándar innegociable es construir sentencias con `select(Usuario).where(...)`.
- **Concatenar cadenas SQL:** Escribir `f"SELECT * FROM u WHERE id = {user_id}"` abre la puerta a inyecciones SQL letales. Usar siempre parámetros vinculados con `text("... WHERE id = :id")` o constructores tipados de Core.
- **Mantener sesiones abiertas indefinidamente:** No cerrar o commitear sesiones retiene conexiones del pool y bloqueos de tablas en la base de datos. Usar siempre el gestor de contexto `with Session(engine) as session:`.

## 9. Resumen

SQLAlchemy 2.0 representa la cúspide de la persistencia relacional en Python al unificar un control de bajo nivel absoluto sobre SQL mediante Core con la expresividad y seguridad de tipos de un ORM moderno basado en `Mapped` y `select()`. Su integración con Alembic y FastAPI constituye el estándar arquitectónico indiscutible para aplicaciones empresariales.

## 10. Referencias oficiales

- Documentación oficial de SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
- Guía de migración a SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html
- Tutorial oficial de SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/tutorial/index.html
