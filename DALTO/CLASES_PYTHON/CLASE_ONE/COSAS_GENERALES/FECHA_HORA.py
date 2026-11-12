# EJERCICIO: OBTENER FECHA Y HORA ACTUALES EN EL SISTEMA.
import datetime # --> FUNCIONES PARA TRABAJAR CON FECHAS Y HORAS.
ahora = datetime.datetime.now()
#print(ahora) # --> IMPRIME LA FECHA Y HORA ACTUAL.

print(type(ahora))

print(ahora.strftime("%d/%m/%Y  %H:%M:%S"))

