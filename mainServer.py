import socket, os, pickle, threading, random
from operator import itemgetter 

### Variables para el manejo de salas y conexiones de clientes
HOST = 'localhost'
PORT = 50001
ROOMS = {}
ROOMScon = {}
startGame = {}
ROOMpiles = {}
ROOMamountDefuses = {}
ROOMpilesPlayers = {}
ROOMSturnPlayers = {}
ROOMSpreviousTurnPlayers = {}
ROOMSpostTurnPlayers = {}
ROOMSplayersAlive = {}
giveCard = {}
toGiveCard = {}

### Variables para el manejo de una partida en una sala
CARDNO = 1
CARDATACK = 2
CARDSKIP = 3
CARDFAVOR = 4
CARDSHUFFLE = 5
CARDSEEFUTURE = 6
CARDDEFUSE = 7
CARDBOMB = 8
CARDGATOBARBA = 9
CARDGATOARCOIRIS = 10
CARDGATOSANDIA = 11
CARDGATOTACO = 12
CARDGATOPAPA = 13

### Funciones para la creacion, manejor y control de ROOMS
## Crea el thread cuando se quiere hacer una sala
def thread_function1(port):
    banner = 0
    RPORT = port
    #print(RPORT)
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.bind((HOST, RPORT))
    print('starting to listen in Room', RPORT)
    ROOMScon[port] = list()
    ROOMSplayersAlive[port] = list()
    ROOMpilesPlayers[port] = {}
    startGame[port] = False
    giveCard[port] = False
    toGiveCard[port] = False
    ROOMpiles[port] = [
        1,1,1,1,1,
        2,2,2,2,
        3,3,3,3,
        4,4,4,4,
        5,5,5,5,
        6,6,6,6,6,
        9,9,9,9,
        10,10,10,10,
        11,11,11,11,
        12,12,12,12,
        13,13,13,13    
    ]
    ROOMamountDefuses[port] = 6
    ROOMSturnPlayers[port] = list()
    ROOMSpreviousTurnPlayers[port] = list()
    ROOMSpostTurnPlayers[port] = list()
    r.listen(5)
    roomThreads = list()
    while (ROOMS[RPORT] < 5):
        #print("In room loop")
        roomCon, temp = r.accept()
        username = "User "+str(ROOMS[RPORT])
        ROOMScon[RPORT].append(roomCon)
        ROOMSplayersAlive[RPORT].append(roomCon)
        ROOMS[RPORT] = ROOMS[RPORT] + 1
        ROOMpilesPlayers[RPORT][roomCon] = []
        print ('Connected by ', temp, ' on room', RPORT)
        print(ROOMS)
        thread_client = threading.Thread(target = game, args=[roomCon,RPORT,username])
        thread_client.start()
        roomThreads.append(thread_client)

