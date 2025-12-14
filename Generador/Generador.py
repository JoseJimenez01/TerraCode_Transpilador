
from Analizador.ASA import ASA
from Generador.Visitador import Visitador

class Generador:
    """
    Clase que carga las funciones del ambiente estándar,\n
    a su vez recorre el ASA para poder generar el código de\n
    python según el código definido.
    """
    asa            : ASA
    visitador      : Visitador

    ambiente_estandar = """import sys

def podar(texto):
    print(texto)

def medir(texto):
    return len(texto)

def recolectar(info=""):
    return input(info)    

def madurar(string):
    return int(string)

def germinar(string):
    return float(string)

"""

    def __init__(self, nuevo_asa: ASA):
        self.asa            = nuevo_asa
        self.visitador      = Visitador() 

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.nodo_raiz is None:
            print([])
        else:
            self.asa.__imprimir_preorden()

    def generar(self):
        """
        Genera el código de python a partir del ASA.
        """
        
        codigo_generado = self.visitador.visitar(self.asa.nodo_raiz)
        print(self.ambiente_estandar)
        print(codigo_generado)


