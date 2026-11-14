# Entornos virtuales en Python con `venv`

Guía para crear, activar, verificar y salir de un entorno virtual desde la terminal, explicando cada comando, sus partes y por qué se usa.

---

## Índice

1. [¿Qué es un entorno virtual y por qué usarlo?](#1-qué-es-un-entorno-virtual-y-por-qué-usarlo)
2. [Crear el entorno](#2-crear-el-entorno)
3. [Entrar (activar)](#3-entrar-activar)
4. [Verificar si estás dentro](#4-verificar-si-estás-dentro)
5. [Salir (desactivar)](#5-salir-desactivar)
6. [Instalar y reproducir dependencias](#6-instalar-y-reproducir-dependencias)
7. [Flujo completo de un proyecto](#7-flujo-completo-de-un-proyecto)
8. [Buenas prácticas para producción](#8-buenas-prácticas-para-producción)
9. [Problemas frecuentes](#9-problemas-frecuentes)
10. [Documentación oficial](#10-documentación-oficial)

---

## 1. ¿Qué es un entorno virtual y por qué usarlo?

Un entorno virtual es una **carpeta dentro de tu proyecto** que contiene una copia aislada del intérprete de Python y su propio `pip`. Todo lo que instales con el entorno activo queda dentro de esa carpeta y no afecta al resto del sistema.

| Sin entorno virtual | Con entorno virtual |
|---|---|
| Las librerías se instalan **globalmente** | Las librerías se instalan **solo en el proyecto** |
| Dos proyectos que piden versiones distintas de una librería entran en conflicto | Cada proyecto tiene sus propias versiones |
| En Linux puedes romper paquetes que usa el propio sistema | El Python del sistema queda intacto |
| Difícil de reproducir en otra máquina | Reproducible con `requirements.txt` |

> **Nota:** en distribuciones Linux modernas (incluido Arch/CachyOS), `pip install` global suele estar bloqueado por el sistema (error `externally-managed-environment`). Los entornos virtuales son la forma correcta de instalar librerías de Python.

---

## 2. Crear el entorno

### Ejemplo simple

Desde la raíz de tu proyecto:

```bash
python -m venv .venv
```

### Desglose del comando

| Parte | Qué significa | Por qué se usa |
|---|---|---|
| `python` | El intérprete que se copiará al entorno | Define la **versión de Python** del entorno. Si usas `python3.12`, el entorno será 3.12 |
| `-m` | Ejecuta un **módulo** de la librería estándar como si fuera un script | Así usas el módulo `venv` que ya viene con Python, sin instalar nada |
| `venv` | Módulo que crea entornos virtuales | Es la herramienta oficial de Python |
| `.venv` | Nombre de la carpeta destino | Es la convención: VS Code y PyCharm la detectan solos, y el punto la oculta en el explorador |

### Qué contiene la carpeta `.venv/`

| Elemento | Contenido |
|---|---|
| `bin/` | Ejecutables: `python`, `pip` y los scripts `activate` |
| `lib/python3.x/site-packages/` | Aquí se instalan **tus librerías** |
| `pyvenv.cfg` | Configuración del entorno (versión y ruta del Python base) |

### Ejemplo avanzado

```bash
# Crear el entorno con una versión específica de Python
python3.12 -m venv .venv

# Crearlo y actualizar pip/setuptools en el mismo paso
python -m venv --upgrade-deps .venv
```

| Opción | Qué hace |
|---|---|
| `python3.12` | Usa exactamente esa versión (debe estar instalada en el sistema) |
| `--upgrade-deps` | Actualiza `pip` y `setuptools` a la última versión al crear el entorno |

> **Nota:** el nombre `.venv` no es obligatorio, pero usar siempre el mismo en todos tus proyectos simplifica scripts, `.gitignore` y configuración del editor.

---

## 3. Entrar (activar)

### Ejemplo simple (Linux / macOS)

```bash
source .venv/bin/activate
```

### Desglose del comando

| Parte | Qué significa | Por qué se usa |
|---|---|---|
| `source` | Ejecuta el script **dentro de tu shell actual** | Si lo ejecutaras normal, correría en un subproceso y los cambios se perderían al terminar. `source` modifica **tu** terminal |
| `.venv/bin/activate` | Ruta al script de activación | Es el script que viene dentro del entorno |

### Qué hace `activate` por dentro

1. Define la variable `VIRTUAL_ENV` con la ruta del entorno.
2. Antepone `.venv/bin` al `PATH`. Por eso, al escribir `python` o `pip`, se usan los del entorno y no los del sistema.
3. Agrega el comando `deactivate`.
4. Intenta cambiar el prompt para mostrar `(.venv)`.

### Script de activación según tu shell

| Shell / Sistema | Comando |
|---|---|
| bash / zsh (Linux, macOS) | `source .venv/bin/activate` |
| fish | `source .venv/bin/activate.fish` |
| csh / tcsh | `source .venv/bin/activate.csh` |
| PowerShell (Windows) | `.venv\Scripts\Activate.ps1` |
| CMD (Windows) | `.venv\Scripts\activate.bat` |

> **Nota (PowerShell):** si Windows bloquea el script, ejecuta una sola vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Ejemplo avanzado: no hace falta activar para ejecutar

Puedes usar el entorno **sin activarlo**, llamando directamente al Python de dentro:

```bash
.venv/bin/python main.py
.venv/bin/python -m pip install requests
```

Esto es lo que se hace en **scripts, cron jobs, servicios `systemd` y Dockerfiles**, donde no hay una terminal interactiva que active nada.

---

## 4. Verificar si estás dentro

Los comandos van de más simple a más completo.

### 4.1 Variable `VIRTUAL_ENV`

```bash
echo $VIRTUAL_ENV
```

| Parte | Significado |
|---|---|
| `echo` | Imprime texto en pantalla |
| `$VIRTUAL_ENV` | Valor de la variable de entorno que define `activate` |

**Si imprime una ruta, estás dentro. Si no imprime nada, no estás dentro.**

```text
/home/usuario/proyecto/.venv     ← dentro
                                 ← vacío: fuera
```

### 4.2 Qué `python` se usaría

```bash
which python
```

`which` muestra la ruta del ejecutable que se usaría al escribir `python`.

| Resultado | Significado |
|---|---|
| `.../proyecto/.venv/bin/python` | Estás dentro del entorno |
| `/usr/bin/python` | Estás usando el Python del sistema |

> En PowerShell usa `Get-Command python` en lugar de `which`.

### 4.3 Verificación desde Python (la más confiable)

```bash
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

| Parte | Qué hace |
|---|---|
| `-c "..."` | Ejecuta el código entre comillas directamente |
| `sys.prefix` | Ruta del entorno actual |
| `sys.base_prefix` | Ruta del Python original con el que se creó el entorno |
| `!=` | Si son distintas, hay un entorno activo y se imprime `True` |

### 4.4 Qué `pip` está en uso

```bash
python -m pip --version
```

Muestra la versión y la **ruta** del `pip`. Si apunta a `.venv/lib/...`, lo que instales irá al entorno.

### 4.5 Qué hay instalado en el entorno

```bash
python -m pip list
```

En un entorno recién creado solo verás `pip` (y a veces `setuptools`). Si ves cientos de paquetes, probablemente estás en el Python global.

### Resumen de verificaciones

| Comando | Qué responde | Fiabilidad |
|---|---|---|
| `echo $VIRTUAL_ENV` | ¿Hay un entorno activado en esta terminal? | Alta |
| `which python` | ¿Qué Python se ejecutaría? | Alta |
| `python -c "import sys; print(sys.prefix != sys.base_prefix)"` | ¿Python mismo detecta un entorno? | **La más alta** |
| Prompt con `(.venv)` | Indicador visual | **Media**: depende del tema del prompt |

### Nota: ¿por qué mi prompt no muestra `(.venv)`?

Temas de prompt como **Powerlevel10k** reemplazan el `(.venv)` por su propio indicador de entorno virtual, normalmente en el lado derecho de la línea. Como la carpeta se llama `.venv` (un nombre genérico), esos temas muestran el **nombre del proyecto** en su lugar.

Para comprobarlo: ejecuta `deactivate`. Si ese texto desaparece del prompt, era el indicador del entorno. Por eso conviene fiarse de `echo $VIRTUAL_ENV` y `which python`, no del prompt.

---

## 5. Salir (desactivar)

```bash
deactivate
```

| Qué hace | Detalle |
|---|---|
| Restaura el `PATH` | Vuelves a usar el `python` y `pip` del sistema |
| Elimina `VIRTUAL_ENV` | `echo $VIRTUAL_ENV` vuelve a salir vacío |
| **No borra nada** | La carpeta `.venv` sigue intacta y puedes volver a entrar cuando quieras |

> **Nota:** `deactivate` solo existe mientras hay un entorno activo. Para **eliminar** un entorno se borra la carpeta: `rm -rf .venv`.

---

## 6. Instalar y reproducir dependencias

### Ejemplo simple

```bash
python -m pip install requests
```

| Parte | Por qué se usa |
|---|---|
| `python -m pip` | Garantiza que el `pip` usado **pertenece al `python` activo**. Escribir solo `pip` a veces ejecuta uno distinto |
| `install requests` | Instala la librería en el entorno actual |

### Comandos de gestión

| Comando | Para qué sirve |
|---|---|
| `python -m pip install requests` | Instala una librería en el entorno activo |
| `python -m pip install requests==2.32.3` | Instala una **versión exacta** |
| `python -m pip uninstall requests` | Desinstala una librería |
| `python -m pip list` | Lista lo instalado |
| `python -m pip freeze > requirements.txt` | Guarda paquetes y versiones exactas. `>` redirige la salida al archivo |
| `python -m pip install -r requirements.txt` | Instala todo lo del archivo (`-r` = leer desde archivo) |
| `python -m pip check` | Verifica que no haya dependencias rotas o incompatibles |

### Ejemplo avanzado: reproducir el entorno en otra máquina

```bash
git clone <repositorio>
cd <proyecto>
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Esto funciona porque se versiona `requirements.txt` y **no** la carpeta `.venv`.

### Ejemplo de `requirements.txt`

```text
requests==2.32.3
python-dotenv==1.0.1
```

> **Nota:** fijar versiones exactas (`==`) hace el entorno **reproducible**. Sin ellas, instalar "hoy" y "dentro de seis meses" puede dar versiones distintas y errores difíciles de rastrear.

---

## 7. Flujo completo de un proyecto

```bash
# 1. Ir al proyecto
cd ~/mi-proyecto

# 2. Crear el entorno (solo la primera vez)
python -m venv .venv

# 3. Activarlo (cada vez que abras una terminal nueva)
source .venv/bin/activate

# 4. Comprobar que estás dentro
echo $VIRTUAL_ENV
which python

# 5. Instalar dependencias y congelarlas
python -m pip install requests
python -m pip freeze > requirements.txt

# 6. Trabajar...
python main.py

# 7. Salir al terminar
deactivate
```

> **Nota:** crear el entorno es **una sola vez** por proyecto. Activarlo es **cada vez** que abres una terminal nueva.

---

## 8. Buenas prácticas para producción

| Práctica | Por qué |
|---|---|
| **Agregar `.venv/` al `.gitignore`** | El entorno es pesado y específico de cada máquina. Se versiona `requirements.txt`, no `.venv` |
| **No mover ni copiar la carpeta `.venv`** | Contiene rutas absolutas internas. Si mueves el proyecto, bórrala y recréala desde `requirements.txt` |
| **Un entorno por proyecto** | Evita conflictos de versiones entre proyectos |
| **Fijar versiones en `requirements.txt`** | Garantiza que desarrollo y producción usen lo mismo |
| **Usar siempre `python -m pip`** | Evita instalar en el entorno equivocado |
| **Nunca usar `sudo pip install`** | Puede romper paquetes que el sistema necesita |
| **Ejecutar `pip check` antes de desplegar** | Detecta incompatibilidades entre dependencias |
| **Separar dependencias de desarrollo** | Ver ejemplo abajo |

### Ejemplo: separar dependencias de producción y de desarrollo

```text
requirements.txt          ← lo que necesita la app para correr
requirements-dev.txt      ← herramientas de desarrollo (tests, linters)
```

Contenido de `requirements-dev.txt`:

```text
-r requirements.txt
pytest==8.3.3
ruff==0.7.0
```

```bash
# En desarrollo
python -m pip install -r requirements-dev.txt

# En producción (solo lo necesario)
python -m pip install -r requirements.txt
```

### Ejemplo: `.gitignore` mínimo

```text
.venv/
__pycache__/
*.pyc
.env
```

---

## 9. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `externally-managed-environment` al hacer `pip install` | Estás fuera del entorno, en el Python del sistema | Activa el entorno y reintenta |
| `command not found: python` dentro del entorno | El entorno se creó con otro nombre de intérprete | Usa `python3`, o recrea el entorno |
| El entorno dejó de funcionar tras mover la carpeta | Rutas absolutas internas | Borra `.venv` y créalo de nuevo |
| `ModuleNotFoundError` aunque instalaste la librería | Instalaste con un `pip` distinto al `python` que ejecuta el script | Usa `python -m pip install ...` con el entorno activo |
| `Activate.ps1 cannot be loaded` (Windows) | Política de ejecución de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| El prompt no muestra `(.venv)` | Tu tema de prompt usa su propio indicador | Verifica con `echo $VIRTUAL_ENV` |

---

## 10. Documentación oficial

| Recurso | Enlace |
|---|---|
| Módulo `venv` (referencia) | https://docs.python.org/3/library/venv.html |
| Tutorial oficial: entornos virtuales y paquetes | https://docs.python.org/3/tutorial/venv.html |
| Python Packaging Guide: usar `pip` y entornos virtuales | https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ |
| Documentación de `pip` | https://pip.pypa.io/en/stable/ |
| Formato de `requirements.txt` | https://pip.pypa.io/en/stable/reference/requirements-file-format/ |