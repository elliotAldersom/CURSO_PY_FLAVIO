""" 
Hacer la función que muestre todos los datos de la tabla
"""

def Datos_Tablas(df):
    return f"Leyendo los datos de la tabla: \n{df.to_string(index=False)}"
    