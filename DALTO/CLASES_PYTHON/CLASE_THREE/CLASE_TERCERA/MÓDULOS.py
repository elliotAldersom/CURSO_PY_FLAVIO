"""

MÓDULO:

¿QUÉ ES?
-UN MÓDULO ES CUALQUIER "ARCHIVO.py" --> EXTENSIÓN py(python)
- EN ESTE CASO, MI MÓDUO ES: MÓDULOS.py (extensión py --> Python).

COSAS QUE PODEMOS HACER:
- PODEMOS LLAMAR A UN MÓDULO DESDE OTRO MÓDULO
- PODEMOS CREAR UN MÓDULO DESDE OTRO, A ESTO SE LE CONOCE "COMO MÓDULOS ANIDADOS" O "SUBMÓDULOS"


TIPOS.
- MÓDULOS DE PYTHON (PYTHON MODULES):
-> SON LOS MÓDULOS QUE YA HECHOS O INCORPORADOS EN PYTHON (CREADOS EN EL LENGUAJE "C")

- MÓDULOS DE TERCEROS (THIRD PARTY MODULES)
-> SON LOS MÓDULOS QUE DESCARGAMOS EN INTERNET (LOS QUE UN USUARIO PUEDE REALIZAR,
LO SUBE A INTERNET Y NOSOTROS LO DESCARGAMOS, PUEDEN SER CÓDIGOS DE UNA EMPRESA,
INCLUSO LIBRERÍAS, LAS CUALES DESCARGAMOS).

- MÓDULOS PROPIOS (OWN MODULES)
->SON LOS MÓDULOS QUE NOSOTROS HACEMOS NOSOTROS

TIPOS DE IMPORTACIÓN:

name_modulo --> NOMBRE DEL MÓDULO.

1) IMPORTAR TODO EL MÓDULO:

import name_modulo

2) IMPORTAR SOLO PARTES ESPECÍFICAS DEL MÓDULO: (ES LO MÁS RECOMENDABLE)
NOS AYUDA A IMPORTAR LAS FUNCIONES COMO FUNCIONES Y NO COMO MÉTODOS

from name_modulo import saludo, despedida        # --> acá, saludo es una parte del módulo

3) RENOMBRAR EL MÓDULO DURANTE LA IMPORTACIÓN: 
(útil para evitar conflictos de nombres o hacer el código más corto).

import name_modulo as nombre_modules  # --> usamos el as, para cambiar el nombre del módulo: 
                                      # de name_modulo a nombre_modules.

4) IMPORTAR TODO EL MÓDULO: (considerado una mala práctica / se recomienda no hacer)

from name_modulo import *

ESTO HACE QUE NO NECESITEMOS AGARRAR LAS FUNCIONES COMO MÉTODOS, SINO USARLO COMO FUNCIÓN.


"""
# EJM: DE IMPORTAR UN MÓDULO COMPLETO:

# Acá lo estamos importando.
import DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR as MÓDULO_SALUDAR

# Acá registramos el nombre.
nombre = input("Ingresa tu nombre: ")

# Dentro de un variable
# Ponemos el nombre del módulo y en forma de método, ponemos la función a utilizar
saludo = MÓDULO_SALUDAR.saludar(nombre)

# Imprimimos
print(saludo)

#Imprimimos el tipo de dato que es
print(type(MÓDULO_SALUDAR))   # --> <class 'module'>


#________________________________________________________

# EJM DE IMPORTAR MÓDULO COMPLETO PERO CON "as":

import DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR as modulo_de_saludo


saludo = modulo_de_saludo.saludar(nombre)
print(saludo)


#____________________________________________________________

# EJM DE IMPORTAR MÓDULO PERO ESPECIFICANDO LA (S) FUNCIÓN (ES):
# Y RENOMBRANDO LOS NOMBRES DE CADA FUNCIÓN:
from DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR import saludar as saludado, despedida as bye

saludo = saludado(nombre)
print(saludo)


adios = bye(nombre)
print(adios)

#_______________________________________________________________

# EJM DE IMPORTAR TODO: 

from DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR import *

saludo = saludar(nombre)
adios = despedida(nombre)
print(f"{saludo}\n{adios}")

#__________________________________________________________________

# Para saber las propiedades y/o atributos del módulo:
from DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR import saludar as bienvenida , despedida as chao
print(bienvenida("flavio"))
print(chao("flavio"))  
print(dir(MÓDULO_SALUDAR))

# Para saber el nombre del módulo que importamos:
import DALTO.CLASES_PYTHON.CLASE_THREE.CLASE_TERCERA.MÓDULO_SALUDAR as Saludar
print(Saludar.__name__)

# Acceder al nombre de nuestros módulos principales:
print(__name__) # --> Imprime main

