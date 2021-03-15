# coding: utf-8
 
from tkinter import * 

#Création de la fenêtre de TKinter
window = Tk()

#Personnalisation de la fenêtre
window.title("Données des robots")
window.geometry("480x320")
window.config(background='green')
window.resizable(width=0, height=0)

#Création de frame (boîte)
frame = Frame()

#Ajout de texte
texte = Label(window, text="On devra mettre en entrée les données des robots", )
texte.pack() 

#Affiche la fenêtre
window.mainloop()