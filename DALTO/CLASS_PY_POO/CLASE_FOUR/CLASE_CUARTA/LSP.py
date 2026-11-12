""" 
LSP: Liskov's Substiution Principle (Principio de Sustitución de Liskov)

- Establlece: "Las clases derivadas tienen que ser sustituibles por sus clases bases"
En pocas palabras, si la clase B es una subclase de A, la clase A debería poder utilizarce
en todos los lugares donde B pueda utilizarce, o sea que la clase B puede hacer todo lo de la clase A. 

"""
# Ejemplo no eficiente (no cumple con el principio):
# class Ave:
#     def volar(self):
#         return "Estoy volando"

# class Pinguino(Ave):
#     def volar(self):
#         return "No puedo volar"

# def hacer_volar(ave = Ave):
#     return ave.volar()

# print(hacer_volar(Ave()))


# Ejemplo con el principio:

class Ave:
    # Ponemos todo lo que tengan en común, en este caso pass pues uno vuela y otro no
    pass

class AveVoladora(Ave):
    def Volar(self):
        return "Estoy volando..."

class AveNoVoladora(Ave):
    def Volar(self):
        return "Yo no puedo volar..."


#________________________________________________________
def hacer_volar(ave = Ave):
    return ave.Volar()
#________________________________________________________

print(hacer_volar(AveVoladora()))
print(hacer_volar(AveNoVoladora()))


# Otra forma de hacer este caso es:

class Ave():
    def Alimentarse(self):
        return f"Me estoy alimentando..."
    
    def Dormir(self):
        return f"Estoy durmiendo..."
    
    def Volar(self):
        #return f"Para esto, debemos de saber que tipo de Ave es..."
        pass

class AveVoladora(Ave):
    def Volar(self):
        return F"Estoy volando..."

class AveNoVoladora(Ave):
    def Volar(self):
        return f"Yo no puedo volar..."

