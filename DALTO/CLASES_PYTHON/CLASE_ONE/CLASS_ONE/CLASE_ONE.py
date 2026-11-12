""" - PYTHON ES UN LENGUAJE DE PROGRAMACIÓN DE PROPÓSITO GENERAL,
YA QUE PUEDE SER UTILIZADO PARA CUALQUIER ACTIVIDAD.
-ES UN LENGUAJE DE ALTO NIVEL.
-FÁCIL DE APRENDER.
-TIPADO DINÁMICO. (la variable se ajusta al dato que se da, todo lo  contrario a un tipado no dinámico).
-LENGUAJE ORIENTADO A OBJETOS.
-ES UN LENGUAJE INTERPRETADO. """

#NONE : NO TIENE VALOR.

#PROGRAMA BASICO --> 

# input --> ingresar un valor o una cadena de texto

""" variable = tipo de variable(input("string"))

print("mi nombre es --> " , variable)   --> general
print("mi nombre es --> + str(variable)) --> numero """


"""nombre=input("INGRESE SU NOMBRE -->  ")
edad=int(input("INGRESE SU EDAD -->  "))

print("EL NOMBRE DEL USUARIO -->  ", nombre)
print(" LA EDAD DEL USUARIO -->  " + str(edad))"""


# DATOS SIMPLES:
"""  CADENA DE TEXTO: SE LES LLAMA STRIMG = CADENA TEXTO """
# -  "strimg" 
# -  'string'
# -  """string"""   
# -  '''string'''   

''' NUMEROS:
- ENTERO: int
edad=int(input("INGRESA SU EDAD: "))

-DECIMAL: float
donacion=float(input("INGRESE LA CANTIDD DE DONACIÓn: ")) '''

'''BOLEANO: 
True:1
False:0 '''
#_________________________________________________________________________

""" VARIABLES: 
a = 2
b = 3
c = a+b
print(C)
nombre = "flavio"
EN ESTOS CASOS a ; b ; c y nombre SON VARIABLES Y SE LES LLAMA ASÍ PUES SUS VALORES PUEDEM VARIAR.
AHORA LAS VARIABLES SE DECLARAN Y SE DEFINEN 
nombre =  ---> se declara
nombre= "FLAVIO" ; ---> se define """
"""
nombre="FLAVIO"
nombre="GERARDO"
print(nombre)
 '''EN ESTE CASO LA VARIABLE LA PRIMERA VEZ SALDRÁ FLAVIO Y LUEGO AL VER OTRA VARIABLE IGUAL DECLARADA PERO
 DEFINIDA DE OTRA FORMA PUES TOMARÁ LA ÚLTIMA VARIABLE EN ESTE CASO LA VARIABLE DEFINIDA CON GERARDO.'''


#TAMBIÉN PODEMOS HACER 
'''numero=21
   numero=21+1
   print(numero)
   
   numero=21
   numero+=1   ---> SI YO ANTEPONGO AL SIGNO (=) CUALQUIER SIGNO(+ ; - ; / ; * ; **) 
                    ESTOS SIGNOS VAN A AFECTAR  LO QUE SIGUE DESPUÉS DEL (=) ESTO SE PUEDE HACER CON DOS O MÁS VARIABLES.
   print(numero)
   EN AMBOS CASOS VA A SALIR 21"""



#CONDICIONES:
#IDENTIFICAR DOS NUMEROS SI SON MAYOR O IGUAL -->  

v1=float(input("INGRESE V1 -->   "))
v2=float(input("INGRESE V2 -->   "))

if (v1>v2):
    print("V1 ES MAYOR QUE V2")
elif(v2>v1):
    print("V2 ES MAYOR QUE V1")
else:
    print("V1 Y V2 SON IGUALES")
#______________________________________________________________________

#CONCATENACUÓN:
#concatenar con +.
nombre= "lucas"
bienvenida= "hola" + nombre + "como estás"
print(bienvenida)


#TAMBIÉN PODEMOS USAR:
nombre=5
bienvenida= "HOLA " + str(nombre) + " ¿CÓMO  ESTÁ?" #concatenar con f-strings.
print(bienvenida)
#ESTE ÚLTIMO CASO ES MÁS OPTIMO PUES SIRVE TANTO PARA TEXTO COMO NÚMEROS.



#OPERADORES DE PERTENENCIA (in / is not / not in)
#EJM: 
print("HOLA" in bienvenida)    #true
print("HOLA" is not bienvenida) #false
print("xd" not in bienvenida) # true
#_______________________________________________________________________________


