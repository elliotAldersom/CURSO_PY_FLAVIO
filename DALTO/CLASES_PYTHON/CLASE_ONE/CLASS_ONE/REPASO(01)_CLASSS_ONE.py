# IMPRIMIR PARTE DE UN STRING:
dato = "Pepito es un pepe feliz";
print(dato[0:2]); # imprime "Pepit"  # imprime
nombre = input("Ingresa tu nombre: ")
contador = len(nombre);
print("Tu nombre tiene " + str(contador) + " caracteres.")

escoger = int(input("Ingresa que número de caracter deseas mostrar: "));
print( "Esto son los caracteres que se muestran: " + nombre[0:escoger]);



# VA A VOTAR LA VARIABLE COM EL VALOR (DEFINIDO) RECIENTEMENTE DEFINIDO.
nombre = input("ingresa tu nombre: ")
nombre = input("ingresa tu nombre: ")
print(nombre)
print("_______________________________________________________________")

# PARA SUMAR, MULTIPLICAR, DIVIDIR, POTENCIAR:
numero = float(input("Ingresa el número: "))
numero2 = float(input("ingresa el numero que deseas restar: "))
resta = numero - numero2
print(resta)
print("_______________________________________________________________")

#CONDICIONES:
if(numero > numero2):
    print("LA RESTA VA A SALIR POSITIVO(+)")
    print("_______________________________________________________________")
elif(numero < numero2):
    print("LA RESTA VA A SALIR NEGATIVO(-)")
    print("_______________________________________________________________")
else:
    print("LA RESTA VA A SALIR CERO(0)")
    print("_______________________________________________________________")

# CONCATENACIÓN CON + :
saludo = "Hola " + nombre + " Como estás."
print(saludo)
print("_______________________________________________________________")

# CONCATENACIÓN CON f-string
fecha_nacimiento = int and str(input("INGRESE SU FECHA DE NACIMIENTO: "))
edad = int(input("INGRESE SU EDAD: "))
saludo2 =  str(nombre) + " veo que tienes " +str(edad) + " ¿Que tal los estudios?"
print(saludo2)
print("_______________________________________________________________")

# PERTENECE O NO PERTENECE (in / is not) :
print("Hola" in saludo)
print("hola" in  saludo)
print(" Como estás." in saludo)
print("¿Que tal los estudios?" is not saludo2)
print("_______________________________________________________________")

# DATOS COMPUESTOS 
# 1) list
agrupacion = [ 2 ,"casa", "hogar", "familia", "padres", "hijos", "mascotas"]
print(agrupacion)
print(type(agrupacion))  # ---> Que tipo de dato es.

agrupacion[1] = "CASITAS" # ---> SÍ SE PUEDE HACER
print(agrupacion)
print(agrupacion[5])
agrupacion = [2 , "CASONAS", "HAY EN HUANDOO", "HUARAL"] # ---> Con esto guardo los elementos de la lista.
print(agrupacion)
print("_______________________________________________________________")

# 2) tupla
agrupacion2 = (2, "parques", "niños", "juegan", "grupos")
print(agrupacion2)
print(type(agrupacion2))
print(agrupacion2[2])
agrupacion2 = (2, "parquecitos", "lueven", "los enamoraritos") # ---> Con esto cambio todos los elementos de la tupla.
print(agrupacion2)
print(agrupacion2[3])
print("_______________________________________________________________")

#agrupacion2[2] = "NIÑOS"  # ---> NO SE PUEDE HACER
#print(agrupacion2)


# 3) set / conjunto 
agrupacion3 = {25 , "senatinos", "estudian", "distintas carreras", "se esfuerzan mucho", "senatinos"}
print(agrupacion3)
print(type(agrupacion3))
#agrupacion3[2] = "estudian" # ---> NO SE PUEDE
#print(agrupacion3)
#print(agrupacion3[2]) # ---< NO SE PUEDE
agrupacion3 = {2 , 3 , 4 ,5 ,"HOLA"}
print(agrupacion3)
print("_______________________________________________________________")

# 4) dict / diccionario
datos = {
    "nombre" : nombre ,
    "edad" : edad ,
    "fecha" : fecha_nacimiento
}
print(datos)
print("_______________________________________________________________")

pedir = input("Que dato desea pedir: ")
print(datos[pedir])
print("_______________________________________________________________")

# OPERADORES ARITMETICOS: 
# 1) SUMA: (+)
suma = numero + numero2
print("LA SUMA ES: "+ str(suma))
print("_______________________________________________________________")

