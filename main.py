from numpy import double
import MSK
import cv2
port = 9
msk = MSK.m_CAM(port)

"""
Erklärung zum neuen Programm:
Die Kamera und die LED-Beleuchtung sind jetzt in je einer Klasse ausgeordnet wurden. Über eine weitere Klasse "MSK"
sind beide Klassen miteinander verknpuepft. 
Dadurch soll der Code verstaendlicher und leichter zu bedienen sein. Jede Funktion hat jetzt einen Erklaerungstext, 
der die Funktion der Funktion beschreibt, sowie die darin enthaltenen Parameter.
Um auf Funktionen der Unterklassen zugreifen zu können, kann man immer mit einen "." Operator eine Klasse weiter "springen".

Beispiel: In Zeile 5 wurde bereits das Objekt "msk" der Klasse MSK erstellt. Um jetzt z.B. die Belichtungsdauer der Kamera 
zu ändern, kann über msk.cam.setExposure(Dauer) dies getan werden. 
Erklärung: Nach msk. befindet man sich in der Klasse MSK und kann dort alle Funktionen (Methoden) benutzen. 
In der Klasse msk wird die Kamera (cam) und die Beleuchtungsplatine / Arduino als eigene Klassen erstellt (leds)
Über msk.cam. befindet man sich nun in der Klasse der Kamera und kann dort alle Methoden benutzen, wie im Beispiel gezeigt,
die Funktion um die Beleuchtungszeit zu erhöhen.

Aufgabe der Main Funktion/Klasse:
    In der Main Funktion sollte nur der Ablauf des Programms, wie z.B. die Menüstruktur oder später eine GUI beschrieben werden.
    Die eigentlichen Funktionen der Multispektralkamera sollten in der MSK Klasse durchgeführt werden.
"""
def printLine():
     print("-------------------------------------------------------------------------------")
#Menüstrukturen:
def hauptmenue(_e):
    if (_e == 1):
        menue_01()
    elif (_e ==2):
        menue_02()
    elif(_e == 3):
        msk.getRGB()
    elif(_e == 4):
        print("Mit welcher LED sollen Bilder gemacht werden?")
        while(1):
            e = int(input())
            if (e == 0):
                break
            elif(e>0 and e <10):
                print("Wie viele Aufnahmen sollen gemacht werden?[0-1000]")
                while(1):
                    f = int(input())
                    if (f==0):
                        return
                    elif(f>0 and f <1000):
                        msk.getNPictures(e,f)
                    else:
                        print("ERROR - Fehlerhafte Eingabe Anzahl Durchlaeufe[0-1000]")
                    
            else:
                print("ERROR - Fehlerhafte Eingabe mehereBildermiteinerLED")
    elif(_e == 5):
        msk.getDiffPicture()
    elif (_e == 6):
        pass
    elif (_e == 7):
        menue_07()
    elif (_e == 8):
        pass
    elif (_e == 9):
        cv2.destroyAllWindows()
    else:
        print("ERROR - Eingabe Hauptmenue")

def menue_01(): #Bilder aufnehmen
    while(1):
        print("Welches Spektrum moechtest du aufnehmen?")
        print("1.: UV-Spektrum")
        print("2.: Sichtbares-Spektrum")
        print("3.: IR-Spektrum")
        print("4.: Komplettes Spektrum")
        print("5.: einzelne LED")
        print("6.: Infos zu den LEDs")
        print("0.: Zurueck ins Hauptmenue.")
        e = int(input())
        if (e == 0):
            break
        elif (e==1):
            msk.saveTempFrame(msk.getNewLEDFrame(1),1)
        elif (e==2):
            i = 2
            while (i < 9):
                msk.saveTempFrame(msk.getNewLEDFrame(i),i)
                i +=1
        elif (e==3):
            i = 9
            while (i < 11):
                msk.saveTempFrame(msk.getNewLEDFrame(i),i)
                i +=1
        elif (e==4):
            i = 1
            while (i < 11):
                msk.saveTempFrame(msk.getNewLEDFrame(i),i)
                i +=1
        elif (e==5):
            print("Welche LED soll aufgenommen werden [1-9]?")
            while(1):
                f = int(input)
                if (f > 0 and f < 11):
                    msk.saveTempFrame(msk.getNewLEDFrame(f),f)
                    break
                else:
                    print("ERROR - Fehlerhafte Eingabe einzelne LED")
        elif (e==6):
            msk.leds.getLEDInfo()
        else:
            print("Error - Fehlerhafte Eingabe Menue01")

