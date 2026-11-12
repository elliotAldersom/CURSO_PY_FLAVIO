import random


# Con esto hacemos que muestre un número aleatorio entre 1 y 100
print(random.randrange(1,100))


# Mostrar números decímales aleatorios:                  
valor_deimal =random.uniform(1,10)
print(round(valor_deimal,2))

# MOSTRAR NÚMEROS PARES:
print(random.randrange(0,100,2))

# AHORA CON LISTAS:
# Podemos usar en este caso una lista o tupla (el set no, l lista no sé, no lo pruebo)
concursantes = ["Juan", "Pedro", "Luis", "Carlos"]

ganador = random.choice(concursantes)

print(f"El ganador es: {ganador}")

# ELEGIR A MÁS DE 1 GANADOR DE LA LISTA O TUPLA:
# Podemos elegir a N concurantes pero: 
# N <= len(lista) and not(N <0) 
# N no puede ser mayor al número de elementos o menor a 0 
concursantes = ["Juan", "Pedro", "Luis", "Carlos"]
N = 3
ganadores = random.sample(concursantes,N)
ganadores = ", ".join(ganadores)
print(f"Y los ganadores son... {ganadores}")


# PEQUEÑO EJERCICIO:
# HACER UNA CONTRASEÑA ALEATORIA:

letras = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
numero = "0123456789"
signos = "!@#$%^&*()_{}:<>?"

todo_junto = f"{letras}{numero}{signos}"
longitud = 10 

contra = random.sample(todo_junto, longitud) # --> Devuelve una Lista []

# ELIMINANDO LOS CORCHETES DE LA LISTA [ ]
contra = "".join(contra)
print(f"Tu contraseña es: {contra}")


# OTRA FORA DE HACER UNA CONTRASEÑA ALEATORIA:
letras = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
numero = "0123456789"
signos = "!@#$%^&*()_\/{}<>?"

longitud = 10 

# caracter = random.sample(letras,4)
# num_caracter = random.sample(numero,4)
# signo_caracter = random.sample(signos,2)

# extension = caracter + num_caracter + signo_caracter

# pasword = "".join(extension)

# print(f"New contra: {pasword}")

# GENERAMOS LA CONTRA
extension = random.sample(letras,4) + random.sample(numero,4) + random.sample(signos,2)

# Mezclando aleatoriamente el orden del pasword:
random.shuffle(extension)  # 🔄 Mezcla el orden

# Eliminando los corchetes de la lista []
pasword = "".join(extension)

print(f"New contra: {pasword}")

""" 
Mezclamos el orden con: random.shuffle(extension)
y eliminamos los corchetes CON pasword = "", join(extension)

Ahora el mezclar va antes del:
pasword = "".join(extension)

ya que no se puede realzar esta accion después de pasarlo a string

"""



# FUNCIONES DE RANDOM:

# 1) random.randrange(1,4)
print(random.randrange(1,4))
""" 
- Esto hace que tome algún número entero
que esté en el rango de 1 - 4 (no incluye al 4)
"""
print("___________________________________________________________")

# 2) random.randint(1,4)
num = random.randint(1,4)
print(num)
""" 
- Esto hace que tome algún número entero
que esté en el rango de 1 - 4 (incluye al 4)
"""
print("___________________________________________________________")
# 3) random.choice()
concursantes = ["Juan", "Pedro", "Luis", "Carlos"]

ganador = random.choice(concursantes)

print(f"El ganador es: {ganador}")

""" 
Devuelve un elemento de aleatorio de 
una lista, tupla y str (String)

EJM:
print(random.choice([10, 20, 30]))  # Ej: 20

print(random.choice(('rojo', 'verde', 'azul')))  # Ej: 'azul'

print(random.choice("Python"))  # Ej: 't'

"""
print("___________________________________________________")
# 4) random.choices(population, weights=None, k=1)
# Devuelve una lista con k elementos aleatorios, seleccionados de population, 
# con posibilidad de repetir.

# EJM SIN WEIGHTS:
print(random.choices(['a', 'b', 'c'], k=5))
# Ejemplo de salida: ['b', 'a', 'a', 'c', 'b']

# EJM CON WEIGHTS:
print(random.choices(['a', 'b', 'c'], weights=[10, 1, 1], k=5))
# Muy probable que salga más veces 'a'

""" 
¿Qué significa weights?
- Es una lista de probabilidades relativas para cada elemento.
-No son porcentajes, sino valores proporcionales.
-Cuanto mayor el peso, mayor la probabilidad de que ese elemento sea elegido.

En el ejemplo anterior:
a tiene un peso de 10, por lo que tiene una probabilidad 10 veces mayor que b y c
"""


valores = ['🍎', '🍌', '🍇']
pesos = [8, 1, 1]

print(random.choices(valores, weights=pesos, k=10))
# Salida:
# ['🍎', '🍎', '🍎', '🍎', '🍎', '🍎', '🍇', '🍇', '🍎', '🍎']
print("________________________________________________")


# 5) random.sample(population, k)
# Devuelve una lista con k elementos aleatorios, seleccionados de population,
# sin posibilidad de repetir
concursantes = ["Juan", "Pedro", "Luis", "Carlos"]
N = 3
ganadores = random.sample(concursantes,N)
ganadores = ", ".join(ganadores)
print(f"Y los ganadores son... {ganadores}")

""" 
Podemos elegir a N concurantes pero: 
N <= len(lista) and not(N <0) 
N no puede ser mayor al número de elementos o menor a 0 


DATO:
ganadores = ", ".join(ganadores)
con esto eliminamos los corchetes []
y separamos los elementos por comas ( , ) 
y si queremos sin comas ( , ) 
sería así: "".join(ganadores)
"""