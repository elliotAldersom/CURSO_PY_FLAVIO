
#EJERCICIO 6


clave=input("INGRESE LA CLAVE DEL SISTEMA  -->  ")
intento=int(input("INGRESE EL NUMERO DE INTENTOS MÁXIMOS -->  "))
i=0

while(i<intento):

    i=i+1   #contador
    prueba=input("INGRESE LA CONTRARSEÑA -->   ")
    
    if(prueba==clave):  #DETERMINAR SI SON IGUALES
        print("CONTRASEÑA CORRECTA")
        break
    else:
        print("VUELVA INTENTAR")

if(i==3): # REFERENTE AL CONTADOR, CUANDO EL # DE INTENTOS ES 3
    print(" NUMERO DE INTENTOS AGOTADOS")



    