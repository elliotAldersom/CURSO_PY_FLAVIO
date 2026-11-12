def Interfaz():
    while True:
        try:
                mensaje = input(''' 
✨ 🤖 BIENVENIDO A LA CALCULADRA 
🤖 ESTAS SON LAS OPERCIONES QUE PUEDES REALIZAR: 
- 1️⃣  Suma ➕ 
- 2️⃣  Resta ➖
- 3️⃣  Multiplicación ✖️
- 4️⃣  División ➗
- 5️⃣  Potenciación 📏📐
- 6️⃣  Radicación 📏📐
- 7️⃣  Factorial ❗
- 8️⃣  Salir  🚪🚶

🤖 Por favor ingrese alguna de las opcines (número o nombre): ''')
        except KeyboardInterrupt:
             print("\n🤖 🚫 Caracter no valido")
        else:
             return (mensaje.strip()).lower()
        
#print(Interfaz())
    
