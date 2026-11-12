nombre=(input("INGRESE EL NOMBRE DE USUARIO:"))
precio=float(input("INGRESE EL PRECIO DEL PRODUCTO:   "))
descuento=0.11*precio 
unidades=int(input("INGRESE LA CANTIDAD DE UNIDADES:  "))

monto_original=precio
monto_descuento=descuento
monto_pagar=precio-descuento
monto_total=monto_pagar*unidades

print("EL PRECIO ORIGINAL DEL PRODUCTO ES:  " + str(monto_original) + "  POR UNIDAD.")
print("EL MONTO DEL DESCUENTO ES:  "  + str(monto_descuento) + "  POR UNIDAD.")
print("EL MONTO A PAGAR ES:  " + str(monto_pagar)+ "  POR UNIDAD.")
print("EL MONTO TOTAL A PAGAR ES:  " + str(monto_total))
print("GRACIAS POR SU COMPRA:  " + str(nombre)  + ".")
