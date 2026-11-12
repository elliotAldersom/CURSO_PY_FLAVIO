# 1. FullName 
nombre_completo = "Flavio Gerardo Silva Estrada" 
alias = "Elliot Alderson" 

print(f"Nombre Completo: {nombre_completo}")
print(f"Alias: {alias}")

# 2. Año actual y edad 
anio_actual = 2026 
edad = 19 

print(f"Año Actual: {anio_actual} | Edad: {edad}")

# 3. precio_gasolina => float 
precio_gasolina = 23.50 
print(f"El precio de la gasolina es: {precio_gasolina}\nEl valor es de tipo: {type(precio_gasolina)}")

# 4. según la edad crear variable es_mayor_de_edad (bool)
es_mayor_edad = edad >= 18
print(type(es_mayor_edad))

print(f"El usuario {nombre_completo} {'es mayor de edad' if es_mayor_edad else 'no es mayor de edad'}") 

# 5. Declarar 3 variables en una linea (desempaquetamiento de tuplas)
username, email, num_phone = "elliotAlderson", "fsociety@gmail.com", 923476128
print(f"Username: {username} | Email: {email} | Num Phone: {num_phone}")

x,y,z = 10, 20, 30 
print(f"La suma de 'x' : {x} + 'y': {y} + 'z' : {z} = {x + y + z}")

# ==== ==== ==== ==== 
# REGLAS DE NOMBRADO Y BUENAS PRÁCTICAS 

# 6. Identifica por qué la variable 1er_lugar = "Juan" genera un error de sintaxis en Python.
# Corrige el nombre usando una regla válida (ej. primer_lugar ) e imprímela.

# 1er_lugar = "Juan" => lanza error de SyntaxError 

# Las variables no empiezan con números 
primer_lugar = "Juan"
print(primer_lugar)

# 7. snake_case para almacenar cantidad de estudiantes en un aula 
canti_estudiantes_aula = 30 
print(f"La cantidad de estudiantes que hay en el aula es de {canti_estudiantes_aula}")

# 8. variables: precio y Precio con valores distintos 
precio = 23.5 
Precio = 12.5 
print(precio) 
print(Precio)

# 9. Corrige el siguiente nombre no recomendado aplicando estándares limpios de Python:
# val1tot=1500 . Usa nombres descriptivos con guiones bajos.

valor_total = 1500
print(valor_total)

# 10. Declara una variable utilizando una palabra reservada de forma incorrecta (por ejemplo,
# intenta nombrar a una variable class = "Python" ), lee el error en Google Colab y luego asígnale
# un nombre correcto como nombre_clase.

# class = 'Python' => 'class' es usado para crear una clase 

nombre_clase = 'Python'
print(f"Nombre de la clase: {nombre_clase}")

# Constantes (snake_case en Mayúsculas) y Casting  

# 11. Declara una constante global para el valor de PI utilizando la convención de constantes en
# Python (todo en mayúsculas con snake_case: VALOR_PI = 3.1416 ). Imprímela.

VALOR_PI = 3.1416 
print(f"El valor de PI es: {VALOR_PI}")

# 12. Define una constante para la velocidad máxima permitida en una vía urbana:
# VELOCIDAD_MAXIMA_URBANA = 60 . Úsala en un mensaje descriptivo impreso.

VELOCIDAD_MAXIMA_URBANA = 60 
print(f"La velocidad máxima en esta vía es de {VELOCIDAD_MAXIMA_URBANA}km/h.")

# 13. Dada una variable de texto con un número, por ejemplo calificacion_texto = "95" ,
# conviértela a entero usando int() , súmale 5 puntos y muestra el resultado final.

calificacion_text = "95" 
calificacion_num = int(calificacion_text) 
calificacion_final = calificacion_num + 5
print(f"El resultado final de la calificación es {calificacion_final}")

# 14. Crea una variable numérica entera llamada stock_productos con valor 12 . Conviértela a tipo
# texto (string) utilizando str() y concaténala en una frase descriptiva.

stock_productos = 12 
stock_productos_description ="En el almacen quedan" + str(stock_productos) + "productos." 
print(stock_productos_description)

# 15. Escribe un mini programa que solicite un precio en formato de texto decimal 
# (ej. precio_str = "129.99" ), lo convierta a tipo float , 
# le calcule un impuesto del 18% y muestre el total final en consola.

precio_str = input("Ingrese el precio en soles (S/.) del producto: ")
precio_float = float(precio_str) 
IGV = 0.18 
precio_final = precio_float * (1 + IGV)

print(f"Precio final: {precio_final} - incluido el 'igv'")