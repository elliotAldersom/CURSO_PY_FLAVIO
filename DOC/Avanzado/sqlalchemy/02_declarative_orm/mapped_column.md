# SQLAlchemy: Mapped y mapped_column

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
sqlalchemy.orm.mapped_column(*args, init=_NoArg.NO_ARG, repr=_NoArg.NO_ARG, default=_NoArg.NO_ARG, default_factory=_NoArg.NO_ARG, compare=_NoArg.NO_ARG, kw_only=_NoArg.NO_ARG, nullable=None, primary_key=False, deferred=False, deferred_group=None, deferred_raiseload=False, use_existing_column=False, **kw)
```

## 2. ¿Qué es?

`mapped_column` es el constructor que define las propiedades y restricciones físicas de una columna relacional (clave primaria, tipos SQL, nulabilidad, índices y valores por defecto) en simbiosis con el tipo `Mapped[...]`.

## 3. ¿Para qué sirve?

Provee tipado bidireccional estricto: informa a analizadores de tipo (Mypy) sobre el tipo en Python (`int`, `str`, `datetime`) mientras define la columna exacta en SQL (`Integer`, `VARCHAR(100)`).

## 4. ¿Cómo funciona?

Inspecciona la anotación `Mapped[T]`. Si se omite el tipo SQL en los argumentos de `mapped_column()`, SQLAlchemy deduce automáticamente el tipo SQL equivalente a partir del tipo de Python anotado en `T`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `*args` | `TypeEngine`, `ForeignKey` | Opcional | N/A | Tipo de columna SQL explícito (ej. `String(50)`) o clave foránea. |
| `primary_key` | `bool` | Opcional | `False` | Marca la columna como parte de la clave primaria. |
| `nullable` | `bool` | Opcional | Infiere de `Optional` | Si admite valores `NULL` (si se anota `Mapped[Optional[T]]`, infiere `True`). |
| `unique` | `bool` | Opcional | `False` | Agrega una restricción de unicidad (`UNIQUE`). |
| `index` | `bool` | Opcional | `False` | Construye un índice relacional para acelerar búsquedas. |
| `default` | `Any` o `Callable` | Opcional | `None` | Valor por defecto en Python al instanciar. |

## 6. Retorno

`MappedColumn`. Descriptor de columna mapeada.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))

print(f"Columna nombre nullable: {Usuario.nombre.nullable}")
print(f"Columna telefono nullable: {Usuario.telefono.nullable}")
```

**Salida real:**

```text
Columna nombre nullable: False
Columna telefono nullable: True
```

### Nivel 2: Intermedio

```python
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Auditoria(Base):
    __tablename__ = "auditorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    # server_default delega el cálculo al motor SQL (CURRENT_TIMESTAMP)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

print(f"Server default configurado: {Auditoria.creado_en.server_default}")
```

**Salida real:**

```text
Server default configurado: <sqlalchemy.sql.functions.now at 0x...; now>
```

### Nivel 3: Avanzado

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# Tipos inferidos automáticamente sin pasar tipos SQL explícitos
class Registro(Base):
    __tablename__ = "registros"
    id: Mapped[int] = mapped_column(primary_key=True)
    activo: Mapped[bool]  # Infiere automáticamente tipo Boolean SQL
    tasa: Mapped[float]   # Infiere automáticamente tipo Float SQL

print(f"Tipo SQL inferido para activo: {Registro.activo.type}")
print(f"Tipo SQL inferido para tasa: {Registro.tasa.type}")
```

**Salida real:**

```text
Tipo SQL inferido para activo: BOOLEAN
Tipo SQL inferido para tasa: FLOAT
```

## 8. Errores frecuentes y casos borde

- **Colocar `Mapped[str]` y esperar que admita `None`:** Si una columna puede ser nula, se debe declarar explícitamente `Mapped[Optional[str]]` o `Mapped[str | None]`. De lo contrario, SQLAlchemy forzará `nullable=False`.
- **Usar el antiguo `Column(...)` en modelos 2.0:** Aunque compatible por retrocompatibilidad, no provee inferencia de tipos con herramientas modernas.

## 9. Buenas prácticas y rendimiento

- Usar `Mapped[int] = mapped_column(primary_key=True)` para todas las claves primarias autoincrementables.
- Especificar siempre longitudes en columnas de texto (`String(255)`) para bases de datos como MySQL u Oracle.

## 10. Métodos relacionados

- [declarative_base](declarative_base.md)
- [relationship](relationship.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
