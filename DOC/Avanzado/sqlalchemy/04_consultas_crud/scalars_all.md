# SQLAlchemy: Consumo de Resultados (scalars, all, first, one_or_none)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
Result.scalars(index=0) -> ScalarResult
ScalarResult.all() -> Sequence[T]
ScalarResult.first() -> Optional[T]
ScalarResult.one() -> T
ScalarResult.one_or_none() -> Optional[T]
```

## 2. ¿Qué es?

`scalars()` transforma un `Result` compuesto por tuplas de base de datos en un `ScalarResult` que entrega directamente las entidades u objetos mapeados de la primera columna.

## 3. ¿Para qué sirve?

Provee los métodos idiomáticos para consumir el conjunto de resultados según la cardinalidad esperada de la consulta de negocio.

## 4. ¿Cómo funciona?

`scalars()` desenrolla la tupla de fila `(Usuario, )` extrayendo el objeto individual `Usuario`. `.all()` agota el cursor devolviendo una lista completa. `.first()` devuelve la primera fila o `None`. `.one()` garantiza que exista exactamente una fila (lanzando excepción si hay 0 o más de 1).

## 5. Parámetros

| Método | Retorno si hay 1 resultado | Retorno si hay 0 resultados | Retorno si hay 2+ resultados |
|---|---|---|---|
| `.all()` | `[Objeto]` (lista) | `[]` (lista vacía) | `[Objeto1, Objeto2, ...]` |
| `.first()` | `Objeto` | `None` | `Objeto1` (ignora el resto) |
| `.one()` | `Objeto` | Lanza `NoResultFound` | Lanza `MultipleResultsFound` |
| `.one_or_none()` | `Objeto` | `None` | Lanza `MultipleResultsFound` |

## 6. Retorno

`ScalarResult` o entidades individuales desempaquetadas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Producto(nombre="A"), Producto(nombre="B")])
    session.commit()

    # scalars().all() entrega lista directa de instancias Producto
    productos = session.scalars(select(Producto)).all()
    print(f"Tipo retornado: {type(productos).__name__}")
    print(f"Objetos extraídos: {[p.nombre for p in productos]}")

engine.dispose()
```

**Salida real:**

```text
Tipo retornado: list
Objetos extraídos: ['A', 'B']
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Config(Base):
    __tablename__ = "configs"
    clave: Mapped[str] = mapped_column(primary_key=True)
    valor: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Config(clave="modo", valor="produccion"))
    session.commit()

    # one_or_none() es ideal para búsquedas por clave única
    cfg = session.scalars(select(Config).where(Config.clave == "modo")).one_or_none()
    inexistente = session.scalars(select(Config).where(Config.clave == "tema")).one_or_none()

    print(f"Config existente: {cfg.valor}")
    print(f"Config inexistente retorna None seguro: {inexistente is None}")

engine.dispose()
```

**Salida real:**

```text
Config existente: produccion
Config inexistente retorna None seguro: True
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Registro(Base):
    __tablename__ = "registros"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Registro(nombre="R1"), Registro(nombre="R2")])
    session.commit()

    # session.scalar() es un atajo directo para session.scalars(...).first()
    primer_nombre = session.scalar(select(Registro.nombre).order_by(Registro.id))
    print(f"Atajo session.scalar(): {primer_nombre}")

engine.dispose()
```

**Salida real:**

```text
Atajo session.scalar(): R1
```

## 8. Errores frecuentes y casos borde

- **Olvidar `.scalars()` al consultar entidades completas:** `session.execute(select(Usuario)).all()` devuelve una lista de tuplas `[(Usuario, ), (Usuario, )]`. Para obtener directamente `[Usuario, Usuario]`, debe llamarse SIEMPRE `session.scalars(...)`.
- **Usar `.one()` cuando puede no haber resultados:** Si la consulta no encuentra coincidencias, `.one()` arroja una excepción `NoResultFound`. Usar `.one_or_none()` si la ausencia es un caso válido.

## 9. Buenas prácticas y rendimiento

- Usar `.one_or_none()` al buscar registros por clave primaria o índice único (ej. email, DNI).
- Usar `session.scalar(stmt)` como atajo conciso cuando se espere un único valor escalar.

## 10. Métodos relacionados

- [select_where](select_where.md)
- [session](../03_sesion_transacciones/session.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars
