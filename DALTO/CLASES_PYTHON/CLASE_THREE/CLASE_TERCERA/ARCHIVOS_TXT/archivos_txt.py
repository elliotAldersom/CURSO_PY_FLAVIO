"""
¿QUÉ ES UN ARCHIVO?
- UN ARCHIVO ES UN CONTENEDOR DE INFORMACIÓN, EL CUAL ESTÁ EN UN FORMATO;
EL FORMATO ES COMO EN UN LENGUAJE DE PROGRAMACIÓN, UN TIPO DE DATO (STING / INT / ARRAYS / etc..)
- LOS ARCHIVOS TIENEN SU PROPIO TIPO DE DATO:
PNG (IMAGEN) / MP4 (AUDIO Y VIDEO) 
- LOS ARCHIVOS SE COMPONEN EN DOS PARTES: 
NOMBRE Y EL FORMATO

ARCHIVO TXT:
ARCHIVO DE TEXTO PLANO
ES ITERABLE

"""

# Para abrirlo, usamos la función open()
# Dentro de ella ponemos la ruta hasta nuestro archivo.txt 
# Es recomendable tener el archivo txt en la misma carpeta del módulo que estamos usando
archivo_sin_leer =  open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_TXT\\Mi_Arcivo_TXT.txt")

# Vamos a leer el archivo ahora: 
# Lo ponemos en comentario para que podamos usar el readlines()
#leer = archivo_sin_leer.read()
#print(leer)

# Esto nos entrega un arrelgo --> []
# Pero en este caso vacío, porque no está cerrado el archivo
# Lo ponemos en comentario para usar el readline()
#lineass = archivo_sin_leer.readlines()
#print(lineass)

# Ahora vamos a leer una sola línea: 
# Lo ponemos en comentario para usar el readline(21)
#linea = archivo_sin_leer.readline()
#print(linea)


# Si le pasamos un número, nos muestras los caracteres hasta ese número.
# Si no hay tantos caracteres, muestra espacios
# Ojo todo esto es en una sola línea
linea = archivo_sin_leer.readline(21)
print(linea)

# Cerramos el archivo: Para que no se vuelva a leer
archivo_sin_leer.close()

# Probamos si podemos leer (sale error):
#print(archivo_sin_leer.read())

# Pero podemos usar la información que ya hemos guardado:
print(linea)