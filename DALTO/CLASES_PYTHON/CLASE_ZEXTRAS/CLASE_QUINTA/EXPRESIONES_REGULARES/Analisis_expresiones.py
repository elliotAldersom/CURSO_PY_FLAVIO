import re 

text = "The quick brown fox jumps over the lazy dog"

x = re.search("^The.*dog$", text)

if x: # --> Si se enceuntra una coincidencia se ejecuta
    print("SI")
else: # --> Si no encuentra nada entra al else
    print("NO")


""" 
DESGLOSAMIENTO: 

x = re.search("^The.*dog$", text)

- ^ : El símbolo ^ indica que la coincidencia debe empezar al inicio de la cadena.

- .*: El .* es un comodín en expresiones regulares. Significa:
        .: Cualquier carácter (excepto saltos de línea).
        *: Cero o más repeticiones del carácter anterior.
En conjunto, .* significa:
Que cualquier secuencia de caracteres (incluyendo ninguno) 
puede ir entre "the" y "dog".

-$: El símbolo $ indica que la coincidencia debe ocurrir al final de la cadena.
    Esto significa que la cadena debe terminar con la palabra "dog".
"""
#_____________________________________________________________

# La cadena en la que se buscarán los patrones
text = "La fecha es 23/06/2021 y el teléfono es +1-555-555-5555"

# El patrón a buscar:
pattern = r"\d{2}/\d{2}/\d{4}"

# El texto con el que se reemplazará el patrón
replacement = "xx/xx/xxxx"

# Reemplazar todas las apariciones del patrón en la cadena de texto
new_text = re.sub(pattern, replacement, text)

# Imprimir el resultado
print(f"Texto modificado con exito: {new_text}")

""" 
VAMOS A EXPLICARLO:
# Reemplazar todas las apariciones del patrón en la cadena de texto
new_text = re.sub(pattern, replacement, text)

- .sub(pattern, replacement, text)
- El sub lo que haces es encontrar la cadena y reemplazrla:
- El primer parámetro (pattern en este caso) es la cadena que buscamos.
- El seundo parámetro (replacemente en este caso) es lo que va a reemplazar a la cadena.
- El tercer parámetro (text en este caso) es la cadena en la que se va a buscar.
"""

# VAMOS A HACER LO MISMO PERO CON EL NÚMERO TELEFÓNICO:
num = r"\+\d{1}-\d{3}-\d{3}-\d{4}"
reemplazo = "+x-xxx-xxx-xxxx"
new_text = re.sub(num, reemplazo, new_text)
print(f"Texto modificado con exito: {new_text}")

#_____________________________________________________________
# VAMOS A ENOCNTRAR TODAS LAS VOCALES:

string = "Reemplazando todas las vocales por ASTERISCO en la letra de esta canción."

new_string = re.sub(r"[aeiouáéíóú]", "*", string, flags= re.IGNORECASE)
print(f"Texto modificado con exito: \n{new_string}")

""" 
EXPLICACIÓN:
new_string = re.sub(r"[aeiou]|[áéíóú]", "*", string, flags= re.IGNORECASE)

Lo que hcemos es que con el --> .sub
reemplazamos algo con otra cosa que le pasemos (ya lo expliqué antes)

[aeiou]|[áéíóú]", "*" 
Acá le pasamos en una especie de lista (por los corcetes --> [])
para que así nos busque uno por uno cada vocal (con tilde o sin tilde)
ya que si le paasamos así: 
aeiou --> NOS VA A BUSCAR DONDE ESTÉN JUNTOS LAS VOCALES

[aeiouáéíóú]", "*" 
Acá le pasamos en una especie de lista (por los corcetes --> [])
para que así nos busque uno por uno cada vocal (con tilde o sin tilde)
ya que si le paasamos así: 
aeiou --> NOS VA A BUSCAR DONDE ESTÉN JUNTOS LAS VOCALES

"""

new_string = re.sub(r"[aeiou]", "*", string, flags= re.IGNORECASE)
new_string = re.sub(r"[áéíóú]", "/", new_string, flags= re.IGNORECASE)
print(f"Texto modificado con exito: \n{new_string}")

""" 
ACÁ HICIMOS QUE LAS VOCALES SIN ACENTOS SE REEMPLACEN POR *
Y LAS VOCALES CON ACENTOS SE REEMPLACEN POR /
"""
#________________________________________________________________
# VERIFICAR SI EL CORREO CUMPLE O NO CUMPLE
email = "example@gmail.com"
pattern = "[a-zA-Z0-9._%+*]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
result = re.match(pattern, email)

if result:
    print("Dirección de correo válida")
else:
    print("Dirección de correo inválida")

""" 
EXPLICACIÓN
a-zA-Z0-9 : BUSCA DE LA a HASTA LA z Y DE LA A HASTA LA Z, TAMBIÉN DEL 0 AL 9
. : ACEPTA TODO LO QUE NO SE UN SALTO DE LÍNEA (\n)
_ : ACEPTA EL GUION BAJO
% : ACEPTA TODO LO QUE ENUENTRE ANTES Y DESPUÉS DE EL LO VA A VALIDAR
+ : ESTO NOS BUSCA 1 O MÁS COINCIDENCIAS

result = re.match(pattern, email)
- El re.macht() sirve para buscar una coincidencia de un patrón solo al
principio de una cadena.Es decir re.match() intenta hcer coincidir el patrón 
con el inicio de la caden, pero no buscará a trvés de toda la cadena como lo hace
re.serch o r.findall

- En el primer parámetro se pasa 
"""
#________________________________________________________________
print("\nVALIDACIÓN DE UNA PÁGINA WEB")
text = "Este es un ejemplo de una página web: https://www.google.com"

pattern = "https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

result = re.findall(pattern, text)

print(result)

""" 
EXPLICACIÓN: 
https? : Verifica si adelante hay un https o http o sea la s es opcional
"""
