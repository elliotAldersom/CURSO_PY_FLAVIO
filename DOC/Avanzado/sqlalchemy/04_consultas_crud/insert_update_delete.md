# SQLAlchemy: Mutaciones Masivas (insert, update, delete)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.insert(table_or_entity).values(**kwargs)
sqlalchemy.update(table_or_entity).where(*whereclause).values(**kwargs)
sqlalchemy.delete(table_or_entity).where(*whereclause)
```

## 2. ¿Qué es?

Constructores de sentencias DML (Data Manipulation Language) de SQLAlchemy 2.0 que ejecutan inserciones, actualizaciones y eliminaciones directas en la base de datos de manera masiva y vectorizada.

## 3. ¿Para qué sirve?

Resuelven la necesidad de actualizar o borrar miles de registros en una sola consulta relacional sin tener que cargar previamente los objetos a la memoria de la aplicación.

## 4. ¿Cómo funciona?

Generan las sentencias relacionales directas (`UPDATE tabla SET ... WHERE ...`). En SQLAlchemy 2.0, estas sentencias DML pueden ejecutarse directamente a través de `session.execute(stmt)`, sincronizando opcionalmente las instancias que ya estaban cargadas en el Identity Map de la sesión.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `table_or_entity` | `Table` o `Type[DeclarativeBase]` | Obligatorio | N/A | Entidad o tabla sobre la cual operar. |
| `values` | `dict` o `**kwargs` | Obligatorio (en insert/update) | N/A | Diccionario de pares columna-valor a asignar. |
| `where` | `BinaryExpression` | Obligatorio (en update/delete de seguridad) | N/A | Condición que delimita los registros a mutar. |

## 6. Retorno

`sqlalchemy.sql.dml.Insert | Update | Delete`. Sentencia DML ejecutable por la sesión.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    precio: Mapped[float]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Producto(nombre="P1", precio=10.0), Producto(nombre="P2", precio=20.0)])
    session.commit()

    # Actualización masiva directa en base de datos sin cargar objetos a memoria
    stmt = update(Producto).where(Producto.precio < 15.0).values(precio=12.5)
    session.execute(stmt)
    session.commit()

    nuevo_precio = session.scalar(select(Producto.precio).where(Producto.nombre == "P1"))
    print(f"Nuevo precio actualizado en bloque: {nuevo_precio}")

engine.dispose()
```

**Salida real:**

```text
Nuevo precio actualizado en bloque: 12.5
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Mensaje(Base):
    __tablename__ = "mensajes"
    id: Mapped[int] = mapped_column(primary_key=True)
    leido: Mapped[bool]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Mensaje(leido=True), Mensaje(leido=False), Mensaje(leido=True)])
    session.commit()

    # Eliminación masiva con delete
    stmt = delete(Mensaje).where(Mensaje.leido == True)
    resultado = session.execute(stmt)
    session.commit()

    print(f"Total registros eliminados (rowcount): {resultado.rowcount}")
    print(f"Restantes en base de datos: {len(session.scalars(select(Mensaje)).all())}")

engine.dispose()
```

**Salida real:**

```text
Total registros eliminados (rowcount): 2
Restantes en base de datos: 1
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Log(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    mensaje: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    # Inserción masiva de alto rendimiento con insert().values(...)
    datos = [{"mensaje": f"Evento #{i}"} for i in range(1, 4)]
    session.execute(insert(Log), datos)
    session.commit()

    total = session.scalar(select(Log).count()) if hasattr(select(Log), 'count') else len(session.scalars(select(Log)).all())
    print(f"Registros insertados masivamente: {total}")

engine.dispose()
```

**Salida real:**

```text
Registros insertados masivamente: 3
```

## 8. Errores frecuentes y casos borde

- **Ejecutar `update()` o `delete()` sin cláusula `where()`:** Omite la condición de filtrado y modifica o borra la tabla ENTERA de forma irreversible.
- **Inconsistencias con objetos ya cargados en sesión:** Si una entidad ya estaba cargada en memoria, un `update()` masivo directo modifica la base de datos pero no la instancia de Python a menos que se configure la sincronización de sesión.

## 9. Buenas prácticas y rendimiento

- Preferir `update()` masivo directo sobre consultas de actualización en bucles `for p in session.scalars(...): p.precio = ...`.
- Consultar siempre `resultado.rowcount` para verificar la cantidad exacta de filas afectadas.

## 10. Métodos relacionados

- [select_where](select_where.md)
- [session_commit_rollback](../03_sesion_transacciones/session_commit_rollback.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html
