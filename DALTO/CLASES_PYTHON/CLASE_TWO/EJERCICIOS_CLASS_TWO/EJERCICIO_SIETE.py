"""

Escribir un programa que pida al usuario dos números
y muestre por pantalla su división.
Si el divisor es cero el programa debe mostrar un error.

"""



def division(numero_a, numero_b):
    divi = numero_a/numero_b
    divi = round(divi,2)
    divi = f"La división entre {numero_a} / {numero_b} es: {divi}"
    return divi



def numero_A():
# EL WHILE TRUE, SE EJCUTARÁ INDEFINIDAMENTE HASTA LLEGAR A UN BREAK.
    while True:
        
       try:
            # PEDIMOS QUE INGRESEN EL PRIMER VALOR
            numero_1 = float(input("Ingrese el valor a dividir: "))
            # COMPARAMOS, SI ES 0, SE EJCUTARÁ EL IF
            # Y NOS VOLVERÁ A PEDIR INGRESAR EL PRIMER VALOR 
            if(numero_1 == 0):
                print("El número no puede ser 0")
            
            # Y SI EL NÚMERO INGRESADO ES > 0, SE EJCUTARÁ EL BREAK
            # O SEA ACABA EL BUCLE:)
            else:
                break
        # AHORA, SI INGRESAMOS UN CARACTER NO NUMÉRICO, SE EJCUTA EL EXCEPT VALUEERROR
       except ValueError:
             print("Caracter ingresado no valido.")
    return numero_1

numero_1 = numero_A()

def numero_B():
    while True: 
      try: 
            numero_2 = float(input(f"Ingrese el número que va a dividir a {numero_1}: "))
            if(numero_2 == 0):
                print("El número no puede ser 0")
            else: 
                break
      except ValueError:
           print("Caracter no valido")
    return numero_2



numero_2 = numero_B()

print(division(numero_1,numero_2))




"""
La forma que debíamos de hacer: 


while True:
        try:
                numero_1 = float(input("Ingrese el primer número: "))
                if(numero_1 == 0):
                        print("Error, el número no puede ser cero")
                else:
                       break
                
        except ValueError:
               print("Caracter no valido.")

while True:
  try:
        numero_2 = float(input(f"Ingrese el segundo número que va a dividir a  {numero_1}: "))
        if(numero_2 == 0):
        
                print("Error, el número no puede ser cero")
        else:
               break
  except ValueError:
               print("Caracter no valido.")
          


print(division(numero_1,numero_2))     

"""