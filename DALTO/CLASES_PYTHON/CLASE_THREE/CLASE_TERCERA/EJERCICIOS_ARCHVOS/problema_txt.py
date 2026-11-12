""" 
Tenemos 2 listas con nombre y apellido,
es decir, una tiene nombre y otra apellido,
tenemos que escribir los datos de un archivo de texto
de forma óptima con un for
"""

def Num_Lista():
    while True:
        try:
            num =int(input("Cuantos datos deseas ingresar: "))
            if(num <= 0):
                print("Debes ingresar un número mayor a 0")
            else:
                print("Número valido ")
                return num
        except ValueError:
            print("Caracter ingresado no valido, intenta de nuevo ")



def Lista_Name(number):
    
    listado = []
    i = 0
    while(i < number):
        elemento = input(f"Ingrese el elemento {(i +1)}: ")
        while(elemento == ""):
            print("No puedes ingresar un elemento vacío.")
            # Lo volvemos a pedir porque sino solo se ejecuta una vez 
            elemento = input(f"Ingrese el elemento {(i +1)}: ")
        while((((elemento.strip()).replace(" ", ""))).isnumeric()):
            print("No puedes ingresar un número, porqué es una lista de texto.")
            elemento = input(f"Ingrese el elemento {(i +1)}: ")
        
        listado.append((elemento.strip().capitalize()))
        print("Elmento ingresado correctamente")
        i += 1
        
    return listado

# Esta función es por si queremos usar edad también:
def Lista_Age(number):
    
    listado = []
    i = 0
    while(i < number):
        while True:
            try:
                elemento = int(input(f"Ingrese el elemento {(i +1)}: "))
                if(elemento <= 0):
                    print("No puedes ingresar un número menor a 0")
                else:
                    listado.append(elemento)
                    print("Elmento ingresado correctamente")
                    break
            except ValueError:
                print("Caracter ingresado no valido, intenta de nuevo ")
        i += 1
        
    return listado
print("Usaremos para todas tus listas la misma cantidad de elementos")

num = Num_Lista()
print("Ahora haremos tu lista de nombres")
lista_nombres = Lista_Name(num)

print("\nAhora haremos tu lista de apellidos")
lista_apellidos = Lista_Name(num)


print("\nAhora haremo tu lista de edades")
lista_edades = Lista_Age(num)

#print(lista_nombres)
#print(lista_apellidos)
#print(lista_edades)



with open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\EJERCICIOS_ARCHVOS\\nombre_apellido_edad.txt", "a" , encoding="UTF-8") as archivo :
   # AMBOS ITERAN IGUAL: 
    archivo.write("Los datos son:\n")
   # 1)
    for name, lastName , age in zip(lista_nombres, lista_apellidos, lista_edades):
        archivo.writelines(f"Nombre: {name}\nApellido: {lastName}\nEdad: {age}\n----------\n")
    
    # 2)
    for i in range(num):
        archivo.write(f"Nombre: {lista_nombres[i]}\nApellido: {lista_apellidos[i]}\nEdad: {lista_edades[i]}\n----------\n")

    # 3)
    for name, lastName , age in zip(lista_nombres, lista_apellidos, lista_edades):
        archivo.writelines(f"{name}  {lastName}  {age}\n----------\n")

print("El proceso acabó exitosamente")