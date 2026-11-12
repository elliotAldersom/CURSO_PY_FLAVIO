# Vamos a importar el módulo que usamos para trabajar con expresiones regulares
# re es el más común, aunque hay más:
# re es el módulo oficial que viene en la biblioteca oficial de python
import re


""" 
Acá lo que más nos importa es que debemos de encontrar coincidencias,
lo que trabajamos con expresiones regulares son patrones, EJM:
- Quiero encontrar una: s.a (ese con un punto y una a)

Y lo que hacemos al encontrar una coincidencia es devolverla,
devolver todas las coincidencias, reemplazarlas por otra, usarla como seperador,
etc.. 

"""

texto =  '''Hola maestro,esta es la cadena 1: como estás mi capitan?
Esta es la segunda (2. ) línea de texto _@_ 40000.
Y esta es la final definitiva mi capitan (3) 90.
Hola y adios 23. capitan.
abab abab ab ab bb bbbb aa aaaaa baba
'''

# Vamos a buscar la primera coincidencia usando: --> re.search()
# En el primer parámetro, le pasamos lo que vamos a buscar
# En el segundo parámetro, le pasamos el texto (variable) donde vamos a buscar
resultado = re.search("n", texto) 
print(resultado)
""" 
imprime: <re.Match object; span=(28, 29), match='n'>
"""

# Vamos a buscar todas las coincidenciaa usando: --> re.findall()
# En el primer parámetro, le pasamos lo que vamos a buscar
# En el segundo parámetro, le pasamos el texto (variable) donde vamos a buscar
resultado_2 = re.findall("esta", texto)  # --> No dejmos espacios, sino también se considera
print(resultado_2)
""" 
imprime: ['n', 'n', 'n', 'n', 'n', 'n', 'n']
"""

# Para buscar todas las coincidencias de 2 palabras
# Utilizamos un patrón que considera 'esta' y 'Esta'
resultado_2 = re.findall(r"([eE]sta)", texto)  # --> No dejmos espacios, sino también se considera
print(resultado_2)
""" 
imprime: ['esta', 'Esta', 'esta']  
"""

# Para buscar 2 palabras distintas
# Usamos el: | que es como el or (en Java el or es |)

resultado_2 = re.findall(r"esta|como", texto) # --> No dejmos espacios, sino también se considera
print(resultado_2)
"""
imprime: ['esta ', ' como', 'esta ']
"""

# Vamos a ignorar las mayúsculas y minúsculas
# Agregamos al final el : re.IGNORECASE

resultado_2 = re.findall(r"esta|y", texto, re.IGNORECASE) # --> No dejmos espacios, sino también se considera
print(resultado_2)
""" 
imprime: ['esta', 'Esta', 'Y', 'esta']
"""

# Usamos el flagas=  
# como parámetro, es útil, si vamos a usar varios flags
resultado_2 = re.findall(r"esta|y", texto, flags=re.IGNORECASE) # --> No dejmos espacios, sino también se considera
print(resultado_2)
""" 
imprime: ['esta', 'Esta', 'Y', 'esta']
"""

""" 
AHORA EMPEZAMOS CON LAS EXPREIONES REGULARES:

DATO:
resultado_3 = re.findall(r"")
al usar la r decimos que lo que vamos a pasar es una expresión regular
"""
# \d -> Busca dígitos numérricos del 0 - 9
resultado_3 = re.findall(r"\d", texto)
print(resultado_3)
"""
imprime: ['1', '2', '3']
"""

# \d -> Busca TODO MENOS dígitos numérricos del 0 - 9
resultado_3 = re.findall(r"\D", texto)
print(resultado_3)
""" 
imprime: 
['H', 'o', 'l', 'a', ' ', 'm', 'a', 'e', 's', 't', 'r', 'o', ',', 'e', 's', 't', 'a', 
' ', 'e', 's', ' ', 'l', 'a', ' ', 'c', 'a', 'd', 'e', 'n', 'a', ' ', ':', 
' ', 'c', 'o', 'm', 'o', ' ', 'e', 's', 't', 'á', 's', ' ', 'm', 'i', 
' ', 'c', 'a', 'p', 'i', 't', 'a', 'n', '?', 
'\n', 'E', 's', 't', 'a', ' ', 'e', 's', ' ', 'l', 'a', ' ', 
's', 'e', 'g', 'u', 'n', 'd', 'a', ' ', '(', ')', ' ', 'l', 'í', 'n', 'e', 'a', 
' ', 'd', 'e', ' ', 't', 'e', 'x', 't', 'o', ' ', '@', 
'\n', 'Y', ' ', 'e', 's', 't', 'a', ' ', 'e', 's', ' ', 'l', 'a', ' ', 
'f', 'i', 'n', 'a', 'l', ' ', 'd', 'e', 'f', 'i', 'n', 'i', 't', 'i', 'v', 'a', 
' ', 'm', 'i', ' ', 'c', 'a', 'p', 'i', 't', 'a', 'n', ' ', '(', ')', '\n']
"""

