import re

#1)  search() : Sirve para encontrar la primera coincidenciaa de lo que buscamos en todo el texto
""" 
- search() :  BUSCA EN TODO EL TEXTO
- Sirve para encontrar la primera coincidenciaa de lo que buscamos en todo el texto, 
si no encuentra nada, retorna un None, y si encuentra coincidencia, devuelve un objeto de tipo
match con información de la coincidencia. Con este objeto obtenido tenemos alguos métodos que podemos realiza:

- group(): Retorna la cadena que coincide con el patrón.
- start(): Retorna el índice de inicio de la coincidencia.
- end(): Retorna el índice final de la coincidencia.
- span(): Retorna una tupla (start, end) con las posiciones de inicio y fin de la coincidencia.
- groups(): Retorna una tupla con todos los grupos capturados en la expresión regular (si usaste paréntesis para agrupar partes del patrón).
- group(n): Si usas grupos en la expresión regular (usando paréntesis), puedes acceder a los diferentes grupos de la coincidencia por índice. (n puede ser 1, 2, 3 ...x)

Estructura:
result = re.search(pattern, string)  
pattern: La parte a buscar.
string: El texto donde se buscrá

"""

texto = """Lo que se canta en el cielo,
Cantamos en la tierra,
Al que se adora en el cielo,
Adoramos en la tierra,
Lo que se canta en el cielo,
Cantamos en la tierra,
Al que se adora en el cielo,
Adoramos en la tierra,
Al Santo, digno,
Al Cordero que vive para siempre,
Hacemos fiesta,
Hoy hacemos una fiesta,
Unidos hoy danzamos,
Con gozo celebramos,
Oh uh oh uh oh,
Fiesta,
Hoy hacemos una fiesta,
En la tierra cantamos,
Juntos gritamos,
Oh uh oh uh oh,
Lo que se canta en el cielo,
Cantamos en la tierra,
Al que se adora en el cielo,
Adoramos en la tierra,
Lo que se canta en el cielo,
Cantamos en la tierra,
Al que se adora en el cielo,
Adoramos en la tierra,
Al Santo, digno,
Al Cordero que vive para siempre,
Hacemos fiesta,
Hoy hacemos una fiesta,
Unidos hoy danzamos,
Con gozo celebramos,
Oh uh oh uh oh,
Fiesta,
Hoy hacemos una fiesta,
En la tierra cantamos,
Juntos gritamos,
Oh uh oh uh oh,
Hacemos fiesta,
(Hacemos fiesta),
Hacemos fiesta,
(Hacemos fiesta),
Hacemos fiesta,
(Hacemos fiesta),
Hacemos fiesta,
(Hacemos fiesta),
Fiesta (fiesta),
Hacemos fiesta (fiesta),
Hacemos fiesta (fiesta),
Hacemos fiesta (fiesta) fiesta,
Hacemos fiesta (fiesta),
Hacemos fiesta (fiesta),
Hacemos fiesta (fiesta),
Fiesta (fiesta) fiesta, fiesta, Oooh
Fiesta,
Hoy hacemos una fiesta,
Unidos hoy danzamos,
Con gozo celebramos,
Oh uh oh uh oh,
Fiesta,
Hoy hacemos una fiesta,
En la tierra cantamos,
Juntos gritamos,
Oh uh oh uh oh,
Oh uh oh uh o."""


# Definir lo que se buscará
# Lo puse entre paréntesis y un más: ()+ 
# Para buscar más de una coincidencia 
# OJO: Esto no es algo necesario
buscar = r'(lo que se canta)+'
# En result guardamos la busqueda, le ponemos re.IGNORECASE (para que tome mayúsculas o minúsculas)
result = re.search(buscar, texto, re.IGNORECASE)

# Hacemos un if-else: (!=None --> Si lo que retorna no es None entra al if sino al else)
if result != None:
    # Creamos un boolean, en caso del if es True:
    boolean = bool(result)
    print(boolean)
    # Imprimir el objeto match:
    print(f"Objecto Match: {result}")
    # Imprimir la cadena de tecto
    result_str = result.group()
    print(result_str)

else: 
    # Craos un boolena, en caso del else es False
    boolean = bool(result)
    print(boolean)
    print(f"No se encontró coincidencia con {buscar}")
    

