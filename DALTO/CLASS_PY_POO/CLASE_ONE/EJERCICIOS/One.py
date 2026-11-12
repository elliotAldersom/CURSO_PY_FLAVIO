""" 
Crear clase estudiante cuyos atributos sean:
- Nombre
- Edad
- Grado

Con un método llamado (que imprima o sea no retorne nada)
- Estudiar : f"El estudiante {nombre} está estudiando"

Crear una instancia (objeto) Estdiante y usar el método, pero con
intercción con el usuario.
- Se debe pedir el nombre, edad, grado

Si después de registrar la instancia el usuario ingresa la palabra
"estudiar" (ignorando el case) se usará el método Estudiar.
"""
# My version:
class Estudiante:
    
    def __init__(self):
        while True:
            try:
                name = input("Ingrese su primer nombre por favor estimado estudiante: ")
                name = name.strip()
                if not(name.isalpha()):
                    print("Haz ingresado un valor numérico o más de un nombre, recuerda solo es tu primer nombre (TEMAS DE SEGURIDAD).")
                    continue
                elif len(name) <=2:
                    print("El nombre debe tener al menos 3 caracteres")
                    continue
            except KeyboardInterrupt:
                print("\nCaracter inválido")
            except EOFError:
                print("Caracter no válido")
            else:
                print("Nombre registrado con exito")
                name = name.capitalize()
                break
        while True:
            try:
                edad = int(input("Ingrese su edad: "))
                if edad <= 1:
                    print("La edad no puede ser menor a 2")
                    continue
            except ValueError:
                print("Caracter no válido")
            except KeyboardInterrupt:
                print("\nCaracter no válido")
            except EOFError:
                print("Caracter no válido")
            else:
                print("Edad registrada con exito.")
                break
        while True:
            try:
                grado = int(input("Ingrese su ciclo (En números del 1 - 10): "))
                
                match grado :
                    case 0:
                       print("El grado no puede ser 0")
                    case 1 | 3:
                       print("Grado válido")
                       grado = str(grado)
                       grado = f"{grado}ro"
                       print(f"Estás en {grado}")
                       break
                    case 2:
                        print("Grado válido")
                        grado = str(grado)
                        grado = f"{grado}do"
                        print(f"Estás en {grado}")
                        break
                    case 4 | 5 | 6:
                        print("Grado válido")
                        grado = str(grado)
                        grado = f"{grado}to"
                        print(f"Estás en {grado}")
                        break
                    case 7 | 10:
                        print("Grado válido")
                        grado = str(grado)
                        grado = f"{grado}mo"
                        print(f"Estás en {grado}")
                        break
                    case 8:
                        print("Grado válido")
                        grado = str(grado)
                        grado = f"{grado}vo"
                        print(f"Estás en {grado}")
                        break
                    case 9:
                        print("Grado válido")
                        grado = str(grado)
                        grado = f"{grado}no"
                        print(f"Estás en {grado}")
                        break
                    case _:
                        print("El grado que acaba de pasar no está en el rango de 1 a 10")
                        continue
            except ValueError:
                print("Caracter no válido, debe de pasar números del 1 - 10")
            except KeyboardInterrupt:
                print("\nCaracter no válido")
            except EOFError:
                print("Caracter no válido")
        
        self.name = name 
        self.age = edad 
        self.grado = grado
    
    def estudiar(self):
        print(f"El estudiante {self.name} de {self.grado} está estudiando")
    def descansar(self):
        print(f"El estudiante {self.name} de {self.grado} no está estudiando")






def Opcion(user : Estudiante): # Pedimos una intancia de la clase Estudiante
    while True: 
        try:
            opcion = input("Ingrese una de las opciones: Estudiar / Descansar / Salir : ---> ")
            opcion = opcion.strip()
            if not(opcion.isalpha()):
                print(f"{user.name} la opción que escojas no debe de ser numéricas")
                continue
            elif (opcion.lower() == "estudiar"):
                user.estudiar()
            elif (opcion.lower() == "descansar"):
                user.descansar()
            elif (opcion.lower() == "salir"):
                print(f"{user.name}, estás saliendo del programa")
                break
            else:
                print(f"{user.name} la opción que escogiste no es válida")
        except KeyboardInterrupt:
            print("\nCaracter no válida")
        except EOFError:
            print("Caracter no válida")

def Datos_Estudiantes(user : Estudiante):
    print(f""" 
DATOS DEL ESTUDIANTE:
- NOMBRE: {user.name} 
- EDAD: {user.age}
- GRADO DE CICLO: {user.grado}
""")

# COMO LA FUNCIÓN NO RETORNA NADA HACEMOS ASÍ:
userOne = Estudiante()
Datos_Estudiantes(userOne)
Opcion(userOne)  # Llamamos a la función con el objeto userOne
userTwo = Estudiante()
Datos_Estudiantes(userTwo)
Opcion(userTwo)
