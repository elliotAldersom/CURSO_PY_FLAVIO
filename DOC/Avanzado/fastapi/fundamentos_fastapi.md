# Fundamentos de FastAPI: Desarrollo de APIs Web Asíncronas y Robustas en Python

FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python basado en tipos estándar de Python 3.8+ (Type Hints), Pydantic y Starlette.

## 2. Introducción

Tradicionalmente, el desarrollo backend en Python estuvo dominado por Django (un framework monolítico tipo "baterías incluidas") y Flask (un microframework síncrono minimalista). Sin embargo, con la llegada del soporte nativo de concurrencia asíncrona (`asyncio` y el estándar ASGI) en Python 3.5+, surgió la necesidad de un framework capaz de manejar decenas de miles de conexiones concurrentes con baja latencia.

Creado por Sebastián Ramírez en 2018, FastAPI revolucionó el ecosistema al unificar tres pilares:
1. **Starlette:** El núcleo de enrutamiento ASGI ultrarrápido que gestiona websockets, eventos y peticiones HTTP asíncronas.
2. **Pydantic:** El motor de validación, serialización y parseo de datos tipados en tiempo de ejecución.
3. **OpenAPI y JSON Schema:** Generación automática de contratos de API estandarizados y documentación interactiva interactiva lista para usar (Swagger UI y ReDoc).

## 3. Fundamentos y conceptos

La arquitectura de FastAPI reposa sobre cuatro conceptos arquitectónicos esenciales:
1. **Tipado Estático como Fuente de Verdad:** FastAPI utiliza las anotaciones de tipo estándar (`str`, `int`, `Optional`, `list`) de Python para:
   - Validar automáticamente que los datos entrantes cumplan el tipo especificado.
   - Convertir y deserializar los datos crudos (JSON o strings de query) a tipos nativos de Python.
   - Documentar la especificación en el esquema OpenAPI.
2. **Concurrencia Asíncrona (Async / Await):** Permite escribir endpoints con `async def` para operaciones bloqueantes de entrada/salida (I/O Bound) como consultas a bases de datos PostgreSQL o llamadas a APIs externas sin bloquear el hilo principal.
3. **Inyección de Dependencias (Dependency Injection):** Un sistema declarativo (`Depends`) que permite componer lógica compartida (autenticación, conexiones a base de datos, paginación) de forma desacoplada y fácilmente testeable.
4. **Validación Declarativa con Modelos Pydantic:** Los cuerpos de petición se modelan como subclases de `pydantic.BaseModel`, centralizando las reglas de negocio y restricciones en esquemas reutilizables.

## 4. Sintaxis y funcionamiento

El flujo mínimo de una aplicación FastAPI se compone de la instanciación de la aplicación y la decoración de funciones de ruta:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Servicio de Usuarios", version="1.0.0")

class Usuario(BaseModel):
    nombre: str
    activo: bool = True

@app.get("/")
def raiz():
    return {"mensaje": "API Operativa"}

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):
    return {"id": 1, "nombre": usuario.nombre, "activo": usuario.activo}
```

FastAPI intercepta la petición entrante, extrae el payload JSON, valida contra `Usuario`, invoca la función y serializa la respuesta a JSON con el código HTTP apropiado.

## 5. Ejemplos prácticos progresivos

### Básico

Creación de una aplicación FastAPI y prueba de endpoints de lectura usando `TestClient` de Starlette.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}

cliente = TestClient(app)
respuesta = cliente.get("/saludo/Alexander")

print(f"Código HTTP de respuesta: {respuesta.status_code}")
print(f"Cuerpo JSON retornado: {respuesta.json()}")
```

**Salida real:**

```text
Código HTTP de respuesta: 200
Cuerpo JSON retornado: {'mensaje': 'Hola, Alexander'}
```

### Intermedio

Validación rigurosa de cuerpos de petición con modelos Pydantic y control de códigos de estado HTTP.

```python
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    nombre: str = Field(min_length=2)
    precio: float = Field(gt=0)

@app.post("/items", status_code=status.HTTP_201_CREATED)
def crear_item(item: Item):
    return {"item_creado": item.nombre, "total_con_iva": round(item.precio * 1.19, 2)}

cliente = TestClient(app)
# Petición válida
r_valida = cliente.post("/items", json={"nombre": "Laptop", "precio": 1000.0})
# Petición inválida (precio negativo viola la restricción gt=0)
r_invalida = cliente.post("/items", json={"nombre": "Laptop", "precio": -50.0})

print(f"Status petición válida: {r_valida.status_code}")
print(f"Respuesta válida: {r_valida.json()}")
print(f"Status petición inválida rechazada automáticamente: {r_invalida.status_code}")
```

