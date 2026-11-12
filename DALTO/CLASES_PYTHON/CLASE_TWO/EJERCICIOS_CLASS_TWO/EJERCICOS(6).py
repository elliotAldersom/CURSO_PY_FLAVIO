"""
HOY FALTÓ EL PORFESOR DE CLASES Y LOS CHICOS SE ORGANIZARON PARA ARMAR LA SUYA PROPIA
UNO DE LOS ALUMNOS VA A SER EL PROFESOR
Y OTRO VA SER SU ASISTENTE.
OBJETIVOS:

A) PEDIR EL NOMBRE Y LA EDAD DE LOS COMPAÑEROS QUE VINIERON HOY 
A CLASE Y ORDENAR LOS DATOS DE MENOR A MAYOR.

B) EL MAYOR ES EL PROFESOR Y EL MENOR ES EL ASISTENTE
¿QUIEN ES EL PROFESOR Y EL ASISTENTE?

"""

compañeros = int(input("Ingrese el número de alumnos a registrar: "));

def cantidad(alumnos):
    
    listado = []
    i = 0
    while(i < alumnos):
        nombre = input(f"Ingrese el nombre del alumno {i+1}: ")
        nombre = nombre.strip()
        nombre = nombre.capitalize()
        edad = int(input(f"Ingrese la edad del alumno {nombre}: "))
        tupla = nombre, edad
        listado.append(tupla)
        print(f"El alummno {nombre} acaba de ser agregado a la lista:)")
        i += 1
    
    listado.sort(key= lambda x : x[1])
    resultado = f"El alumno que hará de profesor es {listado[-1][0]}, y el alumno que será su asistente es {listado[0][0]}"
    return resultado

print(cantidad(compañeros))