# \w --> Busca caracteres alfanuméricos (letras y dígitos)
# es decir: a - z / A - Z / 0 - 9 / _ (guión bajo)
# En Python el guión bajo se considera como alfanumérico, solo en Python
resultado_3 = re.findall(r"\w", texto)
print(resultado_3)
""" 
imprime: 
['H', 'o', 'l', 'a', 'm', 'a', 'e', 's', 't', 'r', 'o', 
'e', 's', 't', 'a', 'e', 's','l', 'a', 'c', 'a', 'd', 'e', 'n', 'a', '1', 
'c', 'o', 'm', 'o', 'e', 's', 't', 'á', 's', 
'm', 'i', 'c', 'a', 'p', 'i', 't', 'a', 'n', 
'E', 's', 't', 'a', 'e', 's', 'l', 'a', 's', 'e', 'g', 'u', 'n', 'd', 'a', '2', 
'l', 'í', 'n', 'e', 'a', 'd', 'e', 't', 'e', 'x', 't', 'o', '_', '_', 
'Y', 'e', 's', 't', 'a', 'e', 's', 'l', 'a', 'f', 'i', 'n', 'a', 'l', 
'd', 'e', 'f', 'i', 'n', 'i', 't', 'i', 'v', 'a', 'm', 'i', 
'c', 'a', 'p', 'i', 't', 'a', 'n', '3', '9', '0']
"""

# \W --> Busca TODO MENOS caracteres alfanuméricos 
resultado_3 = re.findall(r"\W", texto)
print(resultado_3)
""" 
imprime:
[' ', ',', ' ', ' ', ' ', ' ', ':', ' ', ' ', ' ', ' ', '?', '\n', 
' ', ' ', ' ', ' ', '(', ')', ' ', ' ', ' ', ' ', '@', '\n',
' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', ')', ' ', '\n']   
"""

# \s --> Busca espacios en blanco (Espacios comunes, tabulciones (tabs), saltos de línea (\n))
resultado_3 = re.findall(r"\s", texto)
print(resultado_3)
""" 
imprime:
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n',
' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n',
' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n']
"""

# \S --> Busca TODO MENOS espacios en blanco 
resultado_3 = re.findall(r"\S", texto)
print(resultado_3)
""" 
imprime: 
['H', 'o', 'l', 'a', 'm', 'a', 'e', 's', 't', 'r', 'o', ',', 'e', 's', 't', 'a', 
'e', 's', 'l', 'a', 'c', 'a', 'd', 'e', 'n', 'a', '1', ':', 'c', 'o', 'm', 'o', 
'e', 's', 't', 'á', 's', 'm', 'i', 'c', 'a', 'p', 'i', 't', 'a', 'n', '?', 
'E', 's', 't', 'a', 'e', 's', 'l', 'a', 's', 'e', 'g', 'u', 'n', 'd', 'a', 
'(', '2', ')', 'l', 'í', 'n', 'e', 'a', 'd', 'e', 't', 'e', 'x', 't', 'o', 
'_', '@', '_', 
'Y', 'e', 's', 't', 'a', 'e', 's', 'l', 'a', 'f', 'i', 'n', 'a', 'l', 
'd', 'e', 'f', 'i', 'n', 'i', 't', 'i', 'v', 'a', 
'm', 'i', 'c', 'a', 'p', 'i', 't', 'a', 'n', '(', '3', ')', '9', '0']
"""

# . --> Busca TODO MENOOS saltos en línea
resultado_3 = re.findall(r".", texto)
print(resultado_3)
""" 
imprime:
['H', 'o', 'l', 'a', ' ', 'm', 'a', 'e', 's', 't', 'r', 'o', ',', 
'e', 's', 't', 'a', ' ', 'e', 's', ' ', 'l', 'a', ' ', 'c', 'a', 'd', 'e', 'n', 'a',
' ', '1', ':', ' ', 'c', 'o', 'm', 'o', ' ', 'e', 's', 't', 'á', 's', ' ', 
'm', 'i', ' ', 'c', 'a', 'p', 'i', 't', 'a', 'n', '?', 
'E', 's', 't', 'a', ' ', 'e', 's', ' ', 'l', 'a', ' ', 
's', 'e', 'g', 'u', 'n', 'd', 'a', ' ', '(', '2', ')', ' ', 'l', 'í', 'n', 'e', 'a', 
' ', 'd', 'e', ' ', 't', 'e', 'x', 't', 'o', ' ', '_', '@', '_', 
'Y', ' ', 'e', 's', 't', 'a', ' ', 'e', 's', ' ', 'l', 'a', ' ', 
'f', 'i', 'n', 'a', 'l', ' ', 'd', 'e', 'f', 'i', 'n', 'i', 't', 'i', 'v', 'a', ' ', 
'm', 'i', ' ', 'c', 'a', 'p', 'i', 't', 'a', 'n', ' ', '(', '3', ')', ' ', '9', '0']
"""

