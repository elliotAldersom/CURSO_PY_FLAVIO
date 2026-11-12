""" 
Cambiar el tipo de dato de una columna
"""
import pandas as pd 
df = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\EJERCICIOS_ARCHVOS\\archivo.csv")

# Cambiando de int a String (str): Usamos el astype()
df["Edad"] = df["Edad"].astype(str)
print(df["Edad"][0]) #--> Imprime el elemento 0 de la columna Edad
print(type(df["Edad"][0])) #--> Imprime el tipo de elemento 0 de la columna Edad
print(type(df["Edad"])) #--> Imprime el tipo de dato de la columna Edad (<class 'str'>)


""" 
Reemplazar Valores en una Columna 
"""
df["Nombre"] = df["Nombre"].replace("Jorge", "Papango")
print(df["Nombre"])

""" 
Elimnar las columnas con datos faltantes: Esta es la tabla ahora:
Nombre,Apellido,Edad
Flavio,Silva,18.0
Fabian,Silva,21.0
Papango,Estrada,40.0
Flavio,Silva,18.0
Flavio,Silva,18.0
Flavio,Silva,18.0
Carlos,,

"""
# Así falte solo uno, elimina toda la columna
#df = df.dropna(axis=1)
#print(df) #--> Elimina las columnas con datos faltantes 

""" 
Elimina columnas donde todos los valores son NaN
"""
df = df.dropna(axis=1, how='all')  


""" 
Vamos a borrar filas con datos incompletos: Esta es la tabla ahora:

   Nombre Apellido  Edad
0   Flavio    Silva  18.0
1   Fabian    Silva  21.0
2  Papango  Estrada  40.0
3   Carlos      NaN   nan


"""
print(df)
df = df.dropna()
print(f"\n{df}")


""" 
Eliminar las filas repetidas: La tabla es así ahora:

Nombre,Apellido,Edad
Flavio,Silva,18.0
Fabian,Silva,21.0
Papango,Estrada,40.0
Flavio,Silva,18.0
Flavio,Silva,18.0
Flavio,Silva,18.0

"""
df = df.drop_duplicates()
print(df)
# Guardar los cambios realizados en el DataFrame en el archivo.csv:
df.to_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\EJERCICIOS_ARCHVOS\\archivo.csv", index= False, encoding="UTF-8")

