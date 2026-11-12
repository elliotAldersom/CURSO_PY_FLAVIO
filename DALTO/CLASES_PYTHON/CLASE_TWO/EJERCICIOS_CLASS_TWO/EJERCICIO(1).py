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
cantidad = int(input("INGRESE LA CANTIDAD DE ALUMNOS QUE SE VAN A REGISTRAR: "))

def obtener_compañeros(cantidad_1):
    compañeros = []

    for i in range(cantidad_1): 
        nombre = input(f"INGRESE EL NOMBRE DEL ALUMNO {i +1}: ")
        nombre = nombre.strip()
        nombre = nombre.capitalize()
        edad = int(input(f"INGRESE LA EDAD DEL ALUMNO \"{nombre}\": "))
        compañero = (nombre, edad)
        compañeros.append(compañero)
        print(f"ALUMNO REGISTRADO: {nombre} - EDAD: {edad}")
        i += 1
        compañeros.sort(key = lambda x : x[1])
    ordenado = f"LISTADO DE ALUMNOS ORDENADOS DE MENOR A MAYOR:\n {compañeros}"
    final = f"El estudiante que será el profesor es {compañeros[-1][0]}\nEl estudiante que será el asistente es {compañeros[0][0]}"
    return ordenado, final

listado, final = obtener_compañeros(cantidad)
print(f"{final}")

#total = obtener_compañeros(cantidad)
#print(f"LISTADO DE ALUMNOS ORDENADOS DE MENOR A MAYOR:\n {total}")
#print(f"El estudiante que será el profesor es {total[-1][0]}\nEl estudiante que será el asistente es {total[0][0]}")

    

