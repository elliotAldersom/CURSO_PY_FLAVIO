# SQLAlchemy: Construcción de Consultas (select, where, order_by)

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.select(*entities)
Select.where(*whereclause)
Select.order_by(*clauses)
```

## 2. ¿Qué es?

`select()` es el constructor declarativo de sentencias SQL de lectura en SQLAlchemy 2.0, que se complementa con cláusulas de filtrado (`where`), ordenamiento (`order_by`), agrupamiento y límites.

## 3. ¿Para qué sirve?

Reemplaza por completo al método `session.query()` obsoleto, proporcionando una interfaz tipada y uniforme tanto para consultas directas en Core como para entidades del ORM.

## 4. ¿Cómo funciona?

Construye un objeto `Select` inmutable que representa el árbol de sintaxis abstracta (AST) de la consulta SQL. Cada llamada a `.where()` o `.order_by()` devuelve una nueva instancia de `Select` refinada que se compila a la sintaxis del motor configurado.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `*entities` | `Type` o `ColumnElement` | Obligatorio | N/A | Entidad completa mapeada (ej. `Usuario`) o columnas específicas. |
| `*whereclause` | `BinaryExpression` | Opcional | N/A | Condiciones booleanas de filtrado (combinadas por defecto con `AND`). |
| `*clauses` | `ColumnElement` o `UnaryExpression` | Opcional | N/A | Columnas por las cuales ordenar (ej. `Usuario.nombre.desc()`). |

## 6. Retorno

`sqlalchemy.sql.Select`. Objeto de sentencia ejecutable por la sesión.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import select, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    saldo: Mapped[float]

# Construcción de la sentencia select declarativa
stmt = select(Cliente).where(Cliente.saldo > 100.0).order_by(desc(Cliente.saldo))
print(f"Sentencia compilada:\n{stmt}")
```

**Salida real:**

```text
Sentencia compilada:
SELECT clientes.id, clientes.nombre, clientes.saldo 
FROM clientes 
WHERE clientes.saldo > :saldo_1 ORDER BY clientes.saldo DESC
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True)
    categoria: Mapped[str]
    precio: Mapped[float]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([
        Producto(categoria="A", precio=10.0),
        Producto(categoria="B", precio=50.0),
        Producto(categoria="C", precio=100.0)
    ])
    session.commit()

    # Combinación lógica con operador OR explícito
    consulta = select(Producto).where(or_(Producto.categoria == "A", Producto.precio >= 100.0))
    items = session.scalars(consulta).all()

    print(f"Total encontrados con OR: {len(items)}")
engine.dispose()
```

**Salida real:**

```text
Total encontrados con OR: 2
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
    valor: Mapped[int]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Registro(valor=i) for i in range(20)])
    session.commit()

    # Paginación canónica en base de datos con limit y offset
    paginacion = select(Registro).order_by(Registro.id).limit(5).offset(10)
    lote = session.scalars(paginacion).all()

    print(f"IDs del lote paginado (offset 10, limit 5): {[r.id for r in lote]}")
engine.dispose()
```

**Salida real:**

```text
IDs del lote paginado (offset 10, limit 5): [11, 12, 13, 14, 15]
```

## 8. Errores frecuentes y casos borde

- **Usar operadores lógicos de Python `and` / `or` en el `where`:** Escribir `where(CondicionA and CondicionB)` evalúa la expresión booleana en Python inmediatamente, no en SQL. En SQLAlchemy usar comas separadas `where(CondA, CondB)` para AND, o `or_(CondA, CondB)` para OR.
- **Usar `is` en lugar de `==` para comparar columnas:** Escribir `where(Usuario.nombre is None)` evalúa la identidad de Python. Usar `where(Usuario.nombre == None)` o el operador semántico `Usuario.nombre.is_(None)`.

## 9. Buenas prácticas y rendimiento

- Pasar múltiples argumentos a `where()`: `where(Cond1, Cond2)` se compila automáticamente como `Cond1 AND Cond2` de forma limpia.
- Utilizar siempre `.limit()` y `.offset()` para evitar desbordamientos de memoria al consultar tablas con millones de registros.

## 10. Métodos relacionados

- [scalars_all](scalars_all.md)
- [insert_update_delete](insert_update_delete.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
