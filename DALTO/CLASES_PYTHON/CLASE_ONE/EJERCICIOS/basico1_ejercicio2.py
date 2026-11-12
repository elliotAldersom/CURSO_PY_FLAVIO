alumnos_total=int(input("¿CUÁNTOS ALUMNOS SON EN TU SALÓN?:  "))
varones=int(input("¿CUÁNTOS VARONES SON EN TU SALÓN?:  "))
damas=int(input("¿CUÁNTAS DAMAS SON EN TU SALÓN?:  "))

hombres=(varones/alumnos_total)*100
mujeres=(damas/alumnos_total)*100
print("EL % DE VARONES EN TU SALÓN ES DE "+ str(hombres))
print("EL % DE MUJERES EN TU SALÓN ES DE " + str(mujeres))
print("GRACIAS POR EL REGISTRO DE TU SALÓN. SALUDOS! :)")
