""" 
ACÁ HARMOS LA FUNIÓN PARA LA RESTA DE N NÚMEROS:
"""

def Sustraccion():
    while True:
        try:
            print("✨ 🤖 Estás dentro del apartado de RESTA")
            num = int(input("✏️ 🤖 Ingrese el número de elementos que desea restar: "))
            if num <= 1:
                print("🤖 🚫 Mínimo debe de ser 2 números.")
                continue
        except ValueError as v:
            print(f"🤖 🚫 Caracter no valido: {v}")
        except KeyboardInterrupt :
            print(f"\n🤖 🚫 Acabas de ingresar algo no valido")
        else:
            break
    i = 0
    lista = []

    while i < num: 
        try:

            numero = float(input(f"✏️ 🤖 Ingrese el {(i+1)} número: "))
        except ValueError as v:
            print(f"🤖 🚫 Caracter no valido: {v}")
        except KeyboardInterrupt :
            print(f"\n🤖 🚫 Acabas de ingresar algo no valido")
        else:
            lista.append(numero)
            i+= 1
    

    numero_principal = lista[0]
    for valor in lista[1:]: # --> De esta forma accedemos a todos los elementos a partir del que está en el índice 1 (como un range())
        numero_principal -= valor
    
    return f"✨ 🤖 La resta de los números es: {(round(numero_principal, 2))}"

              
#print(Sustraccion())