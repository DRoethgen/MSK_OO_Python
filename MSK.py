import Kamera
import Beleuchtung
import cv2
import os
import numpy
import datetime as dt
class m_CAM:
    def __init__(self, _port=9):
        #IDS SW Kamera Initalisieren
        self.cam = Kamera.Ids_sw_cam()
        #Arduino Initalisieren
        #print("Bitte gib die Nummer des Com-Ports an, an dem der Arduino angeschlossen ist.")
        #port = input()
        # diese Zeile beim Ändern des Ports durch die beiden Zeilen hier drüber ersetzen
        self.leds = Beleuchtung.Leds(_port) 
        self.cam.setPictureMode()
        self.temp_frames = numpy.zeros((10,512,640))            
        self.picsTaken = numpy.zeros((11))
        self.ledNames = ("400nm","450nm","465nm","520nm","585nm","620nm","660nm","730nm","840nm","940nm")
        self.camExpoTimes =[40,40,40,40,40,40,40,40,40,40,40] #0 = keine LED 11 = 940nm.

    def show(self,_frame,_time,_name):
        """show(frame,time,name)
        Funktion die ein Bild temporaer darstellt.
        frame = Bildframe
        time = Dauer die das Bild aktiv gehalten werden soll
        name = Name des Bildfensters
        """
        cv2.imshow(_name,_frame)
        cv2.waitKey(_time)

    def save(self,_frame,_ort,_name,_param = 0,_pName = 0):
        """save(frame,ort,name,param)
        Funktion die ein Bildframe abspeichert
        Frame = Bildframe
        Ort = Speicherstelle
        Name = Dateiname
        Param = 1 -> Speichert die Kameraparameter mit ab
        pName = "ABC" -> Speichert die Kameraparameter mit dem Inhalt von pName als Namenszusatz ab -> Hier also ABC_Datum_Kameraparameter.ini
        """
        oldPfad = os.getcwd()
        if not os.path.exists('Aufnahmen'):
            os.makedirs('Aufnahmen')
        os.chdir('Aufnahmen')
        if (_ort == 0):
            time=dt.datetime.now()
            ort = ('Standard_Aufnahmen/{}_Einzelbilder'.format(time.strftime("%Y%m%d_%H%M%S")))
        else:
            if not os.path.exists(_ort):
                os.makedirs(_ort)
            os.chdir(_ort)
        if (_param == 1):
            self.cam.saveParameter(0,_pName)
        cv2.imwrite(_name,_frame)
        os.chdir(oldPfad)
        
    def getNewLEDFrame(self,_ledNr = 0,_exposure = 0,_gamma = 0, _shutter = 0):
        """getNewLEDFrame(ledNr,exposure,gamma,shutter)
        Liefert einen Bildframe mit den gewunschten Einstellung zurueck.
        ledNr = 0 -> keine LED | 1 = 400nm | ... | 10 = 940nm..
        Exposure (Belichtungszeit) -> Wert in ms für die Belichtungszeit der Kamera
        Gamma -> Gammerkorrektur -> Achtung INT Wert Eingabe 100 => faktor 1 | Eingabe 150 => faktor 1,5 usw.
        shutter -> Hiermit kann zwischen den verschiedenen Shutter Modien gewechselt werden für Details siehe UeyeDoku 
        bzw. in die entsprechende Funktion der Kamera.py
        Wenn keine der Einstellugnsmöglichkeiten mitgegeben wird, wird ein Bild ohne LED und mit den in der Kamera hinterlegten Werten aufgenommen
        """
        if not (_exposure==0):
            self.cam.setExposure(_exposure)
        if not (_gamma==0):
            self.cam.setGamma(_gamma)
        if not (_shutter==0):
            self.cam.setShutterMode(_shutter)
        
        self.leds.setLEDOff()
        if not (_ledNr ==0):
            self.leds.setLED(_ledNr)     
        frame = self.cam.getPicture()
        self.leds.setLEDOff()
        return frame

    def saveTempFrame(self,_frame,_id):
        """saveTempFrame(frame,id)
        Speichert temporaer (solange das Programm laeuft) das aufgenommen Bild an der Stelle ID
        Somit koennen verschiedene Einstellung der Kamera ueberprueft werden und am Ende nur das Bild gespeichert werden,
        welches gewunscht ist.
        Id 1-10 fuer die jeweiligen LEDs."""
        self.temp_frames[_id-1] = _frame
        self.picsTaken[_id] = 1

    def getTempFrame(self,_id):
        """getTempFrame(id)
        Gibt, falls vorhanden das temporaer gespeicherte Bild als Bildframe zurueck"""
        if (self.picsTaken[_id]==1):

            return self.temp_frames[_id-1].astype(numpy.uint8)
        else:
            print("ERROR - getTempFrame - Es wurde noch kein Bild mit ID:"+str(_id)+" gespeichert.")
            return numpy.zeros((512,640)).astype(numpy.uint8)

    def getLEDnames(self,_id):
        """getLEDnames(id)
        Gibt den Namen der zur ID zugehoerigen LED wieder"""
        return (self.ledNames[_id-1])

    def getRGB(self,_expoR = 0,_expoG = 0,_expoB = 0):
        """getRGB(BelichtungszeitRot,BLZGruen,BLZBlau)
        Die Funktion nimmt ein Bild mit der roten, gruenen und blauen LED auf und berechnet daraus ein RGB Bild.
        Anschliessend werden alle vier Bilder unter /Aufnahmen/RGB_[DATUM] gespeichert.
        """
        if (_expoR ==0):
            _expoR = self.camExpoTimes[6]
        if (_expoG ==0):
            _expoG = self.camExpoTimes[3]
        if (_expoB ==0):
            _expoB = self.camExpoTimes[2]
        time=dt.datetime.now()
        ort = ('RGB_Bilder_Multispektralkamera/{}_Einzelbilder_und_RGBBild'.format(time.strftime("%Y%m%d_%H%M%S")))
        frameR = self.getNewLEDFrame(6,_expoR)
        self.save(frameR,ort,"Rot_620nm{}ms.jpg".format(_expoR),1,"Rot")
        frameG = self.getNewLEDFrame(4,_expoG)
        self.save(frameG,ort,"Gruen_520nm{}ms.jpg".format(_expoG),1,"Gruen")
        frameB = self.getNewLEDFrame(3,_expoB)
        self.save(frameB,ort,"Blau_465nm{}ms.jpg".format(_expoB),1,"Blau")
        frameRGB = cv2.merge((frameB,frameG,frameR))
        time=dt.datetime.now()
        self.save(frameRGB,ort,"RGB_Bild_{}.jpg".format(time.strftime("%Y%m%d_%H%M%S")))
    
    def getNPictures(self,_ledNr,_durchlaeufe):
        """getNPictures(ledNr,durchlaeufe)
        Speichert und nimmt eine beliebige Anzahl (Durchlaeufe) von Bildern einer gewuenschten LED (ledNr) ab/auf."""
        i = 0
        time = dt.datetime.now()
        ort = ('EinzelneLED_Multispektralkamera/{}_Einzelbilder'.format(time.strftime("%Y%m%d_%H%M%S")))
        while(i < _durchlaeufe):
            name = ("LED{}_Durchlauf_{}.jpg".format(_ledNr,i))
            self.save(self.getNewLEDFrame(_ledNr),ort,name)
            i +=1

    def getDiffPicture(self,_expoR = 0,_expoG = 0,_expoB = 0,_expoNo = 0):
        """getDiffPicture(BelichtungszeitRot,BLZGruen,BLZBlau)
        Die Funktion berechnet Differenzbilder und aus diesen ein RGB Bild und speichert alle Bilder ab."""
        ##TODO: Die Funktion ist nicht validiert - hier kann in der zweiten Projektwoche weitergearbeitet werden.
        if (_expoR ==0):
            _expoR = self.camExpoTimes[6]
        if (_expoG ==0):
            _expoG = self.camExpoTimes[3]
        if (_expoB ==0):
            _expoB = self.camExpoTimes[2]
        if (_expoNo ==0):
            _expoNo = self.camExpoTimes[0]
        rawFrameNo = self.getNewLEDFrame(0,_expoNo)
        rawFrameRed = self.getNewLEDFrame(6,_expoR)
        rawFrameGreen = self.getNewLEDFrame(4,_expoG)
        rawFrameBlue = self.getNewLEDFrame(3,_expoB)
        subFrameRed = cv2.subtract(rawFrameRed,rawFrameNo)
        subFrameGreen = cv2.subtract(rawFrameGreen,rawFrameNo)
        subFrameBlue = cv2.subtract(rawFrameBlue,rawFrameNo)
        rgbFrame = cv2.merge((subFrameBlue,subFrameGreen,subFrameRed))
        time=dt.datetime.now()
        ort = ('RGB_Diff_Bilder_Multispektralkamera/{}_Raw_Diff_RGB_Bilder'.format(time.strftime("%Y%m%d_%H%M%S")))
        self.save(rawFrameNo,ort,"Raw_noLED{}ms.jpg".format(_expoNo),1,"NoLED")
        self.save(rawFrameRed,ort,"Raw_Red{}ms.jpg".format(_expoR),1,"Red")
        self.save(rawFrameGreen,ort,"Raw_Green{}ms.jpg".format(_expoG),1,"Green")
        self.save(rawFrameBlue,ort,"Raw_Blue{}ms.jpg".format(_expoB),1,"Blue")
        self.save(subFrameRed,ort,"Sub_Red.jpg")
        self.save(subFrameGreen,ort,"Sub_Green.jpg")
        self.save(subFrameBlue,ort,"Sub_Blue.jpg")
        self.save(rgbFrame,ort,"RGB.jpg")

    def getLiveVideo(self):
        """getLiveVideo()
        Spielt solange nicht die Taste Q gedrückt wird einen Videostream ab."""
        self.cam.setVideoMode()
        print("Zum Beenden ins Videoklicken und 'Q' druecken")
        while(1):
            cv2.imshow("Live-Videostream", self.cam.getVideostream())
            if cv2.waitKey(1) & 0xFF == ord('q'): # beendet die Dauerschleife bei der Taste q
                break
    
    def setExpoTimes(self,_newExpo,_id):
        """setExpoTimes(newExpo,id)
        Ueber die Funktion kann die Belichtungszeit (newExpo) einer ausgewaehlten LED (id) veraendert werden
        id = 0 -> Keine Beleuchtung """
        if (_id >=0 and _id <10):
            self.camExpoTimes[_id] = _newExpo
    
    def getExpoTimes(self,_id = 99):
        """getExpoTimes(_id)
        Gibt die aktuell hinterlegte Belichtungszeit der jeweiligen LEDs zurueck.
        Wenn keine ID uebergeben wird, werden die Belichtungszeiten von allen LEDs automatisch in die Konsole 
        ausgegeben."""
        if (_id>=0 and _id <11):
            return self.camExpoTimes[_id]
        elif(_id ==99):
            i = 0
            while(i<11):
                print("Die Belichtungszeit fuer LED{} betraegt aktuell: {} ms.".format(i,self.camExpoTimes[i]))
                i+=1
            return
        else:
            print("ERROR -getExpoTimes")
            return -1

