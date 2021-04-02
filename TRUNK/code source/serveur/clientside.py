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
                print msg_receiv

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
"""
app = qi.Application(url="tcp://172.27.96.32:9559")
app.start()
session = app.session
myClient = Client()
id = session.registerService("Client", Client())
robotClient = session.service("Client")

networkProxy = ALProxy("ALConnectionManager", "172.27.96.32", 9559)
networkProxy.connect(id)
#app.run()
print robotClient.returnIP()
app.stop()
"""
"""
parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="172.27.96.32",help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=9559,help="Naoqi port number")
args = parser.parse_args()

networkProxy = ALProxy("ALConnectionManager", "172.27.96.32", 9559)
session = qi.Session()
session.connect("tcp://172.27.96.32:9559")
serviceId = session.registerService("Client", Client())

robotClient = session.service("Client")
print robotClient
#print robotClient.returnIp()

#session.connect("tcp://" + args.ip + ":" + str(args.port))
#robotClient = session.service("ALConnectionManager")


#print serviceId

#robotClient.connect(serviceId)
#print robotClient.returnIP
"""
#-------------------------------------- Test Client -------------------------------------------------
c1 = Client()
c2 = Client()
c1.connection()
c2.connection()
c1.send_message("Hello world")
c2.send_message("Hello world 2")

c1.disconnection()
c2.disconnection()
"""
c1 = Client()
c2 = Client()
c1.connection()
c2.connection()
#thread_listening1 = threading.Thread(target=c1.listening)
#thread_listening2 = threading.Thread(target=c2.listening)
#thread_listening1.start()
#thread_listening2.start()
print c1.port
d= {1: "ptdr",2: "lol"} 
c1.send_message("Hello world")
c1.send_message(d)
c2.send_message("Hello world 2")
c2.send_message("Hello world 3")
#c1.send_message(h)
c1.disconnection()
c2.disconnection()
"""
#-------------------------------------- Test Unitaires -------------------------------------------------
"""
class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.c1 = Client()
        self.c2 = Client()
        return super().setUp()

    def test_connection_RaisesConnectionRefusedError(self):
        self.assertRaises(ConnectionRefusedError, self.c1.connection)
    
    def test_connection_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.connection, "je veux une erreur de paramètre")

    def test_send_message_isNone(self):
        self.assertIsNone(self.c1.send_message)

    def test_send_message_RaisesIllegalArguments(self):
        self.assertRaises(Exception, self.c1.send_message, (None, 2, "je veux une erreur de paramètre"))

if __name__ == "__main__":
    unittest.main()
"""