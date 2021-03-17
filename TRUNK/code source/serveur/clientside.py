# coding: utf-8
import socket
"""
#Permet d'ouvrir une connexion avec une machine local/distante
ouvrir_connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Nom d'hôte et de port afin de connecter notre socket
hote = "localhost"#socket.gethostbyname(socket.gethostname())
print(hote)
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
        print(msg_recu.decode("utf8"))
except ConnectionRefusedError:
    print("La connexion au serveur a échouée !")
finally:
    ouvrir_connexion_avec_serveur.close()
"""
#--------------------------------------------------------------------
hote = "192.168.56.1" #Doit être l'IP du serveur (ou nom DNS)
port = 10000
HEADER = 64
MESSAGE_DECONNECTION = "fin"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((hote, port))
except ConnectionRefusedError:
    print("La connexion au serveur a échouée !")

def envoyer_message(message=""):
    msg = message.encode("utf8")
    taille_msg = len(msg)
    taille_msg = str(taille_msg).encode("utf8")
    taille_msg += b' ' * (HEADER - len(taille_msg))
    client.send(taille_msg)
    client.send(msg)
    print(client.recv(1024).decode("utf8"))

envoyer_message("Salut les gars !")
envoyer_message(MESSAGE_DECONNECTION)