def game(cli_sock, port, username):
    global startGame
    while True:
        ### Sala de espera al juego
        responseP = cli_sock.recv(4096)
        print(username, " has sent a message")
        objeto = pickle.loads(responseP)

        ### Se lee el encabezado que viene como parte principal del prootocolo para definir como
        ### se leeran los siguientes parametros que se definieron como parte del protocolo
        opcionJuego = objeto['opcion']

        ### La opcion 1 es para poder iniciar la partida, dado que se debe de poder avisar
        ### a los demas jugadores que la partida esta lista cuando ya hay al menos 3 jugadores
        if opcionJuego == 1:
            if cli_sock in ROOMSplayersAlive[port]:
                if startGame[port] == False:
                    ### Se revisa que haya al menos 3 jugadores para poder empezar la partida
                    if ROOMS[port] > 2 and ROOMS[port] < 6:
                        ### Se hace un set de los elementos del juego
                        ### Se revuelve el mazo
                        random.shuffle(ROOMpiles[port])
                        random.shuffle(ROOMpiles[port])
                        random.shuffle(ROOMpiles[port])
                        counter = 9
                        ### Se le da un defuse a cada jugador
                        for player in ROOMScon[port]:
                            ROOMpilesPlayers[port][player].append(7)
                            ROOMamountDefuses[port] = ROOMamountDefuses[port] - 1
                        
                            ### Se reparten 7 cartas a cada jugador

                            for k in range(7):
                                pilaTemporal = ROOMpiles[port]
                                ROOMpilesPlayers[port][player].append(counter)
                                ROOMpiles[port] = pilaTemporal
                            counter = counter + 1

                        ### Se agregan los defuses y bombas al mazo
                        random.shuffle(ROOMpiles[port])
                        random.shuffle(ROOMpiles[port])
                        random.shuffle(ROOMpiles[port])

                        counterBombs = 0
                        for player in ROOMScon[port]:
                            if counterBombs < len(ROOMScon[port]) - 1:
                                ### Se agrega una bomba y se revuelve
                                ROOMpiles[port].append(8)
                                random.shuffle(ROOMpiles[port])
                            counterBombs = counterBombs + 1
                            
                        for j in range(ROOMamountDefuses[port]):
                            ### Se agrega una bomba y se revuelve
                            ROOMpiles[port].append(7)
                            random.shuffle(ROOMpiles[port])

                        ### Hay que revolver bien las cartas :)
                        random.shuffle(ROOMpiles[port])

                        ### Se notifica al resto de jugadores que inicio el juego
                        mensajeInicio = {
                            'header' : 'inicio'
                        }
                        startGame[port] = True
                        mensajeInicioP = pickle.dumps(mensajeInicio)
                        for client in ROOMScon[port]:
                            client.send(mensajeInicioP)

                        ### Luego se notifica el player que va de primero
                        ROOMSturnPlayers[port].append(0)
                        mensajeTurno = {
                            'header' : 'turno',
                            'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                        }
                        mensajeTurnoP = pickle.dumps(mensajeTurno)
                        for client in ROOMScon[port]:
                            client.send(mensajeTurnoP) 

                    ### En caso no haya suficientes jugadores, entonces se manda un mensaje de error
                    ### a todos los clientes
                    else:
                        mensajeInicio = {
                            'header' : 'fallo',
                            'mensaje' : '\nEl juego ha tratado de ser iniciado pero no hay suficientes jugadores aun.'
                        }
                        mensajeInicioP = pickle.dumps(mensajeInicio)
                        for client in ROOMScon[port]:
                            client.send(mensajeInicioP)
                ### En caso se quiera iniciar el juego cuando ya se ha iniciado entonces se manda un mensaje
                ### al cliente para avisarle que la partida ya esta en curso
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego ya fue iniciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP)
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)
        ### La opcion 2 es para poder utilizar el Chat (Broadcast) para poder mandar mensajes con el resto de
        ### jugadores
        elif opcionJuego == 2:
            ### Solo se pueden mandar mensajes cuando la partida ha iniciado
            if startGame[port] == True:
                broadcast_usr(username, cli_sock, objeto, port)
            ### Si no se ha iniciado mandamos un mensaje de error al cliente para indicarle que la partida
            ### aun no ha iniciado
            else:
                mensajeInicio = {
                    'header' : 'fallo',
                    'mensaje' : '\nEl juego aun no ha sido iniciado.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)        

        ### La opcion 3 es para poder realizar una jugada cuando es el turno del cliente
        elif opcionJuego == 3:
            if cli_sock in ROOMSplayersAlive[port]:
                ### Solo se pueden hacer jugadas cuando la partida ha iniciado            
                if startGame[port] == True:
                    if giveCard[port] == False:
                        if cli_sock == ROOMScon[port][ROOMSturnPlayers[port][0]]:
                            print("Jugando tu turno")
                            ### Usar una carta
                            if objeto['jugada'] == 1:
                                cartaPosicion = objeto['carta']
                                if cartaPosicion < len(ROOMpilesPlayers[port][cli_sock]) and cartaPosicion > -1:
                                    cartaJugada = ROOMpilesPlayers[port][cli_sock].pop(cartaPosicion)
                                    if cartaJugada == CARDNO:
                                        if ROOMSpreviousTurnPlayers[port]:
                                            mensajeTurno = {
                                                'header' : 'usoCarta',
                                                'mensaje' : '\nEl jugador uso la carta NO.'
                                            }
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)
                                            for client in ROOMScon[port]:
                                                client.send(mensajeTurnoP) 

                                            ROOMSturnPlayers[port][0] = ROOMSpreviousTurnPlayers[port][0]
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)
                                            for client in ROOMScon[port]:
                                                client.send(mensajeTurnoP) 
                                            ### Al poner un NO se quitan los ATACK y SKIP y no se podra hacer NO al NO
                                            ROOMSpreviousTurnPlayers[port] = []
                                            ROOMSpostTurnPlayers[port] = []
                                        else:
                                            ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                            mensajeInicio = {
                                                'header' : 'fallo',
                                                'mensaje' : '\nNo es posible jugar una carta NO en tu turno.'
                                            }
                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                            cli_sock.send(mensajeInicioP)   
                                    elif cartaJugada == CARDATACK:
                                        ROOMSpreviousTurnPlayers[port] = []
                                        ROOMSpostTurnPlayers[port] = []
                                        ROOMSpreviousTurnPlayers[port].append(ROOMScon[port].index(cli_sock))

                                        ### Buscar quien es el siguiente
                                        ### Se avisa de quien es el siguiente turno
                                        ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                        ### Revisamos si el jugar siguiente esta en la lista de vivos
                                        if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                            ROOMSturnPlayers[port][0] = 0

                                        for jugador in range(len(ROOMScon[port])):
                                            if ROOMScon[port][ROOMSturnPlayers[port][0]] not in ROOMSplayersAlive[port]:
                                                ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                                ### Revisamos si el jugar siguiente esta en la lista de vivos
                                                if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                    ROOMSturnPlayers[port][0] = 0
                                                
                                            else:
                                                ROOMSpostTurnPlayers[port].append(ROOMSturnPlayers[port][0])
                                                break 
                                            
                                        ### Notificamos quien es el proximo en jugar
                                        mensajeTurno = {
                                            'header' : 'turno',
                                            'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                        }
                                        mensajeTurnoP = pickle.dumps(mensajeTurno)
                                        for client in ROOMScon[port]:
                                            client.send(mensajeTurnoP) 

                                    elif cartaJugada == CARDSKIP:
                                        ROOMSpreviousTurnPlayers[port] = [ROOMScon[port].index(cli_sock)]
                                        mensajeTurno = {
                                            'header' : 'usoCarta',
                                            'mensaje' : '\nEl jugador uso la carta SKIP.'
                                        }
                                        mensajeTurnoP = pickle.dumps(mensajeTurno)
                                        for client in ROOMScon[port]:
                                            client.send(mensajeTurnoP) 

                                        mensajeTurnoP = ''
                                        ### Se revisa si el jugador debe repetir turno
                                        if ROOMSpostTurnPlayers[port]:
                                            ROOMSturnPlayers[port] = [ROOMScon[port].index(cli_sock)]
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)

                                            ### Al terminar un turno normal se quita el previous y el post TURN
                                            ROOMSpostTurnPlayers[port] = []
                                        else:
                                            ### Se avisa de quien es el siguiente turno
                                            ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                            ### Revisamos si el jugar siguiente esta en la lista de vivos
                                            if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                ROOMSturnPlayers[port][0] = 0

                                            for jugador in range(len(ROOMScon[port])):
                                                if ROOMScon[port][ROOMSturnPlayers[port][0]] not in ROOMSplayersAlive[port]:
                                                    ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                                    ### Revisamos si el jugar siguiente esta en la lista de vivos
                                                    if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                        ROOMSturnPlayers[port][0] = 0
                                                    
                                                else:
                                                    break 
                                                
                                            ### Notificamos quien es el proximo en jugar
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            ### Al terminar un turno normal se quita el previous y el post TURN
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)
                                            ROOMSpostTurnPlayers[port] = []

                                        for client in ROOMScon[port]:
                                            client.send(mensajeTurnoP)

                                    elif cartaJugada == CARDFAVOR:
                                        indexUsuario = objeto['favor']
                                        if indexUsuario > -1 and indexUsuario < len(ROOMScon[port]):
                                            clientePedir = ROOMScon[port][indexUsuario]
                                            if clientePedir in ROOMSplayersAlive[port]:
                                                toGiveCard[port] = cli_sock
                                                giveCard[port] = clientePedir
                                                mensajeTurno = {
                                                    'header' : 'usoCarta',
                                                    'mensaje' : '\nEl jugador uso la carta FAVOR al User '+ str(indexUsuario)
                                                }
                                                mensajeTurnoP = pickle.dumps(mensajeTurno)
                                                for client in ROOMScon[port]:
                                                    client.send(mensajeTurnoP) 
                                            else:
                                                mensajeInicio = {
                                                    'header' : 'fallo',
                                                    'mensaje' : '\nEl usuario al que le pediste ya no esta jugando.'
                                                }
                                                mensajeInicioP = pickle.dumps(mensajeInicio)
                                                cli_sock.send(mensajeInicioP) 
                                        else:
                                            mensajeInicio = {
                                                'header' : 'fallo',
                                                'mensaje' : '\nOpcion no valida de usuario a pedir carta, repita.'
                                            }
                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                            cli_sock.send(mensajeInicioP)   

                                    elif cartaJugada == CARDSHUFFLE:
                                        random.shuffle(ROOMpiles[port])
                                        mensajeTurno = {
                                            'header' : 'usoCarta',
                                            'mensaje' : '\nEl jugador uso la carta SHUFFLE.'
                                        }
                                        mensajeTurnoP = pickle.dumps(mensajeTurno)
                                        for client in ROOMScon[port]:
                                            client.send(mensajeTurnoP) 

                                    elif cartaJugada == CARDSEEFUTURE:
                                        mensaje = ''
                                        contador = 0
                                        primeraCarta = ''
                                        segundaCarta = ''
                                        terceraCarta = ''

                                        if len(ROOMpiles[port]) >= 3:
                                            primeraCarta = ROOMpiles[port].pop()
                                            segundaCarta = ROOMpiles[port].pop()
                                            terceraCarta = ROOMpiles[port].pop()
                                        elif len(ROOMpiles[port]) == 2:
                                            primeraCarta = ROOMpiles[port].pop()
                                            segundaCarta = ROOMpiles[port].pop()
                                        elif len(ROOMpiles[port]) == 1:
                                            primeraCarta = ROOMpiles[port].pop()

                                        if primeraCarta == CARDNO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta NO'
                                            contador = contador + 1
                                        elif primeraCarta == CARDATACK:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta ATACK'
                                            contador = contador + 1
                                        elif primeraCarta == CARDSKIP:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SKIP'
                                            contador = contador + 1
                                        elif primeraCarta == CARDFAVOR:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta FAVOR'
                                            contador = contador + 1
                                        elif primeraCarta == CARDSHUFFLE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SHUFFLE'
                                            contador = contador + 1
                                        elif primeraCarta == CARDSEEFUTURE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SEE THE FUTURE'
                                            contador = contador + 1
                                        elif primeraCarta == CARDDEFUSE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta DEFUSE'
                                            contador = contador + 1
                                        elif primeraCarta == CARDGATOBARBA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO BARBA'
                                            contador = contador + 1
                                        elif primeraCarta == CARDGATOARCOIRIS:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO ARCOIRIS'
                                            contador = contador + 1
                                        elif primeraCarta == CARDGATOSANDIA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO SANDIA'
                                            contador = contador + 1
                                        elif primeraCarta == CARDGATOTACO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO TACO'
                                            contador = contador + 1
                                        elif primeraCarta == CARDGATOPAPA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO PAPA'
                                            contador = contador + 1
                                        elif primeraCarta == CARDBOMB:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta BOMBA'
                                            contador = contador + 1
                                        else:
                                            contador = contador + 1

                                        if segundaCarta == CARDNO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta NO'
                                            contador = contador + 1
                                        elif segundaCarta == CARDATACK:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta ATACK'
                                            contador = contador + 1
                                        elif segundaCarta == CARDSKIP:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SKIP'
                                            contador = contador + 1
                                        elif segundaCarta == CARDFAVOR:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta FAVOR'
                                            contador = contador + 1
                                        elif segundaCarta == CARDSHUFFLE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SHUFFLE'
                                            contador = contador + 1
                                        elif segundaCarta == CARDSEEFUTURE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SEE THE FUTURE'
                                            contador = contador + 1
                                        elif segundaCarta == CARDDEFUSE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta DEFUSE'
                                            contador = contador + 1
                                        elif segundaCarta == CARDGATOBARBA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO BARBA'
                                            contador = contador + 1
                                        elif segundaCarta == CARDGATOARCOIRIS:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO ARCOIRIS'
                                            contador = contador + 1
                                        elif segundaCarta == CARDGATOSANDIA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO SANDIA'
                                            contador = contador + 1
                                        elif segundaCarta == CARDGATOTACO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO TACO'
                                            contador = contador + 1
                                        elif segundaCarta == CARDGATOPAPA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO PAPA'
                                            contador = contador + 1
                                        elif segundaCarta == CARDBOMB:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta BOMBA'
                                            contador = contador + 1
                                        else:
                                            contador = contador + 1

                                        if terceraCarta == CARDNO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta NO'
                                            contador = contador + 1
                                        elif terceraCarta == CARDATACK:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta ATACK'
                                            contador = contador + 1
                                        elif terceraCarta == CARDSKIP:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SKIP'
                                            contador = contador + 1
                                        elif terceraCarta == CARDFAVOR:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta FAVOR'
                                            contador = contador + 1
                                        elif terceraCarta == CARDSHUFFLE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SHUFFLE'
                                            contador = contador + 1
                                        elif terceraCarta == CARDSEEFUTURE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta SEE THE FUTURE'
                                            contador = contador + 1
                                        elif terceraCarta == CARDDEFUSE:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta DEFUSE'
                                            contador = contador + 1
                                        elif terceraCarta == CARDGATOBARBA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO BARBA'
                                            contador = contador + 1
                                        elif terceraCarta == CARDGATOARCOIRIS:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO ARCOIRIS'
                                            contador = contador + 1
                                        elif terceraCarta == CARDGATOSANDIA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO SANDIA'
                                            contador = contador + 1
                                        elif terceraCarta == CARDGATOTACO:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO TACO'
                                            contador = contador + 1
                                        elif terceraCarta == CARDGATOPAPA:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO PAPA'
                                            contador = contador + 1
                                        elif terceraCarta == CARDBOMB:
                                            mensaje = mensaje + '\n' + str(contador) + '. Carta BOMBA'
                                            contador = contador + 1
                                        else:
                                            contador = contador + 1
                                        
                                        if terceraCarta != '':
                                            ROOMpiles[port].append(terceraCarta)
                                        if segundaCarta != '':
                                            ROOMpiles[port].append(segundaCarta)
                                        if primeraCarta != '':
                                            ROOMpiles[port].append(primeraCarta)

                                        mensajeInicio = {
                                            'header' : 'futuro',
                                            'mensaje' : '\nLas cartas son: \n' + mensaje + '.'
                                        }
                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                        cli_sock.send(mensajeInicioP)

                                    elif cartaJugada == CARDDEFUSE:
                                        ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                        mensajeInicio = {
                                            'header' : 'fallo',
                                            'mensaje' : '\nNo es posible jugar una carta DEFUSE en tu turno.'
                                        }
                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                        cli_sock.send(mensajeInicioP)

                                    else:
                                        indexUsuario = objeto['favor']
                                        if indexUsuario > -1 and indexUsuario < len(ROOMScon[port]):
                                            clientePedir = ROOMScon[port][indexUsuario]
                                            if clientePedir in ROOMSplayersAlive[port]:
                                                opcionCantidadGatos = objeto['gatos']
                                                if opcionCantidadGatos == 1:
                                                    if ROOMpilesPlayers[port][cli_sock].count(cartaJugada) >= 1:
                                                        ### Revisamos si el indice que mando para robar
                                                        cartaPedir = objeto['cartaPedir'] - 1
                                                        if cartaPedir > -1 and cartaPedir < len(ROOMpilesPlayers[port][clientePedir]):
                                                            ROOMpilesPlayers[port][cli_sock].remove(cartaJugada)
                                                            cartaQuitar = ROOMpilesPlayers[port][clientePedir][cartaPedir]
                                                            ROOMpilesPlayers[port][clientePedir].remove(cartaQuitar)
                                                            ROOMpilesPlayers[port][cli_sock].append(cartaQuitar)
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nRobaste la carta exitosamente.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            cli_sock.send(mensajeInicioP) 
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nTe robaron una carta.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            clientePedir.send(mensajeInicioP)
                                                        else:
                                                            ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nEl indice de la carta no es correcto, repita.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            cli_sock.send(mensajeInicioP) 
                                                    else:
                                                        ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                                        mensajeInicio = {
                                                            'header' : 'fallo',
                                                            'mensaje' : '\nNo tienes la cantidad de gatos iguales suficiente, repite.'
                                                        }
                                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                                        cli_sock.send(mensajeInicioP)       
                                                elif opcionCantidadGatos == 2:
                                                    if ROOMpilesPlayers[port][cli_sock].count(cartaJugada) >= 2:
                                                        ROOMpilesPlayers[port][cli_sock].remove(cartaJugada)
                                                        ROOMpilesPlayers[port][cli_sock].remove(cartaJugada)
                                                        ### Revisamos la carta que quiere robar
                                                        cartaPedir = objeto['cartaPedir']
                                                        if cartaPedir > 7:
                                                            cartaPedir = cartaPedir + 1
                                                        if cartaPedir in ROOMpilesPlayers[port][clientePedir]:
                                                            ROOMpilesPlayers[port][clientePedir].remove(cartaPedir)
                                                            ROOMpilesPlayers[port][cli_sock].append(cartaPedir)
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nRobaste la carta exitosamente.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            cli_sock.send(mensajeInicioP) 
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nTe robaron una carta.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            clientePedir.send(mensajeInicioP) 
                                                        else:
                                                            mensajeInicio = {
                                                                'header' : 'fallo',
                                                                'mensaje' : '\nEl jugador no tenia la carta que pediste, y perdiste tus cartas.'
                                                            }
                                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                                            cli_sock.send(mensajeInicioP)   
                                                    else:
                                                        ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                                        mensajeInicio = {
                                                            'header' : 'fallo',
                                                            'mensaje' : '\nNo tienes la cantidad de gatos iguales suficiente, repite.'
                                                        }
                                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                                        cli_sock.send(mensajeInicioP)         
                                                else:
                                                    ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                                    mensajeInicio = {
                                                        'header' : 'fallo',
                                                        'mensaje' : '\nNo elegiste una opcion correcta para cuantos gatos usar, repite.'
                                                    }
                                                    mensajeInicioP = pickle.dumps(mensajeInicio)
                                                    cli_sock.send(mensajeInicioP) 
                                            else:
                                                ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                                mensajeInicio = {
                                                    'header' : 'fallo',
                                                    'mensaje' : '\nEl usuario al que le pediste ya no esta jugando.'
                                                }
                                                mensajeInicioP = pickle.dumps(mensajeInicio)
                                                cli_sock.send(mensajeInicioP) 
                                        else:
                                            ROOMpilesPlayers[port][cli_sock].append(cartaJugada)
                                            mensajeInicio = {
                                                'header' : 'fallo',
                                                'mensaje' : '\nOpcion no valida de usuario a pedir carta, repita.'
                                            }
                                            mensajeInicioP = pickle.dumps(mensajeInicio)
                                            cli_sock.send(mensajeInicioP)

                                else: 
                                    mensajeInicio = {
                                        'header' : 'fallo',
                                        'mensaje' : '\nOpcion no valida de carta, repita.'
                                    }
                                    mensajeInicioP = pickle.dumps(mensajeInicio)
                                    cli_sock.send(mensajeInicioP)    
                            ### Tomar una carta
                            elif objeto['jugada'] == 2:
                                ### Sacar la carta
                                cartaNueva = ROOMpiles[port].pop()
                                ### Revisar si es bomba o no
                                if cartaNueva != 8:
                                    ### Agregar la carta al mazo del jugador
                                    ROOMpilesPlayers[port][cli_sock].append(cartaNueva)
                                    mensajeInicio = {
                                        'header' : 'response',
                                        'mensaje' : '\nTermino tu turno.'
                                    }
                                    mensajeInicioP = pickle.dumps(mensajeInicio)
                                    cli_sock.send(mensajeInicioP)
                                    mensajeTurnoP = ''
                                    ### Se revisa si el jugador debe repetir turno
                                    if ROOMSpostTurnPlayers[port]:
                                        ### Se aplica el turno nuevamente
                                        ROOMSturnPlayers[port] = [ROOMScon[port].index(cli_sock)]
                                        mensajeTurno = {
                                            'header' : 'turno',
                                            'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                        }
                                        ### Al terminar un turno normal se quita el previous y el post TURN
                                        ROOMSpreviousTurnPlayers[port] = []
                                        ROOMSpostTurnPlayers[port] = []
                                    else:
                                        ### Se avisa de quien es el siguiente turno
                                        ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                        ### Revisamos si el jugar siguiente esta en la lista de vivos
                                        if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                            ROOMSturnPlayers[port][0] = 0

                                        for jugador in range(len(ROOMScon[port])):
                                            if ROOMScon[port][ROOMSturnPlayers[port][0]] not in ROOMSplayersAlive[port]:
                                                ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                                ### Revisamos si el jugar siguiente esta en la lista de vivos
                                                if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                    ROOMSturnPlayers[port][0] = 0
                                                
                                            else:
                                                break 
                                            
                                        ### Notificamos quien es el proximo en jugar
                                        mensajeTurno = {
                                            'header' : 'turno',
                                            'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                        }
                                        ### Al terminar un turno normal se quita el previous y el post TURN
                                        ROOMSpreviousTurnPlayers[port] = []
                                        ROOMSpostTurnPlayers[port] = []

                                    mensajeTurnoP = pickle.dumps(mensajeTurno)
                                    for client in ROOMScon[port]:
                                        client.send(mensajeTurnoP)         
                                else:
                                    ### Revisar si tiene defuse
                                    if CARDDEFUSE in ROOMpilesPlayers[port][cli_sock]:
                                        ### Se le quita un Defuse
                                        ROOMpilesPlayers[port][cli_sock].remove(CARDDEFUSE)
                                        ROOMpiles[port].append(cartaNueva)
                                        random.shuffle(ROOMpiles[port])
                                        ### Mensaje terminar turno
                                        mensajeInicio = {
                                            'header' : 'response',
                                            'mensaje' : '\nTe salio bomba pero tenias Defuse\nTermino tu turno.'
                                        }
                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                        cli_sock.send(mensajeInicioP)  

                                        mensajeTurnoP = ''
                                        ### Se revisa si el jugador debe repetir turno
                                        if ROOMSpostTurnPlayers[port]:
                                            ROOMSturnPlayers[port] = [ROOMScon[port].index(cli_sock)]
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            ### Al terminar un turno normal se quita el previous y el post TURN
                                            ROOMSpreviousTurnPlayers[port] = []
                                            ROOMSpostTurnPlayers[port] = []
                                        else:
                                            ### Se avisa de quien es el siguiente turno
                                            ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                            ### Revisamos si el jugar siguiente esta en la lista de vivos
                                            if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                ROOMSturnPlayers[port][0] = 0

                                            for jugador in range(len(ROOMScon[port])):
                                                if ROOMScon[port][ROOMSturnPlayers[port][0]] not in ROOMSplayersAlive[port]:
                                                    ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                                    ### Revisamos si el jugar siguiente esta en la lista de vivos
                                                    if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                        ROOMSturnPlayers[port][0] = 0
                                                    
                                                else:
                                                    break 
                                                
                                            ### Notificamos quien es el proximo en jugar
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            ### Al terminar un turno normal se quita el previous y el post TURN
                                            ROOMSpreviousTurnPlayers[port] = []
                                            ROOMSpostTurnPlayers[port] = []

                                        mensajeTurnoP = pickle.dumps(mensajeTurno)
                                        for client in ROOMScon[port]:
                                            client.send(mensajeTurnoP) 

                                    else:
                                        ### El jugador esta fuera
                                        ROOMSplayersAlive[port].remove(cli_sock)

                                        ### Se le avisa a todos que ya esta afuera
                                        mensajeInicio = {
                                            'header' : 'fuera',
                                            'mensaje' : '\nEl ' + str(username) + ' ha sido eliminado.\n'
                                        }
                                        mensajeInicioP = pickle.dumps(mensajeInicio)
                                        for client in ROOMScon[port]:
                                            client.send(mensajeInicioP) 

                                        ### Si habia un atack o skip se quitan
                                        ROOMSpreviousTurnPlayers[port] = []
                                        ROOMSpostTurnPlayers[port] = []

                                        ### Se avisa de quien es el siguiente turno
                                        ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                        ### Revisamos si el jugar siguiente esta en la lista de vivos
                                        if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                            ROOMSturnPlayers[port][0] = 0

                                        for jugador in range(len(ROOMScon[port])):
                                            if ROOMScon[port][ROOMSturnPlayers[port][0]] not in ROOMSplayersAlive[port]:
                                                ROOMSturnPlayers[port][0] = ROOMSturnPlayers[port][0] + 1
                                                ### Revisamos si el jugar siguiente esta en la lista de vivos
                                                if ROOMSturnPlayers[port][0] >= len(ROOMScon[port]):
                                                    ROOMSturnPlayers[port][0] = 0
                                                
                                            else:
                                                break

                                        ### Se revisa si solo hay un jugador para terminar la partida
                                        if len(ROOMSplayersAlive[port]) == 1:
                                            ### Notificamoso quien es el proximo en jugar
                                            mensajeTurno = {
                                                'header' : 'ganar',
                                                'mensaje' : '\nEl ganador es el User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)
                                            for client in ROOMScon[port]:
                                                client.send(mensajeTurnoP)  
                                        ### En caso que no, entonces se notifica el turno del siguiente
                                        else:
                                            ### Notificamoso quien es el proximo en jugar
                                            mensajeTurno = {
                                                'header' : 'turno',
                                                'mensaje' : '\nEs el turno del User ' + str(ROOMSturnPlayers[port][0])+'.'
                                            }
                                            mensajeTurnoP = pickle.dumps(mensajeTurno)
                                            for client in ROOMScon[port]:
                                                client.send(mensajeTurnoP)

                            else:
                                mensajeInicio = {
                                    'header' : 'fallo',
                                    'mensaje' : '\nOpcion no valida, repita.'
                                }
                                mensajeInicioP = pickle.dumps(mensajeInicio)
                                cli_sock.send(mensajeInicioP)              
                        else:
                            mensajeInicio = {
                                'header' : 'fallo',
                                'mensaje' : '\nNo es tu turno.'
                            }
                            mensajeInicioP = pickle.dumps(mensajeInicio)
                            cli_sock.send(mensajeInicioP)  
                    else:
                        mensajeInicio = {
                            'header' : 'fallo',
                            'mensaje' : '\nEn este momento no puedes hacer jugadas porque un jugador debe hacer un favor.'
                        }
                        mensajeInicioP = pickle.dumps(mensajeInicio)
                        cli_sock.send(mensajeInicioP)  

                ### Si no se ha iniciado mandamos un mensaje de error al cliente para indicarle que la partida
                ### aun no ha iniciado
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego aun no ha sido iniciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP)    
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)

        ### La opcion 4 es para poder dar una carta en caso el jugador este obligado a dar un favor
        elif opcionJuego == 4:
            if cli_sock in ROOMSplayersAlive[port]:
                ### Solo se pueden hacer jugadas cuando la partida ha iniciado            
                if startGame[port] == True:
                    if giveCard[port] != False:
                        if giveCard[port] == cli_sock:
                            numeroCarta = objeto['carta']
                            if numeroCarta > -1 or numeroCarta <= len(ROOMpilesPlayers[port][cli_sock]):
                                carta = ROOMpilesPlayers[port][cli_sock].pop(numeroCarta)
                                ROOMpilesPlayers[port][toGiveCard[port]].append(carta)
                                toGiveCard[port] = False
                                giveCard[port] = False
                            else:
                                mensajeInicio = {
                                    'header' : 'fallo',
                                    'mensaje' : '\nEl numero de carta no coincide con ninguna de las que tienes.'
                                }
                                mensajeInicioP = pickle.dumps(mensajeInicio)
                                cli_sock.send(mensajeInicioP)                
                        else:
                            mensajeInicio = {
                                'header' : 'fallo',
                                'mensaje' : '\nNo eres el jugador elegido para hacer el favor.'
                            }
                            mensajeInicioP = pickle.dumps(mensajeInicio)
                            cli_sock.send(mensajeInicioP)        
                    else:
                        mensajeInicio = {
                            'header' : 'fallo',
                            'mensaje' : '\nNo han pedido un favor en esta ronda.'
                        }
                        mensajeInicioP = pickle.dumps(mensajeInicio)
                        cli_sock.send(mensajeInicioP) 
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego aun no ha sido iniciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP)
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)
 
        ### La opcion 5 es para poder ver las cantidades de cartas en los mazos del juego
        elif opcionJuego == 5:
            if cli_sock in ROOMSplayersAlive[port]:
                ### Solo se pueden hacer jugadas cuando la partida ha iniciado            
                if startGame[port] == True:
                    mensaje = ''
                    contador = 0
                    for jugador in ROOMScon[port]:
                        mensaje = mensaje + '\nCantidad de cartas del User ' + str(contador) + ': ' + str(len(ROOMpilesPlayers[port][jugador]))
                        contador = contador + 1
                    mensaje = mensaje + '\nCantidad de cartas en el Mazo: ' + str(len(ROOMpiles[port]))
                    mensajeEstado = {
                        'header' : 'estado',
                        'mensaje' : '\nEstado del juego: '+mensaje+'\n'
                    }
                    mensajeEstadoP = pickle.dumps(mensajeEstado)
                    cli_sock.send(mensajeEstadoP)
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego aun no ha sido iniciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP)
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)
 
        ### La opcion 6 es para poder ver las cartas que tiene el jugador
        elif opcionJuego == 6:
            if cli_sock in ROOMSplayersAlive[port]:
                ### Solo se pueden hacer jugadas cuando la partida ha iniciado            
                if startGame[port] == True:
                    mensaje = ''
                    contador = 0
                    for carta in ROOMpilesPlayers[port][cli_sock]:
                        if carta == CARDNO:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta NO'
                            contador = contador + 1
                        elif carta == CARDATACK:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta ATACK'
                            contador = contador + 1
                        elif carta == CARDSKIP:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta SKIP'
                            contador = contador + 1
                        elif carta == CARDFAVOR:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta FAVOR'
                            contador = contador + 1
                        elif carta == CARDSHUFFLE:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta SHUFFLE'
                            contador = contador + 1
                        elif carta == CARDSEEFUTURE:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta SEE THE FUTURE'
                            contador = contador + 1
                        elif carta == CARDDEFUSE:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta DEFUSE'
                            contador = contador + 1
                        elif carta == CARDGATOBARBA:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO BARBA'
                            contador = contador + 1
                        elif carta == CARDGATOARCOIRIS:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO ARCOIRIS'
                            contador = contador + 1
                        elif carta == CARDGATOSANDIA:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO SANDIA'
                            contador = contador + 1
                        elif carta == CARDGATOTACO:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO TACO'
                            contador = contador + 1
                        elif carta == CARDGATOPAPA:
                            mensaje = mensaje + '\n' + str(contador) + '. Carta GATO PAPA'
                            contador = contador + 1
                    mensajeEstadoPropio = {
                        'header' : 'estadoPropio',
                        'mensaje' : '\nTus cartas son: '+mensaje+'\n'
                    }
                    mensajeEstadoPropioP = pickle.dumps(mensajeEstadoPropio)
                    cli_sock.send(mensajeEstadoPropioP)
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego aun no ha sido iniciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP) 
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)

        ### La opcion 7 es para poder ver la lista de jugadores
        elif opcionJuego == 7:
            if cli_sock in ROOMSplayersAlive[port]:
                ### Solo se pueden hacer jugadas cuando la partida ha iniciado            
                if startGame[port] == True:
                    mensaje = ''
                    contador = 0
                    for jugador in ROOMScon[port]:
                        mensaje = mensaje + '\n' + str(contador) + '. User ' + str(contador)
                        contador = contador + 1
                    mensajeEstadoPropio = {
                        'header' : 'listaJugadores',
                        'mensaje' : '\nLos jugadores son: '+mensaje+'\n'
                    }
                    mensajeEstadoPropioP = pickle.dumps(mensajeEstadoPropio)
                    cli_sock.send(mensajeEstadoPropioP)
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego aun no ha sido inciado.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    cli_sock.send(mensajeInicioP) 
            ### Estas fuera del juego
            else:
                mensajeInicio = {
                    'header' : 'fuera',
                    'mensaje' : '\nPerdiste, ya no puedes hacer acciones.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)

def broadcast_usr(uname, cli_sock, objeto, port):
    try:
        data = objeto['mensaje']
        if data:
            print("{0} mando un mensaje".format(uname))
            b_usr(cli_sock, uname, data, port)
    except Exception as x:
        print(x.message)

def b_usr(cs_sock, sen_name, msg, port):
    for client in ROOMScon[port]:
        if client != cs_sock:
            objeto = { 
                'header' : 'chat',
                'nombre' : sen_name,
                'mensaje' : msg
            }
            client.send(pickle.dumps(objeto))

### Se solicita que se ingresen los parametros de IP y PORT del servidor
#HOST = input("Bienvenido a Exploding Kittens Server\nIngrese la IP del host: ")
#PORT = int(input("\nIngrese el puerto del Server: "))
c = PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
threads = list()
menu = ""
while(True):
    menu = ""
    #print("Amount of rooms ",len(ROOMS.keys()))
    roomAmount = len(ROOMS.keys())
    menu = menu + "1. Create new room \n"
    if (roomAmount != 0):
        keys = list(map(itemgetter(0), ROOMS.items())) 
        for i in range(roomAmount):
            menu = menu + str(i+2) + ". PORT: " + str(keys[i]) + "\n"
    #print(menu)

    
    conn, addr = s.accept()
    print ('Connected by', addr)
    data_string = pickle.dumps(menu)
    conn.send(data_string)
    data = conn.recv(4096)
    data_variable = pickle.loads(data)
    #print(data_variable)
    if (data_variable == '1'):
        c = c + 1
        x = threading.Thread(target=thread_function1, args=(c,))
        threads.append(x)
        x.start()
        ROOMS[c] = 0

        check_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """
        print("Checking new room....")
        while((check_socket.connect_ex((HOST, c))) == 0):
            pass
        """
        str1 = c
    else:
        str1 = str(keys[int(data_variable)-2])
    data_string = pickle.dumps(str1)
    conn.send(data_string)
    #print("These are the rooms ",ROOMS)

for index, thread in enumerate(threads):
    thread.join

