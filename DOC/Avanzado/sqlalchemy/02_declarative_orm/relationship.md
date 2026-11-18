# SQLAlchemy: relationship y Mapeo de Relaciones

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.orm.relationship(argument=None, secondary=None, *, primaryjoin=None, secondaryjoin=None, foreign_keys=None, uselist=None, order_by=False, back_populates=None, backref=None, post_update=False, cascade=False, lazy='select', **kw)
```

## 2. ¿Qué es?

`relationship` define una relación semántica orientada a objetos entre dos clases mapeadas (1:1, 1:N o N:M), permitiendo navegar colecciones e instancias asociadas a través de atributos en Python.

## 3. ¿Para qué sirve?

Resuelve el problema de interactuar con claves foráneas relacionales mediante objetos nativos de Python, automatizando la carga y persistencia en cascada de entidades vinculadas.

## 4. ¿Cómo funciona?

Inspecciona las claves foráneas (`ForeignKey`) existentes en los metadatos de las tablas. Al asignar o acceder al atributo (ej. `autor.libros`), SQLAlchemy orquesta la sincronización de IDs relacionales y ejecuta las consultas de carga según la estrategia configurada (`lazy`).

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `argument` | `str` o `Type` | Opcional | N/A | Clase mapeada de destino de la relación. |
| `back_populates` | `str` | Opcional | `None` | Nombre del atributo en la clase destino para sincronización bidireccional estricta. |
| `cascade` | `str` | Opcional | `'save-update, merge'` | Reglas de cascada (ej. `'all, delete-orphan'` para borrado de hijos huérfanos). |
| `lazy` | `str` | Opcional | `'select'` | Estrategia de carga (`'select'`, `'joined'`, `'selectin'`, `'raise'`). |
| `secondary` | `Table` o `str` | Opcional | `None` | Tabla asociativa intermedia para relaciones de muchos a muchos (N:M). |

## 6. Retorno

`Relationship`. Descriptor de relación entre entidades.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Padre(Base):
    __tablename__ = "padres"
    id: Mapped[int] = mapped_column(primary_key=True)
    hijos: Mapped[List["Hijo"]] = relationship(back_populates="padre")

class Hijo(Base):
    __tablename__ = "hijos"
    id: Mapped[int] = mapped_column(primary_key=True)
    padre_id: Mapped[int] = mapped_column(ForeignKey("padres.id"))
    padre: Mapped["Padre"] = relationship(back_populates="hijos")

print(f"Relación Padre -> Hijos uselist: {Padre.hijos.property.uselist}")
print(f"Relación Hijo -> Padre uselist: {Hijo.padre.property.uselist}")
```

**Salida real:**

```text
Relación Padre -> Hijos uselist: True
Relación Hijo -> Padre uselist: False
```

### Nivel 2: Intermedio

```python
from typing import List
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Factura(Base):
    __tablename__ = "facturas"
    id: Mapped[int] = mapped_column(primary_key=True)
    # cascade='all, delete-orphan' borra los ítems al borrar la factura
    items: Mapped[List["ItemFactura"]] = relationship(cascade="all, delete-orphan")

class ItemFactura(Base):
    __tablename__ = "items_factura"
    id: Mapped[int] = mapped_column(primary_key=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("facturas.id"))
    monto: Mapped[float]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    f = Factura(items=[ItemFactura(monto=100.0), ItemFactura(monto=250.0)])
    session.add(f)
    session.commit()
    print(f"Factura guardada con {len(f.items)} ítems en cascada")
engine.dispose()
```

**Salida real:**

```text
Factura guardada con 2 ítems en cascada
```

### Nivel 3: Avanzado

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# lazy='raise' previene consultas N+1 accidentales arrojando error si no se hizo eager load
class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    articulos: Mapped[list["Articulo"]] = relationship(lazy="raise")

class Articulo(Base):
    __tablename__ = "articulos"
    id: Mapped[int] = mapped_column(primary_key=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))

print(f"Estrategia de carga de artículos: {Categoria.articulos.property.lazy}")
```

**Salida real:**

```text
Estrategia de carga de artículos: raise
```

## 8. Errores frecuentes y casos borde

- **Usar el viejo `backref` en lugar de `back_populates`:** `backref` creaba atributos mágicos implícitos sin tipado. En SQLAlchemy 2.0 usar SIEMPRE `back_populates` explícito en ambas clases.
- **El problema N+1:** Acceder a `autor.libros` en un bucle de 100 autores emite 101 consultas a la base de datos si se usa la carga perezosa por defecto. Usar `joinedload` o `selectinload`.

## 9. Buenas prácticas y rendimiento

- Configurar `cascade='all, delete-orphan'` en entidades hijas que no tengan existencia de negocio sin su padre.
- Usar `lazy='raise'` en APIs asíncronas para obligar a los desarrolladores a especificar la carga ansiosa explícitamente en la consulta.

## 10. Métodos relacionados

- [mapped_column](mapped_column.md)
- [declarative_base](declarative_base.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/relationships.html
