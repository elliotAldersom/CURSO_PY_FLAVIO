# 2) tupla:
#   - Es inmutable (no se puede modificar, por medio de métodos como el remove, clerar, etc..)
#   - Es ordenada (se puede acceder a los elementos por su posición / índice)
#   - Si se modifica, se debe de modificar toda la variable, no una parte de ella (como agregar valores).

# 2.0) Creando tupla con la función tuple()
# LA FORMA DE CREAR TUPLAS VACÍOS ES AL USAR ESTA FUNCIÓN, NO PPODEMOS HACERLO CON LA FORMA COMÚN.

print("TUPLA:");
tupla_1 = ("dato1","dato2")  # --> Froma común.
print(tupla_1)

tupla = tuple(["Dato1", "Dato2"]) # ----> AL USA LA FUNCIÓN DE TUPLA
                                  # HAY QUE HACER ASÍ: tuple(["V1","V2"]) 
                                  # Primero es una lista, la cual se convierte en tupla
print(tupla)
print("___________________________________________________________");

# 2.1) Creando una tupla de multiples datos, sin paréntesis ().
tupla = "Flavio", "Gerardo", "Silva", "Estrada"  # ---> Otra forma de crear una tupla
# Esta forma se basa en poner datos (strings / int / float) pero separados por comas (,).

print(tupla);
print(type(tupla))
print("___________________________________________________________");

# 2.2) Creando una tupla de un solo dato, sin paréntesis.

tupla = "Flavio Gerardo Silva Estrada",
print(tupla);
print(type(tupla)); 
print("___________________________________________________________");



# Saber cuantas veces se repite un valor en una tupla

miTupla = "danilo","carlos","juan","fabio","juan","juan",12,2334
n_veces = miTupla.count("juan")
print(f"Juan se repite {n_veces} veces en la lista")

# Usar index:
# El index() devuelve el índice de la primera ocurrencia del elemento especificado.
# Si el elemento no está presente, devuelve un ValueError.
print(miTupla.index("juan"))
print(miTupla[4:])
print(miTupla)

"""
- Las tuplas las podemos crear cuando son datos de solo lectura, solo
vamos a leer datos, ahí usamos las tuplas.

"""



