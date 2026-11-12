# VAMOS A HACR EL CÓDIGO QUE NOS CREARÁ EL ARCHIVO.CSV

""" 
LA MEJOR VERSIÓN, NOS PIDE UN TIPO DE DATO PARA CADA CAMPO (COLUMNA)....
"""


class ArchivoCSV:
    def __init__(self):
        import pandas as pd 
        import os
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
        
        
        # DEFIIR TIPO DE DATO POR CADA CAMPO UNA SOLA VEZ:
        tipos_datos_campos =  []
        print("\nAhora ingresará el tipo de dato para cada uno de los datos...")
        for name_campo in encabezados:
            while True:
                try: 
                    tipo = input(f"""
Tienes 2 tipos de de datos disponibles:
1- Numérico
2- Texto

Ingrese por favor el tipo de dato que usará para el campo {name_campo}: """).strip().upper()
                    if tipo == "1" or tipo == "NUMÉRICO" or tipo == "NUMERICO":
                        tipos_datos_campos.append("numérico")
                        break
                    elif tipo == "2" or tipo == "TEXTO" or tipo == "TEXT":
                        tipos_datos_campos.append("texto")
                        break
                    else:
                        print("Opción no válida, por favor ingrese una opción válida...")
                        continue
                except EOFError:
                    print("Por favor ingrese una opción válida...")
                except KeyboardInterrupt:
                    print("\nPor favor ingrese una opción válida...")
        
        
        # Vamos a pedir los datos de los registros de cada campo 
        # También haremos un ID único para cada registro (autoincrementable)
        registros = []
        id_counter = 1 # Contador del ID 
        
        while True: 
            
            print(f"Ahora va a ingresar los datos del usuario cuyo ID es {id_counter}")
            registro_user = [id_counter]
            for name_encabezado , tipo_campo  in  zip(encabezados, tipos_datos_campos):  
                while True:
                    try:
                        if tipo_campo == "numérico":
                            try:
                                value = float(input(f"Ingrese el valor \"numérico\" para el campo {name_encabezado}, cuyo ID único es {id_counter}: "))
                            except ValueError: 
                                print("Debe de ingresar un valor numérico por favor...")
                                continue
                            except KeyboardInterrupt:
                                print("\nPor favor ingrese un valor numérico...")
                                continue
                            except EOFError:
                                print("Por favor ingrese un valor numérico...")
                                continue
                            else:
                                print("Valor válido...")
                                registro_user.append(value)
                                break
                        else: # (Si no es numérico es texto)
                            try:
                                valor = input(f"Ingrese el valor para el campo {name_encabezado}, cuyo ID único es {id_counter}: ").strip().capitalize()
                                if valor == "":
                                    print("El valor no puede estar vacío...")
                                    continue
                            except KeyboardInterrupt:
                                print("\nPor favor ingrese un valor...")
                            except EOFError:
                                print("Por favor ingrese un valor...")
                            else: 
                                print("Valor válido...")
                                registro_user.append(valor)
                                break
                    except KeyboardInterrupt:
                        print("\nPor favor ingrese un valor válido...")
                    except EOFError:
                        print("Por favor ingrese un valor válido...")
            registros.append(registro_user)
                    
                        
                       
                        
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
        #df.to_csv(nameArchivo, index=False, header=True)
        #print(f"¡El archivo {nameArchivo} ha sido creado exitosamente!")
        
        carpeta_destino = "csv_guardados"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        ruta_completa = os.path.join(carpeta_destino, nameArchivo)
        df.to_csv(ruta_completa, index=False, header=True)
        print(f"¡El archivo se guardó exitosamente en {ruta_completa}!") 
        
        
        # GUARDAR LOS ATRIBUTOS:
        self.nameArchivos = nameArchivo
        self.numHead = num_Head
        self.encabezados = encabezados
        self.registros = registros
        self.id_counter = id_counter


# CREAR LA INSTANCIA:

"""
user = ArchivoCSV()

print(user.nameArchivos)
print(user.numHead)
print(user.encabezados)
print(user.registros)
print(user.id_counter)
"""






