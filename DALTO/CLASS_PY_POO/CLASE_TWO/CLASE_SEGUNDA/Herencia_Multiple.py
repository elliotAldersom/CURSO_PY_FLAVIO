class Persona:
    def __init__(self, nombre, edad, nacionalidad):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad

    def Hablar(self):
        print(f"{self.nombre} está hablando en este momento.")


class Artista:
    def __init__(self,habilidad):
        self.habilidad = habilidad

    def Mostrar_Habilidad(self):
        return(f"Mi habilidad es {self.habilidad}.")

# Este es ejemplo de herencia no multiple, sino simple (una clase hija de una clase padre)     
class Estudiante(Persona):
    def __init__(self, nombre, edad, nacionalidad, notas, universidad):
       super().__init__(nombre, edad, nacionalidad)
       self.notas = notas
       self.universidad = universidad


# Este es un ejemplo de herencia multiple, donde una clase hija hereda de dos o más clases padre      
class Empleado_Artista(Persona, Artista):
    # Vamos a tener todos los atributos de las dos clases pero agregamos dos atributos más
    # los cuales son salario y empresa
    def __init__(self, nombre, edad, nacionalidad, habilidad, salario, empresa): 
        # Ahora como son más de una clase padre, debemos de hacer referencia a cada uno
        # para llamarlos, en ves del super() el cual es cuando se hereda de una sola clase Padre o es cooperativo
        # Vamos a usar el nombre de la clse Padre específica para heredar sus atributos
        Persona.__init__(self,nombre,edad,nacionalidad)
        Artista.__init__(self,habilidad)
        self.salario = salario
        self.empresa = empresa
    
    def Presentarse(self):
        # Podríamos usar el self.Mostrar_Habilidad()
        # Pero uso el super() porque es una buena práctica
        # Además, así le digo al programa que Mostrar_Habilidad
        # es un método que estamos trayeno desde arriba, es un método heredado, 
        # es decir, no es um método que llamamos desde self a nosotros mismos
        # sino es un método heredado de la clase Artista
        # Esto es bueno, porque si tenemos un método con el mismo nombre, 
        # con super nos aegurao que usar el método de la clase padre y no de la clase actura.
        return f"{super().Mostrar_Habilidad()}"



person = Empleado_Artista("Pepe", 25, "Mexicano" ,  "Cantar", 5000, "Sony Music")
print(f"Nombre: {person.nombre}\nEdad: {person.edad}\nNacionalidad: {person.nacionalidad}\nHabilidad: {person.habilidad}\nSalario: {person.salario}\nEmpresa: {person.empresa}\nPresentación: {person.Presentarse()}")

# Para saber de que clase hereda:
herencia = issubclass(Empleado_Artista, Artista)
print(herencia) # True 
herencia = issubclass(Empleado_Artista, Persona)
print(herencia) # True

herencia = issubclass(Empleado_Artista, Estudiante)
print(herencia) # False 

# Para saber si un objeto es instancia de un clase (str, int, clase_de_obejtos):
instancia = isinstance(person, Empleado_Artista)
print(instancia) # True
instancia = isinstance(person, Artista)
print(instancia) # True 
# Es True ya que Empleado_Artista hereda de Artista
instancia = isinstance(person, Persona)
print(instancia) # True 
# Es True ya que Empleado_Artista hereda de Persona