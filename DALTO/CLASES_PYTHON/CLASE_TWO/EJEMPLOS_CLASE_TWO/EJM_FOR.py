"""
EJEM DE BUCLE FOR:

"""

a = list(["manzana", "pera", "fresa","mango"]);

b = list(["pollo", "chancho", "ress","pescado"]);

for carne,frutas in zip(b,a):
    print("Para este tipo de carne: " + str(carne) + ", come esta fruta: " + str(frutas))


for num in range(5):
    print(num)

for num in  range(2,10):
    print(num)

# forma incorrecta de recorrer una lista / tupla:

a_2 = len(a);
b_2 = len(b);

for frutas in range(a_2):
   print("la fruta es: " + str(a[frutas]));

# forma correcta de recorrer una lista / tupla:
for carne in enumerate(b):
    print("el tipo de carne es: "+ str(carne))
    indice = carne[0]
    valor = carne[1]
    print("el tipo de carne es: "+ str(valor) + ", y el índice en el que se encuentra es: " + str(indice));
else:
    print("No hay más tipos de carne")

