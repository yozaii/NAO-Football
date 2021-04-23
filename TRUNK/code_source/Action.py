#-*- coding: utf-8 -*-
import time 
import math
import motion
from naoqi import ALProxy
import almath

def connect(module):
    """
    "module" is the name of the API of Nao that we need to make it connect.
    allows to connect the robot.
    Create a proxy to ALMotion and ALRobotPosture.
    
    """
    try:
        return ALProxy(module, IP, PORT)
    except Exception,e:
        print "Could not create proxy"
        print "Error was: ",e

def stiffnessOn(module):
    """"module" is the name of the API of Nao that we need to make it connect.
    This function allows to get stiffness in on mode.

    """
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    # Gets stiffness on
    module.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def danse(postureProxy, motionProxy):
    """
    This function makes the robot danse.
    "postureProxy" is allows Nao to use "ALRobotPosture" API
    "motionProxy" allows Nao to use "ALMotion" API
    """
    # Go to standInit position
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
    """This function allows the robot to sit down to defend.
    We take the parameters that allow the robot to move 
    and  "timeGime" is the time we need for it to remain seated.
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    "motionProxy" allows Nao to use "ALMotion" API.
    """
    #go to sit posture
    postureProxy.goToPosture("Sit", 5)
    #stay as long as given
    time.sleep(timeGiven)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 5)
    
def simpleShoot(postureProxy, motionProxy):
    """
    this function is a the movement of a little shoot for Nao.
    He takes a step forward.
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    "motionProxy" allows Nao to use "ALMotion" API.
    """
    # Send NAO to Pose StandInit
    postureProxy.goToPosture("StandInit", 2)
    #Loop that allows you to start the steps several times
    footStepsList = [] 
    #Step forward with your left foot
    footStepsList.append([["LLeg"], [[0.12, 0.00, 0.0]]])
    footStepsList.append([["LLeg"], [[-0.01, 0.00, 0.0]]]) 
    #Send Foot step
    stepFrequency = 1 #defined the number of cycle to make
    clearExisting = False
    #Loop that allows you to start the steps several times
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
    """The robot shoot on the left side
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    "motionProxy" allows Nao to use "ALMotion" API.
    """
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)

    footStepsList = [] 
    #Sidestep to the left with your left foot
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])
    footStepsList.append([["LLeg"], [[0.00, -0.16, 0.0]]])
    #Send Foot step
    stepFrequency = 0.2 #defined the number of cycle to make
    clearExisting = False
    #Loop that allows you to start the steps several times
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
    """ The robot shoot on the right side
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    "motionProxy" allows Nao to use "ALMotion" API.
    """
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)

    footStepsList = [] 
    #Sidestep to the right with your right foot
    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])
    footStepsList.append([["RLeg"], [[0.00, 0.16, 0.0]]])
    #Send Foot step
    stepFrequency = 1
    clearExisting = False
    #Loop that allows you to start the steps several times
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

def turn(motionProxy, degree):
    """
    The robot has to turn at a certain numbre of degres.
    degree is the value you want the robot to spin
    "motionProxy" allows Nao to use "ALMotion" API.
    """ 
    # theta give the right number to turn nao at a certain degree
    theta = (((math.pi)/2) * degree) / 90
    x = 0 #The robot does not move forward
    y = 0 #The robot does not move to the side
    #Nao moves
    motionProxy.moveTo(x, y, theta)

def standby(postureProxy):
    """
    The robot stays and does nothing.
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    """
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 2)
    # NAO stops mouving
    postureProxy.stopMove()

def get_up(postureProxy):
    """
    Nao gets up.
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    """
    #Nao get to StandInit position
    postureProxy.goToPosture("StandInit", 2)

def walk(motionProxy,x,y,theta ):
    """
    The robot walks.
    x(m).
    y(m).
    theta(degree).
    "motionProxy" allows Nao to use "ALMotion" API.
    """
    motionProxy.moveTo(x, y, theta)
    #Nao get to Init move
    motionProxy.moveInit()
    
    #Nao get to StandInit position
    postureProxy.goToPosture("StandInit", 0.5)

def navigation(motionProxy,postureProxy,navigationProxy, x, y,z):
    """Makes the robot navigate to a relative metrical target pose2D expressed.
    The robot computes a path to avoid obstacles.
    Works only if Nao finds obstacles
    "postureProxy" is allows Nao to use "ALRobotPosture" API.
    "motionProxy" allows Nao to use "ALMotion" API.
    "navigationProxy" allows Nao to use "ALNavigation" API.
    """
    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Scanning the environement.
    motionProxy.startFreeZoneUpdate()

    # Add here an animation with timelines and moves (less than 60 seconds).  
    motionProxy.moveTo(x, y, z * math.pi)
    ###########################################################################
    desiredRadius = 0.6
    displacementConstraint = 0.5
    result = navigationProxy.findFreeZone(desiredRadius, displacementConstraint)

    errorCode = result[0]
    if errorCode != 1:
        worldToCenterFreeZone = almath.Pose2D(result[2][0], result[2][1], 0.0)
        worldToRobot = almath.Pose2D(motionProxy.getRobotPosition(True))
        robotToFreeZoneCenter = almath.pinv(worldToRobot) * worldToCenterFreeZone
        motionProxy.moveTo(robotToFreeZoneCenter.x, robotToFreeZoneCenter.y, 0.0)
    else :
        print "Problem during the update of the free zone."

def walkFaster(motionProxy, postureProxy, x,y,z):
    """ This function makes Nao walk faster than the other function "walk".
    postureProxy is allows Nao to use "ALRobotPosture" API.
    motionProxy allows Nao to use "ALMotion" API.
    """
    # Set NAO in Stiffness On
    stiffnessOn(motionProxy)

    # Send NAO to Pose StandInit
    postureProxy.goToPosture("StandInit", 0.5)
    # TARGET VELOCITY
    X         = x
    Y         = y
    Theta     = z
    Frequency = 1.0

    # Default walk (MaxStepX = 0.04 m)
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    time.sleep(3.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"

    # Speed walk  (MaxStepX = 0.06 m)
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency, [["MaxStepX", 0.06]])
    time.sleep(4.0)
    print "walk Speed X :",motionProxy.getRobotVelocity()[0]," m/s"
    
def contournBall(motionProxy, postureProxy, degree):
    """When the robot will need to move around the ball to position itself correctly.
    degree is the number of degree that makes 1 cycle ( 3 cycle makes nao turn to 180 degree).
    postureProxy is allows Nao to use "ALRobotPosture" API.
    motionProxy allows Nao to use "ALMotion" API.
    """
    #Nao get to StandInit posture
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
    # defined the number of cycle to make
    for j in range(degres):
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
    """this function makes the robot shooting in the ball.
    The movement was mimed on Choregraphe then exported in python langauge.
    motionProxy allows Nao to use "ALMotion" API.
    """
    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    #We get a list of names of joints, time and keys of movement.
    #For each movement, this allows the robot's articulation to be moved according to the time and degree of articulation desired.

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





if __name__ == "__main__":

    IP = "127.0.0.1"
    PORT = 9559
    motionProxy = connect("ALMotion")
    postureProxy = connect("ALRobotPosture")
    navigationProxy = connect("ALNavigation")



