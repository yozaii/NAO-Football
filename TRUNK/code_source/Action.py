#-*- coding: utf-8 -*-
import time
import math
import motion
from naoqi import ALProxy
#import almath 
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

def stiffnessOn(module):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    module.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

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
   
def defense(postureProxy, motionProxy, timeGiven):
    postureProxy.goToPosture("Sit", 5)
    time.sleep(timeGiven)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 5)

def shoot(postureProxy, motionProxy):
    """
    #The robot shoots in the ball.
    """
    # Send NAO to Pose Init
    postureProxy.goToPosture("Stand", 5)
    postureProxy.goToPosture("StandInit", 5)
    stiffnesses  = 1
    isAbsolute  = False
    #here the robot puts its foot back
    names = ["RAnkleRoll","LAnkleRoll","LHipPitch","LAnklePitch","LKneePitch"]
    angleLists = [math.radians(10),math.radians(10),math.radians(10),math.radians(5),math.radians(-10)]
    timeLists = [0.3,0.5,0.7,0.8,0.9]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #here the robot puts its foot back
    names = ["RHipPitch","RAnklePitch","RKneePitch"]
    angleLists = [math.radians(-15),math.radians(35),math.radians(-30)]
    timeLists = [1,1,1]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
 
    

def simpleShoot(postureProxy, motionProxy):
    """
    this function is a the movement of a little shoot for Nao
    """
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)

    footStepsList = [] 
    footStepsList.append([["LLeg"], [[0.12, 0.00, 0.0]]])
    footStepsList.append([["LLeg"], [[-0.01, 0.00, 0.0]]])
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
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)   

def leftSideShoot(postureProxy, motionProxy):
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)

    footStepsList = [] 
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])
    footStepsList.append([["LLeg"], [[0.00, -0.16, 0.0]]])
    stepFrequency = 0.2
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
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)   
    
def rightSideShoot(postureProxy, motionProxy):
    # Send NAO to Pose Init
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

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)

