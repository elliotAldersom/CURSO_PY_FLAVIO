""" 
/*
 * EJERCICIO:
 * - Crea ejemplos de funciones básicas que representen las diferentes
 *   posibilidades del lenguaje:
 *   Sin parámetros ni retorno, con uno o varios parámetros, con retorno...
 * - Comprueba si puedes crear funciones dentro de funciones.
 * - Utiliza algún ejemplo de funciones ya creadas en el lenguaje.
 * - Pon a prueba el concepto de variable LOCAL y GLOBAL.
 * - Debes hacer print por consola del resultado de todos los ejemplos.
 *   (y tener en cuenta que cada lenguaje puede poseer más o menos posibilidades)
 *
 * DIFICULTAD EXTRA (opcional):
 * Crea una función que reciba dos parámetros de tipo cadena de texto y retorne un número.
 * - La función imprime todos los números del 1 al 100. Teniendo en cuenta que:
 *   - Si el número es múltiplo de 3, muestra la cadena de texto del primer parámetro.
 *   - Si el número es múltiplo de 5, muestra la cadena de texto del segundo parámetro.
 *   - Si el número es múltiplo de 3 y de 5, muestra las dos cadenas de texto concatenadas.
 *   - La función retorna el número de veces que se ha impreso el número en lugar de los textos.
 *
 * Presta especial atención a la sintaxis que debes utilizar en cada uno de los casos.
 * Cada lenguaje sigue una convenciones que debes de respetar para que el código se entienda.
 */
"""

# Funciones simple:
# 1) Sin parámetros ni retorno
def Saludo():
    print("Hola Mundo")

Saludo()

# 2) Con parámetros y sin retorno
def Saludo_personalizado(name):
    print(f"Hola {name}")
    
Saludo_personalizado("Flavio")

# 3) Con parámetros y con retorno
def Saludo_personalizado_con_retorno(name, last_name):
    return f"Hola {name.capitalize()} {last_name.capitalize()}"

mensaje = Saludo_personalizado_con_retorno(last_name="Silva" , name="flavIO")
print(mensaje)


# RETONO DE VARIOS VALORES:
def Operaciones_matematicas(a, b):
    suma = a + b
    resta = a - b
    multiplicacion = a * b
    division = round(a/b , 2 ) if b != 0 else "No se puede dividir entre cero"
    return suma, resta, multiplicacion, division

num_1 = 10
num_2 = 3
suma, resta, producto , division = Operaciones_matematicas(a= num_1, b= num_2)

print(f"La suma de {num_1} + {num_2} es: {suma}\nLa resta de {num_1} - {num_2} es: {resta}\nEl producto de {num_1} * {num_2} es: {producto}\nLa división de {num_1} / {num_2} es: {division}")

# CON UN NÚMERO INDEFINIDO DE PARÁMETROS:
# Los argumentos se pasan separados por comas
def Varibale_arg_greet(*names):
    for name in names:
        print(f"Hola {name}")
        
Varibale_arg_greet("Flavio", "Silva", "Juan", "Pedro", "Maria")
""" 
Imprime:
Hola Flavio
Hola Silva
Hola Juan
Hola Pedro
Hola Maria
"""


# Con un número variable de parámetros con palabras clave
def Varibale_key_arg_greet(**names):
    for key, value in names.items():
        print(f"Hola {value} ({key})")
    
Varibale_key_arg_greet(name1="Flavio",
 name2="Silva",
name3="Juan", 
name4="Pedro", 
name5="Maria"
)

# FUNCIONES DENTRO DE OTRAS FUNCIONES:
def outer_function():
    def inner_function():
        print("Hola desde la función interna")
    inner_function()
    
outer_function()

# VARIABLE LOCAL Y GLOBAL:
global_var = "Variable Global"
print(global_var)

def hello_python():
    local_var = f"Hello Python - Variable Local"
    return (f"{local_var} - {global_var}")

print(hello_python())


# EXTRA:

def print_numbers(text_1 , text_2)-> int:
    count = 0
    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print(f"El número  {i} es múltiplo de 3 y 5: {text_1} {text_2}")
        elif i % 3 == 0:
            print(f"El número  {i} es múltiplo de 3: {text_1}")
        elif i % 5 == 0:
            print(f"El número  {i} es múltiplo de 5: {text_2}")
        else:
            print(i)
            count += 1
    return count

num = print_numbers("Fizz", "Buzz")
print(f"Números impresos (no múltiplos de 3 o 5): {num}")