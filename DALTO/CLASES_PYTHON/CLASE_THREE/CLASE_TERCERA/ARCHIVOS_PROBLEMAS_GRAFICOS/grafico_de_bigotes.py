import pandas as pd 
# Importamos una libreia: matplotlib
# Es una libreía de visualización de datos de forma gráfica
# Pero vamos a acceder a pylot, entonces hacemos: 
import matplotlib.pyplot as plt

# También importamos seaborn 
# Es una libreia de gráficos estadísticos
import seaborn as sns

df = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_PROBLEMAS_GRAFICOS\\grafico_de_bigotes.csv")

print(df)

# Vamos a crear un gráfico de barras:
""" 
sns.barplot(x="categoría", y="valor",data= df)
- Le pasamos el parámetro que tendremos en x (categoría)
- Le pasamos el parámetro que tendremos en y (valor)
- Le pasamos el dataframe que vamos a utilizar (df)
"""
# Creando el gráfico
sns.boxplot(x="categoría", y="valor",data= df)


# Mostranod el gráfico
plt.show() 

