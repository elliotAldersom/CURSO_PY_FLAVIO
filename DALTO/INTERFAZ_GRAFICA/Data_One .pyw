""" 
CLASE 1 - RAÍZ
"""

# Importamos todo de la librería de tkinter (*)
# from tkinter import *

# # LLAMA A LA CLASE Tk()
# raiz = Tk() 

# # CAMBIAR NOMBRE DE LA VENTANA:
# raiz.title("Ventana de Inicio")

# # INDICAR SI SE PUEDE O NO MOVER LA FORMA DE LA VENTANA (alargar / encoger)
# # EL FALSE  ES QUE NO Y TRUE QUE SÍ
# # EN MI CASO LO DEJÉ EN TRUE
# raiz.resizable(True, True) # --> (X : False , Y : True) --> (Ancho : False , Alto : True)

# # CAMBIAR EL ÍCONO DE LA VENTANA (debe de ser de extensión .ico):
# # PONEMOS LA RUTA DEL ARCHIVO .ico
# raiz.iconbitmap("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\INTERFAZ_GRAFICA\\inicio.ico")

# # PARA QUE EL USUARIO VISUALICE LA PANTALLA COMO QUEREMOS:
# raiz.geometry("650x500") # --> (X: 650 , Y: 350) --> (Ancho: 650 , Alto: 350)

# # PONER COLOR DE FONDO:
# raiz.config(bg= "#00FFFF")

# PARA VER Y EJECUTAR LA VENTANA:
# SIEMPRE VA AL FINAL DE TODO:
#raiz.mainloop()


""" 
CLASE 2 - FRAME
"""

# Importamos todo de la librería de tkinter (*)
from tkinter import *

# LLAMA A LA CLASE Tk()
raiz = Tk() 

# CAMBIAR NOMBRE DE LA VENTANA:
raiz.title("Ventana de Inicio")

# INDICAR SI SE PUEDE O NO MOVER LA FORMA DE LA VENTANA (alargar / encoger)
# EL FALSE  ES QUE NO Y TRUE QUE SÍ
# EN MI CASO LO DEJÉ EN TRUE
raiz.resizable(True, True) # --> (X : False , Y : True) --> (Ancho : False , Alto : True)

# CAMBIAR EL ÍCONO DE LA VENTANA (debe de ser de extensión .ico):
# PONEMOS LA RUTA DEL ARCHIVO .ico
raiz.iconbitmap("C:\\Users\\Administrador\\Pictures\\CURSO_PY_FLAVIO\\INTERFAZ_GRAFICA\\inicio.ico")

# PARA QUE EL USUARIO VISUALICE LA PANTALLA COMO QUEREMOS:
raiz.geometry("650x500") # --> (X: 650 , Y: 350) --> (Ancho: 650 , Alto: 350)

# PONER COLOR DE FONDO:
raiz.config(bg= "#00FFFF")

#______________________________________________________________
# LLAMAMOS A FRAME DE LA LIBRERÍA TK
# Crear un Frame dentro de la ventana Raiz
myFrame = Frame(raiz)
# EMPAQUETAMOS EL FRAME CON LA RAÍZ:
# Ponemos la ubicanción del frame dentro del cuadro

myFrame.config(
    width= "500" , 
    height= "400",
    bg = "#4B0082",
    bd = 25, # bd = border
    relief= "ridge",
    cursor= "hand2"
)
raiz.config(cursor="hand2")


# Si usamos el place, no podemos usarlo junto con el pack()
# Si queremos usar el pack(), comentemos el place()
#myFrame.place(relx=0.5, rely=0.5, anchor="center")

# Por eso lo comentamos para que funcione el place()
myFrame.pack(expand=True, anchor="sw", fill = "both")
Button(myFrame, text="Saludo", bd= 15, relief="groove").pack(side="top", pady=10)
Button(raiz, text="Saludo2", border=15, relief="groove").pack(side="top", pady=10)


# PARA VER Y EJECUTAR LA VENTANA:
# SIEMPRE VA AL FINAL DE TODO:
raiz.mainloop()


""" 

1. Rojo: #FF0000

2. Verde: #00FF00

3. Azul: #0000FF

4. Amarillo: #FFFF00

5. Cian: #00FFFF

6. Magenta: #FF00FF

7. Naranja: #FFA500

8. Rosa: #FFC0CB

9. Violeta: #8A2BE2

10. Gris: #808080

11. Blanco: #FFFFFF

12. Negro: #000000

13. Marrón: #A52A2A

14. Beige: #F5F5DC

15. Oro: #FFD700

16. Plata: #C0C0C0

17. Oliva: #808000

18. Turquesa: #40E0D0

19. Perla: #F0F8FF

20. Lavanda: #E6E6FA

21. Púrpura: #800080

22. Indigo: #4B0082

23. Coral: #FF7F50

24. Tomate: #FF6347

25. Dorado: #FFD700

26. Menta: #98FB98

27. Salmon: #FA8072

28. Azul marino: #000080

29. Aqua: #00FFFF

30. Azul celeste: #87CEEB

31. Café: #6F4F37

32. Amarillo oscuro: #9B870C

33. Verde pasto: #7CFC00

34. Verde esmeralda: #50C878

35. Fucsia: #FF00FF

36. Lavanda claro: #E0BBE4

37. Cereza: #DE3163

38. Berenjena: #580F41

39. Rosa oscuro: #C71585

40.Blanco antiguo: #FAEBD7

Estos colores pueden ser utilizados en visualizaciones y gráficos en Python,
como en bibliotecas como matplotlib, seaborn, o en interfaces de usuario 
si estás trabajando con Tkinter u otras.

"""

