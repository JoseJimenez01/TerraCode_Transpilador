"""
Archivo encargado de cargar el archivo de terracode
"""

def cargar_prueba(ruta_archivo):
    """
    Entrada: ruta_archivo (str) → Ruta al archivo de prueba

    Salida: Lista de líneas de texto

    Funcionalidad: 
    Lee el contenido de un archivo de prueba y lo devuelve línea por línea.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        return archivo.readlines()
