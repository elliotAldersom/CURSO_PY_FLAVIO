print("DECORADORES MULTIPLES")
"""  ES CUANDO SE APLICA MÁS DE UN DECORADOR A UNA FUNCIÓN O CLASE """
# EJM CON FUNCIÓN: 

def decorador_1(func):
    def wrapper(*args, **kwargs):
        print("Antes de la función (Decorador 1)")
        func(*args, **kwargs)
        print("Después de la función (Decorador 1)")
    return wrapper


def decorador_2(func):
    def wrapper(*args, **kwargs):
        print("Antes de la función (Decorador 2)")
        func(*args, **kwargs)
        print("Después de la función (Decorador 2)")
    return wrapper

@decorador_1
@decorador_2
def saludo():
    print("¡Hola Mundo!")

# Llamada a la función decorada
saludo()


""" 
Imprime:

DECORADORES MULTIPLES
Antes de la función (Decorador 1)  
Antes de la función (Decorador 2)  
¡Hola Mundo!
Después de la función (Decorador 2)
Después de la función (Decorador 1)


EXPLICACIÓN:
1. Cuando se llama a saludo(), primero se ejecuta decorador_1 (Pue está más lejos de la función,
el decorador_1 envuelve al decorador_2 el cual decora a la función).
     - Por ello se muestra primero "Antes de la función (Decorador 1)".
     y luego se muestra "Antes de la función (Decorador 2)" ya que está más cerca de 
     la función a decorar y decoraro_1 envuelve a decorador_2 (estás más externo o lejos 
     de la función a decorar).
2. Luego se ejecuta la función saludo(), mostrando "¡Hola Mundo!".
3. Después se muestra "Después de la función (Decorador 2)".
     - Ya que está más cerca de la función a decorar.
     (Se aplica el mismo razonamiento que en el punto 1 pero al revés).
     
- Lo mismo sería con más de N número de decoradores (misma lógica,
empieza por el más externo y luego el más cercano).
"""

print("________________DECORADOR MULTIPLE__________________________\n")

def Decorador_edad(f):
    def wrapper(*args, **kwargs):
        print("Verificando la edad...")
        edad = f(*args, **kwargs)
        result = "Mayor de edad" if edad >= 18 else "Menor de edad"
        return result
    return wrapper

def Decorador_extra(f):
    def wrapper(*args , **kwargs):
        verificar = f(*args, **kwargs)
        result = "Puede entrar" if  verificar == "Mayor de edad" else "No puede entrar"
        result = f"Resultado de la verificación: {result}"
        return result
    return wrapper

@Decorador_extra
@Decorador_edad
def Obtener_edad():
    while True:
        try: 
            
            age = int(input("Ingrese su edad: "))
            if age <=0:
                print("Error: La edad debe ser un número positivo.")
                continue
            elif age > 120:
                print("Error: La edad ingresada está fuera de un rango válido.")
                continue
            else:
                print("Edad Ingresada")
                return age
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nError: Debe ingresar un número entero.")
            
resultado = Obtener_edad()
print(resultado)



print("________________DECORADOR MULTIPLE DE CLASES________________\n")


class Person:
    def __init__(self, name, age, city, ocupacion):
        self.__name = name
        self.__age = age
        self.__city = city
        self.__ocupacion = ocupacion
    
    # Definir getters para acceder a los atributos privados
    @property
    def name(self):
        return self.__name
    @property
    def age(self):
        return self.__age
    @property
    def city(self): 
        return self.__city
    @property
    def ocupacion(self):
        return self.__ocupacion

    # Definir setters para modificar los atributos privados
    @name.setter
    def name(self, name):
        self.__name = name
    
    @age.setter
    def age(self, age):
        self.__age = age
    
    @city.setter
    def city(self, city):
        self.__city = city
    
    @ocupacion.setter
    def ocupacion(self, ocupacion):
        self.__ocupacion = ocupacion
    
    
def Decorador_info():
    
    def wrapper(cls):
        class Super_Person(cls):
            def __init__(self, name, age, city, ocupacion, altura, peso):
                super().__init__(name, age, city, ocupacion)
                self.__altura = altura
                self.__peso = peso
            
            # Definir getters para acceder a los atributos privados
            @property
            def altura(self):
                return self.__altura
            @property
            def peso(self):
                return self.__peso

            # Definir setters para modificar los atributos privados
            @altura.setter
            def altura(self, altura):
                self.__altura = altura
            
            @peso.setter
            def peso(self, peso):
                self.__peso = peso
            
            # Definir el __str__()
            def __str__(self):
                dicci = {
                    "Name": self.name,
                    "Age": self.age,
                    "City": self.city,
                    "Ocupacion": self.ocupacion,
                    "Altura": self.altura,
                    "Peso": self.peso
                }

                result = "\n".join(f"{key}: {value}" for key,value in dicci.items())
                return result
        return Super_Person
    return wrapper


def Decorador_accion():
    def wrapper(cls):
        class New_Person(cls):
            def Ocupado(self):
                return f"{self.name} se ocupa de {self.ocupacion}"
            def Saludar(self):
                return f"Hola, me llamo {self.name} y tengo {self.age} años."
        return New_Person
    return wrapper
            

@Decorador_accion()
@Decorador_info()
class Persona:
    def __init__(self, name, age, city, ocupacion):
        self.__name = name
        self.__age = age
        self.__city = city
        self.__ocupacion = ocupacion
    
    # Definir getters para acceder a los atributos privados
    @property
    def name(self):
        return self.__name
    @property
    def age(self):
        return self.__age
    @property
    def city(self): 
        return self.__city
    @property
    def ocupacion(self):
        return self.__ocupacion

    # Definir setters para modificar los atributos privados
    @name.setter
    def name(self, name):
        self.__name = name
    
    @age.setter
    def age(self, age):
        self.__age = age
    
    @city.setter
    def city(self, city):
        self.__city = city
    
    @ocupacion.setter
    def ocupacion(self, ocupacion):
        self.__ocupacion = ocupacion
        
        
if __name__ == "__main__":
    print("FORMA USANDO DECORADORES APILADOS:\n")
    person = Persona("Flavio", 18, "Huaral", "Developer", 1.75, 70)
    print(person)
    print(person.Ocupado())
    print(person.Saludar())
    print(type(person))
    print("______________________________________________________________\n")
    person.name = "Gerardo"
    person.age = 19
    person.peso = 66
    person.altura = 1.70
    print(person)
    print(person.Ocupado())
    
    
    print("______________________________________________________________\n")
    print("FORMA SIN USAR DECORADORES APILADOS:\n")
    decorador_1 = Decorador_info()
    decorador_2 = Decorador_accion()
    ejecucion = decorador_2(decorador_1(Person))
    user = ejecucion("Flavio", 18, "Huaral", "Developer", 1.75, 70)
    print(user)
    print(user.Ocupado())
    print(user.Saludar())
    print(type(user))
    print("______________________________________________________________\n")
    user.name = "Gerardo"
    user.age = 19
    user.peso = 66
    user.altura = 1.70
    print(user)
    print(user.Ocupado())