def menue_02(): #Bilder speichern
    print("Welches Bild moechtest du speichern?")
    print("1 = UV")
    print("2 = sichtbare")
    print("3 = IR")
    print("4 = Alle")
    print("5 = ein bestimmtes Bild speichern...")
    print("0 = zurueck ohne speichern")
    while(1):        
        e = int(input())
        if (e==0):
            break
        elif (e>0 and e<6):
            if (e==1):
                msk.save(msk.getTempFrame(1),0,"{}.jpg".format(msk.getLEDnames(1)),0)
                
            elif (e==2):
                i = 2
                while (i < 9):
                    msk.save(msk.getTempFrame(i),0,"{}.jpg".format(msk.getLEDnames(i)),0)
                    i +=1
            elif (e==3):
                i = 9
                while (i < 11):
                    msk.save(msk.getTempFrame(i),0,"{}.jpg".format(msk.getLEDnames(i)),0)
                    i +=1
            elif (e==4):
                i = 1
                while (i < 11):
                    msk.save(msk.getTempFrame(i),0,"{}.jpg".format(msk.getLEDnames(i)),0)
                    i +=1
            elif (e==5):
                print("Welche LED soll gespeichert werden [1-9]?")
                while(1):
                    f = int(input)
                    if (f > 0 and f < 11):
                        msk.save(msk.getTempFrame(f),0,"{}.jpg".format(msk.getLEDnames(f)),0)
                        break
        else:
            print("ERROR - Fehlerhafte Eingabe Menue2")

def menue_07(): #Kalibrieren
    while(1):
        print("Was moechtest du Kalibrieren?")
        print("1.: Kamera (mechanischer Fokus)")
        print("2.: optische Leistung der LEDs")
        print("3.: Beleuchtungszeiten der LEDs einstellen")
        print("4.: Lade Kamera-Parametersatz")
        print("0.: Zurueck ins Hauptmenue")
        while(1):
            e = int(input())
            if (e == 0):
                print("hallo")
                return                
            if (e == 1):
                msk.getLiveVideo()
            elif (e==2):
                 print("Welche LED moechtest du aktivieren?[1-10]")
                 print("0.: zurueck im Menue")
                 while(1):
                    e=int(input)
                    if (e==0):
                        break
                    elif(e>0 and e <11):
                        msk.leds.setLED(e)
                        print("Zum Ausschalten, beliebige Taste druecken")
                        input()
                        msk.leds.setLEDOff()
                    else:
                        print("ERROR - Fehlerhafteeingabe LED Nummer")
            elif (e==3):
                print("Wie lange soll die neue Beleuchtungszeit sein?")
                print("Die minimale Beleuchtungszeit betraegt: {}ms".format(msk.cam.getExposure(2)))
                print("Die maximale Beleuchtungszeit betraegt: {}ms".format(msk.cam.getExposure(3)))
                msk.getExpoTimes()
                while(1):
                    e = int(input())
                    if (e==0):
                        return
                    elif(e>0 and e <400):
                        print("Von welcher LED soll die Beleuchtungszeit auf {} ms veraendert werden [0-10]?".format(e))
                        while(1):
                            f = int(input())
                            if (f>=0 and f <11):
                                msk.setExpoTimes(e,f)
                                break
                            else:
                                print("ERROR - Fehlerhafte Eingabe LED Auswahl")
                    else:
                        print("ERROR - Fehlerhafte Eingabe Belichtungszeit")
            elif (e==4):
                msk.cam.loadParameter(2)
                return
            else:
                print("Error - Fehlerhafte Eingabe menue07")

#AB HIER BEGINNT DAS PROGRAMM


while (1):
    printLine()
    print("------------------------ Multispektralkamera V1.0 -----------------------------")
    print("Was moechtest du tun?")
    print("1. = Bilder aufnehmen")
    print("2. = Bilder speichern")
    print("3. = Mit der Blauen(450nm), der Gruenen(520nm) und der Roten(620nm) ein Bild aufnehmen und es als RGB Bild zusammensetzen")
    print("4. = Eine auszuwählende LED mehrfach hintereinander ein Bild aufnehmen lassen")
    print("5. = Bilder subtrahieren ")
    print("6. =  - ")
    print("7. = Kalibrieren")
    print("8. = -")
    print("9. = Offene Bildfenster schliessen")
    print("0. = Beenden")
    printLine()
    printLine()
    eingabe = int (input())
    if not (eingabe == 0):
        hauptmenue(eingabe)
    else:
        break

msk.cam.__del__()