v1=v2=0

while((v1==v2)):
 v1=float(input("Ingrese el primer valor:  "))
 v2=float(input("Ingrese el segundo valor:  "))
 
# Intecambio de Valores (para ello s necesario tener otra variable)
v0=v1 
v1=v2
v2=v0

print(v1)
print(v2)
print(v0)
