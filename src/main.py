import json
import os
import platform


def limpiar_consola():
    """
    Limpia la consola dependiendo del sistema operativo.
    """
    # Tenemos que tener en cuenta el sistema operativo
    os.system("cls" if platform.system() == "Windows" else "clear")


def pausar():
    """
    Pausa la ejecución hasta que el usuario presione una tecla.
    """

    input("\nPresione una tecla para continuar . . .\n")


def cargar_json(ruta):
    """
    Carga un archivo JSON y devuelve su contenido como dict.

    Args:
        ruta (str): Ruta del archivo JSON.
    """
    if not os.path.exists(ruta):
        print(f"ERROR El archivo '{ruta}' no existe.")
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError: # Capturamos error de formato JSON (creo que es el correcto)
        print(f"ERROR El archivo '{ruta}' tiene un formato JSON inválido.")
        return None


def guardar_json(ruta, data):
    """
    Guarda un diccionario en un archivo JSON.

    Args:
        ruta (str): Ruta del archivo JSON.
        data (dict): Datos a guardar.
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def mostrar_datos(data):
    """
    Muestra en pantalla los usuarios del JSON.

    Args:
        data (dict): Datos cargados del JSON.
    """
    print("\n--- Contenido Actual del JSON ---")

    if data is None or "usuarios" not in data or len(data["usuarios"]) == 0:
        print("ERROR El archivo JSON no contiene usuarios!")
        print("--- Fin del Contenido ---\n")
        return

    for u in data["usuarios"]:
        print(f"ID: {u['id']}, Nombre: {u['nombre']}, Edad: {u['edad']}")

    print("--- Fin del Contenido ---\n")


def inicializar_datos(archivo_origen, archivo_destino):
    """
    Copia el contenido del archivo origen al destino con manejo de errores.

    Args:
        archivo_origen (str): Ruta del archivo JSON origen.
        archivo_destino (str): Ruta del archivo JSON destino.
    """

    if not os.path.exists(archivo_origen):
        print(f"ERROR El archivo origen '{archivo_origen}' no existe. No se realizó la copia.")
        return False

    try:
        with open(archivo_origen, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR El archivo origen '{archivo_origen}' tiene un formato JSON inválido.")
        return False

    guardar_json(archivo_destino, data)
    print(f"Datos inicializados desde '{archivo_origen}' a '{archivo_destino}'.")
    return True


def main():
    archivo_origen = "datos_usuarios_orig.json"
    archivo_destino = "datos_usuarios.json"

    limpiar_consola()

    if not inicializar_datos(archivo_origen, archivo_destino):
        return

    data = cargar_json(archivo_destino)
    if data is None:
        return

    mostrar_datos(data)
    pausar()

    for u in data["usuarios"]:
        if u["id"] == 1:
            u["edad"] = 31
            print("Usuario con ID 1 actualizado.")
            break

    mostrar_datos(data)
    pausar()

    nuevo_usuario = {"id": 3, "nombre": "Pedro", "edad": 40}
    data["usuarios"].append(nuevo_usuario)
    print("Usuario Pedro añadido con éxito.")

    mostrar_datos(data)
    pausar()

    data["usuarios"] = [usuario for usuario in data["usuarios"] if usuario["id"] != 2]
    print("Usuario con ID 2 eliminado.")

    mostrar_datos(data)
    pausar()

    guardar_json("datos_usuarios.json", data)

    print("Operaciones completadas. Archivo actualizado.")

if __name__ == "__main__":
    main()
