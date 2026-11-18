# FastAPI: Inyección de Dependencias con Depends()

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.Depends(dependency=None, *, use_cache=True)
```

## 2. ¿Qué es?

`Depends` es el mecanismo de inyección de dependencias de FastAPI que permite declarar componentes desacoplados reutilizables (conexiones de BD, lógica de negocio, autenticación, paginación) que se ejecutan automáticamente antes del endpoint.

## 3. ¿Para qué sirve?

Elimina la duplicación de código (DRY), desacopla la infraestructura del controlador y simplifica las pruebas unitarias mediante la sobreescritura de dependencias (`app.dependency_overrides`).

## 4. ¿Cómo funciona?

Construye un grafo acíclico dirigido (DAG) de dependencias. Resuelve primero las dependencias jerárquicas más profundas, ejecuta generadores con `yield` para administrar recursos y almacena en caché el resultado por petición si `use_cache=True`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `dependency` | `Callable` (función, generador o clase) | Opcional | `None` | Función o clase a resolver y ejecutar. |
| `use_cache` | `bool` | Opcional | `True` | Si es `True`, reutiliza la misma instancia/retorno dentro de la misma petición HTTP. |

## 6. Retorno

`Any`. El valor retornado por la función de dependencia inyectado en el endpoint.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

def paginacion_comun(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

app = FastAPI()

@app.get("/items")
def leer_items(pag: dict = Depends(paginacion_comun)):
    return {"datos": ["a", "b"], "paginacion": pag}

cliente = TestClient(app)
res = cliente.get("/items?skip=5&limit=25")

print(f"Status: {res.status_code}")
print(f"Dependencia inyectada: {res.json()}")
```

**Salida real:**

```text
Status: 200
Dependencia inyectada: {'datos': ['a', 'b'], 'paginacion': {'skip': 5, 'limit': 25}}
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

recursos = {"conexion_activa": False}

# Dependencia con generador (yield) para apertura y cierre seguro de conexiones
def obtener_sesion_db():
    recursos["conexion_activa"] = True
    try:
        yield "SESION_SQL_ACTIVA"
    finally:
        recursos["conexion_activa"] = False

app = FastAPI()

@app.get("/transaccion")
def ejecutar(db: str = Depends(obtener_sesion_db)):
    return {"db_usada": db, "estado_en_endpoint": recursos["conexion_activa"]}

cliente = TestClient(app)
res = cliente.get("/transaccion")

print(f"Ejecución con sesión inyectada: {res.json()}")
print(f"Recurso liberado limpiamente tras respuesta: {recursos['conexion_activa']}")
```

**Salida real:**

```text
Ejecución con sesión inyectada: {'db_usada': 'SESION_SQL_ACTIVA', 'estado_en_endpoint': True}
Recurso liberado limpiamente tras respuesta: False
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

def servicio_externo_produccion():
    return "DATOS_REALES_DE_PRODUCCION"

app = FastAPI()

@app.get("/datos")
def endpoint(dato: str = Depends(servicio_externo_produccion)):
    return {"fuente": dato}

# Sobreescritura de dependencia en tests unitarios sin tocar el código fuente
def mock_servicio_test():
    return "DATOS_MOCK_SIMULADOS"

app.dependency_overrides[servicio_externo_produccion] = mock_servicio_test

cliente = TestClient(app)
res = cliente.get("/datos")

print(f"Respuesta con mock inyectado: {res.json()}")
app.dependency_overrides.clear()
```

**Salida real:**

```text
Respuesta con mock inyectado: {'fuente': 'DATOS_MOCK_SIMULADOS'}
```

## 8. Errores frecuentes y casos borde

- **Excepciones dentro del bloque `finally` de un generador:** Si el generador lanza una excepción no capturada en el `finally`, puede impedir que la respuesta HTTP se envíe correctamente.
- **`use_cache=False` innecesario:** En dependencias costosas de calcular dentro de una misma petición, desactivar el caché provoca recalcular la misma lógica múltiples veces.

## 9. Buenas prácticas y rendimiento

- Usar generadores con `yield` para manejar sesiones de SQLAlchemy o conexiones de base de datos garantizando su cierre seguro tras la respuesta.
- Emplear `app.dependency_overrides` en la suite de pruebas automatizadas para inyectar bases de datos en memoria (SQLite) en lugar de PostgreSQL.

## 10. Métodos relacionados

- [security](security.md)
- [http_exception](../04_respuestas_errores/http_exception.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/dependencies/
