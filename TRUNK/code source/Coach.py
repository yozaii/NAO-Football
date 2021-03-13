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
        """
        return sqrt(pow(b.get_x() - a.get_x() ,2)+pow(b.get_y() - a.get_y() ,2))


oumar = Coach()
a = Point3D(4,1,3)
b = Point3D(5,9,2)

d = oumar.distance(a,b)

print(d)