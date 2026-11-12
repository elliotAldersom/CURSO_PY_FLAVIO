""" 
SI E MÓDULO A IMPORTAR ESTÁ FUERA DE LA MISMA RUTA
O SEA FUERA DE LA CARPETA O PAQUETE, EN ESTE CASO ES ASÍ:
CLASE_THREE / CLASE_TERCERA , MODULOS_IMPORT (este último contiene el módulo a importar)

Para esto usamos el: import sys
"""

import sys
print(sys) # <module 'sys' (built-in) --> Modulo construido o integredo en python

print(sys.builtin_module_names) # Devuelve una tupla con todos los nombres de todos los módulos

""" 
Esto nos sirve para saber que si creamos un módulo con el mismo
nombre de uno de estos módulos que sale al usar el:
sys.builtin_modue_names
y si tratamos importarlo, Pytohn va a dar prioridad o preferencia
a sus módulos nativos y no a los que hemos hecho nosotros.
"""

# Para saber donde están los módulos hacemos esto:
#print(sys.path) # Nos devuelve la ruta principa.

# Una vez que tengamos la ruta solo agregamos la parte que deseamos acceder
# Algo más, en vez de poner el print(sys.path)
# Podemos simplmente copiar la ruta de la carpeta que deseamos y ya (de ahí en adelante todo es igual):

"""
Esto nso puede generar falsos positivos 
sys.path.append("c:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\MODULOS_IMPORT")
"""

# FORMA ÓPTIMA
# Esto es más útil y efectivo que el anterior, ya que no genera falsos positivos:
# Solo es agregar la ruta de la carpeta raíz y ya.
sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")

print(sys.path)
#Esto nos muestra al final del código, la ruta que acabamos de agregar

# Después de hacer la forma óptima importamos simplemente el módulo que deseamos:
from DALTO.CLASES_PYTHON.CLASE_THREE.MODULOS_IMPORT.saludo_name import Saludar 

print(Saludar())
