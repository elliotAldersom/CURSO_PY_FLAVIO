# DICCIONARIOS 2.0
# ES MUTABLE, PERO SUS KEYS (CLAVES) DEBEN DE SER INMUTABES
print("DICCIONARIOS:");

# CREANDO DICCIONARIOS CON LA FUNCIÓN dict():
# LA FORMA DE CREAR DICICONARIOS VACÍOS ES A USAR ESTA FUNCIÓN, NO PPODEMOS HACERLO CON LA FORMA COMÚN.

diccionario = dict(nombre = "Flavio", apelido =  "Silva", apodo = "Flavito");
print(diccionario);
print("___________________________________________________________");

# CREANDO DICCINARIO DE FORMA COMÚN:

diccionario_1 = {
    "nombre"  : "Flavio",
    "apllido" : "Silva",
    "apodo"   : "Flavito"
};

print(diccionario_1);
print("___________________________________________________________");


# LAS LISTAS Y SETS NO PUEDEN SER CLAVES, PORQUE SON MUTABLES (MODIFICABLES POR ÍNDICE O MÉTODOS).
# LAS TUPLAS SI PUEDEN SER CLAVES, PORQUE SON INMUTABLES (HASHABLE).

# HASHABLE: ES UN OBJETO INMUTABLE, EL CUAL NO PUEDE MODIFICARSE, NI POR ÍNDICE O POR MÉTODS.
# DEBE DE CUMPLIR DOS CONDICIONES CLAVES:
# TENER UN VALOR FIJO DE HASH DURANTE SU VIDA ÚTIL:
# EL VALOR QUE DEVUELVE AL USAR LA FUNCIÓN: hash(objeto) no cambia mientras el objeto exista.
# PUEDE COMPARARSE CON OTROS OBJETOS PARA SABER SI ES IGUAL O DISTINTO MEDIANTE EL MÉTODO: objeto1__eq__(objeto2)

nombre = "dalto";
dato = (nombre,"rancio")
print(type(dato)); # Devuelve tupla
print(hash(dato));
diccionario_01 = {
    dato : "jajajas",
    nombre : "jejeje"
    }

print(f"KEYS CON OBJETO INMUTABLES (HASHABLES): {diccionario_01}");

print("___________________________________________________________");

# SI QUEREMOS INTRODUCIR COMO KEYS ALGÚN DATO MUTABLES USAMOS LA FUNCIÓN: frozenset()
# frozenset(), transforma de mutable a hashable
listado = list(["dalto", "rancio"]);
print(type(listado));
dato_1 = frozenset(listado);
print(type(dato_1));
print(dato_1)
print(hash(dato_1));
diccionario_001 = {
    dato_1 : "jajajas"
}
print("KEYS CON OBJETOS MUTABLES PERO USANDO LA FUNCIÓN FORZENSET(): " + str(diccionario_001));
print("___________________________________________________________");


lista = {1,2,3} # es un set
fs = frozenset(lista)
print(fs)

dict ={
    fs : "hola"
}
print("KEYS CON OBJETOS MUTABLES PERO USANDO LA FUNCIÓN FORZENSET(): " + str(dict));

print("___________________________________________________________");

# CREANDO DICCIONARIOS CON: fronkeys
# ES UNA FUNCIÓN QUE PUEDE CREAR DICCIONARIOS CON TODOS LOS VALORES NONE.
# CON ESTA FORMA SOLO PODEMOS TENER DOS ARGUMENTOS DENTRO, NOS IMPRIME UN NONE, HACE ALGO DISTINTO.
diccionario_002 = dict.fromkeys("nombre"); 
print(diccionario_002); # --> imprime -->  n : none , o : none , m : none , b : none , r : none , e : none

diccionario_002 = dict.fromkeys("nombre", "VALOR A LO QUE SE IGUALA"); 
print(diccionario_002); # --> imprime -->  n : vaor a lo que se iguala , o : valor a lo que se iguala , m : valor a lo que se iguala , b : valor a lo que se iguala ,
                                        #  r : valor a lo que se iguala ,  e : valor a lo que se iguala

# CON NÚMERO DE ARGUMENTOS MAYOR A DOS ARGUMENTOS, ASÍ CADA UNO VA A DECIR NONE EN EL VALOR
diccionario_003 = dict.fromkeys(["nombre", "apellidos", "apellido"]); 
print(diccionario_003);
print(diccionario_003["nombre"]);  # --> Forma de pedir un valor por medio del key.
print(diccionario_003.get("nombre")) # ---> forma de pedir un valor por medio del key.

diccionario_003 = dict.fromkeys(["nombre", "apellidos", "apellido"], "VALOR AL QUE SE IGUALA"); 
print(diccionario_003);
print(diccionario_003["nombre"]) # Imprime el value de este key : Valor al que se iguala
diccionario_003.pop("nombre")
print(diccionario_003)
print(diccionario_003.get("nombre")) # --> sale None porque no se encuentra el valor ni el key







# AGREGANDO UN ELEMENTO A UN DICCIONARIO
print("AGREGANDO UN ELEMENTO A UN DICCIONARIO:")

miditc = {
    "Perú" : "Lima",
    "Argentina" : "Buenos Aires",
    "Chile" : "Santiago",
    "Colombia" : "Bogotá",
    "Ecuador" : "Quito",
    "Venezuela" : "Caracas"
}

print(miditc)
print(miditc["Perú"])
#_______________________

miditc["Italia"] = "Londres" # Esto lo pongo par sobreescribirlo luuego
print(miditc)

# Para sobreescribilo es así:
miditc["Italia"] = "Roma"
print(miditc)



# EJM CON TUPLA COMO KEY:
myTuple = "Perú","Argentina","Chile"
myDict = {
    myTuple[0] : "Lima",
    myTuple[1] : "Buenos Aires",
    myTuple[2] : "Santiago"
}
print(myDict) # --> {'Perú': 'Lima', 'Argentina': 'Buenos Aires' , 'Chile': 'Santiago' }

# ALMACENANDO EN UN DICT : TUPLA, LIST, SET, DICT
name_list = ["Flavio","Fabian","Gerardo"]
age_set = {12,34,45}
myDict2 = {
    "Names" : name_list, # class List
    "Countrys" : myTuple, # class Tuple
    "Age" : age_set, # class Set
    "Capital" : myDict # class Dict
}
print(myDict2)