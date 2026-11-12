def Menu():
    while True:
        try:
            opcion = input("""Bienvenido al juego, tienes las siguientes opciones:
1) Crear Guerrero
2) Fusionar Guerreros
3) Mostrar Guerreros
4) Editar Guerrero
5) Hacer Pelear a tus Guerreros  
6) Salir

Ingrese una de las opciones (por el número de orden): """).strip().lower()
        
            if opcion in ["1", "crear"]:
                return 1
            elif opcion in ["2", "fusionar"]:
                return 2
            elif opcion in ["3", "Mostrar"]:
                return 3
            elif opcion in ["4", "editar"]:
                return 4
            elif opcion in ["5" , "hacer pelear" , "pelear" , "pelea" , "versus" , "vs"]:
                return 5
            elif opcion in ["6" , "salir" , "exit"]:
                return 6
            else:
                print("Ingrese una de las opciones indicadas...")
                continue
        except (ValueError, EOFError, KeyboardInterrupt):
            print("\nPor favor ingrese una de las opciones indicadas...")

# Crear la clase Guerrero
class Guerrero:
    def __init__(self, name, fuerza, resistencia, velocidad):
        self.__nombre = name
        self.__fuerza = fuerza
        self.__resistencia = resistencia 
        self.__velocidad = velocidad
    
    @property
    def Nombre(self):
        return self.__nombre
    
    @property
    def Fuerza(self):
        return self.__fuerza
    
    @property
    def Resistencia(self):
        return self.__resistencia
    
    @property
    def Velocidad(self):
        return self.__velocidad
    
    @Nombre.setter
    def Nombre(self, new_name):
        self.__nombre = new_name
               
    @Fuerza.setter
    def Fuerza(self, x):
       self.__fuerza = x

    @Resistencia.setter
    def Resistencia(self, x):
       self.__resistencia = x
    
    @Velocidad.setter
    def Velocidad(self, x):
        self.__velocidad = x
    
    def __str__(self):
        return f"{self.__nombre} (Fuerza: {self.__fuerza} , Resistencia: {self.__resistencia} , Velocidad: {self.__velocidad})"
    
    def __add__(self, otro):
        new_name = f"{self.__nombre} - {otro.__nombre}"
        
        lista_guerreros = [self.__nombre , otro.__nombre]

        new_fuerza = ((self.__fuerza + otro.__fuerza)/len(lista_guerreros))**2
        new_fuerza = round(new_fuerza)
        
        new_resistencia = ((self.__resistencia + otro.__resistencia)/len(lista_guerreros))**2
        new_resistencia = round(new_resistencia)
        
        new_velocidad = ((self.__velocidad + otro.__velocidad)/len(lista_guerreros))**2
        new_velocidad = round(new_velocidad)
        
        print("Nuevo Guerrero Listo!!")
        return Guerrero(new_name , new_fuerza , new_resistencia , new_velocidad)
    
    def __repr__(self):
        return f'["{self.__nombre}" , {self.__fuerza} , {self.__resistencia} , {self.__velocidad}]'
    
    def __sub__(self, otro):
        dif_fuerza = self.__fuerza - otro.__fuerza
        dif_resistencia = self.__resistencia - otro.__resistencia
        dif_velocidad = self.__velocidad - otro.__velocidad 
        g1 = []
        g2 = []
        
        # Obtener estadísticas
        dicci = {
        "Fuerza" :  0 ,
        "Resistencia" :0 ,
        "Velocidad" : 0
        }
       
        # Con Fuerza
        if dif_fuerza >= 1:
            g1.append(True)
            g2.append(False)
            dicci["Fuerza"] = self.__nombre
            
        elif dif_fuerza == 0:
            g1.append(False)
            g2.append(False)
            dicci["Fuerza"] = "Empate"
            
        else:
            g1.append(False)
            g2.append(True)
            dicci["Fuerza"] = otro.__nombre
          
        # Con Resistencia  
        if dif_resistencia >= 1:
            g1.append(True)
            g2.append(False)
            dicci["Resistencia"] = self.__nombre
        elif dif_resistencia == 0:
            g1.append(False)
            g2.append(False)
            dicci["Resistencia"] = "Empate"
            
        else:
            g1.append(False)
            g2.append(True)
            dicci["Resistencia"] = otro.__nombre
            
            
        # Con Velocidad
        if dif_velocidad >= 1:
            g1.append(True)
            g2.append(False)
            dicci["Velocidad"] = self.__nombre
            
        elif dif_velocidad == 0:
            g1.append(False)
            g2.append(False)
            dicci["Velocidad"] = "Empate"
            
        else:
            g1.append(False)
            g2.append(True)
            dicci["Velocidad"] = otro.__nombre
        
          
        # Tener Ganador
        if (g1.count(True) == g2.count(True)):
            mensaje = "Es un empate"
        elif (g1.count(True) > g2.count(True)):
            mensaje = f"El ganador de la batalla es {self.__nombre}"
        else:
            mensaje = f"El ganador de la batalla es {otro.__nombre}"
    
        # Mostrar Estadisticas
        estadisticas = " || ".join(f"{key}: {value}" for key,value in dicci.items())
        print(f"Estadisticas de la batalla...")
        return mensaje ,estadisticas
    
    def to_list(self):
        return [self.__nombre , self.__fuerza , self.__resistencia , self.__velocidad]
            