#DATOS COMPUESTOS:
"""DATOS QUE DENTRO DE ELLOS TIENEN OTROS DATOS SIMPLES U OTROS DATOS COMPUESTOS PERO QUE PODEMOS AGRUPARLOS"""
# -1) list / lista
lista=["Flavio Silva", "Flavio.G.S.E." , 17, "Guitarrista CRISTIANO"]
print(lista)
print(lista[0]) #ESTO ES PARA MOSTRAR UNA SOLA COSA DE LA LISTA
                # EN PROGRAMACIÓN CONTAMOS DEL 0 - 9 , SE LEE, PRIMER ELEMNTO, INDICE CERO, ETC..


# -2) tupla
tupla = ("Flavio Silva" , "Flavio.G.S.E." , 17 , "Guitarrista CRISTIANO")
print(tupla[0]) #ESTO ES PARA MOSTRAR UN ELEMENTO DE LA TUPLA.
                # EN PROGRAMACIÓN CONTAMOS DEL 0 - 9 , SE LEE, PRIMER ELEMNTO, INDICE CERO, ETC..
                #EN EL CASO DE TUPLA NO SE PUEDE MODIFICAR LOS ELEENTOS.


lista=["Flavio Silva", "Flavio.G.S.E." , 17, "Guitarrista CRISTIANO"]
tupla=("Flavio Silva", "Flavio.G.S.E", 17 , "Guitarrista CRISTIANO")

tupla[3]= "hola"

print(tupla[3])  # NO SE PUEDE HACER ESTO PUES EN LA TUPLA NO SE PUEDE MODIFICAR LOS ELEMENTOS PERO EN LA LISTA SÍ SE PUEDE.
   # EN CASO DE MODIFICAR LA LISTA HUBIERA SIDO ASÍ:
   #     lista[3]= "hola"
   #     print(lista[3])



# -3) set / conjunto
#CREANDO UN CONJUNTO (set)

conjunto = {"Flavio Silva" , "FLAVIO.G.S.E." , 17 , "Guitarristia CRISTIANO"}
#LOS CONJUNTOS NO TIENEN UN ORDEN FIJO, PUEDEN INTERCAMBIARSE.
#NO SE PUEDEN MODIFICAR LOS ELEMENTOS MEDIANTE EL ÍNDICE.
#A DIFERENCIA DE LA LISTA, EN LOS CONJUNTOS NO SE PUEDEN ACCEDER A LOS ELEMENTOS POR EL ÍNDICE.
#NO PERMITE REPETIR VALORES, MIENTRAS LA TUPLA Y LA LISTA SÍ.


# -4) dict / diccionario 
diccionario= {
    'nombre': "Flavio Silva" ,
    'canal' : "Flavo.G.S.E." ,
    'edad' : 17 ,
    'profesion' : "Guitarrista CRISTIANO" ,
    'dato_duplicado' : "Flavio Silva"
}
print(diccionario['nombre']) # AL ESCRIBIR ESTO HAGO QUE EL PROGRAMA MUESTRE EL DATO LLAMADO 'NOMBRE' DEL DICCIONARIO.
                             # nombre en diccionario sería key = clave y Flavio Silva es value = valor.

 #___________________________________________________________________________________________________

#OPERADORES ARITMÉTICOS:
"""
+ (suma) ---> suma = 12 + 5
- (resta) ---> resta = 12 - 5
* (multiplicación) ---> multiplicación = 12 * 5
/ (división) ---> division = 12/5 (LA DIVISIÓN NOS DEVUELVE UN DATO float ASÍ SEA ANETERO.)
// (división baja,  devuelve el entero de la división.) ---> division_baja = 12 // 5
% (moódulo- devuelve el resto de la división) ---> resto = 12 % 5
** (potencia) --->  potencia = 12 ** 5     
PARA HALLAR RAÍZ CUADRADA podemos hacer así:
import math
numero = x ---> float
print(math.sqrt(numero);
Para Hallar cualquier raíz podemos hacer por así:
numero = x ---> float
denominador = y --- int
print(numero**(1/denominador)); ---> Esto ya que en el exponente fraccionario el denominador es raíz 
"""

suma= 12 + 5

resta = 12 - 5

multiplicacion = 12 * 5

division = 12 / 5 #devueleve un  dato float pues así sea un entero va asalir con  un  ounto algo(2.0).

division_baja = 12 // 5 #devuelve un dato int pues este redondea hacia abajo (2.4 = 2  ; 2.9 = 2).

resto = 12 % 5 #muestra el resto(5 * 2 = 10  y para 12 falta 2).

potencia = 12 ** 5

# type(dato) nos devuelve que tipo de dato es:
tipo_de_dato= type(division_baja)

