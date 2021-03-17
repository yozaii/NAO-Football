# -*- coding: utf-8 -*-
import sys

from naoqi import ALProxy
IP = "169.254.145.67"
PORT = 9559

# Create a proxy to ALMotion.
try:
    motionProxy = ALProxy("ALMotion", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e

try:
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

motionProxy.moveTo(1.0, 0.0, 0.0)


def shoot():
    """
    The robot shoot in the ball.
    """

def get_up():
    """
    Nao get up.
    """
   #motionProxy.moveInit()

def walk():
    """
    The robot walk.
    """
    #motionProxy.moveInit()
    #motionProxy.moveTo(0.5, 0, 0)

def turn():
    """
    The robot have to turn.
    """
def standby():
    """
    The robot stay and do nothing.
    """
    #postureProxy.stopMove()

def to_place():
    """
    The robot go to the willing position.
    """
def danse():
    """
    Make the robot danse.
    """