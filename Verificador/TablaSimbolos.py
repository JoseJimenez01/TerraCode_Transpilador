"""
Clase TablaSimbolos
"""

from Analizador.NodoASA import NodoASA

class TablaSimbolos:
    """
    Funcianlidada: Guarda información necesaria para decorar el ASA, 
    junto con la información de tipo y alcance.
    Estructura:
    [
        {key: valor, ...},
        {key: valor, ...},
        ...
    ]
    """
    def __init__(self):
        self.nivel = 0
        self.tabla = []

    def abrir_nivel(self):
        """
        Entrada: Ninguna.
        Saida: Ninguna.
        Funcionalidad: Inicia un nuevo nivel.
        """

        self.nivel += 1
        print(self)

    def cerrar_nivel(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna.
        Funcionalidad: Se cierra el nivel en el que se esat y al hacerlo elimina todos
        los registros de la tabla que estan en ese nivel.
        """

        # Si existen registros en el nivel se eliminan
        for registro in self.tabla:
            if registro['nivel'] == self.nivel:
                self.tabla.remove(registro)

        self.nivel -= 1
        print(self)

    def nuevo_registro(self, nodo: NodoASA):
        """
        Entrada: nodo: El nodo que se va a agregar a la tabla.
        Salida: Ninguna. 
        Funcionalidad: Agrega un nuevo registro a la tabla.
        """

        # Crear el diccionario como nueo registro
        registro = {}

        # Añadir la información del registro
        registro['nombre'] = nodo.contenido
        registro['nivel'] = self.nivel
        registro['referencia'] = nodo

        # Agregar el disccionario a la tabla
        self.tabla.append(registro)
        print(self)

    def verificar_existencia(self, nombre):
        """
        Eantrada: nombre: Nombre del identificador que se busca.
        Salida: regitro: El registro del identificador encontrado, None: Si no se encuentra.
        Funcionalidad: Verifica si un identificador existe cómo variable/función global o local.
        """

        # Buscar por todos los registros de la tabla
        for registro in self.tabla:
            # Si existe, devuelve el registro
            if (registro['nombre'] == nombre and registro['nivel'] <= self.nivel):
                return registro

        return None

    def __str__(self):
        titulo = "\n\033[36mTABLA DE SÍMBOLOS\033[0m  "
        titulo += "Nivel Actual: " + str(self.nivel) + "\n"
        titulo += "-" *40 + "\n"

        cabecera = '{:<20}\t{:<10}\t{:<15}\n'.format("Nombre", "Nivel", "Tipo")
        cabecera += "-" * 50 + "\n"

        fila = ""
        for registro in self.tabla:
            fila += '{:<20}\t{:<10}\t{:<15}\n'.format(
                str(registro['nombre']),
                str(registro['nivel']),
                str(registro['referencia'].atributos.get('tipo', 'Desconocido'))
            )

        return titulo + cabecera + fila
