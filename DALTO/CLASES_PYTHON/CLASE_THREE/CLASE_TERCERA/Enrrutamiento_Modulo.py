""" 
ESTAMOS HACIENDO TODO ESTO DENTRO DE UNA CAREPETA PRINCIPAL, ASÍ QUE ES VALIDA
ABSOLUTAMENTE TODO ESTÁ DENTRO DE UNA MISMA CARPETA.
CLASE_THREE / CLASE_TERCERA (Dentro de esta última están los módulos y la carpeta PAQUETE)
Vamos a importar el Modulo_Saludar que está en la carpeta PAQUETE
- Podemos aplicar lo que vimos en módulos a esta parte, o sea cambiar de nombre,
podemos importar todo el módulo, unas funciones de ellas, etc..

"""
# Vamos a importarlo y usar la función como si fuera un método
import DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.PAQUETE.Saludar 

result = DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.PAQUETE.Saludar.Saludar()
print(result)

# Vamos a importar y usar la función como tal.
from DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.PAQUETE.Saludar import Saludar

result = Saludar()
print(result)


"""

EL ENRRUTAMIENTO DE MÓDULOS CONSISTE COMO USAR MÓDULOS QUE ESTÁN FUERA DEL ALCANCE
DE LA CARPETA EN DONDE NOS ENCONTRAMOS (EJEM: CLASE_ONE / CLASE_TWO / CLASE_THREE)

PARA HACER ESTO POSIBLE HACEMOS LO SIGUIENTE: 

nombre_de_la_carpeta = el nombre de a carpeta que contiene el módulo
name_módulo = el nombre del módulo a importar
saludar= función a importar del módulo

1) IMPORTAR EL MÓDULO QUE ESTÁ EN OTRA CARPETA PERO DENTRO DE LA CARPETA PRINCIPAL:
import nombre_de_la_carpeta.name_módulo

2) IMPORTAR UNA FUNCIÓN DEL MÓDULO QUE ESTÁ EN OTRA CARPETA PERO DENTRO DE LA CARPETA PRINCIPAL:
from nombre_de_la_carpeta.name_módulo import saludar


3) IMPORTAR UN MÓDUO QUE ESTÁ EN OTRA CARPETA (FUERA DE LA PRINCIPAL DE DONDE ESTAMOS)
import sys

"""