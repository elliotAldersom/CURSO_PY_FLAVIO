import os
import tkinter as tk
from tkinter import filedialog

def Seleccionar_carpeta_para_guardar():
    """
    Abre un cuadro de diálogo para que el usuario seleccione una carpeta donde guardar el archivo.
    Maneja interrupciones y entradas inválidas sin detener el programa.
    """
    while True:
        try:
            # Inicializar tkinter para usar el cuadro de diálogo
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de tkinter

            # Abrir cuadro de diálogo para seleccionar una carpeta
            carpeta_seleccionada = filedialog.askdirectory(title="Selecciona la carpeta donde guardar el archivo")
            
            if carpeta_seleccionada:  # Si el usuario seleccionó una carpeta
                print(f"\n📂 Carpeta seleccionada: {carpeta_seleccionada}")
                
                # Confirmación para guardar en la carpeta seleccionada
                while True:
                    try:
                        confirm = input("¿Desea guardar el archivo en esta carpeta? (SI/NO): ").strip().upper()
                        if confirm in ("SI", "S", "SÍ"):
                            print(f"✅ Carpeta '{carpeta_seleccionada}' seleccionada correctamente.")
                            return carpeta_seleccionada  # Devolver la ruta de la carpeta seleccionada
                        elif confirm in ("NO", "N"):
                            print("🔄 Vamos a seleccionar una nueva carpeta...")
                            break  # Volverá a mostrar el cuadro de diálogo para elegir otra carpeta
                        else:
                            print("⚠️ Opción inválida. Escriba SI o NO.")
                    except (KeyboardInterrupt, EOFError):
                        print("\n⚠️ Entrada inválida. Intente nuevamente...")
                        continue
            else:
                print("⚠️ No se seleccionó ninguna carpeta. Intente de nuevo...")
                continue  # Si no se seleccionó ninguna carpeta, vuelve a intentar

        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Entrada inválida. Intente nuevamente...")
            continue

# Ejemplo de uso:
# Esta función seleccionará la carpeta donde guardar el archivo
#carpeta_destino = Seleccionar_carpeta_para_guardar()
#print(f"Carpeta destino: {carpeta_destino}")
