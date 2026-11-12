def Name():
    name = input("Ingrese su nombre: ")
    name = (name.strip()).capitalize()
    return name

def Saludo():
    name =Name()
    return f"Que tal {name}, espero estés muy bien. Anasheii"
