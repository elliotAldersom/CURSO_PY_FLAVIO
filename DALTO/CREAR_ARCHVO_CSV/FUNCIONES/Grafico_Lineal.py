
import pandas as pd

def Lineal(df):
    import matplotlib.pyplot as plt

    columnas_disponibles = list(df.columns[1:])

    

    # Elegir eje X
    while True:
        try:
            # Mostrar columnas disponibles
            print("📌 Columnas disponibles:", columnas_disponibles)
            eje_x = input("👉 Ingrese el nombre de la columna que desea usar para el eje X: ").strip().capitalize()
            if eje_x in columnas_disponibles:
                columnas_disponibles.remove(eje_x)
                break
            else:
                print("❌ Columna inválida. Intente nuevamente...")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Opción no válida. Intente nuevamente...")

    

    # Elegir columnas para el eje Y
    columnas_y = []
    while True:
        try:
            # Mostrar columnas disponibles
            print(f"🟡 Columnas disponibles para el eje Y (sin '{eje_x}'): {columnas_disponibles}")
            columna = input("🎯 Ingrese el nombre de una columna para el eje Y (escriba 'FIN' para terminar): ").strip().capitalize()
            if columna.upper() == "FIN":
                break
            elif columna in columnas_disponibles:
                columnas_y.append(columna)
                columnas_disponibles.remove(columna)
                print(f"✅ '{columna}' agregado. Restantes: {columnas_disponibles}")
            else:
                print("⚠️ Columna inválida o ya usada. Intente otra.")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Opción no válida. Intente nuevamente...")

    if not columnas_y:
        print("🚫 No se seleccionaron columnas válidas para el eje Y.")
        return

    # Construcción del gráfico de líneas
    x = df[eje_x]

    for col in columnas_y:
        plt.plot(x, df[col], marker='o', label=col)

    plt.xlabel(eje_x)
    plt.ylabel("Valores")
    plt.title("📈 Gráfico Lineal Múltiple")
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
Lineal(df)
"""