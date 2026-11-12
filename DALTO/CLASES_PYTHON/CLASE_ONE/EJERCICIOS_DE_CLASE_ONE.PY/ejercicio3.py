"""Juan quiere saber la fecha de un día cualquiera,  pero que sea válida (cualquier año), el va a introducir el número y tiene que salir:
día de mes del año"""

#Resolución:
dia = int(input("Ingrese el día por favor: "))
mes = int(input("Ingrese el mes por favor: "))
año = int(input("Ingrese el año por favor: "))

lista= [0,"enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

if(not(año%4==0)  and not(mes!=2)):
    print("No es válido esta fecha.")

else:
    print(str(dia) + " de " + str(lista[mes]) + " del " + str(año) )

# ESTE ES UN PROGRAMA BIEN BÁSICO Y CON ERRORES 