# one = Guerrero("Goku" , 12 , 13 , 14)
# two = Guerrero("vegeta" , 13, 12, 11)

# three = one - two
# mensaje , tabla = three 
# print(f"{tabla}\n{mensaje}")


# PEDIR DATOS
def Pedir_Datos():
    import re
    while True:
        try:
            print("\nBienvenido, ahora ingresará el nombre de su Guerrero...")
            name = input("\nIngrese el nombre de su Guerrero ").strip().title()
            if name == "":
                print("\nError: El nombre de su Guerrero no puede estar vacío.")
                continue
            elif ((re.search(r"\d" , name) != None) and (re.search(r"[A-Za-z]", name) != None)):
                print("\nEl nombre de su Guerrero está compuesto por texto y números, va a ser aceptado...")
                break
            elif not (re.search(r"[A-Za-z]", name)):
                print("\nError: El nombre del Guerrero debe de tener como mínimo un caracter de texto...")
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: El nombre del Guerrero debe ser un texto...")
        else:
            print("\nOk, acaba de ingresar el nombre de su Guerrero")
            break
    
    while True:
        try:
            print("\nAhora ingresará la fuerza de su Guerrero...\nEl cual debe de estar en rango de 1 - 1000")
            fuerza =  int(input("\nIngrese la fuerza de su Guerrero: "))
           
            if (fuerza in range(1 , 1000)):
                print(f"\nEstableciendo el nivel de fuerza...\nNivel de fuerza: {fuerza} unidades") 
                break     
            else:
                print("\nEl nivel de fuerza no se encuentra en el rango establecido...") 
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: La furza del Guerrero debe de ser un número entero")
    
    while True:
        try:
            print("\nAhora ingresará la resistencia de su Guerrero...\nEl cual debe de estar en rango de 1 - 1000")
            resistencia =  int(input("\nIngrese la resistencia de su Guerrero: "))
            
            if (resistencia in range(1 , 1000)):
                print(f"\nEstableciendo el nivel de resistencia...\nNivel de resistencia: {resistencia} unidades") 
                break     
            else:
                print("\nEl nivel de resistencia no se encuentra en el rango establecido...") 
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: La furza del Guerrero debe de ser un número entero")
    
    while True:
        try:
            print("\nAhora ingresará la velocidad de su Guerrero...\nEl cual debe de estar en rango de 1 - 1000")
            velocidad =  int(input("\nIngrese la velocidad de su Guerrero: "))
            
            if (velocidad in range(1 , 1000)):
                print(f"\nEstableciendo el nivel de velocidad...\nNivel de velocidad: {velocidad} unidades") 
                break     
            else:
                print("\nEl nivel de velocidad no se encuentra en el rango establecido...") 
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: La furza del Guerrero debe de ser un número entero")
    
    print(f"\nAcaba de crear a su Guerrero {name}")
    
    return name, fuerza, resistencia, velocidad

# datos = Pedir_Datos()
# name , fuerza , resistencia , velocidad = datos
# guerrero = Guerrero(name , fuerza, resistencia, velocidad )
# print(guerrero)


