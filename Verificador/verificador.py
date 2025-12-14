"""
Verificador de Terracode
"""

from Analizador.ASA import ASA #Importar el ASA
from Verificador.TablaSimbolos import TablaSimbolos #Importar la tabla de simbolos
from Verificador.Visitador import Visitador #Importar el visitador

class Verificador:
    """
    Clase que se encarga de verificar que no existan problemas de semántica
    """

    def __init__(self, asa_analizado: ASA):
        self.asa = asa_analizado

        self.tabla_simbolos = TablaSimbolos()

        self.visitador = Visitador(self.tabla_simbolos)

    def verificar(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna
        Funcionalidad: Decorar el ASA anteriormente generado
        """

        self.visitador.visitar(self.asa.nodo_raiz)

    def imprimir_asa(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna.
        Funcionalidad. Imprimir el nuevo asa
        """

        print("\033[36mASA decorado:\033[0m\n")
        self.asa.imprimir_asa()
