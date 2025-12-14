# 🌱 Proyecto TerraCode: Primera Entrega

## 🧠 Integrantes
- Jozafath Pérez Fernández - 2023107460
- Alana Calvo Bolaños - 2022040915
- Mary Paz Álvarez Navarrete - 2023138604
- José Gabriel Jiménez Chacón - 2021128841_

## 📚 Curso
IC5701 - Compiladores e Intérpretes  
Profesor: Aurelio Sanabria

---

## 🌻 Motivación

Decidimos crear TerraCode porque nos gusta mucho todo lo relacionado con la jardinería y el ambiente natural. Pensamos que sería interesante mezclar ese gusto con la programación, así que quisimos desarrollar un lenguaje que usará términos del mundo de las plantas, pero que también tuviera sentido en lo que hace un lenguaje de programación.

---

## 🪴 Características del Lenguaje TerraCode

- **Temática**: Jardinería y naturaleza.
- **Sintaxis amigable**: Palabras clave como `Semilla`, `Maceta`, `podar`, etc.
- **Funciones**: Definidas con `Sembrar`, llamadas con `Florecer`
- **Comentarios**: Inician con `#`
- **Entrada/Salida**: `riega` para imprimir, `cosecha` para finalizar ejecución

---

## 🔤 Gramática EBNF (Resumen Inicial)

```ebnf
Programa ::= Instrucciones

Instrucciones ::= Instruccion (Instruccion+es)*

Instruccion ::= Comentario | Declaracion | Asignacion | Funcion | Repeticion | Condicional | Imprimir | CicloCasos | Retorno

Comentario ::= "*" Texto "*"

Declaracion ::= TipoVar Identificador 
TipoVar ::= "Maceta" | "Semilla"

Retorno ::= "Cosechar" (Expresion)?

Asignacion ::= Identificador "=" Expresion

Funcion ::= "Sembrar" Identificador "(" ")" "{" Instrucciones "}" "Florecer"

Repeticion ::= "Fotosintesis" "(" Expresion ")" "{" Instrucciones "}" 

Condicional ::= If+ Else?
If ::= "Exterior" "(" Expresion ")" "{" Instrucciones "}" 
Else ::= "Interior" "{" Instrucciones "}" 
```