import socket, os, pickle, threading
from operator import itemgetter 
HOST = 'localhost'
PORT = 50001
ROOMS = {}
ROOMScon = {}
startGame = {}
def thread_function1(port):
    banner = 0
    RPORT = port
    #print(RPORT)
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.bind((HOST, RPORT))
    print('starting to listen in Room', RPORT)
    ROOMScon[port] = list()
    startGame[port] = False
    r.listen(5)
    roomThreads = list()
    while (ROOMS[RPORT] < 5):
        #print("In room loop")
        roomCon, temp = r.accept()
        username = "User "+str(ROOMS[RPORT])
        ROOMScon[RPORT].append(roomCon)
        ROOMS[RPORT] = ROOMS[RPORT] + 1
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

        opcionJuego = objeto['opcion']
        if opcionJuego == 1:
            if startGame[port] == False:
                if ROOMS[port] > 2 and ROOMS[port] < 6:
                    mensajeInicio = {
                        'header' : 'inicio'
                    }
                    startGame[port] = True
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    for client in ROOMScon[port]:
                        client.send(mensajeInicioP)
                else:
                    mensajeInicio = {
                        'header' : 'fallo',
                        'mensaje' : '\nEl juego ha tratado de ser iniciado pero no hay suficientes jugadores aun.'
                    }
                    mensajeInicioP = pickle.dumps(mensajeInicio)
                    for client in ROOMScon[port]:
                        client.send(mensajeInicioP)

            else:
                mensajeInicio = {
                    'header' : 'fallo',
                    'mensaje' : '\nEl juego ya fue iniciado.'
                }
                mensajeInicioP = pickle.dumps(mensajeInicio)
                cli_sock.send(mensajeInicioP)

        elif opcionJuego == 2:
            if startGame[port] == True:
                broadcast_usr(username, cli_sock, objeto, port)
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

