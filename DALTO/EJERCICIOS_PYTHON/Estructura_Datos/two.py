""" 
/*
 * EJERCICIO:
 * - Muestra ejemplos de creación de todas las estructuras soportadas por defecto
 *   en tu lenguaje.
 * - Utiliza operaciones de inserción, borrado, actualización y ordenación.
 *
 * DIFICULTAD EXTRA (opcional):
 * Crea una agenda de contactos por terminal.
 * - Debes implementar funcionalidades de búsqueda, inserción, actualización
 *   y eliminación de contactos.
 * - Cada contacto debe tener un nombre y un número de teléfono.
 * - El programa solicita en primer lugar cuál es la operación que se quiere realizar,
 *   y a continuación los datos necesarios para llevarla a cabo.
 * - El programa no puede dejar introducir números de teléfono no numéricos y con más
 *   de 11 dígitos (o el número de dígitos que quieras).
 * - También se debe proponer una operación de finalización del programa.
 */
"""
# Hacerlo por clases:

class Agenda:
    def __init__(self):
        self.__agenda =  {}
    
    @property
    def agenda(self):
        return self.__agenda
    
    @agenda.setter
    def agenda(self, new):
        self.__agenda = new
        


class Contacto(Agenda):
    def agregar_contacto(self , dicci):
        if isinstance(dicci, dict):
            for key , value in dicci.items():
                self.agenda[key] = value
    
    
    def eliminar_contacto(self , key):
        if key in self.agenda:
            del self.agenda[key]
            print("Contacto eliminado con exito")
        else:
            print("No se encontró el contacto..")
    
    def actualizar_contacto(self, key , value, opcion):
        if opcion in ["valor" , "value"]:
            if key in self.agenda:
                self.agenda[key] = value
                print("Contacto actualizado...")
                print(f"\n__________________\n{self.agenda[key]} : {key}\n__________________\n")
            else:
                print("No se encontró el contacto...")
         
        elif opcion in ["clave", "key"]:
            if key in self.agenda:
                new_contac = {value : self.agenda[key] }
                self.eliminar_contacto(key)
                self.agregar_contacto(new_contac)
                print("Contacto actualizado...")
                print(f"\n__________________\n{self.agenda[value]} : {value}\n__________________\n")      
            else:
                print("No se encontró el contacto..")               
    
    
    def __str__(self):
        # Crear un string con los contactos enumerados
        contactos = ""
        for idx, (key, value) in enumerate(self.agenda.items(), start=1):
            contactos += f"{str(idx).zfill(2)}. {value}: {key}\n"  # Usamos `zfill(2)` para asegurar que tenga dos dígitos
        return contactos

    def busqueda(self, valor, opcion):
        # Lista para almacenar todas las concurrencias
        lista = []
        num = 1
        if opcion in  ["nombre", "name"]:
            # Recorrer el diccionario
            for key, value in self.agenda.items():
                if valor == value:
                    lista.append((num, value, key))
                    num +=1
                
            if lista:
                return lista, "\n".join([f"{num}. {name} : {numero}" for num, name , numero in lista])
            else: 
                return f"No se encontraron contactos que coincidan con {valor}"
            
        elif opcion in ["número" , "numero" , "num"]:
             # Recorrer el diccionario
            for key, value in self.agenda.items():
                if valor == key:
                    lista.append((num, value, key))
                    num +=1
                
            if lista:
                return lista, "\n".join([f"{num}. {name} : {numero}" for num , name, numero in lista]) 
            else: 
                return f"No se encontraron contactos que coincidan con {valor}"
    
    def ordenar(self):
        print("Comenzando a ordenar alfabéticamente...")
        ordenar = dict(sorted(self.agenda.items() , key= lambda item: item[1]))
        self.agenda = ordenar
        print("Ya se ordeno su agenda de contactos...")
        return ordenar




#_____________________________________________________________________________________________________________  

