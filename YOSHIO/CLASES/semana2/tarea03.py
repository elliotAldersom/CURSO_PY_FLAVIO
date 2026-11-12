categoria = input("Ingrese la categoría, puede ser 'regular', 'VIP', 'empleado': ").strip().lower()

monto_compra = float(input("Ingrese el monto de compra en 'S/.': "))
descuento_decimal = 0.

if(monto_compra < 0): 
    print("NO se puede aplicar descuento pues no compró nada...")

elif(categoria == 'regular'): descuento_decimal = 0.05

elif(categoria == 'vip'): descuento_decimal = 0.2

elif(categoria == 'empleado'): descuento_decimal = 0.3

else: print("Su categoría no cuenta con descuentos...")

monto_final = monto_compra * (1 -descuento_decimal ) if (monto_compra > 0) else None
result = f"Descuento de un {round((descuento_decimal * 100))}%: S/. -{round((monto_compra * descuento_decimal), 2)} | Monto Finla: S/.{round(monto_final,2)} " if (monto_compra > 0) else "Sin descuentos, porque no compró nada."
print(result)