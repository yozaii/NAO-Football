# -*- coding: utf-8 -*-

import math
import random
from Node import *
import Robot as ROBOT
import threading
import time
from Interface.interface import Ui_MainWindow

class Timer(threading.Thread):
    """
    timer of the soccer game
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.sec = 0
        self.minute = 0
        self.running = True

    def setup(self,ui):
        self.ui = ui

    def run(self):
        while self.running:
            if self.sec == 59:
                self.minute += 1
                self.sec = 0
                
            else:
                self.sec +=1
            time.sleep(1)
            self.ui.time.setText("Time: "+ str(self.minute) +":"+str(self.sec))

    def stop(self):
        self.running = False

    def reset(self):
        self.minute = 0
        self.sec = 0


class Coach:
    """ 
    class who dictates who need to do what and making decision about the game
    """
    def __init__(self):

        self.listeRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
        self.listIp = ["127.0.0.1","172.27.96.32","172.27.96.33","172.27.96.34","172.27.96.35","172.27.96.36"]
        self.strat = Strategy.DEFAULT
        self.listRobot = []
        self.posBall = Point2D(0,0)
        self.kickoff = None
        self.timer = Timer()
        self.posCageAdverse = Point2D(0,4.5)
        self.posCageSelf = Point2D(0,-4.5)
        self.perimeterShoot = PerimeterSquare(self.posCageAdverse,2,None,None,None,None)
        self.perimeterGardian = PerimeterSquare(self.posCageAdverse,2,None,None,None,None)
        self.perimeterGround = PerimeterSquare(0,None,Point2D(-3,4.5),Point2D(3,4.5),Point2D(-3,-4.5),Point2D(3,-4.5))

    def createPlayer(self,ip,role):
        """
        create an instance of robot
        """
        # give role
        if role == "GOAL":
            robot = ROBOT.Robot(ip,Role.GOAL,self.strat,self)
        elif role == "RDEFENSE":
            robot = ROBOT.Robot(ip,Role.RDEFENSE,self.strat,self)
        elif role == "LDEFENSE":
            robot = ROBOT.Robot(ip,Role.LDEFENSE,self.strat,self)
        elif role == "RATTACKER":
            robot = ROBOT.Robot(ip,Role.RATTACKER,self.strat,self)
        elif role == "LATTACKER":
            robot = ROBOT.Robot(ip,Role.LATTACKER,self.strat,self)
        elif role == "MIDDLE":
            robot = ROBOT.Robot(ip,Role.MIDDLE,self.strat,self)
        # add thread to the listRobot
        self.listRobot.append(robot)
        # start thread
        robot.start()
        return robot.running

    def ready(self):
        """
        make ready all robots on list
        """
        for robot in self.listRobot:
            robot.ready = True

    def recoverPosBall(self,distance,robot):
        """
        allows to recover the better posBall among list of pos
        """
        mini = math.inf
        for robot in self.listRobot:
            tpl = (robot,robot.distance)
            listDistance.append(tpl)
            if robot.distance >= 0:
                mini = min(mini,robot.distance)

        for tpl in listDistance:
            if mini == tpl[1]:
                self.posBall = tpl[0].posBall

    def stopThreads(self):
        """
        stop all threads
        """
        for robot in self.listRobot:
            robot.stop()
        self.timer.stop()

    def stopThread(self,ip):
        """
        stop a robot threads
        Argument:
        ip -- ip of robot who must stop
        """
        for robot in self.listRobot:
            if ip == robot.ip:
                robot.stop()
                self.listRobot.remove(robot)
                return True
            else:
                return False
        
    def isPresent(self,f,g,posElement):
        """
        allows to know if a point2D is between two others point3D
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
    
    def get_listRole(self):
        return self.__listeRole

    def get_strat(self):
        return self.strat

    def get_listIp(self):
        return self.listIp

    def set_kickoff(self,kickoff):
        self.kickoff = kickoff

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

if __name__ == '__main__':
    unittest.main()
    
