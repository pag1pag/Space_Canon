# Version Finale - Space Canon - Jessy Ribaira & Pierre-Antoine Goutier

from math import sqrt, tan, radians
import os

# permet de savoir l'emplacement dans lequel ce programme est executé
chemin = os.path.dirname(os.path.abspath(__file__))

# Change l'emplacement pour récuperer les images de facon relative et non plus absolu
os.chdir(chemin)

# --Gestion des erreurs--#
# -Version de Python-#
try:
    import tkinter as tk  # python 3.X
except ImportError:
    import Tkinter as tk  # python 2.X

# -images-#
try:
    with open("Images/Fond_ecran.png"):
        pass
    with open("Images/Jouer.png"):
        pass
    with open("Images/Options.png"):
        pass
    with open("Images/Quitter.png"):
        pass
    with open("Images/Fleche_retour.png"):
        pass
    with open("Images/NewtonDrawing.png"):
        pass
except IOError:
    print(
        "Erreur! Le dossier 'Images' et/ou une image n'a (ont) pas pu etre ouvert(es)... Il(Elle) n'existe(nt) "
        "peut-etre plus ou le dossier image n'est pas dans le même dossier que celui de ce fichier")
    os.sys.exit(0)

# -vérification des modules non implémentés de base dans Python-#
try:
    import PIL.Image
    import PIL.ImageTk
except ImportError:
    print("Erreur ! Vous devez installer le module PIL ou PILLOW suivant la version de python (Veuillez récuperer la \
          dernière version d'un de ces modules). \n Voici le protocole a suivre si vous possèder python 3.x >= 3.4 \
          ou 2.x >= 2.7.9 (sinon installer le module 'pip'):\n - Ouvrez l'explorateur de fichier et tapez 'cmd' \
          puis dirigez vous dans le dossier 'Scripts' de Python (utilisez la commande 'cd')\n - Une fois dans \
          l'emplacement du dossier dans l'interpreteur de commande, taper la commande suivante 'pip install Pillow' \
          ou 'easy_install Pillow'\n - Il ne vous reste plus qu'a relancer ce programme pour pouvoir l'utiliser")
    os.sys.exit(0)


