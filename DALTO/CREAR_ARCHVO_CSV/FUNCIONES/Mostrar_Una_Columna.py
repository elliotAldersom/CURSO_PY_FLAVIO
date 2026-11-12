""" 
Acá irá la función para mostrar la columna que el usuario quiera (solo 1)
"""

def Mostrar_Una_Columna(df):
    while True:
        try:
            encabezados =  list(df.head(0))
            pedir =  input(f""" 
Estos son los nombres de los encabezados de tu lista:
{encabezados}
Por favor ingrese el nombre del encabezado del cual desee ver su columna: """).strip()
            if (pedir.title() in encabezados):
               
                return f"Los datos de la columna {pedir.title()} son:\n{df[pedir.title()].to_string(index=False)}"
            elif (pedir.upper() in encabezados):
                return f"Los datos de la columna ID son:\n{df["ID"].to_string(index=False)}"
            else:
                print("Encabezdo no encontrado...")
                continue
        except (KeyboardInterrupt, EOFError,ValueError):
            print("\nOpción no válida...")