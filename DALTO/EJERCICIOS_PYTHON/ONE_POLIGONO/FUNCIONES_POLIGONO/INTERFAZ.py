def Interfaz():
    while True:
        try:
            opcion = input('''
Bienvnido a la calculadora de área de polígonos.
En este programa puedes hallar las áreas de los siguientes polígonos:
- 1) Cuadrado
- 2) Rectángulo
- 3) Triángulo
- 4) Salir

Por favor ingrese la opción que desee (ingrese el número o nombre): ''')
        except KeyboardInterrupt:
            print("\nOpción no válida")
        else:
            return (opcion.strip()).lower()