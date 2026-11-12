# Importamos todo de la librería de tkinter (*)
from tkinter import *

# LLAMA A LA CLASE Tk()
raiz = Tk() 

# CAMBIAR NOMBRE DE LA VENTANA:
raiz.title("Ventana de Inicio")

# INIICAR SI SE PUEE O NO MOVER LA FORMA DE LA VENTANA (alargar / encoger)
# EL FALSE  ES QUE NO Y TRUE QUE SÍ
# EN MI CASO LO DEJ EN TRUE
raiz.resizable(True, True) # --> (X : False , Y : True) --> (Ancho : False , Alto : True)

# CAMBIAR EL ÍCONO DE LA VENTANA (debe de ser de extensión .ico):
# PONEMOS LA RUTA DEL ARCHIVO .ico
raiz.iconbitmap("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\INTERFAZ_GRAFICA\\inicio.ico")

# PARA QUE EL USUARIO VISUALICE LA PANTALLA COMO QUEREMOS:
raiz.geometry("650x500") # --> (X: 650 , Y: 350) --> (Ancho: 650 , Alto: 350)

# PONER COLOR DE FONDO:
raiz.config(bg= " green")

# PARA VER Y EJECUTAR LA VENTANA:
# SIEMPRE VA AL FINAL DE TODO:
raiz.mainloop()