import MSK
import time

"""
Dieses Skript dient dazu, einzlene, neue Funktionen, Klassen zu testen. So muss nicht lange durch das 
Hauptprogramm und die darin enthaltene Struktur navigiert werden, sondern man kann die zutestenen Funktionen direkt
unten aufrufen."""
Port = 7
msk = MSK.m_CAM(Port)


while(1):
    print("0 zum Beenden")
    e = int (input())
    if (e==0):
        break
    msk.get940nm()
    time.sleep(1000)