# 2) RESTA: (-)
resta = numero - numero2
print("LA RESTA ES: "+ str(resta))
print("_______________________________________________________________")

# 3) MULTIPLICACIÓN: (*)
multiplicacion = numero * numero2
print("LA MULTIPLICACIÓN ES: " + str(multiplicacion))
print("_______________________________________________________________")

# 4) DIVISIÓN: (/)
division = numero / numero2
print("LA DIVISIÓN ES: " + str(division))
print("_______________________________________________________________")

# 5) POTENCIA: (**)
potencia = numero ** numero2
print("LA POTENCIA ES: " + str(potencia))
print("_______________________________________________________________")

# 6) DIVISIÓN BAJA: (//)
division_baja = numero // numero2 #---> DEVUELVE EL ENTERO DE LA DIVISIÓN SIN CONSIDERAR EL DECIMAL.
print("LA DIVISIÓN BAJA ES: " + str(division_baja))
print("_______________________________________________________________")

# 7) MODULO: (%)
modulo = numero % numero2 #---> DEVUELVE EL RESTO DE LA DIVISIÓN
print("EL MODULO ES: " + str(modulo))
print("_______________________________________________________________")


# OPERADORES DE COMPARACIÓN  (devuelven TRUE o FALSE y sirve para condiciones).
 #TAMBIÉN FUNCIONA CON STRING.
 
# 1) IGUAL: (==)  
print(numero == numero2)

# 2) DIFERENTE: (!=)
print(numero != numero2)

# 3) MAYOR: (>)
print(numero > numero2)

# 4) MENOR: (<)
print(numero < numero2)

# 5) MAYOR IGUAL QUE: (>=)
print(numero >= numero2)

# 6) MENOR IGUAL QUE: (<=)
print(numero <= numero2 )

# EJEMPLO: 

"""Juan quiere saber la fecha de un día cualquiera,  pero que sea válida (cualquier año), el va a introducir el número y tiene que salir:
día de mes del año"""

#Resolución:
dia = int(input("Ingrese el día por favor: "))
mes = int(input("Ingrese el mes por favor: "))
año = int(input("Ingrese el año por favor: "))

