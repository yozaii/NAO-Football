#------------------------#
#     Classes Robot      #
#------------------------#
from naoqi import ALProxy

class Robot:
    """ 
    class define every robot
    """
    def __init__(self):
    	# robot try to connect to the server
        pass
    	

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

robot = Robot()
robot.connexion("169.254.145.67",9559)