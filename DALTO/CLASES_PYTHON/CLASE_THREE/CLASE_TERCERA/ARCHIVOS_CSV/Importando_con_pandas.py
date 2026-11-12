""" 
CUANDO TRABAJAMOS ESTO DE FORMA PROFESIONAL, LOS MÁS RECOMENDBALE
PARA LEER ARCHIVOS CSV ES USAR LA LIBRERÍA PANDAS Y NO EL CSV

Ahora esto es mucho mejor que usar el import csv
esto nos devuelve una tabla, donde podemos hacer operaciones de pandas
además nos muestra los campos (son los primeros de cada columna), también
nos muestra los registro (las filas)
muy fiel o parecido a un database
"""
# Importar pandas
import pandas as pd
# Para leer un archivo hacemos: pd.read_csv(ruta_archivo.csv)
# Vamos a cambiar los nombres de las columnas con el   ,names=
df = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_CSV\\Datos.csv") #, names= ["Name","Last Name","Age"])
# Le llamamos df porque esto no es el archivo como tal sino el DataFrame
#print(df)
"""
Un DataFrame es un archivo bidimensional, similares a una hoja de cálculo,
podemos trabajar y tratar igual como si fuera una hoja de cálculo,
no exactamnete igual, pero conceptualmente para que lo entendamos.

Entonces al no comportarse como un archivo, tiene su propia forma de accederse.
Siempre los valores que van a tener son dos, Filas y Columnas.
"""
# Obtener los datos de una columnas que queramos: 

print(df.head())    # Imprime las primeras 5 filas
print(df.columns)  # Imprime las columnas del DataFrame
print(repr(df.columns))  # Esto te mostrará las columnas con caracteres invisibles
# Lo normál es que aparezcan los nombres de las columnas entre comillas simpes 
# 'para esto hacemos' , pero me sale así ' "apellido"' 

#_____________________________________________________________________________________
"""ESTO ES ALGO QUE DEBEMOS DE HACER SIEMPRE PRIMERO, POR SI NOS APARECE CON 
CARACTERES INVISIBLES O ESPACIOES DEMÁS, ETC

PERO PODEMOS EVITAR HACER ESTO, SI EN EL ARCHIVO.CSV , NO TENEMOS ESPACIOS DE PORMEDIO
DE CADA ELEMENTO O SEA ES ASÍ: 
"NAME","LAST NAME","AGE"
"FLAVIO","SILVA","18

TODOS JUNTOS SIN ESPACIOS DE PORMEDIO
"""
# Limpiar los nombres de las columnas
df.columns = df.columns.str.replace('"', '').str.strip()

# Limpiar las comillas dobles y los espacios en las celdas del DataFrame
df = df.applymap(lambda x: x.replace('"', '').strip() if isinstance(x, str) else x)
#___________________________________________________________________________________________


# Verificar las columnas después de limpiar
print(df.columns)
print(repr(df.columns))

columna = input("Que columna deseas ver: ")
# Ahora debería funcionar
print(df[columna])

print(df)


"""
Vamos a ver Slicing, es una técnica que tiene Python
que nos permite realizar ciertas cosas cuando trabajamos con algunos elementos.
En el caos de los Arrays nos permite identificar el principio y el final
de las formas que vamos a poder acceder a los elementos
"""
print("\nVamos a ver Slicing\n")
cadena = "0123456789"
print(cadena[4]) # -> Esto nos muestra el elemento en el índice 4

# Pero si deseamos mostrar los elementos del índice 0 al 4 o lo que gustes
# Usamos el Slicing

# Si lo dejamos así nos muestra del principio al fin
print(cadena[:]) 
print(cadena[0:])

# Haciendo esto nos muestra del índice 0 al 4 --> 0123
# No se incluye el 4 (es como el range())
# Si quieres que te muestre el 4, debes incluirlo en el rango
# O sea en ves del 4 pones el 5
print(cadena[0:4]) 
print(cadena[:4])
print(cadena[:5])


# Ahora veremos como hacer si nosotros queremos
# ordenar los datos en la tabla
# por decir ordenar de manor a mayor (por edades)
# ORDENAMOS EL DATAFRAME POR LA EDAD:

# Vamos a ordenarlo de forma ascendente:
df_ordenado_ascendente = df.sort_values("edad") # --> Es necesario guardarlo en una variable
print(df_ordenado_ascendente) # --> Imprimimos la variable

# Vamos a ordenarlo de forma descendente:
df_ordenado_descendente = df.sort_values("edad", ascending=False) # --> Es necesario guardarlo en una variable
print(df_ordenado_descendente) # --> Imprimimos la variable


