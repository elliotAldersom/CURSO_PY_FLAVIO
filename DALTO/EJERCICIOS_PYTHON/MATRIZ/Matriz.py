while True: 
    try: 
        print("Si ingresas un número decimal, se pasará al entero más cercano")
        filas = float(input("Ingrese el número de filas: "))
        if filas <= 0:
            print("No puede ser menor o igual a 0")
            continue
    except ValueError:
        print("No es un número")
    except KeyboardInterrupt:
        print("\nDebe de ser un número.")
    except EOFError: 
        print("\nCaracter no válido.")
    else: 
        print("Número válido")
        filas = int(filas)
        break

while True: 
    try: 
        print("Si ingresas un número decimal, se pasará al entero más cercano")
        columnas = float(input("Ingrese el número de columnas: "))
        if columnas <= 0:
            print("No puede ser menor o igual a 0")
            continue
    except ValueError:
        print("No es un número")
    except KeyboardInterrupt:
        print("\nDebe de ser un número.")
    except EOFError: 
        print("\nCaracter no válido.")
    else: 
        print("Número válido")
        columnas = int(columnas)
        break
    

lista = []

for f in range(filas):
    fila_agregada = []
    for c in range(columnas):
        while True:
            try: 
                elemento = input(f"Ingrese el elemento  agregar a la matriz en el índice ({f},{c}): ")
                elemento = elemento.strip()
                if (len(elemento) == 0):
                    print("El elemento no puede ser vacío")
                    continue
            except KeyboardInterrupt:
                print("\nDebe de ser un número o una letra.")
            except EOFError:
                print("\nCaracter no válido.")
            else: 
                #elemento = elemento.strip()
                if (elemento.isnumeric()):
                    elemento = float(elemento)
                elif (elemento.isalpha()):
                    elemento = elemento.capitalize()
                fila_agregada.append(set([elemento]))
                print("Fila agregada.")
                break
    lista.append(fila_agregada)

# RECORRIENDO LA LISTA SIN INTERCAMBIAR EL PRIMER Y ÚLTIMO ELEMENTO: POR FILAS
print("\nRECORRIENDO LA LISTA SIN INTERCAMBIAR EL PRIMER Y ÚLTIMO ELEMENTO: POR FILAS\n")
for fila in lista:
    print(fila)

# Intercambiar solo la primera y la última fila
lista[0], lista[-1] = lista[-1], lista[0]

# RECORRIENDO LA LISTA YA INTERCAMBIADA:
print("\nRECORRIENDO LA LISTA YA INTERCAMBIADA:\n")   
for fila in lista:
    print(fila)