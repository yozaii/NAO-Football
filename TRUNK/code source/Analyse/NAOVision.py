"""
Inspired by this link : http://doc.aldebaran.com/1-14/dev/python/examples/vision/get_image.html#python-example-vision-getimage
"""

import numpy as np
from naoqi import ALProxy
import vision_definitions
import unittest

IP = '168.1.1.1'
PORT = 9559

class NAOVision :

    def __init__ ( self, IP, PORT) :
        """
        Constructor
        :param IP: Ip of NAO Network
        :param PORT: 9559 by default
        :param CameraID:
        """

        # IP and Port
        self._ip = IP
        self._port = PORT

        # Proxy to ALVideoDevice
        self._videoProxy = None

        # Videomodule name.
        self._imgClientTop = ""
        self._imgClientBottom = ""

        # Image dimensions and parameters
        self._imgWidth = 320
        self._imgHeight = 240
        self._image = np.zeros([self._imgHeight, self._imgWidth, 3], dtype=np.uint8)

        # This will contain an ALImage from NAO robot
        self._alImage = None



    def _subscribeToVideoProxy(self, cameraID):
        """
        Register our video module to the robot
        cameraID = 0, uses the top camera
        cameraID = 1, uses the bottom camera
        """
        self._videoProxy = ALProxy("ALVideoDevice", self._ip, self._port)
        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace

        #"_client" : name of handler (1st argument)
        #cameraID: 0 for bottom, 1 for top (2nd argument)
        #fps (last argument)
        if (cameraID == 0):
            self._imgClientTop = self._videoProxy.subscribeCamera("_clientTop", cameraID,  resolution, colorSpace, 5)
        elif (cameraID == 1):
            self._imgClientBottom = self._videoProxy.subscribeCamera("_clientBottom", cameraID,  resolution, colorSpace, 5)

    def _unsubscribeToVideoProxy(self, cameraID):
        """
        Unregister our naoqi video module
        cameraID = 0, unsubscribes from the top camera
        cameraID = 1, unsubscribes from the bottom camera
        """
        if (cameraID == 0):
            if self._imgClientTop != "":
                self._videoProxyTop.unsubscribe(self._imgClient)
        elif (cameraID == 1):
            if self._imgClientBottom != "":
                self._videoProxyBottom.unsubscribe(self._imgClient)

    def _takeImage(self, cameraID):
        """
        Retrieves a new image from Nao
        """
        if (cameraID == 0):
            self._alImage = self._videoProxyTop.getImageRemote(self._imgClient)
        elif (cameraID == 0):
            self._alImage = self._videoProxyBottom.getImageRemote(self._imgClient)
        #still needs work to get proper dimensions
        self._image.data = self._alImage[6]
        return self._image

class TestNAOVision(unittest.TestCase):

    def testVideoSubscriptionTop(self):
        """
        imgClientTop is empty if subscribeCamera in
        NAOVision.subscribeToVideoProxy encounters an error
        Testing if not empty
        """
        nVis = NAOVision(IP, PORT)
        nVis._subscribeToVideoProxy(0)
        self.assertNotEquals(nVis._imgClientTop, '')


    def testVideoSubscriptionBottom(self):
        """
        imgClientBottom is empty if subscribeCamera in
        NAOVision.subscribeToVideoProxy encounters an error
        Testing if not empty
        """
        nVis = NAOVision(IP, PORT)
        nVis._subscribeToVideoProxy(1)
        self.assertNotEquals(nVis._imgClientBottom, '')


    def testTakeImageTopDimensions(self):
        """
        tests if dimensions are correct when taking an
        image from top camera
        """
        nVis = NAOVision(IP, PORT)
        nVis._subscribeToVideoProxy(1)
        nVis._takeImage(0)
        self.assertEqual(nVis._image.shape, (240L, 320L, 3L))


    #def testTakeImageBottom(self):


if __name__ == "__main__":
    unittest.main()


    #Other tests below:

    """
    nVis = NAOVision(IP,PORT)
    print(nVis._image.shape == (240L, 320L, 3L))
    """