#_______________________________________________________________________________________________________________


#OPERADORES DE COMPARACIÓN: nos devuelven true o false,  sirven para condicionales.
"""
== (igual que)
!= (distinto de)
> (mayor que)
< (menor que)
>= (mayor o igual que)
<= (menor o igual que)  """

igual_que = 5 == 6     #false

distinto_de = 5 != 6   #true

mayor_que = 5 > 6      #false

menor_que = 5 < 6      #true

mayuor_igual = 5 >= 6  #false

menor_igual = 5 <= 6   #true

a = 5
b = 10
c = 20
comparacion_1 = a + b  == c 
comparacion_2 = a + b  != c
comparacion_3 = a + b  >  c
comparacion_4 = a + b  <  c
comparacion_5 = a + b  >= c
comparacion_6 = a + b  <= c

print(comparacion_1)
print(a + b == c)

contraseña_almacenada = "flaviogse"
contraseña_escrita = "flavio"

print(contraseña_almacenada == contraseña_escrita )

#_______________________________________________________________________________________________________________

#CONDICIONALES: Si la condición se cumple es TRUE y el código se va a ejecutar.
               #Si la condición no se cumple es FALSE y el código no se va a ejecutar.
               #Si es FALSE entonces podemos hacer que otro código se ejecute, ahí se ve el if , elif , else.
#EJM:
edad = int(input("INGRESE SU EDAD:  "))
if edad >= 18: 
    print("Eres mayor de edad")
    #todo lo que se escriba acá es prter de if.

else:
    print("Eres menor de edad")
    #todo lo que se escriba dentro es partr de else.Por eso else es escribe fuera de if.

print("No forma parte de ninguna condición") #--> Al no formar parte de nada igual se va a ejecutar.
#ESTRUCTURA: 
condición= "xd"
acción= "xd"
if condición ():  #  1)si esto es true.
    acción  #--> 1)la acción se ejecuta.

if condición (): # 2)Si esto es false.
    acción   #-->2)la acción no se ejecuta

# else - if (elif)
#EJM:

ingreso_mensual = 14000
gastos_mensual = 4000

if (ingreso_mensual >= 10000):
    
    if (ingreso_mensual - gastos_mensual < 0):   # ----> esto es un anidados
      print("Estás en deficit.")
    
    elif ingreso_mensual - gastos_mensual > 3000:
     print("Estás bien")  
    
    else:                        # ---> este else va dentro del primer if
     print("Regula tus gastos")


elif (ingreso_mensual >= 1000):    # ---> un elif va después de u n if no después de un else.
     print("Estás bien en latinoamerica.")


elif (ingreso_mensual >= 500):
    print("Estás bien en colombia.")    #----> se puede poner varios elif.


else: 
    print("Estás mal:(")


# ACÁ SE PONE EN ORDEN, PRIMERO COMPARA SI EL INGRESO ES MAYOR A 10000
#LUEGO COMPARA SI  ES MAYOR A 1000 Y SINO PUES SI ES MAYOR A 500 Y SINO  SALLE EL else.

#_____________________________________________________________________________________________


#OPERADORES LÓGICOS: 
# 1) and   Para que sean True ambos valores deben ser verdadero.
Resultado1 = True and True #Devolver True
Resultado2 = False and True #Devolver False
Resultado3 = True and False #Devolver False
Resultado4 = False and False #Devolver False

"""El and lo podemos usar en condicionales,
ya que para que el resultado sea True se necesita dos True."""

# 2) or  Para que sean False ambos deben ser falsos
Resultado5 = True or True #Devolver True 
Resultado6 = False or True #Devolver True
Resultado7 = True or False #Devolver True
Resultado8 = False or False #Devolver False

"""Este or también puede servir en condicionales, 
ya que para ser True solo se necesita cumplir una condición y no necesariamente todas las requeridas."""

# 3) not
Resultado9 = not True #Devolver False
Resultado10 = not False #Devolver True

Resultado11 = not 2 == 2 #Devolver False
Resultado12=  not 2 == 3 #Devolver True 
print(Resultado11)

"""Este not, tamnién sirve para condicionales,
pues si pones not(2 == 2), con esto dices que 2 no es igual a 2, o sea 2 != 2."""

# 4) & :  Para evaluar en número se usa los numeros enteros pero hechos en 0 y 1.
# en este caso veremos al evalular String, pero estos strings se convierten a conjuntos set.
# Una vez convertido a Set se va a evalular las intersecciones que tengan estas cadenas:

contrasena = "Flavio@!!";

contra = set(contrasena);

signos = {"!","@","#","%","^","&","*","_" , "/"} ; # Esto es un set