# Ahora vamos a ver como concatenarlos 
# Ya tenemos el archivo df, ahora del mismo archivo vamos a hacer el df_2: 
df_2 = pd.read_csv("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\CLASES_PYTHON\\CLASE_THREE\\CLASE_TERCERA\\ARCHIVOS_CSV\\Datos.csv") #, names= ["Name","Last Name","Age"])

# Para concatenarlos usamos la función concat
print("\nVamos a concatenar los dos DataFrame:\n")
df_concatenado = pd.concat([df, df_2]) # --> El parámetro nos pidr una lista, por eso lo pasmaos así
print(df_concatenado)

# Accediendo a las filas con head()
""" 
Con head() podemos accader a cualquier cantidad de registros 
(si lo vemos como tablas de DataBase) que queramos
solo debemos de pasarle hasta el número de registros o bueno filas que queremos ver,
y nos imprime desde la fila 1 hasta el que pasemos.
Pero debemos de pasarle al parámetro el númeor de filas que deseamos ver
si le pasmaos 0, solo nos mostrará los encabezados.
"""
print("\nVamos a acceder a las filas del DataFrame con head() :\n")
print("Con head() podemos accader a cualquier cantidad de registros \n(si lo vemos como tablas de DataBase) que queramos, o filas,\nsolo debemos de pasarle hasta el número de registros o bueno filas que queremos ver,\ny nos imprime desde la fila 1 hasta el que pasemos.\nPero debemos de pasarle al parámetro el númeor de filas que deseamos ver\nsi le pasmaos 0, solo nos mostrará los encabezados.")
primer_fila = df.head(1) # --> El parámetro nos pide un número, y lo guardamos en una variable
print(primer_fila) # --> Imprimimos la variable
filas = df.head(3)
print(filas)
cero_filas = df.head(0)
print(cero_filas)


""" 
- tail : cola en inglés
- head : cabeza en inglés

con tail() accdeemos a las filas o registros de abajo no las de arriba 
como es con head()

Con tail() podemos accader a cualquier cantidad de registros 
(si lo vemos como tablas de DataBase) que queramos, o filas,
solo debemos de pasarle hasta el número de registros o bueno filas que queremos ver,
y nos imprime desde la fila 1 hasta el que pasemos.
Pero debemos de pasarle al parámetro el númeor de filas que deseamos ver
si le pasmaos 0, solo nos mostrará los encabezados.
"""
print("\nVamos a acceder a las últimas filas del DataFrame con tail() : \n")
print("Con tail() podemos accader a cualquier cantidad de registros \n(si lo vemos como tablas de DataBase) que queramos, o filas,\nsolo debemos de pasarle hasta el número de registros o bueno filas que queremos ver,\ny nos imprime desde la fila 1 hasta el que pasemos.\nPero debemos de pasarle al parámetro el númeor de filas que deseamos ver\nsi le pasmaos 0, solo nos mostrará los encabezados.")
ultimas_filas = df.tail(3) # --> El parámetro nos pide un número, y lo guardamos en una variable
print(ultimas_filas) # --> Imprimimos la variable
cero_fila = df.tail(0)
print(cero_fila) 


# Accediendo a la cantidad de filas y columnas con shape

""" 
shape : es una propiedad, atributo
Devuelve como coordenadas (x ,y) x : filas ; y : columnas
Prácticamente es una tupla de la cantidad que hay de filas y columnas,
"""
filas_columnas = df.shape
print(f"\nEstas son la cantidad que hay de (filas, columnas): {filas_columnas}")

# Acceder a las filas totales:
filas_totales = filas_columnas[0]
print(f"\nEstas son las filas totales que hay en la tabla: {filas_totales}")

# Acceder a as columnas totales:
columnas_totales = filas_columnas[1]
print(f"\nEstas son la scolumnas totales que hay en la tabla: {columnas_totales}")

# Vamos a hacer o mismo pero con desempaquetamiento: 
filas_totales2, columnas_totales2 = filas_columnas # --> O también df.shape
print(f"\nEstas son las filas totales que hay en la tabla: {filas_totales2} \nEstas son las columnas totoales: {columnas_totales2}")


# Obteniendo data estadística del DataFRame
df_info = df.describe()
print(f"Esta es la info del DataFrame:\n {df_info}")

""" 
El método describe() nos devuelve una serie de estadísticas
En este caso nos imprime esto:

Esta es la info del DataFrame:
             edad
count   6.000000
mean   15.333333
std     6.683313
min     7.000000
25%    10.500000
50%    15.000000
75%    20.250000
max    24.000000

"""

