import pygame
from print_f import *

class Ability:
    """classe habilité."""
    def __init__(self, name):
        self.name = name

    def activate(self, game, user, target_pos):
        """activation de l'habilité."""
        pass


class Bomb(Ability):
    """habilité bombe."""
    def __init__(self):
        super().__init__("Bomb")

    def activate(self, game, user, target_pos):
        center_x, center_y = target_pos
        
        # calcule les tiles affectées Calculate affected tiles based on the cursor position
        affected_tiles = [
            (center_x + dx, center_y + dy)
            for dx in range(-5, 6)
            for dy in range(-5, 6)
            if (
                1 <= center_x + dx < len(game.map[0]) - 1 and
                1 <= center_y + dy < len(game.map) - 1 and
                abs(dx) + abs(dy) <= 3
            )
        ]