dato = "Pepito es un pepe feliz";

print(dato);
rango = dato[0:2];
print("Acá vemos los caracteres según el rango dado en el sistema: "+ str(rango));

#______________________________________________________________________________________

nombre = input("Ingresa tu nombre: ")
contador = len(nombre);
print("Tu nombre tiene " + str(contador) + " caracteres.")

escoger = int(input("Ingresa que número de caracter deseas mostrar: "));
print( "Esto son los caracteres que se muestran: " + nombre[0:escoger]);