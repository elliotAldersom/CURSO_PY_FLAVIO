# USANDO API DE CHAT GPT (OPEN AI):
import openai

openai.api_key = "tu apiKey acá"


system_rol = ''' Hace de cuenta que sos un analizador de sentimientos.
                Yo te paso sentimientos y vos analizas el sentimiento de los mensajes y me das una respuesta
                con al menos 1 carater y máximo 4 caracteres, SOLO RESPUESTAS NUMÉRICAS, donde -1 es negatividad
                máxima, 0 es neutral y 1 es positividad máxima. (Podes responder solo con ints o floats)'''
                
mensajes = [{"role": "ystemn" , "content" : system_rol }]


class Sentimiento:
    def __init__(self, nombre , color):
        self.nombre = nombre
        self.color = color
    
    def __str__(self):
        return "\x1b[1;{}m{}\x1b[0;37m".format(self.color , self.nombre)
        

class AnalizadorDeSentimientos:
    
    def __init__(self, rangos):
        self.rangos = rangos
    
    def analizar_sentimiento(self, polaridad):
        for rango, sentimiento in self.rangos:
            if rango[0] < polaridad <= rango[1]:
                return sentimiento
        return Sentimiento("Muy negativo" , "31")


rangos = [
    ((-0.8, -0.3) , Sentimiento("Negativo" , "31")),
    ((-0.3, -0.1) , Sentimiento("Algo Negativo" , "31")),
    ((-0.1, 0.1) , Sentimiento("Neutral" , "33")),
    ((0.1, 0.4) , Sentimiento("Algo Positivo" , "32")),
    ((0.5, 0.9) , Sentimiento("Positivo" , "32")),
    ((0.9, 1.0) , Sentimiento("Muy Positivo" , "32")),
]

analizador = AnalizadorDeSentimientos(rangos= rangos )

while True:
    user_pront = input("\x1b[1;33m" + "\nIngrese un texto: " + "\x1b[0;37m")
    mensajes.append({"role": "user" , "content" : user_pront})
    
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = mensajes ,
        max_tokens = 8
    )
    
    respuesta = completion.choices[0].message["content"]
    mensajes.append({"role" : "assistant" , "content" : respuesta})
    
    sentimiento =  analizador.analizar_sentimiento(float(respuesta))
    print(sentimiento)
    
