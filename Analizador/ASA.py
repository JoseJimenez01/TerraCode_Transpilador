"""
Clase ASA
"""

from Analizador.NodoASA import NodoASA

class ASA:
    """
    Clase que representa el Árbol Sintáctico Abstracto (ASA)
    """
    nodo_raiz: NodoASA

    def imprimir_asa(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna.
        Funcionalidad: Imprimir el arból ASA.
        """

        print("\n\033[36mÁrbol de Sintaxis Abstracta (ASA):\033[0m")
        self.__imprimir_preorden(self.nodo_raiz)

    def __imprimir_preorden(self, nodo: NodoASA, nivel=0):
        """
        Entrada: nodo: El nodo a imprimir, nivel: El nivel del arból en el que se encuentra el nodo.
        Salida: Ninguna.
        Funcionalidad: Imprime el árbol ASA en preorden.
        """

        if nodo is None:
            return

        print(f"{'  ' * nivel}{nodo}")

        for hijo in nodo.hijos:
            self.__imprimir_preorden(hijo, nivel + 1)
