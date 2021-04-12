#------------------------#
#    Enumeration/node    #
#------------------------#
from enum import Enum

class Point3D:
    """
    3d point
    Argument:
    x -- x coordonnee
    y -- y coordonnee
    z -- z coordonnee
    """
    def __init__(self,x,y,z):
        self.__x = x
        self.__y = y
        self.__z = z

    def distance(self,posE1,posE2):
        """
        allows to calculate the distance between two point3D
        Argument:
        posE1 -- Position (Point3D) of the element 1
        posE2 -- Position (Point3D) of the element 2
        """

        return sqrt(pow(posE2.get_x() - posE1.get_x() ,2) + pow(posE2.get_y() - posE1.get_y() ,2))

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_y(self, z):
        self.__z = z


class Role(Enum):
    """
    player role
    """
    __order__ = "GOAL RDEFENSE LDEFENSE RATTACKER LATTACKER MIDDLE"
    GOAL = (1,Point3D(0,-4,0))
    RDEFENSE = (2,Point3D(2,-3.35,0))
    LDEFENSE = (3,Point3D(-2,-3.35,0))
    RATTACKER = (4,Point3D(0.3,-3.35,0))
    LATTACKER = (5,Point3D(-0.3,-3.35,0),Point3D(-0.3,-1,0))
    MIDDLE = (6,Point3D(0.3,-3.35,0))


class Element(Enum):
    """
    Element of court
    """
    __order__ = "BALL ALLY ENEMY CAGES"
    BALL = 1
    ALLY = 2
    ENEMY = 3
    CAGES = 4

class Strategy(Enum):
    """
    game strategy
    """
    __order__ = "DEFAULT ULTRA_OFFENSE ULTRA_DEFENSE"
    DEFAULT = 1
    ULTRA_OFFENSE = 2
    ULTRA_DEFENSE = 3

class Phase(Enum):
    """
    game phase
    """
    __order__ = "Initial Set Playing Penalized Finished"
    Initial = 1
    Set = 2
    Ready = 3
    Playing = 4
    Penalized = 5
    Finished = 6

class AffineFunction:
    """
    Affine function
    Argument:
    a -- point of courbe
    b -- point of courbe
    """
    def __init__(self,a,b):
        self.__xa = a.get_x()
        self.__xb = b.get_x()

        self.__ya = a.get_y()
        self.__yb = b.get_y()

        self.__a = (self.__yb - self.__ya) / (self.__xb - self.__xa)
        self.__b = self.__ya - (self.__a * self.__xa)


    def bestFunction(self,f,g,h,i):
        """
        return the distance between two function
        Argument:
        f -- affine Function
        g -- affine Function
        h -- affine Function
        i -- affine Function
        """
        pf.set_y(f.get_y(0))
        pf.set_x(0)

        pg.set_y(f.get_y(0))
        pg.set_x(0)

        ph.set_y(f.get_y(0))
        ph.set_x(0)

        pi.set_y(f.get_y(0))
        pi.set_x(0)


        if distance(pf,pi) <= distance(pg,ph):
            return [g,h]
        else: return [f,i]


    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_x(self,y):
        return (y-self.__b) / self.__a

    def get_y(self,x):
        return self.__a*x + self.__b 

class PerimeterSquare:
    def __init__(self,pos):
        self.__pos = pos
        self.__topLeft.set_y(pos.get_y()+1)
        self.__topLeft.set_x(pos.get_x()-1)
        self.__topRight.set_y(pos.get_y()+1)
        self.__topRight.set_x(pos.get_x()+1)
        self.__botLeft.set_y(pos.get_y()-1)
        self.__botLeft.set_x(pos.get_x()-1)
        self.__botRight.set_y(pos.get_y()-1)
        self.__botRight.set_x(pos.get_x()+1)

    def get_topLeft(self):
        return self.__topLeft

    def get_topRight(self):
        return self.__topRight

    def get_botLeft(self):
        return self.__botLeft

    def get_botRight(self):
        return self.__botRight

if __name__ == "__main__":
    goal = Role.GOAL
    print goal[0], goal[1]
