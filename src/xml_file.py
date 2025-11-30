import os
import xml.etree.ElementTree as ET
import shutil
import json_file


def cargar_xml(ruta):
    """
    Carga un XML y devuelve su árbol. Si falla retorna None.

    Args:
        ruta (str): Ruta del archivo XML.
    """
    if not os.path.exists(ruta):
        print(f"ERROR El archivo '{ruta}' no existe.")
        return None

    try:
        return ET.parse(ruta)
    except ET.ParseError:
        print(f"ERROR El archivo '{ruta}' tiene un formato XML inválido.")
        return None


def guardar_xml(arbol, ruta):
    """
    Guarda un árbol XML en archivo.

    Args:
        arbol (ElementTree): Árbol XML a guardar.
        ruta (str): Ruta del archivo XML.
    """
    arbol.write(ruta, encoding="utf-8", xml_declaration=True)


def crear_arbol(nombre_raiz):
    """
    Genera un árbol XML vacío con un nodo raíz.

    Args:
        nombre_raiz (str): Nombre del nodo raíz.
    """
    raiz = ET.Element(nombre_raiz)
    return ET.ElementTree(raiz)


def mostrar_datos(raiz):
    """
    Muestra los usuarios del XML.

    Args:
        raiz (Element): Nodo raíz del árbol XML.
    """
    print("\n--- Contenido Actual del XML ---")

    usuarios = raiz.findall("usuario")

    if len(usuarios) == 0:
        print("ERROR No hay usuarios en el archivo XML.")
        print("--- Fin del Contenido ---\n")
        return

    for u in usuarios:
        id_ = u.find("id").text
        nombre = u.find("nombre").text
        edad = u.find("edad").text
        print(f"ID: {id_}, Nombre: {nombre}, Edad: {edad}")

    print("--- Fin del Contenido ---\n")


def inicializar_datos(archivo_origen, archivo_destino):
    """
    Copia el archivo XML origen al destino, con manejo de errores.

    Args:
        archivo_origen (str): Ruta del archivo XML origen.
        archivo_destino (str): Ruta del archivo XML destino.
    """

    if not os.path.exists(archivo_origen):
        print(f"ERROR El archivo origen '{archivo_origen}' no existe. No se realizó la copia.")
        return False

    try:
        ET.parse(archivo_origen)
    except ET.ParseError:
        print(f"ERROR El archivo origen '{archivo_origen}' tiene un formato XML inválido.")
        return False

    shutil.copy(archivo_origen, archivo_destino)
    print(f"Datos inicializados desde '{archivo_origen}' a '{archivo_destino}'.")
    return True


def main():
    archivo_origen = "datos_usuarios_orig.xml"
    archivo_destino = "datos_usuarios.xml"

    # Usamos las funciones de json_file para limpiar y pausar, reutilizando código del anterior ejercicio.
    json_file.limpiar_consola()

    inicializado = inicializar_datos(archivo_origen, archivo_destino)

    arbol = cargar_xml(archivo_destino)

    if arbol is None:
        arbol = crear_arbol("usuarios")

    raiz = arbol.getroot()

    mostrar_datos(raiz)
    json_file.pausar()

    for u in raiz.findall("usuario"):
        if u.find("id").text == "1":
            u.find("edad").text = "31"
            print("Usuario con ID 1 actualizado.")
            break

    mostrar_datos(raiz)
    json_file.pausar()

    nuevo = ET.Element("usuario")
    ET.SubElement(nuevo, "id").text = "3"
    ET.SubElement(nuevo, "nombre").text = "Pedro"
    ET.SubElement(nuevo, "edad").text = "40"

    raiz.append(nuevo)
    print("Usuario Pedro añadido con éxito.")

    mostrar_datos(raiz)
    json_file.pausar()

    for u in raiz.findall("usuario"):
        if u.find("id").text == "2":
            raiz.remove(u)
            print("Usuario con ID 2 eliminado.")
            break

    mostrar_datos(raiz)
    json_file.pausar()

    guardar_xml(arbol, archivo_destino)

    print("Operaciones completadas. Archivo actualizado.")


if __name__ == "__main__":
    main()
