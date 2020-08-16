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
ROOMSplayersAlive = {}

### Variables para el manejo de una partida en una sala
CARDNO = 1
CARDATACK = 2
CARDSKIP = 3
CARDFAVOR = 4
CARDSHUFFLE = 5
CARDSEEFUTURE = 6
CARDDEFUSE = 7
CARDBOMB = 8

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
    ROOMpiles[port] = [1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,6]
    ROOMamountDefuses[port] = 6
    ROOMSturnPlayers[port] = list()
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
            if startGame[port] == False:
                ### Se revisa que haya al menos 3 jugadores para poder empezar la partida
                if ROOMS[port] > 2 and ROOMS[port] < 6:
                    ### Se hace un set de los elementos del juego
                    ### Se revuelve el mazo
                    random.shuffle(ROOMpiles[port])
                    random.shuffle(ROOMpiles[port])
                    random.shuffle(ROOMpiles[port])

                    ### Se le da un defuse a cada jugador
                    for player in ROOMScon[port]:
                        ROOMpilesPlayers[port][player].append(7)
                        ROOMamountDefuses[port] = ROOMamountDefuses[port] - 1
                    
                        ### Se reparten 7 cartas a cada jugador
                        for k in range(7):
                            pilaTemporal = ROOMpiles[port]
                            ROOMpilesPlayers[port][player].append(pilaTemporal.pop())
                            ROOMpiles[port] = pilaTemporal

                    ### Se agregan los defuses y bombas al mazo
                    random.shuffle(ROOMpiles[port])
                    random.shuffle(ROOMpiles[port])
                    random.shuffle(ROOMpiles[port])

                    for player in ROOMScon[port]:
                        if i < len(ROOMScon[port]) - 1:
                            ### Se agrega una bomba y se revuelve
                            ROOMpiles[port].append(8)
                            random.shuffle(ROOMpiles[port])
                        
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
                    ROOMSturnPlayers[port].append([0,1])
                    mensajeTurno = {
                        'header' : 'turno',
                        'mensaje' : '\nEs el turno del User '+str(ROOMSturnPlayers[port][0][0])+'.'
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
                    'mensaje' : '\nEl juego aun no ha sido.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)        

        ### La opcion 3 es para poder realizar una jugada cuando es el turno del cliente
        elif opcionJuego == 3:
            ### Solo se pueden hacer jugadas cuando la partida ha iniciado


            
            if startGame[port] == True:
                mensajeInicio = {
                    'header' : 'fallo',
                    'mensaje' : '\nTurno jugador: '+str(ROOMSturnPlayers[port])+' Conexiones: '+str(ROOMScon[port])
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)


                #broadcast_usr(username, cli_sock, objeto, port)
            ### Si no se ha iniciado mandamos un mensaje de error al cliente para indicarle que la partida
            ### aun no ha iniciado
            else:
                mensajeInicio = {
                    'header' : 'fallo',
                    'mensaje' : '\nEl juego aun no ha sido.'
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