if (set(contrasena) & signos) : # El & en un set, significa intersección.  
    print("Valido!!");

else:
    print("Invalido :(");

print(contra & signos);   
                                  # AMBOS CORRECTOS :)
print(set(contrasena) & signos);

"""SI EN UN STRING (HECHO YA SET) NO TIENE NADA EN COMÚN O ESTÁ VACIO, AL HACER PRINT, EL RESULTADO 
QUE SE MOSTRARÁ SERA: () --> ESO DICE QUE ESTÁ VACIO"""

#______________________________________________________________________________________________

#MÉTODOS DE CADENAS: (string methods)   
#ESTRUCTURA DE MÉTODO
#  dato.metodo()   ; print(dato.metodo())

# 1) dir : Devuelve la lista de atributos válidos del objeto pasado. 
          # dir es una función de Python y no es un método.
          #ESTRUCTURA DE FUNCIÓN:   función(dato)   ; print(función(dato))

cadena1 = "soy flavio"
cadena2 ="bienvenido"

resultado = dir(cadena1)  # ----> FUNCIÓN 


print(resultado)     #FORMA 1
                     #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(dir(cadena1))  #FORMA 2  ----> FUNCIÓN

# 2) len : Cuenta los caracteres de una cádena. (ES UNA FUNCIÓN).

cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO"

resultado = len(cadena2)

print(resultado)         #FORMA 1
                         #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(len(cadena1))     #FORMA 2  


# 3) upper : convierte a mayúscula.
           # Esto es un método.

cadena1 = "soy flavio"
cadena2 ="BIENVENIDO"

resultado = cadena1.upper()  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)       #FORMA 1
                       #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena1.upper()) #FORMA 2



# 4) lower : convierte a minúscula.

cadena1 = "soy flavio"
cadena2 ="BIENVENIDO"

resultado = cadena2.lower()  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)       #FORMA 1
                       #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena2.lower()) #FORMA 2          


# 5) capitalize : Primera en mayúscula. Convierte todo en minúscula y la primera en mayúscula.

cadena1 = "soy flavio"
cadena2 ="BIENVENIDO"

resultado = cadena2.capitalize()  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)            #FORMA 1
                            #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena2.capitalize()) #FORMA 2          


# 6) find : Encuentra la primera aparición del valor especificado, sino hay coincidencia devuelve -1.

cadena1 = "soy flavio"
cadena2 ="BIENVENIDO"

resultado = cadena1.find("flavio")  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.
                             # ---> EN ESTE CASO AL PONER LA LETRA "flavio" VA A BUSCAR SU PRIMERA APARICIÓN 
                             # Y LA PRIMERA APARICIÓN ES 4 (SE CUENTA DEL 0 AL 9) y toma en cuenta al espacio.
                             #INCLUSO SE PUEDE BUSCAR LOS ESPACIOS: resultado = cadena1.find(" ").

print(resultado)              #FORMA 1
                              #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena1.find("flavio")) #FORMA 2          


# 7) index : Encuentra la primera aparición del valor especificado, si es que no hay coincidencia devueleve una excepción (error).

cadena1 = "soy flavio"
cadena2 ="BIENVENIDO"

resultado = cadena2.index("V")  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.
                                # ---> EN ESTE CASO AL PONER LA LETRA "V" VA A BUSCAR SU PRIMERA APARICIÓN 
                                # Y LA PRIMERA APARICIÓN ES 4 (SE CUENTA DEL 0 AL 9).
                                #INCLUSO SE PUEDE BUSCAR LOS ESPACIOS: resultado = cadena1.index(" ").

print(resultado)         #FORMA 1
                         #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena2.index(" ")) #FORMA 2  ---> ACÁ SALE ERROR PUES NO HAY NINGÚN ESPACIO.         


# 8) isnumeric :  REVISA SI ES UN TEXTO CON VALORES NUMÉRICO. Si es numérico devuelve TRUE sino FALSE.
                # ASÍ TENGA NÚMEROS Y UNA SOLA CONSONANTE O VOCAL VA A SALIR FALSE.
                # LOS CARACTERES NUMÉRICOS SON VÁLIDOS SI ESTÁN JUNTOS Y NO CON ESPACIOS.
cadena1 = "22112021"
cadena2 ="BIENVENI2"

resultado = cadena2.isnumeric()  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)           #FORMA 1 ---> FALSE
                           #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena1.isnumeric()) #FORMA 2  ---> TRUE


