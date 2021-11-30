import MSK
import time

"""
Dieses Skript dient dazu, einzlene, neue Funktionen, Klassen zu testen. So muss nicht lange durch das 
Hauptprogramm und die darin enthaltene Struktur navigiert werden, sondern man kann die zutestenen Funktionen direkt
unten aufrufen."""
Port = 9
msk = MSK.m_CAM(Port)
print(msk.cam.getFPNMode(2))
print(msk.cam.getFPNMode(1))
msk.leds.debug940nm(3)
msk.cam.setFPNMode(0)
print(msk.cam.getFPNMode())
msk.getLiveVideo()
time.sleep(2)
msk.cam.setFPNMode(1)
print(msk.cam.getFPNMode())
msk.getLiveVideo()
