from random import randint

"""
# Forma 1
attemps= 1
numero_random = randint(0,5)
while int(input("Ingresa el número secreto: ")) != numero_random:
    print(f"Fallaste, el número era {numero_random}. intenta de nuevo")
    numero_random = randint(0,5)
    attemps+=1

print(f"Felicidades, acertaste al número! El numero de intentos realizados fueron: {attemps}")
"""

# Forma 2
lim_attemps = int(input("""
- - - - - GENERADOR DE NUMEROS ALEATORIOS - - - - -
Ingrese el número de oportunidades: """))
lim_num = int(input("Ingrese el número límite del generador aleatorio (1 - Numero): "))
print("- - - - - - - - - - - - - - - - - - -")
# Inicializando Información
numero_random = randint(1,lim_num)
attemps= 1
# Juego principal
while attemps < (lim_attemps+1):
    numero_ingresado = int(input(f"Ingresa un número entre el 1 y el {lim_num}: "))
    if 0 >= numero_ingresado or numero_ingresado > lim_num:
        print(f"¡Este numero excede los limites indicados!\nTe quedan {lim_attemps - attemps} intentos...")  
    
    elif numero_ingresado == numero_random:
        print(f"¡Felicidades :D!, acertaste al número!\nAl {attemps} intento.")
        break 
    
    else:
        
        print(f"Fallaste. intenta de nuevo. \nTe quedan {lim_attemps - attemps} intentos" )
        print("PISTA: El numero que ingresaste es", "mayor" if numero_ingresado > numero_random else "menor",  "Que el Generado.")
    
    attemps+=1
    
    print("- - - - - - - - - - - - - - - - - - -")
else:
    print(f"Fallaste XD. Ya acabaste tus {lim_attemps} intentos")