class Menu(tk.Canvas):
    """Affiche un menu avec plusieurs images. Ce menu permet de choisir entre 'jouer', 'options', et 'quitter'
    La fenêtre du menu s'adapte à  la taille de l'écran de l'utilisateur, contrairement aux autres fenêtres
    Le choix s'effectue en cliquant sur l'un des textes et ouvre une nouvelle fenêtre
    Menu hérite du Canvas, car c'est une toile sur laquelle on ajoute des images sur lesqulles on clique"""

    # Variables qui servent pour la couleur de la trajectoire et du boulet ainsi que la vitesse d'execution
    # et qui sont modifié dans les options mais utilisés dans le jeu
    couleur_boulet = "red"
    couleur_trajectoire = "magenta"
    vitesse_execution = 5

    def __init__(self, parent):
        """Méthode du constructeur"""
        tk.Canvas.__init__(self, parent)  # Menu hérite du Canvas. Pour éviter de surcharger la méthode __init__,
        # c'est-à -dire que la méthode __init__ du Menu écrase la méthode __init__ du canvas, on appelle
        # explicitement la méthode __init__ du canvas dans celle du menu, pour garder les attributs et les méthodes

        # Change le titre de la fenêtre et la met en plein écran
        self.parent = parent
        self.parent.title("Menu")
        self.parent.attributes('-fullscreen', 1)

        # Récupère la taille de l'écran (car la fenêtre est en plein écran) qui peut être différent suivant les
        # ordinateurs
        self.w = parent.winfo_screenwidth()
        self.h = parent.winfo_screenheight()

        # On crée un canvas et on l'affiche avec la méthode grid
        self.canvas = tk.Canvas(parent, width=self.w, height=self.h)
        self.canvas.grid(row=0, column=0)

        # On lie le canvas
        self.canvas.bind("<Button-1>", self.on_click)

        # On appelle la fonction "fonction_image" qui gère les images et leur commande
        self.fonction_image(self.w, self.h)

    def fonction_image(self, w, h):
        """Cette fonction permet la gestion des images
        Elle modifie la taille des images et les affiche"""

        def redimensionnage_image(chemin_image, nouvelle_largeur, nouvelle_hauteur, x, y, pos=tk.NW, tag="None",
                                  afficher=True):
            """Cette fonction modifie la taille des images Elle prend plusieurs paramètres d'entrée : - chemin_image
            : c'est l'endroit où se trouve l'image - nouvelle_hauteur & nouvelle_largeur : cela permet de modifier
            l'image pour qu'elle s'adapte à  la taille de l'écran - x & y : l'endroit où doit être afficher l'image -
            pos : permet de choisir si l'image doit être centrée, en haut à  gauche, etc..., par rapport au x et y -
            tag : attribue un nom de tag à  l'image qui pourra être utilisé après pour attribue une fontion à 
            l'image - afficher : Si la valeur vaut 'True', on affiche l'image dans la fenêtre du menu """

            self.image_pil = PIL.Image.open(chemin_image)  # Image au format PIL
            self.image_pil = self.image_pil.resize((nouvelle_largeur, nouvelle_hauteur))  # Redimensionnage de l'image
            self.image = PIL.ImageTk.PhotoImage(self.image_pil)  # Image au format Tk

            self.canvas.image = self.image  # On garde une référence de ces images pour éviter qu'elles disparaissent
            if afficher:  # Si les images doivent être afficher maintenant, on les affichhe
                self.canvas.create_image(x, y, anchor=pos, image=self.image, tags=tag)  # On affiche ces images

            # On renvoie l'image modifiée
            return self.image

        # On crée des variables pour le chemin des images
        chemin_fond_ecran = "Images/Fond_ecran.png"  # l'image avec des étoiles, la Terre, le titre, le canon,
        # le boulet et la Lune
        chemin_jouer = "Images/Jouer.png"  # L'image avec écrit dessus 'Jouer'
        chemin_option = "Images/Options.png"  # L'image avec écrit dessus 'Option'
        chemin_quitter = "Images/Quitter.png"  # L'image avec écrit dessus 'Quitter'
        chemin_fleche_retour = "Images/Fleche_retour.png"  # L'image avec la flèche jaune

        # On fait appel à  la fonction redimensionnage_image
        self.photo_fond_ecran = redimensionnage_image(chemin_fond_ecran, self.w, self.h, 0,
                                                      0)  # L'image 'Fond_ecran.png' est redimensionné à  la taille
        # de l'écran et placé en haut à  gauche
        self.photo_jouer = redimensionnage_image(chemin_jouer, int(self.w / 5), int(self.h / 8), int(self.w / 2),
                                                 int(self.h / 2) - int(self.h / 10), tag="jouer",
                                                 pos=tk.CENTER)  # 'Jouer.png' -> 1/5 de la largeur de l'écran,
        # 1/8 de la hauteur de l'écran, placé au centre de lécran, avec le tag 'jouer' et positionné de façon centré
        self.photo_options = redimensionnage_image(chemin_option, int(self.w / 5), int(self.h / 8), int(self.w / 2),
                                                   int(self.h / 2), tag="option", pos=tk.CENTER)
        self.photo_quitter = redimensionnage_image(chemin_quitter, int(self.w / 5), int(self.h / 8), int(self.w / 2),
                                                   int(self.h / 2) + int(self.h / 10), tag="quitter", pos=tk.CENTER)

        self.photo_fleche_retour = redimensionnage_image(chemin_fleche_retour, int(self.w / 10), int(self.h / 10), 0, 0,
                                                         afficher=False)  # On ne doit pas afficher tout de suite
        # l'image de la flèche de retour

    def on_click(self, event):
        """Cette fonction récupère les coordonnées des images et permet de savoir si on a cliqué dessus ou non
        Elle attribue aussi une fontion aux images en fonction de leur tag"""

        # La méthode 'bbox' permet de récupérer l'emplacement des images et renvoie sous forme de tuple les
        # coordonnées de l'image

        # Si le clic de la souris est compris entre le coté droit et le coté de gauche de l'image jouer (qui aurait
        # pu être l'image option ou l'image quitter car elles sont toutes centrées)
        if event.x in range(self.canvas.bbox("jouer")[0], self.canvas.bbox("jouer")[2]):
            # Si le clic de la souris est compris entre le coté haut et le coté de bas de l'image jouer
            if event.y in range(self.canvas.bbox("jouer")[1], self.canvas.bbox("jouer")[3]):
                # Effectuer la fonction play
                self.play()
            if event.y in range(self.canvas.bbox("option")[1], self.canvas.bbox("option")[3]):
                self.option()
            if event.y in range(self.canvas.bbox("quitter")[1], self.canvas.bbox("quitter")[3]):
                self.quit()

    def play(self):
        """Affiche le jeu"""
        # Crée une classe 'Jeu'
        Jeu(root)

    def option(self):
        """Affiche les options"""
        # Crée une classe 'Options'
        Options(root)

    def creation_fenetre(self, titre):
        """Permet de créer un modèle de fenêtre qui servira pour les classes héritantes de la classe Menu.
        Seul le titre change en fonction des fenêtres, c'est donc ce paramètre qu'on récupère"""
        self.nom_fenetre = tk.Toplevel(root)  # On crée une nouvelle fenêtre
        self.nom_fenetre.grab_set()  # La fenêtre va récupérer les événements
        self.nom_fenetre.focus_set()  # On met le focus sur la nouvelle fenêtre qui vient d'être crée
        self.nom_fenetre.resizable(False, False)  # Empêche le redimensionnement de la fenêtre
        self.nom_fenetre.title(titre)  # On donne un titre à  la fenêtre
        self.nom_fenetre.attributes('-fullscreen', 1)  # On met la fenêtre en pleine écran

        self.parent.withdraw()  # Fais disparaitre le menu

        return self.nom_fenetre  # On renvoie la fenêtre

    def back(self, nom_fenetre):
        """Créer un bouton de retour, prend en paramètre une fenêtre pour pouvoir placer le
        bouton dedans"""
        self.back_button = tk.Button(nom_fenetre, image=self.photo_fleche_retour,
                                     command=lambda nom_fenetre=nom_fenetre: self.quitter(nom_fenetre))
        return self.back_button

    def quitter(self, nom_fenetre):
        """Fonction qui fais disparaitre la fenêtre actuelle (jouer ou option) pour faire réapparaître le menu"""
        self.parent.deiconify()  # Fais réapparaître le menu
        nom_fenetre.withdraw()  # Fais disparaitre la fenêtre actuelle
        self.parent.grab_set()  # Le menu va récupérer les événements
        self.parent.focus_set()  # On remet le focus sur le menu


