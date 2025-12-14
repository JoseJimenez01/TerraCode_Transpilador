"""
Imprime los errores
"""

import os

def imprimir_errores(errores, path, tipo):
    """
    Entrada: 
    - errores: lista de tuplas.
    - path: Ubicación del archivo.
    - tipo: tipo de error (1 - Léxico, 2 - Sintáctico, 3 - Semántico)

    Salida: None (imprime en consola)

    Funcionalidad:
    Muestra los errores detectados.
    """
    if errores:

        # Dar el mensaje de error dependiendo del tipo
        #Los errores van a ser vistos como 'plagas'
        if tipo == 1:
            print(f"\n\033[34mPlagas léxicas encontradas en el jardín\033[0m \033[33m{os.path.abspath(path)}\033[0m:")

            for caracter, linea in errores:
                print(f"  \033[31mError: Se encontró una oruga '{caracter}' en la rama {linea} \033[0m")
            print(" ")
        
        elif tipo == 2:
            print(f"\n\033[34mPlagas sintácticas encontradas en el jardín:\033[0m \033[33m{os.path.abspath(path)}\033[0m:")
            print("\033[34m-- Se encontró un pulgón llevandose cosas de tú jardín --\033[0m")

            for mensaje, linea in errores:
                print(f"  \033[31mError: {mensaje} en la rama {linea}.\033[0m")
            print(" ")

        elif tipo == 3:
            print(f"\n\033[34mPlagas semánticas encontradas en el jardín:\033[0m \033[33m{os.path.abspath(path)}\033[0m:")
            print("\033[34m-- Se encontró una babosa cambiando cosas de tú jardín --\033[0m")

            for mensaje, linea in errores:
                print(f"  \033[31mError: {mensaje} en la rama {linea}.\033[0m")
            print(" ")