"""" 
Antes de este ejemplo de Validar un nombre: 
Veamos esto, algo básico:   r'\b[A-Z][a-z]{2,}\b'

Explicación: 
- \b : Verifica que antes de la mayúscula (caracter de palabra) vea un caracter de No palabra
- r'' : Para que escribamos lo de REGEX y acepte el \
- [A-Z] : Busca en este caso una letra en mayúscula 
- [a-z]{2,} : Busca en este caso dos letras en minúsculas después de la mayúscula
- \b : Busca que después de la minúscula (caracter de palabra) vea un caracter de No palabra

Caracter de Palabra (\w): Son letras del a-z ; A-Z ; digitos del 0-9 y guión bajo (_)
- En UNICODE (modo normál), también se aceptan letras con acentos (ñ, ú, etc...)
- Si usamos el re.ASCII se limita lo que ya vimos.

Caracter No de Palabra (\W): Todo aquello que no forma parte de lo ue ya dijimos del \w (@   ,    .   -  ? $ % &  ...etc.....)


- OJO: Al decir \b decimos que debe de ver un \W  y  \w  |  \w  y  \W 
No puede ir: \W  y  \W  |  \w  y  \w 



YA HEMOS USADO EL {2,}   PERO.. ¿QUÉ MÁS HAY? 

- Vamos a ver como se indica cantidad (max o  min): 

    Ahí entran los cuantificadores:

    {n} → exactamente n repeticiones

    {n,} → al menos n repeticiones o más

    {n,m} → entre n y m repeticiones

    + → una o más (equivale a {1,})

    * → cero o más (equivale a {0,})

    ? → cero o una (equivale a {0,1})

    EJM: 
     1) [A-Z]{3}
        👉 exactamente 3 mayúsculas seguidas.

        re.findall(r'[A-Z]{3}', "ABC Hola XYZ Mundo A")
        # → ['ABC', 'XYZ']

     2) [A-Z]{2,}
        👉 al menos 2 mayúsculas seguidas.

        re.findall(r'[A-Z]{2,}', "AA B CCC DDDDD")
        # → ['AA', 'CCC', 'DDDDD']
    
     3) [A-Z]{2,4}
        👉 entre 2 y 4 mayúsculas seguidas.

        re.findall(r'[A-Z]{2,4}', "AA BBBB CCCCC")
        # → ['AA', 'BBBB', 'CCCC']
    
     4) [A-Z]+
        👉 una o más mayúsculas seguidas.

        re.findall(r'[A-Z]+', "Hola MUNDO NASA aZ")
        # → ['H', 'MUNDO', 'NASA', 'A', 'Z']

     5) patrón = r'ab*'
        👉 * es equivalente a {0,}
        Es decir: el patrón puede aparecer ninguna vez, una vez o muchas veces.
        texto = "a ab abb abbb aX"
        print(re.findall(patron, texto))
        # ['a', 'ab', 'abb', 'abbb', 'a']

     6) [A-Z]?
        👉 una mayúscula como máximo (0 o 1).

        re.findall(r'[A-Z]?', "Hola")
        # → ['H', '', '', '', '']
"""

# Validar correo Gmail: 
dominio = "gmail"
termino = "com"
patron_nombre = r'[A-Za-z0-9._\-\/$%&#]+@' + dominio + r'\.' + termino + r'\b'

name_pront = input("Ingrese su correo: ").strip()

boolean = bool(re.search(patron_nombre, name_pront))

result = "Correo Válido..." if boolean else "Correo no válido..."
print(result)



# Validar Nombre solo 1 nombre y número : 
regex = r'^[A-Z][a-z0-9]+$'
name = "Fll1vio"
boolean = bool(re.findall(regex, name))
result = f"Nombre Válido: {name}" if boolean else "Nombre no válido..."
print(result)



# Validar Nombre solo 1 nombre: 
regex = r'^[A-Z][a-z]+$'
name = "Flavio"
boolean = bool(re.findall(regex, name))
result = f"Nombre Válido: {name}" if boolean else "Nombre no válido..."
print(result)


# Validar nombre compuestos: 
regex = r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$'
name = "Flavio Gerardo Silva Estrada"
boolean = bool(re.findall(regex, name))
result = f"Nombre Válido: {name}" if boolean else "Nombre no válido..."
print(result)