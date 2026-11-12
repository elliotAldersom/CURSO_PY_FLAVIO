""" 
MÉTODOS ESPECIALES (MÉTODOS DUNDER)
- Son funciones que tienen un nombre especial reservdo,
inician con dos guiones bajos y terminan con dos guiones bajos (_name_)

- Están creados con la finalidad de que nosotros podamos crear funciones 
especiales que con métodos normales no podríamos crear.
"""

class Persona:
    # El método constructor es un método especial
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        
    # Otro es el __str__
    # Este nos entrega una representación del objeto en Str:
    def __str__(self):
        return f"Nombre: {self.nombre} \nEdad: {self.edad}"

    
    def __repr__(self):
        return f'Persona("{self.nombre}",{self.edad})'


one = Persona("Flavio" , 18)
print(one)
""" 
__str__(self)
- Es util, pues de esta forma mostramos al objeto
como cadena de texto, y al imprimirlo nos sale como cadena 
y es util.

print(one)
Imprime:
Nombre: Flavio 
Edad: 18 
"""

one = Persona("Flavio" , 18)

repre = repr(one)
print(repre)
resultado = eval(repre)
print(resultado) 

print(one.nombre)
print(resultado.nombre)

""" 
Que hace el repre? 
- El repre hace una representación de código Python en Str 
en mi caso es Persona("Flavio" , 18)
    - Persona es la clase
    - "Flvio" es en str 
    - 18 en int 
    - Esto lo paso en forma de argumentos: Persona("Flavio" , 18)

- Ahora el eval()
es una funcipón integrada en Python (built-in function), el cual evalua una cadena
como si fuera código Python:
    - En este caso le pasamos repre que tiene repr(one) 
    y el repr es Persona("Flavio", 18)
    y esto como código Python va a instanciar a la clase Persona y crear un objeto
    y al imprimirlo nos va a salir con str pues dentro de la clase pusimos el
    __str__(self) 
    
    Y podemos hacer:
    print(resultado.one) # --> Imprime el nombre 
    
    En estos csos crea un objeto con mismos atributo que one pero independiente
    
"""


#__________________________________________________________________________________________________

""" 
SOBRECARGA DE OPERADORES:

"""

class Persona:
    # El método constructor es un método especial
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        
    # Otro es el __str__
    # Este nos entrega una representación del objeto en Str:
    def __str__(self):
        return f"Nombre: {self.nombre} \nEdad: {self.edad}"

    
    def __repr__(self):
        return f'Persona("{self.nombre}",{self.edad})'
    
    # En este caso usaremos el __add__() para sumar edades de distintos objetos
    def __add__(self, otro):
        nuevo_valor = self.edad + otro.edad
        nuevo_valor = int(nuevo_valor)
        new_object = Persona(self.nombre + otro.nombre , nuevo_valor)
        print(f"La suma de las edades de {self.nombre} y de {otro.nombre} es de {nuevo_valor} años.")
        return new_object

        
Silva= Persona("Flavio" , 18)
Pepe = Persona("José", 20)
Luisa = Persona("Luisa",30)

result = Pepe + Silva + Luisa
print(result.edad)
print(result.nombre)
