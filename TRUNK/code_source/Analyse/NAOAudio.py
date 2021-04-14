from naoqi import ALProxy
import time
from SignalAudio import SignalAudio
import sys
import os

class NAOAudio:
    def __init__(self, IP = "127.0.0.1", PORT = 9559):
        self.__ip = IP #IP robot
        self.__port = PORT #PORT robot 
        
        self.__alTTS = ALProxy("ALTextToSpeech", IP, PORT)
        self.__alMemoryProxy = None #Connection to the module ALMemory
        self.__alDeviceAudioProxy = None #Connection to the module ALAudioDevice
        self.__alAudioRecorder = None #Connection to the module ALAudioRecorder
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
    
    def connectToALMemory(self):
        """
        Connection to the module ALMemory
        """
        try:
            self.__alMemoryProxy = ALProxy("ALMemory", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALMemory"
            print "Error was: ",e
            sys.exit(1)
    
    def connectToALAudioRecorder(self):
        """
        Connection to the module ALAudioRecorder
        """
        try:
            self.__alMemoryProxy = ALProxy("ALAudioRecorder", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALAudioRecorder"
            print "Error was: ",e
            sys.exit(1)
    
    def connectToALTextToSpeech(self):
        """
        Connection to the module ALTextToSpeech
        """
        try:
            self.__alMemoryProxy = ALProxy("ALTextToSpeech", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALTextToSpeech"
            print "Error was: ",e
            sys.exit(1)

    def startRecording(self, path = "/home/nao/recordRobot.wav"):
        """
        Start the audio recording by the robot and save the recording in the given path
        """
        print path
        self.__alDeviceAudioProxy.startMicrophonesRecording(path)

    def stopRecording(self):
        """
        Stop the actual recording
        """
        self.__alDeviceAudioProxy.stopMicrophonesRecording()
        
    def setSpeakerVolume(self, vol = 1):
        self.__alTTS.setVolume(vol)

    def speak(self, sentence = "Ok, I hear a whistlesound, yeaah"):
        self.__alTTS.say(sentence)

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

robot = NAOAudio("172.27.96.33", 9559)

robot.connectToALDeviceAudio()


robot.startRecording()

time.sleep(15)

robot.stopRecording()

#Access to the file NAO and download the specied file in the current desktop folder
cmd = 'scp nao@172.27.96.33:/home/nao/recordRobot.wav .' 
os.system(cmd)

signal = SignalAudio()

robot.setSpeakerVolume()

#if the covariance is greater then 0.5, then it's a whistle and the robot say it
if signal.correlate("whistle-3sec.wav", "recordRobot.wav"):
    robot.speak()
else:
    robot.speak("it seem that is not a whistle audio !")
