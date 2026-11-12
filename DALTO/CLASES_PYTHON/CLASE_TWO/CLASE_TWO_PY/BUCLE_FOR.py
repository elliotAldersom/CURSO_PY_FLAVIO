"""
FOR
¿QUÉ ES UN ELEMENTO ITERABLE?
- UN ELEMENTO ITERABLE TIENE UN ITERADOR QUE DEFINE COMO SE VA A ITERAR, NO TODOS LOS ELEMENTOS
SON ITERABLES, UN ITERABLE ES CUALQUIER OBJETO QUE PUEDES RECORRER (ITERAR) UNO A UNO.
ES DECIR, PUEDES USARLO EN UN BUCLE "for" O PASARLO A FUNCIONES COMO "list()", "tuple()" o "set()"
ESTOS CUATRO ELEMENTOS ITERABLES QUE ACABO DE MENCIONAR SON ITERABLES SIN IMPORTAR SI SU CONTENIDO
ES O NO ITERABLE, POR DECIR, UNA LISTA CON NÚMEROS, PUEDE SER ITERABLE, INDEPENDIENTEMENTE SI 
LOS INT O FLOAT NO SON ITERABLES (INT Y FLOAT, NO SON ITERABLES)
UN ITERABLE PRODUCE ELEMENTOS UNO A LA VEZ, COMO EN UNA SECUENCIA.

EJM DE ITERABLES: 
String       ejm   -->   "hola"
Lista        ejm   -->   [1,2,3]
Tupla        ejm   -->   (1,2,3)
Set          ejm   -->   {1,2,3}
Dicioanrio   ejm   -->   {"a" : 1 , "b" : 2 , "c" : 3}
Range        ejem  -->   range(5)
Frozenset    ejm   -->   frozenset([1,2,3])

OBJETOS PERZONALIZADOS: 
SI IMPLEMENTAN __iter__() o __getitem__() con índices (emepzando desde el 0).

PARA SABER SI UN ONJETO ES ITERABLE PODEMOS USAR LA FUNCIÓN: iter()

n = "d"
print(iter(n)) ---> imprime ciertos números 

n = 23
print(iter(n)) --> imprime error, y dice que no es iterable

¿CÓMO FUNCIONAN LOS ITERABLES? 
- UN ITERABLE ES COMO UN "CONTENEDOR" QUE SABE CÓMO DEVOLVER UN ITERADOR USANDO: __iter__()
- EL ITERADOR ES EL OBJETO QUE REALMENTE DEVUELVE LOS ELEMENTOS UNO A UNO, USANDO: next()

"""

# BUCLE FOR: FOR ES UN BUCLE QUE NOS PERMITE ITERAR, CREAR UNA ITERACIÓN.

# HACIENDO UN BUCLE FOR EN UNA LISTA: RECORRIENDO LA LISTA ANIMALES Y NÚMEROS
animales = ["gato", "perro", "loro", "cocodrilo", "pez"];

print("\nFOR CON LA LISTA DE ANIMALES\n")

for animal in animales :
    print("ahora la variable animal es igual a: " + str(animal));
    print("_____________________________________________")

print("\n_____________________________________________________________________________\n")
print("\nFOR CON LA LISTA DE NÚMEROS\n")

numero_2 = [2,4,6,8,10];

for numero in numero_2:
    resultado = numero * 10
    print("el resultado de multiplicar el número " + str(numero) + " por 10 es: " + str(resultado))
    print("______________________________________________________________________________________")

print("\n________________________________________________________________________________________\n")    


# HACIENDO UN BUCLE FOR PERO PARA LA LISTA ANIMALES Y NUMEROS AL MISMO TIEMPO:
# ÚSAMO LA FUNCIÓN: --> zip()
# PARA ESTO, LAS LISTAS DEBEN DE TENER LA MISMA CANTIDAD DE ELEMENTOS.
# OJO, VA A IMPRIMIR ELEMENTO 1 LISTA 1, ELEMENTO 1 LISTA2, ASÍ SUCESIVAMENTE.
print("MOSTRANDO CON BUCLE FOR AMBAS LISTAS, POR MEDIO DE LA FUNCIÓN: zip()\n");
for numero, animal in zip(numero_2,animales):  # -- TIENE QUE ESTAR ORDENADO, numero con numeros, animal con animales, sino se desordena y numero va a mostrar animales y diseversa.
    print("recorriendo la lista de animales: " + str(animal));
    print("_____________________________________________________");
    resultado = numero * 10;
    print("el resultado de multiplicar " + str(numero) +  " por 10 es: " + str(resultado));
    print("______________________________________________________________________________________");

