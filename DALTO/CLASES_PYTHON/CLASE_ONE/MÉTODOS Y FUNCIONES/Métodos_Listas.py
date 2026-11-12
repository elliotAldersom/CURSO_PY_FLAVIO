

print("MÉTODOS DE LISTAS");



# 1) list : Transforma cualquier tipo de cadena, tupla, set, diccionario a una lista. (da sus características de lista).
string = input("Ingrese un texto: ");
print(list(string));

print("Ingresa valores de texto");
v1 = input("Ingresa el primer valor: ");
v2 = input("Ingresa el segundo valor: ");
v3 = input("Ingresa el tercer valor: ");
v4 = input("Ingresa el cuarto valor: ");

tupla = (v1 , v2 , v3 , v4 );
print("Tu tupla:\n" + str(tupla));

tupla_1 = list(tupla);
print("Tu tupla en lista:\n" + str(tupla_1));

print("________________________________________________________________")

set = {v1 , v2 , v3 , v4};
print("Tu conjunto set:\n" + str(set));

set_1 = list(set);
print("Tu set en lista:\n" + str(set_1));

print("________________________________________________________________");

dict = {
    "valor 1" : v1 ,
    "valor 2" : v2 ,
    "valor 3" : v3 ,
    "valor 4" : v4
}
print("Tu diccionario:\n" + str(dict));

dict_1 = list(dict.values()); # ---> Para que muestre el valor asociado de las claves y no solo las claves.
print("Tu diccionario en una lista:\n" + str(dict_1));

print("________________________________________________________________");

# 2) append : Agrega un elemento a la lista (al final).

lista = list(string);

lista.append("FELIZ DÍA.");

print(lista);

list = ["Enero" , "Febrero" , "Marzo" , "Abril" , "Mayo" , "Junio" , "Julio" , "Agosto"];
print(list);
list.append("Septiembre");
print(list);

print("________________________________________________________________"); 

# 3) insert : Agrega un valor a la lista en el índice especificado.

lista_1 = ["CASA" , "CASITA" , "CASOTA"];
print(lista_1);

cantidad = int(len(lista_1));
indice_1 = cantidad - 1
print("HAY " + str(cantidad) + " ELEMENTOS.")

agregar = input("DESEAS AGREGAR ALGO MÁS A LA LISTA? (SÍ / NO)\n");

if((agregar.lower() == "sí") or (agregar.lower() == "si")):
    dato = input("INGRESE EL TEXTO QUE VA A AGREGAR:\n");
    print("RECUERDE:\nSU NÚMERO DE ÍNDICE ES EL NÚMERO DE ELEMENTOS MENOS UNO, POR LO TANTO SI TIENE " + str(cantidad) + " ELEMENTOS, PARA EL NÚMERO DE ÍNDICE QUE TIENE SE LE RESTA 1, POR LO TANTO TIENE: " + str(indice_1) + " ÍNDICE (S)");
    indice = int(input("INGRESE EL NÚMERO DEL ÍNDICE EN EL QUE VA A AGREGAR SU TEXTO:\n"));
    lista_1.insert(indice, dato);
    print("LA LISTA NUEVA SE VE ASÍ:\n" + str(lista_1));

else:
    print("ENTENDIDO  NO SE VA A AGREGAR NADA.");

print("________________________________________________________________")

#  4) extend : Agrega varios elementos al final de la lista.

print("ESTA ES LA LISTA:\n" + str(list));

agregado = input("DESEAS AGREGAR ALGO MÁS? (SÍ / NO)\n");

if((agregado.upper() == "SÍ") or (agregado.upper() == "SI")):
    dato_1 = input("INGRESE LOS VALORES A AGREGAR, SEPARADO POR COMAS (,):\n");
    dato_01 = dato_1.split(",")  # TAMBIÉ SE PUEDE AGREGAR POR VALORES, SI PEDIMOS QUE INGRESEN VALORES, PERO DEBERIAMOS INGRESAR LOS VALORES QUE DESEAN, Y CON ESTO LO ACORTAMOS YA QUE EL DECIDE Y SE HACE LISTA CON SPLIT Y SE AGREGA.
    list.extend(dato_01);
    print("TU NUEVA LISTA SE VE ASÍ:\n" + str(list));

else:
    print("ENTENDIDO NO SE AGREGARÁ NADA.");

print("________________________________________________________________")

# 5) pop : Elimina el valor del índice que nosotros pasemos, además nos muestra el valor de ese índice

cadena1 = [v1 , v2 , v3 , v4];

print(cadena1);

print(len(cadena1));

borrar = int(input("INGRESA EL ÍNDICE EL CUAL QUIERES BORRAR: "));

print(cadena1.pop(borrar)) # MUESTRA VALOR DEL ÍNDICE.
print(cadena1) #MUESTRA LA LISTA SIN EL ÍNDICE BORRADO.

borrar2 = int(input("INGRESA EL ÍNDICE EL CUAL QUIERES BORRAR: "));

(cadena1.pop(borrar2));
print(cadena1)

print("________________________________________________________________")

# 6) remove : Remueve un elemento de la lista, pero pide su valor, no el índice.

cadena2 = [v1 , v2 , v3 ,v4];
print(cadena2);

remover = input("Ingresa el valor de la lista que deseas borrar: ");
remover_1 = remover.strip()
cadena2.remove(remover_1.capitalize()); # Para borrar ese valor, primero hacemos así y luego se imprime la lista.

print("La lista modificada es aasí:" + str(cadena2));   # Tienes que imprimir la lista sin el método remove, para que se imprima el valor de la lista.

print("________________________________________________________________")

# 7) clear : Elimina toda la lista.

cadena3 = [v1 , v2 , v3 , v4];

print(cadena3);

print("VAMOS A LIMPIAR LA LISTA: " + str(cadena3.clear()) + " Así se ve."); # LA LISTA LIMPIA AL IMRPIMIR VOTA UN NONE.

print("________________________________________________________________")

# 8) sort : Ordena la lista de forma ascendente, solo si es numérico.

print("INGRESA VALORES NUMÉRICOS");

v5 = input("INGRESA EL PRIMER VALOR: ");
v6 = input("INGRESA EL SEGUNDO VALOR: ");
v7 = input("INGRESA EL TERCER VALOR: ");
v8 = input("INGRESA EL CUARTO VALOR: ");

listado = [v5 , v6 , v7 , v8];

print(listado)

listado.sort()
print("TU LISTA ORDENADA:\n" + str(listado))

print("_____________________________________________________________________________________")

# 9) reverse : Invierte el orden de la lista

listado_1 = [v5, v6, v7, v8];

print(listado_1)

listado_1.reverse()
print("TU LISTA INVERTIDA:\n" + str(listado_1))

print("_____________________________________________________________________________________")
