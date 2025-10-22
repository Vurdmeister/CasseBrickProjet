"""
Utf-8
Oscar Lauger
Abdenour Benbouzid
3ETI
Objectif : Jeu du casse brique
Projet Debuté le 6 Octobre
"""
import tkinter as tk
from math import *
from cassebrique import CasseBrique
from regle import Regle
import json # Format pour l'utilisation des PIL
import os

# Création d'une classe pour chaque affichage différent d'une interface en commencant par un menu
# Utilisation de l'héritage

class CasseBriqueApp(CasseBrique):
    def __init__(self, root):
        self.root = root
        self.root.title("Casse-brique")
        self.root.geometry("515x575")
        self.root.resizable(False, False)

        # Liste pour stocker les scores
        self.scores = []
        # Frame principale (on alterne entre menu et jeu)
        self.frame_actuelle = None
        self.afficher_menu()

    # PAGE MENU 
    def afficher_menu(self):
        """Affiche le menu principal"""
        self.detruire_frame_actuelle()

        self.frame_actuelle = tk.Frame(self.root, bg="black")
        self.frame_actuelle.pack(fill="both", expand=True)

        titre = tk.Label(self.frame_actuelle, text=" Casse-Brique ", font=("Arial", 24, "bold"), fg="white", bg="black")
        titre.grid(column = 1,row = 0,pady=20)

        # Bouton pour lancer la fenêtre du jeu (Niveau 1)
        bouton_jouer = tk.Button(self.frame_actuelle, text="NIVEAU 1", font=("Arial", 10, "bold"),
                                 width=10, height=2, command=self.lancer_jeu)
        bouton_jouer.grid(column = 0,row = 1,pady=20,padx = 35)

        # Bouton pour lancer la fenêtre du jeu (Niveau 2)
        bouton_jouer = tk.Button(self.frame_actuelle, text="NIVEAU 2", font=("Arial", 10, "bold"),
                                 width=10, height=2, command=self.lancer_jeu2)
        bouton_jouer.grid(column = 1,row = 1,pady=20)

        # Bouton pour lancer la fenêtre du jeu (Niveau 3)
        bouton_jouer = tk.Button(self.frame_actuelle, text="NIVEAU 3", font=("Arial", 10, "bold"),
                                 width=10, height=2, command=self.lancer_jeu3)
        bouton_jouer.grid(column = 2,row = 1,pady=20)

        # Bouton pour lancer les règles du jeu
        bouton_regle = tk.Button(self.frame_actuelle, text="REGLES", font=("Arial", 10, "bold"),
                                 width=10, height=2, command=self.lancer_regles)
        bouton_regle.grid(column = 1,row = 2,pady=20)

        # Boutton pour quitter le menu
        bouton_quitter = tk.Button(self.frame_actuelle, text="QUITTER", font=("Arial", 10),
                                   width=10, height=2, command=self.root.destroy)
        bouton_quitter.grid(column = 1,row = 3,pady=20)

        self.afficher_scores_menu()

    # LANCEMENT DU JEU 
    def lancer_jeu(self):
        """Lance du niveau 1 du casse-brique"""
        self.detruire_frame_actuelle()
        self.frame_actuelle = CasseBrique(self.root, self.retour_menu, self.ajouter_score,self.sauvegarder_scores,1)
    
    def lancer_jeu2(self):
        """Lance du niveau 2 du casse-brique"""
        self.detruire_frame_actuelle()
        self.frame_actuelle = CasseBrique(self.root, self.retour_menu, self.ajouter_score,self.sauvegarder_scores,2)

    def lancer_jeu3(self):
        """Lance du niveau 2 du casse-brique"""
        self.detruire_frame_actuelle()
        self.frame_actuelle = CasseBrique(self.root, self.retour_menu, self.ajouter_score,self.sauvegarder_scores,3)

    # LANCEMENT DES REGLES
    def lancer_regles(self):
        """Explique les règles du jeu"""
        self.detruire_frame_actuelle()
        self.frame_actuelle = Regle(self.root, self.retour_menu)

    def retour_menu(self):
        """Retourne au menu principal"""
        self.afficher_menu()

    def ajouter_score(self, score):
        """Ajoute le score actuel à la liste des meilleurs scores"""
        self.scores.append(score)

    def detruire_frame_actuelle(self):
        """Détruit le frame courant (menu ou jeu)"""
        if self.frame_actuelle is not None:
            self.frame_actuelle.destroy()

    def afficher_scores_menu(self):
        """Affiche le meilleur score et les 3 derniers scores dans le menu"""
        data = self.charger_scores()
        meilleur_score = data.get("meilleur_score", 0)
        derniers = data.get("derniers_scores", [])

        # Affiche meilleur score
        label_meilleur = tk.Label(self.frame_actuelle,
                                  text=f"🏆 Meilleur score : {meilleur_score}",
                                  fg="gold", bg="black", font=("Arial", 16, "bold"))
        label_meilleur.grid(column = 1,row = 4,pady=20)

        # Affiche les 3 derniers scores s’ils existent
        if derniers:
            texte_derniers = " | ".join(str(s) for s in derniers)
            label_derniers = tk.Label(self.frame_actuelle,
                                      text=f" Derniers scores : {texte_derniers}",
                                      fg="white", bg="black", font=("Arial", 14))
            label_derniers.grid(column = 1,row = 5,pady=20)

    def charger_scores(self):
        """Charge le fichier scores.json, crée un modèle vide si inexistant"""
        if not os.path.exists("scores.json"):
            data = {"meilleur_score": 0, "derniers_scores": []}
            with open("scores.json", "w") as f:
                json.dump(data, f)
            return data
        with open("scores.json", "r") as f:
            return json.load(f)

    def sauvegarder_scores(self, nouveau_score):
        """Met à jour le meilleur et les 3 derniers scores"""
        data = self.charger_scores()

        # Mise à jour des derniers scores
        data["derniers_scores"].insert(0, nouveau_score)
        data["derniers_scores"] = data["derniers_scores"][:3]

        # Mise à jour du meilleur score
        if nouveau_score > data.get("meilleur_score", 0):
            data["meilleur_score"] = nouveau_score

        # Sauvegarde dans le fichier
        with open("scores.json", "w") as f:
            json.dump(data, f, indent=4)

        # Stocke aussi dans la liste temporaire
        self.scores.append(nouveau_score)

# Lancement du jeu
if __name__ == "__main__":
    root = tk.Tk()
    app = CasseBriqueApp(root)
    root.mainloop()

