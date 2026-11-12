import pandas as pd

def Bigotes(df):
    import matplotlib.pyplot as plt

    # Filtra solo columnas numéricas
    columnas_disponibles = df.select_dtypes(include=["int", "float"]).drop(columns=["ID"], errors="ignore").columns.tolist()

    

    columnas_y = []

    while True:
        try:
            print("📌 Columnas disponibles (solo numéricas):", columnas_disponibles)
            columna = input("🎯 Ingrese el nombre de una columna para graficar (escriba 'FIN' para terminar): ").strip().capitalize()
            if columna == "Fin":
                break
            elif columna in columnas_disponibles:
                columnas_y.append(columna)
                columnas_disponibles.remove(columna)
                print(f"✅ '{columna}' agregado. Quedan: {columnas_disponibles}")
            else:
                print("⚠️ Columna inválida, ya usada o no numérica. Intente otra.")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Opción no válida. Intente nuevamente...")

    if not columnas_y:
        print("🚫 No se seleccionaron columnas válidas para el gráfico.")
        return

    # Gráfico de caja con tick_labels
    plt.boxplot([df[col] for col in columnas_y], tick_labels=columnas_y)
    plt.title("📊 Gráfico de Caja (Bigotes)")
    plt.ylabel("Valores")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Ejemplo
"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)
Bigotes(df)
"""




