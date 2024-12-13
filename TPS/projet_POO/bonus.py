import pygame
import random
from config import CELL_SIZE  # Pour utiliser la taille des cellules du jeu

class Bonus:
    def __init__(self, x, y, effect_type):
        """
        Initialise un objet bonus.

        :param x: La position en x sur la carte.
        :param y: La position en y sur la carte.
        :param effect_type: Le type d'effet du bonus (ex: 'health', 'attack', 'defense').
        """
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.cell_size = cell_size
        # Charger les images des bonus en fonction de leur type
        self.images = {
            'health': pygame.image.load("assets/bonus_health.png"),
            'attack': pygame.image.load("assets/bonus_attack.png"),
            'defense': pygame.image.load("assets/bonus_defense.png"),
        }

        # L'image associée au type de bonus
        self.image = pygame.transform.scale(self.images[self.effect_type], (cell_size, cell_size))
        

    def apply_bonus(self, unit):
        """
        Applique l'effet du bonus à une unité.

        :param unit: L'unité qui collecte le bonus.
        """
        if self.effect_type == 'health':
            # Limite les PV à 100 pour éviter que l'unité ait plus de PV que sa capacité maximale
            unit.hp = min(100, unit.hp + 20)
        elif self.effect_type == 'attack':
            unit.attack += 5
        elif self.effect_type == 'defense':
            unit.defense += 5

        print(f"{unit.name} a reçu un bonus de {self.effect_type}!")

    def draw(self, screen):
        """
        Dessine le bonus sur la carte.

        :param screen: La surface Pygame sur laquelle dessiner le bonus.
        """
        screen.blit(self.image, (self.x * self.cell_size, self.y * self.cell_size))

    @staticmethod
    def generate_random_bonus(map_size, cell_size):
        """
        Génère un bonus aléatoire sur la carte.

        :param map_size: Taille de la carte (en cellules).
        :param cell_size: Taille d'une cellule.
        :return: Une instance de Bonus.
        """
        # Générer une position aléatoire dans les dimensions de la carte
        x = random.randint(0, map_size[0] - 1)
        y = random.randint(0, map_size[1] - 1)

        # Choisir un type de bonus aléatoire parmi les options possibles
        effect_type = random.choice(['health', 'attack', 'defense'])

        # Retourner une instance du bonus généré 
        return Bonus(x, y, effect_type, cell_size)

