# FastAPI: APIRouter

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.APIRouter(*, prefix='', tags=None, dependencies=None, default_response_class=Default(JSONResponse), responses=None, callbacks=None, routes=None, redirect_slashes=True, default=None, dependency_overrides_provider=None, route_class=APIRoute, on_startup=None, on_shutdown=None, lifespan=None, deprecated=None, include_in_schema=True, generate_unique_id_function=Default(generate_unique_id))
```

## 2. ¿Qué es?

`APIRouter` es la clase que permite estructurar aplicaciones web grandes en módulos y submódulos independientes organizados por dominios de negocio.

## 3. ¿Para qué sirve?

Resuelve el problema de mantener archivos monolíticos (un archivo principal de miles de líneas), permitiendo que cada controlador resida en su propio paquete y se monte limpiamente en la aplicación principal con `app.include_router()`.

## 4. ¿Cómo funciona?

Opera como un mini-contenedor de rutas que agrupa prefijos URL compartidos (`prefix='/usuarios'`), etiquetas semánticas para la documentación (`tags=['Usuarios']`) y dependencias comunes.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `prefix` | `str` | Opcional | `''` | Prefijo de ruta URL prepuesto a todos los endpoints del router. |
| `tags` | `list[str | Enum]` | Opcional | `None` | Etiquetas para agrupar los endpoints en Swagger UI. |
| `dependencies` | `Sequence[Depends]` | Opcional | `None` | Lista de dependencias aplicadas a todas las rutas del router. |
| `responses` | `dict` | Opcional | `None` | Respuestas de error comunes (ej. 404, 500) documentadas para el grupo. |

## 6. Retorno

`APIRouter`. Instancia del enrutador modular.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/")
def listar_pedidos():
    return [{"id": 1, "total": 150.0}]

app = FastAPI()
app.include_router(router)

cliente = TestClient(app)
res = cliente.get("/pedidos/")
print(f"Código HTTP: {res.status_code}")
print(f"Respuesta del router modular: {res.json()}")
```

**Salida real:**

```text
Código HTTP: 200
Respuesta del router modular: [{'id': 1, 'total': 150.0}]
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

v1_router = APIRouter(prefix="/api/v1")
usuarios_router = APIRouter(prefix="/usuarios", tags=["V1 - Usuarios"])

@usuarios_router.get("/perfil")
def perfil():
    return {"usuario": "admin"}

# Anidamiento jerárquico de routers
v1_router.include_router(usuarios_router)
app = FastAPI()
app.include_router(v1_router)

cliente = TestClient(app)
res = cliente.get("/api/v1/usuarios/perfil")
print(f"Ruta jerárquica resuelta: {res.status_code} - {res.json()}")
```

**Salida real:**

```text
Ruta jerárquica resuelta: 200 - {'usuario': 'admin'}
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException
from fastapi.testclient import TestClient

def validar_api_key(x_key: str = Header(...)):
    if x_key != "clave-secreta":
        raise HTTPException(status_code=403, detail="Acceso denegado")

# Router con seguridad global aplicada a todas sus rutas sin repetir código
router_seguro = APIRouter(prefix="/admin", dependencies=[Depends(validar_api_key)])

@router_seguro.get("/stats")
def stats():
    return {"cpu": "15%"}

app = FastAPI()
app.include_router(router_seguro)

cliente = TestClient(app)
print(f"Petición sin key: {cliente.get('/admin/stats').status_code}")
print(f"Petición con key: {cliente.get('/admin/stats', headers={'x-key': 'clave-secreta'}).status_code}")
```

**Salida real:**

```text
Petición sin key: 422
Petición con key: 200
```

## 8. Errores frecuentes y casos borde

- **Doble barra en prefijos:** Configurar `prefix='/usuarios/'` y luego `@router.get('/')` resulta en la URL `/usuarios//`, generando redirecciones o 404s. No poner barra final en el prefijo: `prefix='/usuarios'`.
- **Olvidar llamar a `app.include_router()`:** Si no se incluye el router en la app principal, las rutas no existirán.

## 9. Buenas prácticas y rendimiento

- Organizar el proyecto con arquitectura Screaming/Limpia: `routers/usuarios.py`, `routers/productos.py`, `routers/autenticacion.py`.
- Inyectar dependencias globales a nivel de router (`dependencies=[Depends(...)]`) para proteger secciones enteras de la API.

## 10. Métodos relacionados

- [fastapi_app](fastapi_app.md)
- [endpoints](endpoints.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/bigger-applications/
