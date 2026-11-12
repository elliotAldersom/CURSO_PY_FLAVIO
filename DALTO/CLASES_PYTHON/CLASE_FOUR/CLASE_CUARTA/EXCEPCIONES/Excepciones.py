""" 
Antes de entender que es una excepción
hay que entender que es un evento.
Un evento es cualquier cosa que ocurre en nuestro programa
eso normalmente nos envía una notificación para poder actuar en consecuencia,
es decir, hacer clic, mover el mouse, teclear y/o soltar cualquier letra,
cualquier cosa suceso dentro de un programa es un evento

Tipos de Eventos:
1. Eventeos del usuario:
Hacer clic en un botón (evento de clic).
Presionar una tecla (evento de teclado).
Mover el ratón (evento de mouse). 
(Cosas que ya acabo de decir).

2. Eventos del sistema:
La llegada de datos a una red (evento de red).
Cambios en el estado de un archivo (evento de archivo).
Se cumple un temporizador (evento de temporizador).

- En los lenguajes de programación, lo que hacemos es capturar estos eventos
para actuar en consecuencia a ellos.

Ahora las Excepciones, por otro lado también son eventos, 
eventos que ocurren durante la ejecución de nuestro programa,
pero este evento lo que hace es interrumpir el flujo normál de ejecución,
es decir, es algo que hace que se detenga toda acción en el programa,
EJM: Tenemos 10 instrucciones, y la instrucción 5 lanza una excepción,
esto hace que se detenga todo el programa.
El objetivo acá es saber actuar en consecuencia cuando hay una excepción, o sea 
saber manejarla, para que el programa no se detenga y siga ejecutándose.
"""

# Vamos a generar una excepción acá.
def suma():
    num_1 = input("Ingrese el primer número: ")
    num_2 = input("Ingrese el segundo número: ")
    return int(num_1) + int(num_2)


"""  
Al ingresar un String y luego se suma como int(num_1) + int(num_2)
nos lanza este error: de tipo --> ValueError

ValueError: invalid literal for int() with base 10: 'String que le pasamos y es una excepción'

- Ahora para solucionarlo, debemos de usar la sentencia:
try: 
    código que se va a intentar y va a evaluar si hay una excepción
except:
    código que se va a ejecutar si hay una excepción
    Mayormente uso un mensaje como 
    print("Caracter invalido, hazlo otra vez")

Tenemos varios tipos de excepciones, y no vamos a estar poniendo uno para cada tipo
así que vamos a poner el general, el que capture todos los que vea y este es:
except: (esto captura todos las excepciones en general)
except Exception: (esto captura todas las excepciones de tipo Exception y de sus subclases )

"""
# Vamos a modificar la función para que maneje las excepciones:
def suma():
    # Entramos al primer bucle, que se encarga del primer número
    while True:
        try:
            # Vamos a corregir primero al primer ingreso
            num_1 = int(input("Ingrese el primer número: "))
            # Si no hay excepción, pasamos a la siguiente instrucción
            # Que en este caso es un break, que corta con el bucle
            break
        except:
            # Si hay una excepción, pasamos a esto
            print("Caracter invalido, hazlo otra vez")
    
    # Entramos al segundo bucle, que se encarga del segundo número
    while True:
        try:
            # Vamos a corregir ahora al segundo ingreso
            num_2 = int(input(f"Ingrese el segundo número, el cual va a sumar a {num_1}: "))
            # Si no hay excepción, pasamos a la siguiente instrucción
            # Que en este caso es un break, que corta con el bucle
            break
        except:
            # Si hay una excepción, pasamos a esto
            print("Caracter invalido, hazlo otra vez")
    # Después de cerrar todos los bucles, retornamos la suma:
    resultado = num_1 + num_2
    return resultado

print(f"La suma es: {suma()}")

"""
Vamos a ver otra forma de hacerlo
- La diferencia es que este me corrige después de ingresar os dos números,
- No me gusta, porque no es como que me diga en que me equivoqué,
- Prefiero que corrija al momento de ingresae el número
"""

def adicion():
    while True:
        num_1 = input("Ingrese el primer número: ")
        num_2 = input("Ingrese el segundo número: ")
        try:
            resultado = int(num_1) + int(num_2)
            break
        except:
            print("Caracter invalido, debe de ser numérico, hazlo otra vez")
    return resultado

print(f"La suma es: {adicion()}")

