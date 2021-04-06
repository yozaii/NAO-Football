# -*- coding: utf-8 -*-
import qi
import argparse
import sys
import time
import math
from naoqi import ALProxy
IP = "127.0.0.1"
#IP = "172.27.96.33"
#IP = "169.254.199.241"
PORT = 9559

def connect(module):
    """
    allows to connect the robot
    Create a proxy to ALMotion and ALRobotPosture.
    """
    try:
        return ALProxy(module, IP, PORT)
    except Exception,e:
        print "Could not create proxy"
        print "Error was: ",e

def RobotFellRecently( eventName, hasFallen, subscriberIdentifier):
    print hasFallen
    
def shoot(postureProxy, motionProxy):
    """
    #The robot shoots in the ball.
    """

    stiffnesses  = 1
    isAbsolute  = False
    #here the robot puts its foot back
    names = ["LHipRoll","RHipPitch"]
    angleLists = [math.radians(5),math.radians(20.3)]
    timeLists = [2.0,2.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    # the robot shoots
    names = ["RKneePitch","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(15),math.radians(-30),math.radians(-6)]
    timeLists = [0.8,0.6,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    postureProxy.goToPosture("StandInit", 2)

def simpleShoot(postureProxy, motionProxy):
    """
    this function is a the movement of a little shoot for Nao
    """
    postureProxy.goToPosture("StandInit", 5)
    stiffnesses  = 1
    isAbsolute  = False
    names = ["RKneePitch","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(15),math.radians(-20),math.radians(-6)]
    timeLists = [0.8,0.6,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    postureProxy.goToPosture("StandInit", 2)

def lSideShoot(postureProxy, motionProxy):
    postureProxy.goToPosture("StandInit", 2)
    footStepsList = [] 
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])
    footStepsList.append([["LLeg"], [[0.00, -0.16, 0.0]]])
    stepFrequency = 1
    clearExisting = False
    for j in range( 1 ):
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
    postureProxy.goToPosture("StandInit", 2)   
    

def rSideShoot(postureProxy, motionProxy):
    postureProxy.goToPosture("StandInit", 2)
    footStepsList = [] 
    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])
    footStepsList.append([["RLeg"], [[0.00, 0.16, 0.0]]])
    stepFrequency = 1
    clearExisting = False
    for j in range(1):
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
    postureProxy.goToPosture("StandInit", 2)

def defense(postureProxy, motionProxy):
    postureProxy.goToPosture("Sit", 5)
    time.sleep(1)
    postureProxy.goToPosture("StandInit", 5)

def postureDeJeu(postureProxy, motionProxy):
    """
    The posture that should have the robot.
    """
    motionProxy.moveInit()
    stiffnesses  = 1
    isAbsolute  = False
    names = ["LElbowRoll","RElbowRoll","LShoulderRoll","RShoulderRoll"]
    angleLists = [math.radians(36.2),math.radians(-36.2),math.radians(-10),math.radians(10)]
    timeLists = [1.0,1.0,1.0,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

def get_up(postureProxy):
    """
    Nao gets up.
    """
    postureProxy.goToPosture("StandInit", 2)

def walk(motionProxy,x,y,theta ):
    """
    The robot walks.
    x(m)
    y(m)
    theta(degree)
    """
    motionProxy.moveTo(x, y, theta)

def turn(motionProxy, degree):
    """
    The robot has to turn at a certain numbre of degres.
    theta give the right number to turn nao at a certain degres
    """ 
    theta = (((math.pi)/2) * degree) / 90
    x = 0
    y = 0
    motionProxy.moveTo(x, y, theta)

def standby(postureProxy):
    """
    The robot stays and does nothing.
    """
    postureProxy.stopMove()

def danse(postureProxy, motionProxy):
    """
    This function makes the robot danse.
    """
    postureProxy.goToPosture("StandInit", 2)
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

def hey():
    animation_player_service = session.service("ALAnimationPlayer")
    tagToAnims = {}
    tagToAnims["myNewTag1"] = ["animations/Stand/Gestures/Hey_1", "animations/Stand/Gestures/Hey_3"]
    animation_player_service.addTagForAnimations(tagToAnims) 

if __name__ == "__main__":
    motionProxy = connect("ALMotion")
    postureProxy = connect("ALRobotPosture")
    #danse(postureProxy, motionProxy)
    #get_up(postureProxy)
    #turn(motionProxy, 40)
    #walk(motionProxy,0.3,0,0)
    #postureDeJeu(postureProxy, motionProxy)
    #shoot(postureProxy,motionProxy)
    #lSideShoot(postureProxy, motionProxy)
    #rSideShoot(postureProxy, motionProxy)
    #simpleShoot(postureProxy, motionProxy)
    defense(postureProxy, motionProxy)


