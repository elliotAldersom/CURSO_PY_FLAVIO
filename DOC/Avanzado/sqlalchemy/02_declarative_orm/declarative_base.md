# SQLAlchemy: DeclarativeBase y Mapeo Declarativo

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
class sqlalchemy.orm.DeclarativeBase(**kw)
```

## 2. ¿Qué es?

`DeclarativeBase` es la clase base universal de SQLAlchemy 2.0 de la cual deben heredar todas las entidades del modelo de datos para ser mapeadas a tablas relacionales.

## 3. ¿Para qué sirve?

Reemplaza a la antigua función `declarative_base()` de SQLAlchemy 1.x, integrando soporte nativo para verificación estática de tipos con Mypy y Pyright sin plugins adicionales.

## 4. ¿Cómo funciona?

Mantiene una instancia centralizada de `MetaData` accesible en `Base.metadata`. Al instanciarse subclases que definen `__tablename__`, la metaclase de `DeclarativeBase` registra automáticamente la definición DDL de la tabla y enlaza los atributos de clase a columnas relacionales.

## 5. Parámetros

| Propiedad / Método Clave | Tipo | Descripción |
|---|---|---|
| `metadata` | `MetaData` | Catálogo de metadatos de todas las tablas registradas en el modelo. |
| `__tablename__` | `str` | Nombre físico exacto de la tabla en el motor relacional. |
| `metadata.create_all(engine)` | Método | Genera y emite las sentencias DDL `CREATE TABLE` en la base de datos conectada. |

## 6. Retorno

`Type[DeclarativeBase]`. La clase base declarativa tipada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

print(f"Base declarativa instanciada: {Base.__name__}")
print(f"Catálogo de metadatos asociado: {type(Base.metadata).__name__}")
```

**Salida real:**

```text
Base declarativa instanciada: Base
Catálogo de metadatos asociado: MetaData
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Rol(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(30))

engine = create_engine("sqlite:///:memory:")
# Creación física de todas las tablas definidas en el metadata
Base.metadata.create_all(engine)

print(f"Tablas registradas en el catálogo: {list(Base.metadata.tables.keys())}")
engine.dispose()
```

**Salida real:**

```text
Tablas registradas en el catálogo: ['roles']
```

### Nivel 3: Avanzado

```python
from sqlalchemy.orm import DeclarativeBase, declared_attr

# Patrón Mixin para columnas compartidas (ej. auditoría de timestamps)
class TimestampMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

class Base(DeclarativeBase):
    pass

class Producto(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)

print(f"Nombre de tabla inferido automáticamente por el mixin: {Producto.__tablename__}")
```

**Salida real:**

```text
Nombre de tabla inferido automáticamente por el mixin: productos
```

## 8. Errores frecuentes y casos borde

- **Usar `declarative_base()` heredado de 1.4:** En SQLAlchemy 2.0 la función está deprecada; la forma moderna estricta es crear una clase que herede de `DeclarativeBase`.
- **Omitir `primary_key=True` en al menos una columna:** El ORM de SQLAlchemy exige que toda tabla registrada tenga al menos una clave primaria para rastrear la identidad de los objetos en memoria.

## 9. Buenas prácticas y rendimiento

- Definir una única clase `Base(DeclarativeBase)` central en un módulo `models/base.py` para que todo el proyecto comparta el mismo `metadata`.
- Utilizar mixins para centralizar columnas comunes como `created_at`, `updated_at` y `id`.

## 10. Métodos relacionados

- [mapped_column](mapped_column.md)
- [relationship](relationship.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html
