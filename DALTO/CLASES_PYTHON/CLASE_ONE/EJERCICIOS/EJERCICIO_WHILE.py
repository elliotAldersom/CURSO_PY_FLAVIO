#EJERCICIO 1
sigue=1

while(True):
   
    canti1=canti2=canti3=-1

    while(canti1<0):
        canti1=float(input("INGRESE EL MONTO DEL PRIMERO -->  "))
   
    while(canti2<0):
        canti2=float(input("INGRESE EL MONTO DEL SEGUNDO -->  "))
    
    while(canti3<0):
        canti3=float(input("INGRESE EL MONTO DEL TERCERO -->  "))


    total=canti2+canti3+canti1

    # OPERATIVA -->  

    p1=round(( canti1/total)*100,2)
    p2=round((canti2/total)*100,2)
    p3=round((canti3/total)*100,2)

    #LECTURA DE DATOS -->

    print("EL % DEL PRIMERO --> " + str(p1))
    print("EL % DEL SEGUNDO --> " + str(p2))
    print("EL % DEL TERCERO --> " + str(p3))
    
    sigue=(input("DESEA SEGUIR (1) -->  "))

    if(sigue!="1"):
       print("FIN DEL PROGRAMA")
       break
