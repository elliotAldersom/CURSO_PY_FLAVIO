""" 
TEMA: HERENCIA MÚLTIPLE Y MRO
TÍTULO: Ejercicio de Herencia Multiple y MRO

- Imagina que estás modelando animales en un zoológico. Crear tres clases:
Animal , Mamifero y Ave. La clase Animal debe tener un método llamado "Comer". 
La clase Mamífero debe tener un método llamado "Amamantar" y la clase 
"Ave" un método llamado "Volar".
 
Ahora, crea una clase "Murcielago" que herede de Mamífero y Ave, en ese orden, y por 
lo tanto debe ser capaz de Amamantar y Volar, además de Comer.

Finalmente, juega con el orden de herencia de la clase Murcielago y observa cómo
cambia el MRO (Método de Resolución de Orden) y el comportamiento de los métodos al usar
super().
"""

class Animal:
    def Comer(self):
        return "El animal está comiendo."

class Mamifero(Animal):
    def Amamantar(self):
        return "El mamífero está amamantando."

class Ave(Animal):
    def Volar(self):
        return "El ave está volando."
    
class Murcielago(Mamifero, Ave):
    pass

murcielago = Murcielago()

print(murcielago.Comer()) # Método de la clase Animal
print(murcielago.Amamantar())  # Método de la clase Mamífero
print(murcielago.Volar())  # Método de la clase Ave

print(Murcielago.mro())  # Mostrando el MRO de la clase Murcielago