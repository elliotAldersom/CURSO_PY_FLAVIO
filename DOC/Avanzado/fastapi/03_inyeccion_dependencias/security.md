# FastAPI: Seguridad y Autenticación con OAuth2PasswordBearer

```python
# NO EJECUTAR (Firma oficial de la API en versión 0.110.x)
fastapi.security.OAuth2PasswordBearer(tokenUrl, *, scheme_name=None, scopes=None, description=None, auto_error=True)
```

## 2. ¿Qué es?

`OAuth2PasswordBearer` es una clase de seguridad que implementa el flujo de autenticación mediante tokens Bearer (JWT) según el estándar OAuth2.

## 3. ¿Para qué sirve?

Provee un mecanismo estandarizado para proteger endpoints privados, extrayendo automáticamente el token del encabezado `Authorization: Bearer <token>` e integrando el botón interactivo de candado en Swagger UI.

## 4. ¿Cómo funciona?

Intercepta las cabeceras HTTP de la petición entrante buscando el prefijo `Bearer`. Si está ausente o malformado y `auto_error=True`, arroja de inmediato una excepción HTTP 401 Unauthorized sin ejecutar el endpoint.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `tokenUrl` | `str` | Obligatorio | N/A | Ruta URL relativa del endpoint de login donde el cliente obtiene el token (ej. `'/auth/token'`). |
| `auto_error` | `bool` | Opcional | `True` | Si es `True`, genera un 401 automático si falta el token. Si es `False`, entrega `None` para autenticación opcional. |
| `scopes` | `dict[str, str]` | Opcional | `None` | Diccionario con permisos y ámbitos de autorización granular. |

## 6. Retorno

`str` (o `None`). La cadena del token Bearer extraída de las cabeceras.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

@app.get("/items/protegidos")
def leer_protegido(token: str = Depends(oauth2_scheme)):
    return {"token_recibido": token}

cliente = TestClient(app)
res_sin_token = cliente.get("/items/protegidos")
res_con_token = cliente.get("/items/protegidos", headers={"Authorization": "Bearer mi-jwt-secreto"})

print(f"Sin token status: {res_sin_token.status_code}")
print(f"Con token status: {res_con_token.status_code} - {res_con_token.json()}")
```

**Salida real:**

```text
Sin token status: 401
Con token status: 200 - {'token_recibido': 'mi-jwt-secreto'}
```

### Nivel 2: Intermedio

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    if token != "token_valido_admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación no válidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"usuario": "admin", "rol": "superusuario"}

app = FastAPI()

@app.get("/perfil")
def perfil(usuario_activo: dict = Depends(obtener_usuario_actual)):
    return {"usuario": usuario_activo["usuario"], "rol": usuario_activo["rol"]}

cliente = TestClient(app)
res = cliente.get("/perfil", headers={"Authorization": "Bearer token_valido_admin"})
print(f"Usuario autenticado e inyectado: {res.json()}")
```

**Salida real:**

```text
Usuario autenticado e inyectado: {'usuario': 'admin', 'rol': 'superusuario'}
```

### Nivel 3: Avanzado

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

# auto_error=False permite endpoints con autenticación opcional para invitados
oauth2_opcional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
app = FastAPI()

@app.get("/contenido")
def contenido(token: str = Depends(oauth2_opcional)):
    if token:
        return {"modo": "premium"}
    return {"modo": "gratuito_con_anuncios"}

cliente = TestClient(app)
res_anonimo = cliente.get("/contenido")
res_premium = cliente.get("/contenido", headers={"Authorization": "Bearer token_pago"})

print(f"Acceso anónimo: {res_anonimo.json()}")
print(f"Acceso premium: {res_premium.json()}")
```

**Salida real:**

```text
Acceso anónimo: {'modo': 'gratuito_con_anuncios'}
Acceso premium: {'modo': 'premium'}
```

## 8. Errores frecuentes y casos borde

- **Olvidar el encabezado `WWW-Authenticate: Bearer` en el 401:** El estándar RFC 6750 exige explícitamente incluir este encabezado al retornar 401 en autenticación Bearer.
- **Hardcodear secretos criptográficos en el código:** La clave secreta de firma JWT nunca debe residir en el código fuente; inyectar siempre mediante variables de entorno con `pydantic-settings`.

## 9. Buenas prácticas y rendimiento

- Combinar siempre `OAuth2PasswordBearer` con librerías seguras de firma de tokens como `PyJWT` o `python-jose`.
- Usar `auto_error=False` cuando se diseñen endpoints híbridos que ofrecen mayor información a usuarios autenticados pero permiten lectura pública a invitados.

## 10. Métodos relacionados

- [depends](depends.md)
- [http_exception](../04_respuestas_errores/http_exception.md)

## 11. Referencias oficiales

- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
