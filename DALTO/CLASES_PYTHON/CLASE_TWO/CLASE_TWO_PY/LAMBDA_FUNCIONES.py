"""

LAMBDA:  Crea funciones anónimas.
-BENEFICIOS:
- Lo podemos usar cuando queremos hacer algo sencillo y rápido
- Retorna automáticamente. sin necesidad de usar el: --> return
a diferencia de def que si usar el return.
- No son aptas para hacer más de una instrucción, solo son para cosas simples y 
de una sola instrucción, como vemos en el siguiente ejemplo:

multi = lambda x : x*2
print(multi(5))
num = int("Ingrese un número: ")
print(multi(num))

________________________________________________________
ESTRUCTURA:
COMO CREAMOS UNA FUNCIÓN LAMBDA?
- PARA HACERLO USAMOS LA SIGUIENTE FORMA:

num= lambda x: x*2

1) Nombre de la función
2) Ponemos lambda con parámetros
3) Igualamos a una expresión
 
"""

multiplicar_por_dos = lambda x : x*2
print(multiplicar_por_dos(5))  # Salida: 10

"""

FILTER: (filtar)
- Sirve para filtrar valores verdaderos (True)
de un iterable, cuando se pasa una condición,
y dicha condición esta puesta en una función,
esta función devuelve un nuevo iterable con (e que tu quieras)
los valores verdaderos (True).

EJM:

listado = [1,2,3,4,5,6,7,8,9,10]
def par(x):
   return x % 2 == 0

filtrado = filter(par, listado)
filtrado = list(filtrado) # --> LO ALMACENAMOS EN UNA LISTA 
                          # (POR ESO DIJE QUE ESCOGEMOS EN QUE ITERAR)
# ADEMAS HAY QUE GUARDAR ESTA LISTA EN UNA VARIABLE
# PAR QUE SE ALMAcENE Y NO SE BORRE, PORQUE SINO DEBERÍAMOS DE ITERARLO OTRA VES.


print(f"El listado con los números que son divisibles entre dos son: {filtrado}");

for i in list(filtrado): # --> LO HICE PARA RECORRER LA LISTA.
# POR ESE MOTIVO LO GUARDE EN OTRA VARIABLE LA LISTA, PARA NO NECESITAR ITERAR OTRA VES.
   print(i)



"""
print("CON DEF:")

def par(x):
   return x % 2 == 0

listado = []

cantidad = int(input("Ingrese el número de elementos que quiere tener en su lista: "))

contador = 0

while(contador < cantidad):
   try:
      num = float(input(f"Ingrese el número: para el elemento {contador + 1}: "))
      listado.append(num)
      contador += 1
   except ValueError:
      print("Error, acaba de ingresar un caracter no valido")

filtrado = filter(par, listado)
filtrado = list(filtrado)
print(f"El listado con los números que son divisibles entre dos son: {filtrado}");

for i in filtrado:
   print(f"Recorriendo la lista: {i}")

print("____________________________________________________________")

print("CON LAMBDA:")
es_par = lambda n :not( n % 2 == 0)

filtrar = filter(es_par, listado)
filtrar = tuple(filtrar)
print(f"La tupla con los números que son impares es: {filtrar}");

for i in filtrar:
   print(f"Recorriendo la tupla: {i}")

print("____________________________________________________________")