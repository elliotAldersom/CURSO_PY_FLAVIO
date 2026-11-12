"""# CREANDO UNA FUNCIÓN SIMPLE
def saludar():
    print("Hola, bienvenido al porgrama.");

# EJECUTANDO LA FUBNCIÓN SIMPLE:
saludar();"""

#  CREANDO UNA FUNCIÓN CON PARÁMETROS:
"""

PARÁMETRO : VARIABLE QUE EXISTE EN UNA FUNCIÓN
variable que se define en la firma (o definición) 
de una función y que sirve para recibir un valor cuando se llama a la función. 
Los parámetros permiten que una función sea más flexible y reutilizable, 
ya que pueden recibir diferentes valores (argumentos) cada vez que se invoca la función.


¿CUÁNDO USARLO?
- Si una función depende de un "input / variable / dato" externo (pasado desde fuera de la función), 
necesita parámetros para poder recibir esa información.
- Si una función obtiene un "input / variable / dato" dentro de ella misma (interno), 
no necesita parámetros, porque la función ya está pidiendo los datos directamente.

"""

def nombre_1(name):
   #name = input("Ingresa tu nombre: ")  --> esto es para no necesitar de parámetros
   name = name.strip()
   name = name.capitalize()
   return name

#name = nombre() # --> LLAMAMOS A  FUNCIÓN PARA QUE SE EJECUTE
# EN ESTE NAME (VARIABLE), ALAMCENAMOS EL VALOR INGRESADO EN LA FUNCIÓN:
# nombre_1() --> sin parámetros, ya que dentro de el hubo un input()


def saludar(nombre, sexo):
    sexo = sexo.strip()
    sexo = sexo.lower()
    
    #nombre = nombre.strip()
    #nombre = nombre.capitalize()
    if(sexo == "mujer" ):
      adjetivo = "reina"
      saludo = "bienvenida"
    
    elif(sexo == "hombre"):
       adjetivo = "king"
       saludo = "bienvenido"
    else:
       adjetivo = "amigo (a)"
       saludo = "bienvenido (a)"
    
    saludo_1 = (f"Hola {nombre}, mi {adjetivo} {saludo} al programa.");
    return saludo_1


sex = input("Ingrese su sexo: ")
name = input("Ingresa tu nombre: ")
name_1 = nombre_1(name)
 
print(saludar(name_1, sex))


# CREAR UNA FUNCIÓN QUE NOS RETORNE VALORES:  por medio de "return"

"""

m = "Flavio"
print(m[1])   --> imprime: l
print(m[0:3]) --> Esto funciona como un range o sea del 0 al 3 del string
              --> imprime: Fla
- Y esto vamos a usar acontinuación
"""
#chars = input("Ingresa los caracteres para generar tu contraseña:\n")
#numa = int(input("ingrese un numero: "))

def crear_contraseña_random(num):
     
    num_entero = str(num)
    num = int(num_entero[0]) 
    chars = input(f"Ingresa los caracteres para generar tu contraseña, debe de ser mínimo de longitud {num + 1} :\n")
    # --> EJM: chars = "abcdefghij"
    while(chars <=  len(chars)):
       print(f"Debe de ser mayor a {num}")
    c1 = num - 2
    c2 = num
    c3 = num - 5
    contraseña = f"{chars[c1]}{chars[c2]}{chars[c3]}{num *2 }"
    return contraseña, num # --> Tuple / (Retornanndo multiples valores)
    #return contraseña # --> Retornando un solo valor

#chars = input("Ingresa los caracteres para generar tu contraseña:\n ")
#name_1 = nombre() # --> LLAMAMOS A  FUNCIÓN PARA QUE SE EJECUTE 


numa = int(input("ingrese un numero: "))
contra = crear_contraseña_random(numa)

print(f"{name_1} tu contraseña es: {contra}")

# DESEMPAQUETANDO LA FUNCIÓM:
# EN ESTE CASO, ESTAMOS LLAMANDO NUEVAMENTE A LA FUNCIÓN
# POR LO TANTO NOS PIDE INGRESAR NUEVAMENTE LOS CARACTERES.

contra,primer_numero = crear_contraseña_random(numa)

print(f"El número utilizado para crearla fue: {primer_numero}")

# MOSTRANDO LOS RESULTADOS OBTENIDOS Y LOS DATOS UTILIZADOS PARA OBTENERLO:
print(contra)
print(primer_numero)
print(type(contra)) # --> Imprime:  <class 'tuple'>


# SUMAR DE VARIOS NÚMEROS: 

