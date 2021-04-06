#------------------------#
#     Classes Coach      #
#------------------------#
# -*- coding: utf-8 -*-
#pyuic5 -x interface.ui -o interface.pyw

import math
import random
from Node import *
import Robot as ROBOT

class Coach:
    """ 
    class who dictates who need to do what and making decision about the game
    Argument:
    Variable:
    """
    def __init__(self):

        self.__listeRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
        self.__listIp = ["127.0.0.1","127.0.0.2","172.96.26.32","172.96.26.33","172.96.26.34","172.96.26.35","172.96.26.36"]
        self.__strat = Strategy.DEFAULT
        self.listRobot = []

    def createPlayer(self,ip,role):
        """
        create an instance of robot
        """
        robot = ROBOT.Robot(ip,role,self.__strat,self)
        self.listRobot.append(robot)

        robot.start()
        return robot.running


    def stopThreads(self):
        for robot in self.listRobot:
            robot.stop()

    def stopThread(self,robot):
            robot.stop()


    def isPresent(self,f,g,posElement):
        """
        allows to know if a point3D is between two others point3D
        Argument:
        f -- Function which corresponds to one of the external lines between two robots
        g -- Function which corresponds to one of the external lines between two robots
        posElement -- Position (Point3D) of the element posElement
        """
        # determinate the f and g to the function isPresent
        if f.get_y(posElement.get_x()) >= g.get_y(posElement.get_x()):
            self.f = f
            self.g = g
        
        else:
            self.f = g
            self.g = f

        # determinate the case
        if self.f.get_x(posElement.get_y()) >= self.g.get_x(posElement.get_y()):
            yCase = posElement.get_y() <= self.f.get_y(posElement.get_x()) and posElement.get_y() >= self.g.get_y(posElement.get_x())
            xCase = posElement.get_x() <= self.f.get_x(posElement.get_y()) and posElement.get_x() >= self.g.get_x(posElement.get_y())
        else:
            yCase = posElement.get_y() <= self.f.get_y(posElement.get_x()) and posElement.get_y() >= self.g.get_y(posElement.get_x())
            xCase = posElement.get_x() >= self.f.get_x(posElement.get_y()) and posElement.get_x() <= self.g.get_x(posElement.get_y())

        horizontalCase = posElement.get_x() == self.f.get_x(posElement.get_y()) and posElement.get_x() == self.g.get_x(posElement.get_y())
        verticalCase = posElement.get_y() == self.f.get_y(posElement.get_x()) and posElement.get_y() == self.g.get_y(posElement.get_x())
        
        

        if horizontalCase and yCase:
            return True
        elif verticalCase and xCase:
            return True
        elif xCase and yCase:
            return True
        else: return False

    def theClosest(self,posElement,listRobot):
        """
        allows to know which ally is closest to a point
        Argument:
        posElement -- position of an element
        listRobot -- the list of allied or enemy robot
        """

        index = 0
        distanceMin = math.inf

        for i in range(5):
            distance = posElement.distance(posElement,listRobot[i].get_pos())
            if distance < distanceMin:
                distanceMin = distance
                index = i

        return listRobot[index]

    def ballPass(self,listEnemyRobot,listAllyRobot,posBall,robotPasser):
        """
        allows to make a good pass
        listEnemyRobot -- the list of enemy robot
        """
        listAllyRobot.remove(robotPasser)
        perimeterBall = PerimeterSquare(posBall)

        for i in range(5):
            perimeterRobot = PerimeterSquare(listAllyRobot[i].get_pos())
            f = AffineFunction(perimeterBall.get_topLeft(),perimeterRobot.get_topLeft())
            g = AffineFunction(perimeterBall.get_topRight(),perimeterRobot.get_topRight())
            h = AffineFunction(perimeterBall.get_botLeft(),perimeterRobot.get_botLeft())
            i = AffineFunction(perimeterBall.get_botRight(),perimeterRobot.get_botRight())
            listFunction = bestFunction(f,g,h,i)
            # boucle pour les ennemies
            for j in range(5):
                if isPresent(listFun[0],listFun[1],listEnemyRobot[j]):
                    break;
            

        # must return list of robot that i can pass the ball
    
    def get_listRole(self):
        return self.__listeRole

    def get_strat(self):
        return self.__strat

    def get_listIp(self):
        return self.__listIp


#******************     TEST Coach/Node    *********************#

import unittest
class test(unittest.TestCase):

    def setUp(self):
        self.oumar = Coach()
        self.posElement = Point3D(1,2,0)
        # case 7-3
        self.f = AffineFunction(Point3D(-1,-2,0),Point3D(1,4,0))
        self.g = AffineFunction(Point3D(1,-3,0),Point3D(3,2,0))
        # case 1-5
        self.h = AffineFunction(Point3D(-3,2,0),Point3D(3,-2,0))
        self.i = AffineFunction(Point3D(-1,4,0),Point3D(5,0,0))

    def testIsPresent1(self):
        """
        test the function isPresent with case 7-3
        """
        self.assertTrue(self.oumar.isPresent(self.f,self.g,self.posElement))

    def testIsPresent2(self):
        """
        test the function isPresent with case 1-5
        """
        self.assertTrue(self.oumar.isPresent(self.i,self.h,self.posElement))

    def testAffineFunction1(self):
        """
        test the a on: ax +b
        """
        self.assertEqual(self.f.get_a(),3)

    def testAffineFunction2(self):
        """
        test the b on: ax +b
        """
        self.assertEqual(self.f.get_b(),1)



def testDistribRole(oumar):
    """
    test if all role are distributed
    """

    print("test of dirstribRole() function")
    for i in range(6):
        oumar.distribRole()
    if len(oumar.get_listRole()) == 0:
        print "success"
    else:
        print "failure"


if __name__ == '__main__':
    testDistribRole(Coach())
    unittest.main()
    
