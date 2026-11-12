""" 
MRO : Método de Resolución de Orden

¿Qué es MRO?
- El Método de Resolución de Orden (MRO) básicamente hace referencia a el orden en el
que Python busca los métodos y atributos de una clase cuando se hereda de múltiples 
clases. Esto es importante tenerlo en cuenta porque es un aspecto crucial de la herencia
ya que debemos de tener en cuenta que si una clase tiene muchos tipos de herencia o 
una cadena larga de herencia, tenemos que entender como funciona y que se va a ejecutar
primero y que se tiene prioridad y que no.
"""



class Persona: 
    def __init__(self, nombre, edad, nacionalidad):
        self. nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad
        
    def Hablar(self):
        return f"La persona {self.nombre} está hablando."


class Artista():
    def __init__(self, habilidad):
        self.habilidad = habilidad
    
    def Presentacion(self):
        return f"Mi habilidad es {self.habilidad}."


class Estudiante(Persona):
    def __init__(self, nombre, edad, nacionalidad, notas, universidad):
        super().__init__(nombre, edad, nacionalidad)
        self.notas = notas
        self.universidad = universidad
    
    def Speaking(self):
        return f"{super().Hablar()} y estudio en {self.universidad} con notas {self.notas}."
        #return super().Hablar()

class Empleado_Artista(Persona, Artista):
    def __init__(self, nombre, edad, nacionalidad, habilidad, salario, empresa):
        Artista.__init__(self, habilidad)
        Persona.__init__(self, nombre, edad, nacionalidad)
        self.sueldo = salario
        self.empresa = empresa
    
    def Presentarse(self):
        return f"{super().Presentacion()}"
    

# Crear Instancia de Persona:
person_one = Persona("Juan", 30, "Colombiano")
print(person_one.nombre)
print(person_one.edad)
print(person_one.nacionalidad)
print(person_one.Hablar())

# Crear Instancia de Artista:
person_two = Artista("Cantar")
print(person_two.habilidad)
print(person_two.Presentacion())

# Crear Instancia de Estudiante:
person_three = Estudiante("Pepe", 17, "peruano", 19, "SENATI")
print(person_three.nombre)
print(person_three.edad)
print(person_three.nacionalidad)
print(person_three.notas)
print(person_three.universidad)
print(person_three.Speaking())
print(person_three.Hablar())

# Crear Instancia de Empleado_Artista:
person_four = Empleado_Artista("Luis", 28, "peruano", "cantar",15000, "Sony Music")
print(person_four.nombre)
print(person_four.edad)
print(person_four.nacionalidad)
print(person_four.habilidad)
print(person_four.sueldo)
print(person_four.empresa)
print(person_four.Presentarse())
print(person_four.Hablar())
print(person_four.Presentacion())




""" 
MRO : Método de Resolución de Orden

¿Qué es MRO?
- El Método de Resolución de Orden (MRO) básicamente hace referencia a el orden en el
que Python busca los métodos y atributos de una clase cuando se hereda de múltiples 
clases. Esto es importante tenerlo en cuenta porque es un aspecto crucial de la herencia
ya que debemos de tener en cuenta que si una clase tiene muchos tipos de herencia o 
una cadena larga de herencia, tenemos que entender como funciona y que se va a ejecutar
primero y que se tiene prioridad y que no.

A partir de acá vamos a tratar com MRO.
"""

class A:
    def hablar(self):
        print("Hola desde A")
        
class B(A):
    # CASO 3
    #def hablar(self):
    #    print("Hola desde B")
    
    pass
        
class C(A):
    # CASO 4
    #def hablar(self):
    #    print("Hola desde C")
    
    pass

class D(B, C):
    # CASO 1
    #def hablar(self):
    #    print("Hola desde D")
    
    
    # CASO 2
    pass
        
d = D()
# CASO 1
d.hablar()  # Esto llamará al método hablar de la clase D

# CASO 2
d.hablar() # Pone el hablar de B porque está primero en el orden:  class D(B, C)
# Si fuera class D(C, B) llamaría al de C

# CASO 3
d.hablar() # Pone el hablar de C porque B no tiene el método hablar definido.

# CASO 4
d.hablar() # Pone el hablar de A porque solo A tiene el método definido

""" 
A ver primero llama al método reescrito en la clase D
Luego llama al de B porque está primero en el orden de herencia (B, C)
Luego llama al de C porque B no tiene el método definido
Luego llama al de A porque solo A tiene el método definido y tanto B y C heredan de A

Ahora si B y C heredan de otra clase, digamos que B hereda de A y C de F
Primero busca en D 
Luego en B
Luego en A 
Luego en C
Luego en F

O sea se busca todo como si fuera una rama o árbol de herencia,
Bucamos primero en toda la rama de la primera clase herdada y luego de la segunda,
y así sucesivamente hasta que encuentre el método o atributo que buscamos.
"""
class I:
    # CASO 3
    def hablar(self):
        print("Hola desde I")   


class F:
    # CASO 3
    #def hablar(self):
    #   print("Hola desde F")
    pass


class G:
    # CASO 3
    #def hablar(self):
    #    print("Hola desde G")
    pass


class E(G):
    # CASO 3
    #def hablar(self):
    #    print("Hola desde E")   
    pass


class A(F):
    #def hablar(self):
    #    print("Hola desde A")
    pass

      
class B(A,I):
    # CASO 3
    def hablar(self):
        print("Hola desde B")
    #pass
    
       
class C(A,I):
    # CASO 4
    #def hablar(self):
    #    print("Hola desde C")
    pass
    
    
class D(B, C):
    # CASO 1
    #def hablar(self):
    #    print("Hola desde D")
    pass

        
d = D()
d.hablar()

# LLAMAR AL MÉTODO ESPECÍFICO DE LA CLASE PADRE QUE DEESEAMOS
# EN CASO QUE LA CLASE QUE PONEMOS, NO ESTE EN EL ORDEN DE HERENCIA
# SE MOSTRARÁ UN ERROR, PUES NO ESTÁ SIENDO HEREDADO.
B.hablar(d)
# FORMA DE SABER EL ORDEN DE BUSQUEDA DE MRO
print(D.mro())
""" 
ESTE ES OTRO EJEMPLO DE MRO, EN EST CASO, MUESTRA EL SALUDO DESDE I, YA QUE B HERDA 
DE A Y DE I.
"""