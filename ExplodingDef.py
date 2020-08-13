from random import sample 
Mazo=[]
MP1=[]
MP2=[]
MP3=[]
MP4=[]
MP5=[]
Carta1="Va a ser que no"
Carta2="Ataque"
Carta3="Pasar"
Carta4="Favor"
Carta5="Barajar"
Carta6="Ver el futuro"
Carta7="Gato1"
Carta8="Gato2"
Carta9="Gato3"
Carta10="Gato4"
Carta11="Salvacion"
Carta12="Bomba"

def MazoPrincipal():
    #Se agrega al mazo la carta "Va a ser que no"
    for i in range(5):
        Mazo.append(Carta1)
    #Se agrega al mazo la carta "Ataque"
    for i in range(4):
        Mazo.append(Carta2)
    #Se agrega al mazo la carta "Pasar"
    for i in range(4):
        Mazo.append(Carta3)
    #Se agrega al mazo la carta "Favor"
    for i in range(4):
        Mazo.append(Carta4)
    #Se agrega al mazo la carta "Barajar"
    for i in range(4):
        Mazo.append(Carta5)
    #Se agrega al mazo la carta "Ver el futuro"
    for i in range(5):
        Mazo.append(Carta6)
    #Se agrega al mazo la carta "Gato1"
    for i in range(4):
        Mazo.append(Carta7)
    #Se agrega al mazo la carta "Gato2"
    for i in range(4):
        Mazo.append(Carta8)
    #Se agrega al mazo la carta "Gato3"
    for i in range(4):
        Mazo.append(Carta9)
    #Se agrega al mazo la carta "Gato4"
    for i in range(4):
        Mazo.append(Carta10)
    return Mazo
def MazoJugadores(Njugadores,Mazo):
    rando=sample(Mazo,k=len(Mazo))
    #####################################Dos Jugadores#####################################################
    if Njugadores=="2":
        for i in range(7):
            MP1.append(rando[0])
            rando.pop(0)
            MP2.append(rando[0])
            rando.pop(0)
        MP1.append(Carta11)
        MP2.append(Carta11)
        for i in range(4):
            rando.append(Carta11)
        for i in range(1):
            rando.append(Carta12)
    #####################################Tres Jugadores#####################################################
    if Njugadores=="3":
        for i in range(7):
            MP1.append(rando[0])
            rando.pop(0)
            MP2.append(rando[0])
            rando.pop(0)
            MP3.append(rando[0])
            rando.pop(0)
        MP1.append(Carta11)
        MP2.append(Carta11)
        MP3.append(Carta11)
        for i in range(3):
            rando.append(Carta11)
        for i in range(2):
            rando.append(Carta12)
    rando=sample(rando,k=len(rando))
    return MP1,MP2,MP3,MP4,MP5,rando

