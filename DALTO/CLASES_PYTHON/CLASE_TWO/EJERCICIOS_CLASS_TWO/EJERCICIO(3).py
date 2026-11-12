"""

ESCRIBIR UN PROGRAMA QUE CALCULE LA SERIA DE FIBONACCI, 
HASTA UN NÚMERO ESPECÍFICOO DE TÉRMINOS.

"""

num = int(input("INGRESE EL NÚMERO QUE QUIER TOMAR COMO PARTIDA: ")) # 1
veces = int(input("INGRESE CUANTAS VECES QUIERE QUE SE REPITA (ejm: 1 / 2 / 3 / ...): ")) # 100

def fib(numero, veces):
    lista = [numero, numero]
    contador = 0
    while(contador < (veces )):
        siguiente_fib = lista[contador ] + lista[contador - (contador + 1)]
        lista.append(siguiente_fib)
        contador += 1
        
    return lista

# r = fib(1, 100) --> EJM USADO
r = fib(num, veces)
for i in r:
    print(i)

print(f"La lista de los números es:\n{r}")

