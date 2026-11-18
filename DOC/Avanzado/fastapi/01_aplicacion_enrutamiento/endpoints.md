# FastAPI: Decoradores de Operaciones de Ruta (get, post, put, delete)

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
@app.get(path, *, response_model=Default(None), status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description='Successful Response', responses=None, deprecated=None, operation_id=None, response_model_include=None, response_model_exclude=None, response_model_by_alias=True, response_model_exclude_unset=False, response_model_exclude_defaults=False, response_model_exclude_none=False, include_in_schema=True, response_class=Default(JSONResponse), name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=Default(generate_unique_id))
```

## 2. ¿Qué es?

Los decoradores de operaciones de ruta (`@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@app.patch`) mapean verbos estándar del protocolo HTTP y rutas URL a funciones controladoras en Python.

## 3. ¿Para qué sirve?

Definen la semántica RESTful del servicio: obtención de recursos (`GET`), creación (`POST`), reemplazo idempotente (`PUT`), eliminación (`DELETE`) o actualización parcial (`PATCH`).

## 4. ¿Cómo funciona?

Registran la función en la tabla de enrutamiento ASGI, asociando el código de estado predeterminado (`status_code`), el esquema de respuesta y los parámetros de documentación OpenAPI.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `path` | `str` | Obligatorio | N/A | Ruta URL relativa del endpoint (debe iniciar con `/`). |
| `status_code` | `int` | Opcional | `200` | Código HTTP de retorno exitoso (ej. `201` para creación en POST, `204` para DELETE). |
| `response_model` | `Type[BaseModel]` | Opcional | `None` | Modelo Pydantic para serializar y filtrar la respuesta. |
| `summary` | `str` | Opcional | `None` | Resumen breve del endpoint en Swagger UI. |
| `deprecated` | `bool` | Opcional | `False` | Marca la ruta como obsoleta en la especificación OpenAPI. |

## 6. Retorno

`Callable`. Decorador que registra la función manejadora de la petición.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items", status_code=status.HTTP_200_OK)
def obtener_items():
    return ["item1", "item2"]

cliente = TestClient(app)
res = cliente.get("/items")
print(f"Status: {res.status_code}")
print(f"Items: {res.json()}")
```

**Salida real:**

```text
Status: 200
Items: ['item1', 'item2']
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Libro(BaseModel):
    titulo: str

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: Libro):
    return {"id": 42, "titulo": libro.titulo}

@app.delete("/libros/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(id: int):
    return None

cliente = TestClient(app)
r_post = cliente.post("/libros", json={"titulo": "Clean Architecture"})
r_del = cliente.delete("/libros/42")

print(f"POST status: {r_post.status_code} - Payload: {r_post.json()}")
print(f"DELETE status: {r_del.status_code} - Body vacío: {r_del.content == b''}")
```

**Salida real:**

```text
POST status: 201 - Payload: {'id': 42, 'titulo': 'Clean Architecture'}
DELETE status: 204 - Body vacío: True
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/legacy-login", deprecated=True, summary="Login obsoleto en desuso")
def login_antiguo():
    return {"aviso": "Usar /auth/v2/token"}

cliente = TestClient(app)
schema = cliente.get("/openapi.json").json()
ruta_meta = schema["paths"]["/legacy-login"]["get"]

print(f"Endpoint marcado como deprecated: {ruta_meta['deprecated']}")
print(f"Summary en OpenAPI: {ruta_meta['summary']}")
```

**Salida real:**

```text
Endpoint marcado como deprecated: True
Summary en OpenAPI: Login obsoleto en desuso
```

## 8. Errores frecuentes y casos borde

- **Retornar contenido en un 204:** Si un endpoint devuelve `status_code=204` pero retorna un diccionario no vacío, viola el estándar HTTP de No Content. En 204 retornar `None` o `Response(status_code=204)`.
- **Usar GET para mutar estado:** Realizar inserciones o borrados en base de datos mediante peticiones `GET` vulnera el estándar REST y es inseguro frente a pre-fetching de navegadores.

## 9. Buenas prácticas y rendimiento

- Usar constantes semánticas de `fastapi.status` (como `status.HTTP_201_CREATED`, `status.HTTP_204_NO_CONTENT`) en lugar de números mágicos hardcodeados.
- Definir siempre `response_model` para evitar filtraciones accidentales de campos sensibles.

## 10. Métodos relacionados

- [apirouter](apirouter.md)
- [response_model](../04_respuestas_errores/response_model.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/first-steps/
