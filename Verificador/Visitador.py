"""
Clase Visitador
"""

from Verificador.TablaSimbolos import TablaSimbolos
from Analizador.NodoASA import NodoASA

class Visitador:
    """
    Clase que tiene los métodos para visitar cada nodo del ASA según sea el tipo de nodo.\n
    Cuando baja por el árbol, va revisando los identificadores y los agrega a la tabla de símbolos,\n
    luego visita los subnodos, y cuando va subiendo hace la inferencia de tipos.\n
    Esto se hacer por cada uno de los nodos del ASA.\n
    """

    def __init__(self, nueva_tabla_simbolos: TablaSimbolos):
        self.tabla_simbolos = nueva_tabla_simbolos
        self.errores = []

    def visitar(self, nodo : NodoASA):
        """
        Entrada: un nodo del ASA.
        Salida: Ninguna.
        Funcionalidad: Recibe el nodo raiz y visita el nod programa
        """

        if nodo.tipo == "Programa":
            self.__visitar_programa(nodo)

        else:
            self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}')

    def __visitar_programa(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo actual que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Programa.

        Nodos: Instrucciones
        """
        for nodo in nodo_actual.hijos:
            self.__visitar_instrucciones(nodo)

    def __visitar_instrucciones(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Instrucciones.

        Nodos: Declaracio_Maceta, Declaracion_Semilla, Funcion_Creada, Retorno, Funcion, Ciclo\n
        Condicional, Funcion_Imprimir, Ciclo_Casos
        """
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            
            # Vistar los nodos válidos
            if nodo.tipo == "Declaracion_maceta":
                self.__visitar_declaracion_maceta(nodo)

            elif nodo.tipo == "Declaracion_semilla":
                self.__visitar_declaracion_semilla(nodo)
            
            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)

            elif nodo.tipo == "Retorno":
                self.__visitar_retorno(nodo)

            elif nodo.tipo == "Funcion":
                self.__visitar_funcion(nodo)

            elif nodo.tipo == "Ciclo":
                self.__visitar_ciclo(nodo)

            elif nodo.tipo == "Condicional":
                self.__visitar_condicional(nodo)

            elif nodo.tipo == "Funcion_Imprimir":
                self.__visitar_funcion_imprimir(nodo)

            elif nodo.tipo == "Ciclo_Casos":
                self.__visitar_ciclo_casos(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo} como nodo hijo de Instrucciones')
                return

    def __visitar_declaracion_maceta(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Declaracio_Maceta.

        Nodos: Expresion, Concatenacion, Funcion_Largo, Funcion_Entrada,\n
        Funcion_String_Entero, Funcion_String_Flotante, Funcion_Creada

        Declaracion ::= "maceta" Identificador "=" Expresion
        """

        # No se verifica la existencia porque en este lenguaje se permite la sobre asignacion

        # Pasar por los nodos hijos de la declaracion
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            
            # Vistar los nodos válidos
            if nodo.tipo == "Expresion":
                self.__visitar_expresion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')
            
            elif nodo.tipo == "Concatenacion":
                self.__visitar_concatenacion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')
            
            elif nodo.tipo == "Funcion_Largo":
                self.__visitar_funcion_largo(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_Entrada":
                self.__visitar_funcion_entrada(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_String_Entero":
                self.__visitar_funcion_string_entero(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_String_Flotante":
                self.__visitar_funcion_string_flotante(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)
                tipo = nodo.atributos.get('tipo')

                # Verificar que no devuleva un ninguno
                # Si es asi, no puede ser una declaración
                if tipo == "Ninguno":
                    self.__error_encontrado(f"La declaración '{nodo_actual.contenido}' no acepta tipos Ninguno y '{nodo.contenido}' retorna Ninguno")
                    return
                
                else:
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Declaracion_maceta')
                return

        # Se infiere el tipo cuando sus nodos son visitados
        # Esto porque dependiendo de la expresión su tipo es diferente

        # Se agrega información al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Impresión de prueba
        print(self.tabla_simbolos)

    def __visitar_declaracion_semilla(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Declaracio_Maceta.

        Nodos: Expresion, Concatenacion, Funcion_Largo, Funcion_Entrada,\n
        Funcion_String_Entero, Funcion_String_Flotante, Funcion_Creada

        Declaracion ::= "semilla" Identificador "=" Expresion 
        Esta es global
        """

        # Verificar que este en el nivel 0 porque es una variable global
        if self.tabla_simbolos.nivel != 0:
            self.__error_encontrado(f"La variable '{nodo_actual.contenido}' es una variable global y no se encuentar donde debería")
            return

        # No se verifica la existencia porque es permitido la re asignacion de variables

        #Pasar por los nodos hijos de la declaracion
        nodo : NodoASA
        for nodo in nodo_actual.hijos:

            # Vistar los nodos válidos
            if nodo.tipo == "Expresion":
                self.__visitar_expresion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Concatenacion":
                self.__visitar_concatenacion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_Largo":
                self.__visitar_funcion_largo(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_Entrada":
                self.__visitar_funcion_entrada(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_String_Entero":
                self.__visitar_funcion_string_entero(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_String_Flotante":
                self.__visitar_funcion_string_flotante(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)
                tipo = nodo.atributos.get('tipo')

                # Verificar que no devuleva un ninguno
                # Si es asi, no puede ser una declaración
                if tipo == "Ninguno":
                    self.__error_encontrado(f"La declaración '{nodo_actual.contenido}' no acepta tipos Ninguno y '{nodo.contenido}' retorna Ninguno")
                    return

                else:
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Declaracion_semilla')
                return

        # Se infiere el tipo cuando sus nodos son visitados
        # Esto porque dependiendo de la expresión su tipo es diferente

        # Se agrega información al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_creada(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_Creada.

        Nodos: Parametros, Entero, Flotante, String, Booleano

        FuncionCreada :: = Identificador "(" ((ValorEstandar | Identificador) ( "," (ValorEstandar | Identificador))* )?")"
        """

        # Se verifica si ya existe la función que se intenta llamar
        registro = self.tabla_simbolos.verificar_existencia(nodo_actual.contenido)

        if registro is None:
            # Dar error de que no existe la función
            self.__error_encontrado(f"No se encuentra la función '{nodo_actual.contenido}'")
            return

        else:
            # Verificar si es una función o una variable
            if registro['referencia'].tipo != "Funcion":
                self.__error_encontrado(f"El nombre '{nodo_actual.contenido}' ya fue usado en una variable")
                return

        # Cantidad de los parametros de la referencia
        nodo_funcion = registro['referencia']
        nodo_parametros_funcion = nodo_funcion.hijos[0] # El primer nodo hijo de funcion es Parametros (si es que posee)

        cantidad_esperada = 0

        if nodo_parametros_funcion.tipo == "Parametros":
            cantidad_esperada = len(nodo_parametros_funcion.hijos)

        # Cantidad de parametros del nodo de funcion creada
        cantidad_actual = 0
        nodo_parametros = nodo_actual.hijos[0]  # Único hijo es "Parametros"

        if nodo_actual.hijos:
            if nodo_parametros.tipo == "Parametros":
                cantidad_actual = len(nodo_parametros.hijos)
            else:
                # No deberia entrar aquí, pero no esta demás verificar
                self.__error_encontrado(f"Se esperaba el nodo 'Parametros' en '{nodo_actual.contenido}'")
                return

        # Verificar que se tenga la misma cantidad de parametros
        if cantidad_esperada == cantidad_actual:
            if cantidad_actual != 0:

                conta = 0
                # Verificar que sean del mismo tipo
                for nodo_parametro_funcion in nodo_parametros_funcion.hijos:
                    tipo_parametro_funcion = nodo_parametro_funcion.atributos.get('tipo')

                    # Visitamos el parametro de la función creada
                    self.__visitar_parametros(nodo_parametros)
                    tipo_parametro = nodo_parametros.hijos[conta].atributos.get('tipo')

                    # Verificar si son iguales o si es un Cualquiera
                    if ((tipo_parametro_funcion != tipo_parametro) and (tipo_parametro_funcion != "Cualquiera")):
                        self.__error_encontrado(f"En la llamada de la función '{nodo_actual.contenido}' se esperaba el tipo {tipo_parametro_funcion} para el parametro '{nodo_parametro_funcion.contenido}'")
                        return
                    
                    conta += 1
        else:
            self.__error_encontrado(f"Se esperaban {cantidad_esperada} argumentos en la llmada de la función '{nodo_actual.contenido}', pero se pasaron {cantidad_actual}")
            return
        
        # Inferir tipo
        # Se infiere el tipo dependiendo de lo que devuelva la función
        nodo_actual.atributos['tipo'] = registro['referencia'].atributos.get('tipo')

    def __visitar_retorno(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Retorno.

        Nodos: Expresion, Concatenacion, Funcion_Largo, Funcion_Entrada,\n
        Funcion_String_Entero, Funcion_String_Flotante, Identificador, Funcion_Creada

        Retorno ::= "cosechar" (Expresion | Identificador)?
        """

        # Verificar si tiene algún nodo hijo
        # Si es asi entonces se visitan
        if nodo_actual.hijos:
            nodo : NodoASA
            for nodo in nodo_actual.hijos:
                # Vistar los nodos válidos
                if nodo.tipo == "Expresion":
                    self.__visitar_expresion(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Concatenacion":
                    self.__visitar_concatenacion(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Funcion_Largo":
                    self.__visitar_funcion_largo(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Funcion_Entrada":
                    self.__visitar_funcion_entrada(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Funcion_String_Entero":
                    self.__visitar_funcion_string_entero(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Funcion_String_Flotante":
                    self.__visitar_funcion_string_flotante(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Identificador":
                    self.__visitar_identificador(nodo)
                    nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                elif nodo.tipo == "Funcion_Creada":
                    self.__visitar_funcion_creada(nodo)
                    tipo = nodo.atributos.get('tipo')

                    # Verificar que no devuleva un ninguno
                    # Si es asi, no deberia ponerse en el retorno
                    if tipo == "Ninguno":
                        self.__error_encontrado(f"La función '{nodo.contenido}' retorna Ninguno y esta en 'cosechar', intenta ponerla en otro lugar")
                        return

                    else:
                        nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

                else:
                    self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Retorno')
                    return
        
        else:
            # Si no tiene un nodo hijo, no devuelve nada
            nodo_actual.atributos['tipo'] = "Ninguno"

        # Se infiere el tipo cuando sus nodos son visitados
        # Esto porque dependiendo de la expresión su tipo es diferente

        # Se agrega información al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion.

        Nodos: Parametros, Instrucciones

        Funcion ::= "sembrar" Identificador "(" (Parametros)? ")" "{" Instrucciones+ "}" "florecer"
        """

        # Verificar si ya existe la función
        registro = self.tabla_simbolos.verificar_existencia(nodo_actual.contenido)

        if registro is not None:
            self.__error_encontrado(f"El nombre '{nodo_actual.contenido}' ya fue usado")
            return
        
        # Si no existe, se abre un nuevo nivel
        self.tabla_simbolos.abrir_nivel()

        # Se visitan los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            if nodo.tipo == "Parametros":
                self.__visitar_parametros(nodo)

            elif nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion')

        # Se hace la inferencia de tipo buscando el nodo retorno en el registro
        registros = self.tabla_simbolos.tabla
        for registro in registros:
            nodo_registro = registro['referencia']
            nivel_registro = registro.get('nivel')

            if ((nodo_registro.tipo == "Retorno") and (nivel_registro == self.tabla_simbolos.nivel)):
                nodo_actual.atributos['tipo'] = nodo_registro.atributos.get('tipo')

        # Una vez, termina de visitar la función se cierra el nivel
        self.tabla_simbolos.cerrar_nivel()

        # Se agrega el registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Impresión de prueba
        print(self.tabla_simbolos)

    def __visitar_parametros(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Parametros.

        Nodos: Identificador, Entero, Flotante, String, Booleano

        Parametros ::= Identificador | ("," Identificador)*
        Para funcion creada los parametros pueden ser identificador o un valor estandar
        """

        # No se agrega al registro por que no hay necesidad de inferir su tipo
        # Si se agregar los al registro los nodos hijos

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            if nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

            elif nodo.tipo == "Entero":
                self.__visitar_entero(nodo)

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)

            elif nodo.tipo == "String":
                self.__visitar_string(nodo)

            elif nodo.tipo == "Booleano":
                self.__visitar_booleano(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Parametros')

    def __visitar_ciclo(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Ciclo.

        Nodos: Expresion, Funcion_Creada, Instrucciones

        Repeticion ::= "fotosintesis" "(" Expresion ")" "{" Instrucciones+ "}"
        """

        # Abrir nuevo nivel
        self.tabla_simbolos.abrir_nivel()

        # Se vista los nodos hijos del ciclo
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Vistar los nodos válidos
            if nodo.tipo == "Expresion":
                self.__visitar_expresion(nodo)

                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'fotosintesis' debe ser de tipo Booleano")
                    return

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)

                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'fotosintesis' debe ser de tipo Booleano")
                    return

            elif nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como no hijo de Ciclo')
                return

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Una vez visitado todo el ciclo se cierra el nivel
        self.tabla_simbolos.cerrar_nivel()

    def __visitar_condicional(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Condicional.

        Nodos: Bloque_If, Bloque_Else

        Condicional ::= If Else?
        """

        # Acá no se va a abrir el nivel

        # Visitar sus nodos hijo
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Verificar que sea el nodo especificado
            if nodo.tipo == "Bloque_If":
                self.__visitar_bloque_if(nodo)

            elif nodo.tipo == "Bloque_Else":
                self.__visitar_bloque_else(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Condicional')
                return
        
        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_bloque_if(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Bloque_If.

        Nodos: Expresion, Funcion_Creada, Instrucciones

        If ::= "exterior" "(" Expresion ")" "{" Instrucciones+ "}"
        """

        # Abrir nivel
        self.tabla_simbolos.abrir_nivel()

        # Visitar los nodos hijos de Bloque_If
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar los nodos identificados
            if nodo.tipo == "Expresión":
                self.__visitar_expresion(nodo)

                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'exterior' debe ser de tipo Booleano")
                    return

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)
                
                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'exterior' debe ser de tipo Booleano")
                    return
                
            elif nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Bloque_If')
                return
            
        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)
            
        # Cerrar el nivel, una vez visitado todo el nodo
        self.tabla_simbolos.cerrar_nivel()

    def __visitar_bloque_else(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Bloque_Else.

        Nodos: Instrucciones

        Else ::= "interior" "{" Instrucciones+ "}"
        """

        # Abrir nivel
        self.tabla_simbolos.abrir_nivel()

        # Visitar el nodo Instrucciones si este existe
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            if nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Bloque_Else')
                return

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Cerrar el nivel, una vez visitado todo el nodo
        self.tabla_simbolos.cerrar_nivel()

    def __visitar_expresion(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion.

        Nodos: Expresion_Logica, Expresion_Comparacion, Expresion_Igualdad \n
        Expresion_Aritmetica, Expresion_Negacion

        Expresion ::= ExpresionLogica | Concatenacion |
        ExpresionAritmetica | ExpresionIgualdad | ExpresionComparacion |
        ExpresionNegacion | LlamadaFuncion | ValorEstandar
        """

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Expresion_Logica":
                self.__visitar_expresion_logica(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Expresion_Comparacion":
                self.__visitar_expresion_comparacion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Expresion_Igualdad":
                self.__visitar_expresion_igualdad(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Expresion_Aritmetica":
                self.__visitar_expresion_aritmetica(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Expresion_Negacion":
                self.__visitar_expresion_negacion(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion')
                return
        
        # Agregar al registro
        # ¿Elimino esto? De todas formas el que cuenta es el de la expresión en especifico
        # Además el contenido esta vacio
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Impresión de prueba
        print(self.tabla_simbolos)

    def __visitar_expresion_logica(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion_Logica.

        Nodos: Expresion_Logica, Expresion_Comparacion, Expresion_Igualdad
        Expresion_Negacion, Booleano, Identificador

        ExpresiónLogica ::= OpLogico '(' ExpresionLogicaTerm (',' ExpresionLogicaTerm)+ ')'
        ExpresionLogicaTerm ::= ExpresionComparacion | ExpresionIgualdad | ValorBooleano | ExpresionNegacion | ExpresionLogica | Identificador
        """

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Expresion_Logica":
                self.__visitar_expresion_logica(nodo)

            elif nodo.tipo == "Expresion_Comparacion":
                self.__visitar_expresion_comparacion(nodo)

            elif nodo.tipo == "Expresion_Igualdad":
                self.__visitar_expresion_igualdad(nodo)

            elif nodo.tipo == "Expresion_Negacion":
                self.__visitar_expresion_negacion(nodo)

            elif nodo.tipo == "Booleano":
                self.__visitar_booleano(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que el identificador sea del tipo booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":

                    # Hacemos la inferencia de tipo
                    if tipo == "Ninguno":
                        # Buscamos el registro para encontrar la referencia y cambiar su tipo
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Booleano"

                        # Tambien se hace la inferencia de tipo de este nodo para decorar el arból
                        nodo.atributos['tipo'] = "Booleano"
                    else:
                        self.__error_encontrado("Se esperaba un Booleano como tipo del identificador para la expresión lógica")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion_Logica')
                return

        # Se hace la inferencia
        nodo_actual.atributos['tipo'] = "Booleano"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_expresion_comparacion(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion_Comparacion.

        Nodos: Entero, Flotante, Identificador, Expresion_Artitmetica

        ExpresionComparacion ::= OpComparacion '(' (ExpresionAritmeticaTerm) ',' (ExpresionAritmeticaTerm) ')'
        ExpresionAritmeticaTerm ::= Entero | Flotante | Identificador | ExpresionAritmetica
        """

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Entero":
                self.__visitar_entero(nodo)

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que su tipo sea el correcto
                tipo = nodo.atributos.get('tipo')

                if tipo not in ('Entero', 'Flotante'):

                    # Hacemos la inferencia
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Flotante"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Flotante"
                    else:
                        self.__error_encontrado("Se esperaba un Flotante o Entero como tipo del identificador para la expresión de comparación")
                        return

            elif nodo.tipo == "Expresion_Artitmetica":
                self.__visitar_expresion_aritmetica(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion_Comparacion')
                return
            
        # Se infiere su tipo
        nodo_actual.atributos['tipo'] = "Booleano"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_expresion_igualdad(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion_Igualdad.

        Nodos: Entero, Flotante, String, Booleano, Identificador, Expresion_Artitmetica

        ExpresionIgualdad ::= 'cactus' '(' (ExpresionAritmeticaTerm | ValorEstandar | Identificador) ',' (ExpresionAritmeticaTerm | ValorEstandar | Identificador) ')'
        ExpresionAritmeticaTerm ::= Entero | Flotante | Identificador | ExpresionAritmetica
        """

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Entero":
                self.__visitar_entero(nodo)

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)

            elif nodo.tipo == "String":
                self.__visitar_string(nodo)

            elif nodo.tipo == "Booleano":
                self.__visitar_booleano(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que su tipo sea el correcto
                tipo = nodo.atributos.get('tipo')
                if tipo not in ('Entero', 'Flotante', 'String', 'Booleano'):
                    
                    # Inferirmos el tipo a Cualquiera si el tipo es Ninguno
                    # Muy dificil hacer la inferencia del tipo cuando literalmente puede ser cualquiera
                    if tipo == "Ninguno":
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Cualquiera"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Cualquiera"
                    else:
                        self.__error_encontrado("Se esperaba un Flotante, Entero, String o Booleano como tipo del identificador para la expresión de igualdad")
                        return

            elif nodo.tipo == "Expresion_Artitmetica":
                self.__visitar_expresion_aritmetica(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion_Igualdad')
                return

        # Se infiere su tipo
        nodo_actual.atributos['tipo'] = "Booleano"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_expresion_aritmetica(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion_Aritmetica.

        Nodos: Entero, Flotante, Identificador, Expresion_Artitmetica

        ExpresionAritmetica ::= OpAritmetico '(' ExpresionAritmeticaTerm (',' ExpresionAritmeticaTerm)+ ')'
        ExpresionAritmeticaTerm ::= Entero | Flotante | Identificador | ExpresionAritmetica
        """
        # Se crea un contador de flotantes
        # Esto para lograr inferir el tipo
        # Ya que con un solo flotante el resultado termina siendo flotante
        flotantes = 0

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Entero":
                self.__visitar_entero(nodo)

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)
                flotantes += 1

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que su tipo sea el correcto
                tipo = nodo.atributos.get('tipo')

                if tipo not in ('Entero', 'Flotante'):

                    # Hacemos inferencia de tipo
                    if tipo == "Ninguno":
                        # Se le da tipo Flotante porque es más fácil
                        # Es más facil porque existe el 3.0, si lo que quisiera poner es 3 entero
                        # Si fuera entrero no podria usar el 3.3 porque solo aceptaria 3

                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Flotante"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Flotante"
                        flotantes += 1
                    else:
                        self.__error_encontrado("Se esperaba un Flotante o Entero como tipo del identificador para la expresión de aritmetica")
                        return

            elif nodo.tipo == "Expresion_Artitmetica":
                self.__visitar_expresion_aritmetica(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion_Aritmetica')
                return

        # Inferir tipo
        # Si es una division entera (dalia) siempre va a ser entero
        if nodo_actual.contenido == "dalia":
            nodo_actual.atributos['tipo'] = "Entero"

        # Si es una divison (diosma) siempre va a ser flotante (más fácil así)
        # Ya que dependiendo de los números dados es entero o flotante y eso no lo sabemos
        elif nodo_actual.contenido == "diosma":
            nodo_actual.atributos['tipo'] = "Flotante"

        # Todos los demás siguen la regla del flotante
        else:
            if flotantes == 0:
                nodo_actual.atributos['tipo'] = "Entero"
            else:
                nodo_actual.atributos['tipo'] = "Flotante"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Impresión de prueba
        print(self.tabla_simbolos)

    def __visitar_expresion_negacion(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Expresion_Negacion.

        Nodos: Expresion_Logica, Expresion_Comparacion, Expresion_Igualdad
        Expresion_Negacion, Booleano, Identificador

        ExpresionNegacion::= "acaro" ExpresionLogicaTerm
        ExpresionLogicaTerm ::= ExpresionComparacion | ExpresionIgualdad | ValorBooleano | ExpresionNegacion | ExpresionLogica | Identificador
        """

        # Visitar nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Expresion_Logica":
                self.__visitar_expresion_logica(nodo)

            elif nodo.tipo == "Expresion_Comparacion":
                self.__visitar_expresion_comparacion(nodo)

            elif nodo.tipo == "Expresion_Igualdad":
                self.__visitar_expresion_igualdad(nodo)

            elif nodo.tipo == "Expresion_Negacion":
                self.__visitar_expresion_negacion(nodo)

            elif nodo.tipo == "Booleano":
                self.__visitar_booleano(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que el identificador sea del tipo booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":

                    # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Booleano"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Booleano"
                    else:
                        self.__error_encontrado("Se esperaba un Booleano como tipo del identificador para la expresión de negación")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Expresion_Negacion')
                return

        # Se infiere su tipo
        nodo_actual.atributos['tipo'] = "Booleano"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_concatenacion(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Concatenacion.

        Nodos: String, Identificador

        Concatenacion ::= “conocarpus” “(“ (String | Identificador) (“,” (String | Identificador))+ “)”
        """

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                tipo= nodo.atributos.get('tipo')
                if tipo != "String":

                    # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "String"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "String"
                    else:
                        self.__error_encontrado("Se esperaba un String como tipo en el identificador para la función 'conocarpus'")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Concatenacion')
                return

        # Se infiere su tipo
        nodo_actual.atributos['tipo'] = "String"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_imprimir(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_Imprimir.

        Nodos: String, Identificador

        Imprimir ::= "podar" "(" String | Identificador ("," (String | Identificador))* ")"
        """

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que sea un string
                tipo= nodo.atributos.get('tipo')
                if tipo != "String":

                    # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "String"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "String"
                    else:
                        self.__error_encontrado("Se esperaba un String como tipo en el identificador para la función 'podar'")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion_Imprimir')
                return
            
        # Se infiere un tipo Ninguno porque no devuelve algo
        nodo_actual.atributos['tipo'] = "Ninguno"

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_largo(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_Largo.

        Nodos: String, Identificador

        Largo ::= "medir" "(" (String | Identificador) ")"
        """

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que el identificador sea un string
                tipo = nodo.atributos.get('tipo')

                if tipo != "String":

                     # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "String"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "String"
                    else:
                        self.__error_encontrado("Se esperaba un String como tipo en el identificador para la función 'medir'")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion_Largo')
                return
            
        # Se infiere su tipo
        nodo_actual.atributos['tipo'] = "Entero"
            
        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_entrada(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_Entrada.

        Nodos: String

        Entrada ::= "recolectar" "(" String ")"
        """

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Visitar el nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion_Largo')
                return
            
        # Inferir su tipo
        nodo_actual.atributos['tipo'] = "String"

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_string_entero(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_String_Entero.

        Nodos: String, Entero, Identificador

        StringEntero ::= "madurar" "(" String | Entero | Identificador ")"
        Devuelve un entero
        """

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

                # Dependiendo del argumneto dado, inferimos el tipo de salida
                nodo_actual.atributos['tipo'] = "Entero"

            elif nodo.tipo == "Entero":
                self.__visitar_entero(nodo)

                # Dependiendo del argumneto dado, inferimos el tipo de salida
                nodo_actual.atributos['tipo'] = "String"

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que el identificador sea un string
                tipo = nodo.atributos.get('tipo')

                if tipo == "String":
                    nodo_actual.atributos['tipo'] = "Entero"
                elif tipo == "Entero":
                    nodo_actual.atributos['tipo'] = "String"
                else:

                    # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Cualquiera"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Cualquiera"
                    else:
                        self.__error_encontrado("Se esperaba un String o Entero como tipo del identificador para la función 'madurar'")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion_String_Entero')
                return

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_funcion_string_flotante(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Funcion_String_Flotante.

        Nodos: String, Identificador

        StringFlotante ::= "germinar" "(" (String | Flotante | Identificador) ")"
        """

        # Visitar los nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "String":
                self.__visitar_string(nodo)

                # Dependiendo dl argumneto dado, inferimos el tipo de salida
                nodo_actual.atributos['tipo'] = "Flotante"

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)

                # Dependiendo del argumneto dado, inferimos el tipo de salida
                nodo_actual.atributos['tipo'] = "String"

            elif nodo.tipo == "Identificador":
                self.__visitar_identificador(nodo)

                # Verificar que el identificador sea un string
                tipo = nodo.atributos.get('tipo')

                if tipo == "String":
                    nodo_actual.atributos['tipo'] = "Flotante"
                elif tipo == "Entero":
                    nodo_actual.atributos['tipo'] = "String"
                else:

                     # Hacemos la inferencia de tipos
                    if tipo == "Ninguno":
                        # Buscamos el registro para cambiar el tipo en la referencia en si
                        registro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
                        registro['referencia'].atributos['tipo']  = "Cualquiera"

                        # Tambien cambiamos el tipo en este nodo, ya que hay que decorar el arbol
                        nodo.atributos['tipo']  = "Cualquiera"
                    else:
                        self.__error_encontrado("Se esperaba un String o Flotante como tipo del identificador para la función 'germinar'")
                        return

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Funcion_String_Flotante')
                return

        # Agregar al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_ciclo_casos(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Ciclo_Casos.

        Nodos: Expresion, Funcion_Creada, Instrucciones, Opcion_Casos, Casos

        CicloCasos ::= "planta" "(" Expresion ")" "{" Instrucciones+ “flor” Identificador '=' Expresion Casos+ CasoDefault "}"
        """

        # Abrir un nuevo nivel
        self.tabla_simbolos.abrir_nivel()

        # Visitar sus nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Expresion":
                self.__visitar_expresion(nodo)

                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'fotosintesis' debe ser de tipo Booleano")
                    return

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)

                # Verificar que sea un Booleano
                tipo = nodo.atributos.get('tipo')
                if tipo != "Booleano":
                    self.__error_encontrado("La condición de 'fotosintesis' debe ser de tipo Booleano")
                    return

            elif nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            elif nodo.tipo == "Opcion_Casos":
                self.__visitar_opcion_casos(nodo)

            elif nodo.tipo == "Casos":
                self.__visitar_casos(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Ciclo_Casos')
                return

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Cerrar el nivel
        self.tabla_simbolos.cerrar_nivel()

    def __visitar_opcion_casos(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Opcion_Casos.

        Nodos: Identificador, Expresion, Funcion_Entrada, Funcion_Largo, Funcion_Creada

        CicloCasos ::= [...] “flor” Identificador '=' Expresion [...]
        """

        # Lo que se hace a continuación no sé si este bien pero es lo que se me ocurrió
        # Esto es para ver si los casos y la opción coinciden en el tipo
        # Si se le ocurre alguna otra solución, arreglelo sin problemas, jajaj

        # Verificar que el identificador no exista
        # Aqui no se permite la sobre asignacion
        nodo_identificador = nodo_actual.hijos[0] # El primer nodo de Opcion_Casos es el de Identificador
        registro = self.tabla_simbolos.verificar_existencia(nodo_identificador.contenido)

        if registro is not None:
            self.__error_encontrado(f"La variable '{nodo_identificador.contenido}' ya fue usada, se debe usar otra después para 'flor'")
            return

        # Visitar sus nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Identificador":
                # Guardar el nodo de identificador
                nodo_identificador = nodo

            elif nodo.tipo == "Expresion":
                self.__visitar_expresion(nodo)
                tipo = nodo.atributos.get('tipo')

                # Inferir el tipo
                nodo_identificador.atributos['tipo'] = tipo
                self.tabla_simbolos.nuevo_registro(nodo_identificador)

                nodo_actual.atributos['tipo'] = tipo

            elif nodo.tipo == "Funcion_Entrada":
                self.__visitar_funcion_entrada(nodo)
                tipo = nodo.atributos.get('tipo')

                # Inferir el tipo
                nodo_identificador.atributos['tipo'] = tipo
                self.tabla_simbolos.nuevo_registro(nodo_identificador)

                nodo_actual.atributos['tipo'] = tipo

            elif nodo.tipo == "Funcion_Largo":
                self.__visitar_funcion_largo(nodo)
                tipo = nodo.atributos.get('tipo')

                # Inferir el tipo
                nodo_identificador.atributos['tipo'] = tipo
                self.tabla_simbolos.nuevo_registro(nodo_identificador)

                nodo_actual.atributos['tipo'] = tipo

            elif nodo.tipo == "Funcion_Creada":
                self.__visitar_funcion_creada(nodo)
                tipo = nodo.atributos.get('tipo')

                # Verificar si no es un tipo Ninguno
                if tipo == "Ninguno":
                    self.__error_encontrado(f"No se puede asignar un tipo Ninguno a la variable '{nodo_identificador.contenido}'")
                    return

                else:
                    # Inferir el tipo
                    nodo_identificador.atributos['tipo'] = tipo
                    self.tabla_simbolos.nuevo_registro(nodo_identificador)

                    nodo_actual.atributos['tipo'] = tipo

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Opcion_Casos')
                return

        # La inferencia se hace en la visita de nodos porque puede ser diferentes tipos

        # Añadir al registro
        # Aqui se añade en nombre con flor para que sea facil de identificar más adelante en los casos
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_casos(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Casos.

        Nodos: Caso, Caso_Default

        CicloCasos ::= [...] Casos+ CasoDefault [...]
        """

        # Visitar sus nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Caso":
                self.__visitar_caso(nodo)

            elif nodo.tipo == "Caso_Default":
                self.__visitar_caso_default(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Casos')
                return
            
        # No se añaden en el registro porque esta función solo sirve como puente a los casos
        # La verdad no veo la necesidad

    def __visitar_caso(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Caso.

        Nodos: Entero, Flotante, String, Booleano, Instrucciones

        Casos ::= ("hoja_compuesta" "(" ValorEstandar ")" "{" Instrucciones+ "}")
        """
        # Creo que lo que voy a aplicar a continuación no se deberia hacer asi
        # Pero fue lo que se me ocurrió
        # Si se le ocurre alguna otra solución, es libre de aplicarla, jajaj

        # Buscar el registro de flor
        registro = self.tabla_simbolos.verificar_existencia('flor')

        # Si no se encuentra el registro hay problemas
        if registro is None:
            self.__error_encontrado("No se encontró la opción del caso")
            return

        # Verificar que sea el ciclo del nivel en el que se esta
        # Si no es asi estamos en probelmas
        if registro['nivel'] != self.tabla_simbolos.nivel:
            self.__error_encontrado("No se ha creado un ciclo de caso")
            return

        # Conseguir el tipo del atributo del registro
        atributo = registro['referencia'].atributos
        tipo_atributo = atributo.get('tipo')

        # A continuación se va a ser la inferencia de tipo

        # Abrir nuevo nivel para los casos
        self.tabla_simbolos.abrir_nivel()

        # Visitar sus nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Entero":
                self.__visitar_entero(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Flotante":
                self.__visitar_flotante(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "String":
                self.__visitar_string(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Booleano":
                self.__visitar_booleano(nodo)
                nodo_actual.atributos['tipo'] = nodo.atributos.get('tipo')

            elif nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Caso')
                return

        # Se infiere los tipos en las visitas ya que pueden ser distintos tipos

        # Conseguir el tipo del nodo_actual
        tipo_actual = nodo_actual.atributos.get('tipo')

        # Verificar que sean del mismo tipo que el que se definió en Opcion_Casos
        if tipo_atributo != tipo_actual:
            nodo_iden_atr = atributo.hijos[0]
            self.__error_encontrado(f"El tipo de dato en '{nodo_iden_atr.contenido}' no es el mismo que el del caso")
            self.__error_encontrado(f"Se esperaba un tipo {tipo_atributo} y se dio un tipo {tipo_actual}")
            return

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Cerrar el nivel
        self.tabla_simbolos.cerrar_nivel()

    def __visitar_caso_default(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita los nodos hijos de Caso_Default.

        Nodos: Instrucciones

        CasoDefault ::= "hoja_simple" "(" ")" "{" Instrucciones+ "}"
        """
        # Aqui no se verifica nada

        # En el default no hay tipo entonces seria ninguno
        nodo_actual.atributos['tipo'] = "Ninguno"

        # Visitar sus nodos hijos
        nodo : NodoASA
        for nodo in nodo_actual.hijos:
            # Visitar nodos
            if nodo.tipo == "Instrucciones":
                self.__visitar_instrucciones(nodo)

            else:
                self.__error_encontrado(f'No se reconoce el tipo de nodo: {nodo.tipo}, como nodo hijo de Caso_Deafult')
                return

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_entero(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita el nodo Entero.
        """

        # Decorar con entero
        nodo_actual.atributos['tipo'] = "Entero"

        # Añadir al registro
        # Sera que elimino esto tambien? Para que quiero referenciar a un entero?
        self.tabla_simbolos.nuevo_registro(nodo_actual)

        # Impresión de prueba
        print(self.tabla_simbolos)

    def __visitar_flotante(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita el nodo Flotante.
        """

        # Decorar con flotante
        nodo_actual.atributos['tipo'] = "Flotante"

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_string(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita el nodo String.
        """

        # Decorar con string
        nodo_actual.atributos['tipo'] = "String"

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_booleano(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita el nodo Booleano.
        """

        # Decorar con booleano
        nodo_actual.atributos['tipo'] = "Booleano"

        # Añadir al registro
        self.tabla_simbolos.nuevo_registro(nodo_actual)

    def __visitar_identificador(self, nodo_actual : NodoASA):
        """
        Entrada: nodo_actual: El nodo que se esta visitando.
        Salida: Ninguna.
        Funcionalidad: Visita el nodo Identificador.
        """

        # Verificar existencia
        registro = self.tabla_simbolos.verificar_existencia(nodo_actual.contenido)

        if not registro:
            self.__error_encontrado(
                f"Identificador '{nodo_actual.contenido}' no declarado.",
                nodo_actual
            )
            
        # Verificar si ya existe o no el registro
        if registro is None:
            # Si no se existe uno se da uno tipo Ninguno
            # Aunque no deberia entrar aqui. Si entra aquí hay algo malo
            nodo_actual.atributos['tipo'] = "Ninguno"

            # Añadir al registro
            self.tabla_simbolos.nuevo_registro(nodo_actual)

            # Impresión de prueba
            print(self.tabla_simbolos)

        else:
            # Verificar que se tenga un atributo para agregarlo
            tipo = registro['referencia'].atributos.get('tipo')
            if tipo:
                nodo_actual.atributos['tipo'] = tipo

    def __error_encontrado(self, mensaje, nodo=None):
        """
        Imprime y almacena un mensaje de error semántico.
        Si se proporciona el nodo, intenta mostrar la línea o información adicional.
        """
        info = ""
        if nodo and hasattr(nodo, "linea"):
            info = f" (línea {nodo.linea})"
        error_msg = f"\033[91m[Error semántico]{info}: {mensaje}\033[0m"
        print(error_msg)
        self.errores.append(error_msg)

    def imprimir_errores(self):
        """
        Imprime todos los errores acumulados, si existen.
        """
        if self.errores:
            print("\n\033[91mResumen de errores semánticos:\033[0m")
            for err in self.errores:
                print(err)
        else:
            print("\033[92mNo se encontraron errores semánticos.\033[0m")