lista= [0,"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

if(not(año%4==0)  and not(mes!=2)):
    print("No es válido esta fecha.")
    print("_______________________________________________________________")
else:
    print(str(dia) + " de " + str(lista[mes]) + " del " + str(año) )
    print("_______________________________________________________________")

#  FUNCIÓN DIR: (LOS ATRIBUTOS DE ESTE OBJETO PASADO).

resultado1 = dir(numero)
print(resultado1)
print("_______________________________________________________________")

print(dir(numero))

print("_______________________________________________________________")

#  FUNCIÓN TYPE: (EL TIPO DE DATO QUE ES).
print(type(numero))

print("_______________________________________________________________")

# MÉTODOS DE CADENA: 

texto = (input("INGRESE EL TEXTO PARA EDITAR: "))
print("_______________________________________________________________")

# 1) upper: PONE todo A MAYÚSCULA.

resultado2 = texto.upper()
print(resultado2)

print("_______________________________________________________________")

#print(agrupacion.upper()) # --> no se puede pues acá se agarra por índice (para list,tupla, diccionario y en set no se puede hacer nada pues es desordenado)

# 2) lower : pone todo en minúscula.

resultado3 = texto.lower()
print(resultado3)

print("_______________________________________________________________")

# print(agrupacion2.lower()) # --> no se puede pues acá se agarra por índice (para list, tupla, diccionario y en set no se puede pues es desordenado)

# 3) capitalize : Primera letra en mayúscula.
resultado4 = texto.capitalize()
print(resultado4)

print("_______________________________________________________________")

# 4) find : Busca la primera aparición de tal palabra contando todos los caracteres, incluso  el espacio y si no encuentra nada devueleve -1.

buscador = (input("QUE DESEAS BUSCAR DEL TEXTO: ")) 

resultado5 = texto.find(buscador)

print(resultado5)

print("_______________________________________________________________")

# 5) index : Devuelve la primera aparición de la palabra o el caracter y si  no lo encuentra devueleve un error.

buscador2 = input("Que otra cosa del texto deseas buscar: ")
resultado6 = texto.index(buscador2)
print(resultado6)

print("_______________________________________________________________")

# 6) isnumeric : Devuelve un true si el valor es numérico y si no lo es da un false, tiene que ser todo necesariamente numéricos.            
DNI = (input("INGRESE SU NÚMERO DE DNI: ")) # --> NO NECESITO PONER EL INT PUES ESTO ANALIZA TEXTO PARA VER SI ESTÁ FORMADO TOTALMENTE POR NÚMEROS.

rersultado7 = DNI.isnumeric()  # --> SI EL DNI TIENE ESPACIOS O CUALQUIER OTRA COSA QUE  NO ES NÚMEROS ES FALSE

print(rersultado7)

print("_______________________________________________________________")

# 7) isalpha : VE SI EL TEXTO ESTÁ COMPUESTO EN SU TOTALIDAD POR STRING (STR) Y SI ES ASÍ DEVUELVE TRUE Y SI NO PUES FALSE.

palabra = input("INGRESE LA PALABRA: ")
resultado8 = palabra.isalpha()

print(resultado8) # --> la oración si tiene espacios va a salir FALSE las letras deben de estar juntas.

print("_______________________________________________________________")

# 8) count : CUENTA EL NÚMERO DE VECES QUE SE REPITE UN CARACTER O CADENA DE TEXTO.
busca_texto = input("QUE PALABRA DEL TEXTO DESEAS BUSCAR PARA VER SUS REPETICIONES: ")

resultado9 = texto.count(busca_texto)

print(resultado9)

print("_______________________________________________________________")

# 9) len : cuenta los caracteres de una cadena (función).
print("AHORA VAMOS A VER CUANTOS CARACTERERES TIENE TU TEXTO:")

resultado10 = len(texto)
print( "TU TEXTO TIENE " + str(resultado10) + " CARACTERES.")

print("_______________________________________________________________")

# 10) startswith : mira si una cadena empieza con otra cadena.

busca_cadena = input("CON QUE QUIERES VERIFICAR QUE INICIA TU TEXTO: ")

resultado11 = texto.startswith(busca_cadena)

print(resultado11)

print("_______________________________________________________________")

# 11) endswith : mira si una cadena termina con otra cadena.

busca_cadena2 = input("CON QUE QUIERES VERIFICAR QUE TERMINA TU TEXTO: ")

resultado12 = texto.endswith(busca_cadena2)

print(resultado12)

print(" ")
print("_______________________________________________________________")

# 12) replace : podemos cambiar un pedazo de la cadena o toda la cadena de texto.
# Busca la coincidencias de la palabra dada para cambiarlas por la nueva dada (cambia todas las coincidencias)
# y si no encuentra ninguna coincidencia devuelve el texto original

print("Quieres volver a hacer tu texto?")

opcional = input("Si o No: ")

if (opcional.lower() ==  "si"):
    nuevo_texto = input("Ingrese su nuevo texto: ")
    cambio_de_texto = texto.replace(texto , nuevo_texto)  # --> No era necesariop pero es para el ejemplo.
    print(" ")
    print(cambio_de_texto)
    separador = cambio_de_texto.split(" ")  # --> Genera una lista el metodo split
    print(separador)
    print(type(separador))

else:
    print("Entendido se dentendrá el proceso de rehacer su texto:)")
    separador = texto.split(" ")
    print(separador) 
    print(type(separador))

print(" ")
print("_________________________________________________________________________")

# 13) split : separa las cadenas de texto donde se encuentre las cadenas que le dimos nosotros, de esta forma genera una lista(list).
# Para hacer esto reemplaza el valor dado por lo encontrado en e string y lo hace en list.
# Recomendable es reemplazar en split las comas (",") o  espacio (" ")

#separador = cambio_de_texto.split(" ") ---> EJM de split ( también está en el if y else)

#_______________________________________________________________________________________________________---

#MÉTODOS DE LISTA

# 1) append : agregamos un valor al final de la lista. (no  cambiamos valores slo agregamos).

grupo = ["Hola" , "como" , "estás" ]
grupo.append("amigo")
print(grupo)
print(" ")


print("""--------------------------------
        / PON TEXTO Y YO LO HAGO EN LISTA /
         -------------------------------- """)
print(" ")
grupo = input("Ingresa tu texto para hacerlo lista, que cada palabra esté separada por espacios y no comas (,): ")
conjunto = grupo.split(" ")
print(conjunto)
aniadir = input("Algo más que deses agregar? ")
if (aniadir.lower() == "si" ):
    nueva_palabra = input("Que palabra deseas agregar: ")
    conjunto.append(nueva_palabra)
    print(conjunto)
    
else:
    print("Entendido no se va agregar nada más.")   