""" 
Esto es incorrecto:

def adicion():
    while True:
        num_1 = input("Ingrese el primer número: ")
        num_2 = input("Ingrese el segundo número: ")
        try:
            resultado = int(num_1) + int(num_2)
            return resultado --> ESTO ESTÁ MAL
        except:
            print("Caracter invalido, debe de ser numérico, hazlo otra vez")

Está mal. pues jmaás llega al except, pues de frente nos vamos al return
jamás evaluamos si el número es correcto, por eso está mal,por ello
debemos de poner el break y fuera del while el return.
"""
#___________________________________________________________________
print("VAMOS A VER LAS FORMAS DE REOSLVER UNA EXCEPCIÓN CON BUENAS PRÁCTICAS.")
""" 
Estas dos formas que vamos a ver son más óptimas y correctas
son buenas prácticas a comparación de las anteriores versiones:
Así como usamos el else en For, lo podemos usar en el While,
esto es así:
Si no se ejecuta el except, se ejecuta el else
Si no se ejecuta el else, se eejcuta el except

Algo más: Estamos agregando el finally a cada uno,
esto no lo hace más óptimo que los demás, sino que es para tener el conocimiento
de que finally se ejecuta sin importar si se ejecuta el except o el else,
siempre se ejecuta.
No es necesario usarlo, pero si gustas hazlo.
"""

def adicion():
    while True:
        num_1 = input("Ingrese el primer número: ")
        num_2 = input("Ingrese el segundo número: ")
        try:
            resultado = int(num_1) + int(num_2)
            
        except Exception as e:
            print("Caracter invalido, debe de ser numérico, hazlo otra vez")
            print(f"Error: {e}")
        else:
            break
        finally:
            # Podemos meterle un mensaje sin importar que se ejecute
            print("Esto se ejecuta siempre, sin importar si se ejecuta el except o else")
    return resultado

print(f"La suma es: {adicion()}")

def suma():
    # Entramos al primer bucle, que se encarga del primer número
    while True:
        try:
            # Vamos a corregir primero al primer ingreso
            num_1 = int(input("Ingrese el primer número: "))
           
        except Exception as e:
            # Si hay una excepción, pasamos a esto
            print("Caracter invalido, hazlo otra vez")
            print(f"Error: {type(e).__name__}") # Nos dice el nombre del error
        else:
            # Si no hay excepción, pasamos a la siguiente instrucción
            # Que en este caso es un break, que corta con el bucle
            break
        finally:
            # Podemos meterle un mensaje sin importar que se ejecute
            print("Esto se ejecuta siempre, sin importar si se ejecuta el except o else")
    
    # Entramos al segundo bucle, que se encarga del segundo número
    while True:
        try:
            # Vamos a corregir ahora al segundo ingreso
            num_2 = int(input(f"Ingrese el segundo número, el cual va a sumar a {num_1}: "))
          
        except Exception as e:
            # Si hay una excepción, pasamos a esto
            print("Caracter invalido, hazlo otra vez")
            print(f"Error: {type(e).__name__}") # Nos dice el nombre del error
        else:
            # Si no hay excepción, pasamos a la siguiente instrucción
            # Que en este caso es un break, que corta con el bucle
            break
        finally:
            # Podemos meterle un mensaje que queramos imprimir sin importar que ocurrar
            print("Esto se ejecuta siempre, sin importar si se ejecuta el except o else")

    # Después de cerrar todos los bucles, retornamos la suma:
    resultado = num_1 + num_2
    return resultado

print(f"Ahora la suma es: {suma()}")


""" 
Algunos tipos de excepciones son:

try:
    num = int(input("Ingrese un número: "))

except ValueError:
    print("¡Eso no es un número válido!")

except ZeroDivisionError:
    print("No puedes dividir entre cero.")

except OverflowError:
    # Si el número es demasiado grande para manejarlo
    print("¡Número demasiado grande!")
    
except ArithmeticError:
    # Si ocurre un error aritmético general (ej. operaciones matemáticas con valores no válidos)
    print("Error aritmético, revisa tus operaciones.")

except Exception as e: # --> Captura la excepcion y lo guarda en una variable (e)
    print(f"Ocurrió un error inesperado: {e}")

EJEMPLOS DEL: except

1) 
    try:
        num = -9
            # Intentamos calcular la raíz cuadrada
        mensaje = (num ** 0.5)  # Esto puede generar un error si el número es negativo
        print(mensaje)
    except ValueError:  # Aquí capturamos un ValueError si intentamos calcular la raíz cuadrada de un número negativo
        print("Error aritmético, no se puede calcular la raíz cuadrada de un número negativo.")



"""