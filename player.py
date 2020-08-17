import socket
import threading
import pickle

### Variables a setear para un cliente
inicioPartida = False

### Variables para el manejo de una partida en una sala
CARDNO = 1
CARDATACK = 2
CARDSKIP = 3
CARDFAVOR = 4
CARDSHUFFLE = 5
CARDSEEFUTURE = 6
CARDDEFUSE = 7
CARDBOMB = 8

### Funciones para poder escuchar y enviar mensajes al Server
## Enviar mensajes
def send():
    global inicioPartida
    while True:
        print(
            '''
            \nTienes las siguientes opciones
            \n1. Iniciar la partida
            \n2. Enviar Mensaje
            \n3. Realizar Jugada
            \n4. Hacer un Favor
            \n5. Ver estado del juego
            \n6. Ver cartas que tengo
            \n7. Ver lista de jugadores conectados
            \n8. Instrucciones
            '''
        )
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
                msg = input('\nYo > ')
                objeto = {
                    'opcion' : opcion,
                    'mensaje': msg 
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.')

        elif opcion == 3:
            if inicioPartida == True:
                jugada = int(input('\nElige una jugada: \n1. Usar carta\n2. Tomar carta\n> '))
                if jugada == 1:
                    objeto = {
                        'opcion' : 5
                    }
                    data_string = pickle.dumps(objeto)
                    cli_sock.send(data_string)
                    objeto = {
                        'opcion' : 6
                    }
                    data_string = pickle.dumps(objeto)
                    cli_sock.send(data_string)
                    carta = int(input('\nElige el numero de carta a usar > '))
                    objeto = {
                        'opcion' : 7
                    }
                    data_string = pickle.dumps(objeto)
                    cli_sock.send(data_string)
                    favor = int(input('''
                        \nSi la carta es un favor o un gato elija el numero de Usuario a pedir la carta (si no lo es ingrese cualquier numero)  > 
                    '''))
                    gatos = int(input('''
                        \nSi la carta es un tipo de gato elija una de las siguientes opciones (si no lo es ingrese cualquier numero)
                        \n1. Usar 2 gatos iguales
                        \n2. Usar 3 gatos iguales
                        \n> 
                    '''))
                    cartaPedir = ''
                    if gatos == 1:
                        cartaPedir = int(input('\nIngrese la posicion de la carta quitar (desde posicion 1 al numero de cartas del jugador): '))
                    elif gatos == 2:
                        print('''
                            \n1. Carta NO
                            \n2. Carta ATACK
                            \n3. Carta SKIP
                            \n4. Carta FAVOR
                            \n5. Carta SHUFFLE
                            \n6. Carta SEE FUTURE
                            \n7. Carta DEFUSE
                            \n8. Carta GATO BARBA
                            \n9. Carta GATO ARCOIRIS
                            \n10. Carta GATO SANDIA
                            \n11. Carta GATO TACO
                            \n12. Carta GATO PAPA
                        ''')
                        cartaPedir = int(input('\nIngrese la carta que desea quitar: '))
                    objeto = {
                        'opcion' : opcion,
                        'jugada' : jugada,
                        'carta' : carta,
                        'favor' : favor,
                        'gatos' : gatos,
                        'cartaPedir' : cartaPedir
                    }
                    data_string = pickle.dumps(objeto)
                    cli_sock.send(data_string)
                elif jugada == 2:
                    objeto = {
                        'opcion' : opcion,
                        'jugada' : jugada
                    }
                    data_string = pickle.dumps(objeto)
                    cli_sock.send(data_string)
                else: 
                    print('Opcion invalida.')
            else:
                print('La partida aun no ha sido iniciada.')  

        elif opcion == 4:
            if inicioPartida == True:
                objeto = {
                    'opcion' : 5
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
                carta = int(input('\nElija el numero de carta de su mazo a dar > '))
                objeto = {
                    'opcion' : opcion,
                    'carta' : carta
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.')    

        elif opcion == 5:
            if inicioPartida == True:
                objeto = {
                    'opcion' : opcion
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.') 

        elif opcion == 6:
            if inicioPartida == True:
                objeto = {
                    'opcion' : opcion
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.')    

        elif opcion == 7:
            if inicioPartida == True:
                objeto = {
                    'opcion' : opcion
                }
                data_string = pickle.dumps(objeto)
                cli_sock.send(data_string)
            else:
                print('La partida aun no ha sido iniciada.')   

        elif opcion == 8:
            print(
                '''
Bienvenido a Exploding Kittens
El objetivo del juego es ir tomando cartas del mazo y evitar sacar las cartas de bomba para no salir de la partida
Además de tomar cartas, se tiene una serie de cartas para poder usar estrategicamente y ser el ultimo en pie en la partida

Al inicio la unica opcion que se tiene es la 1, pero una vez usada esta opcion e inciada la partida se podrán usar el resto

Tienes las siguientes opciones:
1. Iniciar la partida
Con esta opcion podemoos inciar una partida, siempre que hayan 3 a 5 jugadores en la sala. En caso no se cumpla esta condicion
se le notifica a los usuarios el intento fallido de iniciar partida.

2. Enviar Mensaje
Con esta opcion se puede mandar un mensaje a todos los usuarios de la partida

3. Realizar Jugada
Con esta opcion podemos tener 2 opciones al hacer la jugada que son: Usar una carta, y tomar una carta. A partir de las 
acciones que se tomen el juego ira transcurriendo

4. Hacer un Favor
Con esta opcion podemos dar una carta a otro jugador en caso nos lo hayan impuesto

5. Ver estado del juego
Con esta opcion podemos ver el estado del juego, el cual es la informacion publica sobre cuantas cartas hay en el mazo 
restantes y cuantas tiene cada jugador en su propio mazo

6. Ver cartas que tengo
Esta opcion permite ver las cartas que tienes en tu mazo

7. Ver lista de jugadores conectados
Esta opcion permite ver la lista de jugadores conectados en la sala

8. Instrucciones
Nos muestra estas instrucciones en pantalla

CARTAS Y SUS USOS
    CARTA DE NO
Esta carta permite saltar el turno de quien la usa, ósea no tomar carta, y darle 2 turnos al siguiente
jugador. No es acumulable los turnos si se lanzan en cadena.

    CARTA ATACK
Esta carta permite saltarse el turno, ósea no tomar carta y pasar el turno al siguiente jugador.

    CARTA SKIP
Esta carta permite solicitar una carta a un usuario específico, y la carta es la que decida el jugador
al que se le solicitó el favor.

    CARTA SHUFFLE
Esta carta mezcla las cartas que están en el mazo.

    CARTA SEE THE FUTURE
Esta carta le muestra al jugador las próximas 3 cartas que vienen en el mazo, y regresarlas en el
mismo orden después de verlas.

    CARTA DEFUSE
Esta carta permite desactivar la bomba si esta le sale a un jugador. Si se intenta usar la carta de
manera independiente, se muestra un error de que esta carta no se puede jugar, y se devuelve al
jugador.

    CARTA TIPO GATO
Esta carta permite al jugador robar cartas de otro jugador a su elección si se tienen 2 o 3 iguales de
un mismo tipo de gato. Si se tienen 2 iguales y se usan, estas salen de la mano del usuario y este
escoge una carta de su elección con respecto a posición en el mazo sin saber cual es y la roba. Si se
elige usar 3 cartas iguales entonces se roba una carta especifica que pida el jugador que va a robar.
En caso la tenga el adversario, se roba, y en caso no la tenga pues el jugador que quería robar pierde
sus 3 cartas. Si se usa la carta y no se tienen 2 o 3 iguales muestra un mensaje de error y pide repetir
el turno.
                '''
            )

        else:
            print('Opcion invalida')   

## Recibir mensajes
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

        if objeto['header'] == 'turno':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'estado':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'estadoPropio':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'response':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'fuera':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'futuro':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'usoCarta':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'listaJugadores':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

        if objeto['header'] == 'ganar':
            mensajeTurno = objeto['mensaje']
            print(mensajeTurno)
            print('\n> ')

### Se prepara la conexion por medio de sockets
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
### Nos conectamos al servidor que se encarga de crear las salas
ip_address = 'localhost'
port = 50001
### Se solicita que se ingresen los parametros de IP y PORT del servidor
ip_address = input("Bienvenido a Exploding Kittens Server\nIngrese la IP del host: ")
port = int(input("\nIngrese el puerto del Server: "))
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
username = input("Ingrese su username: ")
data_variable = pickle.dumps(username)
cli_sock.send(data_variable)
thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()

