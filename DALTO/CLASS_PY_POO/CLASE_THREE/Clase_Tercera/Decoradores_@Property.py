"""
Usamos el @property
para decirle a Python que vamos acceder a los Getters o incluso
Setters como si fueran una propiedad, o sea sin necesidad de los 
paréntesis () :

Sin @property:

def get_nombre(self):
    return self.__name
    
nombre = flavio.get_nombre()   # Salida: Flavio


Con @property:
@property
def nombre(self):
    return self.__name
    
nombre = flavio.nombre   # Salida: Flavio


De esta forma hacemos con los Setters:

es: @Nombre_Propiedad.setter 

@nombre.setter
    def nombre(self, new_name):
        self.__name = new_name
"""

class Persona:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    
    @property
    def nombre(self):
        return self.__name
    
    @property
    def edad(self):
        return self.__age
    
    @nombre.setter
    def nombre(self, new_name):
        self.__name = new_name
     
    @edad.setter 
    def edad(self, new_age):
        self.__age = new_age
        
    @property
    def Borrar_Datos(self):
       pass
    
    @Borrar_Datos.deleter
    def Borrar_Datos(self):
        print("Borrando los Datos")
        del self.__name
        del self.__age   
        print("Datos borrados con exito...") 
   
flavio = Persona("Flavio", 18)

nombre = flavio.nombre
print(nombre)  # Salida: Flavio

edad = flavio.edad
print(edad)  # Salida: 18


# Modificando el nombre y la edad usando setters
flavio.nombre = "Gerardo"
flavio.edad = 19
new_nombre = flavio.nombre
print(new_nombre)  # Salida: Gerardo

new_edad = flavio.edad
print(new_edad)  # Salida: 19

del flavio.Borrar_Datos

#print(flavio.nombre)