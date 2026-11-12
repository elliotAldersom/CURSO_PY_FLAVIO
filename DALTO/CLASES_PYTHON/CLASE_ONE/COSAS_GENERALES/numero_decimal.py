from decimal import Decimal, ROUND_HALF_UP 

v1 = input("Ingrese el primer valor: ")
v2 = input("Ingrese el segundo valor: ") 
  

suma = Decimal(v1) + Decimal(v2);
adicion = suma.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La suma es " + str(adicion))