print("\n________________________________________________________________________________________\n")    


# BUCLE FOR CON FUNCIÓN RANGE : range()
print("\nFOR USANDO RANGE EN NÚMEROs:\n");

for num in range(5,10): # --> Imprime números desde el 5 hasta uno antes del 10, o sea 5,6,7,8,9
    print(num)

print("\n________________________________________________________________________________________\n")    

for num in range(5): # --> Imprime desde el 0 hasta uno antes del 5
    print(num)

print("\n________________________________________________________________________________________\n")    

"""
range(5) ---> Imprime 5 números pero empezando desde el 0: 0,1,2,3,4 (5 números)
range(2,10) ---> Imprime desde el 2 hasta el 10, va a contar al 2 pero no al 10, 
o sea hasta uno antes del 10: 2,3,4,5,6,7,8,9

"""

print("\nFOR USANDO RANGE PARA MOSTRAS LO VALORES DE UNA LISTA:\n")

# FORMA NO ÓPTIMA DE RECORRER UNA LISTA:
#numero_2 = [2,4,6,8]
for num in range(len(numero_2)):
    print(numero_2[num]) # --> otra forma de acceder a los elementos de una lista

print("\n________________________________________________________________________________________\n")    

# FORMA CORRECTA DE RECORRER UNA LISTA CON SU ÍNDICE:

print("\n FOR USANDO ENUMERATE, MUESTRA EL ÍNDICE Y SU VALOR, CONVIERTE EN TUPLA LA LISTA");

for num in enumerate(numero_2):
    #print(type(num)) # ---> Imprime que es tupla
    #print(num) # --> Imprime índice y valor
    #print(num[0]) # --> Imprime los índices
    #print(num[1]) # ---> Imprime los valores
    indice = num[0]
    valor = num[1]
    print("Indice: " + str(indice) + " valor: " + str(valor))


print("\n________________________________________________________________________________________\n")

# USANDO EL ELSE EN EL FOR:

print("\nUSANFO EL ELSE EN EL BUCLE FOR\n");

for numero in numero_2:
    print("Ejecutando el último bucle, valor actual: " + str(numero));
else: 
    print("El bucle terminó.");

print("\n________________________________________________________________________________________\n");

"""
ABSOLUTAMENTE TODO LO ANTERIOR FUNCIONA EXACTAMENTE IGUAL PARA TUPLAS.

"""

"""
AHORA VAMOS A VER LO MISMO PERO EN SET,  VAMOS A ITERAR CONJUNTOS (SETS)

"""

# ITERARNDO SET:

print("\nITERANDO EN CONJUTO SET\n")

animal_1 = {"gato","perro","pericote","mono"};

objeto = {"casa","cell phone", "guitar electric", "bass electric"};

for e in animal_1:
    print("El animal es: " + str(e));

for e in objeto:
    print("El objeto es: " + str(e));

for animal,objeto in zip(animal_1,objeto):
    print("El animal es: " + str(animal) + "; y el objeto es: " + str(objeto)) 

for i in enumerate(animal_1):
    indice = i[0]
    valor = i[1]
    print("El índice es " + str(indice) + " y el valor es " + str(valor));


"""
TODO LO VISTO FUNCIONA EN TUPLA, LISTA, SET, LA DIFERENCIA QUE PARA ITERAR EN UN SET 
NO SE PUEDE USAR --> range(len(set))
LO QUE DEBEMOS DE USAR ES LA FUNCIÓN ENUMERATE, LA CUAL SIRVE EN LISTA, TUPLA, SET.
ESA ES LA ÚNICA DIFERENCIA.

"""



"""

AHORA VAMOS A VER COMO SE RECORRE UN DICCIONARIO.

"""

# ITERANDO UN DICT (DICCIONARIO)   

print("\nITERANDO UN DICCIONARIO:\n")

nombre = input("INGRESA TU NOMBRE: " );
apellido = input("INGRESA TU APELLIDO: ");
edad = int(input("INGRESA TU EDAD: ")); 

