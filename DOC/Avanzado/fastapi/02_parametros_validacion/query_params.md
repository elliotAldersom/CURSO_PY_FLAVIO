# FastAPI: Query Parameters y Query()

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.Query(default=..., *, default_factory=None, alias=None, title=None, description=None, gt=None, ge=None, lt=None, le=None, min_length=None, max_length=None, regex=None, **extra)
```

## 2. ¿Qué es?

Los parámetros de consulta (Query Parameters) extraen variables pasadas en la cadena de consulta de la URL (después del signo `?`, ej. `?limite=10&orden=desc`) e inyectan validaciones con `Query()`.

## 3. ¿Para qué sirve?

Se utilizan típicamente para operaciones opcionales de paginación, ordenamiento, filtrado y búsqueda en colecciones de recursos.

## 4. ¿Cómo funciona?

Cualquier argumento de la función de endpoint que no forme parte del path de la URL y no sea un modelo complejo de Pydantic es interpretado automáticamente por FastAPI como un parámetro de consulta.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `default` | `Any` | Opcional | `...` | Valor por defecto (si es `...` Ellipsis, el query param se torna OBLIGATORIO). |
| `min_length`, `max_length` | `int` | Opcional | `None` | Límites de longitud de caracteres para strings de búsqueda. |
| `ge`, `le` | `float` | Opcional | `None` | Límites numéricos (ej. límites de paginación). |
| `alias` | `str` | Opcional | `None` | Nombre real en la URL cuando no es un identificador válido en Python (ej. `'item-id'`). |

## 6. Retorno

`Any`. El valor extraído de la query string convertido al tipo declarado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/articulos")
def listar(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

cliente = TestClient(app)
res = cliente.get("/articulos?skip=20&limit=50")

print(f"Status: {res.status_code}")
print(f"Query params parseados: {res.json()}")
```

**Salida real:**

```text
Status: 200
Query params parseados: {'skip': 20, 'limit': 50}
```

### Nivel 2: Intermedio

```python
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

# Búsqueda con longitud mínima obligatoria de 3 caracteres si se pasa
@app.get("/buscar")
def buscar(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    return {"consulta": q}

cliente = TestClient(app)
r_ok = cliente.get("/buscar?q=computador")
r_corta = cliente.get("/buscar?q=pc")  # Viola min_length=3

print(f"Búsqueda válida: {r_ok.status_code}")
print(f"Búsqueda muy corta rechazada con 422: {r_corta.status_code}")
```

**Salida real:**

```text
Búsqueda válida: 200
Búsqueda muy corta rechazada con 422: 422
```

### Nivel 3: Avanzado

```python
from typing import List
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

# Recepción de listas múltiples en query params (?filtro=A&filtro=B)
@app.get("/filtrar")
def filtrar(categoria: List[str] = Query(default=["general"])):
    return {"categorias_seleccionadas": categoria}

cliente = TestClient(app)
res = cliente.get("/filtrar?categoria=tecnologia&categoria=hogar")

print(f"Status: {res.status_code}")
print(f"Lista múltiple recibida: {res.json()}")
```

**Salida real:**

```text
Status: 200
Lista múltiple recibida: {'categorias_seleccionadas': ['tecnologia', 'hogar']}
```

## 8. Errores frecuentes y casos borde

- **Query params obligatorios no documentados:** Declarar `q: str` sin valor por defecto hace que el query param sea OBLIGATORIO; si el cliente no lo envía, FastAPI devuelve error 422.
- **Paginación descontrolada:** No colocar `le=100` en el parámetro `limit` permite que usuarios maliciosos pidan `?limit=1000000`, saturando la memoria del servidor de base de datos.

## 9. Buenas prácticas y rendimiento

- Limitar siempre los parámetros de paginación con `limit: int = Query(20, ge=1, le=100)`.
- Usar `alias` para admitir parámetros con guiones medios en la URL (ej. `filtro_tipo: str = Query(..., alias='filtro-tipo')`).

## 10. Métodos relacionados

- [path_params](path_params.md)
- [request_body](request_body.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/query-params/
