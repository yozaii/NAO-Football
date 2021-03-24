# coding: utf-8
import pickle
import select
import socket
import threading
import unittest
"""
#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
host = 'localhost'
port = 10000 #ceux entre 0 et 1023 sont réservé au système
ouvrir_connexion_avec_clients.bind((host, port)) #connecte notre socket

#Le serveur se met à écouter et peut refuser jusqu'à 5 connexions avant de ne plus rien accepter 
ouvrir_connexion_avec_clients.listen(5)

serveur_est_lance = True
clients_connectes = []
while serveur_est_lance:
    #On écoute si des sockets sont prêt à être lus, au bout de 100ms on retourne une liste de sockets si aucuns changement d'état n'a été détecté
    connexions_demandees, wlist, xlist = select.select([ouvrir_connexion_avec_clients], [], [], 0.1)
    
    for connexion in connexions_demandees:
        #Accepte la connexion d'un client (méthode bloquante)
        socket_client, adresse_client = connexion.accept()
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(socket_client)
    
    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 100ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,
                [], [], 00.1)
    except select.error:
        pass
    else:
        # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            # Client est de type socket
            msg_recu = client.recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode("utf8")
            print("Reçu {}".format(msg_recu))
            client.send(b"5 / 5")
            if msg_recu == "fin":
                print("un client c'est déco")
                serveur_est_lance = False

print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
ouvrir_connexion_avec_clients.close()
"""
#-----------------------------------------------------------------------------------------------
class Server:
    host = socket.gethostbyname(socket.gethostname())
    port = 10000
    HEADER = 64
    DISCONNECTION_MESSAGE = "fin"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    def starting_server():
        #sockets_lu = []
        print("[DEMMARAGE] LE SERVEUR A ÉtÉ LANCÉ")
        Server.server.listen(5)
        print(f"[ÉCOUTE] LE SERVEUR ÉCOUTE A L'ADRESSE {Server.host, Server.port}")
        while True:
            #sockets_lu, sockets_ecrit, sockets_erreur = select.select([serveur], [], [], 0.1)
            socket_client, adresse_client = Server.server.accept()
            thread_connexion = threading.Thread(target=Server.client_connection, args=(socket_client, adresse_client))
            thread_connexion.start()
    
    starting_server = staticmethod(starting_server)

    def client_connection(socket_client=None, adresse_client=None):

        print(f"{adresse_client} c'est connecté !")
        is_connected = True

        while is_connected:
            msg = socket_client.recv(1024)
            #unpickler = pickle.Unpickler(msg)
            msg = pickle.loads(msg)
            print(f"{adresse_client} a envoyé : {msg}")
            if msg == Server.DISCONNECTION_MESSAGE:
                is_connected = False
                socket_client.send("Je te déconnecte".encode("utf8"))
            else:
                socket_client.send("J'ai bien reçu ton message".encode("utf8"))
                #Server.send_message(socket_client)
        
        socket_client.close()
    
    client_connection = staticmethod(client_connection)

    def send_message(message_socket=None):
        Server.server.sendto(message_socket, "ip de coach")
        

#Server.starting_server()

class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_client_connection_with_no_arguments(self):
        self.assertRaises(Exception,Server.client_connection)
    
    def test_client_connection_RaisesIllegalArgument(self):
         self.assertRaises(Exception,Server.client_connection, ("je veux une erreur", None))

    def test_send_message_with_IllegaleArgument(self):
        self.assertRaises(Exception,Server.send_message, ("je veux une erreur", None))


if __name__ == "__main__":

    unittest.main()