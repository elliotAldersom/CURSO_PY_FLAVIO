""" 
¿Qué es el polimorfismo?
Origen Etimológico:
- Del griego "polus" que significa "muchos" y "morphé" que significa "forma".
- Por lo tanto, polimorfismo significa "muchas formas".

Definición:
- Hacer que cuando nosotros, por ejemplo le demos un método a un objeto, se comporte
diferente entendiendo que sus propiedades son diferentes.

EJM:
- Si a un perro le decimos que haga un soido, este va a ladrar.
- Si a un gato le decimos que haga un sonido, este va a maullar.

- EN POCAS PALABRAS:
- Transmitimos el mismo mensaje a diferentes objetos y cada uno responde de manera 
diferente, ya que son distintos objetos con diferentes propiedades y métodos.


"""


# POLIMORFISMO DE INCLUSIÓN:
x = 5 
x = 5.4
x = "Hola"
# Aquí x puede ser un entero, float o una cadena de texto,


class Gato:
    def Sonido(self):
        return "Miau"

class Perro:
    def Sonido(self):
        return "Guau"
    
cat = Gato()
dog = Perro()

# Polimorfismo:
# Acá pasamos el objeto y le ponemos el mismo método
# pero cada objeto responde de manera diferente según su clase.
print(cat.Sonido())  # Salida: Miau
print(dog.Sonido())  # Salida: Guau

# Polimorfismo en función:
# Acá cambiamos el objeto que pasamos como argumento y la función se comporta
# de manera diferente según el tipo de objeto que recibe.
def Hacer_Sonido(animal):
    return animal.Sonido()
print(Hacer_Sonido(cat))  # Salida: Miau
print(Hacer_Sonido(dog))  # Salida: Guau

print("\n______________________________\n")

# Usando Polimorfismo de Herencia:
""" 
Este tipo de polimorfismo se usa más en lenguajes de tipado estático,
en caso de Python que es de tipado dinámico, no es necesario hacer esto, pero 
ambas formas funcionan igual.
"""
class Animal:
    def Sonido(self):
        pass
class Gato(Animal):
    def Sonido(self):
        return "Miau"

class Perro(Animal):
    def Sonido(self):
        return "Guau"
    
cat = Gato()
dog = Perro()

print(cat.Sonido())  # Salida: Miau
print(dog.Sonido())  # Salida: Guau

def Hacer_Sonido(animal):
    return animal.Sonido()
print(Hacer_Sonido(cat))  # Salida: Miau
print(Hacer_Sonido(dog))  # Salida: Guau

print("\n______________________________\n")

# Polimorfismo de Coerción:
""" 
Es un tipo de polimorfismo que permite la transformación 
automática o manual de un tipo de dato a otro
"""

num1 = 3
num2 = 4.4
result = num1 + num2  # Aquí Python convierte automáticamente num1 a float
print(result)  # Salida: 7.4

print(type(num1))  # Salida: <class 'int'>
print(type(num2))  # Salida: <class 'float'>
print(type(result))  # Salida: <class 'float'>



def Recorrer(coleccion):
    for item in coleccion:
        print(f"El elemento actual es: {item}")
        print(type(item))
    
    else: 
        
        print("\n")

lista = [1, 2, 3, 4, 5]
lista2 = ["a", "b", "c", "d", "e"] 
Recorrer(lista)
Recorrer(lista2)



# Duck Typing:
""" 
¿Qué es el Duck Typing?
-En programación, el duck typing, o tipado de pato, es un concepto donde 
el tipo de un objeto se determina por su comportamiento 
(los métodos y atributos que posee) en lugar de su clase explícita.


- Es un concepto de Python (y otros lenguajes dinámicos) que no se enfoca 
en el tipo de objeto, sino en si ese objeto tiene el comportamiento que se espera.

🦆 Viene del dicho:

“Si camina como un pato, nada como un pato y hace cuac como un pato… 
probablemente sea un pato.”

🔧 En programación:
No importa si el objeto es un Perro, Gato, Persona, etc.
Si tiene el método que se espera, Python lo acepta.

- En lugar de confirmar si un objeto es una instancia de una clase específica 
(como Pato o Ganso), el duck typing se enfoca en si el objeto tiene los métodos 
y atributos necesarios para realizar una tarea. 

- Enlaces dinámicos:
-Ocurre en tiempo de ejecución.
Python decide en el momento de correr el programa qué versión del método se va a ejecutar.

✅ En Python, toda llamada a método es dinámica por defecto.

- Enlaces estáticos:
-Ocurre en tiempo de compilación.
El compilador ya sabe qué método se va a llamar, porque está definido y no cambiará.

🛑 Esto ocurre en lenguajes como Java o C++, 
donde los tipos están definidos y el método se resuelve en tiempo de compilación 
(salvo que sea virtual o override).

- Tipo Real:

🔹 Es el tipo verdadero del objeto en memoria, es decir, 
de qué clase fue creado realmente.

Ejemplo:

python
Copiar
Editar
class Animal:
    pass

class Perro(Animal):
    pass

mi_mascota = Perro()
Aquí, aunque mi_mascota parece ser un Animal, en realidad fue creado como un Perro.

🔹 Tipo real: Perro


- Tipo Declarado:

Es el tipo que tú especificas al declarar una variable u objeto.

👉 En lenguajes como Java o C++, es obligatorio.

java
Copiar
Editar
Animal a = new Perro();
Tipo declarado: Animal

Tipo real: Perro

👉 En Python, no es obligatorio, pero puedes usar anotaciones:

python
Copiar
Editar
def hacer_sonido(animal: Animal):  # tipo declarado: Animal
    return animal.Sonido()
    
 
 
___________________________________________________________

class Animal:
    def Sonido(self):
        pass


class Perro(Animal):
    def Sonido(self):
        return "Guau"
    
dog = Perro()   
    
- Según el curso de Python en POO en Soy Dalto
el ipo real para Perro es Animal, pues es la clase base (superclase) de Perro.
    
- Y el declardo es Perro, y con esto creamos el objeto dog.
    
"""


