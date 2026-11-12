
def Name():
    User = input("Ingrese su nombre de usuario: ")
    User = (User.strip()).capitalize()
    return User

def Saludar():
    User = Name()
    mensaje = f"Bienvenido al sistema {User}"
    return mensaje

def Saludar_raro():
    User = Name()
    mensaje = f"Hola {User}, espero estés nashe, ansheli, anasheiii"
    return mensaje

print(__name__)
