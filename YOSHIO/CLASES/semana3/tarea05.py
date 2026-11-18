dict_notas = {
    "Elliot" : 18, 
    "Snowden": 12, 
    "Darlene": 9, 
    "Angel": 14, 
    "Tyrell":  11, 
    "Mr. Robot": 20, 
    "WhitRose": 8
}
nota_mayor = {"alumno": "" , "nota": 0}
nota_acumulada = 0
nota_menor = {"alumno": "", "nota": 20}  # 20 es la máxima nota por eso

for nota in dict_notas.items(): 
    nota_acumulada += nota[1]
    print(f"{nota[0]}: {nota[1]} ({'Aprobado' if nota[1] >= 11 else 'Desaprobado'})\n")

    if(nota[1] > nota_mayor["nota"]): 
        nota_mayor["alumno"] = nota[0]
        nota_mayor["nota"] = nota[1]
    
    if(nota[1] < nota_menor["nota"]): 
        nota_menor["alumno"] = nota[0]
        nota_menor["nota"] = nota[1]

nota_promedio = nota_acumulada / len(dict_notas)
rango = nota_mayor["nota"] - nota_menor["nota"]

sumatoria_diferencia = 0
for nota in dict_notas.values():
    sumatoria_diferencia += (nota - nota_promedio)**2

varianza = sumatoria_diferencia / (len(dict_notas) - 1)
std = varianza ** (1/2)
print(
f""" 
======== ANÁLISIS DE LAS NOTAS ========= 
Nota Mayor : {nota_mayor['nota']} => {nota_mayor['alumno']}
Nota Menor: {nota_menor["nota"]}  => {nota_menor['alumno']}
Rango: {rango}
Promedio: {round(nota_promedio,2)}
Varianza: {round(varianza,2)}
Desv. estandar {round(std,2)}
""")