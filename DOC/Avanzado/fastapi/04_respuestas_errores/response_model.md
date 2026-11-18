# FastAPI: response_model y Modelos de Salida

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
@app.get(path, *, response_model=ModelClass, response_model_exclude_unset=False, response_model_exclude_defaults=False, response_model_exclude_none=False)
```

## 2. ¿Qué es?

`response_model` es un parámetro de los decoradores de endpoint que especifica el esquema de Pydantic utilizado para convertir, filtrar y validar los datos salientes de la respuesta HTTP.

## 3. ¿Para qué sirve?

Garantiza que la API cumpla estrictamente su contrato OpenAPI y previene fugas de seguridad catastróficas al filtrar automáticamente contraseñas, hashes o campos privados antes de enviar el JSON al cliente.

## 4. ¿Cómo funciona?

Toma el objeto retornado por el endpoint (que puede ser un diccionario, una tupla o un modelo ORM de SQLAlchemy), lo valida contra `response_model`, descarta los campos que no pertenezcan al modelo y serializa el JSON limpio.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `response_model` | `Type[BaseModel]` o `list[Type[BaseModel]]` | Obligatorio | N/A | Esquema Pydantic que define los campos públicos permitidos. |
| `response_model_exclude_unset` | `bool` | Opcional | `False` | Si es `True`, no incluye en el JSON los campos que no fueron explícitamente asignados. |
| `response_model_exclude_none` | `bool` | Opcional | `False` | Si es `True`, omite los campos cuyo valor sea `None`. |

## 6. Retorno

`Any`. El payload filtrado y serializado según el esquema declarado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class UsuarioPublico(BaseModel):
    id: int
    nombre: str

app = FastAPI()

# El endpoint maneja internamente el hash_password pero response_model lo filtra
@app.get("/usuario", response_model=UsuarioPublico)
def obtener():
    return {"id": 1, "nombre": "Alexander", "hash_password": "hash_secreto_super_privado"}

cliente = TestClient(app)
res = cliente.get("/usuario")

print(f"Respuesta recibida: {res.json()}")
print(f"Hash sensible filtrado con éxito: {'hash_password' not in res.json()}")
```

**Salida real:**

```text
Respuesta recibida: {'id': 1, 'nombre': 'Alexander'}
Hash sensible filtrado con éxito: True
```

### Nivel 2: Intermedio

```python
from typing import Optional
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Configuracion(BaseModel):
    tema: str = "oscuro"
    notificaciones: bool = True
    telefono: Optional[str] = None

app = FastAPI()

# response_model_exclude_none=True limpia el payload de valores nulos
@app.get("/config", response_model=Configuracion, response_model_exclude_none=True)
def get_config():
    return {"tema": "claro", "notificaciones": False, "telefono": None}

cliente = TestClient(app)
res = cliente.get("/config")

print(f"Payload limpio sin claves None: {res.json()}")
```

**Salida real:**

```text
Payload limpio sin claves None: {'tema': 'claro', 'notificaciones': False}
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict

# Simulación de un modelo ORM (SQLAlchemy) con atributos en lugar de diccionario
class EntidadORM:
    def __init__(self, id, codigo):
        self.id = id
        self.codigo = codigo
        self._meta_privada = "datos_internos"

class EntidadResponse(BaseModel):
    id: int
    codigo: str
    model_config = ConfigDict(from_attributes=True)  # Equivalente a orm_mode=True en v1

app = FastAPI()

@app.get("/entidad", response_model=EntidadResponse)
def leer():
    return EntidadORM(id=10, codigo="ENT-99")

cliente = TestClient(app)
res = cliente.get("/entidad")

print(f"Conversión de objeto ORM a JSON automática: {res.json()}")
```

**Salida real:**

```text
Conversión de objeto ORM a JSON automática: {'id': 10, 'codigo': 'ENT-99'}
```

## 8. Errores frecuentes y casos borde

- **Rendimiento por doble validación innecesaria:** Si el endpoint ya construye y retorna una instancia del mismo modelo especificado en `response_model`, FastAPI volverá a validar el objeto. Si se requiere máxima velocidad en microservicios, retornar diccionarios planos o usar `response_class=ORJSONResponse`.
- **Error de serialización de ORM:** En Pydantic v2, para serializar objetos de SQLAlchemy o Django se debe configurar `model_config = ConfigDict(from_attributes=True)`.

## 9. Buenas prácticas y rendimiento

- Definir siempre modelos estrictos de entrada (`XCreate`) y salida (`XResponse`).
- Usar `response_model_exclude_unset=True` en operaciones `PATCH` para transmitir únicamente los campos modificados.

## 10. Métodos relacionados

- [http_exception](http_exception.md)
- [request_body](../02_parametros_validacion/request_body.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/response-model/
