import unittest
import Action

class TestAction(unittest.TestCase):
   
    
    def setUp(self):
        self.mProxy = Action.connect("ALMotion")
        self.pProxy = Action.connect("ALRobotPosture")
        self.module1 = "ALMotion"
        self.module2 = "ALRobotPosture"
        self.x =0
        self.y = 0
        self.theta = 0
        self.degree = 0
        self.time = 1
    
    def test_connect(self):
        self.assertEqual(self.module1,"ALMotion") or self.assertEqual(self.module2,"ALRobotPosture")
        self.assertRaises(Exception, Action.connect(self.mProxy))
        self.assertRaises(Exception, Action.connect(self.pProxy))

    def test_shoot(self):
        self.assertEqual(self.module1,"ALMotion") or self.assertEqual(self.module2,"ALRobotPosture")

    def test_leftSideShoot(self):
        self.assertEqual(self.module1,"ALMotion") or self.assertEqual(self.module2,"ALRobotPosture")
    
    def test_rightSideShoot(self):
        self.assertEqual(self.module1,"ALMotion") or self.assertEqual(self.module2,"ALRobotPosture")

    def test_postureDeJeu(self):
        self.assertEqual(self.module1,"ALMotion") or self.assertEqual(self.module2,"ALRobotPosture")

    def test_get_up(self):
        self.assertEqual(self.module2,"ALRobotPosture")

    def test_walk(self):
        self.assertEqual(self.module1,"ALMotion")
        self.assertLess(self.x, 20) 
    
    def test_standBy(self):
        self.assertEqual(self.module2,"ALRobotPosture")

    def test_danse(self):  
        self.assertEqual(self.module2,"ALRobotPosture")
    
    def test_turn(self):
        self.assertEqual(self.module1,"ALMotion")
        self.assertLess(self.degree, 360) 

    def test_defense(self):
        self.assertEqual(self.module1,"ALMotion")
        self.assertGreater(self.time, 0.1)

    def test_walkFaster(self):
        self.assertEqual(self.module1,"ALMotion") and self.assertEqual(self.module2,"ALRobotPosture")

    def test_testWalk(self):
        self.assertEqual(self.module1,"ALMotion") and self.assertEqual(self.module2,"ALRobotPosture")

    def test_stiffnessOn(self):
        self.assertEqual(self.module1,"ALMotion") 


if __name__ == '__main__':
    unittest.main()