from decimal import Decimal, ROUND_HALF_UP

print("ALCULADORA\nOperadores aceptados (+ , - , * , / , ** , **1/x)");
a = input("Igrese el primer valor: ");
operador = input("Ingrese el tipo de opearción a desaroollar: ");
b = input("Ingrese el segundo valor: ");

v1 = Decimal(a);
v2 = Decimal(b);

if (operador.strip() == "+"):
    suma = v1 + v2
    print("La suma es: " + str(suma.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
elif (operador.strip() == "-"):
    resta = v1 - v2
    print("La resta es: " + str(resta.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
elif (operador.strip() == "*"):
    producto = v1 * v2
    print("El producto es: " + str(producto.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
elif (operador.strip() == "/"):
    division = v1 / v2
    print("La división es: " + str(division.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
elif (operador.strip() == "**"):
    potencia = v1 ** v2
    print("La potencia es: " + str(potencia.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
elif (operador.strip() == "**1/x"):
    raiz = v1 ** (1/v2)
    print("La raíz es: " + str(raiz.quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)));
else:
    print("operador no aceptado.");
