"""
Clases para los tokens
"""

from enum import Enum, auto

class TipoToken(Enum):
    """
    Enum que define los tipos de tokens posibles del lenguaje TerraCode.
    """
    COMENTARIO = auto()
    PALABRA_CLAVE = auto()
    CONDICIONAL = auto()
    REPETICION = auto()
    ASIGNACION = auto()
    OPERADOR = auto()
    COMPARADOR = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    VALOR_VERDAD = auto()
    PUNTUACION = auto()
    ESPACIOS = auto()
    ESTRUCTURA_DATOS = auto()
    ERROR = auto()

class Token:
    """
    Clase que representa un token identificado en el análisis léxico.

    Atributos:
    - tipo: TipoToken → Tipo de token.
    - lexema: str → Fragmento del código que coincide con el token.
    - linea: int → Línea del archivo donde se encontró.
    """
    def __init__(self, tipo: TipoToken, lexema: str, linea: int):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea

    def __str__(self):
        """
        Salida: str
        Funcionalidad: Representación del token como string.
        """
        return f'{self.tipo.name:20} | {self.lexema:20} | Línea: {self.linea}'
