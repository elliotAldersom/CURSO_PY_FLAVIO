""" 
¿QUÉ ES LA HERENCIA?
- Unos de los pílares fundamentales de la POO, los que nos permite básicamente es: 
Permitir a la clase hija (subclase) acceder a todos los atributos y métodos 
de la clase padre (superclase).
(NOS PERMITE REUTILIZAR CÓDIGO)

EJM:
- Tenemos a la clase persona (Padre) y a la clase estudiante (Hija), un estudiante
es una persona entonces que herede todo lo que tiene y puede hacer una persona pero
agregando cosas nuevas que solo un estudiante puede hacer.
"""
# CREANDO LA CLASE PADRE
class Persona:
    def __init__(self, nombre, edad, nacionalida ):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalida
        
    def saludar(self):
        print(f"Hola, soy {self.nombre}")

# CREANDO LA CLASE HIJA
class Empleado(Persona):
    # VAMOS A PONER PASS
    #pass 
    """ 
    - Pass es cuando queremos crear algo
    pero no queremos definir que va a hacer
    """
    # AHORA AGREGAREMOS NUEVOS ATRIBUTOS:
    def __init__(self,nombre, edad, nacionalidad, trabajo, salario, horas_trabajo):
        super().__init__(nombre, edad, nacionalidad) # --> ACÁ DENTRO LE DECIMOS QUE QUEREMOS HEREDAR
        self.trabajo = trabajo
        self.salario = salario
        self.horas_trabajo = horas_trabajo
    
    # SOBRESCRIBIENDO UN MÉTODO   
    def saludar(self):
        print("HOLASSSSS BRO...")
        
class Estudiante(Persona):
    # VAMOS A PONER PASS
    #pass 
    """ 
    - Pass es cuando queremos crear algo
    pero no queremos definir que va a hacer
    """
    # AHORA AGREGAREMOS NUEVOS ATRIBUTOS:
    def __init__(self,nombre, edad, nacionalidad, centro_estudio, carrera, ciclo, notas):
        super().__init__(nombre, edad, nacionalidad) # --> ACÁ DENTRO LE DECIMOS QUE QUEREMOS HEREDAR
        self.centro_estudios = centro_estudio
        self.carrera = carrera
        self.calificacion = notas
        self.ciclo = ciclo
        
    # SOBRESCRIBIENDO UN MÉTODO   
    def saludar(self):
        print("HOLASSSSS BRO...\nI'm student")
                
       
# CREANDO UNA INSTANCIA DE LA CLASE PADRE: 
PersonOne = Persona("Roberto", 23, "peruano")
print(PersonOne.nombre)
PersonOne.saludar()

# CREANDO UNA INSTANCIA DE LA CLASE HIJA
PersonOne = Empleado("Roberto", 23, "peruano","programador",15000, 8)
print(PersonOne.nombre)
PersonOne.saludar()
print(f"Soy {PersonOne.trabajo}, mi sueldo mensual es de ${PersonOne.salario} y trabajo unas {PersonOne.horas_trabajo} horas diarias.")

PersonOne = Estudiante("Flavio", 18, "peruano", "SENATI","Ingeniería de Software con IA",2,18)
PersonOne.saludar()
print(f"Soy {PersonOne.nombre}, tengo {PersonOne.edad}, de nacionalidad {PersonOne.nacionalidad},estoy en el {PersonOne.ciclo} ciclo de la carrera de {PersonOne.carrera} en {PersonOne.centro_estudios} y mi promedio de notas es de {PersonOne.calificacion}.")


""" 
ESTO QUE VEMOS ES UNA HERECIA JERARQUICA, PUES VARIAS SUBCLASES DEPENDEN DE 
UNA SUPERCLASE
"""


# SOLUIONAR ESTE PROBLEMA

class Estudiante_Trabajador (Estudiante, Empleado):
    def __init__(self, nombre, edad, nacionalidad,trabajo, salario, horas_trabajo, centro_estudio, carrera, ciclo, notas, fuerza):
        Estudiante.__init__(self,nombre, edad, nacionalidad, centro_estudio, carrera, ciclo, notas)
        Empleado.__init__(self,nombre, edad, nacionalidad, trabajo, salario, horas_trabajo)
        self.fuerza = fuerza
        

estudent = Estudiante_Trabajador("Pepe", 18, "Peruano", "Vendedor de pan", "25 soles", "2 h/d", "SENATI", "Mecatrónica", "2do", 18.9, 100)
"""print(\
    estudent.nombre,
    estudent.edad,
    estudent.nacionalidad,
    estudent.trabajo,
    estudent.salario,
    estudent.horas_trabajo,
    estudent.centro_estudios,
    estudent.carrera,
    estudent.ciclo,
    estudent.calificacion,
)"""
