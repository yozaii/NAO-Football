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

        #ballGridLocation is an int that gives the location of  the
        #ball's center in a 4x4 grid (values between 0 -> 15 inclusive)
        self._ballGridLocationTop = [-1, -1]
        self._ballGridLocationBottom = [-1, -1]

        #Ball area as perceived by the camera
        self._ballAreaTop = -1
        self._ballAreaBottom= -1

        #Ball height
        self._ballHeightTop = -1
        self._ballHeightBottom = -1

        #Goal position attributes
        self._goalLeftPostBase = [-1,-1]
        self._goalRightPostBase = [-1, -1]
        self._goalTopPostCenter = [-1,-1]
        self._goalArea = -1

        #The posts grid location
        self._goalLeftBaseGrid = [-1,-1]
        self._goalRightBaseGrid = [-1,-1]
        self._goalTopCenterGrid = [-1, -1]
        self._goalCenterGrid = [-1,-1]

        #Distance from robot to ball in meters
        self._distanceToBall = -1

        self._vision = NVis(IP, PORT)
        self._imPr = ImPr()



        #Connects to top and bottom video cameras
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
            if (ballInfo[0] == -1):
                self._ballCoordinatesTop[0]= -1
                self._ballCoordinatesTop[0]= -1
                self._ballAreaTop = -1
                self._ballHeightTop = -1
                self._ballGridLocationTop = [-1, -1]
                self._distanceToBall = -1

            #If ball is detected
            else :
                #ballInfo[3] corresponds to height of ball
                #ballInfo[4] corresponds to x of center of ball
                #ballinfo[5] corresponds to y of center of ball
                #ballInfo[6] corresponds to the area of the ball
                self._ballCoordinatesTop[0] = ballInfo[4]
                self._ballCoordinatesTop[1] = ballInfo[5]
                self._ballAreaTop = ballInfo[6]
                self._ballHeightTop = ballInfo[3]
                self._updateDistanceToBall()
                self._updateBallGridLocation(self._ballCoordinatesTop[0], self._ballCoordinatesTop[1], 0)

        elif (CameraID == 1):

            #If no ball is detected
            if (ballInfo[0] == -1):
                self._ballCoordinatesBottom[0]= -1
                self._ballCoordinatesBottom[1]= -1
                self._ballAreaBottom = -1
                self._ballHeightBottom = -1
                self._ballGridLocationBottom = [-1, -1]
                self._distanceToBall = -1

            #If ball is detected
            else :
                #ballInfo[4] corresponds to x of center of ball
                #ballinfo[5] corresponds to y of center of ball
                #ballInfo[6] corresponds to the area of the ball
                self._ballCoordinatesBottom[0] = ballInfo[4]
                self._ballCoordinatesBottom[1] = ballInfo[5]
                self._ballAreaBottom = ballInfo[6]
                self._ballHeightBottom = ballInfo[3]
                self._updateDistanceToBall()
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

    def _updateDistanceToBall(self):
        """Updates the distance to ball according to where
        it is perceived on the camera
        """
        #If ball is not seen
        if self._ballHeightTop == -1 and self._ballHeightBottom -1:
            self._distanceToBall = -1

        #If ball is seen
        else:
            #Ball is een aroudn the top of the TopImage
            if self._ballGridLocationTop[1] == 0:
                #ratio allows us to find a more precise approximation
                #of the distance to the ball
                #ratio = self._ballHeightTop
                self._distanceToBall = 4

            elif self._ballGridLocationTop[1] == 1:
                self._distanceToBall = 3

            elif self._ballGridLocationTop[1] == 2:
                self._distanceToBall = 2

            elif self._ballGridLocationTop[1] == 3:
                self._distanceToBall = 1

            #Ball is seen around the top of TopImage
            elif self._ballGridLocationBottom[1] == 0:

                self._distanceToBall = 1

            elif self._ballGridLocationBottom[1] == 1:
                self._distanceToBall = 0.75

            elif self._ballGridLocationBottom[1] == 2:
                self._distanceToBall = 0.5

            elif self._ballGridLocationBottom[1] == 3:
                self._distanceToBall = 0.25



    def _updateGoalInfo(self, img):
        """
        Updates goal related attributes when taking an image
        :param img:
        :return:
        """
        goalInfo = self._imPr.findGoalRectangle(img)

        self._goalLeftPostBase = [goalInfo[0],goalInfo[3]]
        self._goalRightPostBase = [goalInfo[1],goalInfo[3]]
        self._goalTopPost = [(goalInfo[1]+goalInfo[0])/2,goalInfo[2]]#Center of top post
        self._goalArea = goalInfo[4]
        self._updateGoalGridLocation(goalInfo[0],goalInfo[1],goalInfo[2],goalInfo[3])

    def _updateGoalGridLocation(self, l, r, t, b):
        """
        This function updates the value of BallGridLocation
        Returns the value of the square holding
        the x and y pixels in an imaginary grid, with the grid having
        16 squares (from 0->15). Will be called in updateBallCoordinates
        :param x:
        :param y:
        :return:
        """
        if (l != None and r!= None and t!= None and b!= None):

            left = l/80
            right = r/80
            top = t/60
            bot = b/60

            self._goalTopCenterGrid = [(left + right/2)][top]
            self._goalLeftBaseGrid = [left][bot]
            self._goalRightBaseGrid = [right][bot]
            self._goalCenterGrid = [(left+right)/2][(top+bot)/2]

    def _takeTopImage(self, xml):
        """
        Takes an image using the top camera
        and updates ball and goal information accordingly.
        Goal info is updated only when taking pictures from
        top camera
        """
        img = self._vision._takeImage(0)
        self._updateBallInfo(img, xml, 0)
        #self._updateGoalInfo(img)
        return img

    def _takeBottomImage(self, xml):
        """
        Takes an image using the top camera
        and updates ball information accordingly
        """
        img = self._vision._takeImage(1)
        self._updateBallInfo(img, xml, 1)
        return img

    def _ballIsVisible(self):
        """
        A boolean function to check if ball to the is visible or not
        :return: True if visible, False otherwise
        """
        if self._ballGridLocationTop == -1 and self._ballCoordinatesBottom == -1:
            return False
        else:
            return True

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
    time.sleep(3)
    xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'
    analyse = Analyse(IP, 9559)

    print(analyse._vision._videoProxy.getSubscribers())
    #analyse._vision._unsubscribeAll()

    naoimg = analyse._takeTopImage(xml)
    #naoimg2 = analyse._takeBottomImage(xml)
    cv2.imshow('naoimg',naoimg)


    print("distance to ball", analyse._distanceToBall)
    print("ball coordinates top", analyse._ballCoordinatesTop)

    analyse._vision._unsubscribeAll()
    print(analyse._vision._videoProxy.getSubscribers())

    cv2.waitKey()
    cv2.destroyAllWindows()