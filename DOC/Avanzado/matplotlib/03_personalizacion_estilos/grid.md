# Matplotlib: Axes.grid

```python
# NO EJECUTAR (Firma oficial de la API en versión 3.8.x)
Axes.grid(visible=None, which='major', axis='both', **kwargs)
```

## 2. ¿Qué es?

`Axes.grid` conmuta y configura las líneas de cuadrícula cartesianas auxiliares en el fondo del lienzo.

## 3. ¿Para qué sirve?

Facilita la lectura cuantitativa inmediata de valores numéricos proyectando las marcas de los ejes X e Y a través del espacio de datos.

## 4. ¿Cómo funciona?

Itera sobre las marcas mayores (`major`) o menores (`minor`) de los objetos `Axis`, instanciando líneas segmentadas auxiliares con propiedades de estilo dadas y z-order configurable.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Por defecto | Descripción |
|---|---|---|---|---|
| `visible` | `bool` | Opcional | `None` | Si es `True`, muestra la cuadrícula; si es `False`, la oculta. |
| `which` | `'major'`, `'minor'`, `'both'` | Opcional | `'major'` | Tipo de marcas sobre las que proyectar las líneas. |
| `axis` | `'both'`, `'x'`, `'y'` | Opcional | `'both'` | Eje coordenado sobre el cual dibujar las líneas. |
| `linestyle` | `str` | Opcional | `'-'` | Estilo de trazo (`':'`, `'--'`, `'-'`). |
| `alpha` | `float` | Opcional | `None` | Nivel de opacidad/transparencia. |
| `color` | `color` | Opcional | `None` | Tonalidad de la línea auxiliar. |

## 6. Retorno

`None`. Modifica directamente la visibilidad de los artistas de cuadrícula en el eje.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 30, 20])
ax.grid(True, linestyle="--", alpha=0.6)

print(f"Estado de la cuadrícula configurado")
plt.close(fig)
```

**Salida real:**

```text
Estado de la cuadrícula configurado
```

### Nivel 2: Intermedio

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(["Grupo A", "Grupo B"], [150, 280])

# En gráficos de barra categóricos horizontales o verticales, solo se usa un eje
ax.grid(axis="y", linestyle=":", color="gray", alpha=0.7)
print(f"Cuadrícula restringida a eje Y")
plt.close(fig)
```

**Salida real:**

```text
Cuadrícula restringida a eje Y
```

### Nivel 3: Avanzado

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [100, 200, 300])

# Configuración de jerarquía de dibujo (zorder) para que los datos queden arriba
ax.set_axisbelow(True)
ax.grid(True, color="#e0e0e0", linewidth=0.8)

print(f"Axis below activado: {ax.get_axisbelow()}")
plt.close(fig)
```

**Salida real:**

```text
Axis below activado: True
```

## 8. Errores frecuentes y casos borde

- **Líneas de cuadrícula sobre los datos:** Por defecto, algunas versiones pueden dibujar la cuadrícula encima de barras o rellenos. Solución: invocar `ax.set_axisbelow(True)`.
- **Cuadrícula saturada:** Usar líneas negras sólidas (`color='black'`, `alpha=1.0`) distrae la atención de los datos.

## 9. Buenas prácticas y rendimiento

- Usar siempre tonos tenues (`alpha=0.3` a `0.6` o grises `#d3d3d3`) con estilos discontinuos (`'--'` o `':'`).
- En gráficos de barras, activar únicamente la cuadrícula perpendicular al valor numérico (`axis='y'`).

## 10. Métodos relacionados

- [set_lim](set_lim.md)
- [legend](legend.md)

## 11. Referencias oficiales

- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.grid.html