# FORMA NO ÓPTIMA:
def suma_1(nombre, lista):
   numeros_sumados = 0
   for numero in lista:
      numeros_sumados = numeros_sumados + numero
   return f"{nombre}, esta es la suma de todos los números pasados, de forma no óptima {numeros_sumados}"
resultado = suma_1(name_1,[2,3,4,1])
print(resultado)


# FORMA ÓPTIMA:
# UTILIZIANDO EL PARÁMETRO: args (*)
# ESTE PARÁMETRO DEBE DE IR AL FINAL DE TODOS LOS DEMÁS PARÁMETROS
# SI PONEMOS PRIMERO ARGS(*), NO SE PUEDE AGREGAR MÁS PARÁMETROS LUEGO.

def suma(nombre, *numeros):
    
    return f"{nombre}, esta es la suma de todos los números pasados, de forma óptima: {sum(numeros)}"

resultado = suma(name_1, 2,3,4,1,5,5,20,10)
print(resultado)


# OTRA FORMA DE ÓPTIMA:
# USANDO EL ARGS (*) EN EL RETURN

def suma_total( nombre, numeros):
   
   return(f"{nombre} el resultado de los números dados son (suma): {sum([*numeros])}");

numeros = input("Ingrese los números, pero separados por comas (,): ")
numeros = [int(num.strip()) for num in numeros.split(",")] # --> Hacemos una lista comprimida
resultado = suma_total(name_1,numeros)
print(resultado)




"""


LISTA POR COMPRENSIÓN CON BUCLE FOR:
- Una lista por comprensión es una forma compacta y eficiente de crear 
listas en Python. En lugar de usar un bucle for convencional, 
puedes generar una nueva lista en una sola línea.

SINTAXIS:
[nuevo_elemento for elemento in iterable if condición]

EJM:
numeros = [1, 2, 3, 4, 5]
cuadrados_pares = [num ** 2 for num in numeros if num % 2 == 0]

print(cuadrados_pares)


EJM:  
numeros = input("Ingrese los números, pero separados por comas (,): ")
numeros = [int(num) for num in numeros.split(",")]

EXPLICACIÓN: 
- Pedimos al usuario ingresar los números separados por comas,
- Luego a usamos el método split() para generar una lista (iterable), la cual
separa los elementos por medio de las comas (,).
- Luego generamos la lista por comprensión, en la cual se va a recorrer
por medio del bucle for cada elemento que hay en la lista que hicimos con split(),
para que de esta forma generemos una lista de int (enteros) mediante a función int().



FORMA DE HACER SIN A LISTA POR COMPRENSIÓN:

entrada = input("Ingresa los números separados por comas: ")

numeros_str = entrada.split(',')

numeros_listas = []

for num in numeros_str:
    numeros_listas.append(int(num.strip()))

EXPLICACIÓN:
- Primero pedimos al usuario ingresar los números separados por comas.
- Luego a usamos el método split() para generar una lista (iterable).
- Luego generamos una lista vacía llamada numeros_listas.
- Luego recorremos la lista que hicimos con split() por medio del bucle for.
- Luego agregamos cada elemento recorrido por medio del método append(),
también pasamos a enteros el num, pero a este num le quitamos los espacios con 
el método strip().


"""


# VAMOS A VER EL ORDEN PARA HACER LAS FUNCIONES:

def frase(nombre, apellido, adjetivo):
   return f"Hola, me llamo {nombre} {apellido} y soy {adjetivo}"

last_name = input("Ingrese su apellido: ");
caracteristica = input("Ingrese una característica que tenga: ");
frase_1 = frase(name_1, last_name, caracteristica); # --> ACÁ ES: 
# EL PRIMERO CON EL PRIMERO, SEGUNDO CON EL SEGUNDO Y TERCERO CON EL TERCERO
print(frase_1);


# USANDO KEYWORD ARGUMENTS: 
frase_1 = frase(nombre = name_1, adjetivo= caracteristica , apellido =last_name)
# ACÁ ASIGNAMOS UN VALOR A CADA PARÁMETRO,
# ASÍ HACEMOS QUE CADA PARÁMETRO TENGA SU VALOR SIN IMPORTAR SU ORDEN.
# ESTO SE LLAMA "keyword arguments"
print(frase_1)


def frase(nombre, apellido, adjetivo = "guitarrista CRISTIANO"):
   return f"Hola, me llamo {nombre} {apellido} y soy {adjetivo}"

frase_1 = frase(apellido = last_name, nombre = name_1 )
print(frase_1)

# PODEMOS MODIFICAR IGUAL EL PARÁMETRO adjetivo:

frase_1 = frase(apellido = last_name, nombre = name_1, adjetivo = "programador"  )
print(frase_1)
