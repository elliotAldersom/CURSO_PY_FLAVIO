"""

Escribir un programa que almacene la cadena de caracteres contraseña en una variable,
pregunte al usuario por la contraseña e imprima por pantalla si la contraseña 
introducida por el usuario coincide con la guardada en la variable 
sin tener en cuenta mayúsculas y minúsculas.

"""

name = input("Ingresa tu nombre: ");
name = name.strip();
name = name.capitalize();
print(f"Bienvenido {name}, ahora necesitamos registrar una contraseña:)");

simbolos = {"!", "\"", "#", "$", "%", "&", "/", "(", ")", "=", "?", "¡", "¿", "@", "_", "-"};

longitud = int(input("Ingrese la longitud que desee que tenga su contraseña: "))
print(f"Tenga encuenta el uso de símbolos para la contraseña, la longitud de {longitud} que ingresó:\n {simbolos}");


while True:
    # REGISTRO DE LA CONTRA DEBE DE IR ADENTRO DEL WHILE
    contra = input("Ingrese la contraseña para poder validarla en el registro: ");

    set_contra = set(contra)

    if(len(contra) >= longitud):
        if(not(set_contra.isdisjoint(simbolos))):
            print("La contraseña ingresada cumple con los requisitos solicitados");
            print("Ahora vamos a pedir que confirmes tu contraseña")
            

            while True:
                    valida = input("valida la contraseña: ")
                    if(valida == contra):
                        print(f"{name} tu contraseña es valida y acaba de ser registrada:)")
                        break
                    else:
                        print(f"{name} tu contraseña no coincide con la registrada, vuelve a intentarlo.")
            break
        else:
            print("La contraseña ingresada no cumple con los requisitos solicitados")
    else:
        print("La contraseña ingresada no cumple con la longitud ingresada.")


print("____________________________________________________________")

print("INICIO DE SESIÓN: ")

while True:
     print("Ingrese su nombre de usuario para acceder ")
     usuario = input("Ingrese su nombre de usuario: ")
     if(usuario.capitalize() == name):
          print(f"{name} bienvenido al sistema")

          contador = 0
          while contador < 5:
               inicio_contra = input("Ahora para ingresar, pon tu contraseña para validarla: ")
               if(inicio_contra == contra):
                    print(f"{name} bienvenido al sistema, ya puedes acceder a los datos")
                    break
               else:
                    contador += 1
                    print(f"{name} contraseña no coincide, vuelve a intentarlo, te quedan {5 - contador} veces.")
                    
          break
     else:
          print("Nombre de usuario no registrado, vuelve a intentarlo ")
if(contador == 5):
     print(f"{name} te quedaste sin intentos para ingresar a tu contraseña.")