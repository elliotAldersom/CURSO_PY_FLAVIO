#  SRP (Principio de Responsabilidad Única) /  (Single Responsability Principle)
""" 
- Este principio establece algo muy básico:
" Una Clase tiene que tener una y solo una razón para cambiar."

    - Esto signfica que cada clase tiene que tener una única responsabilidad o tarea,
    miremos a las clases como personas que cada una tiene su tarea, si alguien hace marketing
    que haga solo eso, si uno programa que solo haga eso, lo mismo es con las clases, cada uno
    en su única responsabilidad, y si nos damos cuenta que esa clase debe de hacer más cosas, 
    separamos esa clase según las tareas que deben de hacerse y cada una cumple una funcionalidad
    diferente, porque ayuda a evitar sobrecarga, es mejor mantenible y legible, algo importante,
    esa clase o cada clase, puede hacer su tarea sin depender de otras clases.

"""
# Esta es la forma común de hacer un clase, pero no cumple con el SRP.
class Auto: 
    def __init__(self):
        self.posicio = 0 
        self.combustible = 100
    
    def mover(self, distancia):
        if(self.combustible >= distancia/2):
            self.posicio += distancia
            self.combustible -= distancia/2
            print(f"La posición actual del auto es {self.posicio} y resta {self.combustible} de combustible.")
        else:
            print("No hay combustible suficiente...")
    
    def agrega_combustible(self, cantidad):
        if cantidad > 0:
            self.combustible += cantidad
            print(f"Ahora tienes {self.combustible} de combustible.")
        else:
            print("Ingrese una cantidad válida...")
    
    def obtenr_combustible(self):
        return self.combustible

""" 
Como dije, esta clase no cumple con SRP, ya que el code es corto, pero
si fuera un proyecto de vida real, solo para hacer mover el auto se usa mucho code, 
la forma óptima serpia dividir en partes para que cumplan con SRP.
"""


# Usaremos el SRP:
""" 
Con lo que hacemos ahora es, una clase Auto, el cual crear al auto, pero
se le pasa un objeto de clase TanqueDeCombustible, el cual es el combustible
del auto:

- La Clase Auto, tiene el método mover, en el cual se usa una pequeña validación,
y se va modificando los valores de cada atributo.

- La clase TanqueDeCombustible tiene el atributo de combustible (inicia en 100),
métodos de agregar_combustible, obtener_combustible y usar_combustible con un parámetro de cantidad

"""

# Ahora creamos la clase de TanqueDeCombustible
class TanqueDeCombustible:
    # Usamos el constructor para crear el objeto de tanque (100)
    def __init__(self):
        self.combustible = 100
    
    # Usamos el método de agregar_combustible
    def agregar_combustible(self, cantidad):
        # Hacemos una condición para poder agregar al combustible
        if cantidad > 0:
            self.combustible += cantidad
            print(f"Estás agregando {cantidad} de combustible al tanque.\nEstado de Combustible: {self.obtener_combustible()}")
        # Si no pasa, se ejecuta el else
        else:
            print("Estás pasando un número negativo para agregar...")
    
    # Ahora el método de obtener_combustible   
    def obtener_combustible(self):
        # Retorna el nivel de combustible
        return self.combustible

    # Ahora el método de usar_combustible (se pasa una cantidad como argumento)
    def usar_combustible(self, cantidad):
        # Se resta con la cantidad para obetener el total
        self.combustible -= cantidad
    
    # Hacemos un método para ver como se muestra el objeto en Str al imprimir el objeto
    def __str__(self):
        return f"{self.combustible}"


# Creamos la clase Auto (se le pasa un objeto como argumento)
class Auto: 
    # Hacemos el constructor para crear el objeto
    def __init__(self, tanque):
        self.posicion = 0 
        self.tanque = tanque
    
    # Hacemos e método de mover, se le pasa la distancia como argumento  
    def mover(self, distancia):
        # Verificamos si el tanque es mayor o igual a la distancia entre 2
        if(self.tanque.obtener_combustible() >= distancia/2):
            # Si pasa, la posición se le suma la dsitancia
            self.posicion += distancia
            # Se usa el método de usar_combustible el cual resta con la distancia
            # en este caso a la distancia se divide entre 2
            self.tanque.usar_combustible(distancia/2)
            print(f"La posición actual del auto es {self.posicion} y resta {self.tanque.obtener_combustible()} de combustible.")
        # En caso de que no pasa en el if, se ejcuta el else
        else:
            print("No hay combustible suficiente...")
    
    # Hacemos un método para obtener la posición
    def obtener_posicion(self):
        return self.posicion
    
    # Hacemos un método para ver como se muestra el objeto en Str al imprimir el objeto
    def __str__(self):
        return f"Posición: {self.posicion} / Tanque: {self.tanque}"

   
# Primero creamos el objeto de TanqueDeCombustible     
tanque =  TanqueDeCombustible()

# Luego creamos el objeto de Auto y le pasamos como argumento al objeto tanque
coche = Auto(tanque)

# Obtenemos la posición del auto
print(coche.obtener_posicion())

# Vamos a usar el método de mover y pasamos como argumento la distancia
coche.mover(30)

# Usamos el método de agregar_combustible y pasamos argumento de númro positivo
tanque.agregar_combustible(12)

# Otra ves usamos el método de mover con argumento de 30 como distancia
coche.mover(30)
coche.mover(160)
# Vamos a imprimir el objeto coche y se verá el Str de tanque y coche
print(coche) # --> Muestra en str a Auto y TanqueDeCombustibe