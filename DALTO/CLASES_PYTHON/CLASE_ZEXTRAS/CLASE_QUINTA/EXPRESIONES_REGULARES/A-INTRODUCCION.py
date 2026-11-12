# A partir de ahora veremos u pequeño curso de Expresiones Regulares (REGEX) 
# En mi caso el objetivo es: 
""" 
Aprender expresiones regulares e implementarlo al sistema o agenda
de contactos para los números telefónicos:
- El user ingresa así: 123456789
- Pero al mostrarse será así: 123-456-789 
""" 

print("__________________________________________________________________________________")
print("\t\t\tExpresiones Regulares (REGEX)")
print("__________________________________________________________________________________\n")

print("""¿Qué es una Expresión Regular
- Las Expresiones Regulares son una herramienta para encontrar patrones en el texto.
- Validar información ingresada por el usuario.
- Extraer partes del texto.
- Distinguir números, letras, caracteres especiales.
- Hacer Scraping de páginas de Internet. 


DATO:
- En Python trabajaremos con la librería RE. (import re)

ESTRUCTURA: 
- Caracteres Especiales + Reglas de Sintaxis.\n___________________________________________________________________________\n""")



""" 
DATO ANTES DE EMPEZAR: 

-r'' se usa para definir cadenas crudas donde las barras invertidas \ no son tratadas como caracteres de escape, 
lo cual es esencial para escribir patrones de expresiones regulares de manera sencilla.
Sin r'', las barras invertidas tienen que ser duplicadas (por ejemplo, \\d en lugar de \d), 
lo que hace que las expresiones regulares sean más complicadas de escribir.
"""
