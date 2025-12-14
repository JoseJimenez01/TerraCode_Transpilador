"""
Clase NodoASA
"""

class NodoASA:
    """
    Clase que representa un nodo en el Árbol Sintáctico Abstracto (ASA).\n
    """

    def __init__(self, tipo, contenido, atributos=None):
        self.tipo = tipo
        self.contenido = contenido
        self.atributos = atributos or {}
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        """
        Entrada: nodo_hijo: El nuevo nodo a agregar.
        Salida: Ninguna.
        Funcionalidad: Agregar un nodo hijo al nodo.
        """
        self.hijos.append(nodo_hijo)

    def visitar(self, visitador):
        """
        Entrada: visitador: Un objeto visitador que implementa el patrón Visitor.
        Salida: El resultado de la visita al nodo.
        Funcionalidad: Método que permite visitar un nodo del ASA.
        """
        return visitador.visitar(self)

    def __str__(self):
        # Colocar la información del nodo
        info = f"<\"{self.tipo}\", \"{self.contenido}\", {self.atributos}>"

        return info
