"""
Hacer un programa que pida ingresar un número
y veremos si es o no capícua.
"""
def numero():
    print("✨ Ingresa un número para saber si es o no capícua.\nRequisitos:\n✅ El número debe ser mayor a 0\n✅ El número debe de ser como mínimo de 2 dígitos")
    while(True):
        try:
            #numero = int(input("Ingresa un número para saber si es o no capícua.\nRequisitos:\n✅ El número debe ser mayor a 0\n✅ El número debe de ser como mínimo de 2 dígitos\nIngrese el número: "))
            numero = int(input("Ingrese el número: "))
            if(numero > 9):
                return numero;
            elif((numero <= 9) and (numero > 0)):
                advertencia = "El número debe ser de 2 digitos como mínimo."
                print(advertencia)
              
            elif(numero == 0):
                advertencia = "🤖 EL número no puede ser 0"
                print(advertencia)
            else:
                advertencia = "🤖 El número debe de ser mayor a 0"
                print(advertencia)
        except ValueError:
            advertencia = "🤖 El caracter ingresado no es número, intenta de nuevo."
            print(advertencia)
            
        

def capicua(num):
    num = str(num);
    lista = list(num);
    lista_revertida = lista.copy()
    lista_revertida.reverse()
    mensaje = ""
    if(lista == lista_revertida):
        mensaje =f"✨🤖 El número {num} es capícua."
        
    else:
        mensaje =f"✨🤖 El número {num} no 🚫 es capícua."
    return mensaje  


num = numero()
resultado = capicua(num)
print(resultado)
