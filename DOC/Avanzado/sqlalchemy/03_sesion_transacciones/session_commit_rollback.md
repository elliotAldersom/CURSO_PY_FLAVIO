# SQLAlchemy: Session.commit, rollback y flush

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
Session.commit()
Session.rollback()
Session.flush(objects=None)
```

## 2. ¿Qué es?

Métodos que controlan el ciclo de vida de la transacción en la sesión: confirmar cambios (`commit`), revertirlos ante un error (`rollback`) o enviarlos a la base de datos sin cerrar la transacción (`flush`).

## 3. ¿Para qué sirve?

Garantizan la integridad y atomicidad ACID del negocio: permiten consolidar operaciones múltiples o cancelar todo el lote si una regla falla a mitad de camino.

## 4. ¿Cómo funciona?

`flush()` emite las sentencias SQL pendientes (`INSERT`, `UPDATE`) a la base de datos, asignando claves primarias autoincrementables pero sin cerrar la transacción. `commit()` ejecuta un `flush()` previo y emite el comando SQL `COMMIT`. `rollback()` emite `ROLLBACK` y restaura los objetos en memoria a su estado previo.

## 5. Parámetros

| Método | Efecto en SQL | Efecto en Objetos de Memoria |
|---|---|---|
| `flush()` | Emite sentencias SQL pendientes; mantiene la transacción abierta. | Asigna IDs autoincrementables generados por la base de datos. |
| `commit()` | Emite `COMMIT` y cierra la transacción relacional actual. | Expira o preserva atributos según `expire_on_commit`. |
| `rollback()` | Emite `ROLLBACK` y descarta los cambios en la transacción. | Revierte los objetos en memoria eliminando instancias añadidas pendientes. |

## 6. Retorno

`None`. Muta el estado transaccional de la sesión.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    item = Item(nombre="Prueba Flush")
    session.add(item)
    print(f"ID antes del flush: {item.id}")

    # flush() envía el SQL a la base de datos y recupera el ID autogenerado
    session.flush()
    print(f"ID tras flush (sin hacer commit todavía): {item.id}")
    session.commit()

engine.dispose()
```

**Salida real:**

```text
ID antes del flush: None
ID tras flush (sin hacer commit todavía): 1
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Saldo(Base):
    __tablename__ = "saldos"
    id: Mapped[int] = mapped_column(primary_key=True)
    monto: Mapped[float]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(Saldo(monto=500.0))
    session.commit()

    try:
        # Modificación que fallará deliberadamente
        s = session.get(Saldo, 1)
        s.monto = -999.0
        raise ValueError("Operación inválida de negocio")
        session.commit()
    except ValueError:
        session.rollback()
        print("Rollback ejecutado limpiamente tras excepción")

    saldo_final = session.get(Saldo, 1).monto
    print(f"Saldo preservado intacto: {saldo_final}")

engine.dispose()
```

**Salida real:**

```text
Rollback ejecutado limpiamente tras excepción
Saldo preservado intacto: 500.0
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Tarea(Base):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

# with session.begin() ejecuta commit al finalizar o rollback si hay excepción
with Session(engine) as session:
    with session.begin():
        session.add(Tarea(titulo="Tarea Atómica Automática"))

with Session(engine) as session:
    total = len(session.query(Tarea).all()) if hasattr(session, 'query') else len(session.scalars(select(Tarea)).all())
    print("Transacción confirmada automáticamente por bloque begin()")

engine.dispose()
```

**Salida real:**

```text
Transacción confirmada automáticamente por bloque begin()
```

## 8. Errores frecuentes y casos borde

- **Llamar a `commit()` dentro de un bucle de miles de registros:** Hacer un commit por cada registro congela la aplicación debido a los tiempos de escritura en disco (fsync). Agrupar todas las inserciones con `session.add_all()` y hacer UN solo `commit()` al final.
- **Olvidar llamar a `rollback()` tras capturar una excepción:** Una sesión que experimentó un error SQL queda en estado 'inactivo/inválido'; intentar usarla sin llamar `rollback()` lanzará `PendingRollbackError`.

## 9. Buenas prácticas y rendimiento

- Usar `session.flush()` cuando necesites el ID recién generado de una entidad padre para asignarlo como clave foránea a entidades hijas antes de commitear.
- Preferir el gestor de transacciones `with session.begin():` para garantizar commits o rollbacks atómicos.

## 10. Métodos relacionados

- [session](session.md)
- [select_where](../04_consultas_crud/select_where.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
