# SQLAlchemy: Engine.connect y Connection.execute

```python
# NO EJECUTAR (Firma oficial de la API en versión 2.0.x)
Engine.connect() -> Connection
Connection.execute(statement, parameters=None, execution_options=None) -> CursorResult
```

## 2. ¿Qué es?

Métodos que abren un contexto de conexión transaccional de bajo nivel y ejecutan sentencias SQL directas contra el motor relacional.

## 3. ¿Para qué sirve?

Permiten ejecutar consultas DDL (creación de tablas), comandos SQL de mantenimiento de alta velocidad o scripts por lotes sin la sobrecarga del ORM.

## 4. ¿Cómo funciona?

`connect()` extrae una conexión libre del pool. `execute()` compila la sentencia (generada con Core o envuelta en `text()`), enlaza los parámetros de forma segura y devuelve un `CursorResult` iterable.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `statement` | `Executable` o `TextClause` | Obligatorio | N/A | Expresión SQL compilable (generada con `text(...)` o constructores de Core). |
| `parameters` | `dict` o `Sequence[dict]` | Opcional | `None` | Diccionario con los parámetros vinculados a inyectar de forma segura. |

## 6. Retorno

`sqlalchemy.engine.CursorResult`. Resultado iterable que contiene las filas devueltas.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:")

with engine.connect() as conn:
    resultado = conn.execute(text("SELECT 1 AS numero, 'OK' AS estado"))
    fila = resultado.fetchone()
    print(f"Fila obtenida: numero={fila.numero}, estado={fila.estado}")

engine.dispose()
```

**Salida real:**

```text
Fila obtenida: numero=1, estado=OK
```

### Nivel 2: Intermedio

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE logs (id INT, nivel TEXT)"))
    # Inserción masiva de lotes de parámetros (batch execute)
    conn.execute(
        text("INSERT INTO logs (id, nivel) VALUES (:id, :nivel)"),
        [{"id": 1, "nivel": "INFO"}, {"id": 2, "nivel": "WARN"}, {"id": 3, "nivel": "ERROR"}]
    )
    conn.commit()

    total = conn.execute(text("SELECT COUNT(*) FROM logs")).scalar()
    print(f"Total registros insertados en batch: {total}")

engine.dispose()
```

**Salida real:**

```text
Total registros insertados en batch: 3
```

### Nivel 3: Avanzado

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:")

# engine.begin() maneja automáticamente el commit o rollback en caso de excepción
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE cuentas (titular TEXT, saldo REAL)"))
    conn.execute(text("INSERT INTO cuentas VALUES ('Alexander', 1000.0)"))

# Verificación fuera de la transacción atómica
with engine.connect() as conn:
    saldo = conn.execute(text("SELECT saldo FROM cuentas WHERE titular = 'Alexander'")).scalar()
    print(f"Saldo persistido mediante engine.begin(): {saldo}")

engine.dispose()
```

**Salida real:**

```text
Saldo persistido mediante engine.begin(): 1000.0
```

## 8. Errores frecuentes y casos borde

- **Olvidar llamar a `conn.commit()` con `engine.connect()`:** En SQLAlchemy 2.0, las conexiones están en modo 'commit-as-you-go'. Si mutas datos sin invocar `conn.commit()`, los cambios se descartan automáticamente al cerrar el bloque `with`.
- **Pasar strings crudos sin `text()`:** Pasar una cadena pura `conn.execute('SELECT 1')` arroja un error en 2.0; debe envolverse obligatoriamente con `text('SELECT 1')`.

## 9. Buenas prácticas y rendimiento

- Usar el bloque `with engine.begin() as conn:` para transacciones atómicas que hagan commit automático al salir o rollback si ocurre un error.
- Usar `.scalar()` cuando la consulta retorne una única celda (como `COUNT(*)` o un ID generado).

## 10. Métodos relacionados

- [create_engine](create_engine.md)
- [session](../03_sesion_transacciones/session.md)

## 11. Referencias oficiales

- https://docs.sqlalchemy.org/en/20/core/connections.html
