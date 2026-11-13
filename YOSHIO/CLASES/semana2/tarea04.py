password = 'python123'
intentos = 3

while (intentos >0): 
    input_password = input("Ingrese la contraseña: ")
    if(input_password == password):
        print("Contraseña correcta...\nIniciando Sesión...\nBienvenido al sistema...")
        break 

    intentos -= 1
    print(f"Contraseña incorrecta. {intentos} restanes...")