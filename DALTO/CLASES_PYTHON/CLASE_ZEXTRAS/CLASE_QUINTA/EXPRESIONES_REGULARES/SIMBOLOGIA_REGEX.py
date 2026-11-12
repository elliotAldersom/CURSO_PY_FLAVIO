"""
-1) . : Coincide con cualquier carácter, excepto el salto de línea.
-2) ^ : Coincide con el inicio de la cadena.
-3) $ : Coincide con el final de la cadena.
-4) [] : Define una clase de caracteres, por ejemplo, [a-z] coincide con cualquier letra minúscula.
-5) [^] : Negación dentro de una clase de caracteres, por ejemplo, [^a-z] coincide con cualquier carácter que no sea una letra minúscula.
-6) | : Operador OR, permite alternar entre diferentes opciones, por ejemplo, "a|b" coincide con "a" o "b".
-7) () : Agrupación, permite agrupar parte de la expresión para aplicar operadores sobre ellos.
-8) ? : Hace que el carácter anterior sea opcional (0 o 1 vez). Ejemplo: "a?" coincide con "a" o nada.
-9) * : Coincide con el carácter anterior 0 o más veces. Ejemplo: "a*" coincide con una cadena que tiene cero o más "a".
-10) + : Coincide con el carácter anterior 1 o más veces. Ejemplo: "a+" coincide con una cadena que tiene al menos una "a".
-11) {n} : Coincide con exactamente n repeticiones del carácter anterior. Ejemplo: "a{3}" coincide con "aaa".
-12) {n,} : Coincide con n o más repeticiones del carácter anterior. Ejemplo: "a{2,}" coincide con "aa", "aaa", "aaaa", etc.
-13) {n,m} : Coincide con entre n y m repeticiones del carácter anterior. Ejemplo: "a{2,4}" coincide con "aa", "aaa", o "aaaa".
-14) \ : Escapa caracteres especiales, como "." o "*". Ejemplo: "\." busca un punto literal.
-15) \d : Coincide con cualquier dígito (equivalente a [0-9]).
-16) \D : Coincide con cualquier carácter que no sea un dígito.
-17) \w : Coincide con cualquier carácter de palabra (letras, números y guiones bajos, equivalente a [a-zA-Z0-9_]).
-18) \W : Coincide con cualquier carácter que no sea de palabra.
-19) \s : Coincide con cualquier espacio en blanco (espacio, tabulación, salto de línea).
-20) \S : Coincide con cualquier carácter que no sea un espacio en blanco.
-21) \b : Coincide con un límite de palabra (inicio o final de una palabra).
-22) \B : Coincide con cualquier lugar que no sea un límite de palabra.
-23) \n : Coincide con un salto de línea.
-24) \t : Coincide con una tabulación.
-25) (?=...) : Aseguramiento positivo, coincide solo si lo que sigue cumple la condición, pero no consume caracteres. Ejemplo: "a(?=b)" coincide con "a" solo si está seguido de "b".
-26) (?!...) : Aseguramiento negativo, coincide solo si lo que sigue no cumple la condición, pero no consume caracteres. Ejemplo: "a(?!b)" coincide con "a" solo si no está seguido de "b".
-27) (?:...) : Agrupación sin captura, es similar a los paréntesis pero no guarda el contenido para referencias posteriores.
-28) (?P<name>...) : Captura con nombre, permite referirse a los grupos por un nombre en lugar de un número. Ejemplo: (?P<digit>\d) capturará un dígito como "digit".
-29) (?i) : Modificador que hace que la expresión sea insensible a mayúsculas/minúsculas.
-30) (?m) : Modificador de modo multilínea, donde ^ y $ coinciden con el principio y el final de cada línea.
-31) (?s) : Modificador de modo dotall, donde el punto (.) coincide con todos los caracteres, incluidos los saltos de línea.
"""

# 1) . : Coincide con cualquier carácter, excepto el salto de línea.
import re
text = "Ho  @la mundo"
print(re.findall(r"H.*la", text, re.IGNORECASE))  # Coincide con "Ho  @la"


# 2) ^ : Coincide con el inicio de la cadena.
import re
text = "Hola mundo"
print(re.findall(r"^[A-Z]", text, re.IGNORECASE))  # Coincide con "H"


# 3) $ : Coincide con el final de la cadena.
import re
text = "Hola mundo"
print(re.findall(r"mundO$", text , re.IGNORECASE))  # Coincide con "mundo"


# 4) [] : Define una clase de caracteres, por ejemplo, [a-z] coincide con cualquier letra minúscula.
import re
text = "Hola Mundo"
print(re.findall(r"[a-z]", text))  # Coincide con todas las letras minúsculas


# 5) [^] : Negación dentro de una clase de caracteres, por ejemplo, [^a-z] coincide con cualquier carácter que no sea una letra minúscula.
import re
text = "Hola Mundo 123!"
print(re.findall(r"[^a-z]", text))  # Coincide con espacios, números y caracteres especiales


# 6) | : Operador OR, permite alternar entre diferentes opciones, por ejemplo, "a|b" coincide con "a" o "b".
import re
text = "Hola"
print(re.findall(r"[a-z]|[0-9]", text))  # Coincide con "o" , "l" , "a"