class Jeu(Menu):
    """Affiche le jeu. Hérite de la classe Menu"""

    def __init__(self, parent):
        Menu.__init__(self, parent)

        # Création d'une nouvelle fenêtre
        self.fenetre_jeu = self.creation_fenetre("Jeu !")

        # On crée un bouton de retour qui en fait supprime la fenêtre actuel et réaffiche l'autre fenêtre. Ce bouton
        # fait appel à  la fonction 'back'
        self.back(self.fenetre_jeu).grid(row=0, column=0, sticky="w")

        # --Variable--#
        # -Canvas & Image-#
        self.canvas_jeu = tk.Canvas(self.fenetre_jeu, width=600, height=600)  # création d'un canevas
        self.canvas_jeu.grid(row=1, column=0, rowspan=3)  # On affiche le canevas

        self.terre_image_pil = PIL.Image.open("Images/NewtonDrawing.png")  # on prend l'image dans un fichier externe
        self.terre_image_pil = self.terre_image_pil.resize((600, 600))  # Redimensionnage de l'image
        self.terre_image = PIL.ImageTk.PhotoImage(self.terre_image_pil)  # Image au format Tk

        self.canvas_jeu.terre_image = self.terre_image  # référence de l'image
        self.canvas_jeu.create_image(300, 300, image=self.terre_image)  # on met l'image dans le canevas

        # -Barre de vitesse et d'angle-#
        # Creation de la barre de vitesse : vitesse comprise entre 0 et 8000 m/s
        self.barreVitesse = tk.Scale(self.fenetre_jeu, orient='vertical', from_=0, to=8000, resolution=100, length=350,
                                     label='Vitesse (m/s)')
        self.barreVitesse.grid(row=1, column=1)  # affichage de la barre de vitesse

        # Création d'une barre d'angle : angle compris entre 0 et 45 degrées
        self.barreAngle = tk.Scale(self.fenetre_jeu, orient='vertical', from_=0, to=45, resolution=1, length=350,
                                   label='Angle (degrées)')
        self.barreAngle.grid(row=1, column=2)

        # -Boutons-#
        self.feu = tk.Button(self.fenetre_jeu, text='Feu', padx=50, pady=10,
                             command=lambda: self.FireProjectile())  # Creation du bouton 'Feu' qui lance le dessin
        # de la trajectoire
        self.stop = tk.Button(self.fenetre_jeu, text='Stop', padx=50, pady=10,
                              command=lambda: self.StopProjectile())  # Création d'un bouton 'Stop' qui arrête le boulet
        self.go = tk.Button(self.fenetre_jeu, text='Go', padx=50, pady=10,
                            command=lambda: self.GoProjectile())  # Creation du bouton 'Go' qui relance le boulet
        self.effacer = tk.Button(self.fenetre_jeu, text='Effacer les trajectoires', padx=50, pady=10,
                                 command=lambda: self.EffacerTrajectoire())  # Creation du bouton 'Effacer les
        # trajectoires' qui efface la trajectoire
        
        # Affichage des boutons
        self.feu.grid(row=2, column=1)
        self.stop.grid(row=3, column=1)
        self.go.grid(row=3, column=2)
        self.go.config(state=tk.DISABLED)  # Le bouton go est non cliquable au début
        self.effacer.grid(row=2, column=2)

        # -variable-#
        # coordonnees en pixel de la position du centre de la terre sur l'axe des x et des y
        self.centre_terre_x = 300
        self.centre_terre_y = 300
        # Lancer l'animation ou non
        self.marche = True

        self.RayonTerre = 6371000  # en metres
        self.TailleMontagne = self.RayonTerre * 0.165  # echelle pour adapter la taille de la montagne en pixel

    def FireProjectile(self):
        """La fonction qui est enclenché par le bouton 'Feu'
        Elle récupère les valeurs de la vitesse et de l'angle et réinitialise le boulet à  sa position de début"""
        global x, y, vx, vy

        self.GoProjectile()  # Pour pouvoir tirer si jamais on a quand même appuyé sur le bouton stop

        # reinitialisation des valeurs
        x = 0
        y = self.RayonTerre + self.TailleMontagne
        # vitesse initiale
        vx = self.barreVitesse.get()  # on prend la valeur de la vitesse initiale sur la barre de vitesse
        # angle de tir initial
        alpha = self.barreAngle.get()
        alpha = radians(alpha)
        vy = tan(alpha) * vx  # la vitesse en y

        # On appelle la fonction bouger projectile
        self.MoveProjectile()

    def MoveProjectile(self):
        """La fonction qui permet de savoir la position du boulet"""
        global x, y, vx, vy, marche
        newtonG = 6.67e-11  # constante gravitationnelle en unite de SI
        MasseTerre = 5.97e24  # en kiloggramme
        dt = 5  # le nombre de pas par seconde
        r = sqrt((x - self.centre_terre_x) ** 2 + (
                y - self.centre_terre_y) ** 2)  # la distance entre le centre du boulet et le centre de la Terre

        # Pour que le boulet s'arrête à  la surface de la Terre
        if r > self.RayonTerre:
            accel = newtonG * MasseTerre / (r * r)  # acceleration du boulet
            # vecteur accelerateur du boulet en x et en y
            ax = -accel * x / r  # l'accélaration en x
            ay = -accel * y / r  # l'accélaration en y
            vx += ax * dt  # la vitesse en x
            vy += ay * dt  # la vitesse en y
            x += vx * dt  # la position en x
            y += vy * dt  # la position en y

            self.DrawProjectile()  # On appelle la fonction qui va dessiner le boulet et la trajectoire

            if self.marche:  # Si on n'a pas cliqué sur le bouton stop
                root.after(Menu.vitesse_execution,
                           self.MoveProjectile)  # Permet la récursivité de la fonction 'MoveProjectile',
                # c'est-à -dire que la fonction va être réappelée encore et encore

    def DrawProjectile(self):
        global x, y
        """La fonction qui permet de dessiner le boulet et sa trajectoire"""
        self.canvas_jeu.delete(
            "boulet")  # On efface le boulet à  chaque fois que la fonction est appelée car sinon on verrait une
        # succession de boulet alors qu'on veut voir le boulet bouger

        # l'echelle mise en place: adapter les metres en pixels
        MetresParPixel = self.RayonTerre / (0.355 * self.canvas_jeu.winfo_width())
        pixelX = self.canvas_jeu.winfo_width() / 2 + x / MetresParPixel
        pixelY = self.canvas_jeu.winfo_height() / 2 - y / MetresParPixel  # pixel coordinates measured down from the top
        # dessine le boulet
        Boulet = self.canvas_jeu.create_oval(pixelX - 5, pixelY - 5, pixelX + 5, pixelY + 5, fill=Menu.couleur_boulet,
                                             tags="boulet")
        # dessine la trajectoire du boulet
        Trajectoire = self.canvas_jeu.create_line(pixelX - 1, pixelY - 1, pixelX, pixelY, fill=Menu.couleur_trajectoire,
                                                  tags="trajectoire")

    def StopProjectile(self):
        """Permet d'arrêter le dessin"""
        global marche
        self.marche = False
        self.stop.config(state=tk.DISABLED)  # On change l'état du bouton stop en désactivé
        self.go.config(state=tk.NORMAL)  # On change l'état du bouton go en activé

    def GoProjectile(self):
        """Permet d'arrêter le dessin"""
        global marche
        self.marche = True
        self.go.config(state=tk.DISABLED)  # On change l'état du bouton go en désactivé
        self.stop.config(state=tk.NORMAL)  # On change l'état du bouton stop en activé

    def EffacerTrajectoire(self):
        """Efface la trajectoire du boulet"""
        self.canvas_jeu.delete("trajectoire")


