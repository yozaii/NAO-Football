# coding: utf-8
import pickle
import socket
import unittest
"""
#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
host = "localhost"#socket.gethostbyname(socket.gethostname())
print(host)
port = 10000 #ceux entre 0 et 1023 sont réservé au système


try:
    ouvrir_connexion_avec_serveur.connect((host, port))

    msg_a_envoyer = b""
    while msg_a_envoyer != b"fin":
        msg_a_envoyer = input("> ")
        # Peut planter si vous tapez des caractères spéciaux
        msg_a_envoyer = msg_a_envoyer.encode("utf8")
        # On envoie le message
        ouvrir_connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu = ouvrir_connexion_avec_serveur.recv(1024)
        print(msg_recu.decode("utf8"))
except ConnectionRefusedError:
    print("La connexion au serveur a échouée !")
finally:
    ouvrir_connexion_avec_serveur.close()
"""
#--------------------------------------------------------------------
class Client:
    host = "192.168.56.1" #Doit être l'IP du serveur (ou nom DNS)
    port = 10000
    HEADER = 64
    DISCONNECTION_MESSAGE = "fin"

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        try:
            self.client_socket.connect((Client.host, Client.port))
        except ConnectionRefusedError as e:
            print("La connexion au serveur a échouée !")
            raise e

    def send_message(self, message=""):

        if type(message) is str:
            msg = message.encode("utf8")
            """
            lenght_msg = len(msg)
            lenght_msg = str(lenght_msg).encode("utf8")
            lenght_msg += b' ' * (HEADER - len(lenght_msg))
            self.client_socket.send(lenght_msg)
            """
            self.client_socket.send(msg)
            print(self.client_socket.recv(1024).decode("utf8"))
        else:
            msg = pickle.dumps(message)
            print(msg)
            self.client_socket.send(msg)

    def disconnection(self):
        self.send_message(self.DISCONNECTION_MESSAGE)

class Humain:
    def __init__(self):
        self.name = "test"

"""
c1 = Client()
h = Humain()
c1.connection()
d= {1: "ptdr",2: "lol"}
c1.send_message(d)
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