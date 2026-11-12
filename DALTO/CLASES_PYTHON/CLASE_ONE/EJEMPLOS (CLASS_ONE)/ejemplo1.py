"""EJERCICIO -->
1) int (input("  "))   NUMEROS ENTEROS
2) float(input(" "))   NUMEROS DECIMALES
3) (input(" "))   CADENAS DE TEXTO"""

#EJERCICIO 1 -->

monto=float(input("INGRESE EL MONTO DE EQUIPO -->  "))
letra=int(input("INGRESE EL NUMERO DE LETRAS A PAGAR -->  "))
incremento=0.19
interes=0.05

monto_pagar=monto*(1+incremento)
#monto_pagar=monto*1.19

monto_mensual=monto_pagar/letra
pago=round(monto_mensual*(1+interes))
#pago=monto_mensual*1.05

print("EL PAGO MENSUAL ES ---> "+ str(pago))

