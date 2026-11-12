"""
CLASE TWO PYTHON
"""

# Variabes 2.0:


"""
A lo largo de esta clase se va a mostrar funciones para hacer tuplas, sets, diccionarios 
y anteriormente ya hemos visto como hacer listas con un afunción; con estas funciones
podemos realizar una tupla vacía, lista vacía, set vacío, diccionario vacío; pero con la forma
común que son: (tupla) / [lista] / {set} / {dict : diccionario}
no se puede realizar esa acción que se puede hacer con las funciones de cada uno. 
"""
# 1) DESEMPAQUETAMIENTO :  Es una forma de crear variables nuevas, tomando los datos de una tupla.
                          # FUNCIONA CON: listas, tuplas, sets (orden aleatorio) y dict (diccionario)
                          # En el dict, usamos el método values() : nombre,apellido = datos.values()

datos = ["Flavio", "Silva"];   # --> Es una Lista (pero puede ser en otros tipos de datos ok?)
print(type(datos))

# DESEMPAQUETADO DE LA LISTA:
nombre,apellido = datos  # ---> CON ESTO HACEMOS QUE "nombre" = Flavio ; "apellido" = Silva.
                         # ---> Si fueran x valores de la tupla, la variabe seria x también (igual cantidad).

print(datos);
print(nombre);  # --> Imprime  Flavio
print(apellido); # --> Imprime  Silva"""




# tupla: 
t1 = "mi","tupla";
t2 = "mi tupla",;
t3 = ("mi","tupla","nueva");
t4 = tuple(["mi","tupla","nueva"]);

print("\n" + str(t1) + "\n" + str(t2) + "\n" + str(t3) + "\n" + str(t4));

print((t1,t2,t3,t4)); # --> tupla general

# set:
s1 = {"mi tupla", "nueva", "jejeje"};
s2 = set(["mi tupla","nueva","jajaja"]);
print(s1)
print(s2)

s1 = frozenset(["mi tupla", "nueva", "jejeje","jajaja"]);
s2 = frozenset(["mi tupla","nueva","jajaja"]);
s3 = {s1,s2}
print(s3);

sub_01 = s1.issubset(s2)
sub_1 = s1<s2
sub_02 = s2.issubset(s1)
sub_2 = s2<s1

super_01 = s1.issuperset(s2)
super_1 = s1>s2
super_02 = s2.issuperset(s1)
super_2 = s2>s1

print(sub_01)
print(sub_1)
print(sub_02)
print(sub_2)
print(super_01)
print(super_1)
print(super_02)
print(super_2)

print("Es disjunto (no tienen nada en común /True),(tienen algo en común /False): " + str(s1.isdisjoint(s2)));

# dict: diccionario

name = input("Ingresa tu nombre: ");
age = int(input("ingresa tu edad: "));

d1 = {
    "nombre" : name,
    "edad"   : age
};
print("diccionario con la forma común: " + str(d1))


d2 = dict(nombre = name, edad = age);
print("diccionario con la función \"dict\": " + str(d2));

tupla_key = "usuario","nombre";
tupla_key_1 = "usuario","edad";
d3 = {
    tupla_key : name,
    tupla_key_1 : age,
    tupla_key[1] : name,
    tupla_key_1[1] : age
}
print("Diccionario que tiene como key a una tupla: " + str(d3))
print("Los values son: " + str(d3.values()));
print("Los keys son: " + str(d3.keys()));


lista_key = frozenset(["usuario","nombre"])
lista_key_1 = frozenset(["usuario","edad"])
d4 = {
    lista_key : name,
    lista_key_1 : age
}
print("Diccionario que tiene como key a una lista pero pasada de mutable a inmutable con la función \"frozenset()\": " + str(d4))

keys_1 = dict.fromkeys(name) # --> name, porque es iterable 
print("dict con \"dictfromkeys()\": " + str(keys_1))

keys_2 = dict.fromkeys(name,age);
print("dict con \"dictfromkeys()\": " + str(keys_2))

keys_3 = dict.fromkeys(["NOMBRE","EDAD"],name)
print("dict con \"dict.frozenset()\": " + str(keys_3))

keys_4 = dict.fromkeys(["NOMBRE","EDAD"]);
print("dict con \"dict.frozenset()\": " + str(keys_4))


"""age_1 = frozenset(age)
keys_2 = dict.fromkeys(age) # --> con age, sale error pues no es iterable
print("dict con \"dictfromkeys()\": " + str(keys_2))"""



# For: Bucle, para iterar
# Los iterabes son los que se pueden recorrer uno por uno, como las listas, tupas, set, dict, range, string, frozenset

print("\nBUCLE FOR:\n")
t1 = "hola","mundo","hello","world";
for saludo in t1:
    print("Las palabras son: " + str(saludo));

t2 = list([1,2,3,4])
for palabra,numero in zip(t1,t2):
    print("La palabra número " + str(numero) + " es: " + str(palabra));


n = int(input("Ingresa hasta wue número quieres que se muestres (0 - x): "));
for i in range(n):
    print("El número es: " + str(i));

for a in enumerate(t1):
    indice = a[0];
    valor = a[1]
    print("El valor que hay en el índice " + str(indice) + " es: " + str(valor));
else : 
    print("No hay valores en el iterable");



