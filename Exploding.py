from random import sample 
from ExplodingDef import *
Mazo=[]
MP1=[]
MP2=[]
MP3=[]
MP4=[]
MP5=[]

Mazo=MazoPrincipal()
print(Mazo)

print("Bienvenido, ingrese el numero de jugadores")
Njugadores=input("Ingrese el numero de jugadores(Maximo 5): ")
MP1,MP2,MP3,MP4,MP5,rando=MazoJugadores(Njugadores,Mazo)

perdedor=Turnos(Njugadores,MP1,MP2,MP3,MP4,MP5,rando)
print("El ganador es: "+perdedor)


# print(MP1)
# print(MP2)
# print(MP3)
# print(MP4)
# print(MP5)
# print(rando)
