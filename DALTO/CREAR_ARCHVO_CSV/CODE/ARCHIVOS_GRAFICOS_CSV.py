import sys 
sys.path.append("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO")

import pandas as pd

# Importar los módulos:

from DALTO.CREAR_ARCHVO_CSV.CLASES.VERSION_2_0_FINAL import ArchivoCSV # --> CLASE
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Achivos_CSV import Seleccionar_csv_en_pc as Seleccionar_CSV # --> FUNCION
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Interfaz import Interfaz # --> FUNCIONES
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Grafico_Barras import Barras # --> FUNCIÓN 1
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Grafico_Lineal import Lineal # --> FUNCIÓN 2
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Grafico_Dispersion import Dispersion # --> FUNCIÓN 3
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Grafico_Bigotes import Bigotes # --> FUNCIÓN 4 
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Grafico_Circular import Circular # --> FUNCIÓN 5


# IMPORTAR LOS MÓDULOS PARA LA CONSULTA
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Interfaz_Consultas import Interfaz_Consulta # --> Interfaz
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Todos_Datos import Datos_Tablas # --> FUNCIÓN 1
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Una_Columna import Mostrar_Una_Columna # --> FUNCIÓN 2 
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Mas_Columnas import Mostrar_Varias_Columnas # --> FUNCIÓN 3
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Columnas_Head import Mostrar_Con_Head # --> FUNCIÓN 4
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_columnas_Tail import Mostrar_Con_Tail # --> FUNCIÓN 5
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostrar_Por_Id import Mostrar_Por_ID # --> FUNCIÓN 6
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Mostar_Por_Coincidencia import Mostrar_Coincidencias # --> FUNCIÓN 7
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Ordenar_Por_Columna import Ordenar_Y_Guardar # --> FUNCIÓN 8
from DALTO.CREAR_ARCHVO_CSV.FUNCIONES.Sumar_Dato import Sumar_Columnas # --> FUNCIÓN 9


def Gestion_De_Archivos():
    # CREAR O ABRIR EL ARCHIVO CSV
    while True:
        try:
            print("Bienvenido al sistema de \"Gestión de Archivos CSV\"")
            opcion = input("¿Qué deseas hacer? \n1. Crear un archivo CSV \n2.Abrir un Archivo CSV\nIngrese una de las opciones: ").strip().lower()
            if opcion in ["1", "crear un archivo csv" , "crear"]:
                ruta = ArchivoCSV()
                df = pd.read_csv(ruta)
                break
            elif opcion in ["2", "abrir un archivo csv", "abrir"]:
                ruta_buscar = Seleccionar_CSV()
                df = pd.read_csv(ruta_buscar)
                break
            else: 
                print("Opción no válida...")
                continue
        except ValueError:
            print("Se creó el archivo CSV correctamente.\nPor favor, ingrese una de las opciones...")
        except (KeyboardInterrupt, EOFError):
            print("\nPor favor ingrese una de las opciones...")
 
    # DEFINIR CONSULTAS ACTIVAS PARA EL APARTADO DE CONSULTAS:
    #consultas_activas = False # --> False inicialmente (comentado pues no lo usaré...)
    # USAR EL INTERFAZ
    while True:
        try:
            opcion = Interfaz()
            if opcion == "1":
                Barras(df)
            elif opcion == "2":
                Lineal(df)
            elif opcion == "3":
                Dispersion(df)
            elif opcion == "4":
                Bigotes(df)
            elif opcion == "5":
                Circular(df)
            elif opcion == "6":
                print("Te vamos a dirigir a las consultas...")
                #consultas_activas = True # --> True si decide entrar a las consultas
                
                # ACÁ VERÁ EL APARTADO DE CONSULTAS
                while True:
                    opcion = Interfaz_Consulta()
                    if opcion == 1 :
                        result = Datos_Tablas(df)
                        print(result)
                    elif opcion == 2:
                        result = Mostrar_Una_Columna(df)
                        print(result)
                    elif opcion == 3:
                        result = Mostrar_Varias_Columnas(df)
                        print(result)
                    elif opcion == 4:
                        result = Mostrar_Con_Head(df)
                        print(result)
                    elif opcion == 5:
                        result = Mostrar_Con_Tail(df)
                        print(result)
                    elif opcion == 6:
                        result = Mostrar_Por_ID(df)
                        print(result)
                    elif opcion == 7:
                        result = Mostrar_Coincidencias(df)
                        print(result)
                    elif opcion == 8:
                        result = Ordenar_Y_Guardar(df)
                        print(result)
                    elif opcion == 9:
                        result = Sumar_Columnas(df)
                        print(result)
                    elif opcion == 10:  
                        break
                
            elif opcion == "7":
                return("👋 Saliendo del sistema. ¡Hasta pronto!")
                
            else:
                print("❌ Opción inválida. Intente de nuevo...")
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Entrada interrumpida. Intente nuevamente...")
    
    
    
                       
            
print(Gestion_De_Archivos())