#------------------------#
#     Classes Robot      #
#------------------------#
import sys
from threading import Thread
from naoqi import ALProxy
import Action as action
#from serveur.clientside import Client
from Analyse.Analyse import *
from Node import *

xml = 'C:\\Users\\Youssef\\Downloads\\ball_cascade.xml'

class Robot(Thread):
    """ 
    class define every robot
    """
    PORT = 9559

    def __init__(self,ip,role,strat,coach):
        Thread.__init__(self)
        self.__coach = coach
        self.__pos = None
        self.__ip = ip
        self.__role = role
        
        # connection to the differentes modules
        self.tpMotion = self.connectProxy("ALMotion")
        self.tpPosture = self.connectProxy("ALRobotPosture")

        self.running = self.tpMotion[0] and self.tpPosture[0]
        if self.running:
            self._motionProxy = self.tpMotion[1]
            self._postureProxy = self.tpPosture[1]
            self._analyse = Analyse(self.__ip,PORT)
            

    def stop(self):
        self.running = False

    def run(self):
        """wait 10 sec"""
        while self.running:
            action.danse(self._postureProxy,self._motionProxy)
            print "debut du robot: ", self.__ip 
            time.sleep(10)
            print "fin du robot: ", self.__ip
            self.stop()

    def connectionServer(self):
        """
        The client robot access to the server (have to be tested)
        """
        pass
        #self.client.connection()

    def send_postition_to_team(self):
        """
        The client robot send his position to
        the rest of the team (have to be tested)
        """
        pass
        #self.client.send_message(self.get_pos())

    def receive_position_of_team(self):
        """
        Receive the position of his teammate (have to be tested)
        (have to find a way to recup the position of each others robots)
        """
        pass
        #while self.client.is_connected:
         #   thread_listening = threading.Thread(target=self.listening)
          #  thread_listening.start()

    def connectProxy(self,module):
        """
        allows to connect the robot
        """
        try:
            
            return True, ALProxy(module, self.__ip, PORT)
        except Exception,e:
            print "Could not create proxy to ",module
            print "Error was: ",e
        return (False,)

    def get_pos(self):
        return self.__pos

    def set_pos(self,pos):
        self.__pos = pos

    def IA(self,gamePhase):
        """
        is the decisions in game of the robot
        """
        if gamePhase == Phase.Initial:
            # declare his actual position as his origin/home (function)
            action.posturePlay()
            # wait a sound signal
            self.IA(Phase.Set)

        elif gamePhase == Phase.Set:
            # engage the game or analyse where is the ball
            # when NAO detect the ball the closest robot move to it
            # verify if NAO get the ball
            pass

        elif gamePhase == Phase.:
            pass

        elif gamePhase == Phase.:
            pass

        elif gamePhase == Phase.:
            self.stop()


    def scanForBall(self):
        """
        The robot scans the field by looking around for
        the ball. Once the ball is found, it moves its
        body to face the ball
        """
        self._analyse._takeTopImage(xml)
        self._analyse._takeBottomImage(xml)
        #While ball is not found
        while (self._analyse._ballAreaTop == -1 and self._analyse._ballAreaBottom == -1):
            Action.lookAround(self._motionProxy)
            self._analyse._takeTopImage(xml)
            self._analyse._takeBottomImage(xml)

        #The robot and head face the ball
        Action.turnBodyToHeadAngle(self._motionProxy)

    def moveToBall(self):
        """
        The robot moves towards the ball
        :return: exit state. If ball is lost (0) or if ball is at robots feet(1)
        """
        x = 0.5
        y = 0.0
        z = 0.0
        self._analyse._takeTopImage(xml)

        #While the ball is visible in the camera and it is not near the feet
        while ((self._analyse._ballAreaBottom != -1 or self._analyse._ballAreaTop != 1) and
               self._analyse._ballGridLocationBottom[1] != [3,1] and
               self._analyse._ballGridLocationBottom[1] != [3,2]
        ):
            #An image is taken
            self._analyse._takeBottomImage(xml)

            #If the ball is perceived towards the right
            if (self._analyse._ballGridLocationBottom[1] == 3 or
                self._analyse._ballGridLocationTop[1] == 3
            ):
                #The robot looks and moves towards the ball
                x = x - 0.2
                z = z + 0.2
                self._motionProxy.post.move(x,y,z)

            #if the ball is perceived towards the left
            elif (self._analyse._ballGridLocationBottom[1] == 0 or
                  self._analyse._ballGridLocationTop[1] == 3
            ):
                # The robot looks and moves towards the ball
                x = x - 0.2
                z = z - 0.2
                self._motionProxy.post.move(x,y,z)

            #If the ball is perceived around the center
            else:
                x = x + 0.2
                z = 0.0
                self._motionProxy.post.move(x,y,z)

        self._motionProxy.stopMove()

        #If ball is lost return 0
        if (self._analyse._ballAreaBottom != -1):
            return 0
        #If ball is at feet return 1
        elif (self._analyse._ballGridLocationBottom == [3,1] or
               self._analyse._ballGridLocationBottom ==[3,2]
        ):
            return 1


if __name__ == "__main__":


    robot = Robot("faux",'role')
    #robot.moveToBall()
    #ret = robot.moveToBall()
    #print(ret)
    #robot._analyse._vision._unsubscribeAll()

    #Action.turnBodyToHeadAngle(robot._motionProxy)