diccionario = {
   "nombre"   : nombre,
   "apellido" : apellido,
   "edad"     : edad
}

print(diccionario);


# PARA RECORRER LOS KEYS (CLAVES):
for a in diccionario:
    print(a)

# PARA RECORRER LOS KEYS (CLAVES) Y LOS VALUES (VALORES) USAMOS EL MÉTODOD "items()", ESTE DEVUELVE UN ITERABLE.
for a in diccionario.items(): # --> DEVUELVE UNA TUPLA CON CALAVE (O) Y VALOR (1)
     key = a[0]
     value = a[1]
     print("El valor que hay en la clave o índice (porque el dict ahora es una tupla) \"" + str(key) + "\" es: " + str(value));
else:
    print("No hay más valores en el diccionario");


# FOR CON SENTENCIAS "CONTINUE" Y "BREAK":
print("\nFOR CON SENTENCIAS \"CONTINUE\" Y \"BREAK\"\n")
#  HACIENDO QUE EL BUCLE NO IMPRIMA UN ELEMENTO CON "continue".
"""
continue : Cuando el programa encuentra un continue dentro de un bucle,
salta inmediatamente a la siguiente iteración del bucle,
saltándose cualquier código que esté después del continue en esa iteración.
Omite imprimir el valor que pusimos (en este caso, fruta == "granada") y va al siguiente
EJM:
if(fruta == "granada") --> True
va a pasarse de largo y no imprime granada, pero si pasa esto
if(fruta == "granada") --> False
va a imprimir ese valor.
"""

frutas = ["banana","manzana","ciruela","pera","naranja","granada","durazno"];
print("CONTINUE:")
for fruta in frutas:
    if(fruta == "granada"):
        continue
    print("ME VOY A COMER UNA: " + str(fruta));


# HACIENDO QUE EL BUCLE AL LLEGAR A UN ELEMENTE SE DETENGA CON "break".
"""
break : Cuando el programa encuentra un break dentro de un bucle,
termina el bucle completamente y sale de él.
"""

frutas = ["banana","manzana","ciruela","pera","naranja","granada","durazno"];
print("BREAK")
for fruta in frutas:
    print("ME VOY A COMER UNA: " + str(fruta));
    if(fruta == "granada"):
     break
     #print("ME VOY A COMER UNA: " + str(fruta)); --> NO SE MUESTRA NUCA PUES ESTÁ DESPUÉS DEL BREAK
  
print("BUCLE TERMINADO, PUES YA LLEGAMOS HASTA \"GRANADA\"");
# PONGO EL PRINT ACÁ AFUERA Y NO UN ELSE, PUES AL EJECUTAR UB "BREAK" YA NO SE EJECUTA NADA MÁS, TODO SE DETIENE.
# PERO SI NO SE EJECUTA EL "BREAK", O SEA if(fruta == "granada"): --> False
# PUES SE EJECUTARÁ EL ELSE


"""
RECORRER UNA CADENA DE TEXTO:
"""
print("RECORRIENDO (ITERANDO) UNA CADENA DE TEXTO:");

cadena = "HOLA DALTO";
for letra in cadena:
    print(letra); # --> SE RECORRE CARACTER POR CARACTER


"""
FOR EN UNA LINEA DE CÖDIGO:
"""
print("FOR EN UNA LÍNEA DE CÖDIGO:");

numeros = [2,5,8,10];
print(numeros)
# VAMOS A DUPLICAR EL VALOR DE CADA ELEMENTO DEL CÓDIGO:
numeros_duplicados = [x*2 for x in numeros]  # --> LA EXPRESIÓN MATEMÁTICA ES PRIMERO Y LUEGO EL CÓDIGO A EJECUTAR
print(numeros_duplicados);



# ELIMINAR SALTOS DE LÍNEA EN UN BUCLE FOR:
for i in "tucorreo@gmail.com":
    print("hola", end=" ")
    
""" 
No imprimimos el i pues lo que quermos es recorrer cada caracter del 
String pero mostrar hola en vez del caracter.
Esto funciona en Set, Tuple, List, Dict
"""

for i in range(5,106,20):
    print(f"\nEl núero es {i}")
    
""" 
DE ESTA FORMA HACEMOS UN RANGO QUE VALLA DESDE EL 5 HASTA EL 101 EN PASOS DE A 2
"""


