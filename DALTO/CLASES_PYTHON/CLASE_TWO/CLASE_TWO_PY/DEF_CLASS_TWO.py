"""
DEF:
En Python, def se utiliza para definir una función. 
Es una palabra clave que se coloca al inicio de una declaración de función,
y permite crear bloques de código que pueden ser reutilizados.
La sintaxis básica para definir una función con def es la siguiente:

def nombre_de_la_funcion(parametros):
    # cuerpo de la función
    # aquí va el código que realiza la función

nombre_de__la_funcion() ---> llamar a la función.

"""

def saludar(nombre):
    print(f"Hola {nombre} soy un estudiante de senati.")

nombre = input("Ingresa tu nombre: ")
llamada = saludar(nombre)
print(llamada) # --> ESTO IMPRIME: saludar(nombre) y luego un None
# Llamada almacena a la función saludar(nombre), después de imprimir esta función
# Después de imprimir la función, esta va a valer None, y al hacer 
# # print(llamada) va a imprimir el None. 

print(type(llamada)) # ---> imprime : NoneType (Ningún Tipo)


# AHORA VAMOS A VER COMO CAMBIAR EL VALOR QUE IMPRIME DESPUÉS DE LLAMAR A
# LA FUNCÓN saludar(nombre)
# VAMOS A HACER QUE NO SALGA NONE CON RETURN:

def media(num_1, num_2, num_3):
    media_0 = (num_1 + num_2 + num_3) / 3
    return media_0

llamada = media(2,2,5)
print(f"La media de tus notas es: {llamada}") 

print("________________________________________________________")



def promedio(mi_lista):
    if(len(mi_lista) == 0):
        return 0;
     
    n = len(mi_lista)
    suma = sum(mi_lista)
    Prome = suma / n
    return Prome


print("TU LISTA DE NOTAS PARA CALCULAR TU MEDIA EN TU CURSO.")

mi_lista = [];

cantidad = int(input("Ingrese el número de elementos que desea tener en su lista: "));

contador = 0

while(contador < cantidad):
    try:
      elemento = float(input(f"Ingrese la nota para el elemento {contador +1}: " ));
      
      mi_lista.append(elemento)
      contador += 1
    except ValueError:
        print("Por favor ingresa un valor numérico:)");
    
#print(mi_lista)

print(f"Tu promedio es: {promedio(mi_lista)}")

"""

PRINT VS RETURN : 
Print es una función de python que sirve para imoprimir valores por consola.
Return es una función o la sentencia que te permite utilizar 
los valores calulados en una función

def media(num_1, num_2, num_3):
    media = (num_1 + num_2 + num_3) / 3
    print(f"Hola {nombre}")
    return media --> Va a devolver por medio de la función: media()
                    todo lo que esté antes del return, lo que viene después no.

llamada = media(2,2,5)
print(f"La media de tus notas es: {llamada}") 

print("_________________________________________________")

def media(num_1, num_2, num_3):
    media = (num_1 + num_2 + num_3) / 3
   
    return media --> Va a devolver por medio de la función: media()
                    todo lo que esté antes del return, lo que viene después no.

     print(f"Hola {nombre}") --> ESTO NO VA A IMPRIMIRSE POR MEDIO DE LA FUNCIÓN RETURN
                                 PORQUE ESTÁ DESPUÉS DEL RETURN Y NO ANTES.

     
llamada = media(2,2,5)
print(f"La media de tus notas es: {llamada}") 

print("_________________________________________________")

"""

# keyword arguments : Es dar un valor desde los argumentos

def resta(num_1 = 3, num_2 = 2):
    return num_1 - num_2

print(f"Con los valores por defectos: {resta()}");
print(f"Usando el orden con sólo 1 valor: {resta(5)}");
print(f"Usando el orden con otros valores: {resta(5, 3)}");
print(f"Con keyword arguments: {resta(num_1 = 5, num_2 = 3)}");
print(f"Con solo un keyword argument: {resta(num_2 = 3)}");

print("_________________________________________________");

"""


print(f"No se puede hacer keyword argument antes de valores: {resta(num_1 = 3, 2)}")
print(f"Tampoco puedes dar valor por medio de keyword más de una vez a un elemento: {resta(num_1 = 2, num_1 = 3)}")
print(f"Tampoco puedes dar valor por medio de keyword más de una vez a un elemento: {1, num_1 = 3)}") --> El 1 se sobreentiende que ya es num_1

print("__________________________________________________________")
"""

# SCOPE: Alcance.
"""

SCOPE: scope se refiere al alcence de las variables.

SCOPE EN DEF:
- las variables hechas en un def, solo se puede acceder a ella por medio de esa función creada.
EJM:

media_0 = 4 --> ASÍ SE LLAME IGUAL QUE LA VARIABLE QUE ESTÁ EN LA FUNCIÓN,
                ESTOS SON VARIABLES DISTINTOS, PUES UNO ES DENTRO Y OTRA FUERA 
                DE LA FUNCIÓN.
                SI HACEMOS: print(media_0) --> Imprime: 4 
                Ya que está fuera de la función.
- EN ESTE CASO:
media_0 = 4 -> Es una varuable golbal

def media(num_1, num_2, num_3):
    media_0 = (num_1 + num_2 + num_3) / 3 --> media_0 solo se ejecutará al usar la función
    return media_0
    # (media_0) -> Variable local
print(media_0) --> Sale error, porque esta variable pertenece a una función 
                   y solo se ejecuta dentro de ella, no fuera.
    
llamada = media(2,2,5)
print(f"La media de tus notas es: {llamada}") 

- CUANDO SOLO SE PUEDE ACCEDER A UNA VARIABLE DESDE DENTRO DE UNA FUNCIÓN
SE LE VA A LLAMAR, VARIABLE LOCAL.

print("__________________________________________________________")

SCOPE EN WHILE:
-  El while loop crea un scope local dentro del bucle,
lo que significa que las variables definidas dentro del bucle 
solo son accesibles dentro de ese bloque de código. 
Sin embargo, las variables definidas antes del bucle son accesibles dentro del bucle.

- Python permite que las variables definidas dentro de un while (o for)
sean accesibles fuera de ese bloque si están en el ámbito global.

x = 10  # Variable fuera del while
while x > 0:
    y = 5  # Variable dentro del while
    print(x, y)
    x -= 1  # Modificando la variable x dentro del while
print(y)  # Esto imprime '5' ya que 'y' está accesible fuera del while

print("__________________________________________________________")

SCOPE EN FOR:
-El for loop también crea un scope local dentro del bucle.
Sin embargo, las variables definidas antes del for son accesibles dentro del bucle.

z = 20  # Variable fuera del for
for i in range(3):
    w = 2  # Variable dentro del for
    z += w
    print(i, w, z)
print(w)  # 'w' es accesible fuera del for, ya que fue definida dentro del bucle

print("__________________________________________________________")


COMO PASAR DE UNA VARIABLE LOCAL A GOLBAL:
- Para pasar una variable local a global, se utiliza la palabra clave global.
-Usamos la palabra clave -->  golbal

variable = 3
def funcion():
    global variable
    variable = 0
    return variable
    

print(funcion())
print(variable) # imprime: 0


"""
