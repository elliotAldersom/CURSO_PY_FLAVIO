# FastAPI: Request Body y BaseModel (Pydantic)

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.Body(default=..., *, embed=None, media_type='application/json', alias=None, title=None, description=None, **extra)
```

## 2. ¿Qué es?

El cuerpo de petición (Request Body) permite recibir, validar, tipar y deserializar datos complejos enviados por el cliente mediante el payload HTTP (típicamente en formato JSON).

## 3. ¿Para qué sirve?

Resuelve la gestión segura de operaciones de mutación de estado (`POST`, `PUT`, `PATCH`), garantizando que la estructura de los datos entrantes sea estrictamente conforme a las reglas de negocio.

## 4. ¿Cómo funciona?

FastAPI extrae el flujo de bytes de la petición, parsea el JSON y lo valida recursivamente contra el esquema `pydantic.BaseModel`. Si los datos son válidos, entrega una instancia tipada de Python al endpoint; de lo contrario, aborta con código HTTP 422 y un reporte detallado del error.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `BaseModel` | `Type[pydantic.BaseModel]` | Obligatorio | N/A | Clase que define los campos, tipos y validadores del payload. |
| `embed` | `bool` | Opcional | `False` | Si es `True`, exige que el JSON esté anidado dentro de una clave con el nombre del modelo. |
| `media_type` | `str` | Opcional | `'application/json'` | Tipo MIME esperado. |

## 6. Retorno

`BaseModel`. Instancia de Pydantic con los datos ya validados.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float

app = FastAPI()

@app.post("/productos")
def registrar_producto(prod: Producto):
    return {"mensaje": f"Registrado {prod.nombre} con precio {prod.precio}"}

cliente = TestClient(app)
res = cliente.post("/productos", json={"nombre": "Mouse Gamer", "precio": 45.0})

print(f"Status: {res.status_code}")
print(f"Respuesta: {res.json()}")
```

**Salida real:**

```text
Status: 200
Respuesta: {'mensaje': 'Registrado Mouse Gamer con precio 45.0'}
```

### Nivel 2: Intermedio

```python
from typing import List, Optional
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class Detalle(BaseModel):
    producto: str
    cantidad: int = Field(gt=0)

class Factura(BaseModel):
    cliente_id: int
    detalles: List[Detalle]
    observaciones: Optional[str] = None

app = FastAPI()

@app.post("/facturas")
def crear_factura(factura: Factura):
    total_items = sum(d.cantidad for d in factura.detalles)
    return {"cliente": factura.cliente_id, "total_unidades": total_items}

cliente = TestClient(app)
payload = {
    "cliente_id": 99,
    "detalles": [{"producto": "Teclado", "cantidad": 2}, {"producto": "Monitor", "cantidad": 1}]
}
res = cliente.post("/facturas", json=payload)

print(f"Factura procesada con éxito: {res.json()}")
```

**Salida real:**

```text
Factura procesada con éxito: {'cliente': 99, 'total_unidades': 3}
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI, Body
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Usuario(BaseModel):
    usuario: str

app = FastAPI()

# embed=True obliga al cliente a enviar {'usuario': {'usuario': 'alex'}}
@app.post("/usuarios/login")
def login(usuario: Usuario = Body(..., embed=True)):
    return {"usuario_logeado": usuario.usuario}

cliente = TestClient(app)
res = cliente.post("/usuarios/login", json={"usuario": {"usuario": "alex"}})

print(f"Status con body embed: {res.status_code} - {res.json()}")
```

**Salida real:**

```text
Status con body embed: 200 - {'usuario_logeado': 'alex'}
```

## 8. Errores frecuentes y casos borde

- **Enviar JSON con tipos incompatibles:** Enviar un string como `'gratis'` en un campo declarado como `precio: float` genera automáticamente un error `422 Unprocessable Entity`.
- **Modificar objetos mutables en valores por defecto:** Declarar `items: list = []` en un modelo Pydantic v1 causaba errores de referencia compartida; en Pydantic v2 usar `items: List[str] = Field(default_factory=list)`.

## 9. Buenas prácticas y rendimiento

- Usar `pydantic.Field` para agregar restricciones declarativas (`min_length`, `gt`, `le`, `pattern`, `examples`).
- Modelar esquemas separados para entrada (`UsuarioCreate`) y salida (`UsuarioResponse`) para no exponer datos confidenciales como contraseñas.

## 10. Métodos relacionados

- [path_params](path_params.md)
- [response_model](../04_respuestas_errores/response_model.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/body/
