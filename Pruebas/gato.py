
# Variables para cada uno de los campos, movimientos y el turno
bienvenida = "\n\n****************************** Bienvenid@ al juego de 3 en raya para probar el transpilador ******************************\n"
indicacion = "*************** INFORMACION: para digitar en una casilla, escriba el valor FilaColumna en su turno.\n"
A1 = " "
A2 = " "
A3 = " "
B1 = " "
B2 = " "
B3 = " "
C1 = " "
C2 = " "
C3 = " "
jugador1 = ""
jugador2 = ""
turno = "X"
movimientos = 0

def mostrar_tablero():
    """
    Esta funcion imprime el tablero.
    """
    print(f"""
    1   2   3
  -------------
A | {A1} | {A2} | {A3} |
  -------------
B | {B1} | {B2} | {B3} |
  -------------
C | {C1} | {C2} | {C3} |
  -------------
""")

def verificarGanador():
    """
    Esta funcion verifica si hay un ganador, en todas las posibles combinaciones\n
    Retorna True si hay ganador, en caso contrario False.
    """
    if (A1 == A2) and (A2 == A3) and (A3 != " "):
        return True
    if (B1 == B2) and (B2 == B3) and (B3 != " "):
        return True
    if (C1 == C2) and (C2 == C3) and (C3 != " "):
        return True
    if (A1 == B1) and (B1 == C1) and (C1 != " "):
        return True
    if (A2 == B2) and (B2 == C2) and (C2 != " "):
        return True
    if (A3 == B3) and (B3 == C3) and (C3 != " "):
        return True
    if (A1 == B2) and (B2 == C3) and (C3 != " "):
        return True
    if (A3 == B2) and (B2 == C1) and (C1 != " "):
        return True
    return False

def cambiar_turno():
    """
    Cambia el signo a usar en el siguiente turno.
    """
    global turno
    if turno == "X":
        turno = "O"
    else:
        turno = "X"

def asignar_casilla(nombre):
    """
    Asigna el simbolo segun corresponda al turno,\n
    en la casilla indicada.
    """
    global A1, A2, A3, B1, B2, B3, C1, C2, C3
    
    if nombre == "A1" and A1 == " ":
        A1 = turno
        return True
    elif nombre == "A2" and A2 == " ":
        A2 = turno
        return True
    elif nombre == "A3" and A3 == " ":
        A3 = turno
        return True
    elif nombre == "B1" and B1 == " ":
        B1 = turno
        return True
    elif nombre == "B2" and B2 == " ":
        B2 = turno
        return True
    elif nombre == "B3" and B3 == " ":
        B3 = turno
        return True
    elif nombre == "C1" and C1 == " ":
        C1 = turno
        return True
    elif nombre == "C2" and C2 == " ":
        C2 = turno
        return True
    elif nombre == "C3" and C3 == " ":
        C3 = turno
        return True
    else:
        print("Casilla inválida o ya ocupada.")
        return False

#----------- Ejercucion del programa -----------
print(bienvenida)
print(indicacion)
jugador1 = input("Digite el nombre del primer jugador, este usara la X: ")
jugador2 = input("Digite el nombre del segundo jugador, este usara el O: ")

while True:
    mostrar_tablero()
    jugada = input(f"Turno de {turno}.\nEscriba la casilla: ").upper()
    if asignar_casilla(jugada):
        movimientos += 1
        ganador = verificarGanador()

        #Si hay ganador, impime la info
        if ganador:
            mostrar_tablero()
            if turno == "X":
                print(f"¡ Felicidades, gano {jugador1}!")
            else:
                print(f"¡ Felicidades, gano {jugador2}!")
            break
        elif movimientos == 9:
            mostrar_tablero()
            print("¡Lo sentimos, hubo un empate!")
            break
        
        #Si no hay ganador, cambia el turno
        cambiar_turno()
