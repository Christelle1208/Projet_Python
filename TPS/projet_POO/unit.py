import pygame
from config import CELL_SIZE

class Unit:
    def __init__(self, name, hp, attack, defense, range, image_path):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.has_acted = False
        self.x = 0
        self.y = 0
        self.team = None
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Scale image to fit the tile
        self.is_visible = True  # all units start visible

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def get_accessible_tiles(self, move_range):
        """Calcule les cases accessibles à partir de la position actuelle.

        Paramètres
        ----------
        move_range : int
            La distance maximale de déplacement.

        Retourne
        --------
        list[tuple[int, int]]
            Une liste de coordonnées (x, y) des cases accessibles.
        """
        tiles = []
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                if abs(dx) + abs(dy) <= move_range:  # Vérifier les déplacements séparément en x et en y
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:  # Vérifier les limites de la grille
                        tiles.append((new_x, new_y))
        return tiles


    def draw(self, screen):
        # Choix des couleurs en fonction du type de l'unité
        match self.name:
            case 'Tank':
                color = (0, 100, 200)  # Bleu foncé
            case 'Assassin':
                color = (255,0,0)  # Rouge
            case 'Mage':
                color = (225, 105, 160)  # Rose
            case 'Marksman':
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
