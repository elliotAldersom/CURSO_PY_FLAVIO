import pandas as pd
import matplotlib.pyplot as plt

def Circular(df):
    try:
        # Excluir "ID" si existe
        columnas_numericas = df.select_dtypes(include=["int", "float"]).drop(columns=["ID"], errors="ignore").columns.tolist()
        columnas_totales = df.columns[1:].tolist()

        

        # Selección de columna categórica (eje X)
        while True:
            try:
                print("📌 Columnas disponibles:", columnas_totales)
                eje_x = input("🎯 Ingrese la columna categórica (para agrupar, eje X): ").strip().capitalize()
                if eje_x in columnas_totales:
                    break
                else:
                    print("❌ Columna inválida. Intente nuevamente...")
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Opción no válida. Intente nuevamente...")

        # Filtrar columnas numéricas distintas al eje_x
        columnas_validas = [col for col in columnas_numericas if col != eje_x]

        if not columnas_validas:
            print("🚫 No hay columnas numéricas disponibles para graficar.")
            return

       

        # Selección de columna de valores (eje Y)
        while True:
            try:
                print("📊 Columnas numéricas disponibles:", columnas_validas)
                valores = input("🔢 Ingrese la columna numérica para los valores del gráfico: ").strip().capitalize()
                if valores not in df.columns:
                    print("❌ La columna no existe. Intente nuevamente.")
                    continue
                elif valores == eje_x:
                    print("⚠️ La columna ya está usada como eje X. Intente otra.")
                    continue
                elif df[valores].dtype not in ["int64", "float64"]:
                    print("🚫 La columna seleccionada no es numérica. Intente otra.")
                    continue
                break
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Opción no válida. Intente nuevamente...")

        # Agrupar y graficar
        datos = df.groupby(eje_x)[valores].sum()
        if datos.empty:
            print("⚠️ No hay datos válidos para graficar.")
            return

        # Gráfico circular
        plt.pie(datos, labels=datos.index, autopct="%1.1f%%", startangle=90)
        plt.title("🟠 Gráfico Circular")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# Ejemplo de prueba
"""
data = {
    "ID": [1, 2, 3, 4],
    "Cliente": ["Flavio silva", "Laureano", "Fabian", "Jessica estrada"],
    "Pecho": [0.0, 4.0, 1.0, 2.0],
    "Encuentro": [1.0, 1.0, 0.0, 0.0]
}
df = pd.DataFrame(data)
Circular(df)
"""