def Opcion():
    while True:
        try:
            opcion = input("""Bienvenido a su sistema de agenda de contactos\n¿Qué desea realiar?
1) Agregar contacto
2) Actualizar contacto
3) Borrar contacto
4) Ordenar agenda (alfabeticamente)
5) Buscar contactos
6) Mostrar agenda completa
7) Salir
Ingrese una de las opciones: """).strip().lower()
            if opcion in ["1" , "agregar", "aregar contacto"]:
                return 1
            elif opcion in ["2" , "actualiar" , "actualizar contacto"]:
                return 2 
            elif opcion in ["3" , "borrar" , "borrar contacto"]:
                return 3
            elif opcion in ["4" , "ordenar" , "ordenar agenda"]:
                return 4 
            elif opcion in ["5" , "buscar" , "buscar contacto"]:
                return 5 
            elif opcion in ["6" , "mostrar" , "mostrar agenda completa"]:
                return 6 
            elif opcion in ["7" , "salir" , "exit"]:
                return 7
            else:
                print("Ingrese una de las opciones...")
                continue
        except (ValueError, KeyboardInterrupt, OSError):
            print("\nIngrese una de las opciones válidas...")
            

def Pedir_name():
    import re
    while True:
        try:
            name = input("Ingrese el nombre del contacto: ").strip().title()
            if name == "":
                print("Error: El nombre no puede estar vacío.")
                continue
            elif ((re.search(r"\d" , name) != None) and (re.search(r"[A-Za-z]", name) != None)):
                print("Nombre válido")
                return name
            elif not (re.search(r"[A-Za-z]", name)):
                print("Error: El nombre de contacto debe contener como mínimo un caracter de texto...")
                continue
        except(ValueError,EOFError,KeyboardInterrupt):
            print("\nError: El nombre de contacto debe ser un texto...")
        else:
            print("Ok, acaba de ingresar el nombre de contacto...")
            return name
        finally:
            print("Estás colocando el nombre de contacto...")

def Pedir_num(cls):
    while True: 
        try: 
            num = input("Ingrese el número de telefono del contacto: ").strip()
            busqueda = cls.busqueda(num , "numero")
            if isinstance(busqueda, tuple):
                listado, text = busqueda
                print(f"Error: Este número ya pertence a uno de tus contactos \n{text} . \nVe al apartado de actualizar para cambiarlo")
                continue
            
            elif not(num.isdigit()):
                print("Error: Debe de ingresar un número telefónico..")
                
            elif not (isinstance(busqueda, tuple)):
                if len(num) == 9 :
                    print("Número válido...")
                    return num
                else: 
                    print("Debes de ingresar un número de 9 digitos...")
                    continue
            else:
                print("Ingrese un número de 9 digitos...")
                continue
        except (ValueError, KeyboardInterrupt, EOFError):
           print("\nDebe de ingresar un número de telefono...")
            
            
def Actualziar_contacto(cls):
    while True:
        if not cls.agenda: 
            print("No tiene ningún contacto, valla a agregar contactos para verlos...")
            break
        try:
            print(f"____________________________________________\nSus contactos son: \n{cls}____________________________________________")
            opcion = input("Ingrese el nombre del contacto para buscarlo y editarlo: ").strip().title()
            busqueda = cls.busqueda(opcion, "nombre")
            if isinstance(busqueda, tuple):
                listado , text = busqueda
                while True:
                    try:
                        print(text)
                        indice = int(input("Ingrese el número de orden de su contacto para seleccionarlo: "))
                        numero = ""
                        encontrado = False
                        for idx in listado:
                            if indice == idx[0]:
                                encontrado = True
                                numero = idx[2]
                                formato = f"{idx[0]}. {idx[1]} : {idx[2]}"
                                print(f"Contacto seleccionado: \n{formato}")
                                break
                            
                        while encontrado == True :   
                            try:     
                                opcion_cambio = input("Ingrese \"nombre\" para cambiar el nombre del contacto o \nIngrese \"número\" para cambiar el número del contacto o \"ninguno\" para no hacer nada.\nIngrese su respuesta: ").strip().lower()
                                if opcion_cambio in ["nombre" , "name"]:
                                    new_name = Pedir_name()
                                    cls.actualizar_contacto(numero, new_name, "valor")
                                    break
                        
                                elif opcion_cambio in ["numero" , "número"]:
                                    new_num = Pedir_num(cls)
                                    cls.actualizar_contacto(numero, new_num, "key")
                                    break
                                
                                elif opcion_cambio in ["ninguno", "salir"]:
                                    print("Saliendo del apartado...")
                                    break
                                    
                                else: 
                                    print("Ingrese una opción válida...")
                                    continue
                            except (ValueError, KeyboardInterrupt, EOFError):
                                print("\nIngrese una opción válida...") 
                        break
                    except (ValueError, KeyboardInterrupt, EOFError):
                        print("\nIngrese una opción válida...") 
                break               
            else:
                print("No se encontró el nombre del contacto, vuelva a intentarlo...")
                continue    
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nIngrese una opción válida...")



