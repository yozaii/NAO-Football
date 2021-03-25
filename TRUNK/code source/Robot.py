#------------------------#
#     Classes Robot      #
#------------------------#
from naoqi import ALProxy

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