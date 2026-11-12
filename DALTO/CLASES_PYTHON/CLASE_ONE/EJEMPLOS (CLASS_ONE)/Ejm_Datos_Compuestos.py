# tipos de conjuntos o listas:

lista = ["Flavio" , "Gerardo" , "Silva" , "Estrada" , 61088098];
print(lista)
# La lista te permite buscar por el índice y permite cambiar los valores uno por uno.

print(lista[3]);
lista[3] = "ESTRADA"
print(lista)
print("______________________________________________________________________________")


tupla = ("Flavio" , "Gerardo" , "Silva" , "Estrada" , 61088098);
print(tupla)
# no permite cambiar alguno de sus valore de forma individual como la lista, solo cambiar todos los datos o redifinir la variable
print(tupla[3]);
#tupla[3] = "ESTRADA";
#print(tupla[3]) ----> Sale error

tupla = ("Estrada" , "Flavio");
print(tupla) # ---> si se puede
print("______________________________________________________________________________")


set = {"Flavio" , "Gerardo" , "Silva" , "Estrada" , 61088098};
print(set) # Es desordenado, así que no se puede cambiar ningún valor, solo redifinir.
print("______________________________________________________________________________")


diccionario = {
"nombre" : "Flavio" ,
"apellidos" : "Silva Estrada" ,
"DNI" : 61088098 
};
print(diccionario)
print(diccionario['nombre']);
diccionario['nombre'] = "FLAVITO";
print(diccionario)
print("______________________________________________________________________________");
