# VAMOS A HACR EL CÓDIGO QUE NOS CREARÁ EL ARCHIVO.CSV

""" 
ESTA VERSIÓN TIENE ERRORES EN EL MOMENTO DE PEDIR LOS TIPOS DE DATOS PARA CADA INGRESO....
O SEA TE PIDE UN TIPO DE DATO PERO PARA CADA REGISTRO EN GENERAL, NO ES DINÁMICO....
"""
import pandas as pd 

class ArchivoCSV:
    def __init__(self):
        while True: 
            try:
                print("Bienvenido, acá vamos a crear tu archivo.csv")
                nameArchivo = input("Ingrese el nombre que desea para su archivo.csv: ").strip().title()
                if " " in nameArchivo:
                    print("El nombre del archivo no puede contener espacios, por ello estamos modificándolo")
                    nameArchivo = nameArchivo.replace(" ", "_")
                    print(f"El nombre de su archivo ahora es: {nameArchivo}")
                    
                    
                elif "\n" in nameArchivo:
                    print("El nombre del archivo no puede contener saltos de línea")
                    continue
            except KeyboardInterrupt:
                print("\nPor favor estamos ingrese el nombre de su arhivo...")
            except EOFError:
                print("Por favor estamos ingrese el nombre de su archivo...")
            else:
                print("Nombre válido...")
                print(f"El nombre de su archivo es: {nameArchivo}")
                
                # Pedir confirmación del nombre del archivo:
                while True:
                    try:
                        confirmacio = input("Está seguro de usar este nombre como nombre de su archivo.csv? (Si/No): ").strip().upper()
                        if confirmacio == "SI" or confirmacio == "SÍ" or confirmacio == "S":
                            print(f"Nombre confirmado, el nombre es {nameArchivo}")
                            break
                        elif confirmacio == "NO" or confirmacio == "N":
                            print("Okey, vamos a pedir el nombre nuevamente.")
                            break
                        else:
                            print("Acaba de escoger una opción no válida...")
                            continue
                    except KeyboardInterrupt:
                        print("\nPor favor debe de escoger una de las opciones brindadas...")
                    except EOFError:
                        print("Por favor debe de escoger una de las opciones brindadas...")
                if confirmacio == "SI" or confirmacio == "SÍ" or confirmacio == "S":
                    break
        
        # Pedir números de encabezados (mínimo 1)
        while True:
            try:
                num_Head = int(input("Ingrese el número de encabezados que desea tener: "))
                if num_Head <= 0:
                    print("El número de encabezados no puede ser 0 y menos menor a este, mínimo 1")
                    continue
            except ValueError: 
                print("Debes de ingresar un número de encabezados que deseas tener...")
            except KeyboardInterrupt:
                print("\nPor favor debe de ingresar un número de encabezados...")
            except EOFError:
                print("Por favor debe de ingresar un número de encabezados...")
            else:
                print("Número de encabezados válido...")
                
                
                while True: 
                    try:
                        opcion = input(f"El número de encabezados es: {num_Head}\nEstá seguro de usar ese número de encabezados? (Si/No): ").strip().upper()
                        if opcion == "SÍ" or opcion == "SI" or opcion == "S":
                            print(f"Número de encabezados confimado.\nEl número de encabezados es: {num_Head}")
                            break
                        elif opcion == "NO" or opcion == "N":
                            print("Okey, vamos a pedir el número de encabezads nuevamente...")
                            break
                        else:
                            print("Acaba de escoger una opción no válida...")
                            continue
                    except KeyboardInterrupt:
                        print("\nIngrese una de las opciones...")
                    except EOFError:
                        print("Ingrese una de las opciones...")
                if opcion == "SÍ" or opcion == "SI" or opcion == "S":
                    break
        
        # Pedir nombre de los encabezados:
        encabezados = []
        for i in range(1, num_Head + 1):
            while True:
                try:
                    name_Head = input(f"Ingrese el nombre del {i} encabezado: ").strip().title()
                    if name_Head == "":
                        print("El nombre del encabezado no puede estar vacío...")
                        continue
                    elif "\n" in name_Head:
                        print("El nombre del encabezado no puede tener saltos de línea...") 
                        continue
                    elif name_Head.isnumeric():
                        print("El nombre del encabezado no puede ser solamente un número...")
                        continue
                except KeyboardInterrupt:
                    print("\nPor favor ingrese el nombre del encabezado...")
                except EOFError:
                    print("Por favor ingrese el nombre del encabezado...")
                else:
                    print("Nombre válido...")
                    
                    # Confirmar el nombre del encabezdo
                    while True:
                        try:
                            opcion = input(f"El nombre del {i} encabezado es: {name_Head}\nPero está seguro de usar ese nombre de encabezado? (Si/No): ").strip().upper()
                            if opcion == "SÍ" or opcion == "SI" or opcion == "S":
                                encabezados.append(name_Head)
                                print(f"Ok, confirmarción aceptada, se va a agregar \"{name_Head}\" como nombre del encabezado {i}")
                                break
                            elif opcion == "NO" or opcion == "N":
                                print("Okey, vamos a pedir el nombre del encabezado nuevamente...")
                                break
                            else:
                                print("Escogió algo no válido...")
                                continue
                        except  EOFError:
                            print("Por favor ingrese una opción válida...")
                        except KeyboardInterrupt:
                            print("\nPor favor ingrese una opción válida...")
                    if opcion == "SÍ" or opcion == "SI" or opcion == "S":
                        print("Nombre de encabezado agregado.")
                        print(f"El nombre del encabezdo {i} es: {name_Head}")
                        break
        
        
        # Vamos a pedir los datos de los registros de cada campo 
        # También haremos un ID único para cada registro (autoincrementable)
        registros = []
        id_counter = 1 # Contador del ID 
        
        while True: 
            
            print(f"Aora va a ingresar los datos del usuario cuyo ID es {id_counter}")
            registro_user = [id_counter]
                
            while True:
                    try:
                    
                        tipo_dato = input("Va a ingresar un dato \"numérico (1)\" o \"texto (2)\": ").strip().lower()
                        if tipo_dato == "numérico" or tipo_dato == "numerico" or tipo_dato == "1":
                            print("Entonces va a ingresar el dato de tipo numérico...")
                            for i in encabezados:
                                while True:
                                    try:
                                        value = float(input(f"Ingrese el valor numérico para del campo (columna) {i} cuyo ID único es {id_counter}: "))
                                    except ValueError:
                                        print("Por favor ingrese un valor numérico... (no un caracter)")
                                    except EOFError:
                                        print("Por favor ingrese un valor numérico... (no un caracter)")
                                    except KeyboardInterrupt:
                                        print("\nPor favor ingrese un valor numérico... (no un caracter)")
                                    else:
                                        registro_user.append(value)
                                        print(f"Agregando el valor: {value} para el campo {i} del ID {id_counter}...")
                                        break
                            registros.append(registro_user)
                            break
                        
                        elif tipo_dato == "texto" or tipo_dato == "text" or tipo_dato == "2":
                            print("Entonces va a ingresar el dato de tipo texto...")
                            for i in encabezados:
                                while True:
                                    try:
                                        print("Si llegase a ingresar un número, se considerará como texto y no como número; por eso le dimos las opciones para el tipo de dato...")
                                        value = input(f"Ingrese el valor de texto para del campo (columna) {i} cuyo ID único es {id_counter}: ").strip().lower()
                                        if value  == "":
                                            print("El valor no puede ser vacío")
                                            continue
                                    except KeyboardInterrupt:
                                        print("\nPor favor ingrese un valor de texto....")
                                    except EOFError:
                                        print("\nPor favor ingrese un valor de texto....") 
                                    else:
                                        registro_user.append(value)
                                        print(f"Agregando el valor: {value} para el campo {i} del ID {id_counter}...")
                                        break
                            registros.append(registro_user)
                            break
                        else:
                            print("Por favor ingrese una opción para el tipo de dato --> numérico o texto... (1 o 2)")
                            continue
                    except EOFError:
                        print("\nPor favor ingrese una opción para el tipo de dato --> numérico o texto... (1 o 2)")
                    except KeyboardInterrupt:
                        print("\nPor favor ingrese una opción para el tipo de dato --> numérico o texto... (1 o 2)")
                        
                        
            # PREGUNTAR SI QUIERE INGRESAR OTRO DATO MÁS:
            while True:
                try:
                    seguir = input("Desea ingresar otro tipo de dato o no (SI/NO): ").strip().upper()
                    if seguir == "SI" or seguir == "SÍ" or seguir == "S":
                        id_counter += 1 
                        break
                    elif seguir == "NO" or seguir == "N":
                        print("Finalizando el ingreso de datos...")
                        break
                    else:
                        print("Escoja una de las opciones dadas...")
                        continue
                except KeyboardInterrupt:
                    print("\nPor favor ingrese una opción para seguir o no...")
                except EOFError:
                    print("Por favor ingrese una opción para seguir o no...")
            if seguir == "NO" or seguir == "N":
                break
           
                
        
        
        # AGREGAR LA COLUMNA ID: 
        encabezados.insert(0, "ID")
        
        # Asegurarse de que el nombre del archivo tenga la extensión '.csv'
        if not nameArchivo.endswith(".csv"):
            nameArchivo += ".csv"
        # CREAR EL DataFrame:
        df = pd.DataFrame(registros, columns=encabezados)
        
        # GUARDAR EL ARCHIVO CSV:
        df.to_csv(nameArchivo, index=False, header=True)
        print(f"¡El archivo {nameArchivo} ha sido creado exitosamente!")
        
        # GUARDAR LOS ATRIBUTOS:
        self.nameArchivos = nameArchivo
        self.numHead = num_Head
        self.encabezados = encabezados
        self.registros = registros
        self.id_counter = id_counter


# CREAR LA INSTANCIA:
user = ArchivoCSV()

print(user.nameArchivos)
print(user.numHead)
print(user.encabezados)
print(user.registros)
print(user.id_counter)