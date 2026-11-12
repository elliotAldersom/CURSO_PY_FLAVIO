""" 
ACÁ HARMOS LA FUNIÓN PARA LA SUMA DE N NÚMEROS:
"""

def Adicion():
    while True:
        print("✨ 🤖 Estás dentro del apartado de SUMA")
        try:
            num = int(input("✏️ 🤖 Ingrese el número de elmentos que desea sumar: "))
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
    
    resultado = sum(lista)
    return f"✨ 🤖 La suma de los números es {(round(resultado,2))}"
             
#print(Adicion())