class Options(Menu):
    """Affiche les options. Hérite de la classe Menu"""

    def __init__(self, parent):
        Menu.__init__(self, parent)

        # Création d'une nouvelle fenêtre
        self.Fenetre_Options = self.creation_fenetre("Option")

        # On crée un bouton de retour qui en fait supprime la fenêtre actuel
        self.back(self.Fenetre_Options).grid(row=0, column=0)

        # Plusieurs couleurs
        COULEURS = [
            ("Violet", "magenta", 1),
            ("Rouge", "red", 2),
            ("Vert", "green", 3),
            ("Bleu", "blue", 4),
        ]

        # Création d'un label
        self.texte_aide = tk.Label(self.Fenetre_Options, text="Vous voici dans les options du jeu !")
        self.texte_aide.config(font=("Courier", 44))  # On modifie la police et la taille d'écriture du texte
        self.texte_aide.grid(row=0, column=1, columnspan=len(
            COULEURS))  # On affiche le label, 'columnspan' permet d'étendre le texte sur plusieurs colonnes

        # -Couleur du boulet-#
        # Texte qui change de couleur pour le boulet
        self.texte_couleur_boulet = tk.Label(self.Fenetre_Options, text="\nCouleur du boulet\n", fg=Menu.couleur_boulet)
        self.texte_couleur_boulet.config(font=("Comic", 30))
        self.texte_couleur_boulet.grid(row=1, column=1, columnspan=len(COULEURS))

        # Une variable qui servira pour un radiobutton qui sert à  faire un seul choix parmi plusieurs
        self.couleurBoulet = tk.StringVar()
        self.couleurBoulet.set(Menu.couleur_boulet)  # Permet de mettre la valeur situé dans la variable du Menu

        # Création du radiobutton
        for texte, couleur, i in COULEURS:
            radiobutton_couleurBoulet = tk.Radiobutton(self.Fenetre_Options, text=texte, variable=self.couleurBoulet,
                                                       value=couleur, indicatoron=0, command=lambda
                    couleurBoulet=self.couleurBoulet: self.changement_couleur_boulet(couleurBoulet))
            radiobutton_couleurBoulet.grid(row=2, column=i, sticky="NESW", ipady=10)

        # -Couleur de la trajectoire-#
        # Texte qui change de couleur pour la trajectoire
        self.texte_couleur_trajectoire = tk.Label(self.Fenetre_Options, text="\nCouleur de la trajectoire\n",
                                                  fg=Menu.couleur_trajectoire)
        self.texte_couleur_trajectoire.config(font=("Comic", 30))
        self.texte_couleur_trajectoire.grid(row=3, column=1, columnspan=len(COULEURS))

        # Une variable qui servira pour un radiobutton qui sert à  faire un seul choix parmi plusieurs
        self.couleurTrajectoire = tk.StringVar()
        self.couleurTrajectoire.set(
            Menu.couleur_trajectoire)  # Permet de mettre la valeur situé dans la variable du Menu

        # Création du radiobutton
        for texte, couleur, i in COULEURS:
            radiobutton_couleurTrajectoire = tk.Radiobutton(self.Fenetre_Options, text=texte,
                                                            variable=self.couleurTrajectoire, value=couleur,
                                                            indicatoron=0, command=lambda
                    couleurTrajectoire=self.couleurTrajectoire: self.changement_couleur_trajectoire(couleurTrajectoire))
            radiobutton_couleurTrajectoire.grid(row=4, column=i, sticky="NESW", ipady=10)

        # -vitesse d'éxecution-#
        # Label de la vitesse
        self.texte_vitesse_execution = tk.Label(self.Fenetre_Options, text="\nVitesse d'execution du dessin\n")
        self.texte_vitesse_execution.config(font=("Comic", 30))
        self.texte_vitesse_execution.grid(row=5, column=1, columnspan=len(COULEURS))

        # à‰chelle de la vitesse
        self.vitesse_execution = tk.Scale(self.Fenetre_Options, from_=1, to=100, resolution=1, orient="horizontal",
                                          length=400, command=self.changement_vitesse_execution)
        self.vitesse_execution.set(Menu.vitesse_execution)  # Permet de mettre la valeur situé dans la variable du Menu
        self.vitesse_execution.grid(row=6, column=1, columnspan=len(COULEURS))

    def changement_couleur_boulet(self, couleurBoulet):
        """Fonction qui modifie la variable couleur_boulet situé dans le Menu en fonction du choix de la couleur"""
        self.texte_couleur_boulet.config(fg=couleurBoulet.get())
        Menu.couleur_boulet = couleurBoulet.get()

    def changement_couleur_trajectoire(self, couleurTrajectoire):
        """Fonction qui modifie la variable couleur_trajectoire situé dans le Menu en fonction du choix de la couleur"""
        self.texte_couleur_trajectoire.config(fg=couleurTrajectoire.get())
        Menu.couleur_trajectoire = couleurTrajectoire.get()

    def changement_vitesse_execution(self, valeur_scale):
        """Fonction qui modifie la variable vitesse_execution situé dans le Menu en fonction du choix de la vitesse"""
        Menu.vitesse_execution = valeur_scale


# --Code--#
# Créer une fenêtre
root = tk.Tk()

# Créer la classe menu avec comme maître/parent 'root'
Menu(root).grid()

# La réception d'éléments commencent
root.mainloop()
