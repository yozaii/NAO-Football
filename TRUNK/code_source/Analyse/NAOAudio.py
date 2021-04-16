from naoqi import ALProxy
import time
from SignalAudio import SignalAudio
import sys
import os
import unittest

class NAOAudio:
    def __init__(self, IP = "127.0.0.1", PORT = 9559):
        self.__ip = IP #IP robot
        self.__port = PORT #PORT robot 
        
        self.__alTTS = None #Connection to the module ALTextToSpeech
        self.__alMemoryProxy = None #Connection to the module ALMemory
        self.__alDeviceAudioProxy = None #Connection to the module ALAudioDevice
        self.__alSoundDetectionProxy = None #Connection to the module ALSoundDetection

        self.__ALValue = None 

        self.__eventName = "SoundDetected"
        self.__subscriberIdentifier = ""

    #---------------- Connection to NAO's modules ----------------#
    def connectToALTextToSpeech(self):
        """
        Connection to the module ALTextToSpeech
        """
        try:
            self.__alTTS = ALProxy("ALTextToSpeech", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALTextToSpeech"
            print "Error was: ",e
            raise Exception

    def connectToALMemory(self):
        """
        Connection to the module ALMemory
        """
        try:
            self.__alMemoryProxy = ALProxy("ALMemory", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALMemory"
            print "Error was: ",e
            raise Exception

    def connectToALDeviceAudio(self):
        """
        Connection to the module ALAudioDevice
        """
        try:
            self.__alDeviceAudioProxy = ALProxy("ALAudioDevice", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALAudioDevice"
            print "Error was: ",e
            raise Exception

    def connectToALSoundDetection(self):
        """
        Connection to the module ALSoundDetection
        """
        try:
            self.__alSoundDetectionProxy = ALProxy("ALSoundDetection", self.__ip, self.__port)
        except Exception,e:
            print "Could not create proxy to ALSoundDetection"
            print "Error was: ",e
            raise Exception

    #---------------- Recording methods (ALDeviceAudio) ----------------#
    def startRecording(self, path = "/home/nao/recordRobot.wav"):
        """
        Start the audio recording by the robot and save the recording in the given path
        """
        self.__alDeviceAudioProxy.startMicrophonesRecording(path)

    def stopRecording(self):
        """
        Stop the actual recording
        """
        self.__alDeviceAudioProxy.stopMicrophonesRecording()

    #---------------- Speaker methods (ALTextToSpeech) ----------------#
    def setSpeakerVolume(self, vol = 1):
        """
        Set the volume of NOA's voice (between 0 (0%) and 1 (100%))
        """
        self.__alTTS.setVolume(vol)

    def speak(self, sentence = "Ok, I hear a whistlesound, yeaah"):
        """
        Make speak the NAO
        """
        self.__alTTS.say(sentence)

    #---------------- Audio methods (ALSoundDetection) ----------------#
    def setSensitivity(self, sensitivity = 0.5):
        """
        Set the sensitivity of sound (between 0 and 1)
        """
        self.__alSoundDetectionProxy.setParameter("Sensitivity", sensitivity)

    def soundDetected(self):
        """
        Raised when a significant sound has been detected.
        """
        self.__alSoundDetectionProxy.SoundDetected(self.__eventName,self.__ALValue,  self.__subscriberIdentifier)

    #---------------- NAO's files recuperation ----------------#
    def downloadNaoFile(self, path = "scp nao@172.27.96.33:/home/nao/recordRobot.wav ."):
        """
        Access to the NAO's file and download the specied file in the current desktop folder
        """
        cmd = path
        os.system(cmd)
    #---------------- Getter and Setter ----------------#
    def getIP(self):
        return self.__ip

    def getPORT(self):
        return self.__port

class TestNAOAudio(unittest.TestCase):
    """
    def setUp(self):
        return super(NAOAudio, self).setUp()
    """

    def test_Instance_Of_RobotAudio_without_arguments(self):
        """
        Normally IP equals to "127.0.0.1" and PORT 9559
        """
        robotAudio = NAOAudio()

        self.assertEqual(robotAudio.getIP(), "127.0.0.1")
        self.assertEqual(robotAudio.getPORT(), 9559)

    #---------------- Tests with simulator or real robot ----------------#
    def test_connectToALTextToSpeech_without_error(self):
        """
        The method return nothin
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertIsNone(robotAudio.connectToALTextToSpeech)

    def test_connectToALMemory_without_error(self):
        """
        The method return nothin
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertIsNone(robotAudio.connectToALMemory)
    
    def test_connectToALDeviceAudio_without_error(self):
        """
        The method return nothin
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertIsNone(robotAudio.connectToALDeviceAudio)

    def test_connectToALSoundDetection_without_error(self):
        """
        The method return nothin
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertIsNone(robotAudio.connectToALSoundDetection)
    
    def test_startRecording_with_illegals_arguments(self):
        """
        Raise an Exception when illegals arguments are passed
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.startRecording, ("je veux une erreur", None))

    def test_stopRecording_with_illegals_arguments(self):
        """
        Raise an Exception when illegals arguments are passed
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.stopRecording, ("je veux une erreur", None))

    def test_startRecording_with_illegals_arguments(self):
        """
        Raise an Exception when illegals arguments are passed
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.startRecording, ("je veux une erreur", None))

    def test_setSpeakerVolume_with_illegals_arguments(self):
        """
        Raise an Exception when illegals arguments are passed
        (Need simulator or real robot to pass the test)
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.setSpeakerVolume, ("je veux une erreur", None))

    #---------------- Tests without simulator or real robot ----------------#
    def test_connectToALTextToSpeech_without_simulation(self):
        """
        Raise Exception when they are no robot simulation
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.connectToALTextToSpeech)
    
    def test_connectToALMemory_without_simulation(self):
        """
        Raise Exception when they are no robot simulation
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.connectToALMemory)
    
    def test_connectToALDeviceAudio_without_simulation(self):
        """
        Raise Exception when they are no robot simulation
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.connectToALDeviceAudio)
    
    def test_connectToALSoundDetection_without_simulation(self):
        """
        Raise Exception when they are no robot simulation
        """
        robotAudio = NAOAudio()

        self.assertRaises(Exception, robotAudio.connectToALSoundDetection)

    

if __name__ == "__main__":

    unittest.main()

"""
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
    danse(robot.postureProxy, robot.motionProxy)
else:
    robot.speak("it seem that is not a whistle audio !")
"""