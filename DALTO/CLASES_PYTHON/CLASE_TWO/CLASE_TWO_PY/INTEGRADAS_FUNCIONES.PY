"""
FUNCIÓN : UNA FUNCIÓN ES UN FRAGMENTO DE CÓDIGO QUE PODEMOS REUTILIZAR
EN CUAQUIER DE OTRO MOMENTO SIN TENER QUE ESCRIBIR EL CÓDIGO UNA Y OTRA VEZ.

- PODEMOS DECIR QUE UNA FUNCIÓN ES UN FRAGMENTO DE CÓDIGO QUE EJECUTA UNA
TAREA ESPECÍFICIA LA CUAL PODEMOS USAR NOSOTROS PARA FACILITAR EL CÓDIGO.
ventajas:
- La reducción de código, ya que la función ya contiene ese frámento de código.

- La reutilización del código, ya que podemos llamar a la función en cualquier momento.

- La moduladidad, ya que permite separar el programa en partes más pequeñas y manejables
y después poder incluso probarlas aparte y que esto no afecte al programa (se puede 
modificar y volver a integrar al progama).

- Hacer que el código sea más mantenible y se pueda depurar más sencillo, porque el cambio
que queremos hacer tenemos simplemente ir a esa función en específico hacemos el cambio
y ya va a estar en todas las llamadas de la función reflejado ese cambio.

- Hace que el código sea más legible.

"""

# 1) build_in : 

numeros = set([4,7,1,42,15]) # ---> Puede ser: tuple, list, set , dict (iterables)
d01 = dict(n1 = 2, n2 = 34, n3 = 24, n4 = 456, n5 = 70, n6 = 82)

# --> ENCONTRANDO EL NÚMERO MAYOR DE UNA LISTA.
# ---> Usamos la función: max() --> FUNCIONA CON NÚMEROS.
numero_mas_alto = max(numeros)
print("El número más alto de la lista/tupla/set es: " + str(numero_mas_alto));
print("El número más alto de tu dict es: " + str(max(d01.values())));
# --> ENCONTRANDO EL NÚMERO MENOR DE UNA LISTA.
# ---> Usamos la función: min() --> FUNCIONA CON NÚMEROS.
numero_menor = min(numeros)
n_min = min(d01.values())
print("El número más bajo de la lista/tupla/set es: " + str(numero_menor));
print("El número más bajo de tu dict es: " + str(n_min));


# REDONDEANDO A "x" DECIMALES: con la función --> round()

numero = 123.389567
redondeo = round(numero,2) # ---> round((variable del número), (cuanto decimales queremos))
print("El número redondeado a 2 decimales es: " + str(redondeo))

# Retorna un False --> si le pasamos un: 0, vacío, False, ninguno (None), listas, tuple, set

resultado_bool = bool(0)
print(resultado_bool)

resultado_bool = bool()
print(resultado_bool)

resultado_bool = bool(None)
print(resultado_bool)

resultado_bool = bool([])
print(resultado_bool)

resultado_bool = bool(())
print(resultado_bool)

resultado_bool = bool({})
print(resultado_bool)
print("________________________")

# Retorna un True --> si le pasamos un: distinto a 0, True, cadena de texto, listas, tuple, set
# Función: bool()

resultado_bool = bool(-1) # --> -1 != 0 = True
print(resultado_bool)

resultado_bool = bool("Flavio")
print(resultado_bool)

resultado_bool = bool([1,"GSE"])
print(resultado_bool)

resultado_bool = bool((1,"GSE"))
print(resultado_bool)

resultado_bool = bool({1,"GSE"})
print(resultado_bool)
print("________________________")


# Retorna True si todos los valores son verdaderos:
# Función: all() --> COMPRUEBA LO QUE ESTÁ DENTRO DE UN ITERABLE.
# La función all() en Python se utiliza para verificar
# si todos los elementos de un iterable (como una lista, tupla, conjunto, etc.) son verdaderos. 
# Si todos los elementos son evaluados como True, entonces all() devuelve True. 
# Si al menos uno de los elementos es evaluado como False, devuelve False.
# Ejemplo: all([True, True, True]) --> True
# Ejemplo: all([True, False, True]) --> False

print(all("FLAVIO"))

resultado_all = all([234, "true", [344,23], {"name" : "Flavio"}]) # --> Es un diccionario no vacío y se considera True (lo digo por si hay dudas)
print(resultado_all)

resultado_all = all([0, "true", [344,23]])
print(resultado_all) # --> False porque: 0 --> False.

resultado_all = all([234, "true", [344,0]])
print(resultado_all) # --> True porque la lista: [344,0] --> no es una lista vacía.

resultado_all = all([234, "true", [344,None]])
print(resultado_all) # --> True porque la lista: [344,None] --> no es una lista vacía.

print("________________________")

# Sumando todos los elementos de una lista, tuple, set, dict numérica.
# Función: sum()

lista = [2,3,4,6,7,8]
print(sum(lista))

tupla = (2,3,4,6,7,8)
print(sum(tupla))

seting = {2,3,4,6,7,8}
print(sum(seting))

d1 = dict(n1 = 2, n2 = 3, n3 = 4, n4 = 6, n5 = 7, n6 = 8)
print(sum(d1.values()))

d2 = {
    "n1" : 2,
    "n2" : 3,
    "n3" : 4,
    "n4" : 6,
    "n5" : 7,
    "n6" : 8
}

print(sum(d2.values()))

print("________________________")

