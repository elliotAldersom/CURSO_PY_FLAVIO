contra_registrada = "FlavioGSE13/07"

intentos = 0
max_intentos = 5

while intentos < max_intentos:
    intento = input("Ingresa la contraseña registrada: ");
    if(intento == contra_registrada):
        print("Acceso desbloqueado!!\n¡BIENVENIDO!");
        break # SE CORTA EL BUCLE Y NO SE EJECUTA MÁS.
    else: 
        intentos += 1 # SE SUMA 1 AL CONTADOR DE INTENTOS.
        print("Contraseña incorrecta. Intentos restantes: " + str(max_intentos - intentos) + " intentos")
        

if(intentos == max_intentos):
    print("Has agotado todos los intentos. Acceso denegado.");


