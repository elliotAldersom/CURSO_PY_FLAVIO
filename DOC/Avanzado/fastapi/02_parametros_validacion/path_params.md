# FastAPI: Path Parameters y Path()

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.Path(*, default=..., default_factory=None, alias=None, title=None, description=None, gt=None, ge=None, lt=None, le=None, min_length=None, max_length=None, regex=None, **extra)
```

## 2. ¿Qué es?

Los parámetros de ruta (Path Parameters) extraen variables dinámicas codificadas directamente dentro del segmento de la URL e inyectan validaciones adicionales mediante la función `Path()`.

## 3. ¿Para qué sirve?

Permiten identificar unívocamente recursos individuales en una jerarquía RESTful (ej. `/usuarios/{usuario_id}`) garantizando tipos numéricos o formatos específicos.

## 4. ¿Cómo funciona?

FastAPI analiza la plantilla de la ruta URL (`{param}`), coteja la variable con los argumentos tipados de la función y ejecuta la coerción y validación de Pydantic antes de invocar el controlador.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `default` | `Any` | Obligatorio | `...` (Ellipsis) | Los parámetros de ruta son SIEMPRE obligatorios en el estándar HTTP. |
| `ge`, `gt` | `float` | Opcional | `None` | Mayor o igual / Mayor estricto que un valor numérico. |
| `le`, `lt` | `float` | Opcional | `None` | Menor o igual / Menor estricto que un valor numérico. |
| `min_length` | `int` | Opcional | `None` | Longitud mínima de caracteres si el parámetro es un string. |
| `regex` / `pattern` | `str` | Opcional | `None` | Expresión regular que debe cumplir el parámetro. |

## 6. Retorno

`Any`. El valor extraído de la URL convertido al tipo tipado.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items/{item_id}")
def leer_item(item_id: int):
    return {"item_id": item_id, "tipo": str(type(item_id).__name__)}

cliente = TestClient(app)
res = cliente.get("/items/42")

print(f"Status: {res.status_code}")
print(f"Respuesta con coerción de tipo: {res.json()}")
```

**Salida real:**

```text
Status: 200
Respuesta con coerción de tipo: {'item_id': 42, 'tipo': 'int'}
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

app = FastAPI()

# Restricción explícita: ID debe ser entero positivo mayor o igual a 1
@app.get("/cuentas/{cuenta_id}")
def obtener_cuenta(cuenta_id: int = Path(..., ge=1, le=1000000, title="ID de cuenta")):
    return {"cuenta": cuenta_id}

cliente = TestClient(app)
r_valida = cliente.get("/cuentas/500")
r_invalida = cliente.get("/cuentas/0")  # Viola ge=1

print(f"Petición válida (ID 500): {r_valida.status_code}")
print(f"Petición rechazada por regla ge=1: {r_invalida.status_code}")
```

**Salida real:**

```text
Petición válida (ID 500): 200
Petición rechazada por regla ge=1: 422
```

### Nivel 3: Avanzado

```python
from enum import Enum
from fastapi import FastAPI
from fastapi.testclient import TestClient

class Ambiente(str, Enum):
    DEV = "desarrollo"
    STAGE = "pruebas"
    PROD = "produccion"

app = FastAPI()

# Validación basada en enumeraciones predefinidas
@app.get("/servidores/{env}")
def obtener_servidor(env: Ambiente):
    return {"ambiente_activo": env.value}

cliente = TestClient(app)
res_ok = cliente.get("/servidores/produccion")
res_err = cliente.get("/servidores/local")

print(f"Enum válido: {res_ok.status_code} - {res_ok.json()}")
print(f"Enum desconocido rechazado: {res_err.status_code}")
```

**Salida real:**

```text
Enum válido: 200 - {'ambiente_activo': 'produccion'}
Enum desconocido rechazado: 422
```

## 8. Errores frecuentes y casos borde

- **Marcar un parámetro de ruta como opcional:** En el estándar HTTP una URL como `/items/{id}` no puede existir sin el `{id}`; no asignar valores por defecto que sugieran opcionalidad.
- **Conflicto de orden en rutas estáticas vs dinámicas:** Si se define `@app.get('/usuarios/{id}')` antes de `@app.get('/usuarios/yo')`, FastAPI intentará parsear la cadena `'yo'` como un entero `id`, arrojando un error 422. Definir rutas fijas SIEMPRE antes que las dinámicas.

## 9. Buenas prácticas y rendimiento

- Usar `Path(..., ge=1)` para IDs numéricos para evitar consultas con IDs negativos o cero a la base de datos.
- Utilizar clases `Enum` para parámetros de ruta con valores cerrados y predefinidos.

## 10. Métodos relacionados

- [query_params](query_params.md)
- [request_body](request_body.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/path-params/
