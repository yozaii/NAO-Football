#------------------------#
#     Classes Robot      #
#------------------------#
import sys
import threading
from naoqi import ALProxy
import Action as action
#from serveur.clientside import Client
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
        self._stopevent = threading.Event( )
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
        self.running = False
        self._stopevent.set()
        

    def run(self):
        while self.running and not self._stopevent.isSet():
            self.IA(Phase.Initial)
            self.IA(Phase.Ready)
            self._stopevent.wait(2.0)
            

    def connectProxy(self,module):
        """
        allows to connect the robot
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

    def IA(self,gamePhase):
        """
        is the decisions in game of the robot
        """
        if gamePhase == Phase.Initial:
            # BLUE COLOR
            print "robot initial"
            #names = ["ChestBoard/Led/Blue/Actuator/Value"]
            #self.ledProxy.createGroup("MyGroup",names)
            #self.ledProxy.on("MyGroup")
            # declare his actual position as his origin/home (function)
            #action.posturePlay()
            self.IA(Phase.Set)

        elif gamePhase == Phase.Set:
            # YELLOW COLOR
            print "robot set"
            if self.coach.kickoff:
                if self.role == Role.LATTACKER:
                    pass
                    #action.moveTo(Role[2])
                    #self.scanForBall()
                else:
                    pass
                    #action.moveTo(Role[1])
            # turn to be in front of the enemy goal
            #action.turn(self.motionProxy,50)
            while not self.ready:
                continue

        elif gamePhase == Phase.Ready:
            print "robot ready"
            while True:
                break
            self.IA(Phase.Playing)

        elif gamePhase == Phase.Playing:
            # GREEN COLOR
            print "robot playing"
            if self.coach.kickoff:
                if self.role == Role.LATTACKER:
                    print "attaque"
                    #action.shoot()

                elif self.role == Role.GOAL:
                    print "goal"
                    #self.scanForBall()
                    # if posBall.get_y()<0

        elif gamePhase == Phase.Penalized:
            print "penalized"
            # RED COLOR
            time.sleep(40)
            self.IA(Phase.Playing)

        elif gamePhase == Phase.Finished:
            self.stop()

        self._stopevent.wait(2.0)

    def scanForBall(self):
        """
        The robot scans the field by looking around for
        the ball. Once the ball is found, it moves its
        body to face the ball
        """
        self.analyse._takeTopImage(xml)
        self.analyse._takeBottomImage(xml)
        #While ball is not found
        while (self.analyse._ballAreaTop == -1 and self.analyse._ballAreaBottom == -1):
            Action.lookAround(self.motionProxy)
            self.analyse._takeTopImage(xml)
            self.analyse._takeBottomImage(xml)

        #The robot and head face the ball
        Action.turnBodyToHeadAngle(self.motionProxy)

    def moveToBall(self):
        """
        The robot moves towards the ball
        :return: exit state. If ball is lost (0) or if ball is at robots feet(1)
        """
        x = 0.5
        y = 0.0
        z = 0.0
        self.analyse._takeTopImage(xml)

        #While the ball is visible in the camera and it is not near the feet
        while ((self.analyse._ballAreaBottom != -1 or self.analyse._ballAreaTop != 1) and
               self.analyse._ballGridLocationBottom[1] != [3,1] and
               self.analyse._ballGridLocationBottom[1] != [3,2]
        ):
            #An image is taken
            self.analyse._takeBottomImage(xml)

            #If the ball is perceived towards the right
            if (self.analyse._ballGridLocationBottom[1] == 3 or
                self.analyse._ballGridLocationTop[1] == 3
            ):
                #The robot looks and moves towards the ball
                x = x - 0.2
                z = z + 0.2
                self._motionProxy.post.move(x,y,z)

            #if the ball is perceived towards the left
            elif (self.analyse._ballGridLocationBottom[1] == 0 or
                  self.analyse._ballGridLocationTop[1] == 3
            ):
                # The robot looks and moves towards the ball
                x = x - 0.2
                z = z - 0.2
                self.motionProxy.post.move(x,y,z)

            #If the ball is perceived around the center
            else:
                x = x + 0.2
                z = 0.0
                self.motionProxy.post.move(x,y,z)

        self.motionProxy.stopMove()

        #If ball is lost return 0
        if (self.analyse._ballAreaBottom != -1):
            return 0
        #If ball is at feet return 1
        elif (self.analyse._ballGridLocationBottom == [3,1] or
               self.analyse._ballGridLocationBottom ==[3,2]
        ):
            return 1


if __name__ == "__main__":


    robot = Robot("faux",'role')
    #robot.moveToBall()
    #ret = robot.moveToBall()
    #print(ret)
    #robot._analyse._vision._unsubscribeAll()

    #Action.turnBodyToHeadAngle(robot._motionProxy)

