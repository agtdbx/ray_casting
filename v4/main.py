#Importation des librairies
from sre_parse import FLAGS
import pygame as pg
import sys
import time

from map import *
import perso as perso
import projection as projection

class Jeu:
    def __init__(self):
        """
        Cette méthode permet de définir les variables globales du programme
        """
        pg.init() # Initialisation de pygame

        infoObject = pg.display.Info() # On récupère la taille de l'écran
        #self.screen_size = ((infoObject.current_w, infoObject.current_h - 63)) # On soustrait la taille de la barre de tâche en bas
        self.screen_size = ((1920, 1080 - 63)) # On soustrait la taille de la barre de tâche en bas
        self.screen = pg.display.set_mode(self.screen_size, pg.RESIZABLE) # On créer la fenêtre

        self.clock = pg.time.Clock() # Permet d'imposer une limite de fps
        self.fps = 60

        self.runJeu = True

        self.lastTime = time.time()

        self.onlyGame = True

        self.size = 15
        self.map = init_map(64, 67)

        with open("save.txt", "r") as f:
            MAP = f.read()
            f.close()

        my_map = load_map(MAP)

        if (my_map != []):
            self.map = my_map

        self.perso = perso.Perso(self.size * 25, self.size * 20, self.size / 2, self.size)

        if (self.onlyGame):
            self.projection = projection.Projetcion(0, 0, self.screen_size[0], self.screen_size[1], self.size)
        else:
            self.projection = projection.Projetcion(48 * 20, 15, 48*20, 27*20, self.size)


    def run(self):
        """
        Cette méthode permet de définir la boucle principale du jeu
        """
        while self.runJeu: # Boucle pour le jeu
            self.input()
            self.tick()
            self.render()
            self.clock.tick(0)


    def input(self):
        """
        Cette méthode perrmet de gérer les entrées du programme (clic de sourie, appuie de touche)
        """
        for event in pg.event.get(): # On dit à notre programme de tout arrêter quand on appuie sur la croix en haut à droite
            if event.type == pg.QUIT:
                self.quit()
        self.key = pg.key.get_pressed()
        self.key2 = pg.mouse.get_pressed()


    def tick(self):
        """
        C'est dans cette méthode que vont s'effectuer tous les calculs des différents éléments de notre programme.
        Par exemple, quand on appuie sur la touche [Flèche gauche], c'est ici qu'on va calculer nle déplacement du joueur
        """
        delta = time.time() - self.lastTime
        self.lastTime = time.time()

        if (self.key[pg.K_ESCAPE] and self.onlyGame):
            self.quit()

        if self.key2[0] == 1:
            self.map = clic_on_map(self.map, pg.mouse.get_pos(), 0, self.perso.get_hitbox(), self.size)
        if self.key2[2] == 1:
            self.map = clic_on_map(self.map, pg.mouse.get_pos(), 1, self.perso.get_hitbox(), self.size)

        z = self.key[pg.K_z] or self.key[pg.K_UP] or self.key[pg.K_w]
        q = self.key[pg.K_q] or self.key[pg.K_LEFT] or self.key[pg.K_a]
        s = self.key[pg.K_s] or self.key[pg.K_DOWN]
        d = self.key[pg.K_d] or self.key[pg.K_RIGHT]

        self.projection.rotate_camera(pg.mouse.get_pos(), self.perso, self.key)

        self.perso.input(self.map, delta, z, q, s, d)
        self.perso.draw_ray(self.map)


    def render(self): # appel à d'autres fonctions self.render_*() pour l'affichage
        """
        C'est cette méthode qui va gérer l'affichage. Les élements du programme ont déjà bouger, maintenant il ne reste plus qu'à les afficher à l'écran
        """
        pg.display.set_caption(str(self.clock.get_fps()))
        self.screen.fill((0, 0, 0)) # On affiche un écran noir pour effacer tous les autres dessins du précédents passage

        if (not self.onlyGame):
            draw_map(self.map, self.screen, self.size)
            self.perso.draw(self.screen, True, True)
            draw_highlight_map(self.map, self.screen, self.perso.get_views(), self.size)

        self.projection.draw(self.screen, self.perso.get_views(), self.perso.get_rotation())

        pg.display.update() # On update, c'est à dire qu'on applique tous les changements précédents à la fenêtre


    def quit(self):
        """
        C'est la méthode, qui va s'executer lorsqu'on veut arrêter le programme
        """
        if (not self.onlyGame):
            with open("save.txt", "w") as f: # gère close() automatiquement
                f.write(str(get_save_map(self.map)))
                f.close()
        pg.quit() # On quite pygame
        sys.exit()


Jeu().run() # On lance le jeu
