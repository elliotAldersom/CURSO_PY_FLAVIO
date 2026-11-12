from decimal import Decimal, ROUND_HALF_UP

name = input("Ingresa tu nombre: ");
print(name);
print(name[0:3]);
print("________________________________________________________________");

age = int(input("Ingrese su edad: "));
print(age);
print("________________________________________________________________");

print("Te presentamos una lista: ");

print("""Las listas nos dejan acceder a cada valor por índice, nos dejan modificar un elemento.
Y si gustas puedes modificar todos los valors (los que están entre corchetes []).""")

lista = ["Bebé" , "Niñéz" , "Juventud" , "Adultéz" , "Vegéz" , "Muerte"] ;
print(lista);
print("________________________________________________________________");

print("Te presentamos una tupla: ");

print("""Las tuplas, estas no se pueden modificar un solo valor, solo se puede modificar todos los valores a la vez, o sea la variable.
Los valores de las tuplas son los que están dentro de parentesis ( ).
Se pueden buscar por índice.""");

tupla = ("Hoy" , "es" , "un" , "día" , "feliz");
print(tupla);
print("________________________________________________________________");

print("Te presentamos un set: ");

print("""Los set son desordenados y por eso no se pueden acceder a ellos por índice.
Tampoco nos dejan modificar algún elemento por no contar con índices.
Tampoco permiten almacenar valores que se repitan.""");

set = {1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10};
print(set);
print("________________________________________________________________");

print("te presentamos un diccionario:" );

print("""Los diccionarios se pueden modificar de manera completa, o sea tu variable cmbiando de valores.
Los valores de los diccionarios son los que se encuentran entre las llaves { }.
Se pueden buscar por índice.
No recomiendo cambiar un solo valor, porque bueno en lo personal se me hace complicado,
ya que al imprimir el diccionario completo, ese valor se va al último, o puedes solo imprimir según su índice.""");

print("")
diccionario = {
    "nombre" : name ,
    "edad" : age ,
    "pais" : "Perú" ,
    "capital" : "Lima"
};
print(diccionario);
print("________________________________________________________________");

print("OPERADORES NUMÉRICOS:")

print("ADICIÓN:");
v1 = input("Ingresa el primer valor: ");
v2 = input("Ingresa el segundo valor: ");

numero_1 = Decimal(v1);
numero_2 = Decimal(v2);

suma = numero_1 + numero_2 ;
adicion = suma.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La suma de los dos valores es: " + str(adicion));
print("________________________________________________________________");

print("SUSTRACCIÓN:");

resta = numero_1 - numero_2 ;
sustrtaccion = resta.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP );
print("La resta de los dos valores es: " + str(sustrtaccion));
print("________________________________________________________________");

print("PRODUCTO:");

multiplicacion = numero_1 * numero_2 ;
producto = multiplicacion.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("El producto de los valores es: " + str(producto));
print("________________________________________________________________");

print("DIVISIÓN:")

D1 = numero_1 / numero_2 ;
division = D1.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La división de los valores es:" + str(division));
print("________________________________________________________________");

print("POTENCIA:");

P1 = numero_1 ** numero_2 ;
potencia = P1.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La potencia de los valores es: " + str(potencia));
print("________________________________________________________________");

print("RADICACIÓN: ");

R1 = numero_1 **(1/numero_2) ;
radicacion = R1.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La radicación de los valores es: " + str(radicacion));
print("________________________________________________________________");

print("DIVISIÓN BAJA:");
D2 = numero_1 // numero_2 ;
division_baja = D2.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La división baja de los valores es: " + str(division_baja));
print("________________________________________________________________");

print("MODULO:");
M1 = numero_1 % numero_2 ;
modulo = M1.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("El modulo de los valores es: " + str(modulo));
print("________________________________________________________________");

print("IN and NOT IN:");

string = input("Ingrese su texto:\n");
print("El texto ingresado es: " + str(string));

opcion = input("DESEA INGRESAR ALGUNA PALABRA PARA SABER SI ESTÁ PRESENTE \nEN SU TEXTO? ");

