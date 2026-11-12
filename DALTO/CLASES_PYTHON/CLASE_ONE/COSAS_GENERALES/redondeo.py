from decimal import Decimal, ROUND_HALF_UP # Usamos esto pues de esta forma redondeamos de manera más precisa.

numero_1 = (input("Ingresa el numero decimal: ")) #ejm 2.675 - Lo registramos como string

numero = Decimal(numero_1)
redondeado = numero.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
print("El número redondeado es este: " + str(redondeado))  # Salida: 2.68



# Para sumar

numero_2 = input("Ingresa el numero decimal: ");

numeros = Decimal(numero_2);

suma = numero + numeros ;

redondeado2 = suma.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP);
print("La suma es: " + str(redondeado2))