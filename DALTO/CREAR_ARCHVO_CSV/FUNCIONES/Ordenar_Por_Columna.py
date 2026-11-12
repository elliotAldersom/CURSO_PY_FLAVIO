""" 
Función para ordenar por columna ascendente y descendete o por orden alfabético
"""
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import sys 

# Importación de la función Seleccionar_carpeta_para_guardar desde tu código
sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Guardar_En_Carpeta import Seleccionar_carpeta_para_guardar as Guardar_En_Carpeta

def Ordenar_Y_Guardar(df):
    try:
        # Solicitar orden de columna (alfabético o numérico)
        while True:
            try:
                opcion = input("¿Desea ordenar por alfabético (1) o numérico (2)? Ingresa 1 o 2: ").strip()
                if opcion == '1' or opcion == '2':
                    opcion = int(opcion)  # Convertir la opción a número entero
                    break
                else:
                    print("⚠️ Opción no válida. Debe ingresar 1 para alfabético o 2 para numérico.")
            except (ValueError, KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada inválida. Por favor ingrese un número válido (1 o 2).")

        # Filtrar las columnas alfabéticas o numéricas
        if opcion == 1:
            columnas = [col for col in df.columns if df[col].dtype == 'O']  # Alfabético (cadenas)
        elif opcion == 2:
            columnas = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]  # Numérico

        

        # El usuario elige la columna a ordenar
        while True:
            try:
                print(f"Estas son las columnas disponibles para ordenar:\n{', '.join(columnas)}")
                columna = input("Ingrese el nombre de la columna que desea ordenar: ").strip()

                # Comparamos sin considerar mayúsculas/minúsculas
                if columna.lower() in [col.lower() for col in columnas]:
                    columna = [col for col in columnas if col.lower() == columna.lower()][0]  # Encontrar el nombre correcto de la columna
                    break
                else:
                    print("⚠️ Columna no válida. Intente nuevamente...")
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada interrumpida. Volviendo a solicitar el nombre de la columna...")
                continue

        # El usuario elige el orden (ascendente o descendente)
        while True:
            try:
                orden = input("¿Desea ordenar ascendentemente (1) o descendentemente (2)? Ingresa 1 o 2: ").strip()
                if orden == '1':
                    df = df.sort_values(by=columna, ascending=True)
                    break
                elif orden == '2':
                    df = df.sort_values(by=columna, ascending=False)
                    break
                else:
                    print("⚠️ Opción no válida. Debe ingresar 1 para ascendente o 2 para descendente.")
            except (ValueError, KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada inválida. Por favor ingrese un número válido (1 o 2).")

        # Mostrar el DataFrame ordenado
        print(f"\nDatos ordenados por '{columna}' en orden {'ascendente' if orden == '1' else 'descendente'}:")
        print(df.to_string(index=False))

        # Preguntar si se desea guardar una copia del archivo
        while True:
            try:
                confirm = input("¿Desea guardar una copia del archivo? (SI/NO): ").strip().upper()
                if confirm in ["SI", "S", "SÍ"]:
                    # Seleccionar carpeta para guardar
                    carpeta_destino = Guardar_En_Carpeta()

                    # Pedir al usuario un nombre para la copia
                    while True:
                        nombre_copia = input("Ingrese el nombre para la copia del archivo: ").strip()
                        
                        # Verificar que el nombre no sea igual al original
                        if nombre_copia == "archivo_original.csv":
                            print("⚠️ El nombre no debe ser igual al archivo original. Intente de nuevo...")
                            continue
                        
                        # Reemplazar los espacios por guiones bajos y formatear el nombre
                        nombre_copia = nombre_copia.replace(" ", "_").title()

                        # Confirmar el nombre del archivo
                        confirm_nombre = input(f"¿Está seguro de que el nombre es '{nombre_copia}'? (SI/NO): ").strip().upper()
                        if confirm_nombre in ["SI", "S", "SÍ"]:
                            break
                        elif confirm_nombre in ["NO", "N"]:
                            continue

                    # Guardar la copia del archivo
                    archivo_destino = os.path.join(carpeta_destino, f"{nombre_copia}.csv")
                    df.to_csv(archivo_destino, index=False)
                    print(f"✅ La copia ha sido guardada correctamente en '{archivo_destino}'")
                    break
                elif confirm in ["NO", "N"]:
                    print("❌ No se guardó ninguna copia.")
                    break
                else:
                    print("⚠️ Opción no válida. Escriba SI o NO.")
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada inválida. Intente nuevamente...")

    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
"""
# Ejemplo de uso
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}

df = pd.DataFrame(data)
Ordenar_Y_Guardar(df)
"""