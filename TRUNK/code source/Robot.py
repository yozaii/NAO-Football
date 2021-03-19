#------------------------#
#     Classes Robot      #
#------------------------#
from naoqi import ALProxy

class Robot:
    """ 
    class define every robot
    """
    pos = Point3D(0,0,0)

    def __init__(self,pos):
        self.__pos = pos

    def move(self):
            motionProxy.moveTo(1.0, 0.0, 0.0)
    
    def connexion(self,ip,port):
        """ 
        allows robot to connect to the server
        """

        try:
            motionProxy = ALProxy("ALMotion", ip, port)
        except Exception,e:
            print "Could not create proxy to ALMotion"
            print "Error was: ",e

    def get_pos(self):
        return self.__pos

    def set_pos(self,pos):
        self.__pos = pos