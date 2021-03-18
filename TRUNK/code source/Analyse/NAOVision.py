"""
Inspired by this link : http://doc.aldebaran.com/1-14/dev/python/examples/vision/get_image.html#python-example-vision-getimage
"""


import numpy as np
from naoqi import ALProxy
import vision_definitions

class NAOVision :

    def __init__ ( self, IP, PORT, CameraID) :
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
        self._imgClient = ""

        # Image dimensions and parameters
        self._imgWidth = 320
        self._imgHeight = 240
        self._image = np.zeros([self._imgHeight, self._imgWidth, 3], dtype=np.uint8)
        self._cameraID = CameraID
        self.resize(self._imgWidth, self._imgHeight)

        # This will contain an ALImage from NAO robot
        self._alImage = None



    def _subscribeToVideoProxy(self, cameraID):
        """
        Register our video module(_imgCLient) to the robot.
        """
        self._videoProxy = ALProxy("ALVideoDevice", self._ip, self._port)
        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace

        #"_client" : name of handler (1st argument)
        #cameraID: 0 for bottom, 1 for top (2nd argument)
        #fps (last argument)
        self._imgClient = self._videoProxy.subscribe("_client", cameraID,  resolution, colorSpace, 5)

    def _unregisterImageClient(self):
        """
        Unregister our naoqi video module (_imgClient)
        """
        if self._imgClient != "":
            self._videoProxy.unsubscribe(self._imgClient)

    def _takeImage(self):
        """
        Retrieve a new image from Nao.(incomplete)
        """
        self._alImage = self._videoProxy.getImageRemote(self._imgClient)

        #still needs work to get proper dimensions
        self._image = np.append(self._alImage[6])
        return self._image