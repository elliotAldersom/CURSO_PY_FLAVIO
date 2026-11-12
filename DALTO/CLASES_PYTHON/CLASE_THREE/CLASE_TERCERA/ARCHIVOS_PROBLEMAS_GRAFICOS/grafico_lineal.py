import pandas as pd 
# Importamos una libreia: matplotlib
# Es una libreía de visualización de datos de forma gráfica
# Pero vamos a acceder a pylot, entonces hacemos: 
import matplotlib.pyplot as plt

# También importamos seaborn 
# Es una libreia de gráficos estadísticos
import seaborn as sns

df = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_PROBLEMAS_GRAFICOS\\grafico_lineal.csv")

print(df)

# Vamos a crear un gráfico de líneas:
""" 
sns.lineplot(x="fecha", y="comidas",data= df)
- Le pasamos el parámetro que tendremos en x (fecha)
- Le pasamos el parámetro que tendremos en y (comidas)
- Le pasamos el dataframe que vamos a utilizar (df)
"""
# Creando el gráfico
sns.lineplot(x="fecha", y="comidas",data= df)

# Creando un punto en el momento que más se comió
plt.plot("01-03", 17 ,"o") # Este es un punto, en la fecha que le pasemos, para resaltarlo

# Mostranod el gráfico
plt.show() 