# Accediendo a un elemento específico del DataFrame (df) con loc
""" 
loc es una propiedad 
las propiedades son así: objeto.propiedad
En este caso loc nos pide de parámetro el índice,
el cual es la forma de llamar las filas,
las filas tienen sus número, como si fuera su id (si hablamos de DataBase)
Y son como registros en una tabla de base de datos (todo lo digo en fomra de semejanza)

  nombre   apellido  edad
0   flavio      silva    18
1   fabian      silva    21
2  joaquin    salazar     7
3   camila      dalto    24
4     juan    ramirez    10
5  roberto  gutierrez    12

- Le pasamos el índice de fila (o registro) y el campo (hablando en DataBase) que queremos obtener
elemento_especifico = df.loc[0 , "edad"]
elemento_especifico = df.loc[registro , "campo"]

"""
elemento_especifico = df.loc[0 , "edad"]
print(f"El elemento específico que estamos buscando es: {elemento_especifico} , del campo de la edad.")


# Accediendo a un elemento específico del DataFrame con iloc:
""" 
iloc es una propiedad 
las propiedades son así: objeto.propiedad
En este caso loc nos pide de parámetro el índice,
el cual es la forma de llamar las filas,
las filas tienen sus número, como si fuera su id (si hablamos de DataBase)
Y son como registros en una tabla de base de datos (todo lo digo en fomra de semejanza)

  nombre   apellido  edad
0   flavio      silva    18
1   fabian      silva    21
2  joaquin    salazar     7
3   camila      dalto    24
4     juan    ramirez    10
5  roberto  gutierrez    12

- Le pasamos el índice de fila (o registro) y el índice del campo (hablando en DataBase) que queremos obtener
elemento_especifico = df.loc[1 , 2]
elemento_especifico = df.loc[registro , ímdice_del_dato_que_queremos_ver]

los campos son: nombre (índice 0), apellido (índice 1), edad (índice 2)
"""
elemento_especifico = df.iloc[1 , 2]
print(f"El elemento específico que estamos buscando es: {elemento_especifico}, del campo de la edad")


# Accediendo a todas las filas de una columna con iloc (vamos a usar el Slicing ( : ) )
# En este caso quiero que me muestre una sola columna, pero todas las filas de esta columa
# Para ello voy a usar el Slicing ( : )
# Acá le decimos, muestrame todas las filas del elemento 1 (apellido)
apellidos = df.iloc[: , [1, 2]]
print(apellidos)
print(df[["nombre" , "apellido"]])

""" 
el print(apellido) nos imprime esto:

0        silva
1        silva
2      salazar
3        dalto
4      ramirez
5    gutierrez
Name: apellido, dtype: object
Pero esto es más útils pues podemos acceder a más de una columna:
apellidos = df.iloc[: , [1, 2]]
print(apellidos)
print(df["apellido"])
De esta froma podemos ver el apellido y la edad de cada una de las filas o registros:

  apellido  edad
0      silva    18
1      silva    21
2    salazar     7
3      dalto    24
4    ramirez    10
5  gutierrez    12
______________________________________________

el print(df[apelldio]) nos imprime esto:

0        silva
1        silva
2      salazar
3        dalto
4      ramirez
5    gutierrez
Name: apellido, dtype: object

Esto también nos permite mostrar más de una columna, pero de esta forma:
print(df[["nombre" , "apellido"]])

 nombre   apellido
0   flavio      silva
1   fabian      silva
2  joaquin    salazar
3   camila      dalto
4     juan    ramirez
5  roberto  gutierrez
"""

# Ahora vamos a imprimir todo pero de una sola fila
# Anteriormente imprimimos todo de una columna (o campo), y ahora todo de una fila (o registro)
# Para ello vamos a usar el Slicing ( : )
# Acá le decimos, muestrame todas los elementos de una fila o regsitro 
fila_mostrada = df.iloc[3 , :] # --> Funciona igual con df.loc[3 , :]
print(fila_mostrada)

""" 
El print(fila_mostrada) nos imprime esto: 

nombre      camila
apellido     dalto
edad            24
Name: 3, dtype: object

"""
# Accediendo a fila con la edad mayor o igual a 18 años
print("\nAccediendo a todas las columnas de una fila con la edad mayor o igual a 18 años\n")
edad_apta = df.loc[df["edad"] >= 18 ,  :]
print(edad_apta)

""" 
El print(edad_apta) imprime:

   nombre apellido  edad
0  flavio    silva    18
1  fabian    silva    21
3  camila    dalto    24


"""

print("\nAccediendo a todas las columnas de una fila con la edad menor a 18 años y mayores a 0 años\n")
edad_no_apta = df.loc[(df["edad"] < 18) & (df["edad"] > 0) ,  :]
print(edad_no_apta)

""" 
En pandas el and se escribe como & ; el or como | ; el not como ~ 
El print(edad_no_apta) imprime:

  nombre   apellido  edad
2  joaquin    salazar     7
4     juan    ramirez    10
5  roberto  gutierrez    12

"""