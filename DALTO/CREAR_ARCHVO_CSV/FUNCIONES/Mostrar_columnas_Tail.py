""" 
Mostrar registros de abajo hacia arria (usted ingresa el número)
"""
import pandas as pd
def Mostrar_Con_Tail(df):
    while True:
        try: 
            n_filas_columnas = df.shape
            n_filas = n_filas_columnas[0]
            print("Bienvenido, ahora vamos a pedirte que ingreses el número de registros (filas) que quieres ver\nempezando de abajo hacia arriba.")
            num = int(input(f"Ingrese el número de filas que quiere ver (usted tiene {n_filas} filas): "))
           
            if num in range(1,n_filas+1):
                print("Número de filas ingresado es válido")
                break
            else:
                print(f"El número de filas ingresadas debe estar entre 1 y {n_filas}. Intente nuevamente.")
                continue
        except (KeyboardInterrupt, ValueError, EOFError):
            print("\nPor favor ingrese un número de filas para continuar...")
            
    # Mostrar el número de filas desde arriba hacia abajo:
    result = df.tail(num).to_string(index=False)
    return f"Estas son las filas que usted pidió (emepzando de abajo hacia arria):\n{result}"

"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)
print(Mostrar_Con_Tail(df))
"""

"""
id_result =(df.iloc[3,:])
print(id_result.to_frame().T.to_string(index=False))
"""