# 9) isalpha : REVISA SI ES UN TEXTO CON CONSONANTES Y VOCALES. Si es alfa numérico devuelve TRUE y si no sale FALSE.
             # ASÍ TENGA MUCHAS LETRAS PERO UN NÚMERO VA A SALIR FALSE. 
             # LOS CARACTERES QUE SON VÁLIDOS SON DESDE LA  A - Z ; EL ESPACIO NO  ES VÁLIDO ASI QUE DEBE ESCRBIRSE SIN ESPACIOS PARA SER VÁLIDO
             # el es´pacio es un caracter especial.
cadena1 = "SoyFlavio"
cadena2 ="BIENVENI2"

resultado = cadena2.isalpha()  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)         #FORMA 1 ---> FALSE
                         #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena1.isalpha()) #FORMA 2 --> TRUE  


# 10) count : Devuelve el número de ocurrencias (coincidencias) de una cadena en la cadena dada y en una lista o tupla.

cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO"

resultado = cadena2.count("N")  # ---> ASÍ SE HACE PARA EJECUTAR UN MÉTODO.

print(resultado)         #FORMA 1
                         #AMBAS FORMAS SE PUEDE HACER LA FORMA 1 O FORMA 2.
print(cadena1.count("Flavio"))   #FORMA 2


# 11) startswith:  Verificamos si una cadena empieza con otra cadena dada, si es así devuelve TRUE y sino FALSE.
               # CUENTA LOS CARACTERES.

cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO"

resultado = cadena1.startswith("Soy") # ASÍ ES UN MÉTODO ---> TRUE

print(resultado)

print(cadena1.startswith("s"))  # ---> FALSE


# 12) endswith : Verificamos si una cadena termina con otra cadena dada, si es así devuelve TRUE sino  FALSE.
              # CUENTA LOS CARACTERES.

cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO"

resultado = cadena1.endswith("o") # ASÍ ES UN MÉTODO ---> TRUE

print(resultado)

print(cadena1.endswith("S"))  # ---> FALSE


# 13) replace : Remplaza un valor por otro (remplaza un pedazo de la cadena dada, por otra dada).
# BUSCA UNA COINCIDENCIA EN LA CADENA Y LA REMPLAZA Y SINO DEVUELVE LA CADENA ANTERIOR ORIGINAL.
#ADEMÁS REMPLAZA NO SOLO A LA PRIMERA APARICIÓN DE COINCIDENCIA SINO A TODAS.
cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO,Como,Estás"

resultado =  cadena1.replace("o","to")  #---> Stoy Flavito (remplazó a todos).

print(resultado)

print(cadena1.replace("Soy Flavio","SOY UN FLAVITO FELIZ SHI")) #--->REMPLAZÓ A TODA LA CADENA DE TEXTO.

resultado_2 = cadena2.replace(","," ") #---> ACÁ REMPLAZO (",") POR (" ")

print(resultado_2.capitalize())


# 14) split: separar cadenas con la cadena que le pasemos. (genera una lista)
#PARA SABER EL TIPO DE DATO HACEMOS ESTO print(type(variable))

cadena1 = "Soy Flavio"
cadena2 ="BIENVENIDO,Como,Estás"

resultado = cadena2.split(",") # ---> SI EN LA CADENA ENCUENTRA EL CARACTER QUE PONEMMOS (,) VA A SEPARARLO Y ASÍ GENERARÁ UNA LISTA.
print(resultado)

print(type(resultado)) #---> ASÍ VEMOS QUE TIPO DE DATO ES (LISTA)

print(resultado[0]) #---> Para que nos muestre que tiene en el índice 0
                    # En este caso en el índice [0] está BIENVENIDO.
                    
# Ahora si tenemos muchos espacios entre palabras, como:
# hola     como  estás        mi amigo.
# Para caso así, donde solo queremos las palabras, hacemos esto:

cadena1 = "Hola      como estás            mi amigo."
print(cadena1.split())

# 15) title: Transforma la primera letra de cada palabra a mayus.

dato = "hola mundo";
titulo = dato.title();
print(titulo); # Hola Mundo

# 16) strip: Elimina los espacios del inicio y del final del string.

dato_1 = "  Hola mundo  ";
resultado_3 = dato.strip();
print(resultado_3); # "Hola mundo"


# 17) isalnum:
""" 
El método sin parámetros llamado isalnum() comprueba si 
la cadena contiene solo dígitos o caracteres alfabéticos (letras) 
y devuelve True (verdadero) o False (falso) de acuerdo al resultado.
"""

# Demostración del método isalnum():
print('lambda30'.isalnum())
print('lambda'.isalnum())
print('30'.isalnum())
print('@'.isalnum())
print('lambda_30'.isalnum())
print(''.isalnum())

