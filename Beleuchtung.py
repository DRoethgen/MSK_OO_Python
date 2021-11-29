from pyfirmata import Arduino   #pip install pyfirmata
import time
class Leds:
    
    def __init__(self,_port):
        print("Stelle Verbindung mit dem Arduino her...")
        _port = "COM"+str(_port)
        self.__board = Arduino(_port)
        print("Arduino ist bereit")
    
    def setLED(self,ledNr):
        """setLED(ledNR)
        aktiviert in Abhaengigkeit der ledNr die entsprechende LED.
        1 = 400, 2 = 450, 3 = 465, 4 = 520, 5=565, 6 = 620, 7 = 660, 8 = 730, 9 = 850, 10 = 940
        """
        if (ledNr == 1):
            print("Aktiviere LED1 - 400nm")
            self.__board.digital[4].write(0)
            self.__board.digital[8].write(1)
        elif (ledNr == 2):
            print("Aktiviere LED2 - 450nm")
            self.__board.digital[4].write(0)
            self.__board.digital[9].write(1)
        elif (ledNr == 3):
            print("Aktiviere LED3 - 465nm")
            self.__board.digital[4].write(0)
            self.__board.digital[10].write(1)
        elif (ledNr == 4):
            print("Aktiviere LED4 - 520nm")
            self.__board.digital[5].write(0)
            self.__board.digital[8].write(1)
        elif (ledNr == 5):
            print("Aktiviere LED5 - 585nm")
            self.__board.digital[5].write(0)
            self.__board.digital[9].write(1)
        elif (ledNr == 6):
            print("Aktiviere LED6 - 620nm")
            self.__board.digital[5].write(0)
            self.__board.digital[10].write(1)
        elif (ledNr == 7):
            print("Aktiviere LED7 - 660nm")
            self.__board.digital[6].write(0)
            self.__board.digital[8].write(1)
        elif (ledNr == 8):
            print("Aktiviere LED8 - 730nm")
            self.__board.digital[6].write(0)
            self.__board.digital[9].write(1)
        elif (ledNr == 9):
            print("Aktiviere LED9 - 850nm")
            self.__board.digital[6].write(0)
            self.__board.digital[10].write(1)
        elif (ledNr ==10):
            print("Aktiviere LED10 - 940nm")
            self.__board.digital[7].write(0)
            self.__board.digital[8].write(1)
            #self.__board.digital[9].write(1) # für 6 LEDs
            #self.__board.digital[10].write(1) # für 9 LEDs
        else:
            print("ERROR - setLED")
    time.sleep(1/10)

    def setLEDOff(self):
        """
        Schaltet alle LEDs aus.
        """
        i = 4
        while (i < 8):
            self.__board.digital[i].write(1)
            i = i + 1
        while (i < 11):
            self.__board.digital[i].write(0)
            i = i + 1

    def getLEDInfo(self):
        """getLEDInfo
        printet die wesentlichsten Infos zu den LEDs aus.
        """

        print("-------------------------------------------------------------------------------")
        print("Informationen der verwendeten LEDs:")
        print("Nr.:     Spektrum:       Wellenlänge:     Farbe:")
        print(" 1.         UV               400nm       -----")
        print(" 2.   Sichtbares Licht       450nm       Royal Blau")
        print(" 3.   Sichtbares Licht       465nm       Blau ")
        print(" 4.   Sichtbares Licht       520nm       Gruen")
        print(" 5.   Sichtbares Licht       585nm       Amber")
        print(" 6.   Sichtbares Licht       620nm       Rot")
        print(" 7.   Sichtbares Licht       660nm       Rot")
        print(" 8.   Sichtbares Licht       730nm       Far-Rot")
        print(" 9.         IR               840nm       -----")
        print(" 10.        IR               940nm       -----")
        print("-------------------------------------------------------------------------------")
        
    def debug940nm(self,_id):
        print("Aktiviere LED10 - 940nm")
        
        if (_id == 1):
            print("3-LEDs")
            self.__board.digital[7].write(0)
            self.__board.digital[8].write(1)
            time.sleep(1)
        elif (_id ==2):
            print("6-LEDs")
            self.__board.digital[7].write(0)
            self.__board.digital[8].write(1)
            self.__board.digital[9].write(1)
            time.sleep(1)
        elif (_id==3):
            print("9-LEDs")
            self.__board.digital[7].write(0) 
            self.__board.digital[8].write(1)
            self.__board.digital[9].write(1) 
            self.__board.digital[10].write(1)
            time.sleep(1)
        time.sleep(1/10)
        return
