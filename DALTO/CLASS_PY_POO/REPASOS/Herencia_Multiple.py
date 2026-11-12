class Persona:
    def __init__(self, nombre, edad, nacionalidad):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad
    
    def saludar(self):
        return f"{self.nombre} está saludando..."

    def despedirse(self):
        return f"{self.nombre} se está yendo.."



class Estudiante(Persona):
    def __init__(self, nombre, edad, nacionalidad, centro_estudios, carrera, notas):
        super().__init__(nombre, edad, nacionalidad)
        self.centro_estudios = centro_estudios
        self.carrera = carrera
        self.notas = notas
    
    def saludar(self):
        return f"El estudiante {self.nombre}, es estudiante de {self.centro_estudios} y cursa la carrera de {self.carrera}..."
    
    def despedirse(self):
        return f"{self.nombre} se está yendo a su casa después de estudiar en {self.centro_estudios}..."



class Empleado_Estudiante(Estudiante):
    def __init__(self, nombre, edad, nacionalidad, centro_estudios, carrera, notas, trabajo, hora_trabajo, salario):
        super().__init__(nombre, edad, nacionalidad, centro_estudios, carrera, notas)
        self.trabajo = trabajo
        self.hora_trabajo = hora_trabajo
        self.salario = salario
    
    def Presentarse(self):
        return f"{self.nombre} trabaja en {self.trabajo}"
    
    
    # Si quiero saludar de una clase específica hago esto:
    def saludar(self):
        return Persona.saludar(self)

    def despedirse(self):
        return Estudiante.despedirse(self)



class Artista:
    def __init__(self, habilidad):
        self.habilidad = habilidad
    
    def mostrarHabilidad(self):
        return f"La habilidad del artista es {self.habilidad}"



class Artista_Alumno( Artista, Estudiante):
    def __init__(self, nombre, edad, nacionalidad, centro_estudios, carrera, notas, habilidad, trabajo, horas_trabajo, salario):
        Estudiante.__init__(self,nombre, edad, nacionalidad, centro_estudios, carrera, notas) 
        Artista.__init__(self,habilidad)  
        self.trabajo = trabajo
        self.horas_trabajo = horas_trabajo
        self.salario = salario



print(Artista_Alumno.mro())
   
        

Marcos = Artista_Alumno("Marcos", 25, "Peruano", "Senati", "Ingenieria en Sistemas", 19, "Cantar" , "Desarrollador", "8 h/d" , "2000$")
print(Marcos.saludar())
print(Marcos.mostrarHabilidad())
print(Marcos.saludar())

print("\n")
Juan = Empleado_Estudiante("Juan", 25, "Peruano", "Senati", "Diseño Grafico", 19, "Diseñador", "8 h/d", "2000$")

valores_dict = (Juan.__dict__).items()

valor_ordenado = "\n".join(f"{key}: {values}" for key, values in valores_dict)
print(valor_ordenado)

print(Juan.saludar())
print(Juan.despedirse())

