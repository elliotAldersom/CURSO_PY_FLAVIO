
numero_1=numero_2=numero_3=10   #  valor cualquiera que se utiliza para que el bucle while funcione

while((numero_1==numero_2  or numero_1==numero_3  or numero_2==numero_3)):
     numero_1=float(input("INGRESE EL PRIMER NÚMERO:   "))
     numero_2=float(input("INGRESE EL SEGUNDO NÚMERO:   "))
     numero_3=float(input("INGRESE EL TERCER NÚMERO:   "))

if (numero_1> numero_2> numero_3):
     print(str(numero_1)+ " > "+ str(numero_2)+ " > "+ str(numero_3))
    
elif(numero_1>numero_3>numero_2):
     print(str(numero_1)+ " > " + str(numero_3)+ " > " + str(numero_2))

elif(numero_2 > numero_3 > numero_1):
     print(str(numero_2)+ " > " + str(numero_3) + " > " + str(numero_1))

elif(numero_2 > numero_1 > numero_3):
     print(str(numero_2)+ " > "+ str(numero_1)+ " > " + str(numero_3))

elif(numero_3 > numero_2 > numero_1):
     print(str(numero_3)+ " > " + str(numero_2) + " > " + str(numero_1))
   
elif(numero_3 > numero_1 > numero_2):
     print(str(numero_3)+ " > " + str(numero_1) + " > " + str(numero_2))
