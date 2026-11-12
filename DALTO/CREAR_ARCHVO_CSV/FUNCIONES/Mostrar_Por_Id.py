""" 
Mostrar los datos de un registro (fila) por ID
"""
import pandas as pd
def Mostrar_Por_ID(df):
    while True:
        try:
            datos_ID = df["ID"].to_string(index=False)
            datos_ID_Two = df["ID"]
            list_ID = list(datos_ID_Two)
            print(f"Estos son los ID de su tabla:\n{datos_ID}")
            opcion_id = int(input("Ingrese la opción del ID que desea mostrar: "))
            if opcion_id in list_ID:
                print("Opción válida...")
                break
            else:
                print("ID no regstrado")
                continue
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nPor favor ingrese un ID para continuar con el programa...")
    
    # Mostrar registros del ID seleccionado
    result_ID = df.iloc[(opcion_id-1), :]
    result_final = result_ID.to_frame().T.to_string(index=False)
    return f"Mostrando todos los registros del ID {opcion_id}:\n{result_final}"

"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)

print(Mostrar_Por_ID(df))
"""