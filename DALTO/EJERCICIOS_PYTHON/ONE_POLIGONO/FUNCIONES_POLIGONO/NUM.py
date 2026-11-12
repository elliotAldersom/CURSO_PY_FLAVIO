""" 
FUNCIÓN PARA PEDIR LOS NÚMEROS
"""
import sys
sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.INTERFAZ import Interfaz
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.CUADRADO import Cuadrado
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.RECTANGULO import Rectangulo
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.TRINGULO import Triangulo

def Num(name_poligono):
    
        while True:
                if((name_poligono == "1") or (name_poligono == "cuadrado")):
                        while True:
                                try:
                                        num = float(input("Ingrese la medida del lado del cuadrado: "))
                                        if(num <= 0):
                                                raise ZeroDivisionError
                                except ValueError:
                                        print("Cracter no válido")
                                except ZeroDivisionError:
                                        print("La medida del lado debe ser mayor a 0")
                                except KeyboardInterrupt:
                                        print("\nCaracter no válido")
                                else:
                                        print("Medida válida")
                                        num = round(num,2)
                                        cuadrado_num_str = f"{str(num)}^2"
                                        return cuadrado_num_str,num
                                       # print(f"El área del cuadrado {cuadrado_num_str} es: {Cuadrado(num)}")
                                
                elif((name_poligono == "2") or (name_poligono == "rectángulo") or (name_poligono == "rectangulo")):
                        while True:
                                try:
                                        num_1 = float(input("Ingrese la medida de la base del rectángulo: "))
                                        if(num_1 <= 0):
                                                raise ZeroDivisionError
                                except ValueError:
                                        print("Cracter no válido")
                                except ZeroDivisionError:
                                        print("La medida de la base debe ser mayor a 0")
                                except KeyboardInterrupt:
                                        print("\nCaracter no válido")
                                else:
                                        print("Medida válida")
                                        num_1 = round(num_1,2)
                                        base_num_str = str(num_1)
                                        break
                        while True:
                                try:
                                        num_2 = float(input("Ingrese la medida de la altura del rectángulo: "))
                                        if(num_2 <= 0):
                                                raise ZeroDivisionError
                                except ValueError:
                                        print("Cracter no válido")
                                except ZeroDivisionError:
                                        print("La medida de la altura debe ser mayor a 0")
                                except KeyboardInterrupt:
                                        print("\nCaracter no válido")
                                else:
                                        print("Medida válida")
                                        num_2 = round(num_2,2)
                                        altura_num_str = str(num_2)
                                        
                                        # Retorna los valores después de ambos inputs
                                        return (f"{base_num_str} x {altura_num_str}"),num_1,num_2,"rectángulo"
                                        #print(f"El área del rectángulo {base_num_str} * {altura_num_str} es: {Rectangulo(num_1, num_2)}")
                
                elif((name_poligono == "3") or (name_poligono == "triángulo") or (name_poligono == "triangulo")):
                        while True:
                                try:
                                        num_1 = float(input("Ingrese la medida de la base del triángulo: "))
                                        if(num_1 <= 0):
                                                raise ZeroDivisionError
                                except ValueError:
                                        print("Cracter no válido")
                                except ZeroDivisionError:
                                        print("La medida de la base debe ser mayor a 0")
                                except KeyboardInterrupt:
                                        print("\nCaracter no válido")
                                else:
                                        print("Medida válida")
                                        num_1 = round(num_1,2)
                                        base_num_str = str(num_1)
                                        break
                        while True:
                                try:
                                        num_2 = float(input("Ingrese la medida de la altura del triángulo: "))
                                        if(num_2 <= 0):
                                                raise ZeroDivisionError
                                except ValueError:
                                        print("Cracter no válido")
                                except ZeroDivisionError:
                                        print("La medida de la altura debe ser mayor a 0")
                                except KeyboardInterrupt:
                                        print("\nCaracter no válido")
                                else:
                                        print("Medida válida")
                                        num_2 = round(num_2,2)
                                        altura_num_str = str(num_2)
                                        
                                        # Retorna los valores después de ambos inputs
                                        return (f"({base_num_str} x {altura_num_str})/2"),num_1, num_2,"triángulo"
                                        #print(f"El área del triángulo ({base_num_str} * {altura_num_str})/2 es: {Triangulo(num_1, num_2)}")
                
                elif((name_poligono == "4") or (name_poligono == "salir")):
                        return "Saliendo del programa"
                else:
                        print("Opción no válida, intenta de nuevo.")
                        name_poligono = Interfaz()


