"""EL TIEMPO PARA VER LOS CONCEPTOS DE PYTHON EN UN CURSO DE CORRIDO ES DE:
- 2.5 HORAS (MÍNIMO) (DOS HORAS Y MEDIAS)
- 7 HORAS (MÁXIMO)
- 4 HORAS (PROMEDIO)
MIENTRAS ESTE CURSO LO LOGRÓ EN : 1.5 HORAS (HORA Y MEDIA)."""
# A) DIFERENCIA EN PORCENTAJE ENTRE EL CURSO ACTUAL Y:
# EL MÁS RÁPIDO Y MÁS LENTOS DE LOS OTROS CURSOS.
# EL PROMEDIO DE LOS CURSOS

# B) TENIENDO EN CUENTA QUE EL PROMEDIO DE LOS OTROS CURSOS ES DE 5 HORAS Y CON EDICIÓN LO CONVIERTEN A 4 HORAS
# Y EN ESTE CURSO ES DE 3.5 HORAS (TRES HORAS Y MEDIA) Y CON EDICIÓN ES DE 1.5 HORAS (HORA Y MEDIA):
# PORCENTAJE DE MATERIAL INSERVIBLE QUE SE REDUCE EN AMBOS CASOS.

# C) VER 10 HORAS DE ESTE CURSO A CUANTAS DE OTROS CURSOS EQUIVALE? Y VER 10 HORAS DE OTRO CURSO A CUANTO EQUIVALE DE ESTE CURSO?


#RESOLUCIÓN:

tiempo_curso_rapido = 2.5
curso_lento = 7
curso_promedio = 4
curso_actual = 1.5


# A) Diferencia de % del curso actual y los demás:


resultado1 = 100 - ((curso_actual * 100)/tiempo_curso_rapido) 
resultado2 = 100 - ((curso_actual * 100)/curso_lento) 
resultado3 = 100 -((curso_actual * 100)/curso_promedio)

print("La diferencia de porcentaje entre el curso actual y los demás es de:")
print("-  " + str(resultado1) + " % con respecto al curso más el más rápido.")
print("-  " + str(resultado2) + " % con respecto al curso más lento.")
print("-  " + str(resultado3) + " % con respecto al promedio de los curso.")
print(" ")
print("____________________________________________________________________________________________________")
print(" ")

# B) Porcentaje de crudo que se deja de lado o se borra de ambos casos (del promedio y de este curso):

crudo_del_curso_promedio = 5
crudo_del_curso_actual = 3.5

porcentaje_excluido_promedio = 100 - ((curso_promedio * 100)/ crudo_del_curso_promedio)
porcentaje_excluido_actual = 100 - ((curso_actual * 100)/crudo_del_curso_actual)

print("El porcentaje de crudo no usado en ambos casos es de: ")
print("-  " + str(porcentaje_excluido_promedio) + " % del promedio de los otros cursos.")
print("-  " + str(porcentaje_excluido_actual) + " % de este curso.")
print(" ")
print("____________________________________________________________________________________________________")
print(" ")

# C) VER 10 HORAS DE ESTE CURSO A CUANTAS DE OTROS CURSOS EQUIVALE? Y VER 10 HORAS DE OTRO CURSO A CUANTO EQUIVALE DE ESTE CURSO?
edquivalente1 = (curso_promedio/curso_actual)*10
equivalente2 = (curso_actual/curso_promedio)*10

print("EQUIVALENTES DE 10 HORAS EN CADA CURSO: ")
print( "-  Ver 10 horas de este curso equivale a " + str(edquivalente1) + " horas de otros cursos.")
print("-  Ver 10 horas de otros cursos equivale a " + str(equivalente2) + " horas de este curso.")
print(" ")
print("_________________________________________________________________________________________________________")
print(" ")