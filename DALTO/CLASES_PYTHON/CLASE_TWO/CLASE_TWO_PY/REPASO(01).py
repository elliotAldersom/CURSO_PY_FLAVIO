tp = dict(Name ="flavio", Name_2 = "gerardo")

name,name_2 = tp.values()
print("Tu primer nombre es " + str(name) + ", y tu segundo nombre es " + str(name_2));

print(type(tp))
print(type(name))
print(type(name_2))

# tuple ()

tp = ("Flvio", "Gerardo");


tp_01 = "Silva", "Esatrada";

tp_02 = "Flavito",;

tp_general = tp, tp_01, tp_02;
print(tp_general)

# set()

set_1 = set(["Flavio","Gerardo"])
set_2 = set(["Flavio","Gerardo","Silva","Estrada"])
set_3 = frozenset(["Flavito","Juega Free Fire"])
set_4 = frozenset([123, 234])
set_5 = set([set_4, set_3])

print("frozenset " + str(set_5))

print("isdisjoint " + str(set_1.isdisjoint(set_2)));

print( "Intersection "+ str(set_1.intersection(set_2)))

print(set_2 > set_1)
print(set_2 < set_1)
print(set_2.issuperset(set_1))
print(set_2.issubset(set_1))

# dict()

d1 = dict(nombre = "Flavio" , apellido_pa = "Silva" , apellido_ma = "Estrada");


print(d1);

d1 = {
    "nombre" : "Flavio" ,
    "apellido_pa" : "Silva" ,
    "apellido_ma" : "Estrada"
} ;

print(d1)

t1 = "nombre","apellidos"; # --> Tuple 

name = "Flavio Silva Estrada"

name1 = "Flavio"

apellidos = "Silva EStrada"

# d2 = dict( t1 = name) --> NO SE PUEDE, PUES AL HACER EL PRINT VA A SALIR: t1 : "Flavio Silva Estrada"
# print(d2)

d2 = {
    t1 : name ,
    t1[0] : name1 ,
    t1[1] : apellidos
}
print(d2)


l1 = list(["Nombre" ,"apellidos"])  # No hashable
L1 = frozenset(l1)  # --> Si hashable, para saber si es o no hasahble usamos la función: hash(objeto) --> Si es hash, imprime una serie de números

d3 = {
    L1 : name ,
    # L1[0] : name1 ,  ---> No se puede hacer
    # L1[1] : apellidos  ---> No se puede hacer
};
print(d3)

tl = "Flavio", "Gerardo"  # ---> Tuple
d4 = dict.fromkeys(tl, "nombre")
print(d4)


tl = "Flavio", # ---> Tuple
d4 = dict.fromkeys("nombre", tl)
print(d4)

tl = "Flavio", "Gerardo" # --> Tuple
d4 = dict.fromkeys(tl)
print(d4)

tl = "Flavio", # --> Tuple
d4 = dict.fromkeys(tl)
print(d4)


# For : bucle 
# Se encarga de iterar (rcorrer)

# Iterables : Objeto recorribles 
"""
EJM DE ITERABLES: 
- String
- List
- Tuple
- Set
- Dict
- Frozenset
- Range


--> Función para saber si es iterable 
"""


frutas = ["Manzana", "Pera", "Mango", "Fresa", "Pacay", "Maracuyác"];

for frut in frutas:
    print("La fruta es: " + str(frut));

print("_____________________________________________");


frutas = ["Manzana", "Pera", "Mango", "Fresa", "Pacay", "Maracuyác"];
ind = len(frutas)

for  fruit in enumerate(frutas):
    indice = fruit[0]
    valor = fruit[1]
    print("El valor " + str(valor) + ", pertenece al índice: " + str(indice));
    
    
while True:
     print("Tu lista tiene " + str(ind) + " elementos y sus índices son del 0 - " + str(ind - 1))
     pedir =(input("Ingrese el índice para mostrar el valor: "))
     try:
        pedir = int(pedir)
        if(pedir >= 0 and pedir < ind):
          print("El valor que hay en el índice " + str(pedir) + " es: " + str(frutas[pedir]))
          break
        elif(pedir >= ind):
           print("El número ingresado no es valido, pues es mayor al índice.")
           #pedir =(input("Ingrese el índice para mostrar el valor: ")) #--> Ya no es necesario
     except ValueError:
           print("Índice o caracter dado incorrecto, intente de nuevo.")
           #pedir =(input("Ingrese el índice para mostrar el valor: ")) #--> Ya no es necesario

print("____________________________________________________________________________________________________")

frutas = {"Manzana", "Pera", "Mango", "Fresa", "Pacay", "Maracuyác"};


for fruit in enumerate(frutas):
      indice_1 = fruit[0]
      valor_1 = fruit[1]
      print("El valor " + str(valor_1) + ", pertenece al índice: " + str(indice_1));


datos = "Nombre y apellido", "Edad"
name = "Flavio Silva"
age = 18
dicci ={
   datos[0] : name,
   datos[1] : age 
}

for i in dicci.items():
    keys = i[0];
    values = i[1];
    print("El valor " + str(values) + ", pertenece a la clave: " + str(keys)) 


