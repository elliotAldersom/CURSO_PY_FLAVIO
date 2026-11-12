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
print("EL TEXTO DADO SIN ESPACIOES SE VE ASÍ:\n" + str(reemplazo));

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