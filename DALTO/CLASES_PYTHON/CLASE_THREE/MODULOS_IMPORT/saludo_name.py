
def Name():
    User = input("Ingrese su nombre de usuario: ")
    User = (User.strip()).capitalize()
    return User

def Saludar():
    User = Name()
    mensaje = f"Bienvenido al sistema {User}"
    return mensaje

