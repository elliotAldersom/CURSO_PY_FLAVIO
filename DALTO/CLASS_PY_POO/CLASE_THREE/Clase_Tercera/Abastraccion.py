""" 
Abstracción como concepto de POO:
De forma básica la Abstracción significa manejar la complejidad ocultando todos 
los detalles innecesarios al programador o al usuario y dándole solo las funicionalidades
relevantes. Es como crear un interfaz simple que oculte el interfaz compleja

"""

class Auto:
    def __init__(self ):
        self.__estado = "apagado"
    
    @property
    def Mostrar_Estado(self):
        return self.__estado
    
    def encender(self):
        self.__estado = "encendido"
        print("El auto está encendido")
    
    def conducir(self):
        if self.__estado == "apagado":
            self.encender()
        print("Conduciendo el carro")
    def parar(self):
        if self.__estado == "encendido":
            self.__estado = "apagado"
            print("El auto se detuvo...")
        else:
            print("El auto nunca estuvo encendido, por ende ya está detenido...")


mi_auto = Auto()

mi_auto.encender()
mi_auto.parar()
mi_auto.conducir()
mi_auto.parar()
print(mi_auto.Mostrar_Estado)
mi_auto.parar()


""" 
Abstracción:
Clases Abstractas:
- Es una clase que no podemos instanciar, pero es como una receta o plantilla
para poder crear clases a partir de esa plantilla:
EJM:
- Tengo la clase Persona y la puedo usar para definir que cosas tiene un persona como
el nombre, edad, nacionalidad, etc..
Y definir que cosas hace una persona como ver, caminar, correr, hablar, etc..

- Esta clase Persona sería la plantilla y luego creo una clase Estudiante, Jefe,
Trabajador, Artista, todo usarán la plantilla de Persona, es como herencia pero
es un poco más coplejo porque con herencia si tengo clase Persona y heredo a otras clases
puedo igual crear un objeto persona; pero con las clases abstractas no podría crear
un objeto persona, pues la clase abstracta es como una recetca, modelo o plantilla
para todas las demás clses.


Método Abstracto:
- Un método Abstracto es un método que está declarado en la plantilla (clase Abstracta)
pero no tiene ninguna implementación, por decir tengo el método hacer sonioo, pero
no lo implemento, no creo el código de este método, solamente lo dejo ahí, para
cuando cree otra clase que herede de esta clase Abstracta lo pueda implementar.


Termino Implementación:
- Implementar un termino significa definir como va a funcionar, por ejemplo
creo un método que se llame "hacer_sonido" , para hacer una implementación del
método sonido debo de hacer un código que haga sonio (para un gato es miau o perro
guau) , entonces implementar es definir el conjunto de instucrrciones que va a 
realizar un método

"""
#__________________________________________________________________________________________________
# Para empezaar importamos el módulo abc
""" 
Explicación:
from abc import ABC, abstractmethod

1) ABC (Abstract Base Class)
- Es una clase base proporcionda por el módulo abc (Abstract Base Clases) en Python.
Sirve para declarar clases Abstractas
- Se usa como base para crear clases Abstractas. Una clase Abstracta es una clase que no
puede ser instanciada directamente, sino que se utiliza como base para otras clases.
Las clases que heredan de ABC pueden tener método Abstractos (métodos que deben de 
ser implementados en las clases hijas).

EJM:
from abc import ABC

class MiClaseAbstracta(ABC):
    pass



2) abstractmethod  (Método Abstracto)
- Es un decorador que se aplica a un método dentro de una clase que hereda de ABC.
Indica que ese método no tiene implementación en la clase base y debe ser implementado
por las clases hijas.
Se usa para definir método Abstrctos que las clases hijas deben de sobrescribir o implementar.
Si una clase hija no implementa un método marcado como abstractethod, se generará un error al 
intentar instancir esa clase.

EJM:
from abc import ABC, abstractmethod

class MiClaseAbstracta(ABC):
    @abstractmethod
    def metodo_abstracto(self):
        pass



3) Combinación: @classmethod y @abstractmethod

- Cuando combinas ambos decoradores, el método se convierte en un 
método abstracto de clase. Esto significa que cualquier clase hija debe 
implementar este método de clase, que actuará sobre la clase en lugar de una 
instancia.

EJM:
from abc import ABC, classmethod, abstractmethod

class MiClaseAbstracta(ABC):
    @classmethod
    @abstractmethod
    def metodo_abstracto(cls):
        pass



"""
from abc import ABC, abstractmethod

# Creamos Nuestra Plantilla
class Persona(ABC):
    @abstractmethod
    def __init__(self, nombre, edad, sexo, actividad ):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.actividad = actividad
    
    # CREAR MÉTODO ABSTRACTO:
    @abstractmethod
    def Hacer_Actividad(self):
        pass
    
    # CREAR UN MÉTODO GENÉRICO:
    def Presentarse(self):
        return f"Hola me llamo {self.nombre} y tengo {self.edad} años."


# Crear las Clases Hijas:
class Estudiante(Persona):
    def __init__(self, nombre, edad, sexo, actividad):
        super().__init__(nombre, edad, sexo, actividad)
    
    def Hacer_Actividad(self):
           return f"{self.nombre} está estudiando cursos de {self.actividad}"


class Trabajador(Persona):
    def __init__(self, nombre, edad, sexo, actividad, salario):
        super().__init__(nombre, edad, sexo, actividad)
        self.salario = salario
    
    def Hacer_Actividad(self):
           return f"{self.nombre} está trabajando en el rubro de:  {self.actividad}"
    
    def Decir_Sueldo(self):
        return f"Mi sueldo es de {self.salario}"


Silva = Estudiante("Flavio", 18 , "masculino", "programación")
presentacion = Silva.Presentarse()
print(presentacion) 
result = Silva.Hacer_Actividad()
print(result) 

print("_____________________________________________________")

Estrada = Trabajador("Flavio" , 18 , "masculino" , "programación", 12000)
presentacion = Estrada.Presentarse()
print(presentacion)
result = Estrada.Hacer_Actividad()
print(result)
print(Estrada.Decir_Sueldo())
