# PYTHON BÁSICO 1 · EVALUACIÓN INTEGRAL
## Examen Práctico: Python para Análisis de Datos

**Indicaciones:**

Copia los enunciados y datos base en tu cuaderno de Google Colab y desarrolla cada ejercicio en una celda de código independiente.

- Usa nombres descriptivos en `snake_case` para las variables.
- Usa `MAYÚSCULAS` para las constantes.

---

# Sección 1: Variables, Tipos de Datos y Conversión (Casting)

### 1. Registro de Métrica de Campaña

Declara una constante `TASA_IGV = 0.18` y las siguientes variables de un registro de ventas:

```python
id_transaccion = "TX-904"
unidades_vendidas = 14
precio_unitario = 45.90
cliente_recurrente = True
```

**Tareas:**
- Imprime el valor de cada variable.
- Imprime el tipo de dato (`type()`) de cada variable.

### 2. Limpieza de Datos Crudos

En una exportación CSV recibes los campos como texto:

```python
ingresos_str = "12850.75"
devoluciones_str = "420.25"
clientes_activos_str = "310"
```

**Tareas:**
- Convierte los valores a sus tipos numéricos correspondientes (`float` e `int`).
- Calcula el ingreso neto.
- Calcula el ingreso promedio por cliente activo.
- Muestra ambos resultados.

---

# Sección 2: Operadores Aritméticos, Comparación y Lógicos

### 3. Cálculo de KPIs de Conversión

Una página web recibió los siguientes resultados:

```python
visitas = 4850
registros = 610
compras = 145
```

**Tareas:**

1. Calcula la tasa de registro:

   `registros / visitas * 100`

2. Calcula la tasa de conversión a compra:

   `compras / registros * 100`

3. Evalúa con operadores de comparación y lógicos si se cumple la meta de:
   - Más de 10 % de registros.
   - Más de 20 % de conversión a compra.

### 4. Detección de Anomalías en Sensores

Dado un registro de temperatura de servidor y carga de CPU:

```python
temp_actual = 78.5
cpu_porcentaje = 92
en_mantenimiento = False
```

**Tareas:**

Crea una expresión booleana llamada `alerta_critica` que sea `True` si:

- La temperatura supera los 75 grados **o** la CPU es mayor o igual al 90 %.
- Pero no si el servidor está en mantenimiento.

---

# Sección 3: Condicionales (`if / elif / else`)

### 5. Segmentación RFM de Clientes

A partir del gasto anual de un cliente y su frecuencia de compra:

```python
gasto_anual = 1850.0
compras_anio = 9
```

**Tareas:**

Clasifica e imprime su segmento según las siguientes condiciones:

| Segmento | Condición |
|---|---|
| Cliente VIP | Gastó más de 2000 y compró al menos 10 veces. |
| Cliente Frecuente | Gastó al menos 1000 o compró al menos 6 veces. |
| Cliente Ocasional | Cualquier otro caso. |

### 6. Validación de Calidad de Registro

Evalúa un registro con los siguientes datos:

```python
edad_usuario = 17
pais = "PE"
```

**Tareas:**

Usando condicionales anidados:

1. Verifica primero si el país es `"PE"`, `"CL"` o `"CO"` (países habilitados).
2. Si el país está habilitado, verifica si el usuario es mayor o igual a 18 años:
   - Si cumple: imprime `"Registro válido para análisis"`.
   - Si no cumple: imprime `"Descartado: menor de edad"`.
3. Si pertenece a otro país, imprime `"Descartado: fuera de región"`.

---

# Sección 4: Bucles `while` y `for`

### 7. Ingesta y Validación por Consola (`while`)

Simula la carga manual de lotes de producción pidiendo cantidades enteras mediante `input()` hasta que el usuario ingrese `0` para finalizar.

**Tareas:**

- Si ingresa un número negativo, muestra un aviso y usa `continue` para ignorarlo sin sumarlo.
- Si ingresa `0`, finaliza el proceso.
- Al terminar, imprime:
  - La suma total de unidades válidas.
  - Cuántos lotes válidos se registraron.

### 8. Análisis de Serie Temporal de Ventas (`for` y `range`)

Dada la lista de ventas diarias de una semana:

```python
ventas_semana = [1200, 1450, 980, 1600, 1750, 2100, 1900]
```

**Tareas:**

Recórrela usando `range(len(ventas_semana))` para imprimir:

- El número de día (del 1 al 7).
- La venta del día.
- Si estuvo por encima o por debajo de la meta diaria de 1500.

### 9. Conteo de Caracteres y Códigos de Error (`for` en strings)

Dado el registro de eventos de un sistema:

```python
log_estados = "EEOOEOOOEEEOOEO"
```

Donde:
- `E` = Error.
- `O` = Operativo.

**Tareas:**

Recorre el registro con un bucle `for` para:

- Contar cuántos errores ocurrieron.
- Contar cuántas operaciones exitosas ocurrieron.
- Calcular el porcentaje de fallos del sistema.

---

# Sección 5: Estructuras de Datos y Métodos (Listas, Tuplas y Diccionarios)

### 10. Limpieza y Ordenamiento de Lista de Precios

Tienes la siguiente lista:

```python
precios_muestra = [49.9, 120.0, 49.9, 85.5, 310.0, 15.0]
```

**Tareas:**

Aplica métodos de listas para:

a. Agregar `99.0` al final.

b. Insertar `60.0` en el índice `1`.

c. Eliminar la primera aparición de `49.9`.

d. Contar cuántas veces quedó `49.9`.

e. Ordenar la lista de mayor a menor e imprimirla.

### 11. Inmutabilidad y Desempaquetado de Tuplas

Dada la tupla con las coordenadas y altitud de una estación meteorológica:

```python
estacion_lima = (-12.0464, -77.0428, 154)
```

**Tareas:**

- Desempaqueta sus valores en tres variables:
  - `latitud`
  - `longitud`
  - `altitud_msnm`
- Consulta el índice del valor `154` usando `.index()`.
- Imprime un resumen formateado.

### 12. Consolidación de Dataset con Diccionarios

Copia el siguiente diccionario inicial:

```python
producto = {
    "sku": "LP-102",
    "categoria": "Laptops",
    "stock": 18,
    "precio": 3200.0
}
```

**Tareas:**

Realiza las siguientes operaciones utilizando métodos de diccionarios:

1. Usa `.get()` para consultar la clave `"descuento"`, devolviendo `0` por defecto.
2. Actualiza el `"stock"` a `15`.
3. Añade `"marca": "Lenovo"` mediante `.update()`.
4. Elimina `"categoria"` con `.pop()`.
5. Finalmente, recorre `.items()` con un `for` para imprimir cada clave y valor restante.

---

**FIN DEL EXAMEN**

*Python Básico 1 · Examen Práctico (Google Colab)*