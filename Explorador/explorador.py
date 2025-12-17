"""
Explorador de Terracode
"""

import re
from Explorador.tokens import TipoToken, Token
from errores import imprimir_errores

class Scanner:
    """
    Clase principal del analizador léxico.

    Entrada: 
    - lineas_codigo: lista de líneas de texto del archivo fuente.

    Salida: 
    - Lista de tokens válidos y lista de errores léxicos.

    Funcionalidad:
    Analiza el código fuente en busca de tokens definidos según patrones
    del lenguaje TerraCode. Si encuentra errores, aplica recuperación por pánico.
    """
    patrones_token = [
        (TipoToken.COMENTARIO, r'\*[^*]*\*'),
        (TipoToken.PALABRA_CLAVE, r'\b(sembrar|florecer|maceta|semilla|podar|medir|recolectar)\b'),
        (TipoToken.CONDICIONAL, r'\b(exterior|interior)\b'),
        (TipoToken.REPETICION, r'\b(fotosintesis)\b'),
        (TipoToken.ASIGNACION, r'='),
        (TipoToken.OPERADOR, r'\b(sumatra|reseda|bambu|diosma|dalia|magnolia|injerto|dioica|acaro|conocarpus)\b'),
        (TipoToken.COMPARADOR, r'\b(secuoya|bonsai|cactus|rosa|lirio)\b'),
        (TipoToken.VALOR_VERDAD, r'\b(viva|muerta)\b'),
        (TipoToken.ESTRUCTURA_DATOS, r'\b(planta|flor|hoja_compuesta|hoja_simple|cosechar|madurar|germinar)\b'),
        (TipoToken.TEXTO, r'#.*?#'),
        (TipoToken.FLOTANTE, r'[-+]?\d+\.\d+'),
        (TipoToken.ENTERO, r'[-+]?\d+'),
        (TipoToken.IDENTIFICADOR, r'[a-zA-Z_][a-zA-Z0-9_]*'),
        (TipoToken.PUNTUACION, r'[(){};,]'),
        (TipoToken.ESPACIOS, r'\s+'),
    ]

    def __init__(self, lineas_codigo):
        self.lineas = lineas_codigo
        self.tokens = []
        self.errores = []

    def escanear(self):
        """
        Entrada: Ninguna

        Salida: None

        Funcionalidad:
        Recorre todas las líneas del código fuente y analiza cada una
        para extraer tokens o detectar errores.
        """

        for num_linea, linea in enumerate(self.lineas, start=1):
            self._procesar_linea(linea.strip(), num_linea)

    def _procesar_linea(self, linea, num_linea):
        """
        Entrada:
        - linea: str → línea de código fuente
        - num_linea: int → número de línea

        Salida: None

        Funcionalidad:
        Aplica los patrones para extraer tokens. Si no hay coincidencias,
        marca un error y aplica recuperación por pánico.
        """
        while linea:
            # Sí, el else es del for.
            for tipo, patron in self.patrones_token:
                match = re.match(patron, linea)
                if match:
                    # Valida que si existe un numero entero o flotante, si el
                    # caracter que sigue es un string, lo determine como error,
                    # porque un identificador no puede empezar con numeros
                    if (tipo == TipoToken.ENTERO or tipo == TipoToken.FLOTANTE) and \
                        len(linea) > match.end() and linea[match.end()].isalnum() and \
                        not re.match(self.patrones_token[5][1], linea[match.end():]) and \
                        not re.match(self.patrones_token[6][1], linea[match.end():]):
                        caracter_erroneo = match.group()
                        self.errores.append((caracter_erroneo, num_linea))

                    lexema = match.group()
                    if tipo not in [TipoToken.ESPACIOS, TipoToken.COMENTARIO]:
                        self.tokens.append(Token(tipo, lexema, num_linea))
                    linea = linea[match.end():]
                    break
            else:
                # Guarda informacion de errores y recorta el string para
                # seguir validando
                caracter_erroneo = linea[0]
                self.errores.append((caracter_erroneo, num_linea))
                posicion_recuperacion = max(linea.find(';'), linea.find('}'))
                if posicion_recuperacion != -1:
                    linea = linea[posicion_recuperacion+1:]
                else:
                    break
    def imprimir_tokens(self):
        """
        Entrada: None
        Salida: None
        Funcionalidad: Imprime por consola todos los tokens válidos encontrados.
        """
        print("\033[36m\nLista de tokens encontrados:\033[0m")
        for token in self.tokens:
            print(token)

    def obtener_errores(self):
        """
        Entrada: None
        Salida: Lista de errores léxicos
        Funcionalidad: Devuelve la lista de errores para ser usados fuera.
        """
        return self.errores

    def imprirmirErrores(self, path):
        """
        Obtiene los errores lexicos que se hayan almacenado y los imprime

        :param path: La ruta del archivo .tc para formateo del error.
        :returns: -1 si hay errores, 0 si no hay.
        """
        errores_lexicos = self.obtener_errores()

        if errores_lexicos:
            imprimir_errores(errores_lexicos, path, 1)
            return -1
        return 0