from decimal import Decimal, ROUND_HALF_UP
# Operadores aritméticos:
v0 = (input("Oe pa, ingresa pues el valor uno ok?: "))
v00 = (input("Oe pa, ingresa pues el valor dos ok?: "))

v1 = v0.replace("," , ".");
v2 = v00.replace("," , ".");

print("SUMA:");

suma = Decimal(v1) + Decimal(v2) ;
suma_1 = suma.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)
print("La suma es: " + str(suma_1));
print("______________________________________________________________________________");


print("RESTA:");

resta = Decimal(v1) - Decimal(v2) ;
resta_1 = resta.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La resta es: " + str(resta_1));
print("______________________________________________________________________________");


print("MUTIPLICACIÓN:");

multiplicacion = Decimal(v1) * Decimal(v2) ;
multiplicacion_1 = multiplicacion.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La mutplicación es: " + str(multiplicacion_1));
print("______________________________________________________________________________");


print("DIVISIÓN:");

división = Decimal(v1) / Decimal(v2) ;
división_1 = división.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La división es: " + str(división_1));
print("______________________________________________________________________________");


print("DIVISIÓN BAJA:");

división_baja = Decimal(v1) // Decimal(v2);
división_baja_1 = división_baja.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La división baja es: " +str(división_baja_1));
print("______________________________________________________________________________");


print("MODULO:");

modulo = Decimal(v1) % Decimal(v2);
modulo_1 = modulo.quantize(Decimal("0.00"),rounding = ROUND_HALF_UP);
print("El módulo es: " + str(modulo_1));
print("______________________________________________________________________________");


print("RADICACIÓN:");

raiz_1 = Decimal(v1) **(1/ Decimal(v2));
raiz_01 = raiz_1.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La raíz " + str(v2) + " de " + str(v1) + " es: " + str(raiz_01));
print("______________________________________________________________________________");

raiz_2 = Decimal(v2) ** (1/Decimal(v1));
raiz_02 = raiz_2.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La raíz " + str(v1) + " de " + str(v2) + " es: " +str(raiz_02));
print("______________________________________________________________________________");

print("POTENCIA:");

potencia = Decimal(v1) ** Decimal(v2);
potencia_1 = potencia.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP);
print("La potencia es: " + str(potencia_1))

print("______________________________________________________________________________");