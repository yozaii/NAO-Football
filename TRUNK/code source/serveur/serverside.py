# coding: utf-8
import select
import socket

#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
hote = ''
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
            msg_recu = msg_recu.decode()
            print("Reçu {}".format(msg_recu))
            client.send(b"5 / 5")
            if msg_recu == "fin":
                client.close()
                print("un client c'est déco")
                #serveur_est_lance = False

print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
ouvrir_connexion_avec_clients.close()