**Salida real:**

```text
Status petición válida: 201
Respuesta válida: {'item_creado': 'Laptop', 'total_con_iva': 1190.0}
Status petición inválida rechazada automáticamente: 422
```

### Avanzado

Arquitectura modular con `APIRouter`, inyección de dependencias (`Depends`) y autenticación basada en cabeceras HTTP.

```python
from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, status
from fastapi.testclient import TestClient

# Dependencia de seguridad que valida el token de autenticación
def verificar_token(x_token: str = Header(...)):
    if x_token != "secreto-seguro":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso inválido"
        )
    return "usuario_autenticado"

router = APIRouter(prefix="/admin", tags=["Administración"])

@router.get("/dashboard")
def dashboard(usuario: str = Depends(verificar_token)):
    return {"estado": "OK", "operador": usuario}

app = FastAPI()
app.include_router(router)

cliente = TestClient(app)
r_fallo = cliente.get("/admin/dashboard", headers={"x-token": "token-falso"})
r_exito = cliente.get("/admin/dashboard", headers={"x-token": "secreto-seguro"})

print(f"Respuesta sin autorización: {r_fallo.status_code} - {r_fallo.json()['detail']}")
print(f"Respuesta autorizada: {r_exito.status_code} - {r_exito.json()}")
```

**Salida real:**

```text
Respuesta sin autorización: 401 - Token de acceso inválido
Respuesta autorizada: 200 - {'estado': 'OK', 'operador': 'usuario_autenticado'}
```

## 6. Aplicaciones en el mundo real

- **Microservicios de Inferencia de Machine Learning:** Exposición de modelos entrenados (Scikit-learn, PyTorch) mediante endpoints REST de alta velocidad con validación automática de inputs.
- **Sistemas de Pasarelas de Pago y Webhooks:** Recepción y procesamiento concurrente de eventos transaccionales en tiempo real con latencias inferiores a 5 milisegundos.
- **Backends para Aplicaciones Móviles y SPAs:** APIs GraphQL o REST con soporte nativo de WebSockets y documentación interactiva inmediata para equipos frontend.

## 7. Uso en producción

- **Servidor ASGI de Grado de Producción:** Ejecutar siempre FastAPI detrás de un servidor ASGI robusto como Uvicorn gestionado por Gunicorn (en servidores bare-metal o máquinas virtuales) o como proceso único por contenedor en Kubernetes:
  ```bash
  # NO EJECUTAR (Comando de terminal para despliegue productivo)
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
- **Manejo de Operaciones Bloqueantes:** Nunca ejecutar código síncrono intensivo en CPU dentro de funciones declaradas con `async def`. Si una función no usa `await`, declararla simplemente con `def` normal; FastAPI la ejecutará en un threadpool independiente para no congelar el event loop de `asyncio`.
- **CORS Middleware:** Configurar explícitamente `CORSMiddleware` restringiendo orígenes permitidos antes de publicar a producción.

## 8. Errores comunes y recomendaciones

- **Declarar `async def` con bibliotecas síncronas:** Si se utiliza un driver de base de datos síncrono (como `psycopg2` tradicional) o `time.sleep()` dentro de un `async def`, se congela el bucle de eventos completo, degradando el rendimiento de todas las peticiones concurrentes a un solo hilo bloqueante. Usar drivers asíncronos (`asyncpg`, `databases`) o usar `def` estándar.
- **Retornar modelos con contraseñas o campos sensibles:** Utilizar siempre `response_model` para filtrar los campos devueltos y nunca exponer hashes de credenciales o metadatos internos en las respuestas.
- **Olvidar el prefijo `/` en las rutas:** Declarar `@app.get("usuarios")` sin la barra inicial causa inconsistencias de enrutamiento; escribir siempre `@app.get("/usuarios")`.

## 9. Resumen

FastAPI combina la velocidad de NodeJS y Go con la expresividad y elegancia de Python mediante el estándar ASGI y la validación tipada en tiempo de compilación/ejecución con Pydantic. Su sistema de inyección de dependencias, diseño modular con `APIRouter` y autogeneración de OpenAPI lo posicionan como la elección predilecta para arquitecturas modernas orientadas a servicios.

## 10. Referencias oficiales

- Documentación oficial de FastAPI: https://fastapi.tiangolo.com/
- Tutorial de usuario paso a paso: https://fastapi.tiangolo.com/tutorial/
- Repositorio oficial de FastAPI en GitHub: https://github.com/tiangolo/fastapi