# 7) () : Agrupación, permite agrupar parte de la expresión para aplicar operadores sobre ellos.
import re
text = "123 321abc"
print(re.findall(r"([0-9]+)", text))  # Coincide con "123"

# 8) ? : Hace que el carácter anterior sea opcional (0 o 1 vez).
import re
text = "Hola"
print(re.findall(r"Ho?la", text))  # Coincide con "Hola"  --> Busca opcional a la "o" (0 - 1 vez)


# 9) * : Coincide con el carácter anterior 0 o más veces.
import re
text = "Hoooooola"
print(re.findall("Ho*l", text))  # Coincide con "Hooooo"


# 10) + : Coincide con el carácter anterior 1 o más veces.
import re
text = "Hoooola"
print(re.findall("Ho+l", text))  # Coincide con "Hooool"


# 11. {n} : Coincide con exactamente n repeticiones del carácter anterior.
import re
text = "aaabbb"
print(re.findall(r"a{3}", text))  # Coincide con "aaa"


# 12) {n,} : Coincide con n o más repeticiones del carácter anterior.
import re
text = "aaabbb"
print(re.findall("a{2,}", text))  # Coincide con "aaa"


# 13. {n,m} : Coincide con entre n y m repeticiones del carácter anterior.
import re
text = "aaaabbbb"
print(re.findall("a{2,4}", text))  # Coincide con "aaaa"


# 14) \ : Escapa caracteres especiales, como . o *.
import re
text = "Hola. ¿cómo estás?"
print(re.findall(r"\.", text))  # Coincide con el punto "."


# 5) \d : Coincide con cualquier dígito (equivalente a [0-9]).
import re
text = "Mi número es 1234"
print(re.findall("\d", text))  # Coincide con "1", "2", "3", "4"


# 16) \D : Coincide con cualquier carácter que no sea un dígito.
import re
text = "Mi número  @ es 1234"
print(re.findall("\D", text))  # Coincide con ['M', 'i', ' ', 'n', 'ú', 'm', 'e', 'r', 'o', ' ', ' ', '@', ' ', 'e', 's', ' ']


# 17) \w : Coincide con cualquier carácter de palabra (letras, números y guiones bajos).
import re
text = "Hola_mundo 123"
print(re.findall("\w", text))  # Coincide con  ['H', 'o', 'l', 'a', '_', 'm', 'u', 'n', 'd', 'o', '1', '2', '3']


# 18. \W : Coincide con cualquier carácter que no sea de palabra.
import re
text = "Hol@_mundo 123!"
print(re.findall("\W", text))  # Coincide con ['@', ' ', '!']


# 19) \s : Coincide con cualquier espacio en blanco (espacio, tabulación, salto de línea).
import re
text = "\tHola mundo\nCuidate"
print(re.findall("\s", text))  # Coincide con ['\t', ' ', '\n']


# 20) \S : Coincide con cualquier carácter que no sea un espacio en blanco.
import re
text = "Hol@ mundo 12 3"
print(re.findall("\S", text))  # Coincide con ['H', 'o', 'l', '@', 'm', 'u', 'n', 'd', 'o', '1', '2', '3']


# 21) \b : Coincide con un límite de palabra (inicio o final de una palabra).
import re
text = "Hola mundo"
print(re.findall(r"\bHola\b", text))  # Coincide con "Hola"


# 22) \B : Coincide con cualquier lugar que no sea un límite de palabra.
import re
text = "aHolam mundo"
print(re.findall(r"\BHolA\B", text, re.IGNORECASE))  # Coincide con "lo" en "Hola"


# 23) \n : Coincide con un salto de línea.
import re
text = "Hola\nmundo"
print(re.findall("\n", text))  # Coincide con el salto de línea 


# 24) \t : Coincide con una tabulación.
import re
text = "Hola\tmundo"
print(re.findall("\t", text))  # Coincide con la tabulación


# 25) (?=...) : Aseguramiento positivo.
import re
text = "Hola mundo"
print(re.findall("a(?=\s)", text))  # Coincide con "a" solo si está seguida de un espacio en líneaa, salto de línea o tabulación


# 26) (?!...) : Aseguramiento negativo.
import re
text = "Hola mundo"
print(re.findall("a(?!m)", text))  # Coincide con "a" solo si no está seguida de "m"


# 27) (?:...) : Agrupación sin captura.
import re
text = "123abc"
print(re.findall("(?:\d+)", text))  # Coincide con "123" pero no captura el grupo


# 28) (?P<name>...) : Captura con nombre.
import re
text = "123abc"
print(re.findall(r"(?P<String>[a-z]+)", text))  # Captura de la a-z como "String"


# 29) (?i) : Modificador que hace que la expresión sea insensible a mayúsculas/minúsculas.
import re
text = "hola"
print(re.findall("(?i)HOLA", text))  # Coincide con "hola", insensible a mayúsculas


# 30) (?m) : Modificador de modo multilínea.
import re
text = "Hola\nmundo"
print(re.findall("(?m)^m", text))  # Coincide con "m" al inicio de la segunda línea


# 31) (?s) : Modificador de modo dotall.
import re
text = "Hola\nmundo"
print(re.findall("(?s)Hola.mundo", text))  # Coincidirá con ['Hola\nmundo']