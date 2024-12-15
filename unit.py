import pygame
import random
from config import CELL_SIZE
from print_f import print_f
from collections import deque


class Unit:
    """Classe de base pour représenter une unité.

    Attributes:
        name (str): Nom de l'unité.
        max_hp (int): Points de vie maximum.
        hp (int): Points de vie actuels.
        attack (int): Force d'attaque.
        defense (int): Force de défense.
        range (int): Portée d'attaque.
        evasion (float): Taux d'évasion.
        image_path (str): Chemin de l'image de l'unité.
        x (int): Position x sur la carte.
        y (int): Position y sur la carte.
        team (str): Équipe de l'unité.
        image (pygame.Surface): Image de l'unité.
        is_visible (bool): Visibilité de l'unité.
        game (Game): Instance de la classe Game associée.
    """

    def __init__(self, name: str, hp: int, attack: int, defense: int, range: int, evasion: float, image_path: str):
        """Initialisation de l'unité."""
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.evasion = evasion
        self.has_acted = False
        self.x = 0
        self.y = 0
        self.team = None
        self.image = pygame.transform.scale(pygame.image.load(image_path), (CELL_SIZE, CELL_SIZE))
        self.is_visible = True
        self.game = None

    def set_game(self, game):
        """Associe cette unité à une instance de jeu."""
        self.game = game

    def draw(self, screen, current_turn):
        """Dessine l'unité et sa barre de vie si elle est visible."""
        if not self.is_visible and self.team != current_turn:
            return

        # Dessin de l'image de l'unité
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Détermine la couleur des contours
        border_color = None
        if self.team == current_turn:
            border_color = (0, 0, 255)  # Bleu pour les unités alliées
        elif self.is_visible:
            border_color = (255, 0, 0)  # Rouge pour les ennemis

        # Dessin des contours si nécessaire
        if border_color:
            pygame.draw.rect(
                screen,
                border_color,
                (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3
            )

        # Barre de vie
        bar_width = 5
        bar_height = CELL_SIZE
        bar_x = self.x * CELL_SIZE + CELL_SIZE
        bar_y = self.y * CELL_SIZE + (CELL_SIZE - bar_height) // 2

        # Calcul de la hauteur de la barre de vie
        hp_ratio = max(0, self.hp / self.max_hp)
        hp_fill_height = int(bar_height * hp_ratio)

        # Dessin de la barre de vie
        pygame.draw.rect(screen, (255, 0, 0), (bar_x - 5, bar_y, bar_width, bar_height))  # Fond rouge
        pygame.draw.rect(screen, (0, 255, 0), (bar_x - 5, bar_y + bar_height - hp_fill_height, bar_width, hp_fill_height))  # Remplissage vert

    def take_damage(self, amount: int, ignore_defense=False):
        """Applique des dégâts à l'unité avec gestion de l'évasion."""
        evasion = self.evasion
        if self.game.map[self.y][self.x].tile_type == "mud":
            evasion -= 0.1

        if random.random() < evasion:  # Évasion réussie
            if self.is_visible:
                print_f(f"{self.name} a esquivé l'attaque !")
            return

        # Calcul des dégâts
        damage_taken = amount if ignore_defense else max(0, amount - self.defense)
        self.hp -= damage_taken

        if self.is_visible:
            print_f(f"{self.name} prend {damage_taken} dégâts ! PV restant: {self.hp}")

    def can_move_to(self, x: int, y: int, map):
        """Vérifie si l'unité peut se déplacer à la position (x, y)."""
        if not (0 <= x < len(map[0]) and 0 <= y < len(map)):
            return False

        obstacles = {"rock", "wall", "water"}
        if self.name == "Mage":  # Le Mage peut traverser l'eau
            obstacles.remove("water")

        # Parcours en largeur pour trouver un chemin
        queue = deque([(self.x, self.y, 0)])
        visited = set()
        visited.add((self.x, self.y))

        while queue:
            current_x, current_y, steps = queue.popleft()
            if (current_x, current_y) == (x, y):
                return True
            if steps >= self.range + 1:
                continue

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = current_x + dx, current_y + dy

                if (0 <= next_x < len(map[0]) and
                    0 <= next_y < len(map) and
                    (next_x, next_y) not in visited):
                    tile = map[next_y][next_x]
                    if tile.tile_type not in obstacles:
                        queue.append((next_x, next_y, steps + 1))
                        visited.add((next_x, next_y))

        return False

    def attack_enemy(self, target):
        """Attaque une unité ennemie."""
        attack = self.attack
        if self.game.map[self.y][self.x].tile_type == "mud":
            attack *= 0.9  # Réduction des dégâts sur la boue
        print_f(f"{self.name} attaque {target.name} avec des dégâts de {attack}.")
        target.take_damage(attack)
