clave=(input("Ingrese la clave del sistema: "))
intentos=int(input("Ingrese el numero de intentos: "))
i=0
while(i<intentos):
 
   i=i+1    #contador
   prueba=input("Ingresa la contraseña, por favor: ")
   if(prueba==clave):  #determinar si son iguales
      print("contrseña correcta!!")
      print("BIENVENIDO AL SISTEMA!!")
      break

if(i==intentos):
   print("Lo siento, ha agotado los intentos, el sistema se cerrará")
