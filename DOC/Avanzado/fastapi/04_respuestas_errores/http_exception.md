# FastAPI: HTTPException

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.HTTPException(status_code: int, detail: Any = None, headers: Optional[Dict[str, str]] = None)
```

## 2. ¿Qué es?

`HTTPException` es la excepción canónica que se lanza para interrumpir inmediatamente el flujo normal de una petición y devolver una respuesta HTTP de error con su código y payload estructurado.

## 3. ¿Para qué sirve?

Resuelve el manejo limpio de situaciones de error en lógica de negocio (recursos no encontrados, accesos denegados, conflictos de duplicidad) sin acoplar el controlador a retornos condicionales manuales.

## 4. ¿Cómo funciona?

FastAPI cuenta con un gestor global (`exception_handler`) registrado para `HTTPException`. Al lanzarse con `raise`, captura la instancia, extrae `status_code` y serializa el contenido de `detail` dentro de una respuesta JSON estándar `{'detail': ...}`.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `status_code` | `int` | Obligatorio | N/A | Código HTTP de error (ej. `404` Not Found, `403` Forbidden, `409` Conflict). |
| `detail` | `Any` (`str`, `dict`, `list`) | Opcional | `None` | Mensaje descriptivo o estructura de datos con el contexto del error. |
| `headers` | `dict[str, str]` | Opcional | `None` | Encabezados HTTP adicionales a incorporar en la respuesta de error. |

## 6. Retorno

`NoReturn`. No retorna valor; interrumpe el flujo de ejecución mediante `raise`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/usuarios/{user_id}")
def buscar_usuario(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {"id": 1, "nombre": "Alexander"}

cliente = TestClient(app)
res_error = cliente.get("/usuarios/99")

print(f"Status capturado: {res_error.status_code}")
print(f"Cuerpo JSON del error: {res_error.json()}")
```

**Salida real:**

```text
Status capturado: 404
Cuerpo JSON del error: {'detail': 'Usuario no encontrado'}
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/transferencia")
def transferir(monto: float):
    saldo = 100.0
    if monto > saldo:
        # Detalle estructurado con diccionario para que el frontend actúe
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "codigo_error": "SALDO_INSUFICIENTE",
                "saldo_actual": saldo,
                "monto_solicitado": monto
            }
        )
    return {"estado": "transferido"}

cliente = TestClient(app)
res = cliente.post("/transferencia?monto=250")

print(f"Error estructurado: {res.json()['detail']}")
```

**Salida real:**

```text
Error estructurado: {'codigo_error': 'SALDO_INSUFICIENTE', 'saldo_actual': 100.0, 'monto_solicitado': 250.0}
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

class ErrorDominio(Exception):
    def __init__(self, mensaje: str):
        self.mensaje = mensaje

app = FastAPI()

# Manejador personalizado para desacoplar excepciones de dominio de FastAPI
@app.exception_handler(ErrorDominio)
def error_dominio_handler(request: Request, exc: ErrorDominio):
    return JSONResponse(status_code=422, content={"error_aplicacion": exc.mensaje})

@app.get("/accion")
def accion():
    raise ErrorDominio("Violación de regla de negocio pura")

cliente = TestClient(app)
res = cliente.get("/accion")

print(f"Status manejador custom: {res.status_code}")
print(f"JSON retornado por exception_handler: {res.json()}")
```

**Salida real:**

```text
Status manejador custom: 422
JSON retornado por exception_handler: {'error_aplicacion': 'Violación de regla de negocio pura'}
```

## 8. Errores frecuentes y casos borde

- **Usar `return HTTPException(...)` en lugar de `raise HTTPException(...)`:** Si se retorna la excepción en lugar de lanzarla, FastAPI la tratará como un objeto regular y devolverá un código 200 OK con la representación del objeto de excepción.
- **Filtrar trazas de error internas en producción:** Nunca enviar excepciones de SQL crudas o stack traces en el argumento `detail`; exponer solo mensajes controlados de negocio.

## 9. Buenas prácticas y rendimiento

- Usar siempre las constantes de `fastapi.status` (como `status.HTTP_404_NOT_FOUND`).
- En arquitecturas limpias / hexagonales, lanzar excepciones de dominio puro y mapearlas a códigos HTTP en un `app.exception_handler()` centralizado.

## 10. Métodos relacionados

- [response_model](response_model.md)
- [endpoints](../01_aplicacion_enrutamiento/endpoints.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/handling-errors/
