## Descripción
Este módulo se encuentra la implementación del explorador o analizador léxico de Terracode, encargado de escanear el código fuente y descomponerlo en tokens válidos según la gramática del lenguaje. El explorador no solo identifica elementos como palabras clave, operadores, identificadores, operadores, texto, etc, sino que también detecta y reporta errores cuando encuentra símbolos o secuencias inválidas. Para garantizar su correcto funcionamiento, se incluyen pruebas que verifican tanto el reconocimiento preciso de tokens válidos como el manejo adecuado de errores en distintos casos.

El proceso de análisis léxico sigue un flujo estructurado: primero, el lexer recorre el código carácter por carácter, agrupando secuencias válidas (como números, cadenas o identificadores) y asignándoles un tipo de token específico. Si encuentra un símbolo no reconocido (como @ o # en un contexto inválido), genera un error indicando su ubicación (línea) para facilitar la corrección. Por ejemplo, ante la entrada nombre = #Petunia#;, el explorador produciría los tokens IDENTIFICADOR(nombre) y TEXTO(#Petunia#), mientras que para @nombre, mostraría un error como "Error léxico: Símbolo no reconocido '@' en línea 5".

Las pruebas del módulo cubren diversos escenarios, incluyendo tokens válidos, casos bordes (como cadenas sin cerrar o números mal formados) y símbolos ambiguos. Estas pruebas aseguran que el explorador no solo reconozca correctamente la sintaxis válida, sino que también se verifique que se estos faciles de arreglar.

## Descripción de Archivos

### 📄 Archivos Principales

1. **tokens.py**  
   Define la clase `Token`, que representa cada elemento léxico reconocido (tipo, lexema, línea).

2. **errores.py**  
   Implementa la función `imprimir_error`, que muestra errores léxicos con detalles de ubicación (línea).

3. **explorador.py**  
   Contiene la clase `Scanner` (analizador léxico), con las siguientes funcionalidades:
   - Inicialización de tokens y símbolos válidos.
   - Análisis línea por línea del código.
   - Identificación de tokens y errores.
   - Métodos para imprimir resultados (`imprimir_tokens`, `obtener_errores`).

4. **main.py**  
   Punto de entrada para pruebas:
   - Carga archivos de prueba (`prueba1.txt` o `prueba2.txt`).
   - Ejecuta el scanner y muestra los resultados en terminal, siendo estos tokens reconocidos o errores encontrados.


## Explicación de la logica del codigo (General)
Inicialmente en el archivo Main.py se busca el archivo a analizar para cargar todas las lineas de texto que contenga en un string, esto para instanciar un objeto scanner el cual separará cada una de las lineas, además, por cada linea de texto se va verificando si cada patrón que tengan los tipos de tokens especificados hacen match con algún lexema en la linea;
si hace match se guardan para luego ser impresos en consola con la información relacionada y en caso contrario se recorta el string o se guarda la información del error.

Por último se hacen la impresión de los tokens encontrados, al final se especifican los errores encontrados que no concuerdan con alguno de los patrones de los tipos de tokens definidos.
