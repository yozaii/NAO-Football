#------------------------#
#     Classes Coach      #
#------------------------#

from math import *
from Node import *
class Coach:
    """ 
    class who dictates who need to do what and making decision about the game
    """
    def __init__(self):
        pass

    def distance(self,a,b):
        """
        allows to calculate the distance between two point3D
        Argument:
        a -- Position (Point3D) of the element A
        b -- Position (Point3D) of the element B
        """
        return sqrt(pow(b.get_x() - a.get_x() ,2) + pow(b.get_y() - a.get_y() ,2))

    def isPresent(self, f,g,c):
        """
        allows to know if a point3D is between two others point3D
        Argument:
        f -- Function which corresponds to one of the external lines between two robots
        g -- Function which corresponds to one of the external lines between two robots
        c -- Position (Point3D) of the element C
        """
        
        # we verify if the point C is between the function f and g
        if c.get_y() <= f.get_y(c.get_x()) and c.get_y() >= g.get_y(c.get_x()) and c.get_x() <= f.get_x(c.get_y()) and c.get_x() >= g.get_x(c.get_y()):
            return true
        else:
            return false