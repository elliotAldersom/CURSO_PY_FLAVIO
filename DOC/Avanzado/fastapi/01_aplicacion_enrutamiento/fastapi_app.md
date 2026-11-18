# FastAPI: Clase FastAPI

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.FastAPI(*, debug=False, routes=None, title='FastAPI', summary=None, description='', version='0.1.0', openapi_url='/openapi.json', openapi_tags=None, servers=None, dependencies=None, default_response_class=Default(JSONResponse), docs_url='/docs', redoc_url='/redoc', swagger_ui_oauth2_redirect_url='/docs/oauth2-redirect', swagger_ui_init_oauth=None, middleware=None, exception_handlers=None, on_startup=None, on_shutdown=None, lifespan=None, terms_of_service=None, contact=None, license_info=None, openapi_prefix='', root_path='', root_path_in_servers=True, responses=None, callbacks=None, webhooks=None, deprecated=None, include_in_schema=True, swagger_ui_parameters=None, generate_unique_id_function=Default(generate_unique_id), **extra)
```

## 2. ¿Qué es?

`FastAPI` es la clase principal que hereda de `Starlette` e instancía la aplicación web ASGI completa, gestionando el enrutador central, el ciclo de vida (lifespan), middleware y la documentación OpenAPI.

## 3. ¿Para qué sirve?

Actúa como punto de entrada de la arquitectura backend, orquestando todos los endpoints, dependencias globales y metadatos del servicio expuesto.

## 4. ¿Cómo funciona?

Inicializa el árbol de rutas ASGI, monta los esquemas de documentación interactiva Swagger UI (`/docs`) y ReDoc (`/redoc`), e intercepta el flujo HTTP para delegar en middleware y controladores.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `title` | `str` | Opcional | `'FastAPI'` | Nombre oficial de la API en la documentación OpenAPI. |
| `version` | `str` | Opcional | `'0.1.0'` | Versión semántica del servicio. |
| `docs_url` | `str` o `None` | Opcional | `'/docs'` | Ruta para la interfaz interactiva Swagger UI (pasar `None` para desactivar en producción). |
| `redoc_url` | `str` o `None` | Opcional | `'/redoc'` | Ruta para la documentación ReDoc (pasar `None` para desactivar). |
| `lifespan` | `Callable` | Opcional | `None` | Gestor de contexto asíncrono para startup y shutdown. |

## 6. Retorno

`FastAPI`. Instancia de la aplicación ASGI.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(title="Mi API Minima", version="1.0.0")

@app.get("/ping")
def ping():
    return {"status": "ok"}

cliente = TestClient(app)
res = cliente.get("/ping")
print(f"Status: {res.status_code}")
print(f"JSON: {res.json()}")
```

**Salida real:**

```text
Status: 200
JSON: {'status': 'ok'}
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Configuración corporativa completa de metadatos OpenAPI
app = FastAPI(
    title="Servicio de Pagos",
    description="Microservicio de procesamiento financiero",
    version="2.1.0",
    docs_url="/documentacion",
    redoc_url=None  # Desactiva ReDoc
)

cliente = TestClient(app)
res_schema = cliente.get("/openapi.json")

print(f"Título en OpenAPI: {res_schema.json()['info']['title']}")
print(f"Versión registrada: {res_schema.json()['info']['version']}")
```

**Salida real:**

```text
Título en OpenAPI: Servicio de Pagos
Versión registrada: 2.1.0
```

### Nivel 3: Avanzado

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient

estado_db = {"conectado": False}

# Patrón moderno de ciclo de vida con lifespan
@asynccontextmanager
async def ciclo_vida(app: FastAPI):
    estado_db["conectado"] = True
    yield
    estado_db["conectado"] = False

app = FastAPI(lifespan=ciclo_vida)

@app.get("/db-status")
def status():
    return {"db": estado_db["conectado"]}

with TestClient(app) as cliente:
    res = cliente.get("/db-status")
    print(f"Estado DB en ejecución: {res.json()}")
print(f"Estado DB tras shutdown: {estado_db['conectado']}")
```

**Salida real:**

```text
Estado DB en ejecución: {'db': True}
Estado DB tras shutdown: False
```

## 8. Errores frecuentes y casos borde

- **Dejar `/docs` activo en APIs públicas confidenciales:** En producción financiera o médica sensible, los endpoints de Swagger UI deben protegerse o desactivarse configurando `docs_url=None` y `redoc_url=None`.
- **Usar los eventos obsoletos `on_startup` y `on_shutdown`:** En versiones modernas de FastAPI, estos eventos están deprecados; utilizar el gestor unificado `lifespan`.

## 9. Buenas prácticas y rendimiento

- Configurar siempre `title`, `description` y `version` para generar documentación técnica clara y versionada.
- Centralizar recursos pesados (conexiones a bases de datos, carga de modelos ML) dentro de la función generadora `lifespan`.

## 10. Métodos relacionados

- [apirouter](apirouter.md)
- [endpoints](endpoints.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/reference/fastapi/
