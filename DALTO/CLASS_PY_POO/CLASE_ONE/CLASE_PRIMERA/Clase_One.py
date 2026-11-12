# POO : Porgramación Orientada a Objetos
"""
- Modula el código, haciendola más entendible y reutilizable.
- Se basa en crear nuevos tipos de datos llamados "objetos".
- Trataremos a nuestro código como unmódulo de dos partes
- Cada objeto tiene propiedades (variables / atributos) y funciones (métodos).

# Propiedades (atributos):
- Propiedades que definen al objeto.

# Funciones (métodos):
- Las acciones que pueden realizar.

# Para especificar que queremos crear un tipo de dato nuevo se usa la "clase"
# Clase:
- Plantilla donde definiremos los atributos y métodos,
con esta plantilla se pueden crear objetos de ese tipo, dándole valores a sus atributos,
esto es conocido como "instanciar"

- Para instanciar, se hace uso del método --> constructor()
- Este método sirve para crear el objeto y darles los colores necesarios para inicializarlo
- El nombre del método constructor() depende del lenguajne que usamos, en python es: 
__init__()   

- Algo importante de saber, es que una vez creado el objeto, podemos accderer con punto (.)
a sus atributos y métodos.
EJM:  miTaza2.cantidad  --> (200)  ---> Para consultar algo
      miTaza2.liquido   --> (café) ---> Para modificar algo
      miTaza2.beber()   --> Utilizar sus métodos.
___________________________________________________________________________________________________________


LOS CUATRO PILARES DE LA POO:
1) Abstracción:
- Al hacer una ckase, debemos de definir los atributis y los métodos que debe de tener
si definimos que es una canción (en clase), no es necesario incluir todas las características,
tenemos que abstraernos y solo incluir las necesarias para el objetivo que tenemos planeado.
EJM: SI HACEMOS UNA BIBLIOTECA DE MÚSICA
 # Los atributos podrían ser: Nombre; Artista; Duración; Género
 # Los métodos podrían ser: escuchar(); constructor()

SI DESEAMOS USARLO COMO BASE DE DATOS PARA UNA PÁGINA DE VENTAS
# Los atributos podrían ser: Nombre; Precio; Cantidad; Género; Artista
# Los métodos podrían ser: comprar(); constructor()

--> Con la abstracción elegimos cuales serán los atributos y los métodos que definirán
que es una cacnión para nosotros.

- EN CONCLUSIÓN LA ABTRACCIÓN SE BASA EN AGREGAR LOS ATRIBUTOS Y MÉTODOS
REQUERIDOS, SEGÚN LO QUE VAMOS A REALIZAR CON ESA CLASE.

EJM: OTRO EJEMPLO ES UN PERSONAJE DE UN JUEGO
# Los atributos pueden ser: Nombre; Fuerza; Inteligencia; Defensa; Vida; Posición; Contador de acciones que puede realizar
# Los métodos pueden ser: moverse(); atacar(); defenderse(); turno(); constructor()
______________________________________________________________________________________________________________________________________

2) Encapsulación:
- Nosotros podemos hacer un programa por medio de varias clases que se comuniquen entre sí,
a esto se le llama "modularidad", es muy útil, ya que si falla algo en nuestro programa,
es más fácil detectar donde y qué debemos de arreglar. Cada clase debe de tener control propio
de lo que sucede dentro de ella y tener loS métodos adecuados para poder ser reutilizada desde fuera.

Tenemos varias clases y una de ellas se llama personaje y si hacemos un punto en ese clase
personaje. ---> Podremos tener acceso a todos los atributos y métodos que contiene,
lo cual puede ser peligroso, porque podríamos alterar su comportamiento interno; para
solucionarlo podemos declarar cuales de nuestros atributos y métodos van a ser privados
y esto es lo que se conoce como "encapsulación"

EJM: TENEMOS LA CLASE PERSONAJE
# Los atributos pueden ser: Nombre; Fuerza; Inteligencia; Defensa; Vida; Posición; Contador de acciones que puede realizar
# Sus métodos son: constructor(); turno(); atacar(); moverse(); 
y queremos que de todos estos 4 métodos solo sea accsesible el "constructor"
para crear el objeto y "turno" que gestiona la funcionalidad de la clase
# turno, dependiendo del atributo contador y de los deseos de usuarios, controla 
las acciones de atacar y moverse, gastando contadores cada ves que se usen, una vez
no vean contadores, el método termina. Ahora como turno es quien controla os métodos "atacar"
y "moverese", entonces estos deben de ser privados.

Al igual que con los métodos, se puede hacer o mismo con los atributos, podemos
crear métodos de acceso y de modificación de los atributos, dentro de estos métodos
podemos tener control sobre ellos.
# Estos métodos se suelen nombrar con el prefijo "get" para acceder y "set" para modificar
# EJM: getNombre(); setNombre()
# EJM: getFuerza(); setFuerza()

En resumen, si no declaramos los atributos como privados, podemos usarlos desde fuera sin
ningún tipo de control, pero al declararse como privado, estos no podrá consultarse ni
modificarse a no ser que usemos los métodos "get" O "set", definir atributos y métodos como 
públicos y privados es depende el lenguaje.

______________________________________________________________________________________________________________________________________


3) Herencia:
- Ahora creamos la calse guerreo y mago, los cuales tienen todos los atributos
de la clase personaje con  algunos métodos nuevos.

EJM: OTRO EJEMPLO ES UN PERSONAJE DE UN JUEGO
# Los atributos pueden ser: Nombre; Fuerza; Inteligencia; Defensa; Vida; Posición; Contador de acciones que puede realizar
# Los métodos pueden ser: moverse(); atacar(); defenderse(); turno(); constructor(); getNombre(); setNombre()

- En ves de crear todo de nuevo, podemos reutilizar la clase personaje con la herencia
- Entonces a las nuevas clases (guerreo y mago) tendrán todos los atributos y métodos
de la clase personaje, pero también podrán tener sus propios atributos y métodos (las cuales agregamos)
- Esto es lo que se conoce como "herencia"; ya que las nuevas clases heredan de otra clase,
aunque también pueden tener nuevos atributos y métodos.

# A la clase que hereda se le conoce como clase padre o superclase.
# A la clase que hereda se le conoce como clase hijo (a) o subclase.

________________________________________________________________________________________________________________________________________________

4) Polimorfismo:
- Esto permiete a un método ser diferente según que clase lo esté usando, es decir
puede tener muchas formas de usarse.

Volviendo al ejemplo del guerrero, mago y personaje, todos tienen el método atacar
que realiza la misma acción, tienen el mismo código,
pero después de la herencia podemos volver a definir los métodos heredados.

EJM: En guerrero, podemos modifcar el método atacar, el personaje úsaba 
la estadistica fuerza para atacar con las manos
pero queremos que el método acatar de la clase guerrero incremente 
el daño dependiendo de la arma que use, o el mago al usar libros pueda atacar 
medio de la estadítica inteligencia.

_________________________________________________________________________________________________________________________________________________________
"""

