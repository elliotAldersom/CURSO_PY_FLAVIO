import qrcode
dato = "https://www.facebook.com/share/19KGGGgY6k/"
qr = qrcode.make(dato)
qr.save("Iglesia.png")

