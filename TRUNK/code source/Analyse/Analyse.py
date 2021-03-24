from naoqi import ALProxy
from cv2 import cv2
from NAOVision import NAOVision as NVis
from ImageProcessing import ImageProcessing as ImPr
import time
import unittest

IP = '168.1.1.1'
PORT = 9559

class Analyse :

    def __init__(self, IP, PORT):

        #ballCoordinates will give the x,y of the center of the ball
        self._ballCoordinates = [None] * 2

        #ballGridLocation is an int that gives the rough square where the
        #ball's center is (values between 0 -> 15 inclusive)
        self._ballGridLocation = None

        self._vision = NVis(IP, PORT)
        self._imPr = ImPr()

    def _updateBallCoordinates(self, img, xml):
        """
        This function updates the value of ballCoordinates by using
        the ImageProcessing function findBallRectangle()
        :param img:
        :param xml:
        :return:
        """
        ballInfo = self._imPr.findBallRectangle(img,xml)

        #ballInfo[4] corresponds to x of center of ball
        #ballinfo[5] corresponds to y of center of ball
        self._ballCoordinates[0] = ballInfo[4]
        self._ballCoordinates[1] = ballInfo[5]
        self._updateBallGridLocation(self._ballCoordinates[0], self._ballCoordinates[1])

    def _updateBallGridLocation(self, x, y):
        """
        This function updates the value of BallGridLocation
        Returns the value of the square holding
        the x and y pixels in an imaginary grid, with the grid having
        16 squares (from 0->15). Will be called in updateBallCoordinates
        :param x:
        :param y:
        :return:
        """
        xx = x/80
        yy = y/60
        self._ballGridLocation = (xx + 4*(yy))

        return (xx + 4*(yy))

    def _getBallCoordinates(self):
        return self._ballCoordinates

    def _getVision(self):
        return self._vision

class TestAnalyse(unittest.TestCase):

    def testUpdateBallGridLocation(self):
        """
        Tests if BallGridLocation gets updated correctly
        """
        analyse = Analyse(IP,PORT)
        self.assertEqual(10,analyse._updateBallGridLocation(233, 172))

if __name__ == "__main__":
    unittest.main()

    #Other tests below:
    """Testing updateBallCoordinates
    times = time.time()
    img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg',6)
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse(4,5,6)
    analyse._updateBallCoordinates(img,xml)
    print(analyse._getBallCoordinates())
    print(time.time()-times)"""

    """
    #Testing imageCapture on top camera
    analyse._vision._subscribeToVideoProxy(0)
    naoimg = analyse._vision._takeImage(0)
    cv2.imshow('NAOImage',naoimg)
    analyse._vision._unsubscribeToVideoProxy(0)"""