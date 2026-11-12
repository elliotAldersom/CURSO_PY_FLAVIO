
def Interfaz_Consulta():
    while True:
        try:
            opcion = int(input("""
Bienvenido a su apartado de consultas de su archivo CSV
estas son las opciones:

1- Mostrar todos los datos                  
2- Mostrar una columna
3- Mostrar más de una columna
4- Mostrar registros de arriba hacia abajo (usted ingresa el número)
5- Mostrar registros de abajo hacia arriba (usted ingresa el número)
6- Mostrar los datos de un registro (filas) por ID
7- Mostrar los datos por coincidencia
8- Ordenar los datos por la columna que pase (mayor a menor o menor a mayor)
9- Sumar datos de una o más e incluso todas las columnas numéricas
10- Salir

Por favor ingrese la opción en número: """))
            if opcion == 1:
                return 1
            elif opcion == 2:
                return 2
            elif opcion == 3:
                return 3
            elif opcion == 4:
                return 4
            elif opcion == 5:
                return 5
            elif opcion == 6:
                return 6
            elif opcion == 7:
                return 7
            elif opcion == 8:
                return 8
            elif opcion == 9:
                return 9
            elif opcion == 10:
                return 10
            else:
                print("Opción no válida, por favor ingrese una opción válida")
                continue
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nOpción no válida, por favor ingrese una opción válida...")
            
#print(Interfaz_Consulta())