"""
Analizador de Terracode
"""

from Explorador.explorador import TipoToken # Importar explorador y los tokens
from Analizador.NodoASA import NodoASA # Importar la clase NodoASA
from Analizador.ASA import ASA #Imporatar la clase ASA
from errores import imprimir_errores


class Analizador:
    """
    Clase que se encarga de analizar y ver que se cumpla con la gramatica
    evitando problemas sintácticos.
    """

    def __init__(self, tokens_lista):
        """
        Entrada: tokens_lista: Lista de tokens que procesar.
        Salida: Ninguna.
        FUncionalidad: Inicializar el analizador con una lista de tokens.
        """
        self.tokens = tokens_lista
        self.numero_tokens = len(tokens_lista)

        # Verifica si el la lista de tokens viene vacio o no.
        if tokens_lista != []:
            self.token_actual = tokens_lista[0] # Primer token disponible
        else:
            self.token_actual = None

        self.posicion_token_actual = 0 # Posicion inicial

        self.asa = ASA() #Crear el arból

        self.errores = [] # Lista para guardar los errores

    # Método principal que analiza el programa
    def analizar(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna.
        Funcionalidad: Inicia el análisis del programa.
        """

        # Se inicia el analisis, si hay tokens que analizar
        if self.token_actual is not None:
            nodo_asa = self.__analizar_programa()
            self.asa.nodo_raiz = nodo_asa

    def __analizar_programa(self):
        """
        Entrada: Ninguna.
        Salida: nodo_raiz: EL nodo raiz generada durante el analisis del programa.
        Funcionalidad: Analiza el programa completo.

        Programa ::= Instrucciones+
        """

        nodo_raiz = NodoASA(tipo="Programa", contenido="")

        # Crear el nodo de las instrucciones
        nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")

        while not self.__verificar_final():
        
            if self.__verificar_instrucciones():
                nodo_instruccion = self.__analizar_instrucciones()
                nodo_instrucciones.agregar_hijo(nodo_instruccion)

            # Si no se encuentra una instruccion valida entonces no es un programa de Terracode
            else:
                self.__error_detectado("Tú jardin contiene plantas desconocidas - instrucciones no válidas para el programa")

        nodo_raiz.agregar_hijo(nodo_instrucciones)

        return nodo_raiz

    def __analizar_instrucciones(self):
        """
        Entrada: Ninguna.
        Salida: nodo_instruccion: Nodo con las instrucciones identificadas 
        Funcionalidad: Analiza cual instrucción se va a analizar.

        Instrucciones ::= Comentario | Declaracion | FuncionCreada | Funcion | Repeticion | Condicional | Imprimir | CicloCasos | Retorno
        """

        # Comentarios no se analizan

        # Verificar que sea una declaración para analizarla
        if(self.__verificar_palabra_clave("maceta") or self.__verificar_palabra_clave("semilla")):
            nodo_declaracion = self.__analizar_declaracion()

            return nodo_declaracion
        
        # Verificar qeu sea la plabra clave para retornar y asi analizarlo
        elif self.__verificar_estructura_datos("cosechar"):
            nodo_retorno = self.__analizar_retorno()

            return nodo_retorno

        # Verificar que sea una funcion creada para analizarla
        elif self.__verificar_identificador():
            nodo_funcion_creada = self.__analizar_funcion_creada()

            return nodo_funcion_creada

        # Verificar qeu sea una función para analizarla
        elif self.__verificar_palabra_clave("sembrar"):
            nodo_funcion = self.__analizar_funcion()

            return nodo_funcion

        # Verificar que sea un bucle para analizarlo
        elif (self.token_actual.tipo == TipoToken.REPETICION and self.token_actual.lexema == "fotosintesis") :
            nodo_repeticion = self.__analizar_repeticion()

            return nodo_repeticion

        # Verificar que sea una función condicional para analizarla
        elif self.__verificar_condicional("exterior"):
            nodo_condicional = self.__analizar_condicional()

            return nodo_condicional

        # Verificar que sea a palabra clave para la función de imprimir y asi analizarla
        elif self.__verificar_palabra_clave("podar"):
            nodo_funcion_imprimir = self.__analizar_imprimir()

            return nodo_funcion_imprimir

        # Verificar que sea la palabra clave para el ciclo de casos para asi analizarlo
        elif self.__verificar_estructura_datos("planta"):
            nodo_ciclo_casos = self.__analizar_ciclo_casos()

            return nodo_ciclo_casos

    def __verificar_instrucciones(self):
        """
        Entrada: Ninguna.
        Salida: True si se reconocio como una instruccion, False si no son instrucciones validas
        Funcionalidad: Verifica si son instrucciones validas.
        """
        # Comentarios no se analizan

        # Verificar que sea una declaración para analizarla
        if(self.__verificar_palabra_clave("maceta") or self.__verificar_palabra_clave("semilla")):
            return True
        
        # Verificar qeu sea la plabra clave para retornar y asi analizarlo
        elif self.__verificar_estructura_datos("cosechar"):
            return True

        # Verificar que sea una funcion creada para analizarla
        elif self.__verificar_identificador():
            return True

        # Verificar qeu sea una función para analizarla
        elif self.__verificar_palabra_clave("sembrar"):
            return True

        # Verificar que sea un bucle para analizarlo
        elif (self.token_actual.tipo == TipoToken.REPETICION and self.token_actual.lexema == "fotosintesis") :
            return True

        # Verificar que sea una función condicional para analizarla
        elif self.__verificar_condicional("exterior"):
            return True

        # Verificar que sea a palabra clave para la función de imprimir y asi analizarla
        elif self.__verificar_palabra_clave("podar"):
            return True

        # Verificar que sea la palabra clave para el ciclo de casos para asi analizarlo
        elif self.__verificar_estructura_datos("planta"):
            return True

        else:
            return False

    def __analizar_declaracion(self):
        """
        Entrada: Ninguna.
        Salida: nodo_declaracion: Nodo con la declaración identificada.
        Funcionalidad: Analiza si la declaración esta bien escrita.

        Declaracion ::= TipoVar Identificador "=" Expresion
        TipoVar ::= "maceta" | "semilla"
        """
        if self.__verificar_palabra_clave("maceta") or self.__verificar_palabra_clave("semilla"):
            # Guardar el tipo de variable
            tipo_var = self.token_actual.lexema

            self.__siguiente_token()

            if self.__verificar_identificador():
                # Aalizar identificador y obtener su nodo
                nodo_identificador = self.__analizar_identificador()

                # Crear el nodo ASA para la declaración
                nodo_declaracion = NodoASA(tipo="Declaracion_" + tipo_var, contenido=nodo_identificador.contenido)

                if self.token_actual.tipo == TipoToken.ASIGNACION:
                    self.__siguiente_token()

                    if self.__verificar_expresion():

                        # Analizar la expresión y obtener su nodo ASA
                        nodo_expresion = self.__analizar_expresion()
                        
                        # Agregar identificador y expresion
                        nodo_declaracion.agregar_hijo(nodo_expresion)

                        return nodo_declaracion
                    else:
                        self.__error_detectado("Despues del '=' se espera una expresión válida")
                else:
                    self.__error_detectado("Después del identificador se espera un igual")
            else:
                self.__error_detectado("Se espera un idenrtificador después de 'maceta' o 'semilla'")
        else:
            self.__error_detectado("No se encontraron las palabras 'maceta' o 'semilla' al iniciar la declaración")

    def __analizar_funcion_creada(self):
        """
        Entrada: Ninguna.
        Salida: nodo_funcion_creada: Nodo con la infromación dela función creada
        Funcionalidad: Analiza la llamada de una función creada, para verificar que siga bien la granatica

        FuncionCreada :: = Identificador "(" ((ValorEstandar | Identificador) ( "," (ValorEstandar | Identificador))* )?")"
        """

        # Verifica si el token es un identificador
        if self.__verificar_identificador():
            nombre_funcion = self.token_actual.lexema
            self.__siguiente_token()

            # Crear el nodo de la función
            nodo_funcion_creada = NodoASA(tipo="Funcion_Creada", contenido=nombre_funcion)

            # Verificar si el token actual es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar que el token sea un valor estandar o un identificador
                if self.__verificar_valor_estandar() or self.__verificar_identificador():
                    #Crear el nodo de los parametros
                    nodo_parametros = NodoASA(tipo="Parametros", contenido="")

                    # Verificar que tipo de parametro es
                    if self.__verificar_identificador():
                        # Crear el nodo y añadirlo al nodo parametros}
                        nodo_identificador = self.__analizar_identificador()
                        nodo_parametros.agregar_hijo(nodo_identificador)
                    else:
                        nodo_valor_estandar = self.__analizar_valor_estandar()
                        nodo_parametros.agregar_hijo(nodo_valor_estandar)

                    # Mientras existan más parámetros se van a analizar
                    while self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar que el token sea un valor estandar o un identificador
                        if self.__verificar_valor_estandar() or self.__verificar_identificador():

                            # Verificar que tipo de parametro es
                            if self.__verificar_identificador():
                                # Crear el nodo y añadirlo al nodo parametros
                                nodo_identificador = self.__analizar_identificador()
                                nodo_parametros.agregar_hijo(nodo_identificador)
                            else:
                                nodo_valor_estandar = self.__analizar_valor_estandar()
                                nodo_parametros.agregar_hijo(nodo_valor_estandar)

                        else:
                            self.__error_detectado("Se esperaba un identificador, un string, un booleano, un entero o un flotante después de la coma")

                    # Crear nodo con parametros
                    nodo_funcion_creada = NodoASA(tipo="Funcion_Creada", contenido=nombre_funcion)
                    nodo_funcion_creada.agregar_hijo(nodo_parametros)

                # Verificar si el token actual es un paréntesis derecho
                if self.__verificar_puntuacion(")"):
                    self.__siguiente_token()

                    return nodo_funcion_creada
                else:
                    self.__error_detectado("Se esperaba un ')' después del '(' o los parámetros de la función")
            else:
                self.__error_detectado("Se esperaba un '(' después del identificador de la función0")
        else:
            self.__error_detectado("Se esperaba un identificador al iniciar la llamada de la función")

    def __analizar_retorno(self):
        """
        Entrada: Ninguna
        Salida: nodo_retorno: Nodo del retorno identificado
        Funcionalidad: Analiza si el retorno esta bien escrito.

        Retorno ::= "cosechar" (Expresion | Identificador)?
        """

        if self.__verificar_estructura_datos("cosechar"):
            self.__siguiente_token()

            # Crear el nodo para el retorno
            nodo_retorno = NodoASA(tipo="Retorno", contenido="cosechar")

            # Verificar si hay una expresión o un identificador después de "cosechar"
            if self.__verificar_expresion() or self.__verificar_identificador():
                if self.__verificar_identificador():
                    nodo_iden = self.__analizar_identificador()
                    nodo_retorno.agregar_hijo(nodo_iden)

                else:
                    nodo_expresion = self.__analizar_expresion()
                    nodo_retorno.agregar_hijo(nodo_expresion)

            return nodo_retorno

        else:
            self.__error_detectado("Para el retorno se espera la palabra clave 'cosechar'")

    def __analizar_funcion(self):
        """
        Entrada: Ninguna
        Salida: nodo_funcion: Nodo de la función identificada.
        Funcionalidad: Analiza si la función está bien escrita y construye el nodo ASA correspondiente.

        Funcion ::= "sembrar" Identificador "(" (Parametros)? ")" "{" Instrucciones+ "}" "florecer"
        """
        if self.__verificar_palabra_clave("sembrar"):
            self.__siguiente_token()

            # Verificar si el siguiente token es un identificador (nombre de la función)
            if self.__verificar_identificador():
                nodo_identificador = self.__analizar_identificador()

                # Crear el nodo para la función y agregar el identificador
                nodo_funcion = NodoASA(tipo="Funcion", contenido=nodo_identificador.contenido)

                # Verificar si el siguiente token es un paréntesis izquierdo
                if self.__verificar_puntuacion("("):
                    self.__siguiente_token()

                    if self.__verificar_identificador():
                        nodo_parametros = self.__analizar_parametros()
                        nodo_funcion.agregar_hijo(nodo_parametros)

                    # Verificar si el siguiente token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        # Verificar si el siguiente token es un corchete izquierdo
                        if self.__verificar_puntuacion("{"):
                            self.__siguiente_token()

                            # Verificar que existan al menos 1 instruccion
                            if self.__verificar_instrucciones():
                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                nodo_instruccion = self.__analizar_instrucciones()

                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Ciclo para verificar si hay mas instrucciones
                                while self.__verificar_instrucciones():
                                    nodo_instruccion = self.__analizar_instrucciones()
                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                nodo_funcion.agregar_hijo(nodo_instrucciones)

                                if self.__verificar_puntuacion("}"):
                                    self.__siguiente_token()

                                    # Verificar si el siguiente token es la palabra clave "florecer"
                                    if self.__verificar_palabra_clave("florecer"):
                                        self.__siguiente_token()

                                        return nodo_funcion
                                    else:
                                        self.__error_detectado("Se esperaba la palabrabra clave 'florecer' después del '}' al terminar la función")
                                else:
                                    self.__error_detectado("Se esperaba un '}' al finalizar las instrucciones de la función")
                            else:
                                self.__error_detectado("La función debe tener al menos una instruccion válida")
                        else:
                            self.__error_detectado("Se espera un '{' al iniciar las instrucciones de la función")
                    else:
                        self.__error_detectado("Se esperaba un ')' después del '(' o los parámetros de la función")
                else:
                    self.__error_detectado("Se esperaba un '(' después del identificador de la función")
            else:
                self.__error_detectado("Se esperaba un identificador después de la palabra clave 'sembrar'")
        else:
            self.__error_detectado("Al crear una función se espera la palabra clave 'sembrar'")

    def __analizar_parametros(self):
        """
        Entrada: Ninguna
        Salida: nodo_parametos: Nodo de los parametros encontrados.
        Analiza los parámetros de una función y los agrega al nodo padre.

        Parametros ::= Identificador | ("," Identificador)*
        """
        # Verificar si hay al menos un identificador como parámetro
        if self.__verificar_identificador():
            # Crear el nodo de los parametros
            nodo_parametros = NodoASA(tipo="Parametros", contenido="")

            # Analizar el identificador y añadir el nodo al nodo_parametros
            nodo_identificador = self.__analizar_identificador()
            nodo_parametros.agregar_hijo(nodo_identificador)

            # Mientras haya comas, seguir analizando más parámetros
            while self.__verificar_puntuacion(","):
                self.__siguiente_token()

                if self.__verificar_identificador():
                    # Analizar el identificador y añadir el nodo al nodo_parametros
                    nodo_identificador = self.__analizar_identificador()
                    nodo_parametros.agregar_hijo(nodo_identificador)

                else:
                    self.__error_detectado("Se esperaba un identificador después de la coma")

            return nodo_parametros

        else:
            self.__error_detectado("Se esperaba un identificador como parámetro")

    def __analizar_repeticion(self):
        """
        Entrada: Ninguna.
        Salida: nodo_repeticion: Nodo encontrado de la estructura de repeticion.
        Funcionalidad: Analiza si la repetición esta bien escrita.

        Repeticion ::= "fotosintesis" "(" Expresion ")" "{" Instrucciones+ "}"
        """
        # Verificar si el token actual es la palabra clave "fotosintesis"
        if (self.token_actual.tipo == TipoToken.REPETICION and self.token_actual.lexema == "fotosintesis") :
            self.__siguiente_token()

            # Crear el nodo para la repetición
            nodo_repeticion = NodoASA(tipo="Ciclo", contenido="fotositesis")

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token es una expresión
                if self.__verificar_expresion():
                    # Analizar la expresión
                    nodo_expresion = self.__analizar_expresion()
                    nodo_repeticion.agregar_hijo(nodo_expresion)

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        # Verificar si el token es un corchete izquierdo
                        if self.__verificar_puntuacion("{"):
                            self.__siguiente_token()

                            # Verificar que existan al menos 1 instruccion
                            if self.__verificar_instrucciones():
                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                nodo_instruccion = self.__analizar_instrucciones()

                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Ciclo para verificar si hay mas instrucciones
                                while self.__verificar_instrucciones():
                                    nodo_instruccion = self.__analizar_instrucciones()
                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                nodo_repeticion.agregar_hijo(nodo_instrucciones)

                                # Verificar si el siguiente token es un corchete derecho
                                if self.__verificar_puntuacion("}"):
                                    self.__siguiente_token()

                                    return nodo_repeticion
                                else:
                                    self.__error_detectado("Se esperaba un '}' al finalizar las instrucciones de la repetición")
                            else:
                                self.__error_detectado("La repeticón debe tener al menos 1 instruccion valida")
                        else:
                            self.__error_detectado("Se esperaba un '{' al iniciar las instrucciones de la repetición")
                    else:
                        self.__error_detectado("Se esperaba un ')' al finalizar la expresión de la repetición")
                else:
                    self.__error_detectado("Se esperaba una expresión dentro de los paréntesis de la repetición")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra 'fotosintesis'")
        else:
            self.__error_detectado("Al iniciar la repetición se espera la palabra clave 'fotosintesis'")

    def __analizar_condicional(self):
        """
        Entrada: Ninguna
        Salida: nodo_condicional: Nodo con la información del condicional.
        Funcionalidad: Analiza si el condicional esta bien escrito.

        Condicional ::= If Else?
        If ::= "exterior" "(" Expresion ")" "{" Instrucciones+ "}"
        Else ::= "interior" "{" Instrucciones+ "}"
        """
     # Verificar si el token actual es la palabra clave "exterior" (inicio del condicional)
        if self.__verificar_condicional("exterior"):

            # Crear el nodo de la condicional y despues el bloque si
            nodo_condicional = NodoASA(tipo="Condicional", contenido="if/else")
            nodo_if = NodoASA(tipo="Bloque_If", contenido="exterior")

            self.__siguiente_token()

            # Verificar si el siguiente token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Analizar la condición
                if self.__verificar_expresion():
                    nodo_expresion = self.__analizar_expresion()
                    nodo_if.agregar_hijo(nodo_expresion)

                    # Verificar si el siguiente token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        # Verificar si el siguiente token es un corchete izquierdo
                        if self.__verificar_puntuacion("{"):
                            self.__siguiente_token()

                            # Verificar que exista al menos 1 instruccion valida
                            if self.__verificar_instrucciones():
                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                nodo_instruccion = self.__analizar_instrucciones()

                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Ciclo para verificar si hay mas instrucciones
                                while self.__verificar_instrucciones():
                                    nodo_instruccion = self.__analizar_instrucciones()
                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                nodo_if.agregar_hijo(nodo_instrucciones)

                                # Verificar si el siguiente token es un corchete derecho
                                if self.__verificar_puntuacion("}"):
                                    # Agregar el nodo bloque_if al nodo condicional
                                    nodo_condicional.agregar_hijo(nodo_if)

                                    self.__siguiente_token()

                                    # Verificar si existe un bloque "Sino"
                                    if self.__verificar_condicional("interior"):
                                        self.__siguiente_token()

                                        # Crear nodo para el bloqeu "Sino"
                                        nodo_else = NodoASA(tipo="Bloque_Else", contenido="interior")

                                        if self.__verificar_puntuacion("{"):
                                            self.__siguiente_token()

                                            # Verifiar si existe al menos 1 instruccion valida
                                            if self.__verificar_instrucciones():
                                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                                nodo_instruccion = self.__analizar_instrucciones()

                                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                                # Ciclo para verificar si hay mas instrucciones
                                                while self.__verificar_instrucciones():
                                                    nodo_instruccion = self.__analizar_instrucciones()
                                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                                nodo_else.agregar_hijo(nodo_instrucciones)

                                                if self.__verificar_puntuacion("}"):
                                                    # Agregar el nodo del bloqeu else a el nodo condicional
                                                    nodo_condicional.agregar_hijo(nodo_else)

                                                    self.__siguiente_token()
                                                else:
                                                    self.__error_detectado("Se esperaba un '}' al finalizar el bloque 'interior'")
                                            else:
                                                self.__error_detectado("El bloque 'interior' debe contener al menos una instrcuccion valida")
                                        else:
                                            self.__error_detectado("Se esperaba un '{' despues de la palabra clave 'interior'")

                                    return nodo_condicional

                                else:
                                    self.__error_detectado("Se esperaba un '}' al finalizar el bloque 'exterior'")
                            else:
                                self.__error_detectado("El bloque 'exterior' debe contener al menos una instruccion válida")
                        else:
                            self.__error_detectado("Se esperaba un '{' al iniciar el bloque de instrucciones de 'exterior'")
                    else:
                        self.__error_detectado("Se esperaba un ')' al finalizar la condición para 'exterior'")
                else:
                    self.__error_detectado("Se esperaba una expresión válida dentro de los paréntesis del condicional")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra 'exterior")
        else:
            self.__error_detectado("Al iniciar el condicional se espera la palabra clave 'exterior'")

    def __analizar_expresion(self):
        """
        Entrada: Ninguna
        Salida: EL Nodo correspondiente a la expresión identificada.
        Funcionalidad: Analiza si la expresión esta bien escrita.

        Expresion ::= ExpresionLogica | Concatenacion |
        ExpresionAritmetica | ExpresionIgualdad | ExpresionComparacion |
        ExpresionNegacion | LlamadaFuncion | ValorEstandar
        """

        # Verificar que el token actual sea un operador logico
        if self.__verificar_operador_logico(self.token_actual.lexema):
            nodo_expresion_logica = self.__analizar_expresion_logica()

            return nodo_expresion_logica

        # Verificar que el token actual sea la palabra "conocarpus" que es para una concatenación
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "conocarpus"):
            nodo_cancatenacion = self.__analizar_concatenacion()

            return nodo_cancatenacion

        # Verificar que el token actual sea un operador aritmetico
        elif self.__verificar_operador_aritmetico(self.token_actual.lexema):
            nodo_expresion_aritmetica = self.__analizar_expresion_aritmetica()

            return nodo_expresion_aritmetica

        # Verificar que el token actual sea la palabra "cactus" (igualdad)
        elif (self.token_actual.tipo == TipoToken.COMPARADOR and self.token_actual.lexema == "cactus"):
            nodo_expresion_igualdad = self.__analizar_expresion_igualdad()

            return nodo_expresion_igualdad

        # Verificar que el token actual sea un comparador
        elif self.__verificar_comparador(self.token_actual.lexema):
            nodo_expresion_comparacion = self.__analizar_expresion_comparacion()

            return nodo_expresion_comparacion

        # Verificar que el token actual sea la palabra "acaro"
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "acaro"):
            nodo_expresion_negacion = self.__analizar_expresion_negacion()

            return nodo_expresion_negacion

        # Verificar que sea llama a una funcion
        elif self.__verificar_llamada_funcion():
            # Craer el nodo de la expresion de una llamada de una funcion
            nodo_llamada_funcion = self.__analizar_llamada_funcion()

            return nodo_llamada_funcion

        # Verificar que el token actual sea un valor estandar
        elif self.__verificar_valor_estandar():
            nodo_valor_estandar = self.__analizar_valor_estandar()

            return nodo_valor_estandar

        else:
            self.__error_detectado("Se esperaba una expresión válida")

    def __verificar_expresion(self):
        """
        Entrada: Ninguna.
        Salida: True si es una expresión, False si no lo es.
        Funcionalidad: Verifica si el token actual es algpun tipo expresión.
        """

        # Verificar que el token actual sea un operador logico
        if self.__verificar_operador_logico(self.token_actual.lexema):
            return True

        # Verificar que el token actual sea la palabra "conocarpus" que es oara una concatenación
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "conocarpus"):
            return True

        # Verificar que el token actual sea un operador aritmetico
        elif self.__verificar_operador_aritmetico(self.token_actual.lexema):
            return True

        # Verificar que el token actual sea la palabra "cactus"
        # que es para una expresión de igualdad
        elif (self.token_actual.tipo == TipoToken.COMPARADOR and self.token_actual.lexema == "cactus"):
            return True

        # Verificar que el token actual sea un comparador
        elif self.__verificar_comparador(self.token_actual.lexema):
            return True

        # Verificar que el token actual sea la palabra "acaro"
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "acaro"):
            return True

        # Verificar que sea llama a una funcion
        elif self.__verificar_llamada_funcion():
            return True

        # Verificar que el token actual sea un valor estandar
        elif self.__verificar_valor_estandar():
            return True
        else:
            return False

    # Devuelve que tipo de valor estandar es
    def __analizar_valor_estandar(self):
        """
        Entrada: Ninguna.
        Salida: nodo_valor_estandar: Nodo del valor estandar identificado.
        Funcionalidad: Analiza si el valor estandar es correcto.

        ValorEstandar::=  Entero | Flotante | String | ValorBooleano
        """

        valor = self.token_actual.lexema
        tipo = ""

        # Verificar si el token actual es un entero
        if self.__verificar_entero():
            tipo = "Entero"

        # Verificar si el token actual es un flotante
        elif self.__verificar_flotante():
            tipo = "Flotante"

        # Verificar si el token actual es un string
        elif self.__verificar_string():
            tipo = "String"

        # Verificar si el token actual es un valor booleano
        elif self.__verificar_valor_verdad():
            tipo = "Booleano"

        # Verificar si se identifico algun valor estandar
        if(tipo != ""):
            # Crear el nodo ASA
            nodo_valor_estandar = NodoASA(tipo=tipo, contenido=valor)
            self.__siguiente_token()

            return nodo_valor_estandar
        else:
            self.__error_detectado("Se esperaba un entero, flotante, string o booleano")

    def __verificar_valor_estandar(self):
        """
        Entrada: Ninguna.
        Salida: True si es un valor estandar, False si no lo es.
        Funcionalidad: Verifica si es un valor estandar.
        """
        # Verificar si el token actual es un entero
        if self.__verificar_entero():
            return True

        # Verificar si el token actual es un flotante
        elif self.__verificar_flotante():
            return True

        # Verificar si el token actual es un string
        elif self.__verificar_string():
            return True

        # Verificar si el token actual es un valor booleano
        elif self.__verificar_valor_verdad():
            return True
        else:
            return False

    def __analizar_llamada_funcion(self):
        """
        Entrada: Ninguna
        Salida: El nodo de la función de llamada identificada.
        Funcionalidad: Analiza si la llamada de una función esta bien escrita.

        LlamadaFuncion ::= Largo | Entrada | StringEntero | StringFlotante | (Identificador ("(" (ValorEstandar | Identificador) ( "," (ValorEstandar | Identificador))* ")")?)
        """

        # Verificar si el token actual es la palabra clave "medir"
        if self.__verificar_palabra_clave("medir"):
            return self.__analizar_largo()

        # Verificar si el token actual es la palabra clave "recolectar"
        elif self.__verificar_palabra_clave("recolectar"):
            return self.__analizar_entrada()

        # Verificar si el token actual es la palabra "madurar"
        elif self.__verificar_estructura_datos("madurar"):
            return self.__analizar_string_entero()

        # Verificar si el token actual es la palabra "germinar"
        elif self.__verificar_estructura_datos("germinar"):
            return self.__analizar_string_flotante()

        # Verifica si el token es un identificador
        elif self.__verificar_identificador():
            return self.__analizar_funcion_creada()
        
        else:
            self.__error_detectado("Se esperaba un identificador o alguna de las siguientes palabras claves: 'medir', 'recolectar', 'madurar' o 'germinar'")

    def __verificar_llamada_funcion(self):
        """
        Entrada: Ninguna.
        Salida: True si es una llamada de función, False si no lo es.
        Funcionalidad: Verifica si el token actual es una llamada de función.
        """

        # Verificar si el token actual es la palabra clave "medir"
        if self.__verificar_palabra_clave("medir"):
            return True

        # Verificar si el token actual es la palabra clave "recolectar"
        elif self.__verificar_palabra_clave("recolectar"):
            return True

        # Verificar si el token actual es la palabra "madurar"
        elif self.__verificar_estructura_datos("madurar"):
            return True

        # Verificar si el token actual es la palabra "germinar"
        elif self.__verificar_estructura_datos("germinar"):
            return True

        # Verifica si el token es un identificador
        elif self.__verificar_identificador():
            return True
        else:
            return False

    def __analizar_expresion_logica(self):
        """
        Entrada: Ninguna.
        Salida: nodo_expresion: El nodo de la exresion lógica identificada.
        Funcionalidad: Analiza si la expresión lógica esta bien escrita.

        ExpresiónLogica ::= OpLogico '(' ExpresionLogicaTerm (',' ExpresionLogicaTerm)+ ')'
        """

        # Verificar si el token actual es un operador lógico
        if self.__verificar_operador_logico(self.token_actual.lexema):
            operador = self.token_actual.lexema

            self.__siguiente_token()

            # Crear el nodo para la expresión lógica
            nodo_expresion = NodoASA(tipo="Expresion", contenido="")
            nodo_expresion_logica = NodoASA(tipo="Expresion_Logica", contenido=operador)

            # Verificar si el token actual es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token actual es una termino de expresion logica (si o si)
                if self.__verificar_expresion_logica_term():
                    # Crear el nodo del termino de la expresion logica
                    nodo_explog_term = self.__analizar_expresion_logica_term()
                    nodo_expresion_logica.agregar_hijo(nodo_explog_term)

                    # Verificar si el token actual es una coma (si o si)
                    if self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token actual es una termino de expresion logica (si o si)
                        if self.__verificar_expresion_logica_term():
                            nodo_explog_term = self.__analizar_expresion_logica_term()
                            nodo_expresion_logica.agregar_hijo(nodo_explog_term)

                            # Mientras existan más expresiones lógicas se van a analizar
                            # (si existen mas parametros, verificar que tengan la gramatica correcta)
                            while self.__verificar_puntuacion(","):
                                self.__siguiente_token()

                                # Verificar si el token actual es una termino de expresion logica
                                if self.__verificar_expresion_logica_term():
                                    nodo_explog_term = self.__analizar_expresion_logica_term()
                                    nodo_expresion_logica.agregar_hijo(nodo_explog_term)
                                else:
                                    self.__error_detectado("Se esperaba una expresión lógica después de la coma")

                            # Verificar si el token actual es un paréntesis derecho
                            if self.__verificar_puntuacion(")"):
                                nodo_expresion.agregar_hijo(nodo_expresion_logica)
                                self.__siguiente_token()

                                return nodo_expresion
                            else:
                                self.__error_detectado("Se esperaba un ')' al finalizar la expresión lógica")
                        else:
                            self.__error_detectado("Se esperaba una expresión lógica después de la coma")
                    else:
                        self.__error_detectado("Se esperaba una coma después de la expresión logica")
                else:
                    self.__error_detectado("Se esperaba una expresión lógica después del '('")
            else:
                self.__error_detectado("Se esperaba un '(' al iniciar la expresión lógica")
        else:
            self.__error_detectado("Se esperaba alguno de los operadores lógicos: 'injerto', 'dioica'")

    def __analizar_expresion_logica_term(self):
        """
        Entrada: Ninguna.
        Salida: nodo EL nodo de la expresión lógica identificada.
        Funcionalidad: Analiza si el termino de la expresión lógica esta bien escrito.

        ExpresionLogicaTerm ::= ExpresionComparacion | ExpresionIgualdad | ValorBooleano | ExpresionNegacion | ExpresionLogica | Identificador
        """
        # Verificar que el token actual sea un operador logico
        if self.__verificar_operador_logico(self.token_actual.lexema):
            return self.__analizar_expresion_logica()

        # Verificar que el token actual sea la palabra "cactus" que es para una expresión de igualdad
        elif (self.token_actual.tipo == TipoToken.COMPARADOR and self.token_actual.lexema == "cactus"):
            return self.__analizar_expresion_igualdad()

        # Verificar que el token actual sea un comparador
        elif self.__verificar_comparador(self.token_actual.lexema):
            return self.__analizar_expresion_comparacion()

        # Verificar que el token actual sea la palabra "acaro"
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "acaro"):
            return self.__analizar_expresion_negacion()

        # Verificar que el token actual sea un valor de verdad
        elif self.__verificar_valor_verdad():
            valor = self.token_actual.lexema
            nodo = NodoASA(tipo="Booleano", contenido=valor)

            self.__siguiente_token()

            return nodo

        # Verificar que sea un identificador
        elif self.__verificar_identificador():
            nodo = self.__analizar_identificador()

            return nodo
        
        else:
            self.__error_detectado("Se esperaba un valor valor booleano, un identificador o una expresión lógica de comparación, igualdad, negación u otra expresión lógica")

    # Verificar que sean terminos de expresion logica
    def __verificar_expresion_logica_term(self):
        """
        Entrada: Ninguna.
        Salida: True: si es un termino de una expresión lógica valido, False: si no es así.
        Funcionalidad: Verifica si es un termino de una expresión lógica
        """

        # Verificar que el token actual sea un operador logico
        if self.__verificar_operador_logico(self.token_actual.lexema):
            return True

        # Verificar que el token actual sea la palabra "cactus" que es para una expresión de igualdad
        elif (self.token_actual.tipo == TipoToken.COMPARADOR and self.token_actual.lexema == "cactus"):
            return True

        # Verificar que el token actual sea un comparador
        elif self.__verificar_comparador(self.token_actual.lexema):
            return True

        # Verificar que el token actual sea la palabra "acaro"
        elif (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "acaro"):
            return True

        # Verificar que el token actual sea un valor de verdad
        elif self.__verificar_valor_verdad():
            return True

        elif self.__verificar_identificador():
            return True
        else:
            return False

    def __analizar_expresion_comparacion(self):
        """
        Entrada: Ninguna.
        Salida: nodo_expresión: El nodo de la expresión de compración identificado.
        Funcionalidad: Analiza si la expresión de comparción esta bien escrita.

        ExpresionComparacion ::= OpComparacion '(' (ExpresionAritmeticaTerm) ',' (ExpresionAritmeticaTerm) ')'
        """

        # Verificar si el token actual es un operador de comparación
        if self.__verificar_comparador(self.token_actual.lexema):
            operador = self.token_actual.lexema

            self.__siguiente_token()

            # Crear el nodo para la expresion de comparación
            nodo_expresion = NodoASA(tipo="Expresion", contenido="")
            nodo_expresion_comparacion = NodoASA(tipo="Expresion_Comparacion", contenido=operador)

            # Verificar si el token actual es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token actual es una termino de expresion aritmetica (si o si)
                if self.__verificar_expresion_aritmetica_term():

                    # Si es una expresiona ritmetica entonce se analiza
                    nodo_expcomp_term = self.__analizar_expresion_aritmetica_term()
                    nodo_expresion_comparacion.agregar_hijo(nodo_expcomp_term)

                    # Verificar si el nodo es un es una expresion
                    # Si no es expresion se pasa al siguiente token
                    if not nodo_expcomp_term.tipo == "Expresion":
                        self.__siguiente_token()

                    # Verificar si el token actual es una coma (si o si)
                    if self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token actual es una termino de un termino de una expresion aritmetica (si o si)
                        if self.__verificar_expresion_aritmetica_term():
                            # Si es una expresiona ritmetica entonce se analiza
                            nodo_expcomp_term = self.__analizar_expresion_aritmetica_term()
                            nodo_expresion_comparacion.agregar_hijo(nodo_expcomp_term)

                            # Verificar si el nodo es un es una expresion
                            # Si no es expresion se pasa al siguiente token
                            if not nodo_expcomp_term.tipo == "Expresion":
                                self.__siguiente_token()

                            # Verificar si el token actual es un paréntesis derecho
                            if self.__verificar_puntuacion(")"):
                                nodo_expresion.agregar_hijo(nodo_expresion_comparacion)
                                self.__siguiente_token()

                                return nodo_expresion
                            else:
                                self.__error_detectado("Se esperaba un ')' al finalizar la expresión de comparación")
                        else:
                            self.__error_detectado("Se esperaba un termino expresion aritmetica o un identificador")
                    else:
                        self.__error_detectado("Se esperaba una coma después de la expresión aritmetica o un identificador")
                else:
                    self.__error_detectado("Se esperaba un termino de expresion aritmetica o un identificador")
            else:
                self.__error_detectado("Se esperaba un '(' después del operador de compración")
        else:
            self.__error_detectado("Se esperaba alguno de los siguientes operadores de comparación: 'secuoya', 'bonsai', 'rosa', 'lirio'")

    def __analizar_expresion_igualdad(self):
        """
        Entrada: Ninguna.
        Salida: nodo_expresion: El nodo de la expresión de compración identificada.
        Funcionalidad: Analiza si la expresión de igualdad esta bien escrita.

        ExpresionIgualdad ::= 'cactus' '(' (ExpresionAritmeticaTerm | ValorEstandar | Identificador) ',' (ExpresionAritmeticaTerm | ValorEstandar | Identificador) ')'
        """

        # Verificar si el token actual es el palabara "cactus"
        if (self.token_actual.tipo == TipoToken.COMPARADOR and self.token_actual.lexema == "cactus"):
            self.__siguiente_token()

            # Crear el nodo para la expresion de igualdad
            nodo_expresion = NodoASA(tipo="Expresion", contenido="")
            nodo_expresion_igualdad = NodoASA(tipo="Expresion_Igualdad", contenido="cactus")

            # Verificar si el token actual es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token actual es una termino de expresion aritmetica o un valor estandar(si o si)
                if (self.__verificar_expresion_aritmetica_term() or self.__verificar_valor_estandar()):

                    # Verifica si es un valor estandar o una expresion arimetica para crear el nodo correspondiente
                    if self.__verificar_valor_estandar():
                        nodo_expig_term = self.__analizar_valor_estandar()
                    else:
                        nodo_expig_term = self.__analizar_expresion_aritmetica_term()
                        
                         # Verificar si el nodo es un es una expresion
                        # Si no es expresion se pasa al siguiente token
                        if not nodo_expig_term.tipo == "Expresion":
                            self.__siguiente_token()

                    nodo_expresion_igualdad.agregar_hijo(nodo_expig_term)

                    # Verificar si el token actual es una coma (si o si)
                    if self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token actual es una termino de expresion aritmetica o un valor estandar(si o si)
                        if (self.__verificar_expresion_aritmetica_term() or self.__verificar_valor_estandar()):
                            
                            # Verifica si es un valor estandar o una expresion arimetica para crear el nodo correspondiente
                            if self.__verificar_valor_estandar():
                                nodo_expig_term = self.__analizar_valor_estandar()
                            else:
                                nodo_expig_term = self.__analizar_expresion_aritmetica_term()

                                # Verificar si el nodo es un es una expresion
                                # Si no es expresion se pasa al siguiente token
                                if not nodo_expig_term.tipo == "Expresion":
                                    self.__siguiente_token()

                            nodo_expresion_igualdad.agregar_hijo(nodo_expig_term)

                            # Verificar si el token actual es un paréntesis derecho
                            if self.__verificar_puntuacion(")"):
                                nodo_expresion.agregar_hijo(nodo_expresion_igualdad)
                                self.__siguiente_token()

                                return nodo_expresion
                            else:
                                self.__error_detectado("Se esperaba un ')' al finalizar la expresión de igualdad.")
                        else:
                            self.__error_detectado("Se esperaba una expresion aritmetica, un identificador, un entero, un string, un flotante o un booleano")
                    else:
                        self.__error_detectado("Se esperaba una coma después del termino de la expresión de comparación")
                else:
                    self.__error_detectado("Se esperaba una expresion aritmetica, un identificador, un entero, un string, un flotante o un booleano")
            else:
                self.__error_detectado("Se esperaba un '(' después del operador")
        else:
            self.__error_detectado("Se esperaba el operador 'cactus' para iniciar la igualdad")

    def __analizar_expresion_aritmetica(self):
        """
        Entrada: Ninguna
        Salida: nodo_expresion: El nodo de la expresión artmetica identificada.
        Funcionalidad: Analiza si la expresión aritmetica esta bien escrita.

        ExpresionAritmetica ::= OpAritmetico '(' ExpresionAritmeticaTerm (',' ExpresionAritmeticaTerm)+ ')'
        """

        # Verificar que sea un operador aritmetico
        if self.__verificar_operador_aritmetico(self.token_actual.lexema):
            operador = self.token_actual.lexema

            self.__siguiente_token()

            # Crear el nodo para la expresión aritmetica
            nodo_expresion = NodoASA(tipo="Expresion", contenido="")
            nodo_expresion_aritmetica = NodoASA(tipo="Expresion_Aritmetica", contenido=operador)

            # Verificar si el token actual es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token actual es una termino de expresion aritmetica (si o si)
                if self.__verificar_expresion_aritmetica_term():
                    nodo_expart_term = self.__analizar_expresion_aritmetica_term()
                    nodo_expresion_aritmetica.agregar_hijo(nodo_expart_term)

                    # Verificar si el nodo es un es una expresion
                    # Si no es expresion se pasa al siguiente token
                    if not nodo_expart_term.tipo == "Expresion":
                        self.__siguiente_token()

                    # Verificar si el token actual es una coma (si o si)
                    if self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token actual es una termino de expresion aritmetica (si o si)
                        if self.__verificar_expresion_aritmetica_term():
                            nodo_expart_term = self.__analizar_expresion_aritmetica_term()
                            nodo_expresion_aritmetica.agregar_hijo(nodo_expart_term)

                            if not nodo_expart_term.tipo == "Expresion":
                                self.__siguiente_token()

                            # Mientras existan más expresiones aritmeticas se van a analizar (si existen mas parametros, verificar que tengan la gramatica correcta)
                            while self.__verificar_puntuacion(","):
                                self.__siguiente_token()

                                # Verificar si el token actual es una termino de expresion logica
                                if self.__verificar_expresion_aritmetica_term():
                                    nodo_expart_term = self.__analizar_expresion_aritmetica_term()
                                    nodo_expresion_aritmetica.agregar_hijo(nodo_expart_term)

                                    if not nodo_expart_term.tipo == "Expresion":
                                        self.__siguiente_token()
                                else:
                                    self.__error_detectado("Se esperaba una expresión aritmetica, un entero, un flotante o un identificador después de la coma")

                            # Verificar si el token actual es un paréntesis derecho
                            if self.__verificar_puntuacion(")"):
                                nodo_expresion.agregar_hijo(nodo_expresion_aritmetica)
                                self.__siguiente_token()

                                return nodo_expresion
                            else:
                                self.__error_detectado("Se epseraba un ')' al finalizar la expresión aritmetica")
                        else:
                            self.__error_detectado("Se esperaba una expresión aritmetica, un entero, un flotante o un identificador después de la coma")
                    else:
                        self.__error_detectado("Se esperaba una coma después del termino de expresión aritmetica")
                else:
                    self.__error_detectado("Se esperaba una expresión aritmetica, un entero, un flotante o un identificador después de la coma")
            else:
                self.__error_detectado("Se esperaba un '(' después del operador aritmetico")
        else:
            self.__error_detectado("Se esperaba alguno de los siguientes operadores aritmeticos: 'sumatera', 'reseda', 'bambu', 'diosma', 'dalia', 'magnolia'")

    def __analizar_expresion_aritmetica_term(self):
        """
        Entrada: Ninguna.
        Salida: nodo: El nodo del termino identificado.
        Funcionalidad: Analiza si el termino de la expresión aritmetica esta bien escrito.

        ExpresionAritmeticaTerm ::= Entero | Flotante | Identificador | ExpresionAritmetica
        """

        # Verificar si es un entero
        if self.__verificar_entero():
            valor = self.token_actual.lexema
            nodo = NodoASA(tipo="Entero", contenido=valor)

            return nodo

        # Verrificar si es un flotante
        elif self.__verificar_flotante():
            valor = self.token_actual.lexema
            nodo = NodoASA(tipo="Flotante", contenido=valor)

            return nodo

        # Verificar si es un identificador
        elif self.__verificar_identificador():
            valor = self.token_actual.lexema
            nodo = NodoASA(tipo="Identificador", contenido=valor)

            return nodo

        # Verifica si es una expresión aritmetica
        elif self.__verificar_operador_aritmetico(self.token_actual.lexema):
            nodo_expresion_aritmetica = self.__analizar_expresion_aritmetica()

            return nodo_expresion_aritmetica

        # No es ninguno de los anteriores
        else:
            self.__error_detectado("Para una operación aritmetica se ocupa un entero, flotante, identificador o otra operación aritmetica.")

    def __verificar_expresion_aritmetica_term(self):
        """
        Entrada: Ninguna.
        Salida: True si es una expresión aritmética, False si no lo es.
        Funcionalidad: Verifica si el token actual es parte de una expresión aritmética.
        """

        # Verificar si es un entero
        if self.__verificar_entero():
            return True

        # Verrificar si es un flotante
        elif self.__verificar_flotante():
            return True

        # Verificar si es un identificador
        elif self.__verificar_identificador():
            return True

        # Verifica si es una expresión aritmetica
        elif self.__verificar_operador_aritmetico(self.token_actual):
            return True

        # No es ninguno de los anteriores
        else:
            return False

    # Analizar expresión negación
    def __analizar_expresion_negacion(self):
        """
        Entrada: Ninguna.
        Salida: nodo_expresion: El nodo de la expresion de negacion identificada.
        Funcionalidad: Analiza si la exprsion de negación esta bien escrita.

        ExpresionNegacion::= "acaro" ExpresionLogicaTerm
        """

        # Verificar que el token actual sea la palabra "acaro"
        if (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "acaro"):
            self.__siguiente_token()

            # Crear el nodo para la expresion de negacion
            nodo_expresion = NodoASA(tipo="Expresion", contenido="")
            nodo_expresion_negacion = NodoASA(tipo="Expresion_Negación", contenido="acaro")

            # Verifica que el siguiente token sea un termino de una expresión logica
            if self.__verificar_expresion_logica_term():
                nodo_expneg_term = self.__analizar_expresion_logica_term()
                nodo_expresion_negacion.agregar_hijo(nodo_expneg_term)
                nodo_expresion.agregar_hijo(nodo_expresion_negacion)

                return nodo_expresion
            else:
                self.__error_detectado("Se esperaba un valor booleano, un identificador, una expresión lógica, de negación, de comparación o de igualdad")
        else:
            self.__error_detectado("Se esperaba la palabara clave 'acaro' para iniciar la expresión de negación")

    # Analizar la expresión de cancatenación
    def __analizar_concatenacion(self):
        """
        Entrada: Ninguna
        Salida: nodo_concatencion: El nodo de la función de concatenación encontrada.
        Funcionalidad: Analiza si la concatenación esta bien escrita

        Concatenacion ::= “conocarpus” “(“ (String | Identificador) (“,” (String | Identificador))+ “)”
        """

        # Verificar que el token actual sea la palabra "cactus" que es para una concatenación
        if (self.token_actual.tipo == TipoToken.OPERADOR and self.token_actual.lexema == "conocarpus"):
            self.__siguiente_token()

            #Verificar que el token actual sea un parentesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Crear el nodo de la concatenacion
                nodo_concatenacion = NodoASA(tipo="Concatenacion", contenido="conocarpus")

                # Verificar si el token actual es un string oun identificador
                if (self.__verificar_string or self.__verificar_identificador):
                    valor = self.token_actual.lexema

                    # Verificar que tipo de contenido es
                    if self.__verificar_string():
                        nodo_term = NodoASA(tipo= "String", contenido=valor)
                        self.__siguiente_token()
                    else:
                        nodo_term = self.__analizar_identificador()

                    nodo_concatenacion.agregar_hijo(nodo_term)

                    # Verificar que el siguiente token sea una coma (si o si)
                    if self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token actual es un string oun identificador
                        if (self.__verificar_string or self.__verificar_identificador):
                            valor = self.token_actual.lexema

                            # Verificar que tipo de contenido es
                            if self.__verificar_string():
                                nodo_term = NodoASA(tipo= "String", contenido=valor)
                                self.__siguiente_token()
                            else:
                                nodo_term = self.__analizar_identificador()

                            nodo_concatenacion.agregar_hijo(nodo_term)

                            # Analizar strings o identificadores si todavia hay
                            while self.__verificar_puntuacion(","):
                                self.__siguiente_token()

                                if (self.__verificar_string or self.__verificar_identificador):
                                    valor = self.token_actual.lexema

                                    # Verificar que tipo de contenido es
                                    if self.__verificar_string():
                                        nodo_term = NodoASA(tipo= "String", contenido=valor)
                                        self.__siguiente_token()
                                    else:
                                        nodo_term = self.__analizar_identificador()

                                    nodo_concatenacion.agregar_hijo(nodo_term)

                                else:
                                    self.__error_detectado("Debe de haber un identificador o un string")
                            
                            #Verificar que el token actual sea un parentesis derecho
                            if self.__verificar_puntuacion(")"):
                                self.__siguiente_token()

                                return nodo_concatenacion
                            else:
                                self.__error_detectado("Dee haber un ')' al terminar de ingresar el identificador o el string")
                        else:
                            self.__error_detectado("Deberia haber minimo 2 paremetros, ya sea un string o identificador")
                    else:
                        self.__error_detectado("Después del identificador o el string debe haber una coma")
                else:
                    self.__error_detectado("Debe de haber un identificador o un string")
            else:
                self.__error_detectado("Debe de haber un '(' después de la palabra clave 'conocarpus'")
        else:
            self.__error_detectado("Para hacer una concatenación se debe empezar con la palabra clave 'conocarpus'")

    def __verificar_operador_logico(self, operador_logico):
        """
        Entrada: operador_logico: operador logico a verificar.
        Salida: True si es un operador logico, False si no lo es.
        Funcionalidad: Verifica si el token actual es un operador lógico.
        """

        # Verificar que el token actual sea un operador y que sea un operador logico
        if self.token_actual.tipo == TipoToken.OPERADOR and (operador_logico in ("injerto", "dioica")):
            return True

        return False

    # Verficar si es un operador aritmetico
    def __verificar_operador_aritmetico(self, operador_aritmetico):
        """
        Entrada: operador_aritmetico: operador aritmetico a verificar.
        Salida: True si es un operador aritmetico, False si no lo es.
        Funcionalidad: Verifica si el token actual es un operador aritmetico.
        """
        # Verificar que el token actual sea un operador aritmetico
        if self.token_actual.tipo == TipoToken.OPERADOR and not (operador_aritmetico in ("acaro", "conocarpus", "injerto", "dioica")):

            return True

        return False

    # Verificar si es un operador de comparacion
    def __verificar_comparador(self, comparador):
        """
        Entrada: comparador: comparador a verificar.
        Salida: True si es un comparador, False si no lo es.
        Funcionalidad: Verifica si el token actual es un operador de comparación.
        """

        # Verificar que el token actual sea un operador que no sea el de igualdad
        if self.token_actual.tipo == TipoToken.COMPARADOR and not (comparador in ("cactus")):
            return True

        return False

    def __verificar_valor_verdad(self):
        """
        Entrada: Ninguna.
        Salida: True si es un valor de verdad, False si no lo es.
        Funcionalidad: Verifica si el token actual es un valor de verdad.

        ValorBooleano ::= "Viva" | "Muerta"
        """

        # Verifica si el token actual es "viva" o "muerta"
        if (self.token_actual.tipo == TipoToken.VALOR_VERDAD and (self.token_actual.lexema in "viva", "muerta")):
            return True

        return False

    def __analizar_imprimir(self):
        """
        Entrada: Ninguna.
        Salida: nodo_imprimir: El nodo de lla función de imprimir identificado.
        Funcionalidad: Analiza si la función de imprimir esta bien escrita.

        Imprimir ::= "podar" "(" String | Identificador ("," (String | Identificador))* ")"
        """

        # Verificar si el token actual es la palabra clave "podar"
        if self.__verificar_palabra_clave("podar"):
            self.__siguiente_token()

            # Crear el nodo de la función de imprimir
            nodo_imprimir = NodoASA(tipo="Funcion_Imprimir", contenido="podar")

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token es un string o un identificador
                if self.__verificar_string() or self.__verificar_identificador():
                    valor = self.token_actual.lexema

                    # Verificar que tipo de contenido es
                    if self.__verificar_string():
                        nodo_termino = NodoASA(tipo="String", contenido=valor)
                        self.__siguiente_token()
                    else:
                        nodo_termino = self.__analizar_identificador()

                    nodo_imprimir.agregar_hijo(nodo_termino)

                    # Verifica si hay mas de un parametro para imprimir
                    while self.__verificar_puntuacion(","):
                        self.__siguiente_token()

                        # Verificar si el token es un string o un identificador
                        if self.__verificar_string() or self.__verificar_identificador():
                            valor = self.token_actual.lexema

                            # Verificar que tipo de contenido es
                            if self.__verificar_string():
                                nodo_termino = NodoASA(tipo="String", contenido=valor)
                                self.__siguiente_token()
                            else:
                                nodo_termino = self.__analizar_identificador()

                            nodo_imprimir.agregar_hijo(nodo_termino)

                        else:
                            self.__error_detectado("Se esperaba un string o un identificador después de la coma")

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        return nodo_imprimir
                    else:
                        self.__error_detectado("Se esperaba un ')' al finalizar la función de imprimir")
                else:
                    self.__error_detectado("Se esperaba un string o un identificador después '('")
            else:
                self.__error_detectado("Se esperaba un '(' despés de la palabra clave 'podar'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'podar' para iniciar la función de imprimir")

    def __analizar_largo(self):
        """
        Entrada: Ninguna.
        Salida: nodo_largo: El nodo de la función de largo encontrada.
        Funcionalidad: Analiza si la función de largo esta bien escrita.

        Largo ::= "medir" "(" (String | Identificador) ")"
        """

        # Verificar si el token actual es la palabra clave "medir"
        if self.__verificar_palabra_clave("medir"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Crear nodo de la función de largo
                nodo_largo = NodoASA(tipo="Funcion_Largo", contenido="medir")

                # Verificar si el token es un string o un identificador
                if self.__verificar_string() or self.__verificar_identificador():
                    valor = self.token_actual.lexema

                    # Identificar el tipo de valor
                    if self.__verificar_string():
                        nodo_termino = NodoASA(tipo="String", contenido=valor)
                        self.__siguiente_token()
                    else:
                        nodo_termino = self.__analizar_identificador()

                    nodo_largo.agregar_hijo(nodo_termino)

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        return nodo_largo

                    else:
                        self.__error_detectado("Se esperaba un ')' de el string o identificador")
                else:
                    self.__error_detectado("Se esperaba un string o un identificador después de '('")
            else:
                self.__error_detectado("Se esperaba un '(' después la palabra clave 'medir'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'medir' para iniciar la función de largo")

    def __analizar_entrada(self):
        """
        Entrada: Ninguna.
        Salida: nodo_entrada: El nodo de las función de entrada identificado.
        Funcionalidad: Analiza si la función de entrada esta bien escrita.

        Entrada ::= "recolectar" "(" String ")"
        """

        # Verificar si el token actual es la palabra clave "recolectar"
        if self.__verificar_palabra_clave("recolectar"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Crear nodo para la función de entrada
                nodo_entrada = NodoASA(tipo="Funcion_Entrada", contenido="recolectar")

                # Verificar si el token es un string
                if self.__verificar_string():
                    valor = self.token_actual.lexema
                    nodo_string = NodoASA(tipo="String", contenido=valor)

                    self.__siguiente_token()

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        nodo_entrada.agregar_hijo(nodo_string)
                        self.__siguiente_token()

                        return nodo_entrada

                    else:
                        self.__error_detectado("Se esperaba un ')' al finalizar la función de entrada")
                else:
                    self.__error_detectado("Se esperaba un string después de '('")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra clave 'recolectar'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'recolectar' para iniciar la función de entrada")

    # Analizar la función de string a entero
    def __analizar_string_entero(self):
        """
        Entrada: Ninguna.
        Salida: nodo_string_entero: El nodo de la función de atring a entero identificada.
        Funcionalidad: Analiza si la función de string a entero esta bien escrita.

        StringEntero ::= "madurar" "(" String | Entero | Identificador ")"
        """

        # Verificar si el token actual es la palabra clave "madurar"
        if self.__verificar_estructura_datos("madurar"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Crear el nodo de la funcion para pasar strings a enteros y viceversa
                nodo_string_entero = NodoASA(tipo="Funcion_String_Entero", contenido="madurar")
                
                # Verificar si el token es un string
                if self.__verificar_string() or self.__verificar_identificador() or self.__verificar_entero():
                    valor = self.token_actual.lexema

                    # Verificar que tipo de contenido es
                    if self.__verificar_string():
                        nodo_termino = NodoASA(tipo="String", contenido=valor)
                        self.__siguiente_token()
                    
                    elif self.__verificar_entero():
                        nodo_termino = NodoASA(tipo="Entero", contenido=valor)
                        self.__siguiente_token()

                    else:
                        nodo_termino = self.__analizar_identificador()

                    nodo_string_entero.agregar_hijo(nodo_termino)

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        return nodo_string_entero

                    self.__error_detectado("Se esperaba un ')' al finalizar la función de string a entero")
                else:
                    self.__error_detectado("Se esperaba un string después de '('")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra clave 'madurar'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'madurar' para iniciar la función de string a entero")

    # Analizar la función de string a flotante
    def __analizar_string_flotante(self):
        """
        Entrada: Ninguna
        Salida: nodo_string_flotante: El nodo de la función de string a flotante.
        Funcionalidad: Analiza si la función de string a flotante esta bien escrita.

        StringFlotante ::= "germinar" "(" (String | Flotante | Identificador) ")"
        """

        # Verificar si el token actual es la palabra clave "germinar"
        if self.__verificar_estructura_datos("germinar"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Crear el nodo de la funcion para pasar de string a flotante
                nodo_string_flotante = NodoASA(tipo="Funcion_String_Flotante", contenido="germinar")

                # Verificar si el token es un string o un identificador
                if self.__verificar_string() or self.__verificar_identificador() or self.__verificar_flotante():
                    valor = self.token_actual.lexema

                    # Verificar que tipo de contenido es
                    if self.__verificar_string():
                        nodo_termino = NodoASA(tipo="String", contenido=valor)
                        self.__siguiente_token()
                    
                    elif self.__verificar_flotante():
                        nodo_termino = NodoASA(tipo="Flotante", contenido=valor)
                        self.__siguiente_token()

                    else:
                        nodo_termino = self.__analizar_identificador()

                    nodo_string_flotante.agregar_hijo(nodo_termino)

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        return nodo_string_flotante

                    self.__error_detectado("Se esperaba un ')' al finalizar la función de string a flotante")
                else:
                    self.__error_detectado("Se esperaba un string o un identificador después del '('")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra clave 'germinar'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'germinar' para iniciar la función de string a flotante")

    def __analizar_ciclo_casos(self):
        """
        Entrada: Ninguna.
        Salida: nodo_ciclo_casos: El nodo de la estructura del ciclo de casos.
        Funcionalidad: Analiza si el ciclo de casos esta bien escrito.

        CicloCasos ::= "planta" "(" Expresion ")" "{" Instrucciones+ “flor” Identificador '=' Expresion Casos+ CasoDefault "}"
        """

        # Verificar si el token actual es la palabra "planta"
        if self.__verificar_estructura_datos("planta"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token es una expresión
                if self.__verificar_expresion():
                    # Analizar la expresión
                    nodo_expresion = self.__analizar_expresion()

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        # Crear nodo del ciclo de casos
                        nodo_ciclo_casos = NodoASA(tipo="Ciclo_Casos", contenido="planta")
                        nodo_ciclo_casos.agregar_hijo(nodo_expresion)

                        # Verificar si el token es un corchete izquierdo
                        if self.__verificar_puntuacion("{"):
                            self.__siguiente_token()

                            # Verificar si existen al menos una instruccion
                            if self.__verificar_instrucciones():
                                # Crear el nodo de instrucciones
                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                nodo_instruccion = self.__analizar_instrucciones()

                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Ciclo para verificar si hay mas instrucciones
                                while self.__verificar_instrucciones():
                                    nodo_instruccion = self.__analizar_instrucciones()
                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Añadir instrucciones al nodo del caso default
                                nodo_ciclo_casos.agregar_hijo(nodo_instrucciones)

                                # Verificar si el token es la palabra clave "Flor"
                                if self.__verificar_estructura_datos("flor"):
                                    self.__siguiente_token()

                                    # Verificar si el token es un identificador
                                    if self.__verificar_identificador():
                                        nodo = NodoASA(tipo="Opcion_Casos", contenido="flor")
                                        nodo_iden = self.__analizar_identificador()
                                        nodo.agregar_hijo(nodo_iden)

                                        # Veririficar qeu sea un signo de asignacion
                                        if self.token_actual.tipo == TipoToken.ASIGNACION:
                                            self.__siguiente_token()

                                            if self.__verificar_expresion():
                                                # Analizar la expresión y obtener su nodo ASA
                                                nodo_expresion = self.__analizar_expresion()
                                                nodo.agregar_hijo(nodo_expresion)

                                                nodo_ciclo_casos.agregar_hijo(nodo)

                                                # Crear el nodo de los casoso
                                                nodo_casos = NodoASA(tipo="Casos", contenido="")

                                                # Vrificar que exista al menso un ciclo de casos
                                                if self.__verificar_estructura_datos("hoja_compuesta"):
                                                    nodo_caso = self.__analizar_casos()
                                                    nodo_casos.agregar_hijo(nodo_caso)

                                                    while self.__verificar_estructura_datos("hoja_compuesta"):
                                                        nodo_caso = self.__analizar_casos()
                                                        nodo_casos.agregar_hijo(nodo_caso)

                                                    # Verificar si existe un caso por defecto
                                                    if self.__verificar_estructura_datos("hoja_simple"):
                                                        nodo_caso_default = self.__analizar_caso_default()
                                                        nodo_casos.agregar_hijo(nodo_caso_default)

                                                        # Verificar si el token es un corchete derecho
                                                        if self.__verificar_puntuacion("}"):
                                                            nodo_ciclo_casos.agregar_hijo(nodo_casos)

                                                            self.__siguiente_token()

                                                            return nodo_ciclo_casos
                                                        else:
                                                            self.__error_detectado("Se esperaba un '}' al finalizar el ciclo de casos")
                                                    else:
                                                        self.__error_detectado("Se esperaba la palabra clave 'hoja_simple para el caso default")
                                                else:
                                                    self.__error_detectado("Se esperaba la paralabar clave 'hoja_compuesta' para indicar los casos")
                                            else:
                                                self.__error_detectado("Despues del '=' se espera una expresión.")
                                        else:
                                            self.__error_detectado("Después del identificador se espero un '='")
                                    else:
                                        self.__error_detectado("Se esperaba un identificador después de la palabra clave 'flor'")
                                else:
                                    self.__error_detectado("Se esperaba la palabra clave 'flor' después de las instrucciones del ciclo de casos")
                            else:
                                self.__error_detectado("Se esperaban instrucciones para el caso")
                        else:
                            self.__error_detectado("Se esperaba un corchete izquierdo '{' para indicar las instrucción del ciclo de caso")
                    else:
                        self.__error_detectado("Se esperaba ')' despues de la expresión puesta")
                else:
                    self.__error_detectado("Se espera una expresión para el ciclo de casos como condicional")
            else:
                self.__error_detectado("Se esperaba '(' antes de la expresión")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'planta' para iniciar el ciclo de casos")

    def __analizar_casos(self):
        """
        Entrada: Ninguna.
        Salida: nodo_caso: El nodo de los casos encontrados.
        Funcionalidad: Analiza si los casos dentro del ciclo de casos están bien escritos.

        Casos ::= ("hoja_compuesta" "(" ValorEstandar ")" "{" Instrucciones+ "}")
        """

        # Verificar si el token actual sea la palabra "hoja_compuesta"
        if self.__verificar_estructura_datos("hoja_compuesta"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token es un string, entero, flotante o valor booleano
                if self.__verificar_valor_estandar():
                    nodo_valor_estandar = self.__analizar_valor_estandar()

                    # Verificar si el token es un paréntesis derecho
                    if self.__verificar_puntuacion(")"):
                        self.__siguiente_token()

                        # Crear nodo de los casos
                        nodo_caso = NodoASA(tipo="Caso",contenido="")
                        nodo_caso.agregar_hijo(nodo_valor_estandar)

                        # Verificar si el token es un corchete izquierdo
                        if self.__verificar_puntuacion("{"):
                            self.__siguiente_token()

                            # Verificar si existen al menos una instruccion
                            if self.__verificar_instrucciones():
                                # Crear el nodo de instrucciones
                                nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                                nodo_instruccion = self.__analizar_instrucciones()

                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Ciclo para verificar si hay mas instrucciones
                                while self.__verificar_instrucciones():
                                    nodo_instruccion = self.__analizar_instrucciones()
                                    nodo_instrucciones.agregar_hijo(nodo_instruccion)

                                # Añadir instrucciones al nodo del caso default
                                nodo_caso.agregar_hijo(nodo_instrucciones)

                                # Verificar si el token es un corchete derecho
                                if self.__verificar_puntuacion("}"):
                                    self.__siguiente_token()
                                    return nodo_caso
                                
                                else:
                                    self.__error_detectado("Se esperaba un '}' al finalizar las instrucciones del caso")
                            else:
                                self.__error_detectado("Se esperaban instrucciones para el caso")
                        else:
                            self.__error_detectado("Se esperaba un '{' al iniciar las instrucciones del caso")
                    else:
                        self.__error_detectado("Se esperaba un ')' al finalizar la expresión del caso")
                else:
                    self.__error_detectado("Se esperaba un string, entero, flotante o valor booleano después del '('")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra clave 'hoja_compuesta'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'hoja_compuesta' para iniciar el caso")

    def __analizar_caso_default(self):
        """
        Entrada: Ninguna.
        Salida: nodo_caso_default: El nodo del caso por defecto identificado.
        Funcionalidad: Analiza si el caso por defecto está bien escrito.

        CasoDefault ::= "hoja_simple" "(" ")" "{" Instrucciones+ "}"
        """

        # Verificar si el token actual es la palabra "hoja_simple"
        if self.__verificar_estructura_datos("hoja_simple"):
            self.__siguiente_token()

            # Verificar si el token es un paréntesis izquierdo
            if self.__verificar_puntuacion("("):
                self.__siguiente_token()

                # Verificar si el token es un paréntesis derecho
                if self.__verificar_puntuacion(")"):
                    self.__siguiente_token()

                    # Crear el nodo
                    nodo_caso_default = NodoASA(tipo="Caso_Default", contenido="hoja_simple")

                    # Verificar si el token es un corchete izquierdo
                    if self.__verificar_puntuacion("{"):
                        self.__siguiente_token()

                        # Verificar si existen al menos una instruccion
                        if self.__verificar_instrucciones():
                            # Crear el nodo de instrucciones
                            nodo_instrucciones = NodoASA(tipo="Instrucciones", contenido="")
                            nodo_instruccion = self.__analizar_instrucciones()

                            nodo_instrucciones.agregar_hijo(nodo_instruccion)

                            # Ciclo para verificar si hay mas instrucciones
                            while self.__verificar_instrucciones():
                                nodo_instruccion = self.__analizar_instrucciones()
                                nodo_instrucciones.agregar_hijo(nodo_instruccion)

                            # Añadir instrucciones al nodo del caso default
                            nodo_caso_default.agregar_hijo(nodo_instrucciones)

                            # Verificar si el token es un corchete derecho
                            if self.__verificar_puntuacion("}"):
                                self.__siguiente_token()
                                return nodo_caso_default
                            
                            else:
                                self.__error_detectado("Se esperaba un '}' al finalizar las instrucciones del caso por defecto")
                        else:
                            self.__error_detectado("Se esperaban instrucciones para el caso por defecto")
                    else:
                        self.__error_detectado("Se esperaba un '{' después del '('")
                else:
                    self.__error_detectado("Se esperaba un ')' después de '('")
            else:
                self.__error_detectado("Se esperaba un '(' después de la palabra clave 'hoja_simple'")
        else:
            self.__error_detectado("Se esperaba la palabra clave 'hoja_simple' para iniciar el caso por defecto")

    def __verificar_string(self):
        """
        Entrada: token: token a verificar.
        Salida: True si es un string, False si no lo es.
        Funcionalidad: Verifica si el token actual es un string/texto.

        String::= #.*?#
        """
        
        if self.token_actual.tipo == TipoToken.TEXTO:
            return True
        else:
            return False

    def __analizar_identificador(self):
        """
        Entrada: Ninguna.
        Salida: nodo_identificacion: NodoASA con el identificador
        Funcionalidad: Analiza si el identificador coincide con la gramatica
        
        Identificador :: = [a-zA-Z_][a-zA-Z0-9_]*
        """
        if self.token_actual.tipo == TipoToken.IDENTIFICADOR:
            nodo_identificador = NodoASA(tipo="Identificador", contenido=self.token_actual.lexema)
            self.__siguiente_token()

            return nodo_identificador

    def __verificar_identificador(self):
        """
        Entrada: token: token a verificar.
        Salida: True si es un entero, False si no lo es.
        Funcionalidad: Verifica si el token actual es un identificador.
        """

        if self.token_actual.tipo == TipoToken.IDENTIFICADOR:
            return True

        return False

    # Entero ::= r"[-+]?\d+"
    def __verificar_entero(self):
        """
        Entrada: token: token a verificar.
        Salida: True si es un entero, False si no lo es.
        Funcionalidad: Verifica si el token actual es un entero.
        """

        if self.token_actual.tipo == TipoToken.ENTERO:
            return True

        return False

    # Flotante ::= [-+]?\d+\.\d+
    def __verificar_flotante(self):
        """
        Entrada: token: token a verificar.
        Salida: True si es un entero, False si no lo es.
        Funcionalidad: Verifica si el token actual es un flotante.
        """
        
        if self.token_actual.tipo == TipoToken.FLOTANTE:
            return True

        return False

    def __verificar_puntuacion(self, puntuacion):
        """
        Entrada: token: token a verificar.
        Salida: True si es un signo de puntuación, False si no lo es.
        Funcionalidad: Verifica si el token actual es un signo de puntuación.

        [(){};,]
        """

        if (self.token_actual.tipo == TipoToken.PUNTUACION) and (puntuacion == self.token_actual.lexema):
            return True

        return False

    # Verificar que coincida la palabra clave con el texto dado
    def __verificar_palabra_clave(self, palabra_clave):
        """
        Entrada: palabra_clave: palabra clave a verificar.
        Salida: True si es una palabra clave, False si no lo es.
        Funcionalidad: Verifica si el token actual es una palabra clave.
        """

        if (self.token_actual.tipo == TipoToken.PALABRA_CLAVE) and (palabra_clave == self.token_actual.lexema):
            return True

        return False

    # Verifica que sea la palabra para el coindicional
    def __verificar_condicional(self, condicional):
        """
        Entrada: condicional: condicional a verificar.
        Salida: True si es una condicional, False si no lo es.
        Funcionalidad: Veridicar que sea un condicional y si coincide con la palabra clave dada.
        """

        if (self.token_actual.tipo == TipoToken.CONDICIONAL and condicional == self.token_actual.lexema):
            return True

        return False

    # Verificar que sea una estructura de datos y si coinicide con el texto dado
    def __verificar_estructura_datos(self, estructura_datos):
        """
        Entrada: estructura_datos: estructura de datos a verificar.
        Salida: True si es una estructura de datos, False si no lo es.
        Funcionalidad: Verifica si el token actual es una estructura de datos.
        """
        if (self.token_actual.tipo == TipoToken.ESTRUCTURA_DATOS) and (estructura_datos == self.token_actual.lexema):
            return True

        return False

    # Pasar al siguiente token
    def __siguiente_token(self):
        """
        Entrada: Ninguna.
        Salida: Ninguna.
        Funcionalidad: Pasa al siguiente token.
        """

        # Cambiar la posicion actual
        self.posicion_token_actual += 1

        # Verificar que no se haya llegado al final de la lista de tokens
        if not self.__verificar_final():
            # Si no se llegó, se cambia el token actual
            self.token_actual = self.tokens[self.posicion_token_actual]     

    # Verificar su se llego al final del programa
    def __verificar_final(self):
        """
        Entrada: Ninguna.
        Salida: True si se llegó al final, False si no se llegó.
        Funcionalidad: Verifica si se llegó al final del programa.
        """

        if self.posicion_token_actual < self.numero_tokens:
            return False

        return True

    def __error_detectado(self, mensaje):
        """
        Entrada: mensaje: mensaje de error.
        Salida: Ninguna.
        Funcionalidad: Guarda el mensaje de error.
        """

        self.errores.append((mensaje, self.token_actual.linea))
        self.__siguiente_token()

    def obtener_errores(self):
        """
        Entrada: None
        Salida: Lista de errores sintácticos
        Funcionalidad: Devuelve la lista de errores para ser usados fuera.
        """
        return self.errores

    def imprimir_asa(self):
        """
        Entrada: Ninguna
        Salida: Ninguna
        Funcionalidad: Imprimir el ASA asociado
        """

        self.asa.imprimir_asa()

    def imprimirErrores(self, path):
        """
        Obtiene los errores sintacticos que se hayan almacenado y los imprime

        :param path: La ruta del archivo .tc para formateo del error.
        :returns: -1 si hay errores, 0 si no hay.
        """
        errores_sintacticos = self.obtener_errores()

        if errores_sintacticos:
            imprimir_errores(errores_sintacticos, path, 2)
            return -1
        return 0