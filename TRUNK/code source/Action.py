# -*- coding: utf-8 -*-
import sys
import argparse
import math
import time
from naoqi import ALProxy
IP = "127.0.0.1"
#IP = "169.254.60.184"
PORT = 9559

def connect(module):
    """
    allows to connect the robot
    """
    # Create a proxy to ALMotion.
    try:
        return ALProxy(module, IP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e


def shoot(postureProxy, motionProxy):
    """
    #The robot shoot in the ball.
    """

    stiffnesses  = 1
    isAbsolute  = True

    # se baisse sur ses appuies
    appuie = ["LKneePitch","LAnklePitch","RKneePitch","RAnklePitch"]
    angleAppuie = [math.radians(14),math.radians(-14),math.radians(14),math.radians(-14)]
    timeListsAppuie = [1.0,1.0]

    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    names = ["LHipRoll","RHipRoll","RKneePitch","LKneePitch","LAnklePitch"]
    angleLists = [math.radians(17),math.radians(8),math.radians(80),math.radians(14),math.radians(-14)]
    timeLists = [1.0,1.0,1.1,1.2,1.3,1.3]
    

    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    time.sleep(1.5)
    motionProxy.moveInit()


def get_up():
    """
    Nao get up.
    """
    motionProxy.moveInit()
    motionProxy.goToPosture("StandInit", 0.4)

def walk(motionProxy):
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
def danse(postureProxy,motionProxy):
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
    # 5) Step backward & left with your right foot
    footStepsList.append([["RLeg"], [[-0.04, -0.1, 0.0]]])
    # 6)Step forward & right with your right foot
    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])
    # 7) Move your left foot to your right foot
    footStepsList.append([["LLeg"], [[0.00, 0.1, 0.0]]])
    # 8) Sidestep to the right with your right foot
    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])

    ###############################
    # Send Foot step
    ###############################
    stepFrequency = 0.8
    clearExisting = False
    nbStepDance = 2 # defined the number of cycle to make

    for j in range( nbStepDance ):
        for i in range( len(footStepsList) ):
            try:
                motionProxy.setFootStepsWithSpeed(
                    footStepsList[i][0],
                    footStepsList[i][1],
                    [stepFrequency],
                    clearExisting)
            except Exception, errorMsg:
                print str(errorMsg)
                print "This example is not allowed on this robot."
                exit()


    motionProxy.waitUntilMoveIsFinished()

    # Go to rest position
    motionProxy.rest()


motionProxy = connect("ALMotion")
postureProxy = connect("ALRobotPosture")

shoot(postureProxy, motionProxy)