def postureDeJeu(postureProxy, motionProxy):
    """
    The posture that should have the robot.
    """
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 2)
    stiffnesses  = 1
    isAbsolute  = False
    names = ["LElbowRoll","RElbowRoll","LShoulderRoll","RShoulderRoll"]
    angleLists = [math.radians(36.2),math.radians(-36.2),math.radians(-10),math.radians(10)]
    timeLists = [1.0,1.0,1.0,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

def turn(motionProxy, degree):
    """
    The robot has to turn at a certain numbre of degres.
    theta give the right number to turn nao at a certain degres
    """ 
    theta = (((math.pi)/2) * degree) / 90
    x = 0
    y = 2
    motionProxy.moveTo(x, y, theta)

def standby(postureProxy):
    """
    The robot stays and does nothing.
    """
    postureProxy.stopMove()

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
    motionProxy.moveInit()
    postureProxy.goToPosture("StandInit", 0.5)


def walkFaster(motionProxy, postureProxy):
    # Set NAO in Stiffness On
    stiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0

    # Default walk (MaxStepX = 0.04 m)
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    time.sleep(3.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"

    # Speed walk  (MaxStepX = 0.06 m)
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency, [["MaxStepX", 0.06]])
    time.sleep(4.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"
    """
    # stop walk on the next double support
    motionProxy.stopMove()
    """

def testWalk(motionProxy, postureProxy):
    # Set NAO in stiffness On
    stiffnessOn(motionProxy)

    # first we defined the goal
    goal = m.Pose2D(0.0, -0.4, 0.0)

    # We get the dubins solution (control points) by
    # calling an almath function

    circleRadius = 0.04
    # Warning : the circle use by dubins curve
    #           have to be 4*CircleRadius < norm(goal)
    dubinsSolutionAbsolute = m.getDubinsSolutions(goal, circleRadius)

    # moveTo With control Points use relative commands but
    # getDubinsSolution return absolute position
    # So, we compute dubinsSolution in relative way
    dubinsSolutionRelative = []
    dubinsSolutionRelative.append(dubinsSolutionAbsolute[0])
    for i in range(len(dubinsSolutionAbsolute)-1):
        dubinsSolutionRelative.append(
                dubinsSolutionAbsolute[i].inverse() *
                dubinsSolutionAbsolute[i+1])

    # create a vector of moveTo with dubins Control Points
    moveToTargets = []
    for i in range(len(dubinsSolutionRelative)):
        moveToTargets.append(
            [dubinsSolutionRelative[i].x,
             dubinsSolutionRelative[i].y,
             dubinsSolutionRelative[i].theta] )

    # Initialized the Move process and be sure the robot is ready to move
    # without this call, the first getRobotPosition() will not refer to the position
    # of the robot before the move process
    motionProxy.moveInit()

    # get robot position before move
    robotPositionBeforeCommand  = m.Pose2D(motionProxy.getRobotPosition(False))
    motionProxy.moveTo( moveToTargets )
    print "position : ", robotPositionBeforeCommand

    # get robot position after move
    robotPositionAfterCommand = m.Pose2D(motionProxy.getRobotPosition(False))

    # compute and print the robot motion
    robotMoveCommand = m.pose2DInverse(robotPositionBeforeCommand)*robotPositionAfterCommand
    print "The Robot Move Command: ", robotMoveCommand

def coup(motionProxy, postureProxy):

    #motionProxy.wakeUp()
   # Send NAO to Pose Init
    postureProxy.goToPosture("Stand", 5)
    postureProxy.goToPosture("StandInit", 5)
    stiffnesses  = 1
    isAbsolute  = False
    #here the robot puts its foot back
    names = ["LHipRoll","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(15),math.radians(30),math.radians(-10)]
    timeLists = [1.0,1.0,1.1]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    # the robot shoots
    names = ["RKneePitch","RHipPitch","RAnklePitch"]
    angleLists = [math.radians(5),math.radians(-50),math.radians(10)]
    timeLists = [0.8,0.6,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    postureProxy.goToPosture("StandInit", 5)
    names = ["RKneePitch","RHipPitch","RAnklePitch","LHipRoll"]
    angleLists = [math.radians(-5),math.radians(15),math.radians(0),math.radians(-15)]
    timeLists = [0.8,0.6,1.0,1]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    
def contournBall(motionProxy, postureProxy, degree):
    postureProxy.goToPosture("StandInit", 2)
    footStepsList = [] 
    # 1) Step forward with your left foot
    footStepsList.append([["LLeg"], [[0.0, 0.15, -0.2]]])
    # 2) Sidestep to the left with your left foot
    footStepsList.append([["RLeg"], [[0.00, 0.15, -0.2]]])
    # 3) Move your right foot to your left foot
    footStepsList.append([["LLeg"], [[0.00, 0.15, -0.2]]])
    # 4) Sidestep to the left with your left foot
    footStepsList.append([["RLeg"], [[0.00, 0.15, -0.2]]])
    # 5) Step backward & left with your right foot
    footStepsList.append([["LLeg"], [[0.0, 0.15, -0.2]]])
    # 6)Step forward & right with your right foot
    footStepsList.append([["RLeg"], [[0.00, 0.15, -0.2]]])
    # 7) Move your left foot to your right foot
    footStepsList.append([["LLeg"], [[0.00, 0.15, -0.2]]])                    
    # 8) Sidestep to the right with your right foot
    footStepsList.append([["RLeg"], [[0.00, 0.15, -0.2]]])
    ###############################
    # Send Foot step
    ###############################
    stepFrequency = 0.8
    clearExisting = False
    nbStep= 9# defined the number of cycle to make
    for j in range( nbStep):
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
if __name__ == "__main__":


    motionProxy = connect("ALMotion")
    postureProxy = connect("ALRobotPosture")
    #postureProxy.goToPosture("StandInit", 2)
    #time.sleep(2)
    #danse(postureProxy, motionProxy)
    #get_up(postureProxy)
    #turn(motionProxy, 0)
    #walk(motionProxy,0.2,0,0)
    #postureDeJeu(postureProxy, motionProxy)
    #coup(motionProxy, postureProxy)
    shoot(postureProxy,motionProxy)
    #leftSideShoot(postureProxy, motionProxy)
    #rightSideShoot(postureProxy, motionProxy)
    #simpleShoot(postureProxy, motionProxy) 
    #defense(postureProxy, motionProxy, 0.1)
    #walkFaster(motionProxy, postureProxy)
    #contournBall(motionProxy, postureProxy, 0)

