class Animal:
    def __init__(self, tipo , color , velocidad):
        self.tipo = tipo
        self.color = color
        self.velocidad = velocidad
    
    def comer(self):
        return f"El animal de tipo {self.tipo}, está comiendo..."
    def sonido(self):
        return f"El animal está haciendo su sonido..."


class Perro(Animal):
    def __init__(self, tipo , color , velocidad, raza):
        super().__init__(tipo, color, velocidad)
        self.raza = raza
    
    def sonido(self):
        return f"El perro de raza {self.raza} está ladrando: \"Guau Guau...\""
    
animal_cualquier = Animal("Mamifero" ,  "blanco" , "rápido")

dog = Perro("Mamífero", "Negro" , "rápido", "Golden Retriever")

print(animal_cualquier.comer())
print(animal_cualquier.sonido())

print(dog.comer())
print(dog.sonido())