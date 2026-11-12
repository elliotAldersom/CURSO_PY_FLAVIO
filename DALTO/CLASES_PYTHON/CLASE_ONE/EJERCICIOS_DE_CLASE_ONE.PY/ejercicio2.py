"""Suponiendo que cada persona en promedio habla dos palabras por segundo"""
# A) Pedir al usuario que diga cualquier texto real y:
# Clacular cuanto tardará en decir esa frase
# ¿cuantas palabras dijo?

# B) SI se tarda más de un minuto decirle: para flaco tampoco te pedí un testamento.

# RESOLUCIÓN: 
print("***********************************************************")
print("CADA PERSONA EN PROMEDIO DICE DOS PALABRAS POR SEGUNDO    *")
print("***********************************************************")

frase = input("Ingrese por favor el texto para medir el tiempo a tardar:")

cantidad_palabras = frase.split(" ")

print("----------------")

#print(cantidad_palabras)

numeros_palabras = len(cantidad_palabras)

print("La cantidad de palabras dichas son " + str(numeros_palabras) + " y te demoras en decirlo " + str (numeros_palabras/2) + " segundo.")


if (numeros_palabras > 120 ):
    print("Para flaco tampoco te pedí un testamento")

else:
    print(f"genial te demoras menos de un minuto.")