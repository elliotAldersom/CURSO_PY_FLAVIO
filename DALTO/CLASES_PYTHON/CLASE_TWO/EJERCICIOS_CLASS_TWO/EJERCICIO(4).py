"""

Escribir un programa que pregunte al usuario su edad 
y muestre por pantalla si es mayor de edad o no.

"""

name =input("Ingrese su nombre: ")
age = int(input("Ingrese su edad: "))

def mayor_de_edad(nombre, edad):
    nombre = nombre.strip()
    nombre = nombre.capitalize()
    if(edad >= 18):
        bien = f"{nombre} eres mayor de edad"
        return bien
    else:
        mal = f"{nombre} eres menor de edad."
        return mal

resultado = mayor_de_edad(name, age);
print(resultado)

