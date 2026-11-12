print("📐 Vamos a realizar una divisón:")

def division():
    
    while True:
        try:
            num_1 = float(input("Ingrese el primer número: "))
            print("Número valido")
            break
        except ValueError:
            print("Haz ingresado un caracter no válido")
        except ZeroDivisionError:
            print("Error, no puedes usar el 0 como dividendo.")
    
    while True:
        try:
            num_2 = int(input(f"Ingrese el número que va a dividir a {num_1} : "))
            print("Número valido")
            break
        except ValueError:
            print("Haz ingresado un caracter no válido")
        except ZeroDivisionError:
            print("Error, no puedes usar el 0 como divisor.")
    return num_1 / num_2

#resultado = division()
#print(f"La división es {resultado}")

""" 
Esta es mi primera versión de la división, la cual está mal,
ya que el ZeroDivisionError solo se evalua al realizar la division,
o sea debemos de usarlo para el divisor y no dividendo.
"""

def division():
    
    while True:
        try:
            num_1 = float(input("Ingrese el primer número: "))
            if num_1 == 0 :
                print("No puedes usar 0 como dividendo.")
                continue # Vuelve a pedir el número sin continuar el resto del código
            print("Número valido")
            
        
        except KeyboardInterrupt : # Para atrapar exceptcions como Ctrl+C 
            print("\nHaz ingresado un caracter no válido")
        except ValueError : # Para atrapar exceptciones de tipo ValueError
            print("Haz ingresado un caracter no válido")
        else:
            break
        
       
    
    while True:
        try:
            num_2 = float(input(f"Ingrese el número que va a dividir a {num_1} : "))
            
            if (num_2 == 0):
                raise ZeroDivisionError # Si el divisor es 0, lanzo la excepción
                # Acá no es necesario poner el continue
            print("Número valido")
            
       
        except ValueError:
            print("Haz ingresado un caracter no válido")
        except ZeroDivisionError:
            print("Error, no puedes usar el 0 como divisor.")
        except KeyboardInterrupt:
            print("\nHaz ingresado un caracter no válido")
        else:
            break
    
    return num_1 / num_2

resultado = division()
print(f"La división es {resultado}")

""" 
Esta es una forma óptima, manejamos correctamente los errores posibles como 
si ingresan 0 como dividendo o divisor, y también manejamos el caso de que el usuario
ingrese el Control + C o ingrese algo no numérico

- El: KeyboardInterrupt (Maneja en este caso e Control + C)
- El: ValueError (Maneja en este caso e ingreso de algo no numérico)
- El: ZeroDivisionError (Maneja en este caso e ingreso de 0 como dividendo o divisor)

- El raise en el segundo while es para lanzar la excepción de división por cero,
El raise:
El raise te permite lanzar (o generar) una excepción de manera manual. 
En lugar de esperar a que el programa encuentre un error por sí mismo, 
puedes usar raise para detener la ejecución y señalar un problema cuando se 
cumpla una condición específica que tú determines.

Usamos raise para manejar situaciones donde, por ejemplo, 
queremos asegurar que una entrada del usuario sea válida o que se cumpla una condición 
antes de continuar la ejecución del programa.

"""

# EJM BÁSICO DE UN FACTORIAL
num = int(input("Ingrese el factorial de qe número quiere hallar: "))
# La vaiable a se inicializa afuera del bucle, sino no funcionaría
a = 1
for i in range(1,(num + 1)):
    # De esta forma el valor se almacena
    a *=i

print(f"El facorial de {num} es: {a}")