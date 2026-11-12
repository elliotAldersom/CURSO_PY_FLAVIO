import pandas as pd

def Barras(df):
    
    import matplotlib.pyplot as plt

    columnas_disponibles = list(df.columns[1:])

    
    # Selección de columna para eje X
    while True:
        try:
            # Mostrar columnas disponibles
            print("📌 Columnas disponibles:", columnas_disponibles)
            eje_x = input("👉 Ingrese el nombre de la columna que desea usar para el eje X: ").strip().capitalize()
            if eje_x in columnas_disponibles:
                print("✅ Columna seleccionada correctamente...")
                columnas_disponibles.remove(eje_x)  # Ya no disponible
                break
            else:
                print("❌ Columna inválida. Intente nuevamente...")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Opción no válida. Intente nuevamente...")

    

    # Selección de columnas para eje Y
    columnas_y = []
    while True:
        try:
            # Mostrar columnas disponibles
            print(f"🟡 Columnas disponibles para el eje Y (sin '{eje_x}'): {columnas_disponibles}")
            columna = input("🎯 Ingrese el nombre de una columna para el eje Y (escriba 'FIN' para terminar): ").strip().capitalize()
            if columna== "Fin":
                break
            elif columna in columnas_disponibles:
                columnas_y.append(columna)
                columnas_disponibles.remove(columna)  # Eliminar para evitar repetir
                print(f"✅ '{columna}' agregado. Restantes: {columnas_disponibles}")
            else:
                print("⚠️ Columna inválida o ya usada. Intente otra.")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Opción no válida. Intente nuevamente...")

    if not columnas_y:
        print("🚫 No se seleccionaron columnas válidas para el eje Y.")
        return

    # Construcción del gráfico
    x = df[eje_x]
    ancho = 0.8 / len(columnas_y)

    for i, col in enumerate(columnas_y):
        plt.bar([p + i*ancho for p in range(len(x))], df[col], width=ancho, label=col)

    plt.xticks([p + ancho*(len(columnas_y)-1)/2 for p in range(len(x))], x, rotation=45)
    plt.xlabel(eje_x)
    plt.ylabel("Valores")
    plt.title("📊 Gráfico de Barras Múltiples")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)
Barras(df)
"""