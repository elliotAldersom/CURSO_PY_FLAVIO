class Roca:
    def __init__(self, tipo, color, tamaño):
        self.tipo = tipo
        self.color = color
        self.tamaño = tamaño
    
    def moverse(self):
        return f"La piedra de tipo {self.tipo} se está moviendo..."
    

def Pedir_Datos():
    import re
    while True:
        try:
            tipo = input("Ingrese el tipo de la roca: ").strip().capitalize()
            if tipo == "":
                print("Error: El tipo de roca no puede estar vacío.")
                continue
            elif ((re.search(r"\d" , tipo) != None) and (re.search(r"[A-Za-z]", tipo) != None)):
                print("Este tipo de roca tiene números y texto, bueno ese será su nombre supongo...")
                break
            elif not (re.search(r"[A-Za-z]", tipo)):
                print("Error: El tipo de roca debe contener como mínimo un caracter de texto...")
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: El tipo de roca debe ser un texto...")
        else:
            print("Ok, acaba de ingresar el tipo de roca...")
            break
        finally:
            print("Estás colocando el tipo de Roca...")
            
    #______________________________________________________________________________________   
    while True:
        try:
            color = input("Ingrese el color de la roca: ").strip().capitalize()
            if color == "":
                print("Error: El color de la roca no puede estar vacío.")
                continue
            elif ((re.search(r"\d" , color) != None) and (re.search(r"[A-Za-z]", color) != None)):
                print("Este color de roca tiene números y texto, bueno ese será su nombre supongo...")
                break
            elif not(re.search(r"[A-Za-z]", color)):
                print("Error: El color de la roca debe contener como mínimo un caracter de texto...")
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: El color de la roca debe ser un texto...")
        else:
            print("Ok, acaba de ingresar el color de la roca...")
            break
        finally:
            print("Estás colocando el color de Roca...")
            
    #______________________________________________________________________________________ 
    while True:
        try:
            tamaño = input("""Ingrese el tamaño de la roca:\n
1) Grande\n
2) Mediano\n
3) Pequeño\n
Ingrese una de las opciones: """).strip().capitalize()
            if tamaño == "":
                print("Error: El tamaño de la roca no puede estar vacío.")
            elif (tamaño in ["1", "Grande"]):
                tamaño = "Grande"
                print("Ok, escogió el tamaño grande...")
                break
            elif (tamaño in ["2", "Mediano"]):
                tamaño = "Mediano"
                print("Ok, escogió el tamaño mediano...")
                break
            elif (tamaño in ["3", "Pequeño"]):
                tamaño = "Pequeño"
                print("Ok, escogió el tamaño pequeño...")
                break
            else:
                print("Ingrese uno de los tamaños por favor")
        except (ValueError,EOFError,KeyboardInterrupt):
            print("\nError: El tamaño de la roca debe ser uno de los siguientes: Grande, Mediano, Pequeño")
        finally:
            print("Estás colocando el tamaño de Roca...")
    
    return tipo, color, tamaño

tipo,color,tamaño = Pedir_Datos()

roca_One = Roca(tipo, color, tamaño)

valores = (roca_One.__dict__).items()

valor_ordenado = "\n".join(f"{key} : {values}" for  key , values in valores)

print(valor_ordenado)

print(roca_One.tipo)
print(roca_One.color)
print(roca_One.tamaño)
print(roca_One.moverse())