# \n --> Busca saltos en líneas
resultado_3 = re.findall(r"\n", texto)
print(resultado_3)
""" 
imprime: ['\n', '\n', '\n']
"""
# \. ; \* ; \+ ; \[]  --> Ayuda a busar estos caracteres especiales
# \. --> Busca los puntos 
resultado_3 = re.findall(r"\.", texto)
print(resultado_3)
""" 
imprime: ['.', '.']
"""

# Armando una cadena que buque un número, seguido de un punto y un espacio
resultado_caracter = re.findall(r"\d\.\s", texto)
print(resultado_caracter)
""" 
imprime: ['2. ', '4.\n', '0.\n']
"""

# Cómo hacemos para buscar el final o inicio de una línea
# ^String --> Busca si la palabra (String) está al inicio de una línea
resultado_inicio = re.findall(r"^hola", texto, flags=re.M | re.IGNORECASE) # --> Se escribe juntos para que los espacios no afecten
print(resultado_inicio)
""" 
Estamos usando el parámetro flags=re.M  (MULTILINE)
Esto hace que sea multilínea, o sea evalue si la palabra está al inicio de 
cada una de las líneas o después del salto de línea.
También hemos puesto el | re.IGNORECASE 
esto para que ignore si es mayúscula o minúscula 
imprime: 
- Si está al inicio de la línea: ['Hola']
- Si no está al inicio de la línea: []
"""

# $String --> Busca si la palabra (String) está al final de una línea
resultado_final = re.findall(r"capitan[\?\.]$", texto, flags= re.M | re.IGNORECASE)
print(resultado_final)
""" 
En esta caso, tiene los mismo parámtros que el anterior,
ahora la diferencia que el $ no va al inicio sino al final 
de la cadena o dato qu buscamos verificar si está al final o no
de la línea.

resultado_final = re.findall(r"capitan[\?\.]$", texto, flags= re.M | re.IGNORECASE)
Hicimos esto : capitan[\?\.]$ 
para que busque si alguna línea termina con: capitan. o capitan?

imprime:
- Si está al final de la línea: ['capitan?', 'capitan.']
- Si no está al final de la línea: []
"""

# LOS GRUPOS
# {n} --> Busca n cantidad de veces el valor de la izquierda
resultado_n = re.findall(r"\d{2}\.\n",texto) # --> Imprime una cadena donde haya 2 dígitos numérios juntos
print(resultado_n)
""" 
imprime si lo encuentra: ['40', '90'] 
- Muestra el 40 (aunque en la cadena está como 400. )
(pero tiene 2 digitos numéricos y los muestra desde la izquierda)
imprime si no lo encuentra: []


Al hacer esto:
resultado_n = re.findall(r"\d{2}\.",texto) 
imprime: ['00.', '90.', '23.']

Al hacer esto:
resultado_n = re.findall(r"\d{2}\.\n",texto)
imprime: ['00.\n', '90.\n']
"""

# Ahora para hacer rangos:
# {n,m} --> Al menos n veces y como máximo m veces el valor de la izquierda
resultado_max_min = re.findall(r"\d{1,3}\.", texto)
print(resultado_max_min)

""" 
resultado_max_min = re.findall(r"\d{1,3}", texto)
imprime: ['1', '2', '400', '00', '3', '90', '23'] 

resultado_max_min = re.findall(r"\d{1,3}\.", texto)
imprime: ['2.', '000.', '90.', '23.']

resultado_max_min = re.findall(r"ab{1,3}", texto)
Esto busca, una "a" seguida por "b" que se repita mínimo 1 y máximo 3 veces y termina con un punto.
imprime: ['ab', 'ab', 'ab', 'abb']
"""
# DE ESTA FORMA HACEMOS QUE EL RANGO DE {1,3} TOMO A LA "A" Y "B"
# ESTO SE HACE ENCERRANDO CON PARÉNTESIS (ab)
resultado_a_b = re.findall(r"(ab){2} ", texto)
print(resultado_a_b)
""" 
Esto hace que cada ves que se encuentre 2 veces ab 
nos devuelva una ves ab
resultado_a_b = re.findall(r"(ab){2} ", texto)
imprime: ['ab', 'ab']

resultado_a_b = re.findall(r"(ab){1}", texto)
imprime: ['ab', 'ab', 'ab', 'ab', 'ab']
"""

# ESTO HACE QUE EL RANGO DE {1,3} TOME A LA "A" Y "B"
# NOS DEVUELVE "aa";  "ab" ; "bb"
# ESSTO LO LOGRAMOS HACIENDO [ab]
resultado_a_b = re.findall(r"[ab]{2} ", texto)
print(resultado_a_b)

""" 
resultado_a_b = re.findall(r"[ab]{2} ", texto)
imprime: ['ab ', 'ab ', 'ab ', 'ab ', 'bb ', 'bb ', 'aa ', 'aa ']
"""