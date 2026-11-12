""" 
Un decorador toma una función como entrada, le agrega una funcionalidad extra,
y devuelve como salida la misma función pero modificada (bien antes o después
de ejecutarse).

No cambia el código original de la función.

Pueden ser usados, para el manejo de excepciones, validación de datos,
la medición del tiempo de ejecución, en flask , etc...
"""
def Decorador(funcion):
    def funcion_modificada():
        print("Antes de llamar a la función:")
        x = funcion()
        print(x)
        longitud = len(x)
        mensaje =(f"Tu función es de longitud {longitud}")
        return mensaje   
    return funcion_modificada

# def Saludo():
#      print("Hola Mundo")


# saludo_modificado = Decorador(Saludo)

# saludo_modificado()

""" USAMOS EL DECORAOR @ PARA LLAMAR A LA FUNCIÓN Decorador() """
@Decorador
def Saludo():
    return"Hola Mundo"

longitud =Saludo()
print(longitud)

print(Saludo())


""" 
Investigar sobre decoradores de clase y multiple


"""


""" VAMOS A VER UN POCO DE FUNCIONES """
def Suma(a,b):
    return a + b

def Resta(a,b):
    return a - b

def Ejecutar_operacion(funcion,a,b):
    print("Ejecutando la operación...")
    result = funcion(a,b)
    mensaje = f"El resultado de la operación es: {result}"
    print("Operación ejecutada.")
    return mensaje
    

# Vamos a llamar a una función dentro de otra función:
resultado = Ejecutar_operacion(Suma,5,3)
print(resultado)
resultado = Ejecutar_operacion(Resta,5,3)
print(resultado)


""" 
DECORADORES:
- Un decorador es una función el cual recibe como parámetro otra función, y retorna 
ota función (va a agregar algunas cosas a la función original / pasada como argumento).

- Trabajamos con por lo menos 3 funciones:
1) Input 
2) Output
3) La función principal (la que va a ser decorada)

- Miremos como una pequeña formula matemárica: A , B , C 
A(B) -> C
- A es la función decoradora
- B es la función que va a ser decorada
- C es la función resultante (la función decorada)
- Explicado de otra forma: A recibe como argumento a B y retorna C
"""

def funcion_a(funcion_b):
    # Como retorna otra función, debemos de anidar otra función
    def funcion_c( *args, **kwargs):
        print("Antes de llamar a la función")
        x = funcion_b(*args, **kwargs)
        print("Después de llamar a la función")
        return x
    return funcion_c

@funcion_a
def Saludo(name, edad=10, ciudad = "Huaral"):
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

saludar = Saludo("Flavio", 18)
print(saludar)

""" 
Usamos los *args y **kwargs para que la función decorada pueda recibir
cualquier cantidad de argumentos posicionales y de palabras clave sin que 
tengamos que poner la misma cantidad de parámetros de B en C.

- *args: Recibe una cantidad variable de argumentos posicionales y los
empaqueta en una tupla.
- **kwargs: captura los parámetros con nombre
Esto hace que la función decorada sea más flexible y pueda manejar
diferentes firmas de funciones sin problemas.
"""

# Refactorizando y usando la convención para funcion_c
def my_custome_decorator(function):
    # Como retorna otra función, debemos de anidar otra función
    def wrapper( *args, **kwargs):
        print("Antes de llamar a la función")
        x = function(*args, **kwargs)
        print("Después de llamar a la función")
        return x
    return wrapper

@my_custome_decorator
def Saludo(name, edad=10, ciudad = "Huaral"):
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

saludar = Saludo("Flavio", 18)
print(saludar)


#_____________________________________________________________________
def Calcular_tiempo_ejecucion(function):
    import time
    def wrapper( *args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        tiempo_ejecucion = end - start
        print(f"Tiempo de ejecución: {tiempo_ejecucion } segundos")
        return result
    
    return wrapper

@Calcular_tiempo_ejecucion
def Saludo(name, edad=10, ciudad = "Huaral"):
    import time
    time.sleep(2)
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

saludar = Saludo("Flavio", 18)
print(saludar)

print("_______________________________________________________________________")

# FORMA DE HACERLO CON DECORDORES APILADOS:

@my_custome_decorator
@Calcular_tiempo_ejecucion
def Saludo(name, edad=10, ciudad = "Huaral"):
    import time
    time.sleep(2)
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

saludar = Saludo("Flavio", 18)
print(saludar)

print("_______________________________________________________________________")

# FORMA DE HACERLO PERO SIN DECORADORES APILADOS:

def Saludo(name, edad=10, ciudad = "Huaral"):
    import time
    time.sleep(2)
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

decorador = my_custome_decorator

ejecucion = decorador(Saludo)

saludar = ejecucion("Flavio", 18)
print(saludar)



print("_______________________________________________________________________")
""" PASARLE MÁS ARGUMENTOS AL DECORADOR """

def Calcular_tiempo_ejecucion(name_funcion):
   
    def wrapper(function):
        
        def wrapper_2(*args, **kwargs):
            import time
            # EL wrapper_2 es el que va a ejecutar la función original y hallar su tiempo
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            tiempo_ejecucion = end - start
            print(f"Tiempo de ejecución para la funcipn {name_funcion} es de: {tiempo_ejecucion } segundos")
            return result
        
        return wrapper_2
    
    return wrapper

decorador = Calcular_tiempo_ejecucion("Saludo")
ejecucion = decorador(Saludo)
saludar = ejecucion("Flavio", 18 , "Huaral")
print(saludar)
print("_______________________________________________________________________")

@Calcular_tiempo_ejecucion("Saludo")
def Saludo(name, edad=10, ciudad = "Huaral"):
    import time
    time.sleep(2)
    return f"\nHola Mundo. My name is {name}, I'm {edad} years old, and I live in {ciudad}.\n"

saludo = Saludo("Flavio", 18, "Lima")
print(saludo)

print("_______________________________________________________________________")



