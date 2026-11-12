def Division(numero_a, numero_b):
    divi = numero_a/numero_b
    divi = round(divi,2)
    divi = f"La división entre {numero_a} / {numero_b} es: {divi}"
    return divi


def primer_valor():
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

numero_A = primer_valor()

def segundo_valor():
    while True: 
      try: 
            numero_2 = float(input(f"Ingrese el número que va a dividir a {numero_A}: "))
            if(numero_2 == 0):
                print("El número no puede ser 0")
            else: 
                break
      except ValueError:
           print("Caracter no valido")
    return numero_2



