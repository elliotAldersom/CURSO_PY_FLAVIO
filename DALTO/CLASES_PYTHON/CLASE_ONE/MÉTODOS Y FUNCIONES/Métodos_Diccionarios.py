print("MÉTODOS DE DICCIONARIOS");

# 1) keys : Devuelve el valor que hay en las claves (keys), en este caso son 001, 002, 003, 004.

v1 = input("INGRESA EL PRIMER VALOR: ");
v2 = input("INGRESA EL SEGUNDO VALOR: ");
v3 = input("INGRESA EL TERCER VALOR: ");
v4 = input("INGRESA EL CUARTO VALOR: ");

diccionario = {
    "001" : v1 ,
    "002" : v2 ,
    "003" : v3 ,
    "004" : v4 
}

print("EL DCCIONARIO CREADO ES ESTE:\n" + str(diccionario));

diccionario_1 = diccionario.keys()
print("EL DICCIONARIO CON EL MÉTODO KEYS SE VE ASÍ\n" + str(diccionario_1))

print("_______________________________________________________________________");

# 2) values : Devuelve el valor que hay en los valores (values).
valor = diccionario.values()
print("LOS VALORES DE CADA CLAVE SON:\n" + str(valor));

print("_______________________________________________________________________");


# 3) get : Devuelve el valor de la clave que nosotros pasemos.

pregunta = input("DESEAS VER UN VALOR DE UNA DE LAS CLAVES DEL DICCIONARIO: SI / NO\n");

if((pregunta.upper() == "SI") or (pregunta.upper() == "SÍ")):
    print("ESTAS SON LAS CLAVES:\n" + str(diccionario.keys()));
    clave = input("INGRESA LA CLAVE QUE DESEAS VER: ");
    print("EL VALOR DE LA CLAVE ES:\n" + str(diccionario.get(clave)));

else:
    print("ENTENDIDO, NO VAS A PEDIR NADA.");

print("_______________________________________________________________________");


# 4) pop : ELIMINA UN VALOR, PERO PONIENDO UNA CLAVE (KEY).

eliminar = input("DESEAS BORRAR ALGÚN ELEMENTO DE UNA DE LAS CLAVES? SI / NO\n");

if((eliminar.upper() == "SI") or (eliminar.upper() == "SÍ")):
    print("ESTAS SON LAS CLAVES:\n" + str(diccionario.keys()));
    borrar = input("INGRESA LA CLAVE PARA BORRAR SU VALOR: ");
    print("EL VALOR A BORRAR ES\n" + str(diccionario.pop(borrar)));
    print("EL DICCIONARIO SIN ESE VALOR ES:\n" + str(diccionario.values()));
else:
    print("ENTENDIDO, NO VAS A BORRAR NADA.");


print("_______________________________________________________________________");


# 5) items : Es para iterar el diccionario.

print("EL DICCIONARIO ACTUALIZADO ES:\n" + str(diccionario));

iterar = diccionario.items();

print("EL DICCIONARIO ITERADO ES:\n" + str(iterar));

print("_______________________________________________________________________");

# 6) clear : Elimina todos los elementos.

limpiar = diccionario.clear()

print("EL DICCIONARIO LIMPIO SE VE ASÍ:\n" + str(limpiar));

print("_______________________________________________________________________");