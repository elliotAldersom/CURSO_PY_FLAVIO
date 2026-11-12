import pandas as pd 
# Importamos una libreia: matplotlib
# Es una libreía de visualización de datos de forma gráfica
# Pero vamos a acceder a pylot, entonces hacemos: 
import matplotlib.pyplot as plt

# También importamos seaborn 
# Es una libreia de gráficos estadísticos
import seaborn as sns

df = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_PROBLEMAS_GRAFICOS\\grafico_barras.csv")

print(df)

# Vamos a crear un gráfico de barras:
""" 
sns.barplot(x="fuente", y="ingresos",data= df)
- Le pasamos el parámetro que tendremos en x (fuente)
- Le pasamos el parámetro que tendremos en y (ingresos)
- Le pasamos el dataframe que vamos a utilizar (df)
"""
# Creando el gráfico
sns.barplot(x="fuente", y="ingresos",data= df)

# Vamos a hallar el total de ingresos:
total_ingresos = df["ingresos"].sum() # --> sum, acá es un método que suma todos los datos de la columna que pasemos

# Mostrando el total de ingresos:
print(f"El total de ingresos es: {total_ingresos} USD")

# Mostranod el gráfico
plt.show() 