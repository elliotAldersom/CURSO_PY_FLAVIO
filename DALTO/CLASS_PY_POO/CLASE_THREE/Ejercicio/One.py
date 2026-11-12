""" 
Crear juego de Fusión: 
- El juego consiste en crear presonajes, un juego que esos personajes
se pueden fusionar para formar personajes más poderosos que tengan más poder

Para ello deberemos cambiar el comportamiento del operador " + " para que cuando
los personajes se fusionen, salga un nuevo personajes con habilidades mejoradas

Una posible formula es: El promedio de las habilidades de ambos al cuadrado!
"""

class Personaje:
    def __init__(self, name , fuerza , velocidad):
        self.__nombre = name
        self.__fuerza = fuerza 
        self.__velocidad = velocidad
    
    @property
    def Nombre(self):
        return self.__nombre
    
    @property
    def Fuerza(self):
        return self.__fuerza
    
    @property
    def Velocidad(self):
        return self.__velocidad
    
    @Nombre.setter
    def Nombre(self, new_name):
        self.__nombre = new_name
    
    @Fuerza.setter
    def Fuerza(self, new_fuerza):
        self.__fuerza = new_fuerza
    
    @Velocidad.setter
    def Velocidad(self, new_vel):
        self.__velocidad = new_vel
        
    def __str__(self):
        return f"Nombre: {self.__nombre}\nFuerza: {self.__fuerza}\nVelocidad: {self.__velocidad}"
    
    def __repr__(self):
        return f'Personaje("{self.__nombre}" , {self.__fuerza} , {self.__velocidad})'
    
    def __add__(self, otro):
        new_name =f"{self.__nombre} - {otro.__nombre}"
        lista_fuerza = [self.__fuerza, otro.__fuerza]
        new_fuerza = ((sum(lista_fuerza))/len(lista_fuerza))**2
        new_fuerza = round(new_fuerza)
    
        lista_vel = [self.__velocidad , otro.__velocidad]
        new_vel = ((sum(lista_vel))/len(lista_vel))**2
        new_vel = round(new_vel)
        
        new_object = Personaje(new_name , new_fuerza, new_vel)
        print(f"Al combinar los personajes tenemos los siguientes resultados:")
        return new_object


Goku = Personaje("Goku" , 200 , 12)
Vegeta = Personaje("Vegeta" , 150 , 11)
Broly = Personaje("Broly" , 120, 138)
new_personaje = Goku + Vegeta + Broly
print(new_personaje)

