# Pedir al usuario el nombre del archivo
nombre_archivo = input("Ingrese el nombre del archivo (incluyendo la extensión .txt): ")

# Crear o abrir el archivo para agregar texto
with open(nombre_archivo, 'a') as archivo:  # 'a' para abrir en modo de agregar texto
    while True:
        texto = input("Ingrese el texto que desea agregar al archivo (o escriba 'salir' para terminar): ")
        
        # Si el usuario escribe 'salir', terminamos el bucle
        if texto.lower() == 'salir':
            break
        
        # Escribir el texto en el archivo
        archivo.write(texto + '\n')  # Agrega el texto con una nueva línea

print(f"El texto ha sido agregado al archivo {nombre_archivo}.")
