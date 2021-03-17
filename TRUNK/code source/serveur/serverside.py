# coding: utf-8
import select
import socket
import threading
"""
#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
hote = 'localhost'
port = 10000 #ceux entre 0 et 1023 sont réservé au système
ouvrir_connexion_avec_clients.bind((hote, port)) #connecte notre socket

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
                [], [], 0.1)
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

hote = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
print(hote)
port = 10000
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((hote, port))
HEADER = 64

def connexion_client(socket_client=None, adresse_client=None):

    print(f"{adresse_client} c'est connecté !")
    est_connecte = True

    while est_connecte:
        taille_msg = socket_client.recv(HEADER).decode("utf8")
        if taille_msg:
            taille_msg = int(taille_msg)
            msg = socket_client.recv(taille_msg).decode("utf8")
            print(f"{adresse_client} a envoyé : {msg}")
            if msg == "fin":
                est_connecte = False
                socket_client.send("Je te déconnecte".encode("utf8"))
            else:
                socket_client.send("J'ai bien reçu ton message".encode("utf8"))
    
    socket_client.close()

def envoyer_message():
    """
        On envoie un message d'un autre client
    """

def lancer():
    #sockets_lu = []
    print("[DEMMARAGE] LE SERVEUR A ÉtÉ LANCÉ")
    serveur.listen(5)
    print(f"[ÉCOUTE] LE SERVEUR ÉCOUTE A L'ADRESSE {hote, port}")
    while True:
        #sockets_lu, sockets_ecrit, sockets_erreur = select.select([serveur], [], [], 0.1)
        socket_client, adresse_client = serveur.accept()
        thread_connexion = threading.Thread(target=connexion_client, args=(socket_client, adresse_client))
        thread_connexion.start()
        
lancer()