"""
Archivo principal del programa.
Funcionalidad: Verificar si el archivo que contiene el código cumple
    con la gramática definida.
"""

import argparse
import os
from errores import imprimir_errores
from Archivos.cargarArchivo import cargar_prueba
from Explorador.explorador import Scanner
from Analizador.analizador import Analizador
from Verificador.verificador import Verificador
from Generador.Generador import Generador

# Crear el parser
parser = argparse.ArgumentParser(description="\033[32mTranspilador para el lenguaje Terracode\033[0m")
parser.add_argument('--solo_explorar', dest='explorador', action='store_true',
    help="Ejecuta el código hasta el explorador.")
parser.add_argument('--solo_analizar', dest='analizador', action='store_true',
    help="Ejecuta el código hasta el analizador.")
parser.add_argument('--solo_verificar', dest='verificador', action='store_true',
    help="Ejecuta el código hasta el verificador.")
parser.add_argument('--generar_python', dest='python', action='store_true',
    help="Genera el código Python equivalente.")
parser.add_argument('path', type=str, help="Ruta del archivo .tc")

def main():
    """
    Punto de entrada principal del programa. Lee el archivo con código en
    lenguaje Terracode, el archivo debe estar con extensión ".tc",
    dependiendo de la flag, ejecuta hasta cierto punto o genera código python.
    """

    args = parser.parse_args()

    # Cargar el archivo de prueba
    lineas = cargar_prueba(args.path)
    print(f"\033[34mCargando archivo desde:\033[0m \033[33m{os.path.abspath(args.path)}\033[0m")

    if args.explorador is True:
        
        # Explorador
        print("\033[34mHaciendo análisis léxico...\033[0m")
        explorador = Scanner(lineas)
        explorador.escanear()
        explorador.imprimir_tokens()

        # Imprimir errores léxicos (si los hay)
        if explorador.imprirmirErrores(args.path) == -1: return
        
    elif args.analizador is True:

        print("\n\033[34mHaciendo análisis sintáctico...\033[0m")

        #Explorador
        explorador = Scanner(lineas)
        explorador.escanear()
        if explorador.imprirmirErrores(args.path) == -1: return
        
        # Analizador
        analizador = Analizador(explorador.tokens)
        analizador.analizar()
        analizador.imprimir_asa()

        # Imprimir errores sintácticos (si los hay)
        if analizador.imprimirErrores(args.path) == -1: return

    elif args.verificador is True:

        print("\n\033[34mHaciendo análisis semántico...\033[0m\n")

        #Explorador
        explorador = Scanner(lineas)
        explorador.escanear()
        if explorador.imprirmirErrores(args.path) == -1: return

        # Analizador
        analizador = Analizador(explorador.tokens)
        analizador.analizar()
        if analizador.imprimirErrores(args.path) == -1: return
        
        # Verificador
        verificador = Verificador(analizador.asa)
        verificador.verificar()
        verificador.imprimir_asa()

    elif args.python is True:

        print("\n\033[34mGenerando código en Python\033[0m\n")

        #Explorador
        explorador = Scanner(lineas)
        explorador.escanear()
        if explorador.imprirmirErrores(args.path) == -1: return

        # Analizador
        analizador = Analizador(explorador.tokens)
        analizador.analizar()
        if analizador.imprimirErrores(args.path) == -1: return
        
        # Verificador
        verificador = Verificador(analizador.asa)
        verificador.verificar()

        # Generador
        generador = Generador(verificador.asa)
        generador.generar()
        generador.imprimir_asa()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
