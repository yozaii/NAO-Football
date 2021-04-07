from cv2 import cv2
import numpy as np
import math
import unittest

img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg', 6)
img2 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal2.jpg')
img3 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal3.jpg')


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

        #returns coordinates in result image
        infoList = [None] * 7

        if len(balls)>0:
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

        else:
            #x of topleft of rectangle
            infoList[0] = -1
            #y of topleft of rectangle
            infoList[1] = -1
            #rectangle width
            infoList[2] = -1
            #rectangle height
            infoList[3] = -1
            #x of rectangle center
            infoList[4] = -1
            #y of rectangle center
            infoList[5] = -1
            #area of rectangle
            infoList[6] = -1

        return infoList

    def findGoalRectangle(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray before", gray)
        cv2.medianBlur(gray, 3, gray)
        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        cv2.imshow('thresh',thresh)
        edges = cv2.Canny(thresh, 50, 150)
        cv2.imshow('canny', edges)
        lines, points = imPr.houghOnGray(edges, 50)
        res, houghVPoints = imPr.drawHoughLines(gray, lines, "Vertical")
        print(houghVPoints)
        cv2.imshow("res",res)
        minAndMax = imPr.findVerticalExtr(houghVPoints)
        print(minAndMax)
        x1 = minAndMax[0]
        x2 = minAndMax[1]
        cv2.rectangle(img, (x1, 0), (x2, 500), (255, 0, 0), 2)
        cv2.imshow("finally?", img)
        cv2.waitKey()


    def houghOnGray(self, img, pointThresh):
        """
        Performs houghLines on an image
        :param img: The grayscale image to be processed
        :param pointThresh: The threshhold of number of points in HougLines
        :return lines: The np array of hough lines
        :return npPoints : The np array of the hough line points
        """
        lines = cv2.HoughLines(img, 1, np.pi / 180, pointThresh)
        listPoints = []

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                listPoints.append([pt1, pt2])

        npPoints = np.array(listPoints)
        return lines, npPoints

    def drawHoughLines(self, img, lines, type):
        """
        :param img: The image to be processed
        :param lines: A set of hough lines
        :param type: "Vertical" or "Horizontal"
        :return res: The matrix with colored on houghlines
        :return points : An nparray of the points of the lines (Vertical or horizontal or all)
        """
        res = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        pointsList = []

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                [x1, y1] = pt1
                [x2, y2] = pt2
                if x1 != x2:
                    slope = (y2-y1)/(x2-x1)
                else:
                    slope = 9999
                if type == "Vertical" or type == "":
                    if math.fabs(slope) > 13:
                        cv2.line(res, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
                        pointsList.append([pt1, pt2])
                if type == "Horizontal" or type == "":
                    if math.fabs(slope) < 1:
                        cv2.line(res, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
                        pointsList.append([pt1, pt2])

        points = np.array(pointsList)
        return res, points

    def findVerticalExtr(self, points):
        """
        Finds the vertical lines extremities from a set of hough lines
        :param points: The points of the lines
        :return: the indices of the min and max vertical lines
        """
        min = 100000
        max = 0
        for i in range(points.shape[0]):
            y = (points[i][0][0] + points[i][1][0])/2
            if y<=min:
                min = y
            if y>=max:
                max = y

        return [min,max]

    def findHorizontalExtr(self, points):
        """
        Finds the horizontal lines extremities from a set of hough lines
        :param points: The points of the lines
        :return: the indices of the min and max horizontal lines
        """
        min = 100000
        max = 0
        for i in range(points.shape[0]):
            x = points[i][0][1]
            if x <= min:
                min = x
            if x >= max:
                max = x

        return [min, max]



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
    """
    imPr = ImageProcessing()
    imPr.findBallRectangle(img,xml)
    cv2.imshow('img',img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    """

    """
    imPr = ImageProcessing()
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray before", gray)
    cv2.medianBlur(gray, 3, gray)
    cv2.imshow("gray after blur", gray)
    ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh, 50, 150)
    cv2.imshow('thtresh', thresh)
    cv2.imshow('edges', edges)
    lines, points = imPr.houghOnGray(edges, 100)
    res, houghVPoints = imPr.drawHoughLines(gray, lines, "Vertical")
    print(houghVPoints)
    minAndMax = imPr.findVerticalExtr(houghVPoints)
    print(minAndMax)
    cv2.imshow("hough", res)
    cv2.waitKey()
    """
    img3 = cv2.resize(img3, (640,480))
    cv2.imshow('img3',img3)
    cv2.waitKey()
    imPr = ImageProcessing()
    imPr.findGoalRectangle(img3)

