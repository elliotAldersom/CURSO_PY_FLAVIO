""" 
Vamos a abrir el archivo con permisos de edición
Para ellos en el segundo parámetro (antes del encoding= "UFT-8")
Colocamos el "w" --> Siginfica write, nos das permiso de escritura.
Con este permiso reescribimos el archivo.txt
"""
with open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_TXT\\Mi_Arcivo_TXT.txt","w", encoding= "UTF-8") as archivo:
    
    # Sobreescribiendo o reescribiendo el archivo:
    #archivo.write("Estoy reescribiendo el archivo.txt con \"archivo.write()\"")

    # Sobreescribe, y si hacemos varias veces esto, se acumulan
    archivo.writelines(["Hola bro, estoy usando el \"archivo.writelines()\"\n","Esto nos pide un iterable, te recomiendo usar una lista\n","Bueno espero esté bien va?\n"])
    archivo.writelines(["Hola bro, no te olvides de tomar \"agüita\"\n","Espero estés bien\n","DIOS te bendiga bro"])
    
    