if ((opcion.lower() == "sí") or (opcion.lower() == "si")):
     palabra = input("INGRESE LA PALABRA PARA VERIFICAR: ");
     if (palabra in string):
          print("LA PALABRA DADA SI PERTENECE AL TEXTO.");
     else:
          print("LA PALABRA DADA NO PERTENECE AL TEXTO.");
else:
     print("ENTENDIDO, NO DESEA VERIFICAR NADA.");


opcion_1 = input("DESEA INGRESAR ALGUNA PALABRA PARA SABER SI NO ESTÁ PRESENTE \nEN SU TEXTO? ");

if ((opcion.capitalize() == "Si") or (opcion.capitalize() == "Sí")):
     palabra_1 = input("INGRESE LA PALABRA PARA VERIFICAR: ");
     if (palabra_1 not in string ):
          print("LA PALABRA DADA NO PERTENECE AL TEXTO.");
     else:
          print("LA PALABRA DADA SI PERTENECE AL TEXTO.");
else:
     print("ENTENDIDO, NO DESEA VERIFICAR NADA.");
     
print("________________________________________________________________");

print("FUNCIONES Y MÉTODOS:");

print("""FUNCIONES:
SU ESTRUCTURA ES: funcion(variable)
MÉTODOS:
SU ESTRUCTURA ES: variable.metodo()""");

string = input("INGRESE TEXTO PARA REALIZAR LAS FUNCIONES Y MÉTODOS: \n");

# 1) dir: DEVUELVE ATRIBUTOS DEL OBJETO.
atributos = dir(string);
print("LOS ATRIBUTOS DEL OBJETO DADO SON: \n" + str(atributos));

# 2) len: devuelve la lomgitud del objeto dado (número de caracteres).
longitud = len(string);
print("LA LONGITUD DEL OBJETO INGRESADO (NÚMERO DE CARACTERES) ES " + str(longitud));

print("_____________________________________________________________________________________")

# 3) upper: transforma todo el String a mayúscula.
mayus = string.upper();
print("EL STRING EN MAYÚSCULA ES: \n" + str(mayus));

# 4) lower: transforma todo el String a minúscula.
minus = string.lower();
print("EL STRING EN MINÚSCULA ES: \n" + str(minus));

# 5) capitalize: pone el primer caracter del String en mayúscula.
primero = string.capitalize();
print("EL STRING CON EL PRIMERO EN MAYÚSCULA ES ASÍ: \n" + str(primero));

# 6) title: transforma el String a formato título (cada palabra inicia con mayúscula).
titulo = string.title();
print("EL STRING EN FORMATO TÍTULO ES: \n" + str(titulo));

# 7) find: Busca la primera aparición del caracter dado, sino devuelve un -1.
buscar = input("Igrese el caracter a buscar: ");
buscador = string.find(buscar);
print("LA PRIMERA APARICIÓN DEL CARACTER EN EL TEXTO ES EN EL NÚMERO:\n" + str(buscador));

# 8) index: Busca la primera aparicón del caracter dado, sino devuelve un error.
buscar_1 = input("DESEA BUSCAR ALGO MÁS? ");
if((buscar_1.lower() == "sí") or (buscar_1.lower() == "si")):
    dato = input("Ingrese el caracter a buscar: ");
    buscador = string.index(dato);
    print("EL CARACTER INGRESADO SE ENCUENTRA EN EL NÚMERO: \n" + str(buscador));
else:
    print("ENTENDIDO NO SE VA A BUSCAR NADA");

# 9) split: Transforma el texto en una lista.
lista_0 = input("Ingrese con que quiere separar el texto para generar una lista (lo que ingrese debe de estar en el texto): ");
lista = string.split(lista_0);
print("TU TEXTO SE ACABA DE TRANSFORMAR EN UNA LISTA: \n" + str(lista));

# 10) replace: Reeplaza algo del string por lo que tu pongas.
reemplazo = string.replace(" " , "");
print("EL TEXTO DADO SIN ESPACIOS SE VE ASÍ:\n" + str(reemplazo));

# 11) isnumeric: Verifica si tu texto está compuesto por números (totalmente, no acepta espacios, ningún string o ", . ; / \ , etc..").
# 12) isalpha: Verifica si tu texto está compuesto por letras (totalmento, no aceptaespacios, números o ", . ; : \ / , etc..").
buscar_2 = input("QUIERES COMPROBAR SI TU TEXTO ES NUMÉRICO O ALFABÉTICO? ");