# 18) islower: Verifica si solo son letras minúsculas (True) o no (False):
text = "hola mundo"
print(f"{text.islower()}") # True
text = "Hola Mundo"
print(f"{text.islower()}") # False

# 19) isspace: Si está compuesto de espacios es True , y si tiene otros 
# caracteres aparte de espacios es False
text = " "
print(f"{text.isspace()}") # True
text = "\n"
print(f"{text.isspace()}") # True
text = "Hola Mundo"
print(f"{text.isspace()}") # False

# 20) isupper : Si todo está en mayúsculas es True, sino es False
text = "HOLA MUNDO"
print(f"{text.isupper()}") # True
text = "Hola Mundo"
print(f"{text.isupper()}") # False

# 21) join : Espera un Iterable en formato String (str)
# y realiza una unión entre los elementos, por decir:
# Borra los corchetes, parentesis, llaves

lista = ["hola", "xd", "que tal"]
result = ", ".join(lista)
print(result) # hola, xd, que tal

lista_1 = [1,2,3,4]
result = ", ".join(str(x) for x in lista_1)
print(result) # 1, 2, 3, 4
#________________________________________________


tupla =  ("hola", "xd", "que tal")
result = ", ".join(tupla)
print(result)

tupla_1 = (1,2,3,4,5)
result = ", ".join(str(x) for x in tupla_1)
print(result)
#___________________________________________________

set = {"hola", "xd", "que tal"}
result = " ,".join(set)
print(result) # hola, xd, que tal

set_1 = {1,2,3,4,5}
result = ", ".join(str(x) for x in set_1)
print(result)
#_____________________________________________________


dict = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4
    
}

# Ver solo los keys:
result = ", ".join(dict) # dict.keys
print(result)

# Ver solo los values:
result = ", ".join(str(x) for x in dict.values())
print(result)

# Ver tanto Keys como Valuse:
result = ", ".join(f"{key}: {values} " for key, values in dict.items())
print(result) # one:1 two:2 three:3 four:4

# 22) swapcase : Afecta solo a letras, si está en mayus lo pasa a minúscula
# y si está en minúscula, lo pasa a mayúscula, los demás caracteres siguuen iguales

text = "Hola, ¿Cómo estás?"
text_converter = text.swapcase()
print(text_converter)

""" 
DATO DE LOS STRING:
- Al compararlos tengamos en cueneta esto:
    - Dos cadenas son iguales cuando consisten de los mismos caracteres
    en el mismo orden. Del mismo modo, dos cadenas no son iguales 
    cuando no consisten de los mismos caracteres en el mismo orden.

        Ambas comparaciones dan True (verdadero) como resultado:
        
        'alpha' == 'alpha' ---> True
        'alpha' != 'Alpha' --> True

    - Cuando se comparan dos cadenas de diferentes longitudes y la más corta 
    es idéntica a la más larga, la cadena más larga se considera mayor.

        Justo como aquí:
        
            'alpha' < 'alphabet' --> True
        
    - La comparación de cadenas siempre distingue entre mayúsculas y 
    minúsculas (las letras mayúsculas se consideran menores en comparación 
    con las minúsculas).
    
        Justo como aquí:

            'beta' > 'Beta' --> True

"""

# 23) isdigit() : Sirve pasa ver si todos los caracteres del str son numéricos -- Retorna True o False
cadena = "12345"
if cadena.isdigit():
    print("Todos los caracteres son dígitos.")
else:
    print("La cadena contiene caracteres no numéricos.")
# Salida: Todos los caracteres son dígitos

#______________________________________________________________________________________________________________________


# MÉTODOS DE LISTAS:
   
# 1) list : Función / Convierte cualquier cadena, tupla, set, diccionario en una lista.

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", 17])

resultado = len(cadena1) # ---> ACÁ USO LEN PARA CONTAR LOS ELEMENTOS DE LA LIST.

print(cadena1)
print (resultado)

xd =["hola", "como estás", 17] # --.> otra forma de hacer una list.
print(xd)
print(len(xd))  #---> USAMOS LEN PARA CONTAR LA CANTIDAD DE ELEMENTOS.


# 2) Agregando un elemento con append :  SOLO SE PUEDE AGREGAR UN ELEMENTO.
# append modifica directamente a la lista por ello : print(cadena1)

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", 17])

cadena1.append("ESTOY FELIZ") # ---> se hace así

print(cadena1) #---< se hace así.

print(cadena1.append("jrjrjr")) # ---> No sé puede hacer esto.


# 3) insert : Agrega un valor a la lista pero en el índice indicado o especificado.

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", 17])

cadena1.insert(1,"Que tal!!")

print(cadena1)   


