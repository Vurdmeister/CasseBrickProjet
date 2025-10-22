"""
Utf-8
Oscar Lauger
Abdenour Benbouzid
3ETI
Objectif : Jeu du casse brique
"""
import tkinter as tk
from random import uniform, randint
from math import radians, sin, cos

# Création d'un classe pour l'affichage complet du casse-brique et son fonctionnement
class CasseBrique(tk.Frame):
    def __init__(self, root, retour_menu, ajouter_score,sauvegarder_scores,Niveau):
        super().__init__(root, bg="black")
        self.pack(fill="both", expand=True)

        # Rappels vers la classe principale
        self.retour_menu = retour_menu

        # Ajouter les scores dans le menu 
        self.ajouter_score = ajouter_score

        # Sauvegarder dans un fichier json les scores pour afficher les derniers et meilleur score
        self.sauvegarder_scores = sauvegarder_scores

        # Niveau de dificulté
        self.Niveau=Niveau

        # Liste des couleurs des blocs
        self.colors = ["blue", "green", "orange", "purple", "pink", "cyan", "magenta", "gold"]

        # Canvas principal
        self.Largeur = 510
        self.Hauteur = 500
        self.canva = tk.Canvas(self, width=self.Largeur, height=self.Hauteur, bg='black')
        self.canva.grid(column=0, row=1, columnspan=3)

        # Labels score et vie
        self.score_label = tk.Label(self, text="Score : 0", fg='white', bg='black', font=("Arial", 12))
        self.score_label.grid(column=0, row=0, sticky='w', padx=20)

        self.vie_label = tk.Label(self, text="Vies : 3", fg='white', bg='black', font=("Arial", 12))
        self.vie_label.grid(column=2, row=0, sticky='e', padx=20)

        # Bouton retour menu
        self.bouton_menu = tk.Button(self, text='Retour Menu', command=self.retour_menu, font=("Arial", 10))
        self.bouton_menu.grid(column=1, row=0)

        # Bouton lancement du jeu
        self.bouton_jouer = tk.Button(self, text='Jouer', command=self.lancer_jeu, font=("Arial", 10))
        self.bouton_jouer.grid(column=0, row=2, pady=10)

        # Initialisation
        self.initialiser_jeu()

        # États du clavier
        self.left_pressed = False
        self.right_pressed = False

        # Activation clavier fluide
        self.bind_all("<KeyPress>", self.key_press)
        self.bind_all("<KeyRelease>", self.key_release)

        # Lancer la boucle fluide (toujours active)
        self.deplacement_fluide()

    def initialiser_jeu(self):
        """Initialisation du jeu"""
        self.canva.delete("all")
        self.en_jeu = False
        self.score = 0
        self.vies = 3

        # Apelle création balle
        
        self.CreationBalle()

        # Création barre
        self.PosXB = 250
        self.largeur_barre = 100
        self.Barre = self.canva.create_rectangle(
            self.PosXB - self.largeur_barre // 2, 460,
            self.PosXB + self.largeur_barre // 2, 473,
            fill='red'
        )

        # Création blocs
        self.blocs = []
        self.CreationBlock()

        self.update_labels()

    def CreationBalle(self):
        # Création balle
        self.PosX = 250
        self.PosY = 300
        self.R = 9
        self.vitesse = 2
        if self.Niveau == 2:
            self.vitesse = 3
        if self.Niveau == 3:
            self.vitesse = 4
        self.angle = uniform(0.4, 2.6)
        self.DX = self.vitesse * cos(self.angle)
        self.DY = -abs(self.vitesse * sin(self.angle))
        self.ball = self.canva.create_oval(self.PosX - self.R, self.PosY - self.R,
                                           self.PosX + self.R, self.PosY + self.R, fill='yellow')
        
    def CreationBlock(self):
        """Création des blocs colorés"""
        x0, y0, x1, y1 = 10, 25, 72, 55
        for _ in range(6):
            for _ in range(8):
                color = self.colors[randint(0, len(self.colors) - 1)] # Choix de la couleur random
                block = self.canva.create_rectangle(x0, y0, x1, y1, width=2, fill=color) # Création d'un block
                self.blocs.append(block)
                # Déplace les coordonnées
                x0 += 61.5
                x1 += 61.5
            x0, x1 = 10, 72
            y0 += 30
            y1 += 30

    # --- GESTION CLAVIER FLUIDE ---
    def key_press(self, event):
        """Quand une touche est pressée"""
        if not self.en_jeu:
            return
        if event.keysym in ('Left', 'q'):
            self.left_pressed = True
        elif event.keysym in ('Right', 'd'):
            self.right_pressed = True

    def key_release(self, event):
        """Quand une touche est relâchée"""
        if event.keysym in ('Left', 'q'):
            self.left_pressed = False
        elif event.keysym in ('Right', 'd'):
            self.right_pressed = False

    def deplacement_fluide(self):
        """Boucle continue pour déplacement fluide"""
        if self.en_jeu:
            if self.left_pressed:
                self.deplacerBarre(-5)
            if self.right_pressed:
                self.deplacerBarre(5)

        # Relancer cette vérification toutes les 15 ms
        self.after(15, self.deplacement_fluide)

    # --- DÉPLACEMENT et LOGIQUE JEU ---
    def deplacerBarre(self, dx):
        """Déplace la barre dans les limites"""
        x1, y1, x2, y2 = self.canva.coords(self.Barre)
        if 0 <= x1 + dx and x2 + dx <= self.Largeur:
            self.canva.move(self.Barre, dx, 0)
            self.PosXB += dx

    def lancer_jeu(self):
        """Démarre le mouvement de la balle et de la barre"""
        if not self.en_jeu:
            self.en_jeu = True
            self.bouton_jouer.config(state=tk.DISABLED)
            self.deplacementB()

    def deplacementB(self):
        """Déplacement et collisions"""
        if not self.en_jeu:
            return

        self.PosX += self.DX
        self.PosY += self.DY
        
        # Collision de la balle sur les murs
        if self.PosX - self.R <= 0 or self.PosX + self.R >= self.Largeur:
            self.DX = -self.DX
        if self.PosY - self.R <= 0:
            self.DY = -self.DY

        # Collision avec la barre 
        xb1, yb1, xb2, yb2 = self.canva.coords(self.Barre)
        if yb1 <= self.PosY + self.R <= yb2 and xb1 <= self.PosX <= xb2:
            # Remonte légèrement la balle pour éviter qu’elle reste collée
            self.PosY = yb1 - self.R
            self.DY = -abs(self.DY)

            # Calcul plus réaliste du rebond selon la position d'impact
            centre_barre = (xb1 + xb2) / 2
            distance_centre = self.PosX - centre_barre
            ratio = distance_centre / (self.largeur_barre / 2)

            # Angle progressif : plus tu touches sur les bords, plus ça part en diagonale
            max_angle = 60  # Angle max en degrés sur les bords
            angle = ratio * max_angle
            vitesse = (self.DX**2 + self.DY**2)**0.5

            self.DX = vitesse * sin(radians(angle))
            self.DY = -vitesse * cos(radians(angle))

        # Collision avec les blocs 
        for block in self.blocs[:]:
            x1, y1, x2, y2 = self.canva.coords(block)

            # Collision horizontale 
            if x1 <= self.PosX <= x2 and (y1 <= self.PosY + self.R + 0.5 <= y2 or y1 <= self.PosY - self.R - 0.5 <= y2):
                self.canva.delete(block)
                self.blocs.remove(block)

                if self.Niveau == 1 :
                    self.DY = -1.02 * self.DY
                    self.score += 10

                if self.Niveau == 2:
                    self.DY = -1.03 * self.DY
                    self.score += 20

                if self.Niveau == 3:
                    self.DY = -1.05 * self.DY
                    self.score += 30
                    

                self.update_labels()
                break

            # Collision verticale
            elif y1 <= self.PosY <= y2 and (x1 <= self.PosX + self.R + 0.5 <= x2 or x1 <= self.PosX - self.R - 0.5 <= x2):
                self.canva.delete(block)
                self.blocs.remove(block)

                if self.Niveau == 1 :
                    self.DX = -1.01 * self.DX
                    self.score += 10

                if self.Niveau == 2:
                    self.DX = -1.03 * self.DX
                    self.score += 20

                if self.Niveau == 3:
                    self.DX = -1.05 * self.DX
                    self.score += 30

                self.update_labels()
                break

        # Perte de vie
        if self.PosY + self.R >= self.Hauteur:
            self.vies -= 1
            self.score -= 50
            self.update_labels()
            if self.vies <= 0:
                self.game_over("PERDU")
                return
            self.reset_balle()

        # Victoire
        if not self.blocs:
            self.game_over("GAGNÉ")
            return
        
        # Remise à la position initiale de la balle
        self.canva.coords(self.ball, self.PosX - self.R, self.PosY - self.R,
                          self.PosX + self.R, self.PosY + self.R) 
        self.after(10, self.deplacementB) # Attente de 10ms avant deplacement

    def reset_balle(self):
        """Remet la balle au centre"""
        self.PosX, self.PosY = 250, 300
        self.angle = uniform(0.4, 2.6)
        self.DX = self.vitesse * cos(self.angle)
        self.DY = -abs(self.vitesse * sin(self.angle))

    def update_labels(self):
        """Met à jour score et vies"""
        self.score_label.config(text=f"Score : {self.score}")
        self.vie_label.config(text=f"Vies : {self.vies}")

    def game_over(self, message):
        """Fin de partie"""
        self.en_jeu = False
        self.sauvegarder_scores(self.score)
        self.ajouter_score(self.score)
        self.canva.create_text(self.Largeur // 2, self.Hauteur // 2,
                               text=message, fill="white", font=("Arial", 25, "bold"))
        bouton_rejouer = tk.Button(self, text="Rejouer", command=self.rejouer)
        bouton_rejouer.grid(column=1, row=2, pady=10)

    def rejouer(self):
        """Relance une partie"""
        self.initialiser_jeu()
        self.bouton_jouer.config(state=tk.NORMAL)