"""

ESCRIBIR UN PROGRAMA QUE CALCULE LA SERIA DE FIBONACCI, 
HASTA UN NÚMERO ESPECÍFICOO DE TÉRMINOS.

"""

num = int(input("INGRESE EL NÚMERO AL QUE QUIERE LLEGAR: ")) 

def fibonacci(numero):
    a, b = 0,1
    lista = []
    for i in range(numero):
        if( b > numero):
            return lista
        else:
            lista.append(b)
            a, b = b, a+b
           
    return lista

resultado = fibonacci(num)
print(f"Tu lista fibonnacci hasta {num} es: {resultado}");