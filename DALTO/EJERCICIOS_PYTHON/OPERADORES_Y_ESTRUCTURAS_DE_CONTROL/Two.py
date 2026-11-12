""" 
/*
 * EJERCICIO:
 * - Crea ejemplos utilizando todos los tipos de operadores de tu lenguaje:
 *   Aritméticos, lógicos, de comparación, asignación, identidad, pertenencia, bits...
 *   (Ten en cuenta que cada lenguaje puede poseer unos diferentes)
 * - Utilizando las operaciones con operadores que tú quieras, crea ejemplos
 *   que representen todos los tipos de estructuras de control que existan
 *   en tu lenguaje:
 *   Condicionales, iterativas, excepciones...
 * - Debes hacer print por consola del resultado de todos los ejemplos.
 *
 * DIFICULTAD EXTRA (opcional):
 * Crea un programa que imprima por consola todos los números comprendidos
 * entre 10 y 55 (incluidos), pares, y que no son ni el 16 ni múltiplos de 3.
 *
 * Seguro que al revisar detenidamente las posibilidades has descubierto algo nuevo.
 */
"""

# OPERADORES:
# Aritméticos:

# Suma (+)
print(f"Suma: {3+2}\nResta: {12-1}\nMultiplicación: {2*3}\nDivisión: {12/4}\nDivisión baja: {12//5}\nMódulo: {12%5}\nPotencia: {2**3}")

# Comparación:
print(f"Igualdad: {10 == 3}\nDistinto: {12 != 10}\nMayor o igual: {12>=2}\nMenor o igual: {12<= 3}\nMayor: {1>2}\nMenor: {3<4}")

# Lógicos:
print(f"And / && : {(10 + 3 == 13) and (14+1 == 15)}\nOr / || : {(12 == 10) or (10 == 10)}\nNot ! : {not(12==12)}")

# Asignación: 
num = 11 # asignación (el igual asigna un valor)
print(num)
num += 12
print(num)
num -=12 
print(num)
num *=3 
print(num)
num /= 3 
print(num)
num %=4 
print(num) # imprime 3
num +=8 # 11
num //= 2 
print(num) # 5
num **= -1 # 5**-1
print(num) # 0.2
num *=10
num **= 2
#RAÍZ:
num **= 1/2 
print(num) # 2.0


# Identidad: Sirve para comparar el valor de la posición en memoria de la variable
new_num = 2.0
print(f"Num: {num}")
print(f"new_num is num: {new_num is num}")
print(f"new_num is not num: {new_num is not num}")

new_num = num 
print(f"new_num is num: {new_num is num}")

print(f"new_num is not num: {new_num is not num}")

# Pertenecia:
print(f"'f' in 'flavio' : {"f"  in "flavio"}")
print(f"'f' not in 'flavio' : {"f" not in "flavio"}")

# bit:
a = 10 # 1010 en bit
b = 3  # 0011 en bit
print(f"AND: 10 & 3 = {10 & 3}") # 0010 --> 2 en bit
print(f"OR: 10 | 3 = {10 | 3}") # 1011 --> 11 en bit
print(f"XOR: 10 ^ 3 = {10 ^ 3}") # 1001 --> 9 en bit
print(f"NOT: ~10 = {~10}") # Invierte cada valor bit que compone al número: -11
print(f"Desplazamiento a la derecha: 10 >> 2 =  {10 >> 2}") # 0010 --> 2
print(f"Desplazamiento a la izquierda: 10 << 2 =  {10 << 2}") # 101000 --> 40