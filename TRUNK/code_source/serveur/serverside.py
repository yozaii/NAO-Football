# coding: utf-8
import pickle
import socket
import threading
import unittest
 
class Server:
    host = socket.gethostbyname(socket.gethostname())
    port = 10000
    HEADER = 64
    DISCONNECTION_MESSAGE = "fin"
    clients = set()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    def starting_server():
        """
        Start the server and show where he's listening
        """
        print "[DEMMARAGE] LE SERVEUR A EtE LANCE"
        Server.server.listen(5)
        print "[ECOUTE] LE SERVEUR ECOUTE A L'ADRESSE "+str(Server.host)+ ","+str(Server.port)
        while True:
            socket_client, adresse_client = Server.server.accept()
            if socket_client not in Server.clients: #add the clients in a dynamic table
                Server.clients.add(socket_client)
            thread_connexion = threading.Thread(target=Server.client_connection, args=(socket_client, adresse_client))
            thread_connexion.start()
    
    starting_server = staticmethod(starting_server)

    def client_connection(socket_client=None, adresse_client=None):
        """
        Take the connection with a client,
        and catch his message
        """
        print str(adresse_client)+" c'est connecte !"
        is_connected = True

        while is_connected:
            msg = socket_client.recv(1024)
            if len(msg) > 0:
                msg = pickle.loads(msg)
                print str(adresse_client) +"a envoye : "+str(msg)
                if msg == Server.DISCONNECTION_MESSAGE:
                    is_connected = False
                    socket_client.send("Je te deconnecte".encode("utf8"))
                else:
                    Server.broadcast(socket_client, pickle.dumps(msg))
                    #socket_client.send("J'ai bien recu ton message".encode("utf8"))
        if adresse_client in Server.clients:
            Server.clients.remove(socket_client)
        socket_client.close()
    
    client_connection = staticmethod(client_connection)

    def broadcast(adress_sender=None, message_socket=None):
        """
        Send to others clients the message that the current
        client has sent to the server
        """
        for client in Server.clients:
            if adress_sender != client and len(Server.clients) != 0:
                client.send(message_socket)
    
    broadcast = staticmethod(broadcast)
        

#Server.starting_server()

class TestServer(unittest.TestCase):

    def test_client_connection_with_no_arguments(self):
        """
        Raise an exception for the client_connection methode when I don't pass arguments
        """
        self.assertRaises(Exception,Server.client_connection)
    
    def test_client_connection_RaisesIllegalArgument(self):
        """
        Raise an exception for the client_connection methode when I pass illegal arguments
        """
        self.assertRaises(Exception,Server.client_connection, ("je veux une erreur", None))

    def test_broadcast_with_IllegaleArgument(self):
        """
        Raise an exception for the broadcast methode when I pass illegal arguments
        """
        self.assertRaises(Exception, Server.broadcast, ("je veux une erreur", None, "erreur"))

    


if __name__ == "__main__":

    unittest.main()