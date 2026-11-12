donacion=float(input("ingrese la donación :  "))
medicina_general=0.45
cardiologia=0.30
pediatria=0.15
traumatologia=0.10

monto_mg=donacion*medicina_general
monto_c=donacion*cardiologia
monto_p=donacion*pediatria
monto_t=donacion*traumatologia

print("Lo que recibe medicina general es  " + str(monto_mg)+"\n")
print("Lo que le corresponde a cardiologia es  " + str(monto_c)+"\n")
print("Lo que rrcibe pediatria es  "+ str(monto_p) +"\n")
print("Lo que recibe traumatologia es  " + str(monto_t) +"\n")