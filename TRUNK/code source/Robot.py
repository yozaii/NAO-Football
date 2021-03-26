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
        while (self.__analyse._ballArea == -1):
            Action.lookAround(motionProxy)
            self.__analyse._takeTopImage(xml)

        #Once the ball is found we stop the head from moving
        motionProxy.angleInterpolation("HeadYaw",[0.0],[1.0], False)

        #We get the angle of the head
        angle = motionProxy.getAngles("HeadYaw", False)

        #We move the body and face to face the ball
        motionProxy.post.moveTo(0.0, 0.0, angle[0])
        motionProxy.angleInterpolation("HeadYaw", [0.0], [1.0], True)



