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


class Point3D:
    """
    point 3d
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