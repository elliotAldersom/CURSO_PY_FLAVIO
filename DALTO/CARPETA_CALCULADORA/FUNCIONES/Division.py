""" 
ACÁ HARMOS LA FUNIÓN PARA LA MULTIPLICACIÓN DE N NÚMEROS:
"""

def Fraccion():
    
    while True:
        try:
            print("✨ 🤖 Estás dentro del apartado de DIVISIÓN") 
            num = int(input("✏️ 🤖 Ingrese el número de elementos que desea dividir: "))
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
            print("🤖 🚫 No se puede dividir entre 0 o usarlo como base de esta operción.")
        else:
            lista.append(numero)
            i+= 1
    

    numero_principal = lista[0]
    for valor in lista[1:]: # --> De esta forma accedemos a todos los elementos a partir del que está en el índice 1 (como un range())
        numero_principal /= valor
    
    return f"✨ 🤖 La división de los números es: {(round(numero_principal, 2))}"

              
#print(Fraccion())