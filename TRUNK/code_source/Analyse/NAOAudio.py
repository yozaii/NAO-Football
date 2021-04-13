from naoqi import ALProxy

class NAOAudio:
    def __init__(self, IP = "127.0.0.1", PORT = 9559):
        self.__ip = IP #IP robot
        self.__port = PORT #PORT robot
        
        self.__alDeviceAudioProxy = None #Connection to the module ALAudioDevice
        self.__soundDetectionProxy = None #Connection to the module ALSoundDetection
        self.__ALValue = None 

        self.__eventName = "SoundDetected"
        self.__subscriberIdentifier = ""

    def connectToALSoundDetection(self):
        """
        Connection to the module ALSoundDetection
        """
        try:
            self.__soundDetectionProxy = ALProxy("ALSoundDetection", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALSoundDetection"
            print "Error was: ",e
            sys.exit(1)

    def connectToALDeviceAudio(self):
        """
        Connection to the module ALAudioDevice
        """
        try:
            self.__alDeviceAudioProxy = ALProxy("ALAudioDevice", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALAudioDevice"
            print "Error was: ",e
            sys.exit(1)
    
    def startRecording(self):
        self.__alDeviceAudioProxy.startMicrophonesRecording("C:\Users\Emman\Desktop\L3h1\TRUNK\code_source\Analyse\recordRobot.wav")

    def stopRecording(self):
        self.__alDeviceAudioProxy.stopMicrophonesRecording()
        

    def subscribeToALSoundDetection(self, subscribeID = "default"):
        self.__soundDetectionProxy.subscribe(subscribeID)

    def setSensitivity(self, sensitivity = 0.5):
        """
        Set the sensitivity of sound (between 0 and 1)
        """
        self.__soundDetectionProxy.setParameter("Sensitivity", sensitivity)

    def soundDetected(self):
        """
        Raised when a significant sound has been detected.
        """
        self.__soundDetectionProxy.SoundDetected(self.__eventName,self.__ALValue,  self.__subscriberIdentifier)

robot = NAOAudio()

robot.connectToALDeviceAudio()