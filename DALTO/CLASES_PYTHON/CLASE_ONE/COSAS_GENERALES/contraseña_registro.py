name = input("INGRESE SU NOMBRE DE USUARIO: ");
contrasena = input("Ingrese su contraseña \n" + "La contraseña debe ser mayor a 8 digitos y tener diversos signos: \n");

signos = {"!","@","#","%","^","&","*","_" , "/"} ;

if (len(contrasena) >= 8):
    if (set(contrasena) & signos):
      print("Contraseña válida: cumpe con la longitud requerida y el uso de signos.");
      confirmacion= input("AHORA VUELVE A INSERTAR LA CONTRASEÑA PARA CONFIRMARLA:\n")
      if (contrasena == confirmacion):
         print("CONFIRMACIÓN EXITOSA")
      else:
         print("La contraseña no coincide, por favor vuelva a intentarlo.");
    else:
        print("La contraseña no cumpke con el formato requerido de usos de signos.");
else:
   print("La contraseña no cumple con la longitud requerida.");


