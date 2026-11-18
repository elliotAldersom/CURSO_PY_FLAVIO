# Biblioteca SQLAlchemy 2.0: Fichas Técnicas por Método y Componente

SQLAlchemy 2.0 es el toolkit de persistencia relacional y Object Relational Mapper (ORM) canónico en Python, estructurado sobre el patrón Unit of Work y modelado tipado con `Mapped`.

## Estructura Modular

| Categoría | Descripción | Índice |
|---|---|---|
| **01. Motor y Conexiones** | Configuración de Engine, Connection Pooling y ejecución directa | [01_motor_conexiones](01_motor_conexiones/indice.md) |
| **02. Mapeo Declarativo** | `DeclarativeBase`, definición tipada con `mapped_column` y relaciones | [02_declarative_orm](02_declarative_orm/indice.md) |
| **03. Sesión y Transacciones** | Unit of Work, Identity Map y control atómico de transacciones (`commit`/`rollback`) | [03_sesion_transacciones](03_sesion_transacciones/indice.md) |
| **04. Consultas CRUD** | Consultas declarativas con `select()`, mutaciones masivas y métodos escalares | [04_consultas_crud](04_consultas_crud/indice.md) |

Consulte también la guía global: [Fundamentos de SQLAlchemy 2.0](fundamentos_sqlalchemy.md).
