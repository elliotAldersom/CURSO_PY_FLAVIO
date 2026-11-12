def Interfaz():
    while True:
        try:
            opcion = input("""
Bienvenido a la interfáz de gráficos para tu archivo CSV,
estos son los gráficos que puedes realizar: 
1- Gráfico de barras
2- Gráfico lineal
3- Gráfico de dispersión
4- Gráfico de bigote 
5- Gráfico circular
6- Consultar
7- Salir

Por favor ingrese una de las opciones (número o nombre): """).strip().lower()
            if opcion in ['1', 'gráfico de barras', 'barras', 'grafico de barra']:
                return "1"
            elif opcion in ['2', 'gráfico lineal', 'lineal', 'grafico lineal']:
                return "2"
            elif opcion in ['3', 'gráfico de dispersión', 'dispersion', 'grafico de dispersion']:
                return "3"
            elif opcion in ['4', 'gráfico de bigote ', 'bigote' , 'grafico de bigote']:
                return "4"
            elif opcion in ['5', 'gráfico circular ', 'circular' , 'grafico circular']:
                return "5"
            elif opcion in ["6", "consultar", "consultar datos", "consulta"]:
                return "6"
            elif opcion in ['7', 'salir', 'cerrar']:
                return "7"
            else: 
                print("Opción no válida")
                continue
        except KeyboardInterrupt:
            print("\nOpción no válida")
        except EOFError:
            print("Opción no válida")
            
#print(Interfaz())
                