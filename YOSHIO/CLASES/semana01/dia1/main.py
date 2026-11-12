# Vale en el día 1 solo vimos instalación de Python 
# Lo que veremos ahora es parte de la sesión 02 

# Definir variables de tipos

# RULES VARIABLES: 
# 1. NO pueden empezar con un número 
# 2. Solo contienen letras, números y guión bajo, sin Ñ o tildes (á, é, í, ó, ú) 
# 3. La convención para análisis de datos es usar snake_case => nombre_variable 
# 4. Una constante por convención es todo en mayúsculas => NOMBRE_CONST 

text = "Texto" 

entero = 9 

flotante = .5 # 0.5  

booleano = True # => 1  | False => 0 

# Ver el tipo de una variable => función type(variable)
print(type(text)) # <class 'str'>
print(type(entero)) # <class 'int'>
print(type(flotante)) # <class 'float'>
print(type(booleano)) # <class 'bool'>


# Casting => cambiar el tipo de una variable a otro tipo 
print(int(flotante)) # 0 => elimina los decimales y deja lado entero
print(float(entero)) # 9.0
print(str(entero)) # "9"
print(bool(0)) # False
print(bool(1)) # True 
print(bool("")) # False => cadena vacía
print(bool(" ")) # True => cadena con espacio 
print(bool("Texto")) # True => cadena con texto
print(bool([9])) # True => lista con un elemento
print(bool([])) # False => lista vacía
print(bool(None)) # False => valor nulo
print(bool(9)) # True => cualquier número distinto de 0 es True

# ALGO QUE SEA VACÍO O NULO => False | algo que tenga contenido => True

# Pedir datos al usuario => función input() 
nombre = input("Ingrese su nombre: ") # input() => by default return type String (str) 
edad = int(input(f"{nombre}, ahora ingresa tu edad: ")) # int(input()) => return Integer (int)
print(f"Bienvenido {nombre}, tu edad es {edad} años") # f-string => interpolación de variables en un string