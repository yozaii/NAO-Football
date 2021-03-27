# -*- coding: utf-8 -*-
import qi
import argparse
import sys
import time
import math
from naoqi import ALProxy
IP = "127.0.0.1"
#IP = "172.27.96.32"
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
    


def shoot(postureProxy, motionProxy):
    """
    #The robot shoot in the ball.
    """
    motionProxy.moveInit()
    stiffnesses  = 1
    isAbsolute  = False
    #leg 
    names = ["LHipRoll","RHipPitch"]
    angleLists = [math.radians(5),math.radians(20.3)]
    timeLists = [2.0,2.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    
    # on tire
    names = ["RKneePitch","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(15),math.radians(-30),math.radians(-6)]
    timeLists = [0.8,0.6,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 2)

def simpleShoot(postureProxy, motionProxy):

    motionProxy.moveInit()
    stiffnesses  = 1
    isAbsolute  = False
    names = ["RKneePitch","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(15),math.radians(-20),math.radians(-6)]
    timeLists = [0.8,0.6,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 2)

def lSideShoot(postureProxy, motionProxy):
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 2)
    motionProxy.moveTo(0, 0.02, 0)
    motionProxy.moveInit()

def rSideShoot(postureProxy, motionProxy):
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 2)
    stiffnesses  = 1
    isAbsolute  = False
    names = ["RHipRoll"]
    angleLists = [math.radians(-8)]
    timeLists = [0.9]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    motionProxy.moveInit()


def postureDeJeu(postureProxy, motionProxy):
    """
    se met en posture de jeu
    """
    #dabord en pos initial
    motionProxy.moveInit()
    #puis les mains aligner
    stiffnesses  = 1
    isAbsolute  = False
    names = ["LElbowRoll","RElbowRoll","LShoulderRoll","RShoulderRoll"]
    angleLists = [math.radians(36.2),math.radians(-36.2),math.radians(-10),math.radians(10)]
    timeLists = [1.0,1.0,1.0,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

def get_up(postureProxy):
    """
    Nao get up.
    """
    postureProxy.goToPosture("StandInit", 2)

def walk(motionProxy ):
    """
    The robot walk.
    """
    x = 2
    #x(m)
    y = 0
    #y(m)
    theta = 0
    #theta(degree)
    motionProxy.moveInit()
    motionProxy.moveTo(x, y, theta)

def turn(motionProxy, degree):
    """
    The robot has to turn at a certain numbre of degres.
    """
    #this calcul give the right number to turn nao at a certain degres
    theta = (1.5709 * degree) / 90
    x = 0
    y = 0
    #pi/2 anti-clockwise (90 degrees)
    motionProxy.moveInit()
    motionProxy.moveTo(x, y, theta)

def standby(postureProxy):
    """
    The robot stay and do nothing.
    """
    postureProxy.stopMove()

def lookAround(motionProxy):
    """
    The robot looks right and left to scan the field"
    """
    name = "HeadYaw"
    motionProxy.setStiffnesses(name, 1)
    angleLists = [-2.0857, 2.0857]
    timeLists = [2.5, 5.0]
    motionProxy.post.angleInterpolation(name, angleLists, timeLists, True)

def lookTowards(motionProxy, direction):
    """
    The robot looks 45 degrees towards a chosen direction
    :param direction: String containing direction
    """
    motionProxy.setStiffnesses(name, 1)
    name = "HeadYaw"
    if (direction == "Right"):
        motionProxy.post.angleInterpolation(name, [-0.79], [1.0], False)
    elif (direction == "Left"):
        motionProxy.post.angleInterpolation(name, [0.79], [1.0], False)

def turnBodyToHeadAngle(motionProxy):
    """
    The body of the robot aligns itself with head angle
    """
    # Once the ball is found we stop the head from moving
    motionProxy.angleInterpolation("HeadYaw", [0.0], [1.0], False)

    # We get the angle of the head
    angle = motionProxy.getAngles("HeadYaw", False)

    # We move the body and face to face the ball
    motionProxy.moveTo(0.0, 0.0, angle[0])
    motionProxy.angleInterpolation("HeadYaw", [0.0], [1.0], True)


def danse(postureProxy, motionProxy):
    """
    Make the robot danse.
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


motionProxy = connect("ALMotion")
postureProxy = connect("ALRobotPosture")
#danse(postureProxy, motionProxy)
#get_up(postureProxy)
#turn(motionProxy, -40)
#walk(motionProxy)
#postureDeJeu(postureProxy, motionProxy)
#shoot(postureProxy,motionProxy)
#lSideShoot(postureProxy, motionProxy)
rSideShoot(postureProxy, motionProxy)
#simpleShoot(postureProxy, motionProxy)