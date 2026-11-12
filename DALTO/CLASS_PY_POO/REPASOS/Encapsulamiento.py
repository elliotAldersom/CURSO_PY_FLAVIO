# class Person:
#     def __init__(self, name, age):
#         self.__nombre = name
#         self.edad = age
    
#     def presentar_name(self):
#         return f"El nombre es {self.__nombre}"

#     def __presentar_age(self):
#         return f"Su edad es {self.edad}"


# one = Person("Flavio", 18)
# print(one.presentar_name())

# print(one._Person__nombre)

# print(one.edad)
# print(one._Person__presentar_age())



class Person:
    def __init__(self, name, age):
        self.__nombre = name
        self.__edad = age
    
    def get_presentar_name(self):
        return f"El nombre actual es: {self.__nombre}"

    def get_presentar_age(self):  
        return f"Su edad actual es: {self.__edad}"
    
    def set_cambiar_age(self, new_age):
        print(f"Su antigua edad era: {self.__edad}")
        self.__edad = new_age
        print(f"Su nueva edad es {self.__edad}")


Flavio = Person("Flavio", 18)
nombre = Flavio.get_presentar_name()
print(nombre)

Flavio.set_cambiar_age(17)
edad = Flavio.get_presentar_age()
print(edad)