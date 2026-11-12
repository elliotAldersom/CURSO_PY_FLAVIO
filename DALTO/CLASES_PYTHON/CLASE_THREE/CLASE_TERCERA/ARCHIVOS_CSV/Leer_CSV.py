"""
Un archivo CSV es un archivo separado por comas
Los archivos CSv pueden ser interpretado por la mayoría de los programas 
de hoja de cálculo y bases de datos.

Los archivos.csv son iterables también
Nos devuelve como una especie de tabla, la primera lista es
como los nombre de la columna o el campo (database)
"""
# No se olviden de importar el csv:
import csv

with open("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_CSV\\Datos.csv") as archivo_csv:
   # Nos devuelve una especie de tupla, ya que están separadas por comas ( , )
   # print(archivo_csv.read())

   # Lo más recomendable usar es: csv.reader()
   reader = csv.reader(archivo_csv)
   # print(reader) --> Nos devuelve como números, será el objeto o algo así
   # Vamos a recorrer fila por fila 
   for i in reader :
      # De esta forma recorremos fila por fila y nos muestra como lista cada fila
      print(i)

