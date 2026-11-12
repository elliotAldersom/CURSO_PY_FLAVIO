

class Person:
    def __init__(self, name, age, nacionalidad, color_piel, color_ojos, color_cabello):
        while True:
            try:
                name = input("Ingrese su nombre: ").strip().title()
                if len(name) > 2:
                    print("Nombre válido.")
                    break
                else:
                    print("Ingrese un nombre válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su nombe.")
            
        while True:
            try:
                age = int(input("Ingrese su edad: "))
                if age > 0:
                    print("Edad válida.")
                    break
                else:
                    print("Ingrese una edad válida.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su edad.")
        
        while True:
            try:
                nacionalidad = input("Ingrese su nacionalidad: ").strip().capitalize()
                if len(nacionalidad) > 2:
                    print("Nacionalidad válida.")
                    break
                else:
                    print("Ingrese una nacionalidad válida.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su nacionalidad.")
    
        while True: 
            try:
                color_piel = input("Ingrese el color de sus piel: ").strip().tile()
                if len(color_piel) > 2:
                    print("Color de pies válido.")
                    break
                else:
                    print("Ingrese un color de pies válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de sus piel.")
                
        while True:
            try:
                color_ojos = input("Ingrese el color de sus ojos: ").strip().title()
                if len(color_ojos) > 2:
                    print("Color de ojos válido.")
                    break
                else:
                    print("Ingrese un color de ojos válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de sus ojos.")
        
        while True:
            try:
                color_cabello = input("Ingrese el color de su cabello: ").strip().title()
                if len(color_cabello) > 2:
                    print("Color de cabello válido.")
                    break
                else:
                    print("Ingrese un color de cabello válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de su cabello.")
    
        # LLAMANDO A LOS ATRIBUTOS
        self.nombre = name
        self.edad = age
        self.nacionalidad = nacionalidad
        self.color_piel = color_piel
        self.color_ojos = color_ojos
        self.color_cabello = color_cabello
    
    
""" 
Esto es una mala práctica, pues no se debe de pedir datos al usuario dentro de una clase,
lo correcto es que se le pase los datos al crear una instancia de la clase.

Podemos hacer una función que se encargue de pedir los datos al usuario y luego crear la instancia de la clase
con los datos obtenidos.
Esto es para que la clase sea más reutilizable y no dependa de la entrada del usuario.
"""

class Person: 
    def __init__(self, name, age, nacionalidad, color_piel, color_ojos, color_cabello):
        self.nombre = name
        self.edad = age
        self.nacionalidad = nacionalidad
        self.color_piel = color_piel
        self.color_ojos = color_ojos
        self.color_cabello = color_cabello
    
    # Hacemos un método para saludar
    def saludar(self):
        print(f"Hola, soy {self.nombre}, tengo {self.edad} años y soy {self.nacionalidad}.")

# Hacmos una función para pedir los datos al usuario
def Pedir_Datos():
    
    while True:
            try:
                name = input("Ingrese su nombre: ").strip().title()
                if len(name) > 2:
                    print("Nombre válido.")
                    break
                else:
                    print("Ingrese un nombre válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su nombe.")
            
    while True:
            try:
                age = int(input("Ingrese su edad: "))
                if age > 0:
                    print("Edad válida.")
                    break
                else:
                    print("Ingrese una edad válida.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su edad.")
        
    while True:
            try:
                nacionalidad = input("Ingrese su nacionalidad: ").strip().capitalize()
                if len(nacionalidad) > 2:
                    print("Nacionalidad válida.")
                    break
                else:
                    print("Ingrese una nacionalidad válida.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar su nacionalidad.")
    
    while True: 
            try:
                color_piel = input("Ingrese el color de su piel: ").strip().title()
                if len(color_piel) > 2:
                    print("Color de piel válido.")
                    break
                else:
                    print("Ingrese un color de pies válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de sus pies.")
                
    while True:
            try:
                color_ojos = input("Ingrese el color de sus ojos: ").strip().title()
                if len(color_ojos) > 2:
                    print("Color de ojos válido.")
                    break
                else:
                    print("Ingrese un color de ojos válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de sus ojos.")
        
    while True:
            try:
                color_cabello = input("Ingrese el color de su cabello: ").strip().title()
                if len(color_cabello) > 2:
                    print("Color de cabello válido.")
                    break
                else:
                    print("Ingrese un color de cabello válido.")
                    continue
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nDebe de ingresar el color de su cabello.")
                
    # Retornamos los datos obtenidos
    return name, age, nacionalidad, color_piel, color_ojos, color_cabello

# Creamos una instancia de la clase Person
persona = Person(*Pedir_Datos()) # --> Agarra todos los datos obtenidos de la función Pedir_Datos y los pasa como argumentos a la clase Person

# O tabién:
name, age, nacionalidad, color_piel, color_ojos, color_cabello = Pedir_Datos()
# Creamos una instancia de la clase Person
persona = Person(name, age, nacionalidad, color_piel, color_ojos, color_cabello)

""" 
Esto es una buena práctica, pues la clase Person no depende de la entrada del usuario,
sino que se le pasan los datos al crear la instancia de la clase.

Hicimos una función que se encarga de pedir los datos al usuario y luego crear la instancia de la clase
con los datos obtenidos.
"""