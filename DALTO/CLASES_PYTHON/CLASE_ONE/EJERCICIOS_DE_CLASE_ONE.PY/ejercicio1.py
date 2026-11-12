"""EL TIEMPO PARA VER LOS CONCEPTOS DE PYTHON EN UN CURSO DE CORRIDO ES DE:
- 2.5 HORAS (MÍNIMO) (DOS HORAS Y MEDIAS)
- 7 HORAS (MÁXIMO)
- 4 HORAS (PROMEDIO)
MIENTRAS ESTE CURSO LO LOGRÓ EN : 1.5 HORAS (HORA Y MEDIA)."""
# A) DIFERENCIA EN PORCENTAJE ENTRE EL CURSO ACTUAL Y:
# EL MÁS RÁPIDO Y MÁS LENTOS DE LOS OTROS CURSOS.
# EL PROMEDIO DE LOS CURSOS

# B) TENIENDO EN CUENTA QUE EL PROMEDIO DE LOS OTROS CURSOS ES DE 5 HORAS Y CON EDICIÓN LO CONVIERTEN A 4 HORAS
# Y EN ESTE CURSO ES DE 3.5 HORAS (TRES HORAS Y MEDIA) Y CON EDICIÓN ES DE 1,5 HORAS (HORA Y MEDIA):
# PORCENTAJE DE MATERIAL INSERVIBLE QUE SE REDUCE EN AMBOS CASOS.

# C) VER 10 HORAS DE ESTE CURSO A CUANTAS DE OTROS CURSOS EQUIVALE? Y VER 10 HORAS DE OTRO CURSO A CUANTO EQUIVALE DE ESTE CURSO?


#RESOLUCIÓN:

# A) Diferencia de duración en %

# porcentaje en relación al curso más rápido:


tiempo_curso_actual = 1.5

tiempo_del_curso_mas_rapido = 2.5

difererncia_porcentaje= 100 - (tiempo_curso_actual/tiempo_del_curso_mas_rapido*100)

print("--------------------")

print("El curso actual dura un " + str(difererncia_porcentaje) + " % menos que el más rápido. ")


# porcentaje en relación al curso más lento:


tiempo_curso_actual = 1.5

tiempo_del_curso_mas_lento = 7

diferencia_porcentajes2 = 100 - (tiempo_curso_actual/tiempo_del_curso_mas_lento*100)

print("El curso actual dura un " + str(diferencia_porcentajes2) + " % menos que el más lento.")


# poecentaje en relación al promedio de los cursos:

tiempo_curso_actual = 1.5

tiempo_promedio = 4

diferencia_porcentaje3 = 100 - (tiempo_curso_actual/tiempo_promedio*100)

print("El curso actual dura un " + str(diferencia_porcentaje3) + " % menos que el tiempo promedio de los otros cursos.")

print("--------------------")

# B) porcentaje de material inservible (crudo = video sin editar) que se reduce en ambos casos:

# caso 1: otros curso de 5 a 4 horas
otros_cursos_tiempo_total = 5

otros_cursos_tiempo_total_edicion = 4

otros_cursos_porcentaje_reducido = 100-(otros_cursos_tiempo_total_edicion/otros_cursos_tiempo_total*100) #si me pide saber con cuanto material me quedo sería = (otros_cursos_tiempo_total_edicion*100)/otros_cursos_tiempo_total

print("El porcentaje de contenido reducido en otros cursos es de " + str(otros_cursos_porcentaje_reducido) + " %.")

# caso 2: curso actual de 3.5 a 1.5 horas

curso_actual_tiempo_total = 3.5

curso_actual_tiempo_editado = 1.5

curso_actual_porcentaje_reducido = 100-(curso_actual_tiempo_editado/curso_actual_tiempo_total*100) #si me pide saber con cuanto material me quedo sería = (curso_actual_tiempo_editado*100)/curso_actual_tiempo_total

print("El porcentaje de contenido reducido en el curso actual es de " + str(curso_actual_porcentaje_reducido) + " %.")

print("--------------------")

# C) VER 10 HORAS DE ESTE CURSO A CUANTAS DE OTROS CURSOS EQUIVALE? Y VER 10 HORAS DE OTRO CURSO A CUANTO EQUIVALE DE ESTE CURSO?

curso_actual = 1.5

curso_rapido = 3.5

curso_lento = 7

curso_promedio = 4

equivalemte1 = (curso_promedio/curso_actual)*10

equivalente2 = (curso_actual/curso_promedio)*10

print("Ver 10 horas de este curso equivale a " + str(equivalemte1) + " horas promedias de otros cursos.")
print("Ver 10 horas de otro curso equivale a " + str(equivalente2) + " horas de este curso.")

print("--------------------")