#------------------------#
#    Enumeration/node    #
#------------------------#
from enum import Enum


class Role(Enum):
    """
    player role
    """
    GOAL = 1
    RDEFENSE = 2
    LDEFENSE = 3
    RATTACKER = 4
    LATTACKER = 5
    MIDDLE = 6


class Element(Enum):
    """
    Element of court
    """
    BALL = 1
    ALLY = 2
    ENEMY = 3
    CAGES = 4

class Strategy(Enum):
    """
    game strategy
    """
    DEFAULT = 1
    ULTRA_OFFENSE = 2
    ULTRA_DEFENSE = 3

class Point3D:
    """
    3d point
    Argument:
    x --
    y -- 
    z -- 
    """
    def __init__(self,x,y,z):
        self.__x = x
        self.__y = y
        self.__z = z

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

class AffineFunction:
    """
    Affine function
    Argument:
    a -- director coefficient
    b -- ordered at the origin
    """
    def __init__(self,a,b)
        self.__xa = a.get_x()
        self.__xb = b.get_x()

        self.__ya = a.get_y()
        self.__yb = b.get_y()

        self.__a = (self.__yb - self.__ya) / (self.__xb - self.__xa)
        self.__b = self.__ya - (self.__a * self.__xa)

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_x(self,y):
        return (y-self.__b) / self.__a

    def get_y(self,x):
        return self.__a*x + self.__b 

