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
        self._ballCoordinatesTop = [-1, -1]
        self._ballCoordinatesBottom = [-1, -1]

        #ballGridLocation is an int that gives the rough square where the
        #ball's center is (values between 0 -> 15 inclusive)
        self._ballGridLocationTop = [-1, -1]
        self._ballGridLocationBottom = [-1, -1]

        #Ball area as perceived by the camera
        self._ballAreaTop = -1
        self._ballAreaBottom= -1

        self._vision = NVis(IP, PORT)
        self._imPr = ImPr()

        #Connects to top and bottom video cameras
        #self._vision._unsubscribeToVideoProxy(0)
        #self._vision._unsubscribeToVideoProxy(1)
        self._vision._subscribeToVideoProxy(0)
        self._vision._subscribeToVideoProxy(1)

    def _updateBallInfo(self, img, xml, CameraID):
        """
        This function updates the value of all ball related attributes by using
        the ImageProcessing function findBallRectangle().
        :param img: the image to be processed
        :param xml: the xml to use
        :param CameraID: top or bottom camera (0 and 1 respectively)
        """
        ballInfo = self._imPr.findBallRectangle(img, xml)

        if (CameraID == 0):

            #If no ball is detected
            if (len(ballInfo)<1):
                self._ballCoordinatesTop[0]= -1
                self._ballCoordinatesTop[0]= -1
                self._ballAreaTop = -1
                self._ballGridLocationTop = -1

            #If ball is detected
            else :
                #ballInfo[4] corresponds to x of center of ball
                #ballinfo[5] corresponds to y of center of ball
                #ballInfo[6] corresponds to the area of the ball
                self._ballCoordinatesTop[0] = ballInfo[4]
                self._ballCoordinatesTop[1] = ballInfo[5]
                self._ballAreaTop = ballInfo[6]
                self._updateBallGridLocation(self._ballCoordinatesTop[0], self._ballCoordinatesTop[1], 0)

        elif (CameraID == 1):

            #If no ball is detected
            if (len(ballInfo)<1):
                self._ballCoordinatesBottom[0]= -1
                self._ballCoordinatesBottom[0]= -1
                self._ballAreaBottom = -1
                self._ballGridLocationBottom = -1

            #If ball is detected
            else :
                #ballInfo[4] corresponds to x of center of ball
                #ballinfo[5] corresponds to y of center of ball
                #ballInfo[6] corresponds to the area of the ball
                self._ballCoordinatesBottom[0] = ballInfo[4]
                self._ballCoordinatesBottom[1] = ballInfo[5]
                self._ballAreaBottom = ballInfo[6]
                self._updateBallGridLocation(self._ballCoordinatesTop[0], self._ballCoordinatesTop[1], 1)



    def _updateBallGridLocation(self, x, y, cameraID):
        """
        This function updates the value of BallGridLocation
        Returns the value of the square holding
        the x and y pixels in an imaginary grid, with the grid having
        16 squares (from 0->15). Will be called in updateBallCoordinates
        :param x:
        :param y:
        :param cameraID:
        :return:
        """
        if (x != None and y!= None):

            xx = x/80
            yy = y/60
            if (cameraID == 0):
                self._ballGridLocationTop = [xx, yy]
            elif (cameraID == 1):
                self._ballGridLocationBottom = [xx, yy]
            return [xx, yy]

    def _takeTopImage(self, xml):
        """
        Takes an image using the top camera
        and updates ball information accordingly
        """
        img = self._vision._takeImage(0)
        self._updateBallInfo(img, xml, 0)
        return img

    def _takeBottomImage(self, xml):
        """
        Takes an image using the top camera
        and updates ball information accordingly
        """
        img = self._vision._takeImage(1)
        self._updateBallInfo(img, xml, 1)
        return img

class TestAnalyse(unittest.TestCase):

    def testUpdateBallGridLocation(self):
        """
        Tests if BallGridLocation gets updated correctly
        """
        analyse = Analyse(IP,PORT)
        self.assertEqual([2, 2],analyse._updateBallGridLocation(233, 172, 0))





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
    time.sleep(2)
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse('127.0.0.1', 9559)
    print(analyse._vision._videoProxy.getSubscribers())
    #analyse._vision._unsubscribeAll()
    naoimg = analyse._takeTopImage(xml)
    #naoimg2 = analyse._takeBottomImage(xml)
    print(analyse._ballCoordinatesTop)
    cv2.imshow('naoimg',naoimg)
    #cv2.imshow('naoimgbot',naoimg2)
    analyse._vision._unsubscribeAll()
    print(analyse._vision._videoProxy.getSubscribers())
    print(analyse._ballCoordinatesTop)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #cv2.imshow('NAOImage',naoimg)