# DECLARAR CLASE EN PYTHON:

# ABSTRACCIÓN

class personaje:
   
 # Self es un aregumento, que hace referencia a si mismo, al objeto
 # y permite por medio del punto (.) acceder a los atributos y métodos de la clase
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida): 
        self.nombre = nombre ;               # -----
        self.fuerza = fuerza ;               #      -
        self.inteligencia = inteligencia ;   #      ----> ATRIBUTOS
        self.defensa = defensa ;             #      -
        self.vida = vida ;                   #------

    def atributos(self):
        print(self.nombre + ":" , sep="" );
        print("Fuerza", self.fuerza);
        print("Inteligencia", self.inteligencia);
        print("Defensa", self.defensa);
        print("Vida", self.vida);

    def subir_nivel(self, fuerza, inteligencia, defensa):
        self.fuerza = self.fuerza + fuerza ;
        self.inteligencia = self.inteligencia + inteligencia ;
        self.defensa = self.defensa + defensa ;

    def esta_vivo(self):
        return self.vida > 0
    
    def morir(self):
        self.vida = 0 ;
        print(self.nombre + " ha muerto");

    def daño(self, enemigo):
        return self.fuerza - enemigo.defensa
    
    def atacar(self, enemigo):
        daño = self.daño(enemigo) ;
        enemigo.vida = enemigo.vida - daño ;
        print(self.nombre + "Ha realizado" , daño , " puntos de daño a" , enemigo.nombre);
        print("La vida de" , enemigo.nombre , " es" , enemigo.vida);
 
mi_personaje = personaje("BitBoss", 10, 1, 10, 100);
mi_enemigo = personaje("Enemy Stando", 8, 5, 3, 100);

# mi_personaje.nombre = "BitBoss"; ----> Podemos modificar algunos atributos
# mi_personaje.fuerza =  10 ;   ---> Podemos modificar algunos atributos
#print("El nombre del jugador es: "+ str (mi_personaje.nombre));  --> FORMA DE HACER
#print("El nombre del jugador es: ", mi_personaje.nombre);  ---> FORMA DE HACER


mi_personaje.atributos()
mi_enemigo.atributos()

print("NWE DATA:\n_______________________________________________");

mi_personaje.subir_nivel(10, 11, 20)
mi_personaje.atributos()

print("__________________________________________________________");

print(mi_personaje.esta_vivo())
mi_personaje.morir()
mi_personaje.atributos()

print("___________________________________________________________");

print(mi_personaje.daño(mi_enemigo))

print("___________________________________________________________");

mi_personaje.atacar(mi_enemigo)


mi_enemigo.atributos()
