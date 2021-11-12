#Includes:
from pyueye import ueye         #pip install pyueye
import os
import ctypes
import time    
import numpy as np              #pip install numpy
import cv2                      #pip install opencv-python
import datetime as dt
class Ids_sw_cam:

    def __init__(self):
        print("Stelle Verbindung zur Kamera her...")
        #Instancen der Kamera:
        self.__hCam = ueye.HIDS(0)             #0: first available camera;  1-254: The camera with the specified camera ID
        self.__sInfo = ueye.SENSORINFO()
        self.__cInfo = ueye.CAMINFO()
        self.__pcImageMemory = ueye.c_mem_p()
        self.__MemID = ueye.int()
        self.__rectAOI = ueye.IS_RECT()
        self.__pitch = ueye.INT()
        self.__nBitsPerPixel = ueye.INT(24) 
        self.__channels = 3   
        self.__m_nColorMode = ueye.INT()		
        self.__bytes_per_pixel = int(self.__nBitsPerPixel / 8)
        # Starts the driver and establishes the connection to the camera
        nRet = ueye.is_InitCamera(self.__hCam, None)
        if nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        nRet = ueye.is_GetCameraInfo(self.__hCam, self.__cInfo)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")

        nRet = ueye.is_GetSensorInfo(self.__hCam, self.__sInfo)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")

        nRet = ueye.is_ResetToDefault(self.__hCam)

        # Set display mode to DIB
        nRet = ueye.is_SetDisplayMode(self.__hCam, ueye.IS_SET_DM_DIB)
        
        #Switch die Kameramodus je nach verwendeter Hardware
        if int.from_bytes(self.__sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(self.__hCam, self.__nBitsPerPixel, self.__m_nColorMode)
            self.__bytes_per_pixel = int(self.__nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )


        elif int.from_bytes(self.__sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            self.__m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            self.__nBitsPerPixel = ueye.INT(32)
            self.__bytes_per_pixel = int(self.__nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )

        elif int.from_bytes(self.__sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            self.__m_nColorMode = ueye.IS_CM_MONO8
            self.__nBitsPerPixel = ueye.INT(8)
            self.__bytes_per_pixel = int(self.__nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )

        else:
            # for monochrome camera models use Y8 mode
            self.__m_nColorMode = ueye.IS_CM_MONO8
            self.__nBitsPerPixel = ueye.INT(8)
            self.__bytes_per_pixel = int(self.__nBitsPerPixel / 8)
            print("else")
      
        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        nRet = ueye.is_AOI(self.__hCam, ueye.IS_AOI_IMAGE_GET_AOI, self.__rectAOI, ueye.sizeof(self.__rectAOI))
        if nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        self.__width = self.__rectAOI.s32Width
        self.__height = self.__rectAOI.s32Height

        nRet = ueye.is_AllocImageMem(self.__hCam, self.__width, self.__height, self.__nBitsPerPixel, self.__pcImageMemory, self.__MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            nRet = ueye.is_SetImageMem(self.__hCam, self.__pcImageMemory, self.__MemID)
            if nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                nRet = ueye.is_SetColorMode(self.__hCam, self.__m_nColorMode)
        

        nRet = ueye.is_InquireImageMem(self.__hCam, self.__pcImageMemory, self.__MemID, self.__width, self.__height, self.__nBitsPerPixel, self.__pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        # lädt die "autoParam.ini" Parameter
        self.loadParameter(1)
        print("Kamera ist bereit.")

    def __del__(self):
        ueye.is_FreeImageMem(self.__hCam, self.__pcImageMemory, self.__MemID)
        ueye.is_ExitCamera(self.__hCam)

    def loadParameter(self,mode):
        """load Parameter(startup)
        Funktion zum laden der Kameraparamter aus einer .ini Datei. 
        Fuer mode = 0 werden die "AutoParam.ini" Daten geladen.
        Fuer mode = 1 kann der Benutzer ueber das Filesystem auswaehlen, welche Parameter geladen werden sollen.
        """
        null = ueye.int(0)
        oldPfad = os.getcwd()
        if not os.path.exists('Multi_OO_Python'):
            os.makedirs('Multi_OO_Python')
        os.chdir('Multi_OO_Python')
        
        param = ueye.int(ueye.IS_PARAMETERSET_CMD_LOAD_FILE)
        if (mode == 1): #Erster Start beim Starten des Programms
            print("Lädt die hinterlegten Kameraparameter...")
            speicher = ctypes.c_wchar_p("autoParam.ini")
            nret = ueye.is_ParameterSet(self.__hCam,param,speicher,ueye.sizeof(speicher))
        
        elif (mode == 2): #Aufruf zum ändern der ini Datei.
            print("Welcher Datensatz soll geladen werden?")
            nret = ueye.is_ParameterSet(self.__hCam,param,null,ueye.sizeof(null))
        if (nret == ueye.IS_SUCCESS):
            print("Laden erfolgreich")

        else:
            print("Fehler beim Laden der Kameraparameter")

        os.chdir(oldPfad)

    def saveParameter(self,pfad = 0,_name = 0):
        """saveParameter(pfad,name)
        Ueber diese Funktion werden die aktuellen Kameraparameter in einer ini Datei mit dem aktuellen Zeitstempel
        gespeichert. Ueber den Parameter Pfad kann der Pfad mitgegeben werden, wo die Datei gespeichert werden soll.
        Wenn der Pfad leer ist, wird die Datei in den aktuell ausgewaehlten Pfad gespeichert.
        Ueber name kann dem Parameter noch ein Codewort zugeordnet werden. Wenn der Name leer ist, wird nur die Uhrzeit
        als Zuordnung verwendet.
        """
        param = ueye.int(ueye.IS_PARAMETERSET_CMD_SAVE_FILE)
        oldPfad = os.getcwd()  
        if not (pfad == 0):
            if not os.path.exists(pfad):
                os.makedirs(pfad)
            os.chdir(pfad)
        time=dt.datetime.now()
        if not (_name == 0):
            name = '{}_{}_Kameraparameter.ini'.format(_name,time.strftime("%Y%m%d_%H%M%S")) 
        else:
            name = '{}_Kameraparameter.ini'.format(time.strftime("%Y%m%d_%H%M%S"))
        speicher = ctypes.c_wchar_p(name)
        ueye.is_ParameterSet(self.__hCam,param,speicher,ueye.sizeof(speicher))
        os.chdir(oldPfad)

    def setPictureMode(self):
        """startPictureMode()
        Aktiviert den Software-Trigger der Kamera. Jetzt kann mit der takepicture() Funktion einzelene Bilder 
        aufgenommen werden.
        """
        #setzt die Kamera in den Software Trigger Modus
        ueye.is_SetExternalTrigger(self.__hCam,ueye.IS_SET_TRIGGER_SOFTWARE)
        self.getPicture()
        time.sleep(1/10) 

    def getPicture(self):
        """getPicture()
        Nimmt ein einzelnes Bild auf und skalliert es. Als Rueckgabewert wird der Bildframe gesendet.
        """
        ueye.is_FreezeVideo(self.__hCam,ueye.IS_DONT_WAIT)
        time.sleep(500/1000)
        array = ueye.get_data(self.__pcImageMemory,self.__width,self.__height, self.__nBitsPerPixel, self.__pitch, copy=False)
        frame = np.reshape(array,(self.__height.value, self.__width.value, self.__bytes_per_pixel))
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        return frame

    def setVideoMode(self):
        """startVideo()
        Startet den Videomodus der Kamera. Jetzt kann ueber getVideostream auf den aktuellen Videostream zugegeriffen 
        werden.
        """
        #Dieser Modus nimmt dauerhaft auf
        # Activates the camera's live video mode (free run mode)
        nRet = ueye.is_CaptureVideo(self.__hCam, ueye.IS_DONT_WAIT)
        if nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")
        else:
            print("is_CaptureVideo succes")
        time.sleep(1/10) 

    def getVideostream(self):
        """getVideostream
        Gibt den skallierten Videostreamframe zurueck.
        """
        array = ueye.get_data(self.__pcImageMemory, self.__width, self.__height, self.__nBitsPerPixel, self.__pitch, copy=False)
        frame = np.reshape(array,(self.__height.value, self.__width.value, self.__bytes_per_pixel))
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        return frame
        
    def setExposure(self,belichtungszeit):
        """changeExposure(belichtungszeit)
        Ueber den INT-Wert "Belichtungszeit" wird die Zeit eingestellt, bei der die Blende der Kamera geöffnet ist. 
        Hierbei sind die Maximalwerte, abhängig des Pixeltakts und der Framerate zu beachten. Diese Werte können über die 
        Funktion "getExposure(typ)" erfragt werden.
        """
        newexposure = ueye.double(belichtungszeit)
        ueye.is_Exposure(self.__hCam,ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, newexposure, ueye.sizeof(newexposure))
        time.sleep(1/10) 

    def getExposure(self,typ):
        """ getExposure(typ)
        Uber den INT-Wert "typ" kann die aktuelle, sowie die max/minimale Beleuchtungszeit erfragt werden.
        typ = 1 -> aktuelle Beleuchtungszeit
        typ = 2 -> min. Beleuchtungszeit.
        typ = 3 -> max. Beleuchtungszeit.
        """
        nTime = ueye.double(0)
        if (typ == 1):
            nRet  = (ueye.is_Exposure(self.__hCam,ueye.IS_EXPOSURE_CMD_GET_EXPOSURE,nTime,ueye.sizeof(nTime)))
            if (nRet != ueye.IS_SUCCESS):
                print("IS_GET_Exposure ERROR")
            else:
                return nTime
        elif (typ == 2):
            nRet  = (ueye.is_Exposure(self.__hCam,ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN,nTime,ueye.sizeof(nTime)))
            if (nRet != ueye.IS_SUCCESS):
                print("IS_GET_Exposure ERROR")
            else:
                return nTime
        elif (typ == 3):
            nRet  = (ueye.is_Exposure(self.__hCam,ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX,nTime,ueye.sizeof(nTime)))
            if (nRet != ueye.IS_SUCCESS):
                print("IS_GET_Exposure ERROR")
            else:
                return nTime
        else:
            print("Error - Fehlerhafte Eingabe getExposure")
            return nTime
        
    def setGamma(self,gamma):
        """setGamma(gamma)
        Ueber den Wert Gamma kann die Gamma-Korrektur der Kamera veraendert werden. Es wird ein INT-Wert erwartet.
        Standardwert = 100 -> Gammakorrektur = 1.0
        Range: min = 1; max = 1000
        """
        newgamma = ueye.int(gamma)
        ueye.is_Gamma(self.__hCam, ueye.IS_GAMMA_CMD_SET, newgamma,ueye.sizeof(newgamma))
        time.sleep(1/10) 

    def getGamma(self):
        """getGamma(gamma)
        Gibt den aktuell eingestellten Gamma Wert als INT Wert zurueck.
        Faktor = Rueckgabewert / 100
        """
        _gamma = ueye.int()
        ueye.is_Gamma(self.__hCam, ueye.IS_GAMMA_CMD_GET, _gamma, ueye.sizeof(_gamma))
        return _gamma
   
    def setShutterMode(self,mode):
        """setShutterMode(mode)
        Uber den INT-Wert Mode kann der Shutter Modus der Kamera veraendert werden.
        mode = 1 -> Rolling-Shutter-Modus wird unterstützt/Modus setzen
        mode = 2 -> Rolling-Shutter-Modus mit Global-Start wird unterstützt/Modus setzen
        mode = 3 -> Global-Shutter-Modus wird unterstützt/Modus setzen
        mode = 4 -> Global-Shutter-Modus mit anderen Timing-Parametern wird unterstützt/Modus setzen
        """
        if (mode == 1):
            _param = ueye.int(ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING)
        elif(mode == 2):
            _param = ueye.int(ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START)
        elif (mode ==3):
            _param = ueye.int(ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL)
        elif (mode ==4):
            _param = ueye.int(ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING)
        else:
            print("ERROR - ShutterModus")
            return
        ueye.is_DeviceFeature(self.__hCam, ueye.IS_DEVICE_FEATURE_CMD_SET_SHUTTER_MODE, _param, ueye.sizeof(_param))
        time.sleep(1/10) 

    def getShutterMode(self):
        """getShutterMode
        Liefert den aktuellen ShutterModus als String zurueck
        """
        _shutter = ueye.int()
        ueye.is_DeviceFeature(self.__hCam, ueye.IS_DEVICE_FEATURE_CMD_GET_SHUTTER_MODE, _shutter, ueye.sizeof(_shutter))
        if (_shutter == ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING):
            shutter = "Rolling-Shutter-Modus"
        elif (_shutter == ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL):
            shutter = "Global-Shutter-Modus"
        elif (_shutter == ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_ROLLING_GLOBAL_START):
            shutter = "Rolling-Shutter-Modus-Global-Start"
        elif (_shutter == ueye.IS_DEVICE_FEATURE_CAP_SHUTTER_MODE_GLOBAL_ALTERNATIVE_TIMING):
            shutter = "Global-Shutter-Modus-Global-Start"
        else:
            shutter = "Error GET Shuttermode"
        return shutter