# 4)  extend : Con esto agregamos varios elementos a la lista.

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", 17])

cadena1.extend(["SOY UN SENATINO", "ESTUDIO EN SENATI", "EN LA SEDE DE INDEPENDENCIA"])

print(cadena1)

# 5) pop : elimina un elemento de una lista, pide índice y devuelve valor.
# Y si ponemos -1 eliminar el último elemento, -2 (anteúltimo), etc..

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", 17])
print(len(cadena1))
cadena1.pop(0)

print(cadena1)

print(len(cadena1)) #---> muestra el número de elementos después de borrar el elemento del índice 0

cadena1.pop(-1)

print(cadena1)

print(len(cadena1)) # --> muestra el número de elementos después de borrar el último elemento de la lista, índice (4)


# 6) remove : Remueve un elemento de la lista, pide valor.

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", "Quien eres", 7])

cadena1.remove("Quien eres")

print(cadena1)


# 7) clear : Elimina todos los elementos de la lista

cadena1 = list(["Hola", "Soy Flavio", "Tengo 17 años", "Me gusta tocar la guitarra y programar", "Quien eres", 7])

cadena1.clear()

print(cadena1)



# 8) sorted : Ordena la lista igual como sort, pero lo alamacena en una variable
# Funciona en lista, tupla, set, diccionrios
lista = [111, 34, 12, 0 , 1, 10]
lista_ordenada = sorted(lista)
print(lista)
print(lista_ordenada)

# ORDENAR LISTA DE LETRAS Y NÚMEROS:

# Lista con números y texto
mi_lista = [3, "banana", 1, "apple", 2, "cherry"]

# Usando sorted() con key=str para convertir todo a texto
sorted_list = sorted(mi_lista, key=str)

print(sorted_list)  # Salida: [1, 2, 3, 'apple', 'banana', 'cherry']



# 9) sort : ordena los elementos de forma ascendente.
# Si es de texto, se ordena alfabéticamente

cadena1 = list([1000 , -1, 300, 1 , 800 , 9999 , 210 , 2 , 5 , 3 , False, True])

cadena1.sort()

print(cadena1)

# ORDENAR CON LISTAS DE NUMEROS Y LETRAS:

# Lista con números y texto
mi_lista = [3, "banana", 1, "apple", 2, "cherry"]

# Usando sort() con key para convertir todos los elementos a texto
mi_lista.sort(key=str)

print(mi_lista)  # Salida: [1, 2, 3, 'apple', 'banana', 'cherry']


# como DATO : SI  HAY FALSE, TRUE, va a ordenar primero el False y luego el True y de ahí recien los números de forma ascendente.
# ANTES DEL TRUE VA EL 1 Y ANTES DEL FALSE VA EL -1 

#TAMBIÉN SE PUEDE ASÍ : 

cadena1.sort(reverse=True)
print(cadena1) # ---> hace que el orden sea en reversea ( mayor s menor ) --- 1 , 2 , 5 , 10 =  10 , 5 , 2 , 1

cadena1.sort(reverse=False) # ---> hace que el orden no sea (mayor a menor() sino (menor a mayor)--- 10 , 5 , 2 , 1 =  1 , 2 , 5 , 10

# 10) copy = Hace una copia de la lista y la almecena en otra variable:

cadena1 = list([1000 , -1, 300, 1 , 800 , 9999 , 210 , 2 , 5 , 3 , False, True])

copia_lista = cadena1.copy()

print(cadena1)
print(copia_lista)

# 10) reverse = Hace que el orden se invierta ( es lo mismo qur hace con sort pues SORT primero ordena y revrrse() hace la inversa).
# Vamos a invertir la copia_lista y la cadena1 va a quedar normal.

copia_lista.reverse()

print(cadena1)

print(copia_lista)

# 11) index() : Busca el índice de un elemento en la lista.
my_list = ["Fabian", "Flavio", "Geraro","Estrada", "Flavio"]
print(my_list.index("Flavio")) # imprime 1 , ya que en esa posición está la primera aparición

#______________________________________________________________________________________________________________________________________

#MÉTODOS DE DICCIONARIOS: 

# 1) keys() : devuelve una lista de las claves del diccionario (o sea muestra que dato hay, en este caso nombre), también sirve para iterar.

diccionario = {
    "nombre": "Flavio",            # en ves de nombre puede ir : 0
    "apellido": "Silva",           # en ves de apellido puede ir : 1
    "edad":17                      # en ves de edad puede ir : 2  
}                                  # se puede usar claves númericas si deseamos, pero mejor es no hacerlo


claves = diccionario.keys()

print(claves)


# 2) get() : devuelve el valor de una clave

