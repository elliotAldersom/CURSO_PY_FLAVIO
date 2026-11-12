# FORMA SIMPLE Y NO TAN ACERTADA:
from textblob import TextBlob
class Sentimiento:
    def __init__(self, nombre , color):
        self.nombre = nombre
        self.color = color
    
    def __str__(self):
        return "\x1b[1;{}m{}\x1b[0;37m".format(self.color , self.nombre)
    

class AnalizadorDeSentimientos:
    
    def __init__(self, rangos):
        self.rangos = rangos
    
    def analizar_sentimiento(self , texto):
        polaridad = TextBlob(texto)
        polaridad = polaridad.sentiment.polarity
        for rango, sentimiento in self.rangos:
            if rango[0] < polaridad <= rango[1]:
                return sentimiento
        return Sentimiento("Muy negativo" , "31")

rangos = [
    ((-0.6, -0.3) , Sentimiento("Negativo" , "31")),
    ((-0.3, -0.1) , Sentimiento("Algo Negativo" , "31")),
    ((-0.1, 0.1) , Sentimiento("Neutral" , "33")),
    ((0.1, 0.4) , Sentimiento("Algo Positivo" , "32")),
    ((0.5, 0.8) , Sentimiento("Positivo" , "32")),
    ((0.8, 1.0) , Sentimiento("Muy Positivo" , "32")),
]


analizador = AnalizadorDeSentimientos(rangos= rangos )

while True:
    user_pront = input("\x1b[1;33m" + "Ingrese un texto: " + "\x1b[0;37m")
    result = analizador.analizar_sentimiento(user_pront)
    print(result)