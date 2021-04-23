#-*- coding: utf-8 -*-
import time
import math
import motion
from naoqi import ALProxy
#import almath 
IP = "127.0.0.1"
#IP = "172.27.96.34"
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

    postureProxy.goToPosture("StandInit", 0.5)
    stiffnesses  = 1
    isAbsolute  = False
    #here the robot puts its foot back
    names = ["LHipRoll","LAnkleRoll"]
    angleLists = [math.radians(-5),math.radians(15)]
    timeLists = [1.0,1.0]
    motionProxy.setStiffnesses(names, stiffnesses)
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)


    postureProxy.goToPosture("Stand", 0.5)
    
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

    postureProxy.goToPosture("StandInit", 0.5)
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

    names = ["RKneePitch","RHipPitch","RAnklePitch","LHipRoll"]
    angleLists = [math.radians(5),math.radians(-15),math.radians(0),math.radians(-15)]
    timeLists = [0.8,0.6,1.0,1,1,1]
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

def shootFromChoregraphe(motionProxy):
    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.2, 0.36, 0.6, 1.04, 1.2, 1.44, 1.6])
    keys.append([0.573674, 0.573674, 0.497522, 0.497522, 0.573674, 0.573674, 0.573674])

    names.append("HeadYaw")
    times.append([0.2, 0.36, 0.6, 1.04, 1.2, 1.44, 1.6])
    keys.append([-0.01845, -0.01845, -0.0188174, -0.0188174, -0.01845, -0.01845, -0.01845])

    names.append("LAnklePitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([-0.34826, -0.335988, -0.346725, -0.346725, -0.346725, -0.346725, -0.346725, -0.461776, -0.664264, -0.83914, -0.702614, -0.434165, -0.139636, 0.233125, 0.220854])

    names.append("LAnkleRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.00464392, -0.00609397, -0.00455999, -0.00609397, -0.00609397, -0.00609397, 0.00464392, -0.156426, -0.156426, -0.145688, -0.145688, -0.145688, -0.145688, -0.145688, -0.145688])

    names.append("LElbowRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([-0.972515, -0.972515, -0.962705, -0.962705, -0.972515, -0.972515, -0.972832])

    names.append("LElbowYaw")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([-1.3653, -1.3653, -1.34904, -1.35962, -1.3653, -1.3653, -1.3697])

    names.append("LHand")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.262, 0.262, 0.270948, 0.270948, 0.262, 0.262, 0.270948])

    names.append("LHipPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([-0.452487, -0.452487, -0.446352, -0.452487, -0.452487, -0.452487, -0.452487, -0.42641, -0.389594, -0.389594, -0.579811, -0.840591, -1.0124, -1.11518, -1.10751])

    names.append("LHipRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.00157595, -0.00916195, -0.0106959, -0.00916195, -0.00916195, -0.00916195, -0.00916195, -0.032172, -0.032172, -0.032172, -0.032172, -0.032172, -0.032172, -0.032172, -0.032172])

    names.append("LHipYawPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.00464392, 0.00464392, 0.00617791, 0.00464392, 0.00464392, 0.00464392, 0.00464392, -0.033706, -0.033706, -0.033706, -0.033706, -0.049046, -0.049046, -0.049046, -0.049046])

    names.append("LKneePitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.70253, 0.70253, 0.696393, 0.70253, 0.70253, 0.70253, 0.70253, 0.819114, 1.05995, 1.17347, 1.17347, 1.17347, 1.0983, 0.944902, 0.944902])

    names.append("LShoulderPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([1.42965, 1.42965, 1.41554, 1.42759, 1.42965, 1.42965, 1.42759])

    names.append("LShoulderRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.274544, 0.285283, 0.167447, 0.283444, 0.274544, 0.274544, 0.283444])

    names.append("LWristYaw")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.030638, 0.030638, 0.0215546, 0.0215546, 0.030638, 0.030638, 0.0215546])

    names.append("RAnklePitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([-0.348176, -0.490837, -0.484702, -0.490837, -0.535324, -0.507713, -0.51845, -0.51845, -0.507713, -0.507713, -0.507713, -0.507713, -0.507713, -0.507713, -0.507713])

    names.append("RAnkleRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([-0.00302602, -0.095066, -0.323631, -0.105804, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912, -0.200912])

    names.append("RElbowRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.974133, 0.974133, 0.958079, 0.96826, 0.289967, 0.289967, 0.298289])

    names.append("RElbowYaw")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([1.36982, 1.36982, 1.36534, 1.36534, 1.36982, 1.36982, 1.37611])

    names.append("RHand")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.2664, 0.2664, 0.261609, 0.261609, 0.2664, 0.2664, 0.261609])

    names.append("RHipPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([-0.455641, -0.520068, -0.5937, -0.520068, -0.567621, -0.567621, -0.589097, -0.57836, -0.57836, -0.57836, -0.57836, -0.57836, -0.57836, -0.57836, -0.57836])

    names.append("RHipRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.00157595, -0.00916195, 0.047596, -0.00916195, -0.00916195, -0.00916195, 0.00157595, 0.00157595, 0.00157595, 0.00157595, 0.00157595, 0.00157595, 0.00157595, 0.00157595, 0.00157595])

    names.append("RHipYawPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.00464392, 0.00464392, 0.00617791, 0.00464392, 0.00464392, 0.00464392, 0.00464392, -0.033706, -0.033706, -0.033706, -0.033706, -0.049046, -0.049046, -0.049046, -0.049046])

    names.append("RKneePitch")
    times.append([0.2, 0.36, 0.48, 0.6, 0.72, 0.88, 1.04, 1.2, 1.44, 1.6, 1.72, 1.84, 2, 2.16, 2.36])
    keys.append([0.704148, 0.963394, 1.02015, 0.963394, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924, 1.06924])

    names.append("RShoulderPitch")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([1.45121, 1.45121, 1.47596, 1.45576, 1.50643, 1.50643, 1.49031])

    names.append("RShoulderRoll")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([-0.271559, -0.271559, -0.27254, -0.27254, -0.174919, -0.174919, -0.242992])

    names.append("RWristYaw")
    times.append([0.2, 0.36, 0.48, 0.6, 1.2, 1.6, 2])
    keys.append([0.0475121, 0.0475121, 0.0433513, 0.0433513, 0.0475121, 0.0475121, 0.0433513])
    
    motionProxy.angleInterpolation(names, keys, times, True)
   
def moveTo(postureProxy,motionProxy):

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 2)
    # Example showing how to get a simplified robot position in world.
    useSensorValues = False
    result = motionProxy.getRobotPosition(useSensorValues)
    print("Robot Position", result)
    # Example showing how to use this information to know the robot's diplacement.
    useSensorValues = False
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))
    # Make the robot move
    motionProxy.moveTo(0.1, 0.0, 0.2)
    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))
    # Compute robot's' displacement
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print("Robot Move:", robotMove)

def moveToo(postureProxy,motionProxy):

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing how to get a simplified robot position in world.
    result = motionProxy.getRobotPosition()
    print "Next Robot Position", result

    # Example showing how to use this information to know the robot's diplacement
    # during the move process.

    # Make the robot move
    motionProxy.moveTo(0.1, 0.0, 0.1, _async=True) # No blocking due to post called
    time.sleep(1.0)
    initRobotPosition = almath.Pose2D(motionProxy.getNextRobotPosition())

    # Make the robot move
    motionProxy.moveTo(0.0, 0.0, 0.0)

    endRobotPosition = almath.Pose2D(motionProxy.getNextRobotPosition())

    # Compute robot's' displacement
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove
    result = motionProxy.getNextRobotPosition()
    print "Next Robot Position", result



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
    #shoot(postureProxy,motionProxy)
    #leftSideShoot(postureProxy, motionProxy)
    #rightSideShoot(postureProxy, motionProxy)
    #simpleShoot(postureProxy, motionProxy) 
    #defense(postureProxy, motionProxy, 0.1)
    #walkFaster(motionProxy, postureProxy)
    #contournBall(motionProxy, postureProxy, 0)
    #shootFromChoregraphe(motionProxy)
    moveTo(postureProxy,motionProxy)
