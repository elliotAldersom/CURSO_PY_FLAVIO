""" 
Acá haremos el código para mostrar más de una sola columna...
"""
import pandas as pd
def Mostrar_Varias_Columnas(df):
    while True:
        try:
            encabezados = list(df.columns.str.title())
            opcion = input("Quieres ver un rango de columnnas (1) o columnas específicas (2): ").strip().lower()
            if opcion in ["1", "rango", "rango de columnas"]:
                while True:
                    try:
                        print(f"Encabezados disponibles:\n{encabezados}")
                        inicio = input("Ingrese el nombre del encabezado que desea que sea el inicio: ").strip().title()
                        if inicio in encabezados:
                            num_inicio = encabezados.index(inicio)
                            print("Encabezado válido")
                            # EXCLUIMOS LA COLUMNA SELECCIONADA:
                            encabezados_restantes = encabezados[:num_inicio] + encabezados[num_inicio+1:]
                            break
                        else:
                            print("No existe esa columna")
                            continue
                    except (KeyboardInterrupt, EOFError,ValueError):
                        print("\nPor favor ingrese una columna válida...")
                while True:
                    try:
                        print(f"Estos son los enabezados restantes:\n{encabezados_restantes}")
                        final = input("Ingrese el nombre del encabezdo hasta donde quiere mostrar: ").strip().title()
                        if final in encabezados_restantes:
                            num_final = encabezados_restantes.index(final)
                            if num_final < num_inicio:
                                print("No puedes seleccionar un encabezado que esté antes del inicio")
                                continue
                            else:
                                print("Encabezado válido")
                                break
                        else:
                            print("No existe esa columna")
                            continue
                    except (KeyboardInterrupt, EOFError,ValueError):
                        print("\nPor favor ingrese una columna válida...")
                
                columnas_seleccionadas = df.iloc[:, num_inicio:(num_final+2)].to_string(index=False)
                return f"Estos son los registros de las columnas selecondas:\n{columnas_seleccionadas}"
            elif opcion in ["2", "columnas específicas", "específicas", "columnas especificas", "especificas"]:
                while True:
                    try:
                        print(f"Esta son los encabezados de las columnas:\n{encabezados}")
                        num = int(input("Ingrese el número de encabezados que desea ver: "))
                        if num > len(encabezados):
                            print("El número no puede ser mayor al número de columnas...")
                            continue
                        elif num <= 0:
                            print("El número no puede ser menor o igual a 0...")
                            continue
                    except (KeyboardInterrupt, EOFError,ValueError):
                        print("\nPor favor ingrese un número válido...")
                    else:
                        print("Número de columnas seleccionada válida...")
                        break
                
                lista_columna = []
                for i in range(1,(num+1)):
                    while True:
                        try:
                            #encabezados = list(df.columns.str.title())
                            print(f"Esta son los encabezados de las columnas:\n{encabezados}")
                            name_colum = input(f"Ingrese el {i} nombre de la columna que desea ver: ").strip().title()
                            if name_colum in encabezados:
                                if name_colum == "Id":
                                    lista_columna.append(name_colum.upper())
                                    encabezados.remove(name_colum)
                                else:
                                    lista_columna.append(name_colum)
                                    encabezados.remove(name_colum)
                                break
                            else:
                                print("Columna no encontrada o ya usada")
                        except (KeyboardInterrupt, EOFError,ValueError):
                            print("\nPor favor ingrese una columna válida...")
                
                # Mostrar las columnas:
                df_seleccionado = df[lista_columna]
                columnas_seleccionadas = df_seleccionado.to_string(index=False)
                return f"Estos son los registros de las columnas seleccionadas:\n{columnas_seleccionadas}"

            else:
                print("Opción no válida, intente de nuevo...")
                continue
        except (KeyboardInterrupt, EOFError,ValueError):
            print("\nPor favor ingrese una opción válida...")
                            


"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)

print(Mostrar_Varias_Columnas(df))
"""