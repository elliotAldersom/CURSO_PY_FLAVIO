

v1=v2=0

while((v1==v2 or v2==v1)):
  v1=float(input("ingrese el primer valor: "))
  v2=float(input("ingrese el segundo valor: "))

v0=v1  #v0 guarda el valor de v1
v1=v2  #v1 guarda el valor de v2
v2=v0  #v2

print(v1)
print(v2)