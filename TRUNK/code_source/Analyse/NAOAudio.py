import numpy as np
from naoqi import ALProxy
import matplotlib.pyplot as plt
import librosa
import librosa.display
import unittest


class NAOAudio:
    def __init__(self, IP = "127.0.0.1", PORT = 9559):
        self.__ip = IP #IP robot
        self.__port = PORT #PORT robot
        
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


class SignalAudio:
    def __init__(self):
        #path of the audio file format .wav
        self.__whistle_file = None

        # spectrogram of recorded whistles
        self.__whistleBegin = 2000
        self.__whistleEnd = 4000
        self.__sampleRate = 48000

        #
        self.__samplingFrequency = None
        
    def setAudioFile(self, path =""):
        """
        Set the path of the audio file
        """
        self.__whistle_file = path

    def digitized(self):
        """
        The audio file is loaded into a NumPy array after being sampled at a particular sample rate (sr)
        """
        self.__samplingFrequency = librosa.load(self.__whistle_file, sr=self.__sampleRate)

    def visualization(self, width = 6.4, height = 4.8):
        """
        Visualize the sampled signal and plot it (Matplotlib and Librosa librairies needed).
        We depicts the waveform visualization of the amplitude vs the time representation of the signal.
        """
        plt.figure(figsize=(width, height))

        #plotting the sampled signal
        librosa.display.waveplot(self.__samplingFrequency, sr=self.__sampleRate) #Normally sr=sr in te exemple code

    def normalization(self, axis):
        """
        A technique used to adjust the volume of audio files to a standard set level
        """
        return sklearn.preprocessing.minmax_scale(self.__samplingFrequency, axis=axis)