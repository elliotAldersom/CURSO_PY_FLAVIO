sigue=1  #TRUE

while(sigue==1):
    sigue=2  #VALOR QUE PERMITE QUE EL BUCLE FUNCIONE
    while(not(0<=sigue<=1)):
        sigue=int(input("DESEA SEGUIR (1) -->  ")) #COMPROBANTE
    
    if(sigue==1):
        print("EL PROCESO CONTINUA -->  ")  #LA RESPUESTA SI ES TRUE
    elif(sigue==0) :
        print("EL PROCESO SE DETIENE -->  ") #LA RESPUESTA FALSE
        break
