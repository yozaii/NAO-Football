# coding: utf-8
import argparse
import pickle
import socket
import threading
import unittest
import qi
from naoqi import ALProxy

class Client:
    host = "192.168.56.1" #The IP server(ou DNS name)
    port = 10000
    DISCONNECTION_MESSAGE = "fin"

    def __init__(self):
        """
        init the client socket
        """
        self.is_connected = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        """
        connect the client to the server
        and raise an error if the server isn't launched
        """
        try:
            self.is_connected = True
            self.client_socket.connect((Client.host, Client.port))
        except Exception as e:
            self.is_connected = False
            print "La connexion au serveur a échouée !"
            raise e

    def send_message(self, message=""):
        """
        The client send a message through
        the server
        """
        msg = pickle.dumps(message)
        self.client_socket.send(msg)
        print self.client_socket.recv(1024).decode("utf8")

    def listening(self):
        """
        The client is listening if others 
        clients talking to him
        """
        while self.is_connected:
            msg_receiv = self.client_socket.recv(1024)
            if len(msg_receiv) > 0:
                msg_receiv = pickle.loads(msg_receiv)
                print "j'ai bien recu "+msg_receiv

    def disconnection(self):
        """
        Disconnect the client to the server
        """
        self.is_connected = False
        self.send_message(self.DISCONNECTION_MESSAGE)

    def returnIP(self):
        """
        A test function to see if the return
        is the ip adress of the robot or the computer
        """
        return socket.gethostbyname(socket.gethostname())

#-------------------------------------- Test connection to the robot -------------------------------------------------

def testConnectionToRobotWithQi_Application():
    app = qi.Application(url="tcp://172.27.96.32:9559") #Connection to the robot with his IP and port
    app.start()
    session = app.session
    myClient = Client()
    serviceId = session.registerService("Client", MyClient) #We register the Client instance as a service that the robot will use 
    robotClient = session.service("Client") #Using the service "Client" 

    print robotClient.returnIP() #Normally return the robot adress IP
    app.stop()


def testConnectionToRobotWithSession():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="172.27.96.32",help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,help="Naoqi port number")
    args = parser.parse_args()

    session = qi.Session()
    session.connect("tcp://"+ args.ip +":" + str(args.port)) #Connect the session to the robot
    myClient = Client()
    serviceId = session.registerService("Client", MyClient) #Create an ID for the service Client()
    networkProxy = session.service("ALConnectionManager") #Connection to the module "ALConnectionManager" from naoqi
    serviceClient = networkProxy.connect(serviceId) #Connection to the service Client with his ID

    print serviceClient.returnIP() #Normally return the robot adress IP

def testConnectionToRobotWithALConnectionManager():
    networkProxy = ALProxy("ALConnectionManager", "172.27.96.32", 9559) #Connect the module ALConnectionManager with the robot
    networkProxy.connect()

#-------------------------------------- Test Client -------------------------------------------------
c1 = Client()
c2 = Client()

def testConnectionClients():
    """
    test the connection to the server
    """
    c1.connection()
    c2.connection()

def testSend_message():
    """
    test the function send_message
    with several messages
    """
    c1.send_message("Hello world")
    c2.send_message("Hello world 2")
    dictionnary = {1: "Test1", 2: "Test2"}
    c2.send_message(dictionnary)
    c1.send_message("Hello world3")

def testListening():
    """
    test the listening of clients
    Maybe use thread for not blocked the programm
    """
    c1.listening()
    c2.listening()

def testDisconnection():
    """
    test the disconnection to the server
    """
    c1.disconnection()
    c2.disconnection()

#-------------------------------------- Test Unitaires -------------------------------------------------
class TestClient(unittest.TestCase):
    def setUp(self):
        self.c1 = Client()
        self.c2 = Client()
        return super().setUp()

    def test_connection_RaisesConnectionRefusedError(self):
        self.assertRaises(Exception, self.c1.connection)
    
    def test_connection_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.connection, "je veux une erreur de paramètre")

    def test_send_message_isNone(self):
        self.assertIsNone(self.c1.send_message)
        
    def test_send_message_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.send_message, (None, 2, "je veux une erreur de paramètre"))

    def test_disconnection_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.disconnection, ("je veux une erreur de paramètre"))

    def test_listening_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.listening, ("je veux une erreur de paramètre"))
if __name__ == "__main__":
    unittest.main()
