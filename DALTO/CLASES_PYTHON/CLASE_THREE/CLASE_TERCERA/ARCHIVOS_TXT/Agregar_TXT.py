""" 
Vamos a agregar al archivo.txt más texto
y esto lo hacemos dando el permiso de escritura pero con 
append en este caso en vez del "w" , pasamos el "a" .

podemos usar el --> write o writelines
"""

#Pedimos al usuario para que agregue más contenido
agregar = input("Ingresa lo que quieres agregar a tu archivo TXT: ")
with open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_TXT\\Mi_Arcivo_TXT.txt","a", encoding= "UTF-8") as archivo:
    
    # Agregando al archivo con el modo "a", esto agrega todas las veces que lo hagamos correr
    archivo.write("\nEstoy agregando esto al archivo.txt con \"archivo.write()\", pero le di el permiso \"a\"")
    archivo.write("\nHola\n")
    
    # Usando un bucle para agregar varias líneas
    for i in range(5):
        archivo.write(f"Estoy agregando con el bucle for, la línea {i+1} \n")

    # Agregando el al archivo mediante la función input()
    archivo.write(agregar) 

    


    