def Eliminar_contacto(cls):
    while True:
        if not cls.agenda: 
            print("No tiene ningún contacto, valla a agregar contactos para verlos...")
            break
        try:
            print(f"____________________________________________\nSus contactos son: \n{cls}____________________________________________")
            opcion = input("Ingrese el nombre del contacto para buscarlo y eliminarlo: ").strip().title()
            busqueda = cls.busqueda(opcion, "nombre")
            if isinstance(busqueda, tuple):
                listado , text = busqueda
                while True:
                    try:
                        print(text)
                        indice = int(input("Ingrese el número de orden de su contacto para seleccionarlo: "))
                        numero = ""
                        encontrado = False
                        for idx in listado:
                            if indice == idx[0]:
                                encontrado = True
                                numero = idx[2]
                                formato = f"{idx[0]}. {idx[1]} : {idx[2]}"
                                print(f"Contacto seleccionado: \n{formato}")
                                break
                            
                        while encontrado == True :   
                            try:     
                                opcion_cambio = input("Ingrese \"eliminar\" para eliminar el contacto o \nIngrese \"salir\" para no borrarlo.\nIngrese su respuesta: ").strip().lower()
                                if opcion_cambio in ["eliminar" , "borrar"]:
                                    cls.eliminar_contacto(numero)
                                    break 
                                elif opcion_cambio in ["ninguno", "salir", "exit"]:
                                    print("Saliendo del apartado...")
                                    break   
                                else: 
                                    print("Ingrese una opción válida...")
                                    continue
                            except (ValueError, KeyboardInterrupt, EOFError):
                                print("\nIngrese una opción válida...") 
                        break
                    except (ValueError, KeyboardInterrupt, EOFError):
                        print("\nIngrese una opción válida...") 
                break               
            else:
                print("No se encontró el nombre del contacto, vuelva a intentarlo...")
                continue    
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nIngrese una opción válida...")


def Buscar_contacto(cls):
    while True:
        if not cls.agenda: 
            print("No tiene ningún contacto, valla a agregar contactos para verlos...")
            break
        try:
            opcion = input("Ingrese el nombre del contacto para buscarlo y eliminarlo: ").strip().title()
            busqueda = cls.busqueda(opcion, "nombre")
            if isinstance(busqueda, tuple):
                listado , text = busqueda
                print(text)
                break               
            else:
                print("No se encontró el nombre del contacto, vuelva a intentarlo...")
                continue    
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nIngrese una opción válida...")


def Ordenar(cls):
    while True:
        if not cls.agenda: 
            print("No tiene ningún contacto, valla a agregar contactos para ordenarlos...")
            break
        try:
            opcion = input("Seguro de ordenar sus contactos (Se ordenan alfabéticamente) [S/N]: ").strip().lower()
            if opcion in ["s", "si", "sí"]:
                orden = cls.ordenar()
                while True:
                    confirmacion = input("Quiere sobreescribir su antigua agenda por la agenda ordenanda? (No podrá retroceder) [S/N]: ").strip().lower()
                    if confirmacion in ["s", "si", "sí"]:
                        cls.agenda = orden
                        print("Agenda sobreescribida...")
                        print("_______________________________________")
                        print(cls)
                        print("_______________________________________")
                        break
                    elif confirmacion in ["n", "no"]:
                        print("Ok, no se sobreescribe, saliendo del apartado...")
                        break
                    else:
                        print("Ingrese una de las opciones...")
                        continue
                break
            elif opcion in ["n" , "no"]:
                print("Ok, saliendo del apartado...")
                break   
            else:
                print("Ingrese una de las opciones...")
                continue
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nIngrese una opción válida...")


agenda = Contacto()        

while True: 
    opcion = Opcion()
    if opcion == 1:
        name = Pedir_name()
        num = Pedir_num(agenda)
        new_contac = {num : name}
        agenda.agregar_contacto(new_contac)
    
    elif opcion == 2: 
        Actualziar_contacto(agenda)
    
    elif opcion == 3: 
        Eliminar_contacto(agenda)
    
    elif opcion == 4: 
        Ordenar(agenda)
    
    elif opcion == 5: 
        Buscar_contacto(agenda)
    
    elif opcion == 6: 
        print(agenda)
    
    elif opcion == 7: 
        print("saliendo ")
        break