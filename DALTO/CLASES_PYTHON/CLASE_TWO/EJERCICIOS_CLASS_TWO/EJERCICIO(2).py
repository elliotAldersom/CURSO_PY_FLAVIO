"""

CREAR FUNCIÓN QUE AL PASAR UN NÚMERO, NOS GENERE NÚMEROS PRIMOS
HASTA LLEGAR A ESE NÚMERO (0 - x)

"""
numero = int(input("Ingrese el número para verificar los primos que hay: "))


# CREAR FUNCIÓN QUE VERIFIQUE SI ES PRIMO:
def es_primo(num):
    # VERIFICACIÓN QUE EL NÚMERO PASADO NO PUEDA DIVIDIRSE POR NINGUN NÚMERO
    # QUE ESTE DEL RANGO DE 2 - (HASTA UNO ANTES DEL NUM)
    # RANGE(29) --> IMPRIME DEL 0-28
    # RANGE(2, 29) --> IMPRIME DEL 2-28
    for i in range(2,num): # --> range(start, stop)
        # Si es divisible por alguno de los número retorna False y termina el bucle
        if(num % i == 0): return False
    # Si termina el bucle, significa que no fue divisible, emtonces es primo.
    return True



# CREAR UNA FUNCIÓN QUE RETORNE UNA LISTA CON TODOS LOS PRIMOS
def numeros_primos(num):
    # CREAMOS LA LISTA VACÍA, LA CUAL LUEGO ALMACENARÁ A LOS PRIMOS
    primos = []
    for i in range(2, num + 1): # --> Sumamos uno a num para que considere a número que pasamos
       # verificación si el valor es primo.
       resultado =  es_primo(i)

       # si es primo se le agrega a la lista
       if(resultado == True):
           primos.append(i)
    # Vemos cuantos primos hay en la lista.       
    n = len(primos)
    # retornamos la lista y la cantidad de primos
    return primos, n


# DESEMPAQUETAMOS:
primos, cantidad = numeros_primos(numero) 
# IMPRIMIMOS: 
print(f"SE ENCONTRÓ {cantidad} PRIMO (s) Y SON:\n{primos}");     