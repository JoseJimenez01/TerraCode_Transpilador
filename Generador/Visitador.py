
from Analizador.NodoASA import NodoASA

class Visitador:
    """
    Clase que visitará cada uno de los nodos para verificar el tipo de nodo,\n
    para así poder generar el código correspondiente al código del\n
    lenguaje TerraCode.\n

    Todos los métodos revisar reciben un nodo de tipo NodoASA, para\n
    poder hacer las visitas.
    """

    # Se manejara como la cantidad de espacios
    identacion = 0

    def visitar(self, nodo : NodoASA):
        """
        Método que recibe un nodo y lo visita según sea el tipo de nodo.\n
        Entrada: un nodo del ASA.\n
        Salida: todas las llamadas a los metodos que generan codigo .py segun el codigo .tc\n
        """

        if nodo.tipo == "Programa":
            self.__visitar_programa(nodo)

        elif nodo.tipo == "Instrucciones":
            self.__visitar_instrucciones(nodo)

        elif nodo.tipo == "Declaracion_semilla" or nodo.tipo == "Declaracion_maceta":
            self.__visitar_declaracion(nodo)

        elif nodo.tipo == "Funcion_Creada":
            self.__visitar_funcion_creada(nodo)

        elif nodo.tipo == "Identificador":
            self.__visitar_identificador(nodo)

        elif nodo.tipo == "Retorno":
            self.__visitar_retorno(nodo)

        elif nodo.tipo == "Funcion":
            self.__visitar_funcion(nodo)

        elif nodo.tipo == "Parametros":
            self.__visitar_parametros_funcion(nodo)

        elif nodo.tipo == "Ciclo":
            self.__visitar_ciclo(nodo)

        elif nodo.tipo == "Condicional":
            self.__visitar_condicional(nodo)

        elif nodo.tipo == "Bloque_If":
            self.__visitar_bloque_if(nodo)

        elif nodo.tipo == "Bloque_Else":
            self.__visitar_bloque_else(nodo)

        elif nodo.tipo == "Expresion":
            self.__visitar_expresion(nodo)

        elif nodo.tipo == "Expresion_Logica":
            self.__visitar_expresion_logica(nodo)

        elif nodo.tipo == "Expresion_Comparacion":
            self.__visitar_expresion_comparacion(nodo)

        elif nodo.tipo == "Expresion_Igualdad":
            self.__visitar_expresion_igualdad(nodo)

        elif nodo.tipo == "Expresion_Aritmetica":
            self.__visitar_expresion_aritmetica(nodo)

        elif nodo.tipo == "Expresion_Negación":
            self.__visitar_expresion_negacion(nodo)

        elif nodo.tipo == "Booleano":
            self.__visitar_booleano(nodo)

        elif nodo.tipo == "Entero":
            self.__visitar_entero(nodo)

        elif nodo.tipo == "Flotante":
            self.__visitar_flotante(nodo)

        elif nodo.tipo == "Concatenacion":
            self.__visitar_concatenacion(nodo)

        elif nodo.tipo == "Funcion_Imprimir":
            self.__visitar_funcion_imprimir(nodo)

        elif nodo.tipo == "Funcion_Largo":
            self.__visitar_funcion_largo(nodo)

        elif nodo.tipo == "Funcion_Entrada":
            self.__visitar_funcion_entrada(nodo)

        elif nodo.tipo == "Funcion_String_Entero":
            self.__visitar_funcion_string_entero(nodo)

        elif nodo.tipo == "Funcion_String_Flotante":
            self.__visitar_funcion_string_flotante(nodo)

        elif nodo.tipo == "String":
            self.__visitar_string(nodo)

        elif nodo.tipo == "Ciclo_Casos":
            self.__visitar_ciclo_casos(nodo)

        # elif nodo.tipo == "Opcion_Casos":
        #     self.__visitar_opcion_casos(nodo)

        # elif nodo.tipo == "Casos":
        #     self.__visitar_casos(nodo)

        # elif nodo.tipo == "Caso":
        #     self.__visitar_caso(nodo)

        # elif nodo.tipo == "Caso_Default":
        #     self.__visitar_caso_default(nodo)
        
        else:
            print(f"\033[31m No se reconoce el tipo de nodo: {nodo.tipo} \033[0m")

    def __visitar_programa(self, nodo_actual):
        """
        Programa ::= Instrucciones+
        """
        plantilla = """\ndef principal():\n{}\n

if __name__ == '__main__':
    principal()
"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        return plantilla.format('\n'.join(instrucciones[0]))
    
    def __visitar_instrucciones(self, nodo_actual):
        """
        Instrucciones ::= Comentario | Declaracion | FuncionCreada | Funcion | Repeticion |
                          Condicional | Imprimir | CicloCasos | Retorno
        """
        # Si no está en cero, es porque entró a una estructura que amerita identar el código dentro
        # Por lo tanto, agregamos la cantidad de espacios equivalentes a una identación
        if self.identacion != 0:
            self.identacion += 4

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instruccion = nodo.visitar(self)
            instruccion = self.__retornar_identacion() + instruccion
            instrucciones.append(instruccion)

        # Cuando visita las instrucciones, terminaía la estructura, por lo tanto quita la identación
        if self.identacion != 0:
            self.identacion -= 4

        return '\n'.join(instrucciones)

    def __visitar_declaracion(self, nodo_actual):
        """
        Declaracion ::= TipoVar Identificador "=" Expresion 
        TipoVar ::= "maceta" | "semilla"
        """

        plantilla = """{} {} = {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        return plantilla.format(instrucciones[0],instrucciones[1],instrucciones[2])

    def __visitar_funcion_creada(self, nodo_actual):
        """
        FuncionCreada :: = Identificador "(" ((ValorEstandar | Identificador) ( "," (ValorEstandar | Identificador))* )?")"
        """

        plantilla = """{}({})"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0], instrucciones[1])

    def __visitar_identificador(self, nodo_actual):
        """
        Identificador ::= [a-zA-Z][a-zA-Z0-9]*
        """
        return nodo_actual.contenido
    
    def __visitar_retorno(self, nodo_actual):
        """
        Retorno ::= “cosechar” ( Expresion)?
        """

        plantilla = 'return {}'
        valor = ''

        for nodo in nodo_actual.hijos:
            valor = nodo.visitar(self)

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(valor)

    def __visitar_funcion(self, nodo_actual):
        """
        Funcion ::= "sembrar" Identificador "(" (Parametros)? ")" "{" Instrucciones+ "}" "florecer"
        """
        
        # El código dentro, amerita que lo indenten
        self.identacion += 4

        plantilla = """\ndef {}({}):\n{}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        # Cuando se visitan las instrucciones, se terminaría la función
        self.identacion -= 4

        # Intercambia los valores devueltos en las comillas,
        # las instrucciones de la función se separan con un salto de línea
        return plantilla.format(instrucciones[0],instrucciones[1], '\n'.join(instrucciones[2]))

    def __visitar_parametros_funcion(self, nodo_actual):
        """
        Parametros ::= Identificador | ("," Identificador)*
        """
        parametros = []

        for nodo in nodo_actual.hijos:
            parametros.append(nodo.visitar(self))

        #Si la cantidad de parametros es mayor a uno, se separan usando comas
        if len(parametros) > 1:
            return ','.join(parametros)
        else:
            return ''
        
    def __visitar_ciclo(self, nodo_actual):
        """
        Repeticion ::= "fotosintesis" "(" Expresion ")" "{" Instrucciones+ "}" 
        """
        # El código dentro, amerita que lo indenten
        self.identacion += 4

        plantilla = """while {}:\n{}"""

        instrucciones = []

        # Visita la condición
        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Cuando se visitan las instrucciones, se terminaría la función
        self.identacion -= 4

        # Intercambia los valores devueltos en las comillas,
        # las instrucciones del while se separan con un salto de línea
        return plantilla.format(instrucciones[0],'\n'.join(instrucciones[1]))

    def __visitar_condicional(self, nodo_actual):
        """
        Condicional ::= If+ Else?
        """
        plantilla = """{}{}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0], '')

    def __visitar_bloque_if(self, nodo_actual):
        """
        If ::= "exterior" "(" Expresion ")" "{" Instrucciones+ "}"
        """
        # El código dentro, amerita que lo indenten
        self.identacion += 4

        plantilla = """if {}:\n{}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Cuando se visitan las instrucciones, se terminaría la función
        self.identacion -= 4

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0],'\n'.join(instrucciones[1]))

    def __visitar_bloque_else(self, nodo_actual):
        """
        Else ::= "interior" "{" Instrucciones+ "}"
        """
        # El código dentro, amerita que lo indenten
        self.identacion += 4

        plantilla = """else:\n    {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        # Cuando se visitan las instrucciones, se terminaría la función
        self.identacion -= 4

        # Intercambia los valores devueltos en las comillas
        return plantilla.format('\n'.join(instrucciones[0]))
    
    def __visitar_expresion(self, nodo_actual):
        """
        Expresion::= ExpresionLogica | ExpresionAritmetica | ExpresionComparacion | ExpresionIgualdad | ExpresionNegacion | Concatenacion | LlamadaFuncion | ValorEstandar
        """
        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones += [nodo.visitar(self)]

        return '\n'.join(instrucciones)

    def __visitar_expresion_logica(self, nodo_actual):
        """
        ExpresiónLogica ::= OpLogico "(" ExpresionLogicaTerm ("," ExpresionLogicaTerm)+ ")"
        OpLogico ::= "injerto" | "dioica"
        """
        plantilla = """{} {} {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # El operador logico pero en Python
        opLogico = self.__operador_logico(nodo_actual.contenido)

        # Se separan usando el operador logico de TerraCode pasado a python
        return plantilla.format(instrucciones[0], opLogico, instrucciones[2], ' ' + opLogico + ' '.join(instrucciones[3:]))

    def __operador_logico(self, operador):
        """
        Convierte el operador lógico de TerraCode a Python.
        """
        if operador == 'injerto':
            return 'and'

        elif operador == 'dioica':
            return 'or'

    def __visitar_expresion_comparacion(self, nodo_actual):
        """
        ExpresionComparacion ::= OpComparacion “(“ (ExpresionAritmeticaTerm) “,” (ExpresionAritmeticaTerm) “)”
        OpComparacion ::= "secuoya" | "bonsai" | "rosa" | "lirio"
        \nsecuoya: ">"\nbonsai: "<"\nrosa: ">="\nlirio: "<="
        """
        plantilla = """{} {} {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        opComparacion = self.__operador_comparacion(nodo_actual.contenido)

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0],opComparacion,instrucciones[2],' ' + opComparacion + ' '.join(instrucciones[3:]))

    def __operador_comparacion(self, operador):
        """
        Convierte el operador de comparación de TerraCode a Python.
        """
        if operador == 'secuoya':
            return '>'

        elif operador == 'bonsai':
            return '<'

        elif operador == 'rosa':
            return '>='

        elif operador == 'lirio':
            return '<='

    def __visitar_expresion_igualdad(self, nodo_actual):
        """
        ExpresionIgualdad ::= “cactus” “(“ (ExpresionAritmeticaTerm  | ValorEstandar) (“,” (ExpresionAritmeticaTerm  | ValorEstandar) ”)”
        """
        plantilla = """{} == {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0],instrucciones[1])

    def __visitar_expresion_aritmetica(self, nodo_actual):
        """
        ExpresionAritmetica ::= OpAritmetico”'(“ ExpresionAritmeticaTerm (“,” ExpresionAritmeticaTerm)+ “)”
        OpAritmetico ::= "sumatera" | "reseda" | "bambu" | "diosma" | "dalia" | "magnolia" | “conocarpus”
        """
        plantilla = """{} {} {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        opAritmetico = self.__operador_aritmetico(nodo_actual.contenido)

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0],opAritmetico,instrucciones[2],' ' + opAritmetico + ' '.join(instrucciones[3:]))

    def __operador_aritmetico(self, operador):
        """
        Convierte el operador aritmético de TerraCode a Python.
        """
        if operador == 'sumatera':
            return '+'

        elif operador == 'reseda':
            return '-'

        elif operador == 'bambu':
            return '*'

        elif operador == 'diosma':
            return '/'

        elif operador == 'dalia':
            return '//'

        elif operador == 'magnolia':
            return '%'

    def __visitar_expresion_negacion(self, nodo_actual):
        """
        ExpresionNegacion::= "acaro" ExpresionLogicaTerm
        """
        plantilla = """not {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0])

    def __visitar_booleano(self, nodo_actual):
        """
        ValorBooleano ::= "viva" | "muerta"
        """
        return {"viva": True, "muerta": False}.get(nodo_actual.contenido, False)

    def __visitar_entero(self, nodo_actual):
        """
        Entero ::= ("+"|"-")?[0-9]+
        """
        return nodo_actual.contenido

    def __visitar_flotante(self, nodo_actual):
        """
        Flotante ::= ("+"|"-")?[0-9]+"."[0-9]+
        """
        return nodo_actual.contenido

    def __visitar_concatenacion(self, nodo_actual):
        """
        Concatenacion ::= "conocarpus" "(" (String | Identificador ) ("," (String | Identificador))+ ")"
        """
        plantilla = """{} + {}"""

        instrucciones = []

        for nodo in nodo_actual.hijos:
            instrucciones.append(nodo.visitar(self))

        # Intercambia los valores devueltos en las comillas
        return plantilla.format(instrucciones[0], ', '.join(instrucciones[1:]))

    def __visitar_funcion_imprimir(self, nodo_actual):
        """
        Retorna el contenido de la funcion, se llamara con las funciones de ambiente estandar ya definidas.
        """
        return "podar(" + nodo_actual.hijos[0].visitar(self) + ")"

    def __visitar_funcion_largo(self, nodo_actual):
        """
        Retorna el contenido de la funcion, se llamara con las funciones de ambiente estandar ya definidas.
        """
        return "medir(" + nodo_actual.hijos[0].visitar(self) + ")"

    def __visitar_funcion_entrada(self, nodo_actual):
        """
        Retorna el contenido de la funcion, se llamara con las funciones de ambiente estandar ya definidas.
        """
        return "recolectar(" + nodo_actual.hijos[0].visitar(self) + ")"

    def __visitar_funcion_string_entero(self, nodo_actual):
        """
        Retorna el contenido de la funcion, se llamara con las funciones de ambiente estandar ya definidas.
        """
        return "madurar(" + nodo_actual.hijos[0].visitar(self) + ")"

    def __visitar_funcion_string_flotante(self, nodo_actual):
        """
        Retorna el contenido de la funcion, se llamara con las funciones de ambiente estandar ya definidas.
        """
        return "germinar(" + nodo_actual.hijos[0].visitar(self) + ")"

    def __visitar_string(self, nodo_actual):
        """
        String ::= “#” Texto “#”
        Texto ::= [A-Z]?[a-z]?[0-9]?[ÁÉÍÓÚáéíóúÑñÜü ]*

        Aunque se está usando:\n
        '#.*?#'\n
        en el explorador.
        """
        return nodo_actual.contenido.replace('#', '"')

    def __visitar_ciclo_casos(self, nodo_actual):
        """
        CicloCasos ::= "planta" "(" Expresion ")" "{" Instrucciones "flor" Identificador "=" Expresion Casos+ CasoDefault "}"
        
        planta(Expresion) {
            Instrucciones
            flor Identificador = Expresion
            
            Casos+
            
            CasoDefault
        }
        """
        # La estructura como tal es un ciclo
        self.__visitar_ciclo(nodo_actual)

    # def __visitar_opcion_casos(nodo):
    #     """
    #     Casos ::= "hoja_compuesta" "(" ValorEstandar ")" "{" Instrucciones+ "}"

    #     hoja_compuesta( ValorEstandar ) {
    #         Instrucciones+
    #     }
    #     """
    
    # elif nodo.tipo is "OpcionCasos":
    #     self.__visitar_opcion_casos(nodo)

    # elif nodo.tipo is "Casos":
    #     self.__visitar_casos(nodo)

    # elif nodo.tipo is "Caso":
    #     self.__visitar_caso(nodo)

    # elif nodo.tipo is "CasoDefault":
    #     self.__visitar_caso_default(nodo)

    # CicloCasos ::= "planta" "(" Expresion ")" "{" Instrucciones “flor” Identificador ‘=’ Expresion Casos+ CasoDefault "}" 
    # Casos ::= "hoja_compuesta" "(" ValorEstandar ")" "{" Instrucciones+ "}"
    # CasoDefault ::= "hoja_simple" "(" ")" "{" Instrucciones+ "}"

    def __retornar_identacion(self):
        """
        Retorna la cantidad de espacios correspondientes a la identación actual.
        """
        return " " * self.identacion
    






