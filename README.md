# Proyecto-1-Redes

> Descripción

> El presente proyecto está basado en la creación de un juego de cartas implementando un protocolo de comunicación creado por nosotros, basado en TCP, mientras que el juego implementado es Exploding Kittens, el cual es un juego basado en turnos cuyo objetivo es sobrevivir a las bombas que se encuentran en el mazo, en el cual cada turno el jugador debe de activar cartas especiales y al no tener ninguna deben de tomar una carta del mazo con el riesgo de que sea una bomba.


## Contenido

- [Instalación](#instalación)
- [Funcionamiento](#funcionamiento)
- [Desarrolladores](#desarrolladores)


## Instalación

### Herramientas

- No es necesario instalar herramientas adicionales. Todo lo necesario para comenzar es el command prompt. Si es más conveniente se puede usar cualquier IDE pero no es necesario.

### Python

-Descargar e instalar Python 3.x

<a href="https://www.python.org/">

### Librerías

- os
- pickle
- random
- socket
- threading

> Todas las librerías utilizadas son estándar con Python 3.x

### Clone

- Clonar este repositorio a tu ordenador local `https://github.com/val17102/Proyecto-1-Redes.git`

### Setup

- If you want more syntax highlighting, format your code like this:

> Para iniciar el servidor: Abrir un command prompt en la ubicación del archivo "mainServer.py"

```shell
$ py mainServer.py
```
> Para iniciar un cliente: Abrir un command prompt en la ubicación del archivo "player.py"

```shell
$ py player.py
```

## Funcionamiento

> El funcionamiento del protocolo que fue utilizado para el proyecto se lleva a cabo por medio de  comunicación por Sockets BSD, el cual envía y recibe la información de los usuarios y de las jugadas por medio de diccionarios que nosotros estructuramos y realizamos por medio de python. Estos diccionarios contienen la información de la jugada más reciente, el mazo de los jugadores y del siguiente jugador que debe de jugar, nuestro protocolo se encarga de unir y separar esa información, ya sea cuando es enviado o cuando es recibido por los distintos jugadores.

## Desarrolladores

- Luis Esturban
- David Soto
- Miguel Valle
