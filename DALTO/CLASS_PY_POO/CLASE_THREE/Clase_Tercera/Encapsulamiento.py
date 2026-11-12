""" 
¿Qué es el Encapsulamiento?
- Básicamente consiste en proteger los elementos de una clase, podemos proteger
atributos, métodos, variables, etc..

- Con esto nos ayuda a que no se pueda acceder a los atributos, métodos,
todo aquello que queramos proteger, desde fuera de la clase.
"""

class MiClase: 
    def __init__(self):
        self._atributo_privado =  "Valor"
        

user = MiClase()
print(user._atributo_privado)  # Salida: Valor

""" 
- En Python, se reconoce como atributo privado al hacer esto: (1 guión bajo)
    self._(nombre del atributo) = "valor_del atributo"

- Si bien es cierto, esto no lo hace privado (protegido), ya que se puede acceder a él, pero
de esta forma el desarrollador sabe que no debe acceder a este atributo.

- En Python en Encapsulamiento tenemos 3 tipos:
- Público:
- Protegido: (1 guión bajo)
- Muy privado (my muy Privado): (2 guiones bajos)

- En otros lenguajes hay: 
- Público: (public)
- Protegido: (protected)
- Privado: (private)
"""

class MiClase: 
    # Haciendo un atributo muy privado:
    def __init__(self):
        self.__atributo_privado =  "Valor"
    
    # Haciendo un método muy privado:    
    def __hablar(self):
        return("Hola, soy un método de la clase MiClase")
        

user = MiClase()
#print(user.__atributo_privado) # Sale error
#user = MiClase()
print(user._MiClase__atributo_privado)  # Salida: Valor
#print(user.__hablar()) # Sale error
print(user._MiClase__hablar())

""" 
- En Python, se reconoce como atributo muy privado al hacer esto: (2 guiones bajos)
    self.__(nombre del atributo) = "valor_del atributo"

user = MiClase()
print(user.__atributo_privado) # Sale error

- Se puede acceder, pero de una forma diferente:

user = MiClase()
print(user._MiClase__atributo_privado)  # Salida: Valor
"""


#___________________________________________________

""" 
Getters y Setters:

- El Getter es un método que tenemos que utilizar para acceder a un atributo 
que es muy privado o privado.

- El Setter es un método que debemos de utilizar para modificar o establecer
el valor de un atributo muy privado o privado.


"""
print("\n____________________________________________________\n")
print("Getters y Setters")

class Persona:
    def __init__(self, name, age):
        self._name = name
        self._age = age


flavio = Persona("Flavio", 18)


# AL TENER UN GUIÓN BAJO, NO DEBEMOS D ACCEDER ASÍ, AUNQUE SE PUEDA
print(flavio._name)  # Salida: Flavio
print(flavio._age)   # Salida: 18



# PARA ACCEDER DE FORMA CORRECTA SE USAR UN GETTER:
# ESTE ES EN UN CASO DE ATRIBUTO PRIVADO (PROTEGIDO)
print("\nUSANDO GETTERS:\n")
class Persona:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    def get_nombre(self):
        return self._name


flavio = Persona("Flavio", 18)

nombre = flavio.get_nombre()
print(nombre)  # Salida: Flavio


# ESTE ES EN EL CASO DE UN ATRIBUTO MUY MUY PRIVADO (PRIVADO)

class Persona:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    
    def get_nombre(self):
        return self.__name
    
    def get_edad(self):
        return self.__age


flavio = Persona("Flavio", 18)

nombre = flavio.get_nombre()
print(nombre)  # Salida: Flavio

edad = flavio.get_edad()
print(edad)  # Salida: 18



#_____________________________________________
print("\nUSANDO SETTERS:\n")
# USMAMOS UN SETTER PARA MODIFICAR UN ATRIBUTO
# PODEMOS HACERLO CON UN ATRIBUTO PROTEGIDO O PRIVADO
# FUNCIONA DE LA MISMA MANERA (1 o 2 guiones bajos según el caso)

class Persona:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    
    def get_nombre(self):
        return self.__name
    
    def get_edad(self):
        return self.__age
    
    def set_nombre(self, new_name):
        self.__name = new_name
        
    def set_edad(self, new_age):
        self.__age = new_age
    
   


flavio = Persona("Flavio", 18)

nombre = flavio.get_nombre()
print(nombre)  # Salida: Flavio

edad = flavio.get_edad()
print(edad)  # Salida: 18


# Modificando el nombre y la edad usando setters
flavio.set_nombre("Gerardo")
flavio.set_edad(19)
new_nombre = flavio.get_nombre()
print(new_nombre)  # Salida: Gerardo

new_edad = flavio.get_edad()
print(new_edad)  # Salida: 19


""" 
Si hicieramos esto:
new_nombre = flavio.set_nombre("Gerardo")
print(new_nombre)  # Salida: None

new_edad = flavio.set_edad(19)
print(new_edad)  # Salida: None

- Esto no funcionaría, ya que los setters no retornan nada, solo modifican
el valor del atributo muy privado o privado.
"""
