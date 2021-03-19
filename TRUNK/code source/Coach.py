#------------------------#
#     Classes Coach      #
#------------------------#

from math import *
from Node import *
class Coach:
    """ 
    class who dictates who need to do what and making decision about the game
    Argument:
    Variable:
    """

    role = list(Role)
    strat = Strategy.DEFAULT


    def __init__(self):
        if strat == Strategy.DEFAULT:
            role.remove(Role.MIDDLE)

    def distribRole(self):
        """
        allows to give a role to the robot
        """

        choice = random.choice(role)
        role.remove(choice)
        return choice

    def isPresent(self,f,g,posElement):
        """
        allows to know if a point3D is between two others point3D
        Argument:
        f -- Function which corresponds to one of the external lines between two robots
        g -- Function which corresponds to one of the external lines between two robots
        posElement -- Position (Point3D) of the element C
        """

        # we verify if the point C is between the function f and g
        if posElement.get_y() <= f.get_y(posElement.get_x()) and posElement.get_y() >= g.get_y(posElement.get_x()) and posElement.get_x() <= f.get_x(posElement.get_y()) and posElement.get_x() >= g.get_x(posElement.get_y()):
            return true
        else:
            return false

    def theClosest(self,posElement,listRobot):
        """
        allows to know which ally is closest to a point
        Argument:
        posElement -- position of an element
        listRobot -- the list of allied or enemy robot
        """

        index = 0
        distanceMin = math.inf

        for i in range(5):
            distance = posElement.distance(posElement,listRobot[i].get_pos())
            if distance < distanceMin:
                distanceMin = distance
                index = i

        return listRobot[index]

    def ballPass(self,listEnemyRobot,listAllyRobot,posBall,robotPasser):
        """
        allows to make a good pass
        listEnemyRobot -- the list of enemy robot
        """
        listAllyRobot.remove(robotPasser)
        perimeterBall = PerimeterSquare(posBall)

        for i in range(5):
            perimeterRobot = PerimeterSquare(listAllyRobot[i].get_pos())
            f = AffineFunction(perimeterBall.get_topLeft(),perimeterRobot.get_topLeft())
            g = AffineFunction(perimeterBall.get_topRight(),perimeterRobot.get_topRight())
            h = AffineFunction(perimeterBall.get_botLeft(),perimeterRobot.get_botLeft())
            i = AffineFunction(perimeterBall.get_botRight(),perimeterRobot.get_botRight())
            listFunction = bestFunction(f,g,h,i)
            # boucle pour les ennemies
            for j in range(5):
                if isPresent(listFun[0],listFun[1],listEnemyRobot[j]):
                    break;
            

        # doit retourner la liste des robots à qui je peux faire la passe