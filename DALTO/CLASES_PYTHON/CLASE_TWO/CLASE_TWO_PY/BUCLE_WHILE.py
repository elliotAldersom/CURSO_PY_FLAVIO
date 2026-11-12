"""
ESTE BUCLE WHILE, ES UNA SENTENCIA QUE NOS PERMITE EJECUTAR UN CÓDIGO VARIAS VECES,
A DIFERENCIA DEL BUCLE FOR, ESTE BUCLE SE EJECUTARÁ SIEMPRE Y CUANDO UNA CONDICIÓN 
SEA VERDADERA (TRUE)

"""

contador = 0

# MIENTRAS LA CONDICIÓN SE CUMPLA (TRUE), SE VA A EJECUTAR:
while contador <10: 
    contador +=1
    print(contador)
    
print("El while llegó a su fin.");


print("\nREGISTRO DE CONTRASEÑA\n")

usuario = input("Ingrese el nombre de usuario: ");
usuario = (usuario.strip()).capitalize()
print(f"tu nombre de usaurio es {usuario}")
longitud = int(input("Ingresa la longitud que deseas que sea el mínimo de tu contraseña: "));
simbolos = set(["@","!","¡","#","$","&","/","(",")","=","?","¿",">","<"])

while True:
  registro = input("Ingresa tu contraseña para registrar: ");
  registro_set = set(registro)

  if(len(registro) >= longitud):
     if(registro_set.isdisjoint(simbolos) == False):
          print("Contraseña ingresada valida.")
          print("Ahora confirmemos tu contraseña para registrar.")
          while True:
              confirmado = input("Confirma tu contraseña para registrarla de una vez: ");
              if(registro == confirmado):
                print("Contraseña registrada con éxitio, bienvenido al sistema "  +str(usuario));
                break 
              else:
               print("Contraseña no coincide, vuelva a intentarlo.");
          break
     else:
        print("La contraseña no cumple con los requisitos necesarios.");
  else:
     print("La contraseña no cumple con la longitud mínima que pusiste, la cual es de " + str(longitud) + " caracteres.");


print("\nInicio de sesión en el sistema\n");

print("A continuación vamos a pedir que valides tu nombre de usuario:)");

while True:
   nombre = input("Ingresa tu nombre de usuario para validarlo: ");
   if(nombre == usuario):
      print("Bienvenido al sistema " + str(usuario) + "\nAhora necesitamos que ingreses tu contraseña:)")
      i = 0
      while i < 5:
         confirmar_contraseña = input("Ingresa tu contraseña para inciar sesión en el sistema: ");
         if(confirmar_contraseña == registro):
            print("Contraseña correcta.\nBienvenido a tu cuenta " + str(usuario) + ".");
            break
         else:
            i += 1
            print("Contraseña invalida, te quedan " + str(5 - i) + " intentos")
      break
   else:
      print("Nombre de usuario no registrado, intenta de nuevo.")

if(i == 5):
   print("Intento agotados, no puedes ingresar, vuelve a abrir la página.")