if((buscar_2.lower() == "sí") or (buscar_2.lower() == "si")):
    if(reemplazo.isnumeric() == True):
        print("TU TEXTO ES NÚMERICO.");
    elif(reemplazo.isalpha() == True):
        print("TU TEXTO ES ALFABÉTICO.");
    else:
        print("TU TEXTO NO ES NI NUMÉRICO NI ALFABÉTICO.");
        print("DEBE DE SER PORQUE CONTIENE UNA MEZCLA ENTRE NUMERO Y LETRAS O SÍMBOLOS ESPECIALES.");
else:
    print("ENTENDIDO NO QUIERE VERIFICAR NADA.");

# 13 / 14) startswith/ endswith : con que inicia/termina la cadena dada.
palabra = input("Quieres saber con que inicia o termina tu texto?\n");

if((palabra.lower() == "si") or (palabra.lower() == "sí")):
     opcion = input("Que quieres buscar, en inicio o final?\n");
     if(opcion.lower() == "inicio"):
         palabra_1 = input("Ingrese la palabra a buscar: ");
         buscar_2 = string.startswith(palabra_1);
         if(buscar_2 == True):
             print("Tu texto si inicia con la palabra o cadena dada.");
         else:
             print("El texto no inicia con la palabra o cadena dada.");
     elif(opcion.lower() == "final"):
         palabra_2 = input("Ingrese la palabra a buscar: ");
         buscar_3 =  string.endswith(palabra_2);
         if(buscar_3 == True):
           print("El texto si termina con la palarba o cadena dada.");
         else:
           print("El texto no termina con la palabra o cadena dada.");
else:
    print("Entendido no desea buscar o confirmar nada.");

# 15) count : Devuelve las veces que aparece la cadena dada en el texto o lista.

count = input("Ingresa la palabra o caracter para ver cuantas veces se repite en el texto:\n");

count_1 = string.count(count);

if(count_1 == 0):
    print("No se encuentra ninguna repetición de la palabra dada.");
else:
    print("Tu texto contiene " + str(count_1) + " veces la palabra dada.");

# 16) strip : elimina los espacios tanto del inicio y del final de tu cadena dada.
palabra_3 = input("Ingrese la palabra con espacios al inicio y al final para usar el método strip.\n");

corregido = palabra_3.strip();

print("Así se ve tu texto sin strip:\n" + str(palabra_3) + "\nAsí se ve tu string con strip:\n" + str(corregido));

print("_____________________________________________________________________________________")



""" 
MÉTODOS: variable.método();
1) Upper()
2) Lower()
3) Capitalize()
4) Title()
5) Index()
6) Find()
7) Replace()
8) Split()
9) Count()
10) Startswith()
11) Endswith()
12) Isnumeric()
13) Isalpha()
14) Strip()

Funciones: función(variable)
1) len()
2) dir()
3) type()
print("_____________________________________________________________________________________")
"""


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


"""
ÍNDICE DE MÉTODOS DE LISTA:
- append : Agrega un valor al final de la lista.
- insert : Te permite agregar un valor en el índice especifiaco.
- extend : Fusiona una lista (b) con otra lista (a), la list(b) va después de la list(a)
- pop : Elimina un valor pidiendo el índice, además te puede mostrar el vlor del índice.
- remove : Elimina un valor pidiendo ese mismo valor.
- sort : Ordena la lista de forma ascendente, solo si es numérico.
- reverse : Invierte el orden de la lista.
- celar : Elimina todos los valores de la lista, imprime un "None".

FUNCIONES DE LISTAS
- list : Lo transforma en lista.

print("_____________________________________________________________________________________")
"""

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

"""
ÍNDICE DE MÉTODOS DE DICCIONARIO;
- keys : Muestra los keys (claves) del dict.
- values : Muestra los valores del dict, de cada uno de los keys.
- get : Te pide poner el valor de una clave (key) para poder ver el valor (value) de ella.
- pop : Elimina un valor, pero nos pide su clave (key), nos puede mostrar su value.
- items : Es para iterar el dict.
- clear : Elimina todos los elementos o limpia el dict.


print("_____________________________________________________________________________________");

"""




