def Delimitar(funcion):
    def Funcion_Nueva():
        print("Analizando si eres mayor de edad...") 
        while True:
            x = funcion()
            if x in range(18, 131):
                mensaje = f"Eres mayor de edad : {x} años"
                return mensaje
            elif x < 18 and x >= 0:
                mensaje = f"Eres menor de edad : {x} años"
                return mensaje
            else:
                mensaje =  f"Tu edad no es válida, está por debajo o por encima de la edad admitida..."
                print(mensaje)
                continue
    return Funcion_Nueva

@Delimitar
def Pedir_Edad():
    while True:
        try:
            edad = int(input("Ingrese su edad: "))
        except (ValueError, EOFError, KeyboardInterrupt):
            print("\nIngrese su edad correctamente...")
        else:
            print("Edad admitida...")
            return edad
        finally:
            print("Estás ingresando tu edad para verificar si eres mayor de edad o no...")

edad = Pedir_Edad()
print(edad)

