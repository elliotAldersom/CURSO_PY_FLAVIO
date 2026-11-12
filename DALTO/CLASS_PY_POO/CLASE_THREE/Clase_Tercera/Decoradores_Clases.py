#PASOS:

# 1) Primero definimos un decorador para la clase:
# O se definimos una funcipon, el cual tiene otra función anidada
def User_decorator():
    
    # 2) Definir la función anidada:
    # Esta función anidada recibe obligatoriamente como parámetro una clase
    # Por convención se le suele llamar "cls"
    def super_user(cls):
        
        # 3) Dentro de la función anidada, vamos a definir una nueva clase:
        # Esta nueva clase hereda de la clase que se pasa como parámetro
        class SuperUser(cls):
            
            # 4) Vamos a agregar nuevos métodos a la clase que hemos creado
            # Estos métodos no existen en la clase original
            # También podemos sobreescribir métodos de la clase original
            # Si sobreescribimos un método, podemos usar "super()" para llamar al método
            # Podemos agregar atributos nuevos en el constructor de la nueva clase
            
            def __init__(self, name, last_name, rango="User"):
                super().__init__(name, last_name)
                self.rango = rango
            
            def get_fullname(self):
                return f"{self.get_name()} {self.get_last_name()}"

            def get_range(self):
                return f"Rango: {self.rango.capitalize()}"
            
            def __str__(self):
                return f"{self.rango.capitalize()}: {self.get_fullname()}"
        
        # 5) Retornamos la nueva clase creada
        return SuperUser
    
    # 6) Retornamos la función anidada
    return super_user


@User_decorator()
class User:
    def __init__(self, name , last_name):
        self.name = name
        self.last_name = last_name
    
    def get_name(self):
        return self.name.capitalize()
    
    def get_last_name(self):
        return self.last_name.capitalize()




if __name__ == "__main__":
    user = User("Flavio" , "Silva", "developer")
    print(user.get_fullname())
    print(user.get_range())
    print(user)
    print(type(user))
