""" 
OCP : Open/Closed Principle (Principio de Abierto y Cerrado)
- Este principio nos dice que las entidades de Software, en este caso
"las clases, los módulos, las funciones, etc, tienen que estar abierta
para la extensión, pero cerradas para modificción (open for extension / closed for modifications)"

- En definitiva significa que deberíamos poder agregarle nuevas funcionalidades, 
sin tener que cambiar el código fuente de la case o entidades como tal.

EJM:
- En este ejemplo, ponemos el método de  Noificar, el cual puede ser de varias formas 
como Email, sms, etc.. 
Para ello hacemos una especie de clase abstracta, con el método de Notificar, 
y hacemos clases hijas con la implementación del método Notifcar, cada quien debe de 
tener su forma de hacer llegar el mensaje al usuario, por eso hcemos de cuenta que ponemos 
el atributo según corresponda como email / sms o si es whatsapp.

- Esto es con el fin de que si deseamos agregar más funciones de forma de mandar
una notificación, no modificamos la clase principal (Notificador) , sino
hacemos clases hijas, que se encarguen de hacerlo, buscamos dividir todo, para no
modificar la misma clase siempre, además podemos hacer la clase de Usuario y tener el objeto 
de Usuario y pasarlo para Email o Sms.

- Si sabemos que en un futuro vamos a agregarle más funcionalidades a algo, tenemos que dejar
un sistema que esté abierto para agregar más funciones pero no para modificarlo, por decir
Notificador() -> tiene todo lo importante para mandar mensajes (Usuario y mensaje), solo falta
agregaar las funiones para diversas formas de mandar el mensaje, sin modificar la clase principal.
"""
# Creando la clase Padre
# Sería bueno, hacer clase usuario para tener el nombre del usuario con su email, etc...
class Notificador:
    def __init__(self, usuario, mensaje):
        self.usuario = usuario
        self.mensaje = mensaje
    
    def Notificar(self):
        # Hacemos esto para hacer un método abstracto (Forma sencilla)
        # Con esto hacemos que cualquier clase hija que herede de acá debe implementar este método
        # Además se llamara al raise NotImplementedError si se trata de instanciar de esta clase Padre
        raise NotImplementedError

# Creando las clases hijas, con la implementación del método
class NotificarEmail(Notificador):
    def Notificar(self):
        # Ponemos el email, ya que debemos hacer la forma de mandar el email
        print(f"Enviando mensaje por Email a {self.usuario.email}")

class NotificarSMS(Notificador):
    def Notificar(self):
        # Ponemos el sms, ya que debemos hacer la forma de mandar el sms
        print(f"Enviando mensaje por SMS a {self.usuario.sms}")
        
class NotificarWhatsApp(Notificador):
    def Notificar(self):
        # Ponemos el whatsapp, ya que debemos hacer la forma de mandar el whatsapp
        print(f"Enviaando mensaje de WhatsApp a {self.usuario.whatsapp}")

class NotificarMessenger(Notificador):
    def Notificar(self):
        # Ponemos el messenger, ya que debemos hacer la forma de mandar el messenger
        print(f"Enviaando mensaje de Messenger a {self.usuario.messenger}")

one = NotificarEmail("flavioestrada1412@gmail.com", "hola")