""" 
TIPOS DE CURSORES:
    hand2: El cursor de una mano
    arrow: El cursor de flecha estándar.
    circle: Un cursor circular.
    clock: Un cursor de reloj.
    cross: Un cursor de cruz.
    dotbox: Un cursor de caja con puntos.
    exchange: Un cursor de intercambio.
    fleur: Un cursor de flor.
    heart: Un cursor de corazón.
    man: Un cursor de hombre.
    mouse: Un cursor de ratón.
    pirate: Un cursor de pirata.
    plus: Un cursor de más.
    shuttle: Un cursor de lanzadera.
    sizing: Un cursor de tamaño (cambio de tamaño).
    spider: Un cursor de araña.
    spraycan: Un cursor de lata de aerosol.
    star: Un cursor de estrella.
    target: Un cursor de objetivo.
    tcross: Un cursor de cruz en T.
    trek: Un cursor de emigrar.
    watch: Un cursor de reloj.

"""


""" 
Los parámetros más comunes de .pack():
1) side: especifica el lado del contenedor donde se ubique el widget.
    Lado Izquierdo
    myFrame.pack(side= left)

    Lado Derecho
    myFrame.pack(side= "right")


    "top": coloca el widget en la parte superior del contenedor.

    "bottom": coloca el widget en la parte inferior del contenedor.

    "left": coloca el widget en el lado izquierdo.

    "right": coloca el widget en el lado derecho.

2) anchor: Define cómo se alinea el contenido dentro del widget 
(si el widget es más grande que el contenido que contiene). 
Los valores posibles para anchor son:

    "n": Norte (arriba).

    "s": Sur (abajo).

    "e": Este (derecha).

    "w": Oeste (izquierda).

    "ne", "nw", "se", "sw": Noreste, Noroeste, Sureste, Suroeste.

    "center": Centro (por defecto).

    Ejemplo:

    myFrame.pack(side="left", anchor="n")

3) fill: especifica cómo se expande el widget dentro del contenedor.

    "x": Expande el widget solo en el eje horizontal (ancho).

    "y": Expande el widget solo en el eje vertical (alto).

    "both": Expande el widget tanto en el eje horizontal como en el vertical.

    None: No expande el widget (comportamiento predeterminado).

    Ejemplo:

    myFrame.pack(side="top", fill="x")

4) expand: especifica si el widget se expande dentro del contenedor.

    True: El widget se expandirá para ocupar el espacio disponible.

    False: El widget no se expandirá (comportamiento predeterminado).

    Ejemplo:

    myFrame.pack(side="top", expand=True)

5) padx y pady: Controlan el relleno (espacio vacío) a lo largo del 
eje horizontal (padx) y vertical (pady).

    padx agrega espacio a los lados izquierdo y derecho.

    pady agrega espacio a los lados superior e inferior.
    
    Ejemplo:
    myFrame.pack(side="top", padx=10, pady=10)



"""

""" 
VAMOS A VER LOS POSIBLES PARÁMETROS DEL config():

El método .config() en Tkinter se utiliza para cambiar 
las propiedades de un widget ya existente, y puedes usarlo 
para modificar su apariencia, comportamiento y otras configuraciones. 
El parámetro bg se refiere al color de fondo del widget.

Parámetros Comunes para .config()
Aquí hay algunos parámetros comunes que puedes usar con .config() 
para cambiar las propiedades de un Frame u otros widgets en Tkinter:

1. bg o background: Establece el color de fondo del widget.

- Ejemplo: myFrame.config(bg="#4B0082")

2 fg o foreground: Establece el color del texto (si el widget lo tiene).

- Ejemplo: myFrame.config(fg="white")

3. width: Establece el ancho del widget en píxeles.

- Ejemplo: myFrame.config(width=300)

4. height: Establece la altura del widget en píxeles.

- Ejemplo: myFrame.config(height=200)

5. font: Establece la fuente del texto (si aplica al widget).

- Ejemplo: myFrame.config(font=("Arial", 12))

6. borderwidth: Establece el grosor del borde del widget.

- Ejemplo: myFrame.config(borderwidth=2)

7. relief: Establece el estilo del borde del widget (combinado con borderwidth).

Ejemplos:

    - flat: sin borde.

    - raised: borde elevado.

    - sunken: borde hundido.

    - groove: borde en forma de surco.

    - ridge: borde con un borde doble.

- Ejemplo: myFrame.config(relief="sunken")

8. highlightbackground: Establece el color del borde cuando el widget no está enfocado.

- Ejemplo: myFrame.config(highlightbackground="gray")

9. highlightcolor: Establece el color del borde cuando el widget está enfocado.

- Ejemplo: myFrame.config(highlightcolor="blue")

10. padx y pady: Establecen el relleno interno del widget en las direcciones horizontal y vertical, respectivamente.

- Ejemplo: myFrame.config(padx=10, pady=10)

11. relief: Establece el estilo del borde del widget.

- Ejemplo: myFrame.config(relief="flat")

12. anchor: Establece la posición del contenido dentro del widget (se usa principalmente con texto).

    - Ejemplos: "n", "s", "e", "w", "ne", "sw", "center".

    - Ejemplo: myLabel.config(anchor="center")


EJEMPLO DE USO: 
myFrame = tk.Frame(root)

myFrame.config(
    bg="#4B0082",  # Color de fondo
    fg="white",    # Color del texto
    width=300,     # Ancho del widget
    height=200,    # Altura del widget
    relief="raised",  # Borde elevado
    padx=20,        # Relleno horizontal
    pady=20         # Relleno vertical
)
O TAMBIÉN: 
myFrame.config(bg="#4B0082", fg="white", width=300, height=200, relief="raised", padx=20, pady=20)

myFrame.pack()

"""