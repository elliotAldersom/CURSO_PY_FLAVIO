""" 
ChatBot de Analizador de Sentimientos

- En este proyecto, podrías desarrollar un ChatBot en Python, 
que nos pida que le digamos algo y tome eso que le decimos, analice
el sentimiento y nos responda cual es el sentimiento.

- Este proyecto te daría la oportuidad de trabajar con varios aspectos:
POO, módulos, API, análisis de datos, etc...
"""

# FORMA SIMPLE Y NO TAN ACERTADA:
from textblob import TextBlob

class AnalizadorDeSentimientos:
     def Analizar_sentimiento(self, texto):
         analisis = TextBlob(texto)
         if analisis.sentiment.polarity > 0:
             return "positivo"
         elif analisis.sentiment.polarity == 0:
             return "neutral"
         else:
             return "negativo"

# analizador = AnalizadorDeSentimientos()
# text = "This is funny, but is not my intersting"
# result = analizador.Analizar_sentimiento(text)
# print(result)


# USANDO API DE CHAT GPT (OPEN AI):
import openai

openai.api_key = "tu apiKey de openAI"


system_rol = ''' Hace de cuenta que sos un analizador de sentimientos.
                Yo te paso sentimientos y vos analizas el sentimiento de los mensajes y me das una respuesta
                con al menos 1 carater y máximo 4 caracteres, SOLO RESPUESTAS NUMÉRICAS, donde -1 es negatividad
                máxima, 0 es neutral y 1 es positividad máxima. (Podes responder solo con ints o floats)'''
                
mensajes = [{"role": "ystemn" , "content" : system_rol }]

class AnalizadorDeSentimientos:
    def analizar_sentimiento(self, polaridad):
        if polaridad > -0.8 and polaridad <= -0.3:
            return "\x1b[1;31m" + "Negativo" + "\x1b[0;37m"
        elif polaridad > -0.3 and polaridad < -0.1:
            return "\x1b[1;31m" + "Algo Negativo" + "\x1b[0;37m"
        elif polaridad >= -0.1 and polaridad <= 0.1:
            return "\x1b[1;33m" + "Neutral" + "\x1b[0;37m"
        elif polaridad >= 0.1 and polaridad <= 0.4:
            return "\x1b[1;32m" + "Algo Positivo" + "\x1b[0;3m"
        elif polaridad >= 0.4 and polaridad <= 0.9:
            return "\x1b[1;32m" + "Positivo" + "\x1b[0;37m"
        elif polaridad > 0.9:
            return "\x1b[1;32m" + "Muy Positivo" + "\x1b[0;37m"
        else:
            return "\x1b[1;31m" + "Muy Negativo" + "\x1b[0;37m"


analizador = AnalizadorDeSentimientos()

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
    


