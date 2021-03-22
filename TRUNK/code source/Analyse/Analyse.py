from naoqi import ALProxy
from cv2 import cv2
from NAOVision import NAOVision as nvis
from ImageProcessing import ImageProcessing as ImPr
import time

class Analyse :

    def __init__(self, IP, PORT):

        #ballCoordinates will give the x,y of the center of the ball
        self._ballCoordinates = [None] * 2

        self._vision = nvis(IP, PORT)
        self._ImPr = ImPr()

    def _updateBallCoordinates(self,img,xml):
        """
        This function updates the value of ballCoordinates by using
        the ImageProcessing function findBallRectangle()
        :param img:
        :param xml:
        :return:
        """
        ballInfo = self._ImPr.findBallRectangle(img,xml)
        self._ballCoordinates[0] = ballInfo[4]
        self._ballCoordinates[1] = ballInfo[5]

    def _getBallCoordinates(self):
        return self._ballCoordinates

    def _getVision(self):
        return self._vision

if __name__ == "__main__":

    #Testing updateBallCoordinates
    times = time.time()
    img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg',6)
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse(4,5,6)
    analyse._updateBallCoordinates(img,xml)
    print(analyse._getBallCoordinates())
    print(time.time()-times)

    #Testing imageCapture on top camera
    analyse._vision._subscribeToVideoProxy(0)
    naoimg = analyse._vision._takeImage(0)
    cv2.imshow('NAOImage',naoimg)
    analyse._vision._unsubscribeToVideoProxy(0)