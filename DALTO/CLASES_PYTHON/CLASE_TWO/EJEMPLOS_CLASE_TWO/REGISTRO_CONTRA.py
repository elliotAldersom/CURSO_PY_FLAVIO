print("QUE TAL, BIENVENIDO AL SISTEMA DE UNIVERSE COMPANY.")

name = input("Antes de que genere su contraseña, ingrese su nombre (von su primer apellido):\n");
simbolos = set(["@","!","¡","#","$","&","/","(",")","=","?","¿",">","<"])
print("Muy bien " + str(name) + ", ahora creemos tu contraseña.");

longitud = int(input("Ingresa la longitud que deseas que sea tu contraseña: "));

contra = input("Registra tu contraseña para saber si puede ser valida para el registro, usa símbolos especiales: ");
seting = set(contra);

while True:
    if(len(contra) >= longitud):
        if(seting.isdisjoint(simbolos) == False):
            print("Contraseña ingresada valida para el registro\nAhora vamos a confrimarla.");

            while True:
                confirmar = input("Confirme su contraseña para el registro en el sistema: ");
                if(confirmar == contra):
                    print("Contraseña registrada con exito.\nPor favor no se olvide que esta contraseña es necesaria para su asistencia en el trabajo");
                    break;
                else:
                    print("Confirmación incorrecta, vuelve a intentarlo.")
            break
        else:
            print("La contraseña no cumple con los símbolos requeridos.");
    else:
        print("La contraseña no cumple con la longitud requerida.");