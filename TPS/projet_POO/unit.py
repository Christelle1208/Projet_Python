import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

     def __init__(self, name, hp, attack, defense, speed, range):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range = range
        self.has_acted = False
        self.x = 0
        self.y = 0
        self.team = None
        self.color = None

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        # Choix des couleurs en fonction du type de l'unité
        match self.type_perso:
            case 'Tank':
                color = (0, 100, 200)  # Bleu foncé
            case 'Assassin':
                color = (255,0,0)  # Rouge
            case 'Mage':
                color = (225, 105, 160)  # Rose
            case 'Archer_poison':
                color = (135, 50, 215)  # Violet
            case 'Archer_electricite':
                color = (255, 255, 0)  # Jaune
            case _:
                color = (150, 150, 150)  # Gris pour les types inconnus

        # Encadrer l'unité sélectionnée
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dessiner la forme selon l'équipe
        center_x, center_y = self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2
        if self.team == 'player':
            # Joueur : Cercle
            pygame.draw.circle(screen, color, (center_x, center_y), CELL_SIZE // 3)
        else:
            # Ennemi : Triangle
            points = [
                (center_x, center_y - CELL_SIZE // 3),  # Sommet du triangle
                (center_x - CELL_SIZE // 3, center_y + CELL_SIZE // 3),  # Bas gauche
                (center_x + CELL_SIZE // 3, center_y + CELL_SIZE // 3)   # Bas droite
            ]
            pygame.draw.polygon(screen, color, points)
