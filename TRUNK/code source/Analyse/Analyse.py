from naoqi import ALProxy
from cv2 import cv2
from NAOVision import NAOVision as nvis
from ImageProcessing import ImageProcessing as ImPr

class Analyse :

    def __init__(self, IP, PORT, CameraID):

        self._ballCoordinates = None
        #self._vision = nvis.__init__(IP,PORT,CameraID)
        self._ImPr = ImPr()

"""Temporary tests"""
img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg',6)
xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
analyse = Analyse.__init__(4,5,6)
analyse._ImPr.findBallRectangle(img,xml)