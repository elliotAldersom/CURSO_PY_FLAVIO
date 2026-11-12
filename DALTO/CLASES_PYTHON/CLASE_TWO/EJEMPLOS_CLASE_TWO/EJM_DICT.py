name = input("ingresa tu nombre: ");
last_name = input("ingresa tu apellido: ");
name_completo = name + " " + last_name
a = dict(name = name, apellido = last_name )
print(a)

t = "name","last name"
a_1 = dict(t = name_completo)
print(a_1)

nombre_apellido = input("Ingresa tu primer nombre y tu apellido parterno: ");
t_1 = nombre_apellido.split(" ")
t_2 = frozenset(t_1)

a_2 = {
    t[0]: t_1[0],
    t[1] : t_1[1]
}

print(a_2)

t_3 = frozenset(["nombre", "apellido"])
a_3 ={
    t_2 : t_3
}
print(a_3)
