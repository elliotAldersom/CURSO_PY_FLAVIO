""" 
ACÁ HAREMOS LA FUNCIÓN PARA FACTORIZAR UN NÚMERO X
"""

def Factorial():
    while True: 
        try:
            print("✨ 🤖 Estás dentro del apartado de FACTORIAL") 
            n = int(input("✏️ 🤖 Ingrese el número del cual quiere hallar su factorial: "))
            if n < 0:
                print("🤖 🚫 El factorial no existe para números negativos")
                continue
            if n == 0:
                return "✨ 🤖 El fctorial de 0 es: 1"
                
        except ValueError as e:
            print(f"🤖 🚫 Caracter no valido: {e}")    
        except KeyboardInterrupt:
            print("\n🤖 🚫 Caracter no valido.")
        else:
            break 

    resultado = 1
    for i in range(1,(n+1)):
        resultado *= i
    
    return f"✨ 🤖 El factorial de {n} es: {resultado}"

#print(Factorial())
    

        