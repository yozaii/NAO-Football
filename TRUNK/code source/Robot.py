#------------------------#
#     Classes Robot      #
#------------------------#
import threading
from naoqi import ALProxy
import Analyse
import Action
from .serveur.clientside import Client
from .Node import Point3D

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
        self.client = Client()
        self.__pos2 = None
        self.__pos3 = None
        self.__pos4 = None
        self.__pos5 = None


        # connection to the differentes modules
        motionProxy = connectProxy("ALMotion")
        postureProxy = connectProxy("ALRobotPosture")
        vision = NVis(ip, PORT)

        # talk with servor to know his role 
        

        # take his place for his role
        #moveTo(role.initPos)

    def connectionServer(self):
        """
        The client robot access to the server (have to be tested)
        """
        self.client.connection()
    
    def send_postition_to_team(self):
        """
        The client robot send his position to
        the rest of the team (have to be tested)
        """
        self.client.send_message(self.get_pos())

    def receive_position_of_team(self):
        """
        Receive the position of his teammate (have to be tested)
        (have to find a way to recup the position of each others robots)
        """
        while self.client.is_connected:
            thread_listening = threading.Thread(target=self.listening)
            thread_listening.start()
        
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
               self.__analyse._ballGridLocationBottom[1] != [3,1] and
               self.__analyse._ballGridLocationBottom[1] != [3,2]
        ):
            #An image is taken
            self.__analyse._takeBottomImage(xml)

            #If the ball is perceived towards the right
            if (self.__analyse._ballGridLocationBottom[1] == 3):
                #The robot looks and moves towards the ball
                Action.lookTowards(motionProxy, "Right")
                Action.turnBodyToHeadAngle(motionProxy)
                motionProxy.waitUntilMoveIsFinished()
                motionProxy.post.moveTowards(1.0,0.0,0.0)

            #if the ball is perceived towards the left
            elif (self.__analyse._ballGridLocationBottom[1] == 0):
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
        elif (self.__analyse._ballGridLocationBottom == [3,1] or
               self.__analyse._ballGridLocationBottom ==[3,2]
        ):
            return 1




