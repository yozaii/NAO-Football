from cv2 import cv2
import numpy as np
import math
import unittest

img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg', 6)
xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'

class ImageProcessing :

    def findBallRectangle (self, img, xmlfile):
        """
        Finds the ball in an image
            and sends back info
        :param img: the image to process
        :param xmlfile: xml file for CascadeClassifier
        :return : infolist
            infoList[0] = x coordinate of beginning of rectangle (topleft)
            infoList[1] = y coordinate of beginning of rectangle (topleft)
            infoList[2] = width of rectangle
            infoList[3] = length of rectangle
            infoList[4] = x of center of rectangle
            infoList[5] = y of center of rectangle
            infoList[6] = center of rectangle

        """
        #showing source image
        cv2.imshow('source',img)

        #the classifier from xml file
        ball_cascade = cv2.CascadeClassifier(xmlfile)

        #source img converted to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #detecting the ball
        balls = ball_cascade.detectMultiScale(gray, 1.3, 5)

        #filling in the rectangles in result image
        for (x, y, w, h) in balls:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

        #showing result image
        cv2.imshow('result', img)
        cv2.waitKey()
        cv2.destroyAllWindows()

        #returns coordinates in result image
        infoList = [None] * 7

        #x of topleft of rectangle
        infoList[0] = balls[0][0]
        #y of topleft of rectangle
        infoList[1] = balls[0][1]
        #rectangle width
        infoList[2] = balls[0][2]
        #rectangle height
        infoList[3] = balls[0][3]
        #x of rectangle center
        infoList[4] = balls[0][0] + balls[0][2]/2
        #y of rectangle center
        infoList[5] = balls[0][1] + balls[0][3]/2
        #area of rectangle
        infoList[6] = balls[0][2]*balls[0][3]

        return infoList

class TestImageProcessing(unittest.TestCase):

    """
    tests if the list returned by findBallRectangle returns
    a list of size 7
    """
    def testReturnFindBallRectangleSize(self):
        ImPr = ImageProcessing()
        self.assertEqual(len(ImPr.findBallRectangle(img, xml)), 7)

    def testRandom(self):
        self.assertEqual(1,1)

if __name__ == "__main__":
    #unittest.main()

    #Other tests below:
    dim = (320,240)
    output = cv2.resize(img, dim)
    print(output.shape)