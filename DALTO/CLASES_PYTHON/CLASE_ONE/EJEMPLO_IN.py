while True:
    try:
        print("Asignaturas acturales:\nSoftware\nInformática\nMatemáticas")
        asignatura = input("Ingrese su asigntura: ")
        asignatura = (asignatura.strip()).capitalize()

        if (asignatura in ["Software", "Informática","Informatica","Matemáticas","Matematicas"]):
            print(f"Asignatura correcta: {asignatura}")
            break
        else: 
            print("Asignatura incorrecta")
            continue
    except KeyboardInterrupt:
        print("\nESE CARACÁCTER NO ES    VÁLIDO\n") 
    except EOFError: # POR SI ALGUIEN INGRESA CONTROL + Z
        print("\nESE CARÁCTER NO ES VÁLIDO\n")
     