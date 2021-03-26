from naoqi import ALProxy
from cv2 import cv2
from NAOVision import NAOVision as NVis
from ImageProcessing import ImageProcessing as ImPr
import time
import unittest

IP = '172.27.96.32'
PORT = 9559

class Analyse :

    def __init__(self, IP, PORT):

        #ballCoordinates will give the x,y of the center of the ball
        self._ballCoordinates = [None] * 2

        #ballGridLocation is an int that gives the rough square where the
        #ball's center is (values between 0 -> 15 inclusive)
        self._ballGridLocation = None

        #Ball area as perceived by the camera
        self._ballArea

        self._vision = NVis(IP, PORT)
        self._imPr = ImPr()

        #Connects to top and bottom video cameras
        self._vision._subscribeToVideoProxy(0)
        self._vision._subscribeToVideoProxy(1)

    def _updateBallInfo(self, img, xml):
        """
        This function updates the value of all ball related attributes by using
        the ImageProcessing function findBallRectangle()
        :param img:
        :param xml:
        :return:
        """
        ballInfo = self._imPr.findBallRectangle(img,xml)

        #If no ball is detected
        if (len(ballInfo)<1):
            self._ballCoordinates[0]= -1
            self._ballCoordinates[0]= -1
            self._ballArea = -1
            self._ballGridLocation = -1

        #If ball is detected
        else :
            #ballInfo[4] corresponds to x of center of ball
            #ballinfo[5] corresponds to y of center of ball
            #ballInfo[6] corresponds to the area of the ball
            self._ballCoordinates[0] = ballInfo[4]
            self._ballCoordinates[1] = ballInfo[5]
            self._ballArea = ballInfo[6]
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

    def _takeTopImage(self, xml):
        """
        Takes an image using the top camera
        and updates ball information accordingly
        """
        img = self._vision._takeImage(0)
        self._updateBallInfo(img, xml)

    def _takeBottomImage(self,img,xml):
        """
        Takes an image using the top camera
        and updates ball information accordingly
        """
        img = self._vision._takeImage(1)
        self._updateBallInfo(img, xml)

    def _getBallCoordinates(self):
        return self._ballCoordinates

    def _getBallArea(self):
        return self._ballArea

    def _getBallGridLocation(self):
        return self._ballGridLocation



class TestAnalyse(unittest.TestCase):

    def testUpdateBallGridLocation(self):
        """
        Tests if BallGridLocation gets updated correctly
        """
        analyse = Analyse(IP,PORT)
        self.assertEqual(10,analyse._updateBallGridLocation(233, 172))



if __name__ == "__main__":
    #unittest.main()

    #Other tests below:
    """Testing updateBallCoordinates
    times = time.time()
    img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg',6)
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse(4,5,6)
    analyse._updateBallCoordinates(img,xml)
    print(analyse._getBallCoordinates())
    print(time.time()-times)"""


    #Testing imageCapture on top camera
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse('172.27.96.32', 9559)
    print(analyse._vision._videoProxy)
    analyse._vision._subscribeToVideoProxy(0)
    print(analyse._vision._imgClientTop)
    print(analyse._vision._videoProxy)
    naoimg = analyse._vision._takeImage(0)
    analyse._updateBallCoordinates(naoimg, xml)
    print(analyse._ballCoordinates)
    print(analyse._ballGridLocation)
    #cv2.imshow('NAOImage',naoimg)
    #cv2.waitKey()
    #cv2.destroyAllWindows()