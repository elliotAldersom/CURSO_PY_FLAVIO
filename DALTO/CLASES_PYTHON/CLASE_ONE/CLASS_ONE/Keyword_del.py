
""" 
 VAMOS A VER COMO USAR EL del
 
"""
 # En objetos
class Stack:
    def __init__(self):
         self.__stack_list = []


    def push(self, val):
        self.__stack_list.append(val)


    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val


stack_object = Stack()


stack_object.push(3)
stack_object.push(2)
stack_object.push(1)
print(stack_object._Stack__stack_list)
# [3, 2, 1]

print(stack_object.pop())
print(stack_object.pop())
print(stack_object.pop())


""" 
Podemos usarlo para borrar variables enteras, lista y diccionarios
- Pero no se puede en tupla, string, set
"""
# Eliminar una variable:
x = 5
del x  # Elimina la variable x


# Eliminar un valor de una lista
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(lista)
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
val = lista[-1]
del lista[-1]
print(val) # 10
print(lista)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]    
print(lista[-1]) # 9

# Eliminar un rango de elementos
rango = lista[:4]
del lista[:4]
print(lista)
# [5, 6, 7, 8, 9]
print(rango)
# [1, 2, 3, 4]

rango = lista[2:4]
del lista[2:4]
print(lista)
# [5, 6, 9]
print(rango)
# [7, 8]

# Eliminar clves en diccionario:
dic = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print(dic)
del dic['a']  # Elimina la clave 'a'
print(dic)

# Para borrar el valor de un dic, puede ser así o en None
dic["d"] = "" # Podemos poner None, pero al iprimmir saldrá None
print(dic)