# Editar Guerrero 
def Editar_Guerrero(guerrero):
    import re
    while True:
        try:
            opcion = input(f"""Que desea modificar de su Guerrero {guerrero.Nombre}:
1) Nombre
2) Fuerza
3) Resistencia
4) Velocidad
5) TODO
6) Salir

Ingrese una de las opciones (numéricas): """).strip().lower()

            # DEFINIR LAS FUNCIONES DE EDICÓN:
            def New_Name():
                while True:
                    try:
                        print(f"Okey, vas a modificar el nombre del Guerrero {guerrero.Nombre}, si no deseas modificarlo ingresa un \"0\"")   
                        new_name = input(f"\nIngrese el nuevo nombre del Guerrero {guerrero.Nombre}: ").strip().title()
                        if new_name == "0":
                            return "Ok, no va a cambiar el nombre de su Guerrero..."
                        elif new_name == "":
                            print("\nError: El nombre de su Guerrero no puede estar vacío.")
                            continue
                        elif ((re.search(r"\d" , new_name) != None) and (re.search(r"[A-Za-z]", new_name) != None)):
                            print("\nEl nombre de su Guerrero está compuesto por texto y números, va a ser aceptado...")
                            while True:
                                try:
                                    confirmation = input(f"\nEstá seguro de cambiar el nombre del Guerrero {guerrero.Nombre} a {new_name}? [S/N]: ").strip().lower()
                                    if confirmation == "":
                                        print("\nDebe de ingresar una de las opciones para continuar...")
                                    elif confirmation in ["no" , "not" , "n"]:
                                        print("\nOkey, aún no se va a modificar el nombre, si no desea modificar el nombre escriba \"0\" o ingrese el nuevo nombre...")
                                        break
                                    elif confirmation in ["yes" , "s" , "sí" , "si"]:
                                        guerrero.Nombre = new_name
                                        return f"\nNombre cambiado con exito, ahora tu guerrero se llama {guerrero.Nombre}"    
                                    else:
                                        print("\nIngrese una de las opciones...")
                                        continue
                                except (ValueError, EOFError, KeyboardInterrupt):
                                    print("\nIngrese una de las opciones por favor...")     
                                            
                        elif not (re.search(r"[A-Za-z]", new_name)):
                            print("\nError: El nombre del Guerrero debe de tener como mínimo un caracter de texto...")
                            continue
                    except(ValueError,EOFError,KeyboardInterrupt):
                        print("\nError: El nombre del Guerrero debe ser un texto...")
                    else:
                        print("\nOk, acaba de ingresar el nuevo nombre de su Guerrero")
                        while True:
                            try:
                                confirmation = input(f"\nEstá seguro de cambiar el nombre del Guerrero {guerrero.Nombre} a {new_name}? [S/N]: ").strip().lower()
                                if confirmation == "":
                                    print("\nDebe de ingresar una de las opciones para continuar...")
                                    continue
                                elif confirmation in ["no" , "not" , "n"]:
                                    print("\nOkey, aún no se va a modificar el nombre, si desea no modificar el nombre escriba \"0\" o ingrese el nuevo nombre...")
                                    break
                                elif confirmation in ["yes" , "s" , "sí" , "si"]:
                                    guerrero.Nombre = new_name
                                    return f"\nNombre cambiado con exito, ahora tu guerrero se llama {guerrero.Nombre}"      
                                else:
                                    print("\nIngrese una de las opciones...")
                                    continue
                            except (ValueError, EOFError, KeyboardInterrupt):
                                print("\nIngrese una de las opciones por favor...") 
                
                
            def New_Fuerza():
                while True:
                    try:
                        print(f"\nAhora ingresará la nueva fuerza de su Guerrero {guerrero.Nombre}\nEl cual debe de estar en rango de 1 - 1000")
                        print(f"Fuerza actual: {guerrero.Fuerza}")
                        new_fuerza =  int(input("\nIngrese la nueva fuerza de su Guerrero: "))
                            
                        if new_fuerza == 0:
                            return "Ok, no va a cambiar la fuerza de su Guerrero..."
                        elif (new_fuerza in range(1 , 1000)):
                            print(f"\nOk, vamos a pedir que confirmes su nueva fuerza...")
                            while True:
                                try:
                                    confirmation = input(f"\nEstá seguro de cambiar la fuerza del Guerrero {guerrero.Nombre} : {guerrero.Fuerza} a {new_fuerza}? [S/N]: ").strip().lower()
                                    if confirmation == "":
                                        print("\nDebe de ingresar una de las opciones para continuar...")
                                        continue
                                    elif confirmation in ["no" , "not" , "n"]:
                                        print("\nOkey, aún no se va a modificar la fuerza de su Guerrero, si no desea modificar su fuerza escriba \"0\" o ingrese la nueva fuerza...")
                                        break
                                    elif confirmation in ["yes" , "s" , "sí" , "si"]:
                                        guerrero.Fuerza = new_fuerza
                                        return f"\nFuerza cambiado con exito, ahora la fuerza de su guerrero {guerrero.Nombre} es {guerrero.Fuerza}"
                                    else:
                                        print("\nIngrese una de las opciones...")
                                        continue
                                except (ValueError, EOFError, KeyboardInterrupt):
                                    print("\nIngrese una de las opciones por favor...")
                            break   
                        else:
                            print("\nEl nivel de fuerza no se encuentra en el rango establecido...") 
                            continue
                    except(ValueError,EOFError,KeyboardInterrupt):
                        print("\nError: La furza del Guerrero debe de ser un número entero")
                            
            
            def New_Resistencia():
                while True:
                    try:
                        print(f"\nAhora ingresará la nueva resistencia de su Guerrero {guerrero.Nombre}\nEl cual debe de estar en rango de 1 - 1000")
                        print(f"Resistencia actual: {guerrero.Resistencia}")
                        new_resistencia =  int(input("\nIngrese la nueva resistencia de su Guerrero: "))

                        if new_resistencia == 0:
                            return "Ok, no va a cambiar la resistencia de su Guerrero..."
                        elif (new_resistencia in range(1 , 1000)):
                            print(f"\nOk, vamos a pedir que confirmes su nueva resistencia...")
                            while True:
                                try:
                                    confirmation = input(f"\nEstá seguro de cambiar la resistencia del Guerrero {guerrero.Nombre} : {guerrero.Resistencia} a {new_resistencia}? [S/N]: ").strip().lower()
                                    if confirmation == "":
                                        print("\nDebe de ingresar una de las opciones para continuar...")
                                        continue
                                    elif confirmation in ["no" , "not" , "n"]:
                                        print("\nOkey, aún no se va a modificar la resistencia de su Guerrero, si no desea modificar su fuerza escriba \"0\" o ingrese la nueva fuerza...")
                                        break
                                    elif confirmation in ["yes" , "s" , "sí" , "si"]:
                                        guerrero.Resistencia = new_resistencia
                                        return f"\nResistencia cambiado con exito, ahora la resistencia de su guerrero {guerrero.Nombre} es {guerrero.Resistencia}"
                                    else:
                                        print("\nIngrese una de las opciones...")
                                        continue
                                except (ValueError, EOFError, KeyboardInterrupt):
                                    print("\nIngrese una de las opciones por favor...")
                            break   
                        else:
                            print("\nEl nivel de resistencia no se encuentra en el rango establecido...") 
                            continue
                    except(ValueError,EOFError,KeyboardInterrupt):
                        print("\nError: La resistencia del Guerrero debe de ser un número entero")
            
            
            def New_Velocidad():
                while True:
                    try:
                        print(f"\nAhora ingresará la nueva velocidad de su Guerrero {guerrero.Nombre}\nEl cual debe de estar en rango de 1 - 1000")
                        print(f"Velocidad actual: {guerrero.Velocidad}")
                        new_velocidad =  int(input("\nIngrese la nueva velocidad de su Guerrero: "))

                        if new_velocidad == 0:
                            return "Ok, no va a cambiar la velocidad de su Guerrero..."
                        elif (new_velocidad in range(1 , 1000)):
                            print(f"\nOk, vamos a pedir que confirmes su nueva velocidad...")
                            while True:
                                try:
                                    confirmation = input(f"\nEstá seguro de cambiar la velocidad del Guerrero {guerrero.Nombre} : {guerrero.Resistencia} a {new_velocidad}? [S/N]: ").strip().lower()
                                    if confirmation == "":
                                        print("\nDebe de ingresar una de las opciones para continuar...")
                                        continue
                                    elif confirmation in ["no" , "not" , "n"]:
                                        print("\nOkey, aún no se va a modificar la velocidad de su Guerrero, si no desea modificar su velocidad escriba \"0\" o ingrese la nueva fuerza...")
                                        break
                                    elif confirmation in ["yes" , "s" , "sí" , "si"]:
                                        guerrero.Velocidad = new_velocidad
                                        return f"\nVelocidad cambiado con exito, ahora la velocidad de su guerrero {guerrero.Nombre} es {guerrero.Velocidad}"
                                    else:
                                        print("\nIngrese una de las opciones...")
                                        continue
                                except (ValueError, EOFError, KeyboardInterrupt):
                                    print("\nIngrese una de las opciones por favor...")
                            break   
                        else:
                            print("\nEl nivel de velocidad no se encuentra en el rango establecido...") 
                            continue
                    except(ValueError,EOFError,KeyboardInterrupt):
                        print("\nError: La velocidad del Guerrero debe de ser un número entero")
            
            # Entrar a las condicionales
            if (opcion in ["1" , "nombre" , "name"]):
                print(New_Name())                   
            elif opcion in ["2" , "fuerza"]:  
                print(New_Fuerza())
            elif opcion in ["3" , "resistencia"]: 
                print(New_Resistencia())
            elif opcion in ["4" , "velocidad"]: 
                print(New_Velocidad())
            elif opcion in ["5" , "todo"]:
                print(New_Name())
                print(New_Fuerza())
                print(New_Resistencia())
                print(New_Velocidad())
            elif opcion in ["6" , "salir", "exit"]:
                print("\nSaliendo del apartado de edición...")
                break
            else: 
                print("\nIngese una de las opciones dadas...")
        except (ValueError, EOFError, KeyboardInterrupt):
            print("\nPor favor ingrese una de las opciones dadas...")
            



