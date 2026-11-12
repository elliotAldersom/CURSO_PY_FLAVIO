# 3) set:
#   - Es un conjunto de datos (no tiene orden)
#   - No se pueden repetir los datos (no se pueden repetir los elementos)
#   - No se pueden modificar (por medio del índice), solo por medio de métodos.
#   - ES MUTABLE.
#   - No se pueden acceder a los elementos por su posición / índice.

print("set:");
# 3.0) Creando un set con la función set: PARA HACER UN SET VACÍO NECESITAMOS USAR LA FUNCIÓN set().

set_1 = set(["dato1", "dato2"]); # ---> Así se hace un conjunot set
# Tenemos que pasarle una lista dentro de a función para así convertirlo a un conjunto set.
print(set_1);
print(type(set_1));
print("___________________________________________________________");

# 3.1) Metiendo un conjunto dentro de otro conjunto:

# PARA HACER ESTO POSIBLE USAMOS LA FUNCIÓN: frozenset()
# Esta función nos permite crear un conjunto de datos que son inmutables.
# Luego de llamar a la función, pasamos una lista, la cual contendrá los datos a pasar.

conjunto_1 = frozenset([ "DATO1", "DATO2"]);  
conjunto_2 = { conjunto_1, "DATO3", "DATO4" };
print(conjunto_2);
print("___________________________________________________________");


#TEORIA DE CONJUNTO: 
# 1) El conjunto_2 es un subconjunto de conjunto_2, pues contiene algunos datos del conjunto_1.
# 2) El conjunto_1 es un superconjunto del conjunto_2, pues contiene al conjunto_2 y más.
# TODO ESTO DEPENDE DE DONDE PARTIMOS COMO CONJUNTO:
# Si conjunto_1 es el conjunto, entonces se cumple el "1)".
# Si conjunto_2 es e conjunto, entonces se cumple el "2)".

# EJM:
conjunto_1 = {1, 3, 5, 7, "$"};
conjunto_2 = {1, 5, 7, "$"};
# verificación de subconjunto (subset)  : método issubset() ---> imprime valores booleano (True/ False).
resultado_1 = conjunto_2.issubset(conjunto_1); # ---> Usamo el método:
resultado_2 = conjunto_1.issubset(conjunto_2); # ---> issubset()
resultado_3 = conjunto_2 < conjunto_1  # ---> Otra forma.
resultado_4 = conjunto_1 < conjunto_2 # ---> Otra forma.

print(resultado_1);
print(resultado_2);
print(resultado_3);
print(resultado_4);

print("___________________________________________________________");

# verificación de superconjunto (superset) : método issuperset() ---> imprime valores booleanos (True / False).

resultado_01 = conjunto_1.issuperset(conjunto_2); # --> Usamos el método:
resultado_02 = conjunto_2.issuperset(conjunto_1); # --> issuperset()
resultado_03 = conjunto_1 > conjunto_2  # --> Otra forma.
resultado_04 = conjunto_2 > conjunto_1 # --> Otra forma.
print(resultado_01);
print(resultado_02);
print(resultado_03);
print(resultado_04);

print("___________________________________________________________");

# Verificar si hay no hay nada en común: método --> isdisjoint() (es disjunto / no hay nada en común).

resultado_001 = conjunto_2.isdisjoint(conjunto_1);   # ---> SI  NO HAY NADA EN COMÚN, IMPRIME TRUE, Y SI TIENE ALGO EN COMÚN, DEVUELVE FALSE.
print(resultado_001);

print("___________________________________________________________"); 

# Verificar intersecciones: Método --> intersection()

set_1 = set(["Flavio","Gerardo"])
set_2 = set(["Flavio","Gerardo","Silva","Estrada"])

print( "Intersection "+ str(set_1.intersection(set_2)))

print("___________________________________________________________"); 
