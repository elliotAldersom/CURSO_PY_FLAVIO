# Detectando un número CABA y ocultandolo (número telefónico con código de país)
import re

texto = "Hola Pedro, mi número de teléfono es: +51 941 611-934 o sino 934-234-123"

pattern = r"(\+\d{1,3}(\s|-))?\d{1,3}(\s|-)\d{1,3}(\s|-)\d{1,3}" # --> Para validar el número del país ya que pueden ser de 1, 2 o 3 digitos

reempalzo = re.sub(pattern, "(número oculto)", texto)
print(reempalzo)

""" 
Otra forma:
pattern = r"\+?\d{1,3}(\s|-)?\d{1,3}(\s|-)?\d{1,3}(\s|-)?\d{1,3}"
print(reemplazo)
"""
