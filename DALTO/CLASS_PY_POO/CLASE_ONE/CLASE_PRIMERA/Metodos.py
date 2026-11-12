""" 
Ya hemos visto que es una propiedad (atributos o características del objeto),
un objeto es una instancia de una clase, ahora los métodos son las acciones que 
puede realizar el objeto.
EJM:
- Correr
- Caminar
- Sentarse
- Hablar
- Comer
ETC...

- Ahora en estructura, un método es una función que se encuentra dentro de una clase.

- ESTA ES LA FUNCIÓN: (Es solo un ejemplo, ya que hacer un nombre no es una acción de un celular, sino más bien un atributo)
def funcion_name():
    while True:
        try:
            name= input("Ingrese su nombre: ")
            name = name.strip()
            #if isinstance(name,int) or isinstance(name,float): --# EN ESTE CASO NO AYUDA (YA QUE PASAMOS STR)
            if name.isnumeric():
                print("Error, el nombre no puede ser un número")
                continue
            elif len(name)<=4:
                print("Error, el nombre debe tener al menos 5 caracteres")
                continue
        except KeyboardInterrupt:
            print("\nCaracter no válido.")
        except EOFError:
            print("Caracter no válido")
        else: 
            name = name.title()
            return f"Hola {name}"
print(funcion_name())
"""
class CellPhone:
    # MÉTODO ESPECIAL (CONSTRUCTOR)
    def __init__(self, marca, modelo, camara ="80MP"):
        print("\nVirtual Store VIP")
        self.marca = marca 
        self.modelo = modelo
        self.camara = camara
    
        
    # ESTE SI ES UN MÉTODO DE LA CLASE CellPhone, ES UNA FUNCIÓN PERO ES UN MÉTODO
    # TODA FUNCIÓN DENTRO DE UNA CLASE ES UN MÉTODO DE ESA MISMA CLASE
    # PERO LE PONEMOS EL SELF
    
    def funcion_name(self): 
        while True:
            try:
                name= input("Ingrese su nombre: ")
                name = name.strip()
                #if isinstance(name,int) or isinstance(name,float): --# EN ESTE CASO NO AYUDA (YA QUE PASAMOS STR)
                if not(name.isalpha()):
                    print("Error, el nombre no puede ser un número")
                    continue
                elif len(name)<=4:
                    print("Error, el nombre debe tener al menos 5 caracteres")
                    continue
            except KeyboardInterrupt:
                print("\nCaracter no válido.")
            except EOFError:
                print("Caracter no válido")
            else: 
                name = name.title()
                return f"Hola {name}"
            
    def llamar(self):
        return(f"Estás llamando desde un {self.marca} modelo {self.modelo}")
    def cortar(self):
        return(f"Estás cortando la llamada desde un {self.marca} modelo {self.modelo}")
   
        
cel1 = CellPhone(marca= "Samsung", modelo= "S25", camara= "60MP")
cel2 = CellPhone(marca= "Apple", modelo= "Apple 15Pro Max")

name_user = cel1.funcion_name()
print(f"{name_user}, {cel1.llamar()}")
print(f"CARACTERÍSTICAS:\n{cel1.marca}\n{cel1.modelo}\n{cel1.camara}")
name_user_2 = cel2.funcion_name()
print(f"{name_user_2}, {cel2.cortar()}")
print(f"CARACTERÍSTICAS:\n{cel2.marca}\n{cel2.modelo}\n{cel2.camara}")

