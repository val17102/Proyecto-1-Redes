import socket
import threading
import pickle

### Variables a setear para un cliente
inicioPartida = False

def send():
    global inicioPartida
    while True:
        print('\nTienes las siguientes opciones\n1. Iniciar la partida\n2. Enviar Mensaje')
        opcion = int(input('\nIngresa el numero de opcion > '))
        if opcion == 1:
            if inicioPartida == False:
                objeto = {
                    'opcion': opcion
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string) 
            else:
                print('La partida ya fue iniciada.')

        elif opcion == 2:
            if inicioPartida == True:
                msg = input('\nMe > ')
                objeto = {
                    'opcion' : opcion,
                    'mensaje': msg 
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.')

def receive():
    global inicioPartida
    while True:
        responseP = cli_sock.recv(4096)
        objeto = pickle.loads(responseP)

        if objeto['header'] == 'chat':
            sen_name = objeto['nombre']
            data_string = objeto['mensaje']

            print('\n' + str(sen_name) + ' > ' + str(data_string))
            print('\n> ')

        if objeto['header'] == 'inicio':
            inicioPartida = True
            print('\nEl juego ha sido iniciado')
            print('\n> ')

        if objeto['header'] == 'fallo':
            mensajeFallo = objeto['mensaje']
            print(mensajeFallo)
            print('\n> ')

### Se prepara la conexion por medio de sockets
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
### Nos conectamos al servidor que se encarga de crear las salas
ip_address = 'localhost'
port = 50001
### Conexion al server creador de salas 
cli_sock.connect((ip_address, port))
data = cli_sock.recv(4096)
data_variable = pickle.loads(data)
### Se solicita que se determine si se quiere crear una nueva sala o si se desea unir a una
print("Bienvenido a Exploding Kittens\nElija una de las siguientes opciones \n")
opcion1 = input(data_variable)
data_string = pickle.dumps(opcion1)
cli_sock.send(data_string)
### Recibimos el puerto para conectarnos de parte del servidor principal
data = cli_sock.recv(4096)
data_variable = pickle.loads(data)
cli_sock.close()
### Proceso para unirse a una sala
### Nos conectamos al servidor sala
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print("Conectandose en el puerto: ", data_variable)
serverResponseRoom = int(data_variable)
print(serverResponseRoom)

cli_sock.connect((ip_address, serverResponseRoom))
print("Conected")

thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()

