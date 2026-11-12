print("""REGISTRO DE CONTRASEÑA
LA CONTRASEÑA DEBE DE CONTENER SÍMBOLOS ESPECIALES Y DEBE DER MAYOR A 8 DIGITOS      
""");
registro = input("REGISTRE CONTRASEÑA:\n");

simbolos = {"!","#","$","%","&","/","(",")","=","?","¿","¡","@"}
R1 = set(registro);

if(len(registro) >=8):
   if(R1.isdisjoint(simbolos) == False):
      print("La contraseña contiene simbolos especiales");
      print("Por lo tanto, su contraseña es segura");
      confir = input("CONFIRME SU CONTRSEÑA:\nPARA REGISTRARLA A SU CUENTA.\n")
      if(confir == registro):
              print("La contraseña ha sido registrada con éxito");
      else:
              print("La contraseña no coincide");
   else:
       print("La contraseña no contiene simbolos especiales");
       print("Por lo tanto, su contraseña no es segura");
else:
     print("La contraseña no cumple con la longitud requeridad");