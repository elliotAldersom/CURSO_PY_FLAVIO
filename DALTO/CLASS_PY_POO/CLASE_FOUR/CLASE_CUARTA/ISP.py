""" 
ISP: Interface Segregation Principle (Principio de Segregación de Interfaces)
- Nos dice "Ningún cliente debe de ser forzado a depender de interfaces que no utilice"
Es decir, tenemos que eliminar las dependencias que no vamos a utilizar, o sea no forcemos 
al cliente a que dependa de interfaces que no usamos, en Python las interfaces se aplican de
una forma diferente  
Podeos decir que si un objeto proporciona ciertos métodos con ciertos nombres, puede ser tratado
como interfaz
"""

# EN ESTE CASO CON INTERFAZ NOS REFERIMOS A CLASES ABSTRACTA
from abc import ABC , abstractmethod

class Trabajador(ABC):
    
    @abstractmethod
    def comer(self):
        pass
    
    @abstractmethod
    def trabajar(self):
        pass
    
    @abstractmethod
    def dormir(self):
        pass


class Humano(Trabajador):
    
    def comer(self):
        return "El humano está comiendo"
    
    def trabajar(self):
        return "El humano está trabajando"
    
    def dormir(self):
        return "El humano está durmiendo"
    

class Robot(Trabajador):

    def comer(self):
        pass
    
    def trabajar(self):
        return "El robot está trabajando"

    def dormir(self):
        pass

robot = Robot()
print(robot.comer())
print(robot.trabajar())
print(robot.dormir())


# En este caso anterior violamos el principio de segregación de interfaz
# Para solocuinarlo, debemos de dividir el interfaz en interfaces más pequeñas


class Trabajador(ABC):
    @abstractmethod
    def trabajar(self):
        pass

class Comedor(ABC):
    @abstractmethod
    def comer(self):
        pass

class Durmiente(ABC):
    @abstractmethod
    def dormir(self):
        pass 

class Humano(Trabajador, Comedor , Durmiente):
    
    def trabajar(self):
        return "El humano está trabajando"
    
    def comer(self):
        return "El humano está comiendo"
    
    def dormir(self):
        return "El humano está durmiendo"

class Robot(Trabajador):
    
    def trabajar(self):
        return "El robot está trabajando"

bot = Robot()
print(bot.trabajar())

humano = Humano()
print(f"{humano.comer()}\n{humano.dormir()}\n{humano.trabajar()}")