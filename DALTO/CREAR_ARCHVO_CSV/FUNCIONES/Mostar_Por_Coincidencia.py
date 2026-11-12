"""
Mostrar datos por coincidencia
""" 

import pandas as pd

def Mostrar_Coincidencias(df):
    while True:
        try:
            # Excluir la columna 'ID' de las opciones para búsqueda
            columnas = [col for col in df.columns if col != 'ID']
            print(f"Estas son las columnas disponibles para búsqueda:\n{', '.join(columnas)}")
            
            # El usuario selecciona la columna por la que desea hacer la búsqueda
            columna_seleccionada = input("Ingrese el nombre de la columna en la que desea buscar: ").strip().title()
            
            if columna_seleccionada not in columnas:
                print("⚠️ Columna no válida. Intente nuevamente...")
                continue  # Si la columna no existe, continuar con el bucle

            # Bucle para asegurar que el usuario ingrese un valor válido
            while True:
                # Mostrar los valores de la columna seleccionada (todos los valores, no solo únicos)
                valores = df[columna_seleccionada]
                print("OJO: Este sistema te busca todas las coincidencias que contengan lo que usted busque.\nPor decir si ingresa un nombre como Juan\nSe le mostrará todos los datos que contengan Juan por decir:\nSan juan , Juan Ramirez\nY si busca números, si busca el 0 ingrese 0.0\nSi no se mostrará todos los que terminen en 0")
                print(f"Valores en la columna '{columna_seleccionada}':\n{', '.join(map(str, valores))}")

                try:
                    # El usuario elige un valor para hacer la búsqueda
                    valor_buscado = input(f"Ingrese el valor que desea buscar en la columna '{columna_seleccionada}': ").strip().lower()  # Convertimos a minúsculas

                    # Verificar si hay coincidencias con el valor ingresado (insensible a mayúsculas/minúsculas)
                    registros_coincidentes = df[df[columna_seleccionada].astype(str).str.contains(valor_buscado, case=False, na=False)]  # Búsqueda insensible a mayúsculas

                    if registros_coincidentes.empty:
                        print("❌ No se encontraron registros que coincidan con el valor ingresado. Intente nuevamente...")
                    else:
                        # Si hay coincidencias, mostrar los registros
                        print(f"\nRegistros que coinciden con '{valor_buscado}' en la columna '{columna_seleccionada}':")
                        print(registros_coincidentes.to_string(index=False))
                        break  # Salir del bucle si los registros son encontrados

                except (KeyboardInterrupt, EOFError, ValueError):
                    print("⚠️ Entrada inválida. Intente nuevamente...")

            break  # Salir del bucle principal si todo está correcto

        except (KeyboardInterrupt, EOFError, ValueError):
            print("\n⚠️ Entrada inválida. Intente nuevamente...")

"""
# Ejemplo de uso con un DataFrame de ejemplo
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada", "Flavio", "Flavio Silva", "Flavio silva"],
    "Pecho": [0.0, 4.0, 1.0, 2.0, 0.0, 0.0, 1.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0, 2.0, 1.0, 2.0]
}
df = pd.DataFrame(data)

# Llamamos a la función para mostrar los datos por coincidencia
print(Mostrar_Coincidencias(df))
"""