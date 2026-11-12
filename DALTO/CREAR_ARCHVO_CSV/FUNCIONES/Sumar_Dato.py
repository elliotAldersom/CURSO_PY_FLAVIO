""" 
Sumar datos de una o más e incluso todas las columnas numéricas
"""

import pandas as pd

def Sumar_Columnas(df):
    try:
        # Filtrar las columnas numéricas y excluir la columna 'ID'
        columnas_numericas = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != 'ID']
        
        while True:
            try:
                # Mostrar las columnas numéricas disponibles
                print(f"Estas son las columnas numéricas disponibles para sumar:\n{', '.join(columnas_numericas)}")
                
                # Pedir al usuario si desea sumar una columna específica, varias o todas
                opcion = input("¿Desea sumar una columna específica (1), varias columnas (2) o todas las columnas numéricas (3)? Ingresa 1, 2 o 3: ").strip().lower()

                if opcion == '1':
                    # Sumar una columna específica
                    while True:
                        print(f"Estas son las columnas numéricas disponibles para sumar:\n{', '.join(columnas_numericas)}")  # Mostrar columnas disponibles
                        columna = input("Ingrese el nombre de la columna que desea sumar: ").strip().lower()  # Convertir a minúsculas
                        # Compara insensiblemente a mayúsculas/minúsculas
                        if columna in [col.lower() for col in columnas_numericas]:
                            columna_correcta = [col for col in columnas_numericas if col.lower() == columna][0]  # Encuentra el nombre correcto
                            suma = df[columna_correcta].sum()
                            print(f"La suma de la columna '{columna_correcta}' es: {suma}")
                            break
                        else:
                            print("⚠️ Columna no válida. Intente nuevamente...")
                            continue
                    break  # Salir después de sumar una columna específica

                elif opcion == '2':
                    # Sumar varias columnas
                    columnas_seleccionadas = []
                    while True:
                        print(f"Estas son las columnas numéricas disponibles para sumar:\n{', '.join(columnas_numericas)}")  # Mostrar columnas disponibles
                        columna = input("Ingrese el nombre de la columna que desea sumar (FIN para terminar): ").strip().lower()  # Convertir a minúsculas
                        if columna == "fin":
                            break  # Salir cuando el usuario deje en blanco
                        # Excluir las columnas ya seleccionadas
                        if columna in [col.lower() for col in columnas_numericas]:
                            columna_correcta = [col for col in columnas_numericas if col.lower() == columna][0]  # Encuentra el nombre correcto
                            columnas_seleccionadas.append(columna_correcta)
                            columnas_numericas.remove(columna_correcta)  # Eliminar columna seleccionada
                        else:
                            print("⚠️ Columna no válida o ya seleccionada. Intente nuevamente...")
                            continue
                    
                    if columnas_seleccionadas:
                        suma = df[columnas_seleccionadas].sum().sum()
                        print(f"La suma de las columnas seleccionadas ({', '.join(columnas_seleccionadas)}) es: {suma}")
                    else:
                        print("⚠️ No se seleccionaron columnas válidas.")
                    break  # Salir después de sumar las columnas seleccionadas

                elif opcion == '3':
                    # Sumar todas las columnas numéricas
                    suma = df[columnas_numericas].sum().sum()
                    print(f"La suma de todas las columnas numéricas es: {suma}")
                    break  # Salir después de sumar todas las columnas

                else:
                    print("⚠️ Opción no válida. Debe ingresar 1, 2 o 3.")

            except (ValueError, KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada inválida. Intente nuevamente...")

    except Exception as e:
        print(f"\n⚠️ Error inesperado: {e}")

# Ejemplo de uso
"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}

df = pd.DataFrame(data)
Sumar_Columnas(df)
"""