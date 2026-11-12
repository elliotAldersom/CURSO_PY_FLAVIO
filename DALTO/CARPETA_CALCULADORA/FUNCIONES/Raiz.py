""" 
ACÁ HARMOS LA FUNIÓN PARA LA RADICACION DE N NÚMEROS:
"""

def Radicacion():
    while True:
        try:
            print("✨ 🤖Estás dentro del apartado de RADICACIÓN") 
            num = int(input("✏️ 🤖 Ingrese el número de elementos que desea para realizar la radicación: "))
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
            if numero == 0:
                raise ZeroDivisionError
        except ValueError as v:
            print(f"🤖 🚫 Caracter no valido: {v}")
        except KeyboardInterrupt :
            print(f"\n🤖 🚫 Acabas de ingresar algo no valido")
        except ZeroDivisionError:
            print("🤖 🚫 No puedes sacar raíz de 0 o usar 0 como base de la operación,")
        else:
            lista.append(numero)
            i+= 1
    

    numero_principal = lista[0]
    for valor in lista[1:]: # --> De esta forma accedemos a todos los elementos a partir del que está en el índice 1 (como un range())
        numero_principal **= 1/valor
    
    return f"✨ 🤖 La raíz final de lo números: {(round(numero_principal, 2))}"

              
#print(Radicacion())