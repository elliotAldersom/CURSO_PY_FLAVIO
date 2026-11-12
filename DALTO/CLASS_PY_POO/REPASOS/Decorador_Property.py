class Person:
    def __init__(self, name, age):
        self.__nombre = name
        self.__edad = age
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, new_name):
        self.__nombre = new_name
    
    @property
    def edad(self):
        return self.__edad
    
    @edad.setter
    def edad(self,new_edad):
        self.__edad = new_edad
    
    @property
    def Datos(self):
        # ESTA FORMA MUESTRA EL _Person__nombre y no queremos que se vea así
        #data = (self.__dict__).items()
        
        # HACEMOS ASÍ:
        data = {
            "Nombre" : self.__nombre,
            "Edad" : self.__edad
        }.items()
        data_order = "\n".join(f"{key}: {value}" for key,value in data)
        return data_order
    
    @Datos.setter
    def Datos(self, new_Data):
        if isinstance(new_Data , tuple) and len(new_Data) == 2:
            name = new_Data[0]
            if isinstance(name , str):
                name = (name.strip()).title()
                edad = new_Data[1]
                if isinstance(edad , int):
                    self.__nombre = name 
                    self.__edad = edad
                    print ("Datos cambiados existosamente...")
                else:
                    print("La edad debe ser un número entero")
            else:
                print("El nombre debe ser texto")
        else:
            print("Los datos deben ser un par de valores (nombre, edad), si no es así no se modifican")
                

    @Datos.deleter
    def Datos(self):
        confir = input("Desea eliminar sus datos [S/N]: ").strip().lower()
        if confir == "s":
            del self.__nombre
            del self.__edad 
            print("Datos borrados...") 
        elif confir == "n":
            print("No se borraron los datos...")
        else: 
            print("No escogió nada y por lo tanto no se borrará...")
        

xd = Person("Juan", 25)
nombre = xd.nombre
print(nombre)
print(xd.nombre)
xd.nombre = "Pedro"
new_name = xd.nombre
print(new_name)
print(xd.nombre)
print("______________")
print(xd.Datos)

xd.Datos = "Flavio Gerardo" , 19
new_data = xd.Datos
print(new_data)

del xd.Datos
try:
    print(xd.Datos)
except AttributeError:
    print("Ya no hay datos para mostrar...")