def Turnos(Njugadores,MP1,MP2,MP3,MP4,MP5,rando):
    #####################################Dos Jugadores#####################################################
    if Njugadores=="2":
        perdedor=""
        print(rando)
        fin=False
        FinTurnoP1=False
        FinTurnoP2=False
        while fin==False:
            print("Turno de jugador1")
            FinTurnoP1=False
            while FinTurnoP1==False:
                if "Bomba" in MP1 and "Salvacion" not in MP1:
                    print("Tienes bomba y no salvacion, eliminado")
                    perdedor="P2"
                    FinTurnoP1=True
                    FinTurnoP2=True
                    fin=True 
                elif "Bomba" in MP1 and "Salvacion" in MP1:
                    print("salvacion utilizada, fin de turno")
                    MP1.remove("Salvacion")
                    MP1.remove("Bomba")
                    rando.append(Carta12)
                    rando=sample(rando,k=len(rando))
                    print(rando)
                    FinTurnoP1=True
                else:
                    print("Que carta desea Jugar")
                    ContadorP1=1
                    print(MP1)
                    for i in MP1:
                        print(str(ContadorP1)+". "+i)
                        ContadorP1+=1
                    print("X. Terminar")
                    if "Va a ser que no" in MP1 or "Ataque" in MP1 or "Pasar" in MP1 or "Favor" in MP1 or "Barajar" in MP1 or "Ver el futuro" in MP1:
                        a=input()
                        if a=="Terminar":
                            MP1.append(rando[0])
                            rando.pop(0)
                            FinTurnoP1=True
                        elif a=="Pasar":
                            FinTurnoP1=True
                        elif a=="Ataque":
                            MP2.append(rando[0])
                            rando.pop(0)
                        elif a=="Favor":
                            MP2=sample(MP2,k=len(MP2))
                            MP1.append(MP2[0])
                            MP2.pop(0)
                        elif a=="Barajar":
                            rando=sample(rando,k=len(rando))
                        elif a=="Ver el futuro":
                            print(rando[0]+"-"+rando[1]+"-"+rando[2]+"-"+rando[3]+"-"+rando[4])
                        try:
                            MP1.remove(a)
                        except:
                            print(MP1)
                    else:
                        print("No tiene mas cartas jugables")
                        MP1.append(rando[0])
                        rando.pop(0)
                        FinTurnoP1=True
            print("Turno de jugador 2")
            FinTurnoP2=False
            while FinTurnoP2==False:
                if "Bomba" in MP2 and "Salvacion" not in MP2:
                    print("Tienes bomba y no salvacion, eliminado")
                    perdedor="P1"
                    FinTurnoP1=True
                    FinTurnoP2=True
                    fin=True 
                elif "Bomba" in MP2 and "Salvacion" in MP2:
                    print("salvacion utilizada, fin de turno")
                    MP2.remove("Salvacion")
                    MP2.remove("Bomba")
                    rando.append(Carta12)
                    rando=sample(rando,k=len(rando))
                    print(rando)
                    FinTurnoP2=True
                else:
                    print("Que carta desea Jugar")
                    ContadorP2=1
                    print(MP2)
                    for i in MP2:
                        print(str(ContadorP2)+". "+i)
                        ContadorP2+=1
                    print("4. Terminar")
                    if "Va a ser que no" in MP2 or "Ataque" in MP2 or "Pasar" in MP2 or "Favor" in MP2 or "Barajar" in MP2 or "Ver el futuro" in MP2:
                        a=input()
                        if a=="Terminar":
                            MP2.append(rando[0])
                            rando.pop(0)
                            FinTurnoP2=True
                        elif a=="Pasar":
                            FinTurnoP2=True
                        elif a=="Ataque":
                            MP1.append(rando[0])
                            rando.pop(0)
                        elif a=="Favor":
                            MP1=sample(MP1,k=len(MP1))
                            MP2.append(MP1[0])
                            MP1.pop(0)
                        elif a=="Barajar":
                            rando=sample(rando,k=len(rando))
                        elif a=="Ver el futuro":
                            print(rando[0]+"-"+rando[1]+"-"+rando[2]+"-"+rando[3]+"-"+rando[4])
                        try:
                            MP2.remove(a)
                        except:
                            print(MP2)
                    else:
                        print("No tiene mas cartas jugables")
                        MP2.append(rando[0])
                        rando.pop(0)
                        FinTurnoP2=True
    #####################################Tres Jugadores#####################################################
    if Njugadores=="3":
        perdedor=""
        print(rando)
        fin=False
        P1OUT=False
        P2OUT=False
        P3OUT=False
        FinTurnoP1=False
        FinTurnoP2=False
        FinTurnoP3=False
        while fin==False:
            P1OUT=False
            P2OUT=False
            P3OUT=False
            print("################Turno de jugador1################")
            FinTurnoP1=False
            while FinTurnoP1==False:
                if "Bomba" in MP1 and "Salvacion" not in MP1:
                    print("Tienes bomba y no salvacion, eliminado")
                    perdedor="P1"
                    FinTurnoP1=True
                    # FinTurnoP2=True
                    P1OUT=True
                    #fin=True 
                elif "Bomba" in MP1 and "Salvacion" in MP1:
                    print("salvacion utilizada, fin de turno")
                    MP1.remove("Salvacion")
                    MP1.remove("Bomba")
                    rando.append(Carta12)
                    rando=sample(rando,k=len(rando))
                    print(rando)
                    FinTurnoP1=True
                else:
                    print("Que carta desea Jugar")
                    ContadorP1=1
                    print(MP1)
                    for i in MP1:
                        print(str(ContadorP1)+". "+i)
                        ContadorP1+=1
                    print("X. Terminar")
                    if "Va a ser que no" in MP1 or "Ataque" in MP1 or "Pasar" in MP1 or "Favor" in MP1 or "Barajar" in MP1 or "Ver el futuro" in MP1:
                        a=input()
                        if a=="Terminar":
                            MP1.append(rando[0])
                            rando.pop(0)
                            FinTurnoP1=True
                        elif a=="Pasar":
                            FinTurnoP1=True
                        elif a=="Ataque":
                            MP2.append(rando[0])
                            rando.pop(0)
                        elif a=="Favor":
                            MP2=sample(MP2,k=len(MP2))
                            MP1.append(MP2[0])
                            MP2.pop(0)
                        elif a=="Barajar":
                            rando=sample(rando,k=len(rando))
                        elif a=="Ver el futuro":
                            print(rando[0]+"-"+rando[1]+"-"+rando[2]+"-"+rando[3]+"-"+rando[4])
                        try:
                            MP1.remove(a)
                        except:
                            print(MP1)
                    else:
                        print("No tiene mas cartas jugables")
                        MP1.append(rando[0])
                        rando.pop(0)
                        FinTurnoP1=True
            print("################Turno de jugador 2################")
            FinTurnoP2=False
            while FinTurnoP2==False:
                if "Bomba" in MP2 and "Salvacion" not in MP2:
                    print("Tienes bomba y no salvacion, eliminado")
                    perdedor="P2"
                    # FinTurnoP1=True
                    FinTurnoP2=True
                    P2OUT=True
                    # fin=True 
                elif "Bomba" in MP2 and "Salvacion" in MP2:
                    print("salvacion utilizada, fin de turno")
                    MP2.remove("Salvacion")
                    MP2.remove("Bomba")
                    rando.append(Carta12)
                    rando=sample(rando,k=len(rando))
                    print(rando)
                    FinTurnoP2=True
                else:
                    print("Que carta desea Jugar")
                    ContadorP2=1
                    print(MP2)
                    for i in MP2:
                        print(str(ContadorP2)+". "+i)
                        ContadorP2+=1
                    print("4. Terminar")
                    if "Va a ser que no" in MP2 or "Ataque" in MP2 or "Pasar" in MP2 or "Favor" in MP2 or "Barajar" in MP2 or "Ver el futuro" in MP2:
                        a=input()
                        if a=="Terminar":
                            MP2.append(rando[0])
                            rando.pop(0)
                            FinTurnoP2=True
                        elif a=="Pasar":
                            FinTurnoP2=True
                        elif a=="Ataque":
                            MP1.append(rando[0])
                            rando.pop(0)
                        elif a=="Favor":
                            MP3=sample(MP3,k=len(MP3))
                            MP2.append(MP3[0])
                            MP3.pop(0)
                        elif a=="Barajar":
                            rando=sample(rando,k=len(rando))
                        elif a=="Ver el futuro":
                            print(rando[0]+"-"+rando[1]+"-"+rando[2]+"-"+rando[3]+"-"+rando[4])
                        try:
                            MP2.remove(a)
                        except:
                            print(MP2)
                    else:
                        print("No tiene mas cartas jugables")
                        MP2.append(rando[0])
                        rando.pop(0)
                        FinTurnoP2=True
            print("################Turno de jugador 3################")
            FinTurnoP3=False
            while FinTurnoP3==False:
                if "Bomba" in MP3 and "Salvacion" not in MP3:
                    print("Tienes bomba y no salvacion, eliminado")
                    perdedor="P3"
                    # FinTurnoP1=True
                    # FinTurnoP2=True
                    FinTurnoP3=True
                    P3OUT=True
                    # fin=True 
                elif "Bomba" in MP3 and "Salvacion" in MP3:
                    print("salvacion utilizada, fin de turno")
                    MP3.remove("Salvacion")
                    MP3.remove("Bomba")
                    rando.append(Carta12)
                    rando=sample(rando,k=len(rando))
                    print(rando)
                    FinTurnoP3=True
                else:
                    print("Que carta desea Jugar")
                    ContadorP3=1
                    print(MP3)
                    for i in MP3:
                        print(str(ContadorP3)+". "+i)
                        ContadorP3+=1
                    print("x. Terminar")
                    if "Va a ser que no" in MP3 or "Ataque" in MP3 or "Pasar" in MP3 or "Favor" in MP3 or "Barajar" in MP3 or "Ver el futuro" in MP3:
                        a=input()
                        if a=="Terminar":
                            MP3.append(rando[0])
                            rando.pop(0)
                            FinTurnoP3=True
                        elif a=="Pasar":
                            FinTurnoP3=True
                        elif a=="Ataque":
                            MP1.append(rando[0])
                            rando.pop(0)
                        elif a=="Favor":
                            MP1=sample(MP1,k=len(MP1))
                            MP3.append(MP1[0])
                            MP1.pop(0)
                        elif a=="Barajar":
                            rando=sample(rando,k=len(rando))
                        elif a=="Ver el futuro":
                            print(rando[0]+"-"+rando[1]+"-"+rando[2]+"-"+rando[3]+"-"+rando[4])
                        try:
                            MP3.remove(a)
                        except:
                            print(MP3)
                    else:
                        print("No tiene mas cartas jugables")
                        MP3.append(rando[0])
                        rando.pop(0)
                        FinTurnoP3=True
            if P1OUT==True and P2OUT==True:
                perdedor="P3"
                fin=True
            if P2OUT==True and P3OUT==True:
                perdedor="P1"
                fin=True
            if P3OUT==True and P1OUT==True:
                perdedor="P2"
                fin=True
    return perdedor