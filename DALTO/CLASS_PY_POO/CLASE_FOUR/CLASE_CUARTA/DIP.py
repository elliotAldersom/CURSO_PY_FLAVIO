""" 
DIP: Dependency Inversion Principle (Principio de Inversión de Dependencia)
- Establece dos cosas: 
1) "Los módulos de alto nivel no tienen que depender de los de bajo nivel, sino que los
dos deben de depender de las abstracciones." 

2) "Las abstracciones no dependen de los detalles, sino los detalles de las abstracciones."

- Es decir, no debemos de depender de implementaciones específicas, o sea no debemos de depender de una 
función en particular, o de algún code que haga algo, sino que tenemos que depender de interfaces más complejas,
de cosas más grandes, no podemos hacer que una calculadora dependa de una función porque sino se rompe, tenemos
que hacer que dependa de una clase más grande que quizás abarque toda la calculadora, de esta forma las clases
de más alto nivel (las que contienen toda lógica) se mantengan independiente de las de bajo nivel (que son las que 
realizan tareas específicas), esto nos pemite ser más flexible, permite cambiar las implementaciones sin afectar
a nada que esté por encima de ellas, además facilitan el testeo, además podemos introducir implementaicones "mod" 
o "falsas" en lugar de las implementaciones reales, lo cual es muy util.

"""
""" 
Acá justo vemos, que CorrectorOrtografico depende de Diccionario,
pues vamos a ajustar toda la lógica a esta clase Diccionario en el método
de Corregir_texto, y no puede ser así, pues lo principal es el
CorrectorOrtografico y Diccionario es más pequeño y mínimo, no podemos
hacer que todo el programa depende de esto...
"""
class Diccionario:
    def Verifica_palabra(self, palabra):
        # Toda la lógica para verificar dicha palabra.
        pass


class CorrectorOrtográfico:
    def __init__(self):
        self.diccionario = Diccionario()
    
    def Corregir_texto(self, texto):
        # Usamos el diccionario para corregir el texto
        pass
    
# Por ello vamos a hacerlo de otra manera:

from abc import ABC, abstractmethod

# Hacemos una clase Abstracta
class VerificadorOrtografico(ABC):
   @abstractmethod
   def Verificar_palabra(self, palabra): 
        pass 

# Ahora creamos una clase de Diccionario y hacemos su implementaición
class Diccionario(VerificadorOrtografico):
    def Verificar_palabra(self, palabra):
        # Lógica para verificar palabra si está en el diccionario...
        pass

# Ahora creamos una clase de ServicioOnline y hacemos su implementaición
class ServicioOnline(VerificadorOrtografico):
    def Verificar_palabra(self, palabra):
        # Lóica para verificar palabras desde el servicio web
        pass

# Ahora hacemos la clase principa, que se encarga de corregir
# vamos a pasarle un "verificador" sea de Diccionario y se ServicioOnline
class CorrectorOrtografico:
    def __init__(self, verificador):
        self.verificador = verificador
    
    def Corregir_texto(self, texto):
        # Usamos el verificador para corregir texto
        pass

corrector = CorrectorOrtografico(Diccionario())
corrector = CorrectorOrtografico(ServicioOnline())