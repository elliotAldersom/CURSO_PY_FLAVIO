""" 
TEMA: HERENCIA 
TÍTULO: Ejercicio de Herencia y uso de super
- Crear un sistema para una escuela. En este sistema, vamos a tener dos clases
principales, Persona y Estudinte. La clase Persona tendrá los atríbutos nombre y edad
y un método que imprima el nombre y la edad de la persona. La calse Estudiante heredará
de la clase Persona y también tendrá un atributo adicional llamdo grado y un método 
que imprima el grado del estudiante.

Deberás utilizar super en el método de inicilización (init) para reutilizar el código
de la clase padre (Persona). Luego crea una instancia de la clase Estudiante e imprime
sus atributos y métodos para asegurarte de que todo funciona correctamente. 
"""

class Persona:
    def __init__(self, nombre,edad):
        self.nombre = nombre
        self.edad = edad
    
    def Presentarse(self):
        return f"Mi nombre es {self.nombre} y mi edad es {self.edad} años"
    
class Estudiante(Persona):
    def __init__(self, nombre, edad, grado):
        super().__init__(nombre, edad)
        self.grado = grado
    
    def Presentarse(self):
       return f"{super().Presentarse()}, y estoy en el grado {self.grado}."
    
# Crear una instancia de Estudiante
user_one = Estudiante("Flavio", 18 , "2do")

print(user_one.nombre)
print(user_one.edad)
print(user_one.grado)

print(user_one.Presentarse()) # Usando el método de la clase hija
print(Persona.Presentarse(user_one))  # Usando el método de la clase padre
print(Estudiante.mro()) # Mostrando la jerarquía de la clase Estudiante