""" 
ACÁ HAREMOS EL CÓDIGO DE LA CALCULADORA COMO TAL,
IMPORTANDO LOS MÓDULOS DEL PAQUETE FUNCIONES
"""

import sys 

sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")

print("\nBIENVENIDO, ESTÁS DENTRO DE LA CALCULADORA")
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Interfaz import Interfaz
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Suma import Adicion # 1
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Resta import Sustraccion # 2
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Multiplicacion import Producto # 3
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Division import Fraccion # 4
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Potencia import Potenciacion # 5
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Raiz import Radicacion # 6
from DALTO.CARPETA_CALCULADORA.FUNCIONES.Factoriales import Factorial # 7


while True:
    opcion =Interfaz()
    
    if((opcion == "suma") or (opcion == "1")):
        result = Adicion()
        print(result)
    elif((opcion == "resta") or (opcion == "2")):
        result = Sustraccion()
        print(result)
    elif((opcion == "multiplicación") or (opcion == "3") or (opcion == "multiplicacion")):
        result = Producto()
        print(result)
    elif((opcion == "división") or (opcion == "4") or (opcion == "division")):
        result = Fraccion()
        print(result)
    elif((opcion == "potencición") or (opcion == "5") or (opcion == "potenciacion")):
        result = Potenciacion()
        print(result) 
    elif((opcion == "radicación") or (opcion == "6") or (opcion == "radicacion")):
        result = Radicacion()
        print(result) 
    elif((opcion == "factorial") or (opcion == "7")  ):
        result = Factorial()
        print(result) 
    elif((opcion == "salir") or (opcion == "8")):
        print("🚪🚶 Saliendo de la calculadora")
        break
    else:
        print("🤖 🚫 La opción no es válida par realizar alguna de las operaciones.")
        continue