"""
Pedir que los alumnos ingresen su nombre y su edad,
ordenarlos por edad,
escoger al mayor como profesor y al menor como su asistente.
"""


def listado_alumnos(num):
    lista = []
    i = 0 
    while(i < num):
        name = input(f"Ingrese el nombre del {i + 1} alumno: ")
        name = (name.strip()).capitalize()
        age = int(input(f"Ingrese la edad de {name}: "))
        tupla = name, age
        lista.append(tupla)
        print(f"{name} de {age} años de edad acaba de ser agregado exitosamente.")
        i += 1 
    
    lista_ordenada = sorted(lista, key = lambda x : x[1]) # ORDENA LA LISTA, LA FUNCIÓN SORTED ENTREGA UNA LISTA NUEVA, NO LA MODIFICA A LA ORIGINAL
    mensaje = f"El alumno que hará de maestro es {lista_ordenada[-1][0]} porque es el mayor con la edad de {lista_ordenada[-1][1]} años.\nY el alumno que hará de asistente es {lista_ordenada[0][0]}, pues es el menor con la edad de {lista_ordenada[0][1]} años."
    
    return mensaje

num = int(input("Ingrese el número de alumnos a registrar: "))
resultado = listado_alumnos(num)
print(resultado)