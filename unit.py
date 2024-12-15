import pygame
from config import CELL_SIZE
import random
from print_f import *
from collections import deque

class Unit:
    """Classe de base pour les unités.
    Attributes:
        name (str): nom de l'unité.
        max_hp (int): points de vie maximum.
        hp (int): points de vie actuels.
        attack (int): force d'attaque.
        defense (int): force de défense.
        range (int): portée d'attaque.
        evasion (float): taux d'évasion.
        image_path (str): chemin de l'image de l'unité.
        x (int): position x sur la carte.
        y (int): position y sur la carte.
        team (str): équipe de l'unité.
        image (pygame.Surface): image de l'unité.
        is_visible (bool): si l'unité est visible.
        game (Game): instance de la classe Game.
    """
    def __init__(self, name, hp, attack, defense, range, evasion, image_path):
        """Initialisation de l'unité.
        Args:
            name (str): nom de l'unité.
            hp (int): points de vie maximum.
            attack (int): force d'attaque.
            defense (int): force de défense.
            range (int): portée d'attaque.
            evasion (float): taux d'évasion.
            image_path (str): chemin de l'image de l'unité.
        """
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.range = range
        self.has_acted = False
        self.evasion = evasion
        self.x = 0
        self.y = 0
        self.team = None
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  
        self.is_visible = True
        self.game = None

    def set_game(self, game):
        """Association de cette unité à une instance de jeu."""
        self.game = game

    def draw(self, screen, current_turn):
        """Dessinez l'unité et sa barre HP si elle est visible."""
        if not self.is_visible and self.team != current_turn:
            return 

        # dessin de l'image du personnage
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        if self.team == current_turn:
            border_color = (0, 0, 255)  # bleu pour les unités alliées
        elif self.is_visible:
            border_color = (255, 0, 0)  # rouge pour l'ennemi
        else:
            border_color = None

        # dessine les contours des personnages
        if border_color:
            pygame.draw.rect(
                screen,
                border_color,
                (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3
            )

        # barre de vie
        bar_width = 5
        bar_height = CELL_SIZE
        bar_x = self.x * CELL_SIZE + CELL_SIZE
        bar_y = self.y * CELL_SIZE + (CELL_SIZE - bar_height) // 2

        # calcul de la barre proportionnelle pour les PV
        hp_ratio = max(0, self.hp / self.max_hp)
        hp_fill_height = int(bar_height * hp_ratio)

        # dessin de la barre de vie
        pygame.draw.rect(screen, (255, 0, 0), (bar_x - 5, bar_y, bar_width, bar_height))  
        pygame.draw.rect(screen, (0, 255, 0), (bar_x - 5, bar_y + bar_height - hp_fill_height, bar_width, hp_fill_height)) 

    def take_damage(self, amount, ignore_defense=False):
        """Calcule et applique les dégâts avec gestion de l'évasion."""
        evasion = self.evasion
        if self.game.map[self.y][self.x].tile_type == "mud":
            evasion -= 0.1
        if random.random() < evasion:  # vérification de l'évasion
            if self.is_visible:
                print_f(f"{self.name} a esquivé l'attaque !")
            return

        # dégâts si l'évasion échoue
        damage_taken = amount if ignore_defense else max(0, amount - self.defense)
        self.hp -= damage_taken

        if self.is_visible:
            print_f(f"{self.name} prend {amount} dégâts ! PV restant: {self.hp}")

    def can_move_to(self, x, y, map):
        """Vérifie si la position cible (x, y) est dans la portée de mouvement de l'unité."""
        if not (0 <= x < len(map[0]) and 0 <= y < len(map)):
            return False

        obstacles = {"rock", "wall", "water"}
        if self.name == "Mage":
            obstacles.remove("water")

        
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

                if (1 <= next_x < len(map[0]) - 1 and
                    1 <= next_y < len(map) - 1 and
                    (next_x, next_y) not in visited):
                    tile = map[next_y][next_x]
                    if tile.tile_type not in obstacles:
                        queue.append((next_x, next_y, steps + 1))
                        visited.add((next_x, next_y))

        return False

    def attack_enemy(self, target):
        """Attaque l'unité cible."""
        attack = self.attack
        if self.game.map[self.y][self.x].tile_type == "mud":
            attack *= 0.9
        print_f(f"{self.name} attaque {target.name} avec des dégâts de {attack}.")
        target.take_damage(attack)

