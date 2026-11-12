""" 
/*
 * EJERCICIO:
 * - Muestra ejemplos de creación de todas las estructuras soportadas por defecto
 *   en tu lenguaje.
 * - Utiliza operaciones de inserción, borrado, actualización y ordenación.
 *
 * DIFICULTAD EXTRA (opcional):
 * Crea una agenda de contactos por terminal.
 * - Debes implementar funcionalidades de búsqueda, inserción, actualización
 *   y eliminación de contactos.
 * - Cada contacto debe tener un nombre y un número de teléfono.
 * - El programa solicita en primer lugar cuál es la operación que se quiere realizar,
 *   y a continuación los datos necesarios para llevarla a cabo.
 * - El programa no puede dejar introducir números de teléfono no numéricos y con más
 *   de 11 dígitos (o el número de dígitos que quieras).
 * - También se debe proponer una operación de finalización del programa.
 */
"""

# Estructuras por defecto:
# 1) Listas
my_list = [1, 2, 3, 4, 5 , "Hola" , "Python" , "Hola" , "Hola"]
print("Lista:", my_list)
print("Agreagando un elemento a la lista al final: 'Nuevo elemento al final'")
my_list.append("Nuevo elemento al final")
print(my_list)
print("Agregando un elemento a la lista en la posicion 2: 'Nuevo elemento en la posicion 2'")
my_list.insert(2, "Nuevo elemento en la posicion 2")
print(my_list)
print("Agregando otra lista al final de la lista: [6,7,8] , lo agrega al final de la lista original")
new_list = [6, 7, 8]
my_list.extend(new_list)
print(my_list)
print("Eliminando un elemento de la lista: 'Hola', solo la primera ocurrencia")
my_list.remove("Hola")
print(my_list)
print("Eliminando un elemento de la lista en la posicion 3: Usamos el comando del o pop()")
del my_list[3]
print(my_list)
my_list.pop(-1)  # Elimina el último elemento
print(my_list)
print("Contando cuantas veces aparece 'Hola' en la lista:")
print(my_list.count("Hola"))

print("Actualizar un elemento de la lista en la posicion 0:")
my_list[0] = "Elemento actualizado"
print(my_list)

print("Obteniendo el indice de un elemento en la lista: 'Python'")
print(my_list.index("Python"))

print("Ordenando con sort() y luego con sort(key = len ,reverse = False) y luego con reverse()")
my_list_numbers = [5, 2, 9, 1, 5, 6]
print("Lista de numeros antes de ordenar:", my_list_numbers)
my_list_numbers.sort()
print("Lista de numeros despues de ordenar:", my_list_numbers)

my_list_strings = ["banana", "apple", "cherry"]
print("Lista de strings antes de ordenar:", my_list_strings)
my_list_strings.sort()
print("Lista de strings despues de ordenar:", my_list_strings)

print(f"La primera lista original es: \n{my_list}")
my_list.sort(key= str, reverse=False)
print(f"La primera lista ordenada alfabeticamente es:\n{my_list}")

my_list_str = [x for x in my_list if isinstance(x, str)]
my_list_str.sort(key=len)
print(my_list_str)
print(f"La primera lista ordenada por longitud (solo texto) es:\n{my_list}")

my_list.sort(key=lambda x: len(str(x)), reverse= True)
print(f"Ordenado por longitud, pero pasando todo a texto, vamos a invertirlo con parámetro de reverse = True: \n{my_list}")

my_list.reverse()
print("Lista invertida por seguna vezz con reverse():\n", my_list)
print(type(my_list))
print("\n__________________________________________________________\n")

# 2) Tuplas
my_tuple = (1, 2, 3, 4, 5 , "Hola" , "Python")
print("Tupla:", my_tuple)
print(my_tuple[2])
print(type(my_tuple))