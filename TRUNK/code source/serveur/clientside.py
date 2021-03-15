# coding: utf-8
import socket

#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
hote = "localhost"
port = 10000 #ceux entre 0 et 1023 sont réservé au système


try:
    ouvrir_connexion_avec_serveur.connect((hote, port))

    msg_a_envoyer = b""
    while msg_a_envoyer != b"fin":
        msg_a_envoyer = input("> ")
        # Peut planter si vous tapez des caractères spéciaux
        msg_a_envoyer = msg_a_envoyer.encode("utf8")
        # On envoie le message
        ouvrir_connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu = ouvrir_connexion_avec_serveur.recv(1024)
        print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
    """
    ouvrir_connexion_avec_serveur.connect((hote,port))
    donnees = "Test pour le serveur ok !"
    donnees = donnees.encode("utf8")

    socket.socket.sendall(donnees)"""
except ConnectionRefusedError:
    print("La onnexion au serveur a échouée !")
finally:
    ouvrir_connexion_avec_serveur.close()

