import os

def Seleccionar_csv_en_pc():
    """
    Busca archivos .csv en las carpetas desde el directorio actual.
    Permite al usuario escribir parte del nombre, muestra coincidencias ignorando mayúsculas,
    permite elegir uno y confirmar antes de abrir. 
    Maneja interrupciones del usuario sin detener el programa.
    """
    while True:
        try:
            palabra_clave = input("\n🔍 Ingrese parte del nombre del archivo .csv que desea buscar: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ Entrada inválida. Por favor, intente nuevamente...")
            continue

        coincidencias = []
        for carpeta, _, archivos in os.walk(os.getcwd()):
            for archivo in archivos:
                if archivo.endswith(".csv") and palabra_clave in archivo.lower():
                    coincidencias.append(os.path.join(carpeta, archivo))

        if not coincidencias:
            print("❌ No se encontraron archivos .csv que coincidan. Intente de nuevo...")
            continue

        print("\n📂 Archivos .csv encontrados:")
        for idx, archivo in enumerate(coincidencias, 1):
            print(f"[{idx}] {archivo}")

        while True:
            try:
                eleccion = input("\n✅ Ingrese el número del archivo que desea abrir: ").strip()
                if not eleccion.isdigit():
                    print("⚠️ Ingrese un número válido...")
                    continue
                eleccion = int(eleccion)
                if 1 <= eleccion <= len(coincidencias):
                    ruta_archivo = coincidencias[eleccion - 1]
                    print(f"\n📄 Archivo seleccionado: {ruta_archivo}")
                else:
                    print("⚠️ Número fuera de rango.")
                    continue
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Entrada inválida. Intente de nuevo...")
                continue

            # Confirmación para abrir archivo
            while True:
                try:
                    confirm = input("¿Desea abrir este archivo? (SI/NO): ").strip().upper()
                    if confirm in ("SI", "SÍ", "S"):
                        print(f"✅ Archivo '{ruta_archivo}' abierto correctamente. Ya puedes usar los métodos de la clase.")
                        return ruta_archivo
                    elif confirm in ("NO", "N"):
                        print("🔁 Vamos a realizar una nueva búsqueda...")
                        break  # Volverá al input de palabra_clave
                    else:
                        print("⚠️ Opción inválida. Escriba SI o NO.")
                except (KeyboardInterrupt, EOFError):
                    print("\n⚠️ Entrada inválida. Intente nuevamente...")
                    continue
            break  # Salir del while de elección si ya confirmó NO y quiere buscar otro



#print(Seleccionar_csv_en_pc())