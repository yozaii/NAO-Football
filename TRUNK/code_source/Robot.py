#-*- coding: utf-8 -*-
import sys
import threading
from naoqi import ALProxy
import Action as action
from Analyse.Analyse import *
from Node import *
import time

xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'

class Robot(threading.Thread):
    """ 
    class define every robot
    """
    PORT = 9559

    def __init__(self,ip,role,strat,coach):
        threading.Thread.__init__(self)
        self.arretthread = False
        self.coach = coach
        self.pos = None
        self.ip = ip
        self.role = role
        self.ready = False

        # connection to the differentes modules
        self.tpMotion = self.connectProxy("ALMotion")
        self.tpPosture = self.connectProxy("ALRobotPosture")
        self.tpLed = self.connectProxy("ALLeds")

        # booleane to confirm if every proxy are available
        self.running = self.tpMotion[0] and self.tpPosture[0] and self.tpLed[0]
        if self.running:
            self.motionProxy = self.tpMotion[1]
            self.postureProxy = self.tpPosture[1]
            self.ledProxy = self.tpLed[1]
            self.analyse = Analyse(self.ip,PORT)

    def stop(self):
        """
        stop threads
        """
        self.arretthread = True

    def trace(self, frame, event, arg):
        """
        force stoping
        """
        if event=='line':
            if self.arretthread:
                raise SystemExit()
        return self.trace

    def run(self):
        """
        run thread
        """
        if self.running:
            try:
                sys.settrace(self.trace)
                self.IA(Phase.Initial)
                self.IA(Phase.Ready)

                sys.settrace(None)
            except:
                sys.settrace(None)

    def connectProxy(self,module):
        """
        make a connection proxy to the robot
        """
        try:
            
            return True, ALProxy(module, self.ip, PORT)
        except Exception,e:
            print "Could not create proxy to ",module
            print "Error was: ",e
        return (False,)

    def get_pos(self):
        return self.pos

    def set_pos(self,pos):
        self.pos = pos

    def play(condition,x,y):
        """
        playing routine
        
        # we scan the ground to detect the ball
        if self.scanForBall():
            # if the ball is in the playing area according to the role and in the playing area
            if condition and self.coach.perimeterGround.perimeter(self.coach.posBall):
                # we move until we are near
                if self.moveToBall():
                    # if we are in the firing range and in the alignment of the cages
                    if self.coach.perimeterShoot.perimeter() and alignement():
                        # we shoot
                        action.shoot()
                    # otherwise if there is an obstacle
                    elif obstacle():
                        # we try to make a pass
                        if self.coach.passBall():
                            action.passTo(pos)
                        # otherwise we bypass
                        else:
                            action.contourne()
                    # otherwise we place ourselves in the perimeter and we align ourselves
                    else:
                        action.moveTo(self.coach.posCage)
                        action.turn(self.motionProxy,degree)
            else:
                action.moveTo(Point2D(x,y))
        """
        pass

    def IA(self,gamePhase):
        """
        decision per phase of robot
        """
        if gamePhase == Phase.Initial:
            # BLUE COLOR
            self.ledProxy.fadeListRGB('ChestLeds', [0x000000ff], [0])
            # declare his actual position as his origin/home (function)
            self.IA(Phase.Set)

        elif gamePhase == Phase.Set:
            # YELLOW COLOR
            self.ledProxy.fadeListRGB('ChestLeds', [0x00f5bb19], [0])
            if self.coach.kickoff:
                if self.role == Role.LATTACKER:
                    action.moveTo(Role[2])
                    self.scanForBall()
                else:
                    action.moveTo(Role[1])
            # turn to be in front of the enemy goal
            action.turn(self.motionProxy,degresOfTurn)
            while not self.ready:
                continue

        elif gamePhase == Phase.Ready:
            # wait sonor signal (function)
            self.IA(Phase.Playing)

        elif gamePhase == Phase.Playing:
            # GREEN COLOR
            self.ledProxy.fadeListRGB('ChestLeds', [0x0000ff00], [0])
            # according to the role
            if self.role == Role.LATTACKER:
                # if we have the kickoff
                if self.coach.kickoff:
                    action.shoot()
                while self.coach.timer.minute < 10:
                    #play((self.coach.posBall.get_y() > -0.75 and coach.posBall.get_x() < 0),-0.75,0)
                    break
                    
            elif self.role == Role.RATTACKER:
                while self.coach.timer.minute < 10:
                    #play((self.coach.posBall.get_y() > -0.75 and coach.posBall.get_x() > 0),0.75,0)
                    break
                
            elif self.role == Role.LDEFENSE:
                while self.coach.timer.minute < 10:
                    #play((self.coach.posBall.get_y() < -0.75 and coach.posBall.get_x() > 0),-0.75,-3)
                    break
                
            elif self.role == Role.RDEFENSE:
                while self.coach.timer.minute < 10:
                    #play((self.coach.posBall.get_y() < -0.75 and coach.posBall.get_x() > 0),0.75,-3)
                    break

            elif self.role == Role.GOAL:
                while self.coach.timer.minute < 10:
                    """
                    # if the ball comes into our camp, the robot moves according to it
                    if self.coach.posBall.get_y() > -2:
			            if self.coach.posBall.get_x() < 0:
				            action.moveTo(Point2D(-1,-4.2))
			            elif self.coach.posBall.get_() > 0:
				            action.moveTo(Point2D(1,-4.2))
                    # if it enters the perimeter of the keeper, he sits down to protect the cages
                    if self.coach.perimeterGardian.perimeter(self.coach.posBall):
                        action.defense(self.postureProxy,self.motionProxy,10)
                    """
                    break

        elif gamePhase == Phase.Penalized:
            # RED COLOR
            self.ledProxy.fadeListRGB('ChestLeds', [0x00FF0000], [0])
            time.sleep(40)
            self.IA(Phase.Playing)

        elif gamePhase == Phase.Finished:
            self.ledProxy.fadeListRGB('ChestLeds', [0x0000000], [0])
            self.stop()

    def scanForBall(self):
        """
        The robot scans the field by looking around for
        the ball. Once the ball is found, it moves its
        body to face the ball
        """
        self._analyse._takeTopImage(xml)
        self._analyse._takeBottomImage(xml)
        self._motionProxy.angleInterpolation("HeadPitch", [0.1], [1.0], True)
        self._motionProxy.setStiffnesses("HeadPitch", 1)
        t1 = time.time()
        t2 = time.time() - t1
        #While ball is not found
        while (self._analyse._ballAreaTop == -1 and self._analyse._ballAreaBottom == -1 and t2 <12):
            self._analyse._takeTopImage(xml)
            self._analyse._takeBottomImage(xml)
            Action.lookAround(self._motionProxy)
            t2 = time.time() - t1

        #The robot and head face the ball
        Action.turnBodyToHeadAngle(self._motionProxy)

    def moveToBall(self):
        """
        The robot moves towards the ball
        :return: exit state. If ball is lost (0) or if ball is at robots feet(1)
        """
        x = 0.6
        y = 0.0
        z = 0.0

        #Fix head angle
        self._motionProxy.angleInterpolation("HeadYaw",[0.0], [1.0],True)
        self._motionProxy.angleInterpolation("HeadPitch", [0.1], [1.0], True)
        self._motionProxy.setStiffnesses("HeadPitch", 0)

        self._analyse._takeTopImage(xml)
        self._analyse._takeBottomImage(xml)
        #While the ball is visible in the camera and it is not near the feet
        while ((self._analyse._ballAreaBottom != -1 or self._analyse._ballAreaTop != -1) and
               (self._analyse._ballGridLocationBottom[0] != [3] and
               self._analyse._ballGridLocationBottom[1] != [1])

        ):
            self._motionProxy.post.move(x, y, z)
            #An image is taken
            self._analyse._takeBottomImage(xml)
            self._analyse._takeTopImage(xml)

            #If the ball is perceived towards the right
            if (self._analyse._ballGridLocationBottom[1] == 3 or
                self._analyse._ballGridLocationTop[1] == 3
            ):
                #The robot looks and moves towards the ball
                x = 0
                z = 0.2


            #if the ball is perceived towards the left
            elif (self._analyse._ballGridLocationBottom[1] == 0 or
                  self._analyse._ballGridLocationTop[1] == 0
            ):
                # The robot looks and moves towards the
                x = 0
                z = -0.2


            #If the ball is perceived around the center
            else:
                if (x<1):
                    x = x + 0.2
                z = 0.0

        self._motionProxy.stopMove()
        self._motionProxy.move(0.0,0.0,0.0)

        #If ball is lost return 0
        if (self._analyse._ballAreaBottom != -1):
            return False
        #If ball is at feet return 1
        elif (self._analyse._ballGridLocationBottom == [3,1] or
               self._analyse._ballGridLocationBottom ==[3,2]
        ):
            return True

#******************     TEST Robot    *********************#

if __name__ == "__main__":


    robot = Robot("faux",'role')
    #robot.moveToBall()
    #ret = robot.moveToBall()
    #print(ret)
    #robot._analyse._vision._unsubscribeAll()

    #Action.turnBodyToHeadAngle(robot._motionProxy)

