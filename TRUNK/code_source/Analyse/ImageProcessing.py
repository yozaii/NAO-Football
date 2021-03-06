from cv2 import cv2
import numpy as np
import math
import unittest

img = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\1.jpg', 6)
img2 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal2.jpg')
img3 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal3.jpg')
img4 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal4.jpg')
img5 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal5.jpg')
img6 = cv2.imread('C:\\Users\\Youssef\\Desktop\\Robocup Images\\Goal6.jpg')




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
            infoList[6] = area of rectangle

        """
        #showing source image
        #cv2.imshow('source',img)

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
        #cv2.imshow('res',img)

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
        """
        Draws a rectangle over the goal
        :param img:
        :return: a list -> goalInfoList with
            goalInfoList[0] = Left post
            goalInfoList[1] = Right post
            goalInfoList[2] = Top post
            goalInfoList[3] = Base of goal
            goalInfoList[4] = Area of goal
        """
        blueFilterImg = self.keepBlue(img)
        #Converts image to gray
        gray = cv2.cvtColor(blueFilterImg, cv2.COLOR_BGR2GRAY)
        #Blurs noise
        cv2.medianBlur(gray, 3, gray)

        #Threshold to keep only dark-ish objects
        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        #Edges detection
        edges = cv2.Canny(thresh, 50, 150)

        #Hough transform and resulting horizontal / vertical lines
        lines, points = self.houghOnGray(edges, 30)
        res, houghVPoints, houghHPoints = self.drawHoughLines(gray, lines)

        #x coordinates of left and right posts
        leftAndRightPosts = self.findVerticalExtr(houghVPoints)

        #y coordinates of the top post
        topPost = self.findHorizontalTop(houghHPoints)
        x1 = leftAndRightPosts[0]
        x2 = leftAndRightPosts[1]
        y1 = topPost

        #width between the two vertical posts
        width = x2 - x1
        #length of the vertical posts is slightly shorter than horizontal post
        postLength = int(width * 0.8)
        y2 = y1 + postLength


        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        goalInfoList = [None] * 7

        goalInfoList[0] = x1 #Left post
        goalInfoList[1] = x2 #Right post
        goalInfoList[2] = y1 #Top post
        goalInfoList[3] = y2#Base of goal
        goalInfoList[4] = width * postLength#Area of rectangle

        return goalInfoList

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

    def drawHoughLines(self, img, lines):
        """
        :param img: The image to be processed
        :param lines: A set of hough lines
        :param type: "Vertical" or "Horizontal"
        :return res: The matrix with colored on houghlines
        :return vPoints : An nparray of the points of the vertical lines
        """
        res = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        vPointsList = []
        hPointsList = []
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
                    slope = float(y2-y1)/float(x2-x1)
                else:
                    slope = 9999
                #slope  of line = 13 is approx 85 degrees
                if math.fabs(slope) > 13:
                    cv2.line(res, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
                    vPointsList.append([pt1, pt2])
                if math.fabs(slope) < 0.1:
                    cv2.line(res, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
                    hPointsList.append([pt1, pt2])

        vPoints = np.array(vPointsList)
        hPoints = np.array(hPointsList)
        return res, vPoints, hPoints

    def findVerticalExtr(self, points):
        """
        Finds the vertical lines extremities from a set of hough lines
        :param points: The points of the lines
        :return: the x coordinates of the min and max vertical lines
        """
        min = 100000
        max = 0
        for i in range(points.shape[0]):
            x = (points[i][0][0] + points[i][1][0])/2
            if x<=min:
                min = x
            if x>=max:
                max = x

        return [min,max]

    def findHorizontalTop(self, points):
        """
        Finds the highest horizontal line in the image
        (Note that xy plane in opencv starts from the top,
        y increases as you go down)
        :param points: The points of the lines
        :return: the y coordinates of the top horizontal line
        """
        min = 10000
        for i in range(points.shape[0]):
            y = (points[i][0][1] + points[i][1][1])/2
            if y <= min:
                min = y

        return min

    def keepBlue(self, img):
        """
        Filters all colors other than blue
        """
        res = img.copy()
        for i in range(res.shape[0]):
            for j in range(res.shape[1]):
                b = res[i][j][0]
                g = res[i][j][1]
                r = res[i][j][2]
                if ((r > 50 or g > 100) or (b<30 and g>100)):
                    res[i][j][0] = 255
                    res[i][j][1] = 255
                    res[i][j][2] = 255

        return res


class TestImageProcessing(unittest.TestCase):

    """
    tests if the list returned by findBallRectangle returns
    a list of size 7
    """
    def testReturnFindBallRectangleSize(self):
        ImPr = ImageProcessing()
        self.assertEqual(len(ImPr.findBallRectangle(img, xml)), 7)

    def testFindBallRectangle(self):
        ImPr = ImageProcessing()
        im = img
        bList = ImPr.findBallRectangle(im, xml)

        #20 pixel margin of error for each except area (20*20 = 400)

        if bList[0] <= 471 and bList[0] >= 431: xTopLeft = True
        if bList[1] <= 372 and bList[1] >= 332: yTopLeft = True
        if bList[2] <= 78 and bList[2] >= 38: width = True
        if bList[3] <= 78 and bList[3] >= 38: height = True
        if bList[4] <= 500 and bList[4] >= 460: xCenter = True
        if bList[5] <= 401 and bList[5] >= 361: yCenter = True
        if bList[6] <= 3764 and bList[6] >= 2964: area = True
        [451, 352, 58, 58, 480, 381, 3364]

        bool1 = xTopLeft and yTopLeft and width and height
        bool2 = xCenter and yCenter and area
        boolAll = bool1 and bool2

        self.assertEqual(True, boolAll)

    def testKeepBlue(self):
        """
        Fails if there are non-blue or non-white pixels
        :return:
        """
        ImPr = ImageProcessing()
        im = ImPr.keepBlue(img)
        boolOnlyBlue = True
        bool1 = True
        bool2 = True
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                b = im[i][j][0]
                g = im[i][j][1]
                r = im[i][j][2]
                if (r == 255 and g == 255 and b!= 255):
                    bool1 = False
                if (r > 50 or g > 100) and (b<30):
                    bool2 = False
        boolOnlyBlue = bool1 and bool2
        self.assertEqual(True, boolOnlyBlue)

    def testFindVerticalExtr(self):

        ImPr = ImageProcessing()

        point1 = np.array([[200, 115], [40, 300]])
        point2 = np.array([[100, 100], [7, 45]])
        point3 = np.array([[470, 88], [90, 200]])
        point4 = np.array([[89, 153], [172, 233]])
        points = [point1, point2, point3, point4]
        pts = np.array(points)
        res = ImPr.findVerticalExtr(pts)
        bool1 = res[0] == 53
        bool2 = res[1] == 280
        boolAll = bool1 and bool2
        self.assertEqual(True, boolAll)

    def testFindHorizontalTop(self):
        ImPr = ImageProcessing()

        point1 = np.array([[200, 115], [40, 300]])
        point2 = np.array([[100, 100], [7, 45]])
        point3 = np.array([[470, 88], [90, 200]])
        point4 = np.array([[89, 153], [172, 233]])
        points = [point1, point2, point3, point4]
        pts = np.array(points)
        top = ImPr.findHorizontalTop(pts)
        boolTop = top == 72
        self.assertEqual(True, boolTop)

    def testGoalDetectionTwo(self):
        ImPr = ImageProcessing()
        boolLeft = False
        boolRight = False
        boolTop = False
        boolBot = False
        boolArea = False

        im2 = cv2.resize(img2, (320, 240))
        res = ImPr.findGoalRectangle(im2)

        if res[0]<=15 and res[0]>=0: boolLeft = True
        if res[1]<=330 and res[1]>=310: boolRight = True
        if res[2]<=67 and res[2]>=47: boolTop = True
        if res[3]<=319 and res[3]>=299: boolBot = True
        if res[4]<=79780 and res[4]>= 78980: boolArea = True

        boolAll = boolLeft and boolRight and boolTop and boolBot and boolArea
        self.assertEqual(True,boolAll)

    def testGoalDetectionThree(self):
        ImPr = ImageProcessing()
        boolLeft = False
        boolRight = False
        boolTop = False
        boolBot = False
        boolArea = False

        im3 = cv2.resize(img3, (320, 240))
        res = ImPr.findGoalRectangle(im3)

        if res[0] <= 53 and res[0] >= 33: boolLeft = True
        if res[1] <= 325 and res[1] >= 305: boolRight = True
        if res[2] <= 31 and res[2] >= 11: boolTop = True
        if res[3] <= 248 and res[3] >= 228: boolBot = True
        if res[4] <= 59424 and res[4] >= 58624: boolArea = True

        boolAll = boolLeft and boolRight and boolTop and boolBot and boolArea
        self.assertEqual(True, boolAll)

    def testGoalDetectionFour(self):
        ImPr = ImageProcessing()
        boolLeft = False
        boolRight = False
        boolTop = False
        boolBot = False
        boolArea = False

        im4 = cv2.resize(img4, (320, 240))
        res = ImPr.findGoalRectangle(im4)

        if res[0] <= 176 and res[0] >= 156: boolLeft = True
        if res[1] <= 283 and res[1] >= 263: boolRight = True
        if res[2] <= 33 and res[2] >= 13: boolTop = True
        if res[3] <= 118 and res[3] >= 90: boolBot = True
        if res[4] <= 9495 and res[4] >= 8695: boolArea = True

        boolAll = boolLeft and boolRight and boolTop and boolBot and boolArea
        self.assertEqual(True, boolAll)

    def testGoalDetectionFive(self):
        ImPr = ImageProcessing()
        boolLeft = False
        boolRight = False
        boolTop = False
        boolBot = False
        boolArea = False

        im5 = cv2.resize(img5, (320, 240))
        res = ImPr.findGoalRectangle(im5)

        if res[0] <= 49 and res[0] >= 29: boolLeft = True
        if res[1] <= 141 and res[1] >= 121: boolRight = True
        if res[2] <= 116 and res[2] >= 96: boolTop = True
        if res[3] <= 189 and res[3] >= 169: boolBot = True
        if res[4] <= 7116 and res[4] >= 6316: boolArea = True

        boolAll = boolLeft and boolRight and boolTop and boolBot and boolArea
        self.assertEqual(True, boolAll)

    def testGoalDetectionSix(self):
        ImPr = ImageProcessing()
        boolLeft = False
        boolRight = False
        boolTop = False
        boolBot = False
        boolArea = False

        im6 = cv2.resize(img6, (320, 240))
        res = ImPr.findGoalRectangle(im6)

        if res[0] <= 91 and res[0] >= 71: boolLeft = True
        if res[1] <= 181 and res[1] >= 161: boolRight = True
        if res[2] <= 23 and res[2] >= 3: boolTop = True
        if res[3] <= 95 and res[3] >= 75: boolBot = True
        if res[4] <= 6880 and res[4] >= 6080: boolArea = True

        boolAll = boolLeft and boolRight and boolTop and boolBot and boolArea
        self.assertEqual(True, boolAll)

if __name__ == "__main__":

    unittest.main()