# Armar todo:
lista_guerrero = []

while True:
    opcion = Menu()
    if opcion == 1:
        data = Pedir_Datos()
        name , fuerza , resistencia , velocidad = data 
        guerrero = Guerrero(name , fuerza , resistencia , velocidad)
        print(f"\nGuerrero creado:\n{guerrero}")
        
        lista_guerrero.append(guerrero) # Guardamos el objeto completo
        #print(lista_guerrero)
    elif opcion == 2:
        num = len(lista_guerrero)
        if num < 2 :
            print("\nNúmero de Guerreros insuficiente para esta acción...\nCree más Guerreros!!!")
        else:
            
            while True:
                try:
                    # Mostrar guerreros con índice:
                    for id , g in  enumerate(lista_guerrero,1):
                        print(f"{id}) {g.to_list()}")
                    index1 = int(input("\nIngrese el ID del primer Guerrero que desea fusionar: "))-1
                    if (lista_guerrero[index1]) and (index1 in range(num)):
                        g1 = lista_guerrero[index1]
                        print(f"\nGuerrero seleccionado correctamente {g1.Nombre}")
                        while True:
                            try:
                                index2 = int(input(f"\nIngrese el ID del segundo Guerrero para fusionarlo con {g1.Nombre}: "))-1
                                if (index2 != index1) and (lista_guerrero[index2]) and (index2 in range(num)):
                                    g2 = lista_guerrero[index2]
                                    print(f"\nGuerreros seleccionados para la fusión: {g1.Nombre} || {g2.Nombre}")
                                    print("FUSIONANDO...")
                                    g3 = g1 + g2
                                    lista_guerrero.append(g3)
                                    print(f"Nuevo Guerrero!!\n{g3}")
                                    break
                                elif index1 == index2 :
                                    print("Ya seleccionaste a este Guerrero anteriormente...")
                                    continue
                                else:
                                    print("No se enceuntra el Guerrero seleccionado...")
                                    continue
                            except (ValueError, EOFError, KeyboardInterrupt, IndexError):
                                print("Ingrese un ID válido...")
                        break
                            
                    else:
                        print("Ingrese un ID válido para seleccionar a su Guerrero...")
                        continue
                except (ValueError, EOFError, KeyboardInterrupt, IndexError):
                    print("Ingrese un ID válido...")
    
    elif opcion == 3:
        import random
        num = len(lista_guerrero)
        if num < 1:
            print("No tiene Guerreros suficientes para reaizar esta acción...")
        elif num == 1 : 
            print("Mostrando a su único Gureero")
            for id , g in enumerate(lista_guerrero, 1):
                print(f"{id}) {g}")            
        else:
            while True:
                try:
                    elegir = input("Tiene dos formas de elegir como desea ver a sus guerreros:\n1) Todos juntos \n2) Uno solo pero al azar\nIngrese su opción (numérica): ").strip().lower()
                    if elegir in ["1" , "todos juntos" , "juntos"]:
                        print("\nVamos a mostrar todos sus personajes...")
                        for id , g in enumerate(lista_guerrero , 1):
                            print(f"{id}) {g}")
                            
                        else:
                            print("\nEsos son todos sus guerreros...") 
                            break 
                    elif elegir in ["2" , "uno" , "uno solo" , "al azar" , "azar" , "uno solo pero al azar"]:
                        id_azar = random.randrange(num)
                        guerrero_escogido = lista_guerrero[id_azar]
                        print(f"\nEste es el Guerrero escogido al azar:\n{guerrero_escogido}")
                        break
                    else:
                        print("\nIngrese una de las opciones dadas...")
                        continue
                except (IndexError, KeyboardInterrupt, ValueError, EOFError):
                    print("\nDebe de ingresar una de las opciones dadas...")
            
    elif opcion == 4:
        if len(lista_guerrero) < 1:
            print("Número de Guerreros insuficinte para esta acción...")
        else:
            while True:
                try:
                    num = len(lista_guerrero)
                    print("Estos son todos sus Guerreros para la edicón...")
                    for id, g in enumerate(lista_guerrero,1):
                        print(f"{id}) {g}")
                    pedir_guerrero = int(input("Ingrese el ID de su Guerrero: "))-1
                    
                    if (lista_guerrero[pedir_guerrero]) and (pedir_guerrero in range(num)):
                        objeto = lista_guerrero[pedir_guerrero]
                        editado = Editar_Guerrero(objeto)
                        print(editado)
                        break
                except (IndexError, KeyboardInterrupt, ValueError, EOFError):
                    print("\nDebe de ingresar una de las opciones dadas...")
    
    elif opcion == 5:
        num = len(lista_guerrero)
        if num < 2 :
            print("\nNúmero de Guerreros insuficiente para esta acción...\nCree más Guerreros!!!")
        else:
            
            while True:
                try:
                    # Mostrar guerreros con índice:
                    for id , g in  enumerate(lista_guerrero,1):
                        print(f"{id}) {g.Nombre}")
                    index1 = int(input("\nIngrese el ID del primer Guerrero para hacer el V/S: "))-1
                    if (lista_guerrero[index1]) and (index1 in range(num)):
                        g1 = lista_guerrero[index1]
                        print(f"\nGuerrero seleccionado correctamente {g1.Nombre}")
                        while True:
                            try:
                                index2 = int(input(f"\nIngrese el ID del segundo Guerrero para que se enfrente con {g1.Nombre}: "))-1
                                if (index2 != index1) and (lista_guerrero[index2]) and (index2 in range(num)):
                                    g2 = lista_guerrero[index2]
                                    print(f"\nGuerreros seleccionados para la batall: {g1.Nombre} || {g2.Nombre}")
                                    print("Batallando...")
                                    result = g1 - g2 
                                    mensaje , tabla = result
                                    print(f"{tabla}\n{mensaje}")
                                    break
                                elif index1 == index2 :
                                    print("Ya seleccionaste a este Guerrero anteriormente...")
                                    continue
                                else:
                                    print("No se enceuntra el Guerrero seleccionado...")
                                    continue
                            except (ValueError, EOFError, KeyboardInterrupt, IndexError):
                                print("Ingrese un ID válido...")
                        break
                            
                    else:
                        print("Ingrese un ID válido para seleccionar a su Guerrero...")
                        continue
                except (ValueError, EOFError, KeyboardInterrupt, IndexError):
                    print("Ingrese un ID válido...")
    
    elif opcion == 6 :
        print("\nSaliendo del juego...")
        break
