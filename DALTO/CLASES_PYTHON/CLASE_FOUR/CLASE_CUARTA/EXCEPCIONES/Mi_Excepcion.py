""" 
Creando mi propia excepción personalizada:
"""
class MiExcepcion(Exception):
    def __init__(self, error):
        print(f"El error es: {error} ")


""" 
Lanzando la excepción con raise
"""
try:
    # raise es la palabra clave para lanzar una excepción
    raise MiExcepcion("Bro te equivocaste")
except:
    print("Se ha producido un error")
