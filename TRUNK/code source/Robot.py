#------------------------#
#     Classes Robot      #
#------------------------#
from naoqi import ALProxy
import Analyse
import Action

class Robot:
    """ 
    class define every robot
    """
    PORT = 9559
    pos = Point3D(0,0,0)

    def __init__(self,pos,ip,role):
        self.__pos = pos
        self.__ip = ip
        self.__role = role
        self.__analyse = Analyse.Analyse(ip,PORT)


        # connection to the differentes modules
        motionProxy = connectProxy("ALMotion")
        postureProxy = connectProxy("ALRobotPosture")
        vision = NVis(ip, PORT)

        # talk with servor to know his role 
        

        # take his place for his role
        #moveTo(role.initPos)

    def connectProxy(self,ip,module):
        """
        allows to connect the robot
        """
        try:
            return ALProxy(module, ip, PORT)
        except Exception,e:
            print "Could not create proxy to ",module
            print "Error was: ",e

    def get_pos(self):
        return self.__pos

    def set_pos(self,pos):
        self.__pos = pos

    def IA(self):
        """
        is the decisions in game of the robot
        """

    def scanForBall(self):
        """
        The robot scans the field by looking around for
        the ball. Once the ball is found, it moves its
        body to face the ball
        """
        #While ball is not found
        while (self.__analyse._ballAreaTop == -1 && self.__analyse._ballAreaBottom == -1):
            Action.lookAround(motionProxy)
            self.__analyse._takeTopImage(xml)
            self.__analyse._takeBottomImage(xml)

        #The robot and head face the ball
        Action.turnBodyToHeadAngle(motionProxy)

    def moveToBall(self):
        """
        The robot moves towards the ball
        :return: exit state. If ball is lost (0) or if ball is at robots feet(1)
        """
        self.__analyse._takeBottomImage(xml)

        #While the ball is visible in the camera and it is not near the feet
        while (self.__analyse._ballAreaBottom != -1 and
               self.__analyse._ballGridLocationBottom !=13 and
               self.__analyse._ballGridLocationBottom !=14
        ):
            #An image is taken
            self.__analyse._takeBottomImage(xml)

            #If the ball is perceived towards the right
            if (self.__analyse._ballGridLocationBottom == 3 or
                self.__analyse._ballGridLocationBottom == 7 or
                self.__analyse._ballGridLocationBottom == 11 or
                self.__analyse._ballGridLocationBottom == 15

            ):
                #The robot looks and moves towards the ball
                Action.lookTowards(motionProxy, "Right")
                Action.turnBodyToHeadAngle(motionProxy)
                motionProxy.waitUntilMoveIsFinished()
                motionProxy.post.moveTowards(1.0,0.0,0.0)

            #if the ball is perceived towards the left
            elif (self.__analyse._ballGridLocationBottom == 0 or
                self.__analyse._ballGridLocationBottom == 4 or
                self.__analyse._ballGridLocationBottom == 8 or
                self.__analyse._ballGridLocationBottom == 12
            ):
                # The robot looks and moves towards the ball
                Action.lookTowards(motionProxy, "Left")
                Action.turnBodyToHeadAngle(motionProxy)
                motionProxy.waitUntilMoveIsFinished()
                motionProxy.post.moveTowards(1.0,0.0,0.0)

            #If the ball is perceived around the center
            else:
                motionProxy.post.moveTowards(1.0,0.0,0.0)

        motionProxy.stopMove()

        #If ball is lost return 0
        if (self.__analyse._ballAreaBottom != -1):
            return 0
        #If ball is at feet return 1
        elif (self.__analyse._ballGridLocationBottom ==13 or
               self.__analyse._ballGridLocationBottom ==14
        ):
            return 1




