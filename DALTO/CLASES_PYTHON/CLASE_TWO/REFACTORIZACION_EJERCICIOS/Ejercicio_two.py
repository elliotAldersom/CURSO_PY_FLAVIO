"""
El usuario ingresa un númeor cualquiera,
y vamos a gennerar una lista de números primos
hasta el número que el haya pasado.
"""

def num():
    while(True):
        num = input("✨ 📐 Ingrese el número: ")
        num = num.strip()
        if(not(num.isnumeric())):
            print("🤖 ❌ Acabas de ingresar un caracter no numérico, intenta de nuevo.")
        elif((num.isnumeric()) and (int(num) <= 1 )):
            print("🤖 ❌ El número debe ser mayor a 0, no igual y tampoco menor.")

        elif((num.isnumeric()) and (int(num) > 1)):
            numero = int(num)
            print("🤖 ✅ Número valido para esta operación.")
            return numero # No pongo el break, pues con el return se detiene y no se ejecuta más ya que es una función.
            

def isCousin(num):
    for i in range(2, num):
        if(num % i == 0):
            return False
        
    return True

def  listaCousin(num):
    num += 1
    lista = []
    for i in range(2, num):
        if(isCousin(i) == True):
            lista.append(i)
    return(lista)

numero = num()
lista_primos = listaCousin(numero)
print(f"✨ 🤖 Esta es la lista de los números primos hasta el número {numero}:\n{lista_primos}")
