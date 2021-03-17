# -*- coding: utf-8 -*-
import sys
import argparse
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

try:
    talkProxy = ALProxy("ALTextToSpeech",IP,PORT)
except Exception, e:
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ", e    

motionProxy.wakeUp()
talkProxy.setLanguage("French")
talkProxy.say("Bon, c'est partie.")

def shoot():
    """
    The robot shoot in the ball.
    """

def get_up():
    """
    Nao get up.
    """
   motionProxy.moveInit()
   motionProxy.goToPosture("StandInit", 0.4)

def walk():
    """
    The robot walk.
    """
    motionProxy.moveInit()
    motionProxy.moveTo(0.5, 0, 0)

def turn():
    """
    The robot have to turn.
    """
def standby():
    """
    The robot stay and do nothing.
    """
    postureProxy.stopMove()

def to_place():
    """
    The robot go to the willing position.
    """
def danse():
    """
    Make the robot danse.
    """
    postureProxy.goToPosture("StandInit", 0.5)
    footStepsList = [] 
    # 1) Step forward with your left foot
    footStepsList.append([["LLeg"], [[0.06, 0.1, 0.0]]])
    # 2) Sidestep to the left with your left foot
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])
    # 3) Move your right foot to your left foot
    footStepsList.append([["RLeg"], [[0.00, -0.1, 0.0]]])
    # 4) Sidestep to the left with your left foot
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])