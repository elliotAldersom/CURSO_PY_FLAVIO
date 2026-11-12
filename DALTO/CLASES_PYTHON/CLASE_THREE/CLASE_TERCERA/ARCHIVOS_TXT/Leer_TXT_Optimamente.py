"""
Haremos lo mismo que en archivos_txt pero más barato 😎
Usamos with open()
with open nos tira menos errores excepciones que open
Vamos a usar el encoding = "UTF-8" 
Para garantizar que lea correctamente los caracteres especiales como acentos.
Aunque mi Python ya los lee correctamente.
"""
with open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_TXT\\Mi_Arcivo_TXT.txt",encoding= "UTF-8") as archivo:
    print("Hola bro..\nEl archivo se leyó correctamente. 😎") # --> Esto se ejecuta si se abrió correctamente el archivo txt 
    
    # Leemos el archivo:
    leido = archivo.read()
    print(leido)
# No es necesario cerrarlo al usar with open

