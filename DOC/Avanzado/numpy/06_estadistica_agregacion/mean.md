# `numpy.mean`

```python
# NO EJECUTAR (Firma oficial de la API en NumPy 2.x)
numpy.mean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True)
```

## 2. ¿Qué es?

Es una **función de reducción estadística** que computa la media aritmética a lo largo de un eje.

## 3. ¿Para qué sirve?

Calcula promedios analíticos en datos multidimensionales.

## 4. ¿Cómo funciona?

1. Suma los valores en precisión flotante y divide por el conteo de elementos evaluados.

## 5. Parámetros

| Parámetro | Tipo | Obligatorio | Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `a` | arreglo | Obligatorio | Posicional | Arreglo a promediar. |
| `axis` | `int`, tupla | Opcional | `None` | Eje de reducción. |

## 6. Retorno

Escalar o `numpy.ndarray`.

## 7. Ejemplos en tres niveles

### Nivel 1: Básico

```python
import numpy as np
print(np.mean([10, 20, 30]))
```

**Salida real:**

```text
20.0
```

---

### Nivel 2: Intermedio

```python
import numpy as np
m = np.array([[10, 20], [30, 40]])
print('Promedio por columna:', np.mean(m, axis=0))
```

**Salida real:**

```text
Promedio por columna: [20. 30.]
```

---

### Nivel 3: Avanzado

```python
import numpy as np
datos = np.array([10.0, np.nan, 30.0])
# nanmean ignora valores NaN
print('Promedio seguro con nanmean:', np.nanmean(datos))
```

**Salida real:**

```text
Promedio seguro con nanmean: 20.0
```

## 8. Errores frecuentes y casos borde

1. Arreglos con valores `NaN`: `np.mean` retorna `NaN`. Usar `np.nanmean()`.

## 9. Buenas prácticas y rendimiento

* Usar `np.nanmean` si los datos pueden contener valores nulos.

## 10. Métodos relacionados

* `median` — Mediana robusta.

## 11. Referencias oficiales

* **API Reference:** [`numpy.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html) (NumPy 2.x).
