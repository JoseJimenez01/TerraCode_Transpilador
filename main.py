"""
Archivo principal del programa.
Funcionalidad: Verificar si el archivo que contiene el código cumple
    con la gramática definida.
"""

import argparse
from Archivos.cargarArchivo import cargar_prueba
from Explorador.explorador import Scanner
from errores import imprimir_errores
from Analizador.analizador import Analizador
from Verificador.verificador import Verificador
from Generador.Generador import Generador

# Crear el parser
parser = argparse.ArgumentParser(description="Archivo del código fuente")
parser.add_argument("path", type=str, help="Ruta del archivo")

def main():
    """
    Funcionalidad:
    Punto de entrada principal del programa. Carga una prueba,
    ejecuta el análisis léxico e imprime resultados.
    """

    args = parser.parse_args()

    # Cargar el archivo de prueba
    print(f"\033[34mCargando archivo desde:\033[0m \033[33m{args.path}\033[0m")
    lineas = cargar_prueba(args.path)

    # Explorador
    print("\033[34mIniciando análisis léxico...\033[0m")
    scanner = Scanner(lineas)
    scanner.escanear()

    # Imprimir tokens generados (opcional para depuración)
    #scanner.imprimir_tokens()

    # Imprimir errores léxicos (si los hay)
    errores_lexicos = scanner.obtener_errores()
    if errores_lexicos:
        imprimir_errores(errores_lexicos, args.path, 1)
        return  # Detener ejecución si hay errores léxicos

    # Analizador
    print("\n\033[34mIniciando análisis sintáctico...\033[0m")
    analizador = Analizador(scanner.tokens)
    analizador.analizar()
    analizador.imprimir_asa()

    # Imprimir errores sintácticos (si los hay)
    errores_sintacticos = analizador.obtener_errores()
    if errores_sintacticos:
        imprimir_errores(errores_sintacticos, args.path, 2)
        return  # Detener ejecución si hay errores sintácticos

    print("\n\033[34mIniciando análisis semántico...\033[0m\n")
    #verificador = Verificador(analizador.asa)
    #verificador.verificar()
    #verificador.imprimir_asa()

    #generador = Generador(analizador.asa)
    #generador.generar()
    #generador.imprimir_asa()

if __name__ == "__main__":
    main()
