import MSK
import time
import os
"""
Dieses Skript dient dazu, einzlene, neue Funktionen, Klassen zu testen. So muss nicht lange durch das 
Hauptprogramm und die darin enthaltene Struktur navigiert werden, sondern man kann die zutestenen Funktionen direkt
unten aufrufen."""

msk = MSK.m_CAM()

#msk.getNPictures(5,10)
#msk.getDiffPicture()
#msk.saveTempFrame(msk.getNewLEDFrame(1),1)
#i = 1
#while(i<3):
#    print(i)
#    print(msk.getTempFrame(i))
#    i+=1
#while(1):
#    time.sleep(1)
msk.setExpoTimes(28,7)