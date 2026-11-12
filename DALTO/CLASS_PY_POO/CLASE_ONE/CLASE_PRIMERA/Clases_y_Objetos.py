""" 
Imaginemos que queremos hacer celulares
Con la programación secuencial es así:
- Esto se hace muy tedioso de trabajar
- Por lo tanto trabajar con la forma secuncial 
para cosas así es muy tedioso, complicado.

En este ejemplo tenemos 3 marcas de celulares con 3 propiedades (características)
Y que pasa si tenemos 10 celulares, así sean con estas 3 proiedades?
Pues sería muy complicado de trabajar con la programación secuencial.
"""
celular1_marca = "samsung"
celular2_marca = "apple"
celular3_marca = "huawei"

celular1_modelo = "S23"
celular2_modelo = "iPhone 15 pro"
celular3_modelo = "P20 pro"

celular1_camaraT = "24MP"
celular2_camaraT = "24MP"
celular3_camaraT = "8MP"

celular1_camaraF = "48MP"
celular2_camaraF = "48MP"
celular3_camaraF = "12MP"


""" 
¿QUÉ ES UNA CLASE?
- Es como la receta que debemos de seguir para hacer un objeto.
- Nos permite definir cuales van a ser las características y cualidades
y todo lo que tendrá el objeto.
¿QUÉ ES UN OBJETO?
- Es el producto que tenemos después de hacer la receta.
Es una instancia de la clase.

"""

""" 
PARA CREAR UNA CLASE USAMOS LA PALABRA RESERVADA CLASS:
Podemos usar el snake case: 
EJM: 
todo_minuscula_separado_por_guiones_bajos
camel case: primeraSegundaTercera
pascal case: PrimeraSegundaTercera 
Y usamos Pascal Case para definir una clase. (buena práctica)

Dentro de las clases se definen los atributos y los métodos, las cuales
tendrán cada objeto (instancia) de la clase.

- Hay 2 tipos de atributos:
- Estáticos: ya que para todos los objetos serán iguales
se pueden modificar fuera de la clase:
celular1 = Celular()
celular1.camara = "50MP"
"""

class Celular():
    
    # Atributos Estáticos
    marca = "Samsung"
    modelo = "S23"
    camara = "48MP" 
    
# Crear objeto: 
# Estamos instanciando la clase para hacer una istancia de la clase el cual es el objeto
# Entonces al instancair una clase, estamos creando un objeto.
celular1 = Celular()
celular2 = Celular()
celular3 = Celular()
celular4 = Celular()
print(celular1)
print(celular2)
print(celular3)
print(celular4)

""" 
En el celular1:
Imprime: <__main__.Celular object at 0x000001A11FF07230>
Nos dice que es un objeto de la clase Celular y nos dice
el espacio de la memoria RAM en la cual se almacena.

"""

print(celular1.marca) # --> Acceder a la marca
print(celular1.modelo) # --> Acceder al modelo
print(celular1.camara) # --> Acceder a la camara


""" 
ATRIBUTOS: 
- Son variables que pertenecen a una clase
HAY 2 TIPOS DE ATRIBUTOS:
- Estáticos: ya que para todos los objetos serán iguales
Se pueden modificar fuera de la clase:
celular1 = Celular()
celular1.camara = "50MP"

- Atributos de instancia:
Se llaman así, porque nosotros las definimos cuando instanciamos una clase
(crear un objeto)
Y para esto usamos el constructor __init__()
el cual es un método especial, que se ejecuta cuando instanciamos una clase
de forma automática.

Primero hacemos
def __init__(self):
- self es una forma de hacerse referencia a si mismo (mismo objeto)

O sea si digo: self.marca es como decir: celular1.marca


Como segundo paso hacemos:
def __init__(self, marca, modelo, camara):
- Le pasamos los parámetros que queremos que tenga el objeto (separado por comas ( , ))
Ojo: Se lo pasamos como parámetros (luego son argumentos, cuando el usuario lo ingresa)

Después definimos los atributos del objeto: self.atributo = parámetro deseado
Nos va quedando así:
class CellPhone:
    def __init__(self, marca, modelo, camara):
        self.marca = marca   # --> El self.marca es la propiedad del objeto
        self.modelo = modelo # --> El self.modelo es la propiedad del objeto
        self.camara = camara # --> El self.camara es la propiedad del objeto
    
celular1 = Celular("Samsung", "S22", "20MP")
print(f"\n{celular1.marca}\n{celular1.modelo}\n{celular1.camara}")

O TAMBIÉN:
celular1 = CellPhone(marca="Xiaomi", modelo="XP30", camara="60MP")
print(f"\n{celular1.marca}\n{celular1.modelo}\n{celular1.camara}")
"""

class CellPhone:
    # Atributos de instancia:
    # Llamamos al constructor con función: def __init__() 
    # __init__() es un método especial
    def __init__(self, marca, modelo, camara = "80MP"):
        # self es una forma de hacerse referencia a si mismo (mismo objeto)
        
        # Agregando un print dentro del self
        print("\nVIRTUAL STORE VIP")
        
        # Definiendo los valores de cada atributo
        self.marca = marca + " Virtual Store"
        self.modelo = modelo
        self.camara = camara
celular1 = CellPhone(marca="Xiaomi", modelo="XP30", camara="60MP")
print(f"\n{celular1.marca}\n{celular1.modelo}\n{celular1.camara}")

celular2 = CellPhone(marca="Samsung", modelo="S25 ultra", camara="60MP")
print(f"\n{celular2.marca}\n{celular2.modelo}\n{celular2.camara}")


# LE DIMOS UN VALOR POR DEFAULT AL PARÁMETRO DE CAMARA = 80MP
# O sea si no le pasamos el parámetro de camara, por defecto es 80MP
celular3 = CellPhone(marca="Huawei", modelo="30Pro Max")
print(f"\n{celular3.marca}\n{celular3.modelo}\n{celular3.camara}")