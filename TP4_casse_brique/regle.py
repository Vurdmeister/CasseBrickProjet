"""
Utf-8
Oscar Lauger
Abdenour Benbouzid
3ETI
Objectif : Jeu du casse brique
"""
import tkinter as tk

# Création d'une classe pour les règles

class Regle(tk.Frame):
    def __init__(self, root, retour_menu):
        super().__init__(root, bg="black")
        self.pack(fill="both", expand=True)

        # Rappels vers la classe principale
        self.retour_menu = retour_menu

        # Bouton retour menu
        self.bouton_menu = tk.Button(self, text='Retour Menu', command=self.retour_menu, font=("Arial", 10))
        self.bouton_menu.grid(column=0, row=0)

        # Règles scores et vies
        self.regle_score = tk.Label(self, text="Vous obtenez du scores à chaque brique toucher\n" \
        " 10 pour le Niveau 1, 20 pour le 2 et 30 pour le 3.\n" \
        " et vous perdez -50 de score si vous perdez une vie.\n" \
        " A chaque brique toucher la balle augmente de vitesse. \n" \
        " Si vous perdez une vie, remise à 0 de la vitesse.\n" \
        "Vous avez un total de 3 vies.\n"\
        "deplacement avec Q et D ou flèche gauche et droite "   ,fg='white', bg='black', font=("Arial", 14))
        self.regle_score.grid(column=0, row=1,padx = 15, pady = 100)
