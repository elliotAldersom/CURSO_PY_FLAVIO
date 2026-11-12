
import sys
sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.CUADRADO import Cuadrado
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.TRINGULO import Triangulo
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.RECTANGULO import Rectangulo
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.NUM import Num 
from DALTO.EJERCICIOS_PYTHON.ONE_POLIGONO.FUNCIONES_POLIGONO.INTERFAZ import Interfaz
def Poligono():
    while True:
        opcion = Interfaz()
        resultado = Num(opcion)
        if(isinstance(resultado, str) and (resultado == "Saliendo del programa")):
            return(resultado)
        elif(len(resultado) == 2):
            str_result,lado = resultado
            print(f"El área del cuadrado {str_result} es: {Cuadrado(lado)}")
        elif((len(resultado) == 4) and  (resultado[3] == "rectángulo")  ):
            str_result,base,altura,string = resultado
            print(f"El área del {string} {str_result} es: {Rectangulo(base= base, altura=altura)}")
        elif((len(resultado) == 4) and ((resultado[3] == "triángulo"))):
            str_result,base,altura,string = resultado
            print(f"El área del {string} {str_result} es: {Triangulo(base= base, altura=altura)}")
        
            


print(Poligono())