diccionario = {
    "nombre": "Flavio",             # en ves de nombre puede ir : 0
    "apellido": "Silva",            # en ves de apellido puede ir : 1
    "edad":17                       # en ves de edad puede ir : 2  
}                                   # se puede usar claves númericas si deseamos, pero mejor es no hacerlo así.
   

claves = diccionario.get("nombre")    # ---> forma1   --->  así no lo encuentre continua el programa.
                               # AMBAS FORMAS SON VÁLIDAS, PERO LA PRIMERA ES LA MEJOR
claves = diccionario["nombre"]  # ---> forma 2   ---> si no encuentra nada el programa se detiene.

print(claves)


# 3) clear() : elimina todos los elementos.

diccionario = {
    "nombre": "Flavio",          # en ves de nombre puede ir : 0
    "apellido": "Silva",         # en ves de apellido puede ir : 1
    "edad":17                    # en ves de edad puede ir : 2
}                                # se puede usar claves númericas si deseamos, pero mejor es no hacerlo.

diccionario.clear()   

print(diccionario)


# 4) pop() : elimina un elemento, pidiendo clave.

diccionario = {
    "nombre": "Flavio",          # en ves de nombre puede ir : 0
    "apellido": "Silva",         # en ves de apellido puede ir : 1
    "edad":17                    # en ves de edad puede ir : 2
}                                # se puede usar claves númericas si deseamos, pero mejor es no hacerlo.

diccionario.pop("nombre")

print(diccionario)

# 5) items() : para iterar el dict en un loop for.

diccionario = {
    "nombre": "Flavio",          # en ves de nombre puede ir : 0
    "apellido": "Silva",         # en ves de apellido puede ir : 1
    "edad":17                    # en ves de edad puede ir : 2
}                                # se puede usar claves númericas si deseamos, pero mejor es no hacerlo.

diccionario_iterable = diccionario.items()

print(diccionario_iterable)  # ---> con esto iteramos el diccionario y recorremos el elemento para luego acceder a cada uno.

#6) values : Muestra el valor de cada claves, sin mostrar las claves.

clave = diccionario.values();
print("LOS VALORES DE CADA CLAVES SON:\n" + str(clave))  


# 7) sorted() : Para ordenar, en este caso será alfabéticamente 
# a) Por key:
agenda = {'flavio': '12345', 'juan': '67890', 'maria': '11223', 'ana': '33445'}

# Ordenar por clave
ordenado_por_clave = dict(sorted(agenda.items()))

print(ordenado_por_clave)

""" 
Salida:
{'ana': '33445', 'flavio': '12345', 'juan': '67890', 'maria': '11223'}
"""
# b) Por value:
agenda = {'flavio': '12345', 'juan': '67890', 'maria': '11223', 'ana': '33445'}

# Ordenar por valor
ordenado_por_valor = dict(sorted(agenda.items(), key=lambda item: item[1]))

print(ordenado_por_valor)

""" 
Salida:
{'maria': '11223', 'flavio': '12345', 'ana': '33445', 'juan': '67890'}
"""

#___________________________________________________________________________________________________________________________________


# input :  

# 1) Pedir datos al usuario : 

name = input("What is your name? : ")    # ------> ACÁ ESTAMOS USANDO CADENAS DE TEXTO.

print(name)

print("El nombre es: " + str(name)) # ---> Agregando texto y + str(name)

print(f"El nombre es: {name}")      # ---> Concatenando



number = float(input("INGRESA EL NÚMERO: "))   # -------> ACÁ ESTAMOS USANDO NÚMEROS (INT) , (FLOAT).

print(f"El número es: {number}")

print("EL NÚMERO ES: " + str(number))

resultado = int(float(number)*2)  # ---> ESTO SI QUEREMOS QUE LA MULTIPLICACIÓN EN SU RESULTADO NO TENGA DECIMAL.

print(resultado)

"""
DESPUÉS DE ESTO VIENE EJERCICIOS DE CLASE ONE.
"""

#______________________________________________________________________________________________________________

# FECHA Y HORA ACTUALES CON datatime.

import datetime # --> FUNCIONES PARA TRABAJAR CON FECHAS Y HORAS.
ahora = datetime.datetime.now()

print(ahora) # --> IMPRIME LA FECHA Y HORA ACTUAL.

print(type(ahora))

print(ahora.strftime("%d/%m/%Y  %H:%M:%S")) #---> ACÁ SE´PARAMOS LA FECHA EN DIA(%d), MES(%m), AÑO(%Y), hora(%H), MINUTO(%M), SEGUNDO(%S)